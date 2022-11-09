---
aliases:
- /head/api-flows.html
- /HEAD/api-flows.html
- /api-flows.html
date: '2021-08-12'
menu:
  corda-community-4-9:
    identifier: corda-community-4-9-api-flows
    parent: corda-community-4-9-corda-api
    weight: 220
tags:
- api
- flows
title: 'API: Flows'
---

# Flows

Flows allow your CorDapp to communicate with other parties on a network. Before you begin, familiarize yourself with the flow key concepts.

In this document, you will:

* See an example flow for a basic ledger update, demonstrating the `Initiator` and `Responder` sides of a flow.
* Get an explanation of `Flowlogic`, including annotations and calls.
* Learn how to build transactions and extract states from the vault.
* Explore how nodes communicate and share data.
* Learn how to use subflows.
* Discover flow exceptions and how they are resolved.
* Find out how to visually track the progress of a flow.
* Learn how you can expand the reach of your flows by calling external systems.
* Uncover the best practices for concurrency, locking, and waiting.
* Discover how to gracefully end a flow by killing it.

Each concept is illustrated with sample code.

## An example flow

If Alice and Bob want to agree a basic ledger update, they would create a flow with two sides, one for each party:

* An `Initiator` side: A flow class that initiates the request to update the ledger.
* A `Responder` side: A flow class that responds to the request to update the ledger.

### Initiator flow class example

In this example, the `Initiator` does the majority of the work - they will build, sign, verify, and finalize the transaction.

**Step 1: Build the transaction**

The `initiator`:

1. Chooses a notary for the transaction.
2. Create a transaction builder.
3. Extracts any input states from the vault and adds them to the builder.
4. Creates any output states and adds them to the builder.
5. Adds any commands, attachments or time windows to the builder.

**Step 2: Sign the transaction**

The `initiator`:

1. Signs the transaction builder.
2. Converts the builder into a signed transaction.

**Step 3: Verify the transaction**

The `initiator`:

1. Runs the [contracts](api-contracts.md) contained in the CorDapp.
2. Verifies that the transaction is valid based on the contracts.


**Step 4: Get the counterparty’s signature**

The `initiator`:

1. Sends the transaction to the responding counterparty.
2. Waits to get the responding counterparty’s signature.
3. Adds the responding counterparty’s signature to the transaction.
4. Verifies the transaction’s signatures.

**Step 5: Finalize the transaction**

The `initiator`:

1. Sends the transaction to the notary.
2. Waits to receive the notarized transaction.
3. Records the transaction locally.
4. Stores any relevant states in the vault.
5. Sends the transaction to the counterparty for recording.

You can visualize the work performed by initiator like this:

{{< figure alt="flow overview" width=80% zoom="./resources/flow-overview.png" >}}

## Responder flow class example

The `responder` verifies, signs, and records the transaction.

**Step 1: Verify the transaction**

The `responder`:

1. Receives the transaction from the counterparty.
2. Verifies the transaction’s existing signatures.
3. Runs the [contracts](api-contracts.md) contained in the CorDapp.
4. Verifies that the transaction is valid based on the contracts.


**Step 2: Sign the transaction**

The `responder`:

1. Generates a signature for the transaction.
2. Sends the signature back to the counterparty.

**Step 3 - Record the transaction**

The `responder`:

1. Receives the notarized transaction from the `initiator`.
2. Records the transaction locally.
3. Stores any relevant states in the vault.

The transaction is now part of the ledger.

## The `FlowLogic` class

