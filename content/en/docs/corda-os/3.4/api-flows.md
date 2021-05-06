---
aliases:
- /releases/release-V3.4/api-flows.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-4:
    identifier: corda-os-3-4-api-flows
    parent: corda-os-3-4-corda-api
    weight: 1070
tags:
- api
- flows
title: 'API: Flows'
---




# API: Flows

{{< note >}}
Before reading this page, you should be familiar with the key concepts of [Flows](key-concepts-flows.md).

{{< /note >}}


## An example flow

Before we discuss the API offered by the flow, let’s consider what a standard flow may look like.

Imagine a flow for agreeing a basic ledger update between Alice and Bob. This flow will have two sides:


* An `Initiator` side, that will initiate the request to update the ledger
* A `Responder` side, that will respond to the request to update the ledger


### Initiator

In our flow, the Initiator flow class will be doing the majority of the work:

*Part 1 - Build the transaction*


* Choose a notary for the transaction
* Create a transaction builder
* Extract any input states from the vault and add them to the builder
* Create any output states and add them to the builder
* Add any commands, attachments and timestamps to the builder

*Part 2 - Sign the transaction*


* Sign the transaction builder
* Convert the builder to a signed transaction

*Part 3 - Verify the transaction*


* Verify the transaction by running its contracts

*Part 4 - Gather the counterparty’s signature*


* Send the transaction to the counterparty
* Wait to receive back the counterparty’s signature
* Add the counterparty’s signature to the transaction
* Verify the transaction’s signatures

*Part 5 - Finalize the transaction*


* Send the transaction to the notary
* Wait to receive back the notarised transaction
* Record the transaction locally
* Store any relevant states in the vault
* Send the transaction to the counterparty for recording

We can visualize the work performed by initiator as follows:

![flow overview](/en/images/flow-overview.png "flow overview")

### Responder

To respond to these actions, the responder takes the following steps:

*Part 1 - Sign the transaction*


* Receive the transaction from the counterparty
* Verify the transaction’s existing signatures
* Verify the transaction by running its contracts
* Generate a signature over the transaction
* Send the signature back to the counterparty

*Part 2 - Record the transaction*


* Receive the notarised transaction from the counterparty
* Record the transaction locally
* Store any relevant states in the vault


## FlowLogic

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


## FlowLogic annotations

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


## Call

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


## ServiceHub

Within `FlowLogic.call`, the flow developer has access to the node’s `ServiceHub`, which provides access to the
various services the node provides. We will use the `ServiceHub` extensively in the examples that follow. You can
also see [API: ServiceHub](api-service-hub.md) for information about the services the `ServiceHub` offers.


## Common flow tasks

There are a number of common tasks that you will need to perform within `FlowLogic.call` in order to agree ledger
updates. This section details the API for common tasks.


### Transaction building

The majority of the work performed during a flow will be to build, verify and sign a transaction. This is covered
in [API: Transactions](api-transactions.md).


### Extracting states from the vault

When building a transaction, you’ll often need to extract the states you wish to consume from the vault. This is
covered in [API: Vault Query](api-vault-query.md).


### Retrieving information about other nodes

We can retrieve information about other nodes on the network and the services they offer using
`ServiceHub.networkMapCache`.


#### Notaries

Remember that a transaction generally needs a notary to:


* Prevent double-spends if the transaction has inputs
* Serve as a timestamping authority if the transaction has a time-window

There are several ways to retrieve a notary from the network map:

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
Party specificNotary = getServiceHub().getNetworkMapCache().getNotary(notaryName);
// Alternatively, we can pick an arbitrary notary from the notary
// list. However, it is always preferable to specify the notary
// explicitly, as the notary list might change when new notaries are
// introduced, or old ones decommissioned.
Party firstNotary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0);

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


#### Specific counterparties

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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


### Communication between parties

In order to create a communication session between your initiator flow and the receiver flow you must call
`initiateFlow(party: Party): FlowSession`

