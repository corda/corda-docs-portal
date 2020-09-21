---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    identifier: corda-enterprise-4-5-cordapps-flows
    name: "Writing CorDapp flows"
    parent: corda-enterprise-4-5-cordapps
tags:
- api
- flows
title: Writing CorDapp Flows
weight: 8
---




# Writing CorDapp Flows

Before we discuss the details of the flow API, consider what a standard flow may look like.

Imagine a flow for agreeing a basic ledger update between Alice and Bob. This flow will have two sides:

* An `Initiator` side, that will initiate the request to update the ledger
* A `Responder` side, that will respond to the request to update the ledger

## Initiator

In our flow, the Initiator flow class will be doing the majority of the work, the iniator will, in order:

**Part 1 - Building the transaction**

* Choose a notary for the transaction
* Create a transaction builder
* Extract any input states from the vault and add them to the builder
* Create any output states and add them to the builder
* Add any commands, attachments and time-window to the builder

**Part 2 - Sign the transaction**

* Sign the transaction builder
* Convert the builder to a signed transaction

**Part 3 - Verify the transaction**

* Verify the transaction by running its contracts

**Part 4 - Gather the counterparty’s signature**

* Send the transaction to the responding counterparty
* Wait to receive back the responding counterparty’s signature
* Add the responding counterparty’s signature to the transaction
* Verify the transaction’s signatures

**Part 5 - Finalize the transaction**

* Send the transaction to the notary
* Wait to receive back the notarised transaction
* Record the transaction locally
* Store any relevant states in the vault
* Send the transaction to the counterparty for recording

We can visualize the work performed by initiator as follows:

![flow overview](../resources/flow-overview.png "flow overview")

## Responder

To respond to these actions, the responder takes the following steps:

**Part 1 - Sign the transaction**

* Receive the transaction from the counterparty
* Verify the transaction’s existing signatures
* Verify the transaction by running its contracts
* Generate a signature over the transaction
* Send the signature back to the counterparty

**Part 2 - Record the transaction**

* Receive the notarised transaction from the initiator
* Record the transaction locally
* Store any relevant states in the vault

## Understand the FlowLogic class

In practice, a flow is implemented as one or more communicating `FlowLogic` subclasses. The `FlowLogic`
subclass’s constructor can take any number of arguments of any type. The generic of `FlowLogic` (e.g.
`FlowLogic<SignedTransaction>`) indicates the flow’s return type.

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}

```kotlin
class Initiator(val arg1: Boolean,
                val arg2: Int,
                val counterparty: Party): FlowLogic<SignedTransaction>() { }

class Responder(val otherParty: Party) : FlowLogic<Unit>() { }
```

{{% /tab %}}

{{% tab name="java" %}}

```java
public static class Initiator extends FlowLogic<SignedTransaction> {
    private final boolean arg1;
    private final int arg2;
    private final Party counterparty;

    public Initiator(boolean arg1, int arg2, Party counterparty) {
        this.arg1 = arg1;
        this.arg2 = arg2;
        this.counterparty = counterparty;
    }

}

public static class Responder extends FlowLogic<Void> { }
```

{{% /tab %}}

{{< /tabs >}}

### FlowLogic annotations

Any flow from which you want to initiate other flows must be annotated with the `@InitiatingFlow` annotation.
Additionally, if you wish to start the flow via RPC, you must annotate it with the `@StartableByRPC` annotation:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}

```kotlin
@InitiatingFlow
@StartableByRPC
class Initiator(): FlowLogic<Unit>() { }
```

{{% /tab %}}

{{% tab name="java" %}}

```java
@InitiatingFlow
@StartableByRPC
public static class Initiator extends FlowLogic<Unit> { }
```

{{% /tab %}}

{{< /tabs >}}

Meanwhile, any flow that responds to a message from another flow must be annotated with the `@InitiatedBy` annotation.
`@InitiatedBy` takes the class of the flow it is responding to as its single parameter:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}

```kotlin
@InitiatedBy(Initiator::class)
class Responder(val otherSideSession: FlowSession) : FlowLogic<Unit>() { }
```

{{% /tab %}}

{{% tab name="java" %}}

```java
@InitiatedBy(Initiator.class)
public static class Responder extends FlowLogic<Void> { }
```

{{% /tab %}}

{{< /tabs >}}

Additionally, any flow that is started by a `SchedulableState` must be annotated with the `@SchedulableFlow`
annotation.

### Call

Each `FlowLogic` subclass must override `FlowLogic.call()`, which describes the actions it will take as part of
the flow. For example, the actions of the initiator’s side of the flow would be defined in `Initiator.call`, and the
actions of the responder’s side of the flow would be defined in `Responder.call`.

In order for nodes to be able to run multiple flows concurrently, and to allow flows to survive node upgrades and
restarts, flows need to be checkpointable and serializable to disk. This is achieved by marking `FlowLogic.call()`,
as well as any function invoked from within `FlowLogic.call()`, with an `@Suspendable` annotation.

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}

```kotlin
class Initiator(val counterparty: Party): FlowLogic<Unit>() {
    @Suspendable
    override fun call() { }
}
```

{{% /tab %}}

{{% tab name="java" %}}

```java
public static class InitiatorFlow extends FlowLogic<Void> {
    private final Party counterparty;

    public Initiator(Party counterparty) {
        this.counterparty = counterparty;
    }

    @Suspendable
    @Override
    public Void call() throws FlowException { }

}
```

{{% /tab %}}

{{< /tabs >}}

### ServiceHub

Within `FlowLogic.call`, the flow developer has access to the node’s `ServiceHub`, which provides access to the
various services the node provides. We will use the `ServiceHub` extensively in the examples that follow. You can
also see [Accessing node services](api-service-hub.md) for information about the services the `ServiceHub` offers.

### Common flow tasks

There are a number of common tasks that you will need to perform within `FlowLogic.call` in order to agree ledger
updates. This section details the API for common tasks.

## Transaction building

The majority of the work performed during a flow will be to build, verify and sign a transaction. This is covered
in [Understanding transactions](api-transactions.md).

## Extracting states from the vault

When building a transaction, you’ll often need to extract the states you wish to consume from the vault. This is
covered in [Writing vault queries](api-vault-query.md).

## Retrieving information about other nodes

We can retrieve information about other nodes on the network and the services they offer using
`ServiceHub.networkMapCache`.

### Notaries

Remember that a transaction generally needs a notary to:

* Prevent double-spends if the transaction has inputs
* Serve as a timestamping authority if the transaction has a time-window

A notary can be retrieved from the network map as follows:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}

```kotlin
val notaryName: CordaX500Name = CordaX500Name(
        organisation = "Notary Service",
        locality = "London",
        country = "GB")
val specificNotary: Party = serviceHub.networkMapCache.getNotary(notaryName)!!
// Alternatively, we can pick an arbitrary notary from the notary
// list. However, it is always preferable to specify the notary
// explicitly, as the notary list might change when new notaries are
// introduced, or old ones decommissioned.
val firstNotary: Party = serviceHub.networkMapCache.notaryIdentities.first()

```

{{% /tab %}}

{{% tab name="java" %}}

```java
CordaX500Name notaryName = new CordaX500Name("Notary Service", "London", "GB");
Party specificNotary = Objects.requireNonNull(getServiceHub().getNetworkMapCache().getNotary(notaryName));
// Alternatively, we can pick an arbitrary notary from the notary
// list. However, it is always preferable to specify the notary
// explicitly, as the notary list might change when new notaries are
// introduced, or old ones decommissioned.
Party firstNotary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0);

```

{{% /tab %}}

{{< /tabs >}}

### Specific counterparties