You can implement flows as one or more communicating `FlowLogic` subclasses. The `FlowLogic`
subclass’s constructor can take any number of arguments of any type. The generic `FlowLogic` (e.g.
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

### `FlowLogic` annotations

Use annotations to track the interactions between flows.

* `@InitiatingFlow`: If you plan to initiate additional flows from an initial flow, you must annotate the first flow with `@InitiatingFlow`.

* `@StartableByRPC`: If you plan to start the flow via RPC, annotate it with `@StartableByRPC`:

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

`@InitiatedBy`: If a flow responds to any messages from another flow, use `@InitiatedBy`. `@InitiatedBy` takes the class of the flow it is responding to as its single parameter:

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

* `@SchedulableFlow`: If a `SchedulableState` starts a flow, annotate the flow with `@SchedulableFlow`.

### `FlowLogic` calls

Each `FlowLogic` subclass must override `FlowLogic.call()`, which describes the actions it will take as part of
the flow. For example, the actions of the initiator’s side of the flow would be defined in `Initiator.call`, and the
actions of the responder’s side of the flow would be defined in `Responder.call`.

For nodes to run multiple flows concurrently, and survive node upgrades and
restarts, flows need to be checkpointable and serializable to disk. To do this, mark `FlowLogic.call()`,
and any function invoked from within `FlowLogic.call()`, with an `@Suspendable` annotation.

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

### Accessing the node's `ServiceHub`

You can access the node's `ServiceHub` within `FlowLogic.call`. The `ServiceHub` provides access to the
node's services. See [Accessing node services](api-service-hub.md) for more information.

### Common flow tasks

To agree ledger updates, you need to perform a number of common tasks within `FlowLogic.call`:

* **Transaction building:** The majority of the work performed during a flow is building, verifying, and signing a transaction. See [Understanding transactions](api-transactions.md).
* **Extracting states from the vault:**: When building a transaction, you’ll often need to extract the states you wish to consume from the vault. See [Writing vault queries](api-vault-query.md).
* **Retrieving information about other nodes:**: You can retrieve information about other nodes on the network and the services they offer using `ServiceHub.networkMapCache`.

### Notaries

Transactions generally need a notary to:

* Prevent double-spends if the transaction has inputs.
* Serve as a timestamping authority if the transaction has a time window.

You can retreive a notary from the network map:

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

### Retrieving specific counterparties

You can use the network map to retrieve a specific counterparty:

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

To create a communication session between your `initiator` flow and the `receiver` flow, you must call
`initiateFlow(party: Party): FlowSession`.

`FlowSession` instances provide three functions:

* `send(payload: Any)`
  * Sends the `payload` object
* `receive(receiveType: Class<R>): R`
  * Receives an object of type `receiveType`
* `sendAndReceive(receiveType: Class<R>, payload: Any): R`
  * Sends the `payload` object and receives an object of type `receiveType` back

``FlowLogic`` also provides functions that can receive messages from multiple sessions and send messages to multiple sessions:

* `receiveAllMap(sessions: Map<FlowSession, Class<out Any>>): Map<FlowSession, UntrustworthyData<Any>>`
  * Receives from all `FlowSession` objects specified in the passed in map. The received types may differ.
* `receiveAll(receiveType: Class<R>, sessions: List<FlowSession>): List<UntrustworthyData<R>>`
  * Receives from all `FlowSession` objects specified in the passed in list. The received types must be the same.
* `sendAll(payload: Any, sessions: Set<FlowSession>)`
  * Sends the ``payload`` object to all the provided `FlowSession`.
* `sendAllMap(payloadsPerSession: Map<FlowSession, Any>)`
  * Sends a potentially different payload to each `FlowSession`, as specified by the provided `payloadsPerSession`.

{{% note %}}
It's more efficient to call `sendAndReceive` instead of calling `send` and then `receive`. It's also more efficient to call `sendAll / receiveAll` instead of multiple individual `send` and `receive` calls.
{{% /note %}}

### Create communication sessions with `InitiateFlow`

`initiateFlow` creates a communication session with the `Party` that you pass in.

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

When you call this function, no communication happens until the first
`send` or `receive`. At that point the counterparty will either:

* Ignore the message, if they are not registered to respond to messages from your flow.
* Start a flow, if they have one registered to respond to your flow.

### Send

Once you have a `FlowSession` object, you can send arbitrary data to a counterparty:

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

The flow on the other side must eventually reach a corresponding `receive` call to get the message.

### Receiving data from counterparties

You can choose to wait to receive arbitrary data of a specific type from a counterparty. This implies a corresponding
`send` call in the counterparty’s flow. A few scenarios:

* You never receive a message back. In the current design, the flow is paused until the node’s owner kills the flow.
* Instead of sending a message back, the counterparty throws a `FlowException`. This exception is propagated back
  to you. You can use the error message to establish what happened.
* You receive a message back, but it’s of the wrong type. In this case, a `FlowException` is thrown.
* You receive back a message of the correct type.

If `FlowLogic` calls `receive` or `sendAndReceive`, `FlowLogic` is suspended until it receives a response.

If you receive the data wrapped in an `UntrustworthyData` instance. This is a reminder to check that the data is as expected. Unwrap the `UntrustworthyData` using a lambda to examine it:

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

You're not limited to exchanging data with a single counterparty. You can use flows to send messages to as many parties
as you need to. Each party can invoke a different response flow:

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
If you initiate several flows from the same `@InitiatingFlow` flow, then on the receiving side you must be
prepared to be initiated by any of the corresponding `initiateFlow()` calls. A good way of handling this ambiguity
is to send “role” message as your first message to the initiated flow, indicating which part of the initiating flow
the rest of the counter-flow should conform to. For example, you could send an enum, and on the other side start with a switch
statement.

{{< /warning >}}

### SendAndReceive

You can use a single call to send data to a counterparty and wait to receive data of a specific type back. The
type of data sent doesn’t need to match the type of the data received:

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

Imagine you are now on the `Responder` side of the flow. You had this exchange with the `Initiator`:

* The `Initiator` sent you an `Any` instance.
* You responded with an `Integer` instance.
* The `Initiator` sent you a `String` instance and is waiting to receive a `Boolean` instance from you.

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

Subflows are pieces of reusable flows that you can run by calling `FlowLogic.subFlow`. There are two broad categories
of subflows: inlined and initiating. Initiating flows initiate counter-flows automatically, while inlined ones expect a parent counter-flow to run the inlined
counterpart.

### Inlined subflows

Inlined subflows inherit their calling flow’s type when they initiate a new session with a counterparty. For example, flow A calls an inlined subflow B, which in turn initiates a session with a party. The `FlowLogic` type used to
determine which counter-flow should be kicked off is A, not B. This means that the other side of this
inlined flow must be implemented explicitly in the kicked-off flow. You can do this by calling a
matching inlined counter-flow, or by implementing the other side explicitly in the kicked-off parent flow.

An example of this type of flow is `CollectSignaturesFlow`. It has a counter-flow, `SignTransactionFlow`, which isn’t
annotated with `InitiatedBy`. This is because both of these flows are inlined. The kick-off relationship is
defined when the parent flows call `CollectSignaturesFlow` and `SignTransactionFlow`.

In the code, inlined subflows appear as regular `FlowLogic` instances, *without* either of the `@InitiatingFlow` or
`@InitiatedBy` annotation.

{{< note >}}
Inlined flows aren’t versioned; they inherit their parent flow’s version.

{{< /note >}}

### Initiating subflows

Initiating subflows annotated with the `@InitiatingFlow` annotation. When this type of flow initiates a session, its
type is used to determine which `@InitiatedBy` flow to kick off on the counterparty.

An example is the `@InitiatingFlow InitiatorFlow`/`@InitiatedBy ResponderFlow` flow pair in the `FlowCookbook`.

{{< note >}}
Initiating flows are versioned separately from their parents.

{{< /note >}}
{{< note >}}
The only exception to this rule is `FinalityFlow`, which is annotated with `@InitiatingFlow` but is an inlined flow. `FinalityFlow` was previously initiating, and the annotation exists to maintain backwards compatibility.

{{< /note >}}

#### Core initiating subflows

Corda-provided initiating subflows are a little different from standard ones. They are versioned together with the
platform, and their initiated counter-flows are registered explicitly. This eliminates the need for the `InitiatedBy`
annotation.

### Library flows

Corda installs four initiating subflow pairs on each node by default:

* `NotaryChangeFlow`/`NotaryChangeHandler`, used to change a state’s notary.
* `ContractUpgradeFlow.Initiate`/`ContractUpgradeHandler`, used to change a state’s contract.
* `SwapIdentitiesFlow`/`SwapIdentitiesHandler`, used to exchange confidential identities with a
  counterparty.

{{< warning >}}
`SwapIdentitiesFlow` and `SwapIdentitiesHandler` are only installed if you include the `confidential-identities` module. The `confidential-identities` module is not yet stabilized, so the
`SwapIdentitiesFlow`/`SwapIdentitiesHandler` API may change in future releases. See [API stability guarantees](api-stability-guarantees.md).

{{< /warning >}}

Corda provides a number of built-in inlined subflows that you can use to handle common tasks. The most
important are:

* `FinalityFlow`, used to notarize, locally record, and broadcast a signed transaction to its participants
  and any extra parties.
* `ReceiveFinalityFlow`, used to receive these notarized transactions from the `FinalityFlow` sender and record them locally.
* `CollectSignaturesFlow`, used to collect a transaction’s required signatures.
* `SendTransactionFlow`, used to send a signed transaction if it needs to be resolved on
  the other side.
* `ReceiveTransactionFlow`, used to receive a signed transaction.


### FinalityFlow

`FinalityFlow` lets you notarize the transaction and record it in the vault of the participants of all
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

You can choose to send the transaction to additional parties who aren’t one of the state’s participants:

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

To record a transaction for all parties:

1. **Only one** party calls `FinalityFlow`.
2. All other parties  **must** call `ReceiveFinalityFlow` in their responder
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

`idOfTxWeSigned` is an optional parameter used to confirm that you have received the right transaction. It comes from `SignTransactionFlow`
which is described in the error handling behaviour section.

Some transactions only have one participant: the initiator. That means there are no other
parties to send transactions to during `FinalityFlow`. In this case, use an empty `counterpartySession` list.

Once a transaction is notarized and its input states consumed by the flow initiator, if the participant(s) receiving the
transaction fail to verify it, or the receiving flow (the finality handler) fails due to some other error, then
all parties will not have the up-to-date view of the ledger.

To recover from this scenario, the receiver’s finality handler is automatically sent to the `node-flow-hospital`. There, it is suspended and retried from its last checkpoint
upon node restart, or according to other conditional retry rules - see [flow hospital runtime behavior](node-flow-hospital.md).
This gives the node operator the opportunity to recover from the error. Until the issue is resolved, the node will continue to retry the flow
on each startup. Upon successful completion by the receiver’s finality flow, the ledger will become fully consistent.

{{< warning >}}
It’s possible to forcibly terminate the erroring finality handler using the `killFlow` RPC. However, this risks an inconsistent view of the ledger.

{{< /warning >}}



### CollectSignaturesFlow/SignTransactionFlow

The transaction's commands dictate the parties who need to sign a transaction. After you sign a
transaction, you can automatically gather the signatures of the other required signers using
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

Check that:

* The transaction received is the expected type, and has the expected types of inputs and outputs.
* The properties of the outputs are expected, unless you have integrated reference
  data sources to facilitate this.
* The transaction is correctly spending asset states and is not spending them maliciously. The transaction creator could have access to some of signer’s state references.


### `SendTransactionFlow` and `ReceiveTransactionFlow`

When you verify a transaction you've received from a counterparty, you must also verify every transaction in its
dependency chain. This means the receiving party needs to be able to ask the sender for all the details of the chain.
The sender sends the transaction using `SendTransactionFlow` to process all subsequent
transaction data vending requests while the receiver walks the dependency chain using `ReceiveTransactionFlow`:

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

You can send and receive a `StateAndRef` dependency chain and automatically resolve its dependencies:

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

#### Why inlined subflows?

Inlined subflows provide a way to share commonly used flow code *while forcing users to create a parent flow*. Without inlined flows, flow users could create insecure chains of events. For
example, a user could make `CollectSignaturesFlow` an initiating flow that automatically kicks off
`SignTransactionFlow`, which signs the transaction. A malicious node could send any transaction to
them using `CollectSignaturesFlow`, and they would automatically sign it.

If you make this pair of flows inlined, you can make sure the user actively chooses to either sign the transaction or not by
forcing them to nest it in their own parent flows.

If you’re writing a subflow, the decision of whether you should make it initiating should depend on whether
the counter-flow needs broader context to achieve its goal.

## FlowException

Suppose a node throws an exception while running a flow. Any counterparty flows waiting for a message from the node
(as part of a call to `receive` or `sendAndReceive`) are notified that the flow has ended unexpectedly
and that the related counterparty flows will be terminated. However, the counterparties are not told what the exception is.

If you wish to notify any waiting counterparties of the exception cause, throw a
`FlowException`:

The flow framework automatically propagates the `FlowException` back to the waiting counterparties.

There are many scenarios in which throwing a `FlowException` would be appropriate:

* A transaction doesn’t `verify()`.
* A transaction’s signatures are invalid.
* The transaction does not match the parameters of the deal as discussed.
* You are reneging on a deal.

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

Some operations can fail intermittently, and will succeed if they are tried again later. Flows can halt their
execution in such situations. By throwing a `HospitalizeFlowException`, a flow will stop and retry at a later time (on the next node restart).

A `HospitalizeFlowException` can be defined in various ways:

{{< note >}}
If a `HospitalizeFlowException` is wrapping or extending an exception already being handled by the node-flow-hospital, the outcome of a flow may change. For example, the flow
could instantly retry or terminate if a critical error occurred.

{{< /note >}}
{{< note >}}
`HospitalizeFlowException` can be extended for customized exceptions. These exceptions are treated in the same way when thrown.

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

You can give your flow a progress tracker. This lets you track the flow’s progress visually in your node’s CRaSH shell.

To provide a progress tracker, override the flow's `FlowLogic.progressTracker`:

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

Then, update the progress tracker’s current step as you progress through the flow:

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

You can wait for the result of an external operation running outside of the context of a flow - flows suspend when
waiting for a result. This frees up flow worker threads to continue processing other flows.

{{< note >}}
Flow worker threads belong to the thread pool that executes flows.

{{< /note >}}
You could use this functionality to:

* Trigger a long running process on an external system.
* Retrieve information from an external service that might go down.

`FlowLogic` provides two `await` functions that allow custom operations to be defined and executed outside of the context of a flow:

* `FlowExternalOperation`: Returns a result which should be run using a thread from one of the node’s
  thread pools.
* `FlowExternalAsyncOperation`: Returns a future, which you should run on a thread provided for its implementation.
  Threading needs to be explicitly handled when using `FlowExternalAsyncOperation`.
* `FlowExternalOperation`: Allows developers to write an operation that runs on a thread provided by the node’s flow external operation
  thread pool.

{{< note >}}
The size of the external operation thread pool can be configured. See [the node configuration documentation](corda-configuration-file.md).

{{< /note >}}
You can call `FlowExternalOperation` from a flow to run an operation on a new thread, allowing the flow to suspend:

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

In the code above:

1. `ExternalService` is a Corda service that provides a way to contact an external system (by HTTP in this example). `ExternalService.retrieveDataFromExternalSystem` is passed a `deduplicationId` which is included as part of the request to the external system. The external system, in this example, handles deduplication and returns the previous result if it was already
   computed.
2. An implementation of `FlowExternalOperation` (`RetrieveDataFromExternalSystem`) is created that calls `ExternalService.retrieveDataFromExternalSystem`.
3. `RetrieveDataFromExternalSystem` is passed into `await` to execute the code contained in `RetrieveDataFromExternalSystem.execute`.
4. The result of `RetrieveDataFromExternalSystem.execute` is returned to the flow once its execution finishes.

`FlowExternalAsyncOperation` allows developers to write an operation that returns a future with threading handled within the CorDapp.

{{< warning >}}
Threading must be explicitly controlled when using `FlowExternalAsyncOperation`. If a new thread is not spawned or provided by a thread pool, then a future runs on its current flow worker thread. This prevents the flow worker thread from freeing up and allowing another flow to take control and run.

{{< /warning >}}

Implementations of `FlowExternalAsyncOperation` must return a `CompletableFuture`. The developer decides how to create this future.
The best practice is to use `CompletableFuture.supplyAsync` and supply an executor to run the future. You can use other libraries to
generate futures, as long as a `CompletableFuture` is returned out of `FlowExternalAsyncOperation`. You can see an example of creating a future
using Guava’s ListenableFuture below.

{{< note >}}
You can chain the future to execute further operations that continue using the same thread the future started on. For example,
`CompletableFuture`’s `whenComplete`, `exceptionally` or `thenApply` could be used (their async versions are also valid).

{{< /note >}}
Below is an example of how you can call `FlowExternalAsyncOperation`:

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

In the code above:

1. `ExternalService` is a Corda service that provides a way to contact an external system (by HTTP in this example). `ExternalService.retrieveDataFromExternalSystem` is passed a `deduplicationId`, which is included as part of the request to the external system. The external system, in this example, handles deduplication and returns the previous result if it was already computed.
2. A `CompletableFuture` is created that contacts the external system. `CompletableFuture.supplyAsync` takes in a reference to the
   `ExecutorService`, which provides a thread for the external operation to run on.
3. An implementation of `FlowExternalAsyncOperation` (`RetrieveDataFromExternalSystem`) is created that calls the `ExternalService.retrieveDataFromExternalSystem`.
4. `RetrieveDataFromExternalSystem` is passed into `await` to execute the code contained in `RetrieveDataFromExternalSystem.execute`.
5. The result of `RetrieveDataFromExternalSystem.execute` is then returned to the flow once its execution finishes.

A flow can rerun from any point where it suspends. That means a flow can execute code multiple times depending on the retry point. For context contained inside a flow, values are reset to the state recorded at the last suspension point. This means that most properties inside are flow safe when retrying. External operations are at greater risk because they are executed outside of
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
Some examples of how you could handle deduplication:

* The external system records successful computations and returns previous results if requested again.
* The external system is idempotent, meaning the computation can be made multiple times without altering any state.
* An extra external service maintains a record of deduplication IDs.
* Deduplication is recorded inside of the node’s database.

{{< note >}}
Handling deduplication on the external system’s side is preferred compared to handling it inside of the node.

{{< /note >}}

{{< warning >}}
You shouldn't use in-memory data structures to handle deduplication as their state will not survive node restarts.

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

1. A `ListenableFuture` is created and receives a thread from the `ListeningExecutorService`. This future does all the processing.
2. A `CompletableFuture` is created, so that it can be returned to and executed by a `FlowExternalAsyncOperation`.
3. A `FutureCallback` is registered to the `ListenableFuture`, which will complete the `CompletableFuture` (either successfully or
   exceptionally) depending on the outcome of the `ListenableFuture`.
4. `CompletableFuture.cancel` is overridden to propagate its cancellation down to the underlying `ListenableFuture`.

## Concurrency, locking and waiting

Corda is designed to:

* Run many flows in parallel.
* Persist flows to storage and resurrect those flows later.

This means you should take care when performing locking or waiting operations.

Flows should avoid using locks or interacting with objects that are shared between flows (except for `ServiceHub` and other
carefully crafted services such as Oracles). Locks significantly reduce the scalability of the
node, and can cause the node to deadlock if they remain locked across flow context-switch boundaries (such as when sending
and receiving from peers or sleeping).

A flow can wait until a specific transaction has been received and verified by the node using *FlowLogic.waitForLedgerCommit*.
Otherwise, schedule activities for future times using `SchedulableState`.

If you need to create brief pauses in flows, you have the option of using `FlowLogic.sleep` where you
might have used `Thread.sleep`. Flows should **not** use `Thread.sleep`, since this will prevent the node from
processing other flows in the meantime, significantly impairing the performance of the node.

Corda is optimized for short-lived flows. Long-lived flows make upgrading nodes or CorDapps much more
complicated. You should not use `FlowLogic.sleep` to create long-running flows or as a substitute for the `SchedulableState`
scheduler.

For example, the `finance` package uses `FlowLogic.sleep` to make several attempts at coin selection when
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

A flow becomes unusable and problematic when it is:

* Blocked due to a never-ending or long-running loop.
* Waiting indefinitely for another node to respond.
  *Started accidentally.

To resolve these issues, you can kill a flow. This effectively "cancels" that flow.

### Overview

Killing a flow gracefully terminates the flow. When you kill a flow:

1. An `UnexpectedFlowEndException` is propagated to any nodes the flow is interacting with.
2. The flow releases its resources and any soft locks that it reserved.
3. An exception is returned to the calling client (as a `FlowKilledException` unless another exception is specified).

You can kill a flow using:

* The `flow kill` shell command.
* The `CordaRPCOps.killFlow` command, when writing an RPC client.

#### Exceptions

Exceptions are only propagated between flows (either from a flow initiator to its responder, or vice versa) when there is an active session established between them. A session is considered active if there are further calls to functions that interact with it within the flow's execution, such as `send`, `receive`, and `sendAndReceive`. If a flow’s counterparty flow is killed, it only receives an `UnexceptedFlowEndException` once it interacts with the failed session again.

A `FlowKilledException` is propagated to the client that started the initiating flow. You cannot catch the `KilledFlowException` unless it is thrown manually - see [cooperating with a killed flow](#cooperating-with-a-killed-flow).

### Cooperating with a killed flow

To allow a killed flow to terminate when you execute the kill flow command, make sure your flow includes exit points.

All suspendable functions (functions annotated with `@Suspendable`) already take this into account, and check if a flow has been killed. This allows a killed flow to terminate when reaching a suspendable function. The flow will also exit if it is currently suspended:

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

A killed flow running this code will exit when it reaches the next `sendAndReceive`, or immediately if the flow is already suspended by the `sendAndReceive` call.

If your flow has functions that are not marked as `@Suspendable`, you may need to check the status of the flow manually to cooperate with the kill flow request - add a check on the `isKilled` flag of the flow:


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

The function in the example above exits the loop by checking the `isKilled` flag and throws an exception if the flow has been killed.

There are two overloads of `checkFlowIsNotKilled` that simplify the code above:

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