`FlowSession` instances in turn provide three functions:


* `send(payload: Any)`
    * Sends the `payload` object


* `receive(receiveType: Class<R>): R`
    * Receives an object of type `receiveType`


* `sendAndReceive(receiveType: Class<R>, payload: Any): R`
    * Sends the `payload` object and receives an object of type `receiveType` back



In addition `FlowLogic` provides functions that batch receives:
* `receiveAllMap(sessions: Map<FlowSession, Class<out Any>>): Map<FlowSession, UntrustworthyData<Any>>`



* Receives from all
{{< warning >}}``{{< /warning >}}

FlowSession``s specified in the passed in map. The received types may differ.



* `receiveAll(receiveType: Class<R>, sessions: List<FlowSession>): List<UntrustworthyData<R>>`
    * Receives from all
{{< warning >}}``{{< /warning >}}

FlowSession``s specified in the passed in list. The received types must be the same.



The batched functions are implemented more efficiently by the flow framework.


#### InitiateFlow

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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Note that at the time of call to this function no actual communication is done, this is deferred to the first
send/receive, at which point the counterparty will either:


* Ignore the message if they are not registered to respond to messages from this flow.
* Start the flow they have registered to respond to this flow.


#### Send

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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

The flow on the other side must eventually reach a corresponding `receive` call to get this message.


#### Receive

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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


{{< warning >}}
If you initiate several flows from the same `@InitiatingFlow` flow then on the receiving side you must be
prepared to be initiated by any of the corresponding `initiateFlow()` calls! A good way of handling this ambiguity
is to send as a first message a “role” message to the initiated flow, indicating which part of the initiating flow
the rest of the counter-flow should conform to. For example send an enum, and on the other side start with a switch
statement.

{{< /warning >}}



#### SendAndReceive

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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


#### Counterparty response

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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


### Why sessions?

Before `FlowSession` s were introduced the send/receive API looked a bit different. They were functions on
`FlowLogic` and took the address `Party` as argument. The platform internally maintained a mapping from `Party` to
session, hiding sessions from the user completely.

Although this is a convenient API it introduces subtle issues where a message that was originally meant for a specific
session may end up in another.

Consider the following contrived example using the old `Party` based API:

{{< tabs name="tabs-13" >}}
{{% tab name="kotlin" %}}
```kotlin
@InitiatingFlow
class LaunchSpaceshipFlow : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val shouldLaunchSpaceship = receive<Boolean>(getPresident()).unwrap { it }
        if (shouldLaunchSpaceship) {
            launchSpaceship()
        }
    }

    fun launchSpaceship() {
    }

    fun getPresident(): Party {
        TODO()
    }
}

@InitiatedBy(LaunchSpaceshipFlow::class)
@InitiatingFlow
class PresidentSpaceshipFlow(val launcher: Party) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val needCoffee = true
        send(getSecretary(), needCoffee)
        val shouldLaunchSpaceship = false
        send(launcher, shouldLaunchSpaceship)
    }

    fun getSecretary(): Party {
        TODO()
    }
}

@InitiatedBy(PresidentSpaceshipFlow::class)
class SecretaryFlow(val president: Party) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        // ignore
    }
}

```
{{% /tab %}}