We can also use the network map to retrieve a specific counterparty:

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}

```kotlin
val counterpartyName: CordaX500Name = CordaX500Name(
        organisation = "NodeA",
        locality = "London",
        country = "GB")
val namedCounterparty: Party = serviceHub.identityService.wellKnownPartyFromX500Name(counterpartyName) ?:
        throw IllegalArgumentException("Couldn't find counterparty for NodeA in identity service")
val keyedCounterparty: Party = serviceHub.identityService.partyFromKey(dummyPubKey) ?:
        throw IllegalArgumentException("Couldn't find counterparty with key: $dummyPubKey in identity service")

```

{{% /tab %}}

{{% tab name="java" %}}

```java
CordaX500Name counterPartyName = new CordaX500Name("NodeA", "London", "GB");
Party namedCounterparty = getServiceHub().getIdentityService().wellKnownPartyFromX500Name(counterPartyName);
Party keyedCounterparty = getServiceHub().getIdentityService().partyFromKey(dummyPubKey);

```

{{% /tab %}}

{{< /tabs >}}

## Communication between parties

In order to create a communication session between your initiator flow and the receiver flow you must call
`initiateFlow(party: Party): FlowSession`

`FlowSession` instances in turn provide three functions:

* `send(payload: Any)`
  * Sends the `payload` object
* `receive(receiveType: Class<R>): R`
  * Receives an object of type `receiveType`
* `sendAndReceive(receiveType: Class<R>, payload: Any): R`
  * Sends the `payload` object and receives an object of type `receiveType` back

In addition ``FlowLogic`` provides functions that can receive messages from multiple sessions and send messages to multiple sessions:

* `receiveAllMap(sessions: Map<FlowSession, Class<out Any>>): Map<FlowSession, UntrustworthyData<Any>>`
  * Receives from all `FlowSession` objects specified in the passed in map. The received types may differ.
* `receiveAll(receiveType: Class<R>, sessions: List<FlowSession>): List<UntrustworthyData<R>>`
  * Receives from all `FlowSession` objects specified in the passed in list. The received types must be the same.
* `sendAll(payload: Any, sessions: Set<FlowSession>)`
  * Sends the ``payload`` object to all the provided `FlowSession`.
* `sendAllMap(payloadsPerSession: Map<FlowSession, Any>)`
  * Sends a potentially different payload to each `FlowSession`, as specified by the provided `payloadsPerSession`.

{{% note %}}
It's more efficient to call `sendAndReceive` instead of calling `send` and then `receive`. It's also more efficient to call `sendAll / receiveAll` instead of multiple `send / receive` respectively.
{{% /note %}}

### InitiateFlow

`initiateFlow` creates a communication session with the passed in `Party`.

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}

```kotlin
val counterpartySession: FlowSession = initiateFlow(counterparty)

```

{{% /tab %}}

{{% tab name="java" %}}

```java
FlowSession counterpartySession = initiateFlow(counterparty);

```

{{% /tab %}}

{{< /tabs >}}

Note that at the time of call to this function no actual communication is done, this is deferred to the first
send/receive, at which point the counterparty will either:

* Ignore the message if they are not registered to respond to messages from this flow.
* Start the flow they have registered to respond to this flow.

### Send

Once we have a `FlowSession` object we can send arbitrary data to a counterparty:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}

```kotlin
counterpartySession.send(Any())

```

{{% /tab %}}

{{% tab name="java" %}}

```java
counterpartySession.send(new Object());

```

{{% /tab %}}

{{< /tabs >}}

The flow on the other side must eventually reach a corresponding `receive` call to get this message.

### Receive

We can also wait to receive arbitrary data of a specific type from a counterparty. Again, this implies a corresponding
`send` call in the counterparty’s flow. A few scenarios:

* We never receive a message back. In the current design, the flow is paused until the node’s owner kills the flow.
* Instead of sending a message back, the counterparty throws a `FlowException`. This exception is propagated back
to us, and we can use the error message to establish what happened.
* We receive a message back, but it’s of the wrong type. In this case, a `FlowException` is thrown.
* We receive back a message of the correct type. All is good.

Upon calling `receive` (or `sendAndReceive`), the `FlowLogic` is suspended until it receives a response.

We receive the data wrapped in an `UntrustworthyData` instance. This is a reminder that the data we receive may not
be what it appears to be! We must unwrap the `UntrustworthyData` using a lambda:

{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}

```kotlin
val packet1: UntrustworthyData<Int> = counterpartySession.receive<Int>()
val int: Int = packet1.unwrap { data ->
    // Perform checking on the object received.
    // T O D O: Check the received object.
    // Return the object.
    data
}

```

{{% /tab %}}

{{% tab name="java" %}}

```java
UntrustworthyData<Integer> packet1 = counterpartySession.receive(Integer.class);
Integer integer = packet1.unwrap(data -> {
    // Perform checking on the object received.
    // T O D O: Check the received object.
    // Return the object.
    return data;
});

```

{{% /tab %}}

{{< /tabs >}}

We’re not limited to sending to and receiving from a single counterparty. A flow can send messages to as many parties
as it likes, and each party can invoke a different response flow:

{{< tabs name="tabs-10" >}}
{{% tab name="kotlin" %}}

```kotlin
val regulatorSession: FlowSession = initiateFlow(regulator)
regulatorSession.send(Any())
val packet3: UntrustworthyData<Any> = regulatorSession.receive<Any>()

```

{{% /tab %}}

{{% tab name="java" %}}

```java
FlowSession regulatorSession = initiateFlow(regulator);
regulatorSession.send(new Object());
UntrustworthyData<Object> packet3 = regulatorSession.receive(Object.class);

```

{{% /tab %}}

{{< /tabs >}}

{{< warning >}}
If you initiate several flows from the same `@InitiatingFlow` flow then on the receiving side you must be
prepared to be initiated by any of the corresponding `initiateFlow()` calls! A good way of handling this ambiguity
is to send as a first message a “role” message to the initiated flow, indicating which part of the initiating flow
the rest of the counter-flow should conform to. For example send an enum, and on the other side start with a switch
statement.

{{< /warning >}}

### SendAndReceive

We can also use a single call to send data to a counterparty and wait to receive data of a specific type back. The
type of data sent doesn’t need to match the type of the data received back:

{{< tabs name="tabs-11" >}}
{{% tab name="kotlin" %}}

```kotlin
val packet2: UntrustworthyData<Boolean> = counterpartySession.sendAndReceive<Boolean>("You can send and receive any class!")
val boolean: Boolean = packet2.unwrap { data ->
    // Perform checking on the object received.
    // T O D O: Check the received object.
    // Return the object.
    data
}

```

{{% /tab %}}

{{% tab name="java" %}}

```java
UntrustworthyData<Boolean> packet2 = counterpartySession.sendAndReceive(Boolean.class, "You can send and receive any class!");
Boolean bool = packet2.unwrap(data -> {
    // Perform checking on the object received.
    // T O D O: Check the received object.
    // Return the object.
    return data;
});

```

{{% /tab %}}

{{< /tabs >}}

### Counterparty response

Suppose we’re now on the `Responder` side of the flow. We just received the following series of messages from the
`Initiator`:

* They sent us an `Any` instance
* They waited to receive an `Integer` instance back
* They sent a `String` instance and waited to receive a `Boolean` instance back

Our side of the flow must mirror these calls. We could do this as follows:

{{< tabs name="tabs-12" >}}
{{% tab name="kotlin" %}}

```kotlin
val any: Any = counterpartySession.receive<Any>().unwrap { data -> data }
val string: String = counterpartySession.sendAndReceive<String>(99).unwrap { data -> data }
counterpartySession.send(true)

```

{{% /tab %}}

{{% tab name="java" %}}

```java
Object obj = counterpartySession.receive(Object.class).unwrap(data -> data);
String string = counterpartySession.sendAndReceive(String.class, 99).unwrap(data -> data);
counterpartySession.send(true);

```

{{% /tab %}}

{{< /tabs >}}

## Subflows

Subflows are pieces of reusable flows that may be run by calling `FlowLogic.subFlow`. There are two broad categories
of subflows, inlined and initiating ones. The main difference lies in the counter-flow’s starting method, initiating
ones initiate counter-flows automatically, while inlined ones expect some parent counter-flow to run the inlined
counterpart.

### Inlined subflows

Inlined subflows inherit their calling flow’s type when initiating a new session with a counterparty. For example, say
we have flow A calling an inlined subflow B, which in turn initiates a session with a party. The FlowLogic type used to
determine which counter-flow should be kicked off will be A, not B. Note that this means that the other side of this
inlined flow must therefore be implemented explicitly in the kicked off flow as well. This may be done by calling a
matching inlined counter-flow, or by implementing the other side explicitly in the kicked off parent flow.

An example of such a flow is `CollectSignaturesFlow`. It has a counter-flow `SignTransactionFlow` that isn’t
annotated with `InitiatedBy`. This is because both of these flows are inlined; the kick-off relationship will be
defined by the parent flows calling `CollectSignaturesFlow` and `SignTransactionFlow`.

In the code inlined subflows appear as regular `FlowLogic` instances, *without* either of the `@InitiatingFlow` or
`@InitiatedBy` annotation.

{{< note >}}
Inlined flows aren’t versioned; they inherit their parent flow’s version.

{{< /note >}}

### Initiating subflows

Initiating subflows are ones annotated with the `@InitiatingFlow` annotation. When such a flow initiates a session its
type will be used to determine which `@InitiatedBy` flow to kick off on the counterparty.

An example is the `@InitiatingFlow InitiatorFlow`/`@InitiatedBy ResponderFlow` flow pair in the `FlowCookbook`.

{{< note >}}
Initiating flows are versioned separately from their parents.

{{< /note >}}
{{< note >}}
The only exception to this rule is `FinalityFlow` which is annotated with `@InitiatingFlow` but is an inlined flow. This flow
was previously initiating and the annotation exists to maintain backwards compatibility with old code.

{{< /note >}}

#### Core initiating subflows

Corda-provided initiating subflows are a little different to standard ones as they are versioned together with the
platform, and their initiated counter-flows are registered explicitly, so there is no need for the `InitiatedBy`
annotation.

### Library flows

Corda installs four initiating subflow pairs on each node by default:

* `NotaryChangeFlow`/`NotaryChangeHandler`, which should be used to change a state’s notary
* `ContractUpgradeFlow.Initiate`/`ContractUpgradeHandler`, which should be used to change a state’s contract
* `SwapIdentitiesFlow`/`SwapIdentitiesHandler`, which is used to exchange confidential identities with a
counterparty

{{< warning >}}
`SwapIdentitiesFlow`/`SwapIdentitiesHandler` are only installed if the `confidential-identities` module
is included. The `confidential-identities` module  is still not stabilised, so the
`SwapIdentitiesFlow`/`SwapIdentitiesHandler` API may change in future releases. See [API stability guarantees](api-stability-guarantees.md).

{{< /warning >}}

Corda also provides a number of built-in inlined subflows that should be used for handling common tasks. The most
important are:

* `FinalityFlow` which is used to notarise, record locally and then broadcast a signed transaction to its participants
and any extra parties.
* `ReceiveFinalityFlow` to receive these notarised transactions from the `FinalityFlow` sender and record locally.
* `CollectSignaturesFlow` , which should be used to collect a transaction’s required signatures
* `SendTransactionFlow` , which should be used to send a signed transaction if it needed to be resolved on
the other side.
* `ReceiveTransactionFlow`, which should be used receive a signed transaction

Let’s look at some of these flows in more detail.

### FinalityFlow

`FinalityFlow` allows us to notarise the transaction and get it recorded in the vault of the participants of all
the transaction’s states:

{{< tabs name="tabs-13" >}}
{{% tab name="kotlin" %}}

```kotlin
val notarisedTx1: SignedTransaction = subFlow(FinalityFlow(fullySignedTx, listOf(counterpartySession), FINALISATION.childProgressTracker()))

```

{{% /tab %}}

{{% tab name="java" %}}

```java
SignedTransaction notarisedTx1 = subFlow(new FinalityFlow(fullySignedTx, singleton(counterpartySession), FINALISATION.childProgressTracker()));

```

{{% /tab %}}

{{< /tabs >}}

We can also choose to send the transaction to additional parties who aren’t one of the state’s participants:

{{< tabs name="tabs-14" >}}
{{% tab name="kotlin" %}}

```kotlin
val partySessions: List<FlowSession> = listOf(counterpartySession, initiateFlow(regulator))
val notarisedTx2: SignedTransaction = subFlow(FinalityFlow(fullySignedTx, partySessions, FINALISATION.childProgressTracker()))

```

{{% /tab %}}

{{% tab name="java" %}}

```java
List<FlowSession> partySessions = Arrays.asList(counterpartySession, initiateFlow(regulator));
SignedTransaction notarisedTx2 = subFlow(new FinalityFlow(fullySignedTx, partySessions, FINALISATION.childProgressTracker()));

```

{{% /tab %}}

{{< /tabs >}}

Only one party has to call `FinalityFlow` for a given transaction to be recorded by all participants. It **must not**
be called by every participant. Instead, every other particpant **must** call `ReceiveFinalityFlow` in their responder
flow to receive the transaction:

{{< tabs name="tabs-15" >}}
{{% tab name="kotlin" %}}

```kotlin
subFlow(ReceiveFinalityFlow(counterpartySession, expectedTxId = idOfTxWeSigned))

```

{{% /tab %}}

{{% tab name="java" %}}

```java
subFlow(new ReceiveFinalityFlow(counterpartySession, idOfTxWeSigned));

```

{{% /tab %}}

{{< /tabs >}}

`idOfTxWeSigned` is an optional parameter used to confirm that we got the right transaction. It comes from using `SignTransactionFlow`
which is described in the error handling behaviour section.

In some cases, transactions will only have one participant, the initiator. In these instances, there are no other
parties to send the transactions to during `FinalityFlow`. In these cases the `counterpartySession` list must exist,
but be empty.