[LaunchSpaceshipFlow.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/LaunchSpaceshipFlow.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

The intention of the flows is very clear: LaunchSpaceshipFlow asks the president whether a spaceship should be launched.
It is expecting a boolean reply. The president in return first tells the secretary that they need coffee, which is also
communicated with a boolean. Afterwards the president replies to the launcher that they don’t want to launch.

However the above can go horribly wrong when the `launcher` happens to be the same party `getSecretary` returns. In
this case the boolean meant for the secretary will be received by the launcher!

This indicates that `Party` is not a good identifier for the communication sequence, and indeed the `Party` based
API may introduce ways for an attacker to fish for information and even trigger unintended control flow like in the
above case.

Hence we introduced `FlowSession`, which identifies the communication sequence. With `FlowSession` s the above set
of flows would look like this:

{{< tabs name="tabs-14" >}}
{{% tab name="kotlin" %}}
```kotlin
@InitiatingFlow
class LaunchSpaceshipFlowCorrect : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val presidentSession = initiateFlow(getPresident())
        val shouldLaunchSpaceship = presidentSession.receive<Boolean>().unwrap { it }
        if (shouldLaunchSpaceship) {
            launchSpaceship()
        }
    }

    fun launchSpaceship() {
    }

    fun getPresident(): Party {
        TODO()
    }
}

@InitiatedBy(LaunchSpaceshipFlowCorrect::class)
@InitiatingFlow
class PresidentSpaceshipFlowCorrect(val launcherSession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val needCoffee = true
        val secretarySession = initiateFlow(getSecretary())
        secretarySession.send(needCoffee)
        val shouldLaunchSpaceship = false
        launcherSession.send(shouldLaunchSpaceship)
    }

    fun getSecretary(): Party {
        TODO()
    }
}

@InitiatedBy(PresidentSpaceshipFlowCorrect::class)
class SecretaryFlowCorrect(val presidentSession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        // ignore
    }
}

```
{{% /tab %}}




[LaunchSpaceshipFlow.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/LaunchSpaceshipFlow.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Note how the president is now explicit about which session it wants to send to.


### Porting from the old Party-based API

In the old API the first `send` or `receive` to a `Party` was the one kicking off the counter-flow. This is now
explicit in the `initiateFlow` function call. To port existing code:

{{< tabs name="tabs-15" >}}
{{% tab name="kotlin" %}}
```kotlin
send(regulator, Any()) // Old API
// becomes
val session = initiateFlow(regulator)
session.send(Any())

```
{{% /tab %}}



{{% tab name="java" %}}
```java
send(regulator, new Object()); // Old API
// becomes
FlowSession session = initiateFlow(regulator);
session.send(new Object());

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

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

### Core initiating subflows

Corda-provided initiating subflows are a little different to standard ones as they are versioned together with the
platform, and their initiated counter-flows are registered explicitly, so there is no need for the `InitiatedBy`
annotation.

An example is the `FinalityFlow`/`FinalityHandler` flow pair.


### Built-in subflows

Corda provides a number of built-in flows that should be used for handling common tasks. The most important are:


* `CollectSignaturesFlow` (inlined), which should be used to collect a transaction’s required signatures
* `FinalityFlow` (initiating), which should be used to notarise and record a transaction as well as to broadcast it to
all relevant parties
* `SendTransactionFlow` (inlined), which should be used to send a signed transaction if it needed to be resolved on
the other side.
* `ReceiveTransactionFlow` (inlined), which should be used receive a signed transaction
* `ContractUpgradeFlow` (initiating), which should be used to change a state’s contract
* `NotaryChangeFlow` (initiating), which should be used to change a state’s notary

Let’s look at three very common examples.


### FinalityFlow

`FinalityFlow` allows us to notarise the transaction and get it recorded in the vault of the participants of all
the transaction’s states:

{{< tabs name="tabs-16" >}}
{{% tab name="kotlin" %}}
```kotlin
val notarisedTx1: SignedTransaction = subFlow(FinalityFlow(fullySignedTx, FINALISATION.childProgressTracker()))

```
{{% /tab %}}



{{% tab name="java" %}}
```java
SignedTransaction notarisedTx1 = subFlow(new FinalityFlow(fullySignedTx, FINALISATION.childProgressTracker()));

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

We can also choose to send the transaction to additional parties who aren’t one of the state’s participants:

{{< tabs name="tabs-17" >}}
{{% tab name="kotlin" %}}
```kotlin
val additionalParties: Set<Party> = setOf(regulator)
val notarisedTx2: SignedTransaction = subFlow(FinalityFlow(fullySignedTx, additionalParties, FINALISATION.childProgressTracker()))

```
{{% /tab %}}



{{% tab name="java" %}}
```java
Set<Party> additionalParties = Collections.singleton(regulator);
SignedTransaction notarisedTx2 = subFlow(new FinalityFlow(fullySignedTx, additionalParties, FINALISATION.childProgressTracker()));

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Only one party has to call `FinalityFlow` for a given transaction to be recorded by all participants. It does
**not** need to be called by each participant individually.


### CollectSignaturesFlow/SignTransactionFlow

The list of parties who need to sign a transaction is dictated by the transaction’s commands. Once we’ve signed a
transaction ourselves, we can automatically gather the signatures of the other required signers using
`CollectSignaturesFlow`:

{{< tabs name="tabs-18" >}}
{{% tab name="kotlin" %}}
```kotlin
val fullySignedTx: SignedTransaction = subFlow(CollectSignaturesFlow(twiceSignedTx, setOf(counterpartySession, regulatorSession), SIGS_GATHERING.childProgressTracker()))

```
{{% /tab %}}



{{% tab name="java" %}}
```java
SignedTransaction fullySignedTx = subFlow(new CollectSignaturesFlow(twiceSignedTx, Collections.emptySet(), SIGS_GATHERING.childProgressTracker()));

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Each required signer will need to respond by invoking its own `SignTransactionFlow` subclass to check the
transaction and provide their signature if they are satisfied:

{{< tabs name="tabs-19" >}}
{{% tab name="kotlin" %}}
```kotlin
val signTransactionFlow: SignTransactionFlow = object : SignTransactionFlow(counterpartySession) {
    override fun checkTransaction(stx: SignedTransaction) = requireThat {
        // Any additional checking we see fit...
        val outputState = stx.tx.outputsOfType<DummyState>().single()
        assert(outputState.magicNumber == 777)
    }
}

subFlow(signTransactionFlow)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
class SignTxFlow extends SignTransactionFlow {
    private SignTxFlow(FlowSession otherSession, ProgressTracker progressTracker) {
        super(otherSession, progressTracker);
    }

    @Override
    protected void checkTransaction(SignedTransaction stx) {
        requireThat(require -> {
            // Any additional checking we see fit...
            DummyState outputState = (DummyState) stx.getTx().getOutputs().get(0).getData();
            assert (outputState.getMagicNumber() == 777);
            return null;
        });
    }
}

subFlow(new SignTxFlow(counterpartySession, SignTransactionFlow.tracker()));

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


### SendTransactionFlow/ReceiveTransactionFlow

Verifying a transaction received from a counterparty also requires verification of every transaction in its
dependency chain. This means the receiving party needs to be able to ask the sender all the details of the chain.
The sender will use `SendTransactionFlow` for sending the transaction and then for processing all subsequent
transaction data vending requests as the receiver walks the dependency chain using `ReceiveTransactionFlow`:

{{< tabs name="tabs-20" >}}
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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

We can receive the transaction using `ReceiveTransactionFlow`, which will automatically download all the
dependencies and verify the transaction:

{{< tabs name="tabs-21" >}}
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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

We can also send and receive a `StateAndRef` dependency chain and automatically resolve its dependencies:

{{< tabs name="tabs-22" >}}
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
List<StateAndRef<DummyState>> resolvedStateAndRef = subFlow(new ReceiveStateAndRefFlow<DummyState>(counterpartySession));

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


### Why inlined subflows?

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

{{< tabs name="tabs-23" >}}
{{% tab name="kotlin" %}}
```kotlin
/**
 * Exception which can be thrown by a [FlowLogic] at any point in its logic to unexpectedly bring it to a permanent end.
 * The exception will propagate to all counterparty flows and will be thrown on their end the next time they wait on a
 * [FlowSession.receive] or [FlowSession.sendAndReceive]. Any flow which no longer needs to do a receive, or has already ended,
 * will not receive the exception (if this is required then have them wait for a confirmation message).
 *
 * [FlowException] (or a subclass) can be a valid expected response from a flow, particularly ones which act as a service.
 * It is recommended a [FlowLogic] document the [FlowException] types it can throw.
 */
open class FlowException(message: String?, cause: Throwable?) : CordaException(message, cause) {
    constructor(message: String?) : this(message, null)
    constructor(cause: Throwable?) : this(cause?.toString(), cause)
    constructor() : this(null, null)
}

```
{{% /tab %}}




[FlowException.kt](https://github.com/corda/corda/blob/release/os/3.4/core/src/main/kotlin/net/corda/core/flows/FlowException.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

The flow framework will automatically propagate the `FlowException` back to the waiting counterparties.

There are many scenarios in which throwing a `FlowException` would be appropriate:


* A transaction doesn’t `verify()`
* A transaction’s signatures are invalid
* The transaction does not match the parameters of the deal as discussed
* You are reneging on a deal


## ProgressTracker

We can give our flow a progress tracker. This allows us to see the flow’s progress visually in our node’s CRaSH shell.

To provide a progress tracker, we have to override `FlowLogic.progressTracker` in our flow:

{{< tabs name="tabs-24" >}}
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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

We then update the progress tracker’s current step as we progress through the flow as follows:

{{< tabs name="tabs-25" >}}
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




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/kotlin/net/corda/docs/FlowCookbook.kt) | [FlowCookbookJava.java](https://github.com/corda/corda/blob/release/os/3.4/docs/source/example-code/src/main/java/net/corda/docs/FlowCookbookJava.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


## Concurrency, Locking and Waiting

This is an advanced topic.  Because Corda is designed to:


* run many flows in parallel,
* may persist flows to storage and resurrect those flows much later,
* (in the future) migrate flows between JVMs,

flows should avoid use of locks and typically not even attempt to interact with objects shared between flows (except
`ServiceHub` and other carefully crafted services such as Oracles.  See [Writing oracle services](oracles.md)).
Locks will significantly reduce the scalability of the node, in the best case, and can cause the node to deadlock if they
remain locked across flow context switch boundaries (such as sending and receiving
from peers discussed above, and the sleep discussed below).

If you need activities that are scheduled, you should investigate the use of `SchedulableState`.
However, we appreciate that Corda support for some more advanced patterns is still in the future, and if there is a need
for brief pauses in flows then you should use `FlowLogic.sleep` in place of where you might have used `Thread.sleep`.
Flows should expressly not use `Thread.sleep`, since this will prevent the node from processing other flows
in the meantime, significantly impairing the performance of the node.
Even `FlowLogic.sleep` is not to be used to create long running flows, since the Corda ethos is for short lived flows
(otherwise upgrading nodes or CorDapps is much more complicated), or as a substitute to using the `SchedulableState` scheduler.

Currently the `finance` package uses `FlowLogic.sleep` to make several attempts at coin selection, where necessary,
when many states are soft locked and we wish to wait for those, or other new states in their place, to become unlocked.


```kotlin
for (retryCount in 1..MAX_RETRIES) {
    if (!attemptSpend(services, amount, lockId, notary, onlyFromIssuerParties, withIssuerRefs, stateAndRefs)) {
        log.warn("Coin selection failed on attempt $retryCount")
        // TODO: revisit the back off strategy for contended spending.
        if (retryCount != MAX_RETRIES) {
            stateAndRefs.clear()
            val durationMillis = (minOf(RETRY_SLEEP.shl(retryCount), RETRY_CAP / 2) * (1.0 + Math.random())).toInt()
            FlowLogic.sleep(durationMillis.millis)
        } else {
            log.warn("Insufficient spendable states identified for $amount")
        }
    } else {
        break
    }
}

```

[AbstractCashSelection.kt](https://github.com/corda/corda/blob/release/os/3.4/finance/src/main/kotlin/net/corda/finance/contracts/asset/cash/selection/AbstractCashSelection.kt)