Once a transaction has been notarised and its input states consumed by the flow initiator (eg. sender), should the participant(s) receiving the
transaction fail to verify it, or the receiving flow (the finality handler) fails due to some other error, we then have a scenario where not
all parties have the correct up to date view of the ledger (a condition where eventual consistency between participants takes longer than is
normally the case under Corda’s [eventual consistency model](https://en.wikipedia.org/wiki/Eventual_consistency)). To recover from this scenario,
the receiver’s finality handler will automatically be sent to the node-flow-hospital where it’s suspended and retried from its last checkpoint
upon node restart, or according to other conditional retry rules explained in [flow hospital runtime behaviour](../node/node-flow-hospital.md#flow-hospital-runtime).
This gives the node operator the opportunity to recover from the error. Until the issue is resolved the node will continue to retry the flow
on each startup. Upon successful completion by the receiver’s finality flow, the ledger will become fully consistent once again.

{{< warning >}}
It’s possible to forcibly terminate the erroring finality handler using the `killFlow` RPC but at the risk of an inconsistent view of the ledger.

{{< /warning >}}

{{< note >}}
A future release will allow retrying hospitalised flows without restarting the node, i.e. via RPC.

{{< /note >}}

### CollectSignaturesFlow/SignTransactionFlow

The list of parties who need to sign a transaction is dictated by the transaction’s commands. Once we’ve signed a
transaction ourselves, we can automatically gather the signatures of the other required signers using
`CollectSignaturesFlow`:

{{< tabs name="tabs-16" >}}
{{% tab name="kotlin" %}}

```kotlin
val fullySignedTx: SignedTransaction = subFlow(CollectSignaturesFlow(twiceSignedTx, setOf(counterpartySession, regulatorSession), SIGS_GATHERING.childProgressTracker()))

```

{{% /tab %}}

{{% tab name="java" %}}

```java
SignedTransaction fullySignedTx = subFlow(new CollectSignaturesFlow(twiceSignedTx, emptySet(), SIGS_GATHERING.childProgressTracker()));

```

{{% /tab %}}

{{< /tabs >}}

Each required signer will need to respond by invoking its own `SignTransactionFlow` subclass to check the
transaction (by implementing the `checkTransaction` method) and provide their signature if they are satisfied:

{{< tabs name="tabs-17" >}}
{{% tab name="kotlin" %}}

```kotlin
val signTransactionFlow: SignTransactionFlow = object : SignTransactionFlow(counterpartySession) {
    override fun checkTransaction(stx: SignedTransaction) = requireThat {
        // Any additional checking we see fit...
        val outputState = stx.tx.outputsOfType<DummyState>().single()
        require(outputState.magicNumber == 777)
    }
}

val idOfTxWeSigned = subFlow(signTransactionFlow).id

```

{{% /tab %}}

{{% tab name="java" %}}

```java
class SignTxFlow extends SignTransactionFlow {
    private SignTxFlow(FlowSession otherSession, ProgressTracker progressTracker) {
        super(otherSession, progressTracker);
    }

    @Override
    protected void checkTransaction(@NotNull SignedTransaction stx) {
        requireThat(require -> {
            // Any additional checking we see fit...
            DummyState outputState = (DummyState) stx.getTx().getOutputs().get(0).getData();
            checkArgument(outputState.getMagicNumber() == 777);
            return null;
        });
    }
}

SecureHash idOfTxWeSigned = subFlow(new SignTxFlow(counterpartySession, SignTransactionFlow.tracker())).getId();

```

{{% /tab %}}

{{< /tabs >}}

Types of things to check include:

* Ensuring that the transaction received is the expected type, i.e. has the expected type of inputs and outputs
* Checking that the properties of the outputs are expected, this is in the absence of integrating reference
data sources to facilitate this
* Checking that the transaction is not incorrectly spending (perhaps maliciously) asset states, as potentially
the transaction creator has access to some of signer’s state references

### SendTransactionFlow/ReceiveTransactionFlow

Verifying a transaction received from a counterparty also requires verification of every transaction in its
dependency chain. This means the receiving party needs to be able to ask the sender all the details of the chain.
The sender will use `SendTransactionFlow` for sending the transaction and then for processing all subsequent
transaction data vending requests as the receiver walks the dependency chain using `ReceiveTransactionFlow`:

{{< tabs name="tabs-18" >}}
{{% tab name="kotlin" %}}

```kotlin
subFlow(SendTransactionFlow(counterpartySession, twiceSignedTx))

// Optional request verification to further restrict data access.
subFlow(object : SendTransactionFlow(counterpartySession, twiceSignedTx) {
    override fun verifyDataRequest(dataRequest: FetchDataFlow.Request.Data) {
        // Extra request verification.
    }
})

```

{{% /tab %}}

{{% tab name="java" %}}

```java
subFlow(new SendTransactionFlow(counterpartySession, twiceSignedTx));

// Optional request verification to further restrict data access.
subFlow(new SendTransactionFlow(counterpartySession, twiceSignedTx) {
    @Override
    protected void verifyDataRequest(@NotNull FetchDataFlow.Request.Data dataRequest) {
        // Extra request verification.
    }
});

```

{{% /tab %}}

{{< /tabs >}}

We can receive the transaction using `ReceiveTransactionFlow`, which will automatically download all the
dependencies and verify the transaction:

{{< tabs name="tabs-19" >}}
{{% tab name="kotlin" %}}

```kotlin
val verifiedTransaction = subFlow(ReceiveTransactionFlow(counterpartySession))

```

{{% /tab %}}

{{% tab name="java" %}}

```java
SignedTransaction verifiedTransaction = subFlow(new ReceiveTransactionFlow(counterpartySession));

```

{{% /tab %}}

{{< /tabs >}}

We can also send and receive a `StateAndRef` dependency chain and automatically resolve its dependencies:

{{< tabs name="tabs-20" >}}
{{% tab name="kotlin" %}}

```kotlin
subFlow(SendStateAndRefFlow(counterpartySession, dummyStates))

// On the receive side ...
val resolvedStateAndRef = subFlow(ReceiveStateAndRefFlow<DummyState>(counterpartySession))

```

{{% /tab %}}

{{% tab name="java" %}}

```java
subFlow(new SendStateAndRefFlow(counterpartySession, dummyStates));

// On the receive side ...
List<StateAndRef<DummyState>> resolvedStateAndRef = subFlow(new ReceiveStateAndRefFlow<>(counterpartySession));

```

{{% /tab %}}

{{< /tabs >}}

#### Why inlined subflows

Inlined subflows provide a way to share commonly used flow code *while forcing users to create a parent flow*. Take for
example `CollectSignaturesFlow`. Say we made it an initiating flow that automatically kicks off
`SignTransactionFlow` that signs the transaction. This would mean malicious nodes can just send any old transaction to
us using `CollectSignaturesFlow` and we would automatically sign it!

By making this pair of flows inlined we provide control to the user over whether to sign the transaction or not by
forcing them to nest it in their own parent flows.

In general if you’re writing a subflow the decision of whether you should make it initiating should depend on whether
the counter-flow needs broader context to achieve its goal.

## FlowException

Suppose a node throws an exception while running a flow. Any counterparty flows waiting for a message from the node
(i.e. as part of a call to `receive` or `sendAndReceive`) will be notified that the flow has unexpectedly
ended and will themselves end. However, the exception thrown will not be propagated back to the counterparties.

If you wish to notify any waiting counterparties of the cause of the exception, you can do so by throwing a
`FlowException`:

The flow framework will automatically propagate the `FlowException` back to the waiting counterparties.

There are many scenarios in which throwing a `FlowException` would be appropriate:

* A transaction doesn’t `verify()`
* A transaction’s signatures are invalid
* The transaction does not match the parameters of the deal as discussed
* You are reneging on a deal

Below is an example using `FlowException`:

```kotlin
@InitiatingFlow
class SendMoneyFlow(private val moneyRecipient: Party) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val money = Money(10.0, USD)
        try {
            initiateFlow(moneyRecipient).sendAndReceive<Unit>(money)
        } catch (e: FlowException) {
            if (e.cause is WrongCurrencyException) {
                log.info(e.message, e)
            }
        }
    }
}

@InitiatedBy(SendMoneyFlow::class)
class ReceiveMoneyFlow(private val moneySender: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val receivedMoney = moneySender.receive<Money>().unwrap { it }
        if (receivedMoney.currency != GBP) {
            // Wrap a thrown Exception with a FlowException for the counter party to receive it.
            throw FlowException(WrongCurrencyException("I only accept GBP, sorry!"))
        }
    }
}

class WrongCurrencyException(message: String) : CordaRuntimeException(message)
```

## HospitalizeFlowException

Some operations can fail intermittently and will succeed if they are tried again at a later time. Flows have the ability to halt their
execution in such situations. By throwing a `HospitalizeFlowException` a flow will stop and retry at a later time (on the next node restart).

A `HospitalizeFlowException` can be defined in various ways:

{{< note >}}
If a `HospitalizeFlowException` is wrapping or extending an exception already being handled by the node-flow-hospital, the outcome of a flow may change. For example, the flow
could instantly retry or terminate if a critical error occurred.

{{< /note >}}
{{< note >}}
`HospitalizeFlowException` can be extended for customized exceptions. These exceptions will be treated in the same way when thrown.

{{< /note >}}
Below is an example of a flow that should retry again in the future if an error occurs:

```kotlin
class TryAccessServiceFlow(): FlowLogic<Unit>() {
    override fun call() {
        try {
            val code = serviceHub.cordaService(HTTPService::class.java).get() // throws UnknownHostException.
        } catch (e: UnknownHostException) {
            // Accessing the service failed! It might be offline. Let's hospitalize this flow, and have it retry again on next node startup.
            throw HospitalizeFlowException("Service might be offline!", e)
        }
    }
}
```

## ProgressTracker

We can give our flow a progress tracker. This allows us to see the flow’s progress visually in our node’s CRaSH shell.

To provide a progress tracker, we have to override `FlowLogic.progressTracker` in our flow:

{{< tabs name="tabs-21" >}}
{{% tab name="kotlin" %}}

```kotlin
companion object {
    object ID_OTHER_NODES : Step("Identifying other nodes on the network.")
    object SENDING_AND_RECEIVING_DATA : Step("Sending data between parties.")
    object EXTRACTING_VAULT_STATES : Step("Extracting states from the vault.")
    object OTHER_TX_COMPONENTS : Step("Gathering a transaction's other components.")
    object TX_BUILDING : Step("Building a transaction.")
    object TX_SIGNING : Step("Signing a transaction.")
    object TX_VERIFICATION : Step("Verifying a transaction.")
    object SIGS_GATHERING : Step("Gathering a transaction's signatures.") {
        // Wiring up a child progress tracker allows us to see the
        // subflow's progress steps in our flow's progress tracker.
        override fun childProgressTracker() = CollectSignaturesFlow.tracker()
    }

    object VERIFYING_SIGS : Step("Verifying a transaction's signatures.")
    object FINALISATION : Step("Finalising a transaction.") {
        override fun childProgressTracker() = FinalityFlow.tracker()
    }

    fun tracker() = ProgressTracker(
            ID_OTHER_NODES,
            SENDING_AND_RECEIVING_DATA,
            EXTRACTING_VAULT_STATES,
            OTHER_TX_COMPONENTS,
            TX_BUILDING,
            TX_SIGNING,
            TX_VERIFICATION,
            SIGS_GATHERING,
            VERIFYING_SIGS,
            FINALISATION
    )
}

```

{{% /tab %}}

{{% tab name="java" %}}

```java
private static final Step ID_OTHER_NODES = new Step("Identifying other nodes on the network.");
private static final Step SENDING_AND_RECEIVING_DATA = new Step("Sending data between parties.");
private static final Step EXTRACTING_VAULT_STATES = new Step("Extracting states from the vault.");
private static final Step OTHER_TX_COMPONENTS = new Step("Gathering a transaction's other components.");
private static final Step TX_BUILDING = new Step("Building a transaction.");
private static final Step TX_SIGNING = new Step("Signing a transaction.");
private static final Step TX_VERIFICATION = new Step("Verifying a transaction.");
private static final Step SIGS_GATHERING = new Step("Gathering a transaction's signatures.") {
    // Wiring up a child progress tracker allows us to see the
    // subflow's progress steps in our flow's progress tracker.
    @Override
    public ProgressTracker childProgressTracker() {
        return CollectSignaturesFlow.tracker();
    }
};
private static final Step VERIFYING_SIGS = new Step("Verifying a transaction's signatures.");
private static final Step FINALISATION = new Step("Finalising a transaction.") {
    @Override
    public ProgressTracker childProgressTracker() {
        return FinalityFlow.tracker();
    }
};

private final ProgressTracker progressTracker = new ProgressTracker(
        ID_OTHER_NODES,
        SENDING_AND_RECEIVING_DATA,
        EXTRACTING_VAULT_STATES,
        OTHER_TX_COMPONENTS,
        TX_BUILDING,
        TX_SIGNING,
        TX_VERIFICATION,
        SIGS_GATHERING,
        FINALISATION
);

```

{{% /tab %}}

{{< /tabs >}}

We then update the progress tracker’s current step as we progress through the flow as follows:

{{< tabs name="tabs-22" >}}
{{% tab name="kotlin" %}}

```kotlin
progressTracker.currentStep = ID_OTHER_NODES

```

{{% /tab %}}

{{% tab name="java" %}}

```java
progressTracker.setCurrentStep(ID_OTHER_NODES);

```

{{% /tab %}}

{{< /tabs >}}

## Calling external systems inside of flows

Flows provide the ability to await the result of an external operation running outside of the context of a flow. A flow will suspend while
awaiting a result. This frees up a flow worker thread to continuing processing other flows.

{{< note >}}
Flow worker threads belong to the thread pool that executes flows.

{{< /note >}}
Examples of where this functionality is useful include:

* Triggering a long running process on an external system
* Retrieving information from a external service that might go down

`FlowLogic` provides two `await` functions that allow custom operations to be defined and executed outside of the context of a flow.
Below are the interfaces that must be implemented and passed into `await`, along with brief descriptions of what they do:

* `FlowExternalOperation` - An operation that returns a result which should be run using a thread from one of the node’s
thread pools.
* `FlowExternalAsyncOperation` - An operation that returns a future which should be run on a thread provided to its implementation.
Threading needs to be explicitly handled when using `FlowExternalAsyncOperation`.

`FlowExternalOperation` allows developers to write an operation that will run on a thread provided by the node’s flow external operation
thread pool.

{{< note >}}
The size of the external operation thread pool can be configured, see [the node configuration documentation](../node/setup/corda-configuration-file.md#corda-configuration-flow-external-operation-thread-pool-size).

{{< /note >}}
Below is an example of how `FlowExternalOperation` can be called from a flow to run an operation on a new thread, allowing the flow to suspend:

{{< tabs name="tabs-23" >}}
{{% tab name="kotlin" %}}

```kotlin
@StartableByRPC
class FlowUsingFlowExternalOperation : FlowLogic<Unit>() {

    @Suspendable
    override fun call() {
        // Other flow operations

        // Call [FlowLogic.await] to execute an external operation
        // The result of the operation is returned to the flow
        val response: Response = await(
            // Pass in an implementation of [FlowExternalOperation]
            RetrieveDataFromExternalSystem(
                serviceHub.cordaService(ExternalService::class.java),
                Data("amount", 1)
            )
        )
        // Other flow operations
    }

    class RetrieveDataFromExternalSystem(
        private val externalService: ExternalService,
        private val data: Data
    ) : FlowExternalOperation<Response> {

        // Implement [execute] which will be run on a thread outside of the flow's context
        override fun execute(deduplicationId: String): Response {
            return externalService.retrieveDataFromExternalSystem(deduplicationId, data)
        }
    }
}

@CordaService
class ExternalService(serviceHub: AppServiceHub) : SingletonSerializeAsToken() {

    private val client: OkHttpClient = OkHttpClient()

    fun retrieveDataFromExternalSystem(deduplicationId: String, data: Data): Response {
        return try {
            // [DeduplicationId] passed into the request so the external system can handle deduplication
            client.newCall(
                Request.Builder().url("https://externalsystem.com/endpoint/$deduplicationId").post(
                    RequestBody.create(
                        MediaType.parse("text/plain"), data.toString()
                    )
                ).build()
            ).execute()
        } catch (e: IOException) {
            // Handle checked exception
            throw HospitalizeFlowException("External API call failed", e)
        }
    }
}

data class Data(val name: String, val value: Any)
```

{{% /tab %}}

{{% tab name="java" %}}

```java
@StartableByRPC
public class FlowUsingFlowExternalOperation extends FlowLogic<Void> {

    @Override
    @Suspendable
    public Void call() {
        // Other flow operations

        // Call [FlowLogic.await] to execute an external operation
        // The result of the operation is returned to the flow
        Response response = await(
                // Pass in an implementation of [FlowExternalOperation]
                new RetrieveDataFromExternalSystem(
                        getServiceHub().cordaService(ExternalService.class),
                        new Data("amount", 1)
                )
        );
        // Other flow operations
        return null;
    }

    public class RetrieveDataFromExternalSystem implements FlowExternalOperation<Response> {

        private ExternalService externalService;
        private Data data;

        public RetrieveDataFromExternalSystem(ExternalService externalService, Data data) {
            this.externalService = externalService;
            this.data = data;
        }

        // Implement [execute] which will be run on a thread outside of the flow's context
        @Override
        public Response execute(String deduplicationId) {
            return externalService.retrieveDataFromExternalSystem(deduplicationId, data);
        }
    }
}

@CordaService
public class ExternalService extends SingletonSerializeAsToken {

    private OkHttpClient client = new OkHttpClient();

    public ExternalService(AppServiceHub serviceHub) { }

    public Response retrieveDataFromExternalSystem(String deduplicationId, Data data) {
        try {
            // [DeduplicationId] passed into the request so the external system can handle deduplication
            return client.newCall(
                    new Request.Builder().url("https://externalsystem.com/endpoint/" + deduplicationId).post(
                            RequestBody.create(
                                    MediaType.parse("text/plain"), data.toString()
                            )
                    ).build()
            ).execute();
        } catch (IOException e) {
            // Must handle checked exception
            throw new HospitalizeFlowException("External API call failed", e);
        }
    }
}

public class Data {

    private String name;
    private Object value;

    public Data(String name, Object value) {
        this.name = name;
        this.value = value;
    }

    public String getName() {
        return name;
    }

    public Object getValue() {
        return value;
    }
}
```

{{% /tab %}}

{{< /tabs >}}

In summary, the following steps are taken in the code above:

* `ExternalService` is a Corda service that provides a way to contact an external system (by HTTP in this example).
* `ExternalService.retrieveDataFromExternalSystem` is passed a `deduplicationId` which is included as part of the request to the
external system. The external system, in this example, will handle deduplication and return the previous result if it was already
computed.
* An implementation of `FlowExternalOperation` (`RetrieveDataFromExternalSystem`) is created that calls `ExternalService.retrieveDataFromExternalSystem`.
* `RetrieveDataFromExternalSystem` is then passed into `await` to execute the code contained in `RetrieveDataFromExternalSystem.execute`.
* The result of `RetrieveDataFromExternalSystem.execute` is then returned to the flow once its execution finishes.

`FlowExternalAsyncOperation` allows developers to write an operation that returns a future whose threading is handled within the CorDapp.

{{< warning >}}
Threading must be explicitly controlled when using `FlowExternalAsyncOperation`. A future will be run on its current flow worker
thread if a new thread is not spawned or provided by a thread pool. This prevents the flow worker thread from freeing up and allowing
another flow to take control and run.

{{< /warning >}}

Implementations of `FlowExternalAsyncOperation` must return a `CompletableFuture`. How this future is created is up to the developer.
It is recommended to use `CompletableFuture.supplyAsync` and supply an executor to run the future on. Other libraries can be used to
generate futures, as long as a `CompletableFuture` is returned out of `FlowExternalAsyncOperation`. An example of creating a future
using [Guava’s ListenableFuture](#api-flows-guava-future-conversion) is given in a following section.

{{< note >}}
The future can be chained to execute further operations that continue using the same thread the future started on. For example,
`CompletableFuture`’s `whenComplete`, `exceptionally` or `thenApply` could be used (their async versions are also valid).

{{< /note >}}
Below is an example of how `FlowExternalAsyncOperation` can be called from a flow:

{{< tabs name="tabs-24" >}}
{{% tab name="kotlin" %}}

```kotlin
@StartableByRPC
class FlowUsingFlowExternalAsyncOperation : FlowLogic<Unit>() {

    @Suspendable
    override fun call() {
        // Other flow operations

        // Call [FlowLogic.await] to execute an external operation
        // The result of the operation is returned to the flow
        val response: Response = await(
            // Pass in an implementation of [FlowExternalAsyncOperation]
            RetrieveDataFromExternalSystem(
                serviceHub.cordaService(ExternalService::class.java),
                Data("amount", 1)
            )
        )
        // Other flow operations
    }

    class RetrieveDataFromExternalSystem(
        private val externalService: ExternalService,
        private val data: Data
    ) : FlowExternalAsyncOperation<Response> {

        // Implement [execute] which needs to be provided with a new thread to benefit from suspending the flow
        override fun execute(deduplicationId: String): CompletableFuture<Response> {
            return externalService.retrieveDataFromExternalSystem(deduplicationId, data)
        }
    }
}

@CordaService
class ExternalService(serviceHub: AppServiceHub) : SingletonSerializeAsToken() {

    private val client: OkHttpClient = OkHttpClient()

    // [ExecutorService] created to provide a fixed number of threads to the futures created in this service
    private val executor: ExecutorService = Executors.newFixedThreadPool(
        4,
        ThreadFactoryBuilder().setNameFormat("external-service-thread").build()
    )

    fun retrieveDataFromExternalSystem(deduplicationId: String, data: Data): CompletableFuture<Response> {
        // Create a [CompletableFuture] to be executed by the [FlowExternalAsyncOperation]
        return CompletableFuture.supplyAsync(
            Supplier {
                try {
                    // [DeduplicationId] passed into the request so the external system can handle deduplication
                    client.newCall(
                        Request.Builder().url("https://externalsystem.com/endpoint/$deduplicationId").post(
                            RequestBody.create(
                                MediaType.parse("text/plain"), data.toString()
                            )
                        ).build()
                    ).execute()
                } catch (e: IOException) {
                    // Handle checked exception
                    throw HospitalizeFlowException("External API call failed", e)
                }
            },
            // The future must run on a new thread
            executor
        )
    }
}

data class Data(val name: String, val value: Any)
```

{{% /tab %}}

{{% tab name="java" %}}

```java
@StartableByRPC
public class FlowUsingFlowExternalAsyncOperation extends FlowLogic<Void> {

    @Override
    @Suspendable
    public Void call() {
        // Other flow operations

        // Call [FlowLogic.await] to execute an external operation
        // The result of the operation is returned to the flow
        Response response = await(
                // Pass in an implementation of [FlowExternalAsyncOperation]
                new RetrieveDataFromExternalSystem(
                        getServiceHub().cordaService(ExternalService.class),
                        new Data("amount", 1)
                )
        );
        // Other flow operations
        return null;
    }

    public class RetrieveDataFromExternalSystem implements FlowExternalAsyncOperation<Response> {

        private ExternalService externalService;
        private Data data;

        public RetrieveDataFromExternalSystem(ExternalService externalService, Data data) {
            this.externalService = externalService;
            this.data = data;
        }

        // Implement [execute] which needs to be provided with a new thread to benefit from suspending the flow
        @Override
        public CompletableFuture<Response> execute(String deduplicationId) {
            return externalService.retrieveDataFromExternalSystem(deduplicationId, data);
        }
    }
}

@CordaService
public class ExternalService extends SingletonSerializeAsToken {

    private OkHttpClient client = new OkHttpClient();

    // [ExecutorService] created to provide a fixed number of threads to the futures created in this service
    private ExecutorService executor = Executors.newFixedThreadPool(
            4,
            new ThreadFactoryBuilder().setNameFormat("external-service-thread").build()
    );

    public ExternalService(AppServiceHub serviceHub) { }

    public CompletableFuture<Response> retrieveDataFromExternalSystem(String deduplicationId, Data data) {
        // Create a [CompletableFuture] to be executed by the [FlowExternalAsyncOperation]
        return CompletableFuture.supplyAsync(
                () -> {
                    try {
                        // [DeduplicationId] passed into the request so the external system can handle deduplication
                        return client.newCall(
                                new Request.Builder().url("https://externalsystem.com/endpoint/" + deduplicationId).post(
                                        RequestBody.create(
                                                MediaType.parse("text/plain"), data.toString()
                                        )
                                ).build()
                        ).execute();
                    } catch (IOException e) {
                        // Must handle checked exception
                        throw new HospitalizeFlowException("External API call failed", e);
                    }
                },
                // The future must run on a new thread
                executor
        );
    }
}

public class Data {

    private String name;
    private Object value;

    public Data(String name, Object value) {
        this.name = name;
        this.value = value;
    }

    public String getName() {
        return name;
    }

    public Object getValue() {
        return value;
    }
}
```

{{% /tab %}}

{{< /tabs >}}

In summary, the following steps are taken in the code above:

* `ExternalService` is a Corda service that provides a way to contact an external system (by HTTP in this example).
* `ExternalService.retrieveDataFromExternalSystem` is passed a `deduplicationId` which is included as part of the request to the
external system. The external system, in this example, will handle deduplication and return the previous result if it was already
computed.
* A `CompletableFuture` is created that contacts the external system. `CompletableFuture.supplyAsync` takes in a reference to the
`ExecutorService` which will provide a thread for the external operation to run on.
* An implementation of `FlowExternalAsyncOperation` (`RetrieveDataFromExternalSystem`) is created that calls the `ExternalService.retrieveDataFromExternalSystem`.
* `RetrieveDataFromExternalSystem` is then passed into `await` to execute the code contained in `RetrieveDataFromExternalSystem.execute`.
* The result of `RetrieveDataFromExternalSystem.execute` is then returned to the flow once its execution finishes.

A Flow has the ability to rerun from any point where it suspends. Due to this, a flow can execute code multiple times depending on where it
retries. For context contained inside a flow, values will be reset to their state recorded at the last suspension point. This makes most
properties existing inside a flow safe when retrying. External operations do not have the same guarantees as they are executed outside of
the context of flows.

External operations are provided with a `deduplicationId` to allow CorDapps to decide whether to run the operation again or return a
result retrieved from a previous attempt. How deduplication is handled depends on the CorDapp and how the external system works. For
example, an external system might already handle this scenario and return the result from a previous calculation or it could be idempotent
and can be safely executed multiple times.

{{< warning >}}
There is no inbuilt deduplication for external operations. Any deduplication must be explicitly handled in whatever way is
appropriate for the CorDapp and external system.

{{< /warning >}}

The `deduplicationId` passed to an external operation is constructed from its calling flow’s ID and the number of suspends the flow has
made. Therefore, the `deduplicationId` is guaranteed to be the same on a retry and will never be used again once the flow has successfully
reached its next suspension point.

{{< note >}}
Any external operations that did not finish processing (or were kept in the flow hospital due to an error) will be retried upon node
restart.

{{< /note >}}
Below are examples of how deduplication could be handled:

* The external system records successful computations and returns previous results if requested again.
* The external system is idempotent, meaning the computation can be made multiple times without altering any state (similar to the point above).
* An extra external service maintains a record of deduplication IDs.
* Recorded inside of the node’s database.

{{< note >}}
Handling deduplication on the external system’s side is preferred compared to handling it inside of the node.

{{< /note >}}

{{< warning >}}
In-memory data structures should not be used for handling deduplication as their state will not survive node restarts.

{{< /warning >}}

The code below demonstrates how to convert a `ListenableFuture` into a `CompletableFuture`, allowing the result to be executed using a
`FlowExternalAsyncOperation`.

{{< tabs name="tabs-25" >}}
{{% tab name="kotlin" %}}

```kotlin
@CordaService
class ExternalService(serviceHub: AppServiceHub) : SingletonSerializeAsToken() {

    private val client: OkHttpClient = OkHttpClient()

    // Guava's [ListeningExecutorService] created to supply a fixed number of threads
    private val guavaExecutor: ListeningExecutorService = MoreExecutors.listeningDecorator(
        Executors.newFixedThreadPool(
            4,
            ThreadFactoryBuilder().setNameFormat("guava-thread").build()
        )
    )

    fun retrieveDataFromExternalSystem(deduplicationId: String, data: Data): CompletableFuture<Response> {
        // Create a Guava [ListenableFuture]
        val guavaFuture: ListenableFuture<Response> = guavaExecutor.submit(Callable<Response> {
            try {
                // [DeduplicationId] passed into the request so the external system can handle deduplication
                client.newCall(
                    Request.Builder().url("https://externalsystem.com/endpoint/$deduplicationId").post(
                        RequestBody.create(
                            MediaType.parse("text/plain"), data.toString()
                        )
                    ).build()
                ).execute()
            } catch (e: IOException) {
                // Handle checked exception
                throw HospitalizeFlowException("External API call failed", e)
            }
        })
        // Create a [CompletableFuture]
        return object : CompletableFuture<Response>() {
            override fun cancel(mayInterruptIfRunning: Boolean): Boolean {
                return guavaFuture.cancel(mayInterruptIfRunning).also {
                    super.cancel(mayInterruptIfRunning)
                }
            }
        }.also { completableFuture ->
            // Create a callback that completes the returned [CompletableFuture] when the underlying [ListenableFuture] finishes
            val callback = object : FutureCallback<Response> {
                override fun onSuccess(result: Response?) {
                    completableFuture.complete(result)
                }

                override fun onFailure(t: Throwable) {
                    completableFuture.completeExceptionally(t)
                }
            }
            // Register the callback
            Futures.addCallback(guavaFuture, callback, guavaExecutor)
        }
    }
}
```

{{% /tab %}}

{{% tab name="java" %}}

```java
@CordaService
public class ExternalService extends SingletonSerializeAsToken {

    private OkHttpClient client = new OkHttpClient();

    public ExternalService(AppServiceHub serviceHub) { }

    private ListeningExecutorService guavaExecutor = MoreExecutors.listeningDecorator(
            Executors.newFixedThreadPool(
                    4,
                    new ThreadFactoryBuilder().setNameFormat("guava-thread").build()
            )
    );

    public CompletableFuture<Response> retrieveDataFromExternalSystem(String deduplicationId, Data data) {
        // Create a Guava [ListenableFuture]
        ListenableFuture<Response> guavaFuture = guavaExecutor.submit(() -> {
            try {
                // [DeduplicationId] passed into the request so the external system can handle deduplication
                return client.newCall(
                        new Request.Builder().url("https://externalsystem.com/endpoint/" + deduplicationId).post(
                                RequestBody.create(
                                        MediaType.parse("text/plain"), data.toString()
                                )
                        ).build()
                ).execute();
            } catch (IOException e) {
                // Must handle checked exception
                throw new HospitalizeFlowException("External API call failed", e);
            }
        });
        // Create a [CompletableFuture]
        CompletableFuture<Response> completableFuture = new CompletableFuture<Response>() {
            // If the returned [CompletableFuture] is cancelled then the underlying [ListenableFuture] must be cancelled as well
            @Override
            public boolean cancel(boolean mayInterruptIfRunning) {
                boolean result = guavaFuture.cancel(mayInterruptIfRunning);
                super.cancel(mayInterruptIfRunning);
                return result;
            }
        };
        // Create a callback that completes the returned [CompletableFuture] when the underlying [ListenableFuture] finishes
        FutureCallback<Response> callback = new FutureCallback<Response>() {
            @Override
            public void onSuccess(Response result) {
                completableFuture.complete(result);
            }

            @Override
            public void onFailure(Throwable t) {
                completableFuture.completeExceptionally(t);
            }
        };
        // Register the callback
        Futures.addCallback(guavaFuture, callback, guavaExecutor);

        return completableFuture;
    }
}
```

{{% /tab %}}

{{< /tabs >}}

In the code above:

* A `ListenableFuture` is created and receives a thread from the `ListeningExecutorService`. This future does all the processing.
* A `CompletableFuture` is created, so that it can be returned to and executed by a `FlowExternalAsyncOperation`.
* A `FutureCallback` is registered to the `ListenableFuture`, which will complete the `CompletableFuture` (either successfully or
exceptionally) depending on the outcome of the `ListenableFuture`.
* `CompletableFuture.cancel` is overridden to propagate its cancellation down to the underlying `ListenableFuture`.

## Concurrency, Locking and Waiting

Corda is designed to:

* run many flows in parallel
* persist flows to storage and resurrect those flows much later
* (in the future) migrate flows between JVMs

Because of this, care must be taken when performing locking or waiting operations.

Flows should avoid using locks or interacting with objects that are shared between flows (except for `ServiceHub` and other
carefully crafted services such as Oracles.  See oracles). Locks will significantly reduce the scalability of the
node, and can cause the node to deadlock if they remain locked across flow context switch boundaries (such as when sending
and receiving from peers, as discussed above, or sleeping, as discussed below).

A flow can wait until a specific transaction has been received and verified by the node using *FlowLogic.waitForLedgerCommit*.
Outside of this, scheduling an activity to occur at some future time should be achieved using `SchedulableState`.

However, if there is a need for brief pauses in flows, you have the option of using `FlowLogic.sleep` in place of where you
might have used `Thread.sleep`. Flows should expressly not use `Thread.sleep`, since this will prevent the node from
processing other flows in the meantime, significantly impairing the performance of the node.

Even `FlowLogic.sleep` should not be used to create long running flows or as a substitute to using the `SchedulableState`
scheduler, since the Corda ethos is for short-lived flows (long-lived flows make upgrading nodes or CorDapps much more
complicated).

For example, the `finance` package currently uses `FlowLogic.sleep` to make several attempts at coin selection when
many states are soft locked, to wait for states to become unlocked:

```kotlin
for (retryCount in 1..maxRetries) {
    if (!attemptSpend(services, amount, lockId, notary, onlyFromIssuerParties, withIssuerRefs, stateAndRefs)) {
        log.warn("Coin selection failed on attempt $retryCount")
        // TODO: revisit the back off strategy for contended spending.
        if (retryCount != maxRetries) {
            stateAndRefs.clear()
            val durationMillis = (minOf(retrySleep.shl(retryCount), retryCap / 2) * (1.0 + Math.random())).toInt()
            FlowLogic.sleep(durationMillis.millis)
        } else {
            log.warn("Insufficient spendable states identified for $amount")
        }
    } else {
        break
    }
}
```

## Killing flows

A flow becomes unusable and problematic in the following cases:

- Blocked due to a never-ending or long-running loop.
- Waiting indefinitely for another node to respond.
- Started accidentally.

To resolve such issues, you can kill a flow - this will effectively "cancel" that flow.

### Overview

Killing a flow will gracefully terminate the flow. When you kill a flow, the following sequence of events occurs:

1. An `UnexpectedFlowEndException` is propagated to any nodes the flow is interacting with.
2. The flow releases its resources and any soft locks that it reserved.
3. An exception is returned to the calling client (as a `FlowKilledException` unless another exception is specified).

A flow can be killed through the following means:

- `flow kill` shell command.
- `CordaRPCOps.killFlow` when writing a RPC client.

#### Exceptions

Exceptions are only propagated between flows (either from a flow initiator to its responder, or vice versa) when there is an active session established between them. A session is considered active if there are further calls to functions that interact with it within the flow's execution, such as `send`, `receive`, and `sendAndReceive`. If a flow’s counter party flow is killed, it only receives an `UnexceptedFlowEndException` once it interacts with the failed session again.

A `FlowKilledException` is propagated to client that started the initiating flow. The `KilledFlowException` cannot be caught unless manually thrown as documented below in [Cooperating with a killed flow](#cooperating-with-a-killed-flow).

### Cooperating with a killed flow

To allow for a killed flow to terminate when the kill flow command has been executed, at the time of writing the flow you must ensure that the flow includes exit points.

All suspendable functions (functions annotated with `@Suspendable`) already take this into account and check if a flow has been killed. This allows a killed flow to terminate when reaching a suspendable function. The flow will also exit if it is currently suspended.

An example of this is shown below:

{{< tabs name="tabs-26" >}}
{{% tab name="kotlin" %}}
```kotlin
@Suspendable
override fun call() {
    val session = initiateFlow(party)
    while (true) {
        // processing code
        session.sendAndReceive<String>("Here is some data")
    }
}
```
{{% /tab %}}
{{% tab name="java" %}}
```java
@Override
@Suspendable
public Void call() {
    FlowSession session = initiateFlow(party);
    while (true) {
        // processing code
        session.sendAndReceive(String.class,"Here is some data");
    }
}
```
{{% /tab %}}
{{< /tabs >}}

A killed flow running the code above, will exit either when it reaches the next `sendAndReceive` or straight away if the flow is already suspended due to the `sendAndReceive` call.

If your flow has functions that are not marked as `@suspendable`, you may need to check the status of the flow manually to cooperate with the kill flow request.

To do so, add a check on the `isKilled` flag of the flow. Use the example below to see how this is done:


{{< tabs name="tabs-27" >}}
{{% tab name="kotlin" %}}
```kotlin
@Suspendable
override fun call() {
    while (true) {
        if (isKilled) {
            throw KilledFlowException(runId)
        }
        // processing code
    }
}
```
{{% /tab %}}
{{% tab name="java" %}}
```java
@Override
@Suspendable
public Void call() {
    while (true) {
        if (isKilled()) {
            throw new KilledFlowException(getRunId());
        }
        // processing code
    }
}
```
{{% /tab %}}
{{< /tabs >}}

The function in the example above exits the loop by checking the `isKilled` flag and throwing an exception if the flow has been killed.

There are also two overloads of `checkFlowIsNotKilled` that simplify the code above:

{{< tabs name="tabs-28" >}}
{{% tab name="kotlin" %}}
```kotlin
@Suspendable
override fun call() {
    while (true) {
        checkFlowIsNotKilled()
        // processing code
    }
}
```
{{% /tab %}}
{{% tab name="java" %}}
```java
@Override
@Suspendable
public Void call() {
    while (true) {
        checkFlowIsNotKilled();
        // processing code
    }
}
```
{{% /tab %}}
{{< /tabs >}}

The other overload takes in a message to add to the returned `KilledFlowException`.

{{< note >}}
If a section of a flow is processing-heavy and does not include any calls to suspendable functions, consider moving it into an [external operation](#calling-external-systems-inside-of-flows). Killing a flow that is suspended while performing an external operation does not require any special handling within the flow.
{{< /note >}}
