---
aliases:
- /head/api-transactions.html
- /HEAD/api-transactions.html
- /api-transactions.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-api-transactions
    parent: corda-os-4-8-corda-api
    weight: 300
tags:
- api
- transactions
title: 'API: Transactions'
---




# API: Transactions

The Transactions API is [blurb]

{{< note >}}
Before reading this page, familiarize yourself with the key concepts of [Transactions](key-concepts-transactions.md).

See also [Reissuing states](reissuing-states.md) with a guaranteed state replacement, which allows you to break transaction backchains.
{{< /note >}}


## Transaction lifecycle

Transactions occupy three states between creation and final inclusion on the ledger:

* `TransactionBuilder`. A transaction’s initial state. This is the only state during which the transaction is
mutable, so you must add all the required components before moving on.
* `SignedTransaction`. The transaction now has one or more digital signatures, making it immutable. This is the
transaction type that is passed around to collect additional signatures and that is recorded on the ledger.
* `LedgerTransaction`. The transaction has been “resolved” - for example, its inputs have been converted from
references to actual states - allowing the transaction to be fully inspected.

The transitions between the three stages are as follows:

{{< figure alt="transaction flow" width=80% zoom="/en/images/transaction-flow.png" >}}

## Transaction components

A transaction consists of six types of components:


* 1+ states:
    * 0+ input states
    * 0+ output states
    * 0+ reference input states


* 1+ commands
* 0+ attachments
* 0 or 1 time-window
    * A transaction with a time-window must also have a notary



Each component corresponds to a specific class in the Corda API. The following section describes each component class,
and how it is created.


### Input states

An input state is added to a transaction as a `StateAndRef`, which combines:

* The `ContractState` itself
* A `StateRef` identifying this `ContractState` as the output of a specific transaction

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourStateAndRef: StateAndRef<DummyState> = serviceHub.toStateAndRef<DummyState>(ourStateRef)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
StateAndRef ourStateAndRef = getServiceHub().toStateAndRef(ourStateRef);

```
{{% /tab %}}

{{< /tabs >}}

A `StateRef` uniquely identifies an input state. The notary then uses it to mark the input state as historic. A ```StatRef``` is made up of:

* The hash of the transaction that generated the state
* The state’s index in the outputs of that transaction

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourStateRef: StateRef = StateRef(SecureHash.sha256("DummyTransactionHash"), 0)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
StateRef ourStateRef = new StateRef(SecureHash.sha256("DummyTransactionHash"), 0);

```
{{% /tab %}}

{{< /tabs >}}

The `StateRef` links an input state back to the transaction that created it. Transactions form
“chains” linking each input back to an original issuance transaction. Nodes verifying a transaction
“walk the chain” to verify that each input was generated through a valid sequence of transactions.


#### Reference input states


{{< warning >}}
Reference states are only available on Corda networks with a minimum platform version >= 4.

{{< /warning >}}


The reference input state is represented by the `ReferencedStateAndRef` object. It is
obtained from the `StateAndRef` by calling `StateAndRef.referenced()`.

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
val referenceState: ReferencedStateAndRef<DummyState> = ourStateAndRef.referenced()

```
{{% /tab %}}



{{% tab name="java" %}}
```java
ReferencedStateAndRef referenceState = ourStateAndRef.referenced();

```
{{% /tab %}}

{{< /tabs >}}

**Handling of update races:**

When applied to a flow which uses reference states, the
`WithReferencedStatesFlow` executes a flow as a subFlow. If the flow fails due to a `NotaryError.Conflict`
for a reference state, then it will be suspended until the state refs for the reference states are consumed. In this
case, a consumption means that:

* The owner of the reference state has updated the state with a valid, notarized transaction.
* The owner of the reference state has shared the update with the node attempting to run the flow which uses the
reference state.
* The node has successfully committed the transaction updating the reference state (and all the dependencies), and
added the updated reference state to the vault.

At the point where the transaction updating the state being used as a reference is committed to storage and the vault
update occurs, then the `WithReferencedStatesFlow` wakes up and re-executes the provided flow.

When notarization failure occurs, it is most likely
because the creator of the reference state in your transaction has updated the said state.
The creator ordinarily implements flows for syndicating updates out to users, but these flows can be affected by the communication
delay between the use of a state and the node processing this use. `WithReferenceStatesFlow` is a way to navigate this issue.

{{< warning >}}
This flow facilitates automated re-running of flows which use
reference states. The flow using reference states should include checks to ensure that the reference data is
reasonable, especially if the economics of the transaction depends upon the data contained within a reference state.
{{< /warning >}}

### Output states

A transaction's output states cannot be used as the reference of a previous transaction's outputs. This is because the output
states do not exist until the transaction is committed. Instead, desired output states are created as `ContractState` instances, and
added to the transaction directly:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourOutputState: DummyState = DummyState()

```
{{% /tab %}}



{{% tab name="java" %}}
```java
DummyState ourOutputState = new DummyState();

```
{{% /tab %}}

{{< /tabs >}}

In cases where an output state is an update of an input state, you may want to create the output state by basing
it on that input state:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourOtherOutputState: DummyState = ourOutputState.copy(magicNumber = 77)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
DummyState ourOtherOutputState = ourOutputState.copy(77);

```
{{% /tab %}}

{{< /tabs >}}

A output state must be associated with a contract before it can be added to a transaction.
Wrapping the output state in a `StateAndContract` is the way to do this. This combines:

* The `ContractState` representing the output states
* A `String` identifying the contract governing the state

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
val  ourOutput: StateAndContract = StateAndContract(ourOutputState, DummyContract.PROGRAM_ID)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
StateAndContract ourOutput = new StateAndContract(ourOutputState, DummyContract.PROGRAM_ID);

```
{{% /tab %}}

{{< /tabs >}}


### Commands

A command is added to the transaction as a `Command`, which combines:


* A `CommandData` instance indicating the command’s type
* A `List<PublicKey>` representing the command’s required signers

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
val commandData: DummyContract.Commands.Create = DummyContract.Commands.Create()
val ourPubKey: PublicKey = serviceHub.myInfo.legalIdentitiesAndCerts.first().owningKey
val counterpartyPubKey: PublicKey = counterparty.owningKey
val requiredSigners: List<PublicKey> = listOf(ourPubKey, counterpartyPubKey)
val ourCommand: Command<DummyContract.Commands.Create> = Command(commandData, requiredSigners)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
DummyContract.Commands.Create commandData = new DummyContract.Commands.Create();
PublicKey ourPubKey = getServiceHub().getMyInfo().getLegalIdentitiesAndCerts().get(0).getOwningKey();
PublicKey counterpartyPubKey = counterparty.getOwningKey();
List<PublicKey> requiredSigners = ImmutableList.of(ourPubKey, counterpartyPubKey);
Command<DummyContract.Commands.Create> ourCommand = new Command<>(commandData, requiredSigners);

```
{{% /tab %}}

{{< /tabs >}}


### Attachments

Attachments are identified by their hash:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourAttachment: SecureHash = SecureHash.sha256("DummyAttachment")

```
{{% /tab %}}



{{% tab name="java" %}}
```java
SecureHash ourAttachment = SecureHash.sha256("DummyAttachment");

```
{{% /tab %}}

{{< /tabs >}}

The attachment with the corresponding hash must have been uploaded ahead of time via the node’s RPC interface.


### Time-windows

Time windows represent the period during which the transaction must be notarized. They have a start and an end
time, or may be set as open at either end:

{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourTimeWindow: TimeWindow = TimeWindow.between(Instant.MIN, Instant.MAX)
val ourAfter: TimeWindow = TimeWindow.fromOnly(Instant.MIN)
val ourBefore: TimeWindow = TimeWindow.untilOnly(Instant.MAX)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TimeWindow ourTimeWindow = TimeWindow.between(Instant.MIN, Instant.MAX);
TimeWindow ourAfter = TimeWindow.fromOnly(Instant.MIN);
TimeWindow ourBefore = TimeWindow.untilOnly(Instant.MAX);

```
{{% /tab %}}

{{< /tabs >}}

Time windows can be defined as an `Instant` plus/minus a time tolerance (e.g. 30 seconds):

{{< tabs name="tabs-10" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourTimeWindow2: TimeWindow = TimeWindow.withTolerance(serviceHub.clock.instant(), 30.seconds)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TimeWindow ourTimeWindow2 = TimeWindow.withTolerance(getServiceHub().getClock().instant(), Duration.ofSeconds(30));

```
{{% /tab %}}

{{< /tabs >}}

Or as a start-time plus a duration:

{{< tabs name="tabs-11" >}}
{{% tab name="kotlin" %}}
```kotlin
val ourTimeWindow3: TimeWindow = TimeWindow.fromStartAndDuration(serviceHub.clock.instant(), 30.seconds)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TimeWindow ourTimeWindow3 = TimeWindow.fromStartAndDuration(getServiceHub().getClock().instant(), Duration.ofSeconds(30));

```
{{% /tab %}}

{{< /tabs >}}


## TransactionBuilder


### Creating a builder

The first step when creating a transaction proposal is to instantiate a `TransactionBuilder`.

If the transaction has input states or a time-window, you need to instantiate the builder with a reference to the notary
that will notarize the inputs and verify the time-window:

{{< tabs name="tabs-12" >}}
{{% tab name="kotlin" %}}
```kotlin
val txBuilder: TransactionBuilder = TransactionBuilder(specificNotary)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TransactionBuilder txBuilder = new TransactionBuilder(specificNotary);

```
{{% /tab %}}

{{< /tabs >}}

We discuss the selection of a notary in [API: Flows](api-flows.md).

If the transaction does not have any input states or a time-window, it does not require a notary, and can be
instantiated without one:

{{< tabs name="tabs-13" >}}
{{% tab name="kotlin" %}}
```kotlin
val txBuilderNoNotary: TransactionBuilder = TransactionBuilder()

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TransactionBuilder txBuilderNoNotary = new TransactionBuilder();

```
{{% /tab %}}

{{< /tabs >}}


### Adding items

The next step is to build up the transaction proposal by adding the desired components.

Components are added to the builder using the `TransactionBuilder.withItems` method:

{{< tabs name="tabs-14" >}}
{{% tab name="kotlin" %}}
```kotlin
    /** A more convenient way to add items to this transaction that calls the add* methods for you based on type */
    fun withItems(vararg items: Any) = apply {
        for (t in items) {
            when (t) {
                is StateAndRef<*> -> addInputState(t)
                is ReferencedStateAndRef<*> -> addReferenceState(t)
                is AttachmentId -> addAttachment(t)
                is TransactionState<*> -> addOutputState(t)
                is StateAndContract -> addOutputState(t.state, t.contract)
                is ContractState -> throw UnsupportedOperationException("Removed as of V1: please use a StateAndContract instead")
                is Command<*> -> addCommand(t)
                is CommandData -> throw IllegalArgumentException("You passed an instance of CommandData, but that lacks the pubkey. You need to wrap it in a Command object first.")
                is TimeWindow -> setTimeWindow(t)
                is PrivacySalt -> setPrivacySalt(t)
                else -> throw IllegalArgumentException("Wrong argument type: ${t.javaClass}")
            }
        }
    }

```
{{% /tab %}}




[TransactionBuilder.kt](https://github.com/corda/corda/blob/release/os/4.8/core/src/main/kotlin/net/corda/core/transactions/TransactionBuilder.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

`withItems` takes a `vararg` of objects and adds them to the builder based on their type:


* `StateAndRef` objects are added as input states
* `ReferencedStateAndRef` objects are added as reference input states
* `TransactionState` and `StateAndContract` objects are added as output states
    * Both `TransactionState` and `StateAndContract` are wrappers around a `ContractState` output that link the
output to a specific contract


* `Command` objects are added as commands
* `SecureHash` objects are added as attachments
* A `TimeWindow` object replaces the transaction’s existing `TimeWindow`, if any

Passing in objects of any other type will cause an `IllegalArgumentException` to be thrown.

Here’s an example usage of `TransactionBuilder.withItems`:

{{< tabs name="tabs-15" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.withItems(
        // Inputs, as ``StateAndRef``s that reference the outputs of previous transactions
        ourStateAndRef,
        // Outputs, as ``StateAndContract``s
        ourOutput,
        // Commands, as ``Command``s
        ourCommand,
        // Attachments, as ``SecureHash``es
        ourAttachment,
        // A time-window, as ``TimeWindow``
        ourTimeWindow
)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.withItems(
        // Inputs, as ``StateAndRef``s that reference to the outputs of previous transactions
        ourStateAndRef,
        // Outputs, as ``StateAndContract``s
        ourOutput,
        // Commands, as ``Command``s
        ourCommand,
        // Attachments, as ``SecureHash``es
        ourAttachment,
        // A time-window, as ``TimeWindow``
        ourTimeWindow
);

```
{{% /tab %}}

{{< /tabs >}}

There are also individual methods for adding components.

Here are the methods for adding inputs and attachments:

{{< tabs name="tabs-16" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.addInputState(ourStateAndRef)
txBuilder.addAttachment(ourAttachment)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.addInputState(ourStateAndRef);
txBuilder.addAttachment(ourAttachment);

```
{{% /tab %}}

{{< /tabs >}}

An output state can be added as a `ContractState`, contract class name and notary:

{{< tabs name="tabs-17" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID, specificNotary)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID, specificNotary);

```
{{% /tab %}}

{{< /tabs >}}

If the notary field is left blank, the transaction’s default notary is used:

{{< tabs name="tabs-18" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID);

```
{{% /tab %}}

{{< /tabs >}}

Or you can add the output state as a `TransactionState`, which already specifies the output’s contract and notary:

{{< tabs name="tabs-19" >}}
{{% tab name="kotlin" %}}
```kotlin
val txState: TransactionState<DummyState> = TransactionState(ourOutputState, DummyContract.PROGRAM_ID, specificNotary)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TransactionState txState = new TransactionState(ourOutputState, DummyContract.PROGRAM_ID, specificNotary);

```
{{% /tab %}}

{{< /tabs >}}

Commands can be added as a `Command`:

{{< tabs name="tabs-20" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.addCommand(ourCommand)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.addCommand(ourCommand);

```
{{% /tab %}}

{{< /tabs >}}

Or as `CommandData` and a `vararg PublicKey`:

{{< tabs name="tabs-21" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.addCommand(commandData, ourPubKey, counterpartyPubKey)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.addCommand(commandData, ourPubKey, counterpartyPubKey);

```
{{% /tab %}}

{{< /tabs >}}

For the time-window, you can set a time-window directly:

{{< tabs name="tabs-22" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.setTimeWindow(ourTimeWindow)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.setTimeWindow(ourTimeWindow);

```
{{% /tab %}}

{{< /tabs >}}

Or define the time-window as a time plus a duration (e.g. 45 seconds):

{{< tabs name="tabs-23" >}}
{{% tab name="kotlin" %}}
```kotlin
txBuilder.setTimeWindow(serviceHub.clock.instant(), 45.seconds)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
txBuilder.setTimeWindow(getServiceHub().getClock().instant(), Duration.ofSeconds(45));

```
{{% /tab %}}

{{< /tabs >}}


### Signing the builder

Once the builder is ready, finalize it by signing it and converting it into a `SignedTransaction`.

It is signed with your legal identity key:

{{< tabs name="tabs-24" >}}
{{% tab name="kotlin" %}}
```kotlin
val onceSignedTx: SignedTransaction = serviceHub.signInitialTransaction(txBuilder)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
SignedTransaction onceSignedTx = getServiceHub().signInitialTransaction(txBuilder);

```
{{% /tab %}}

{{< /tabs >}}

You can also choose to use another one of our public keys:

{{< tabs name="tabs-25" >}}
{{% tab name="kotlin" %}}
```kotlin
val otherIdentity: PartyAndCertificate = serviceHub.keyManagementService.freshKeyAndCert(ourIdentityAndCert, false)
val onceSignedTx2: SignedTransaction = serviceHub.signInitialTransaction(txBuilder, otherIdentity.owningKey)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
PartyAndCertificate otherIdentity = getServiceHub().getKeyManagementService().freshKeyAndCert(getOurIdentityAndCert(), false);
SignedTransaction onceSignedTx2 = getServiceHub().signInitialTransaction(txBuilder, otherIdentity.getOwningKey());

```
{{% /tab %}}

{{< /tabs >}}

The outcome of this process is to create an immutable `SignedTransaction` with your signature over it.


## SignedTransaction

A `SignedTransaction` is a combination of:


* An immutable transaction
* A list of signatures over that transaction

{{< tabs name="tabs-26" >}}
{{% tab name="kotlin" %}}
```kotlin
@KeepForDJVM
@CordaSerializable
data class SignedTransaction(val txBits: SerializedBytes<CoreTransaction>,
                             override val sigs: List<TransactionSignature>
) : TransactionWithSignatures {

```
{{% /tab %}}




[SignedTransaction.kt](https://github.com/corda/corda/blob/release/os/4.8/core/src/main/kotlin/net/corda/core/transactions/SignedTransaction.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Before adding your signature to the transaction, verify both the transaction’s contents and the
transaction’s signatures.


### Verifying the transaction’s contents

A transaction is only valid if its dependency chain is also valid. All
the states in the transaction’s dependency chain must be retrieved to verify the transaction’s contents.
In order to do this, request any states in the chain that the node does not currently have in its local storage from the
proposer(s) of the transaction. This process is handled by a built-in flow called `ReceiveTransactionFlow`.
See [API: Flows](api-flows.md) for more details.

Verify the transaction’s contents to ensure that it satisfies the contracts of all the transaction’s input
and output states:

{{< tabs name="tabs-27" >}}
{{% tab name="kotlin" %}}
```kotlin
twiceSignedTx.verify(serviceHub)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
twiceSignedTx.verify(getServiceHub());

```
{{% /tab %}}

{{< /tabs >}}

It is possible to perform additional validation of the transaction contents before signing, to ensure
that the transaction proposal represents an agreement you wish to enter into.

Before this is possible, it is necessary to resolve the `StateRef` and `SecureHash` instances into actual `ContractState` and `Attachment` instances, which
are then inspected. This is because the `SignedTransaction` holds its inputs as `StateRef` instances, and its attachments as `SecureHash`
instances. These alone do not alone provide enough information to properly validate the transaction’s contents.
Resolving these instances requires using the `ServiceHub` to convert the `SignedTransaction` into a `LedgerTransaction`:

{{< tabs name="tabs-28" >}}
{{% tab name="kotlin" %}}
```kotlin
val ledgerTx: LedgerTransaction = twiceSignedTx.toLedgerTransaction(serviceHub)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
LedgerTransaction ledgerTx = twiceSignedTx.toLedgerTransaction(getServiceHub());

```
{{% /tab %}}

{{< /tabs >}}

Additional verification is now possible. Here’s a simple example:

{{< tabs name="tabs-29" >}}
{{% tab name="kotlin" %}}
```kotlin
val outputState: DummyState = ledgerTx.outputsOfType<DummyState>().single()
if (outputState.magicNumber == 777) {
    // ``FlowException`` is a special exception type. It will be
    // propagated back to any counterparty flows waiting for a
    // message from this flow, notifying them that the flow has
    // failed.
    throw FlowException("We expected a magic number of 777.")
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
DummyState outputState = ledgerTx.outputsOfType(DummyState.class).get(0);
if (outputState.getMagicNumber() != 777) {
    // ``FlowException`` is a special exception type. It will be
    // propagated back to any counterparty flows waiting for a
    // message from this flow, notifying them that the flow has
    // failed.
    throw new FlowException("We expected a magic number of 777.");
}

```
{{% /tab %}}

{{< /tabs >}}


### Verifying the transaction’s signatures

Aside from verifying that the transaction’s contents are valid, you also need to check that the signatures are valid. A
valid signature over the hash of the transaction prevents tampering.

To verify that all the transaction’s required signatures are present and valid:

{{< tabs name="tabs-30" >}}
{{% tab name="kotlin" %}}
```kotlin
fullySignedTx.verifyRequiredSignatures()

```
{{% /tab %}}



{{% tab name="java" %}}
```java
fullySignedTx.verifyRequiredSignatures();

```
{{% /tab %}}

{{< /tabs >}}

To verify the transaction’s existing signatures before all of them have been collected use `SignedTransaction.verifySignaturesExcept`, which
takes a `vararg` of the public keys within which the signatures are allowed to be missing:

{{< tabs name="tabs-31" >}}
{{% tab name="kotlin" %}}
```kotlin
onceSignedTx.verifySignaturesExcept(counterpartyPubKey)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
onceSignedTx.verifySignaturesExcept(counterpartyPubKey);

```
{{% /tab %}}

{{< /tabs >}}

There is also an overload of `SignedTransaction.verifySignaturesExcept`, which takes a `Collection` of the
public keys for which the signatures are allowed to be missing:

{{< tabs name="tabs-32" >}}
{{% tab name="kotlin" %}}
```kotlin
onceSignedTx.verifySignaturesExcept(listOf(counterpartyPubKey))

```
{{% /tab %}}



{{% tab name="java" %}}
```java
onceSignedTx.verifySignaturesExcept(singletonList(counterpartyPubKey));

```
{{% /tab %}}

{{< /tabs >}}

If the transaction is missing any signatures without the corresponding public keys being passed in, a
`SignaturesMissingException` is thrown.

You can also choose to simply verify the signatures that are present:

{{< tabs name="tabs-33" >}}
{{% tab name="kotlin" %}}
```kotlin
twiceSignedTx.checkSignaturesAreValid()

```
{{% /tab %}}



{{% tab name="java" %}}
```java
twiceSignedTx.checkSignaturesAreValid();

```
{{% /tab %}}

{{< /tabs >}}

Be very careful, however - this function neither guarantees that the signatures that are present are required, nor
checks whether any signatures are missing.


### Signing the transaction

Once you are satisfied with the contents and existing signatures over the transaction, you add your signature to the
`SignedTransaction` to indicate that you approve the transaction.

You can sign using the legal identity key, as follows:

{{< tabs name="tabs-34" >}}
{{% tab name="kotlin" %}}
```kotlin
val twiceSignedTx: SignedTransaction = serviceHub.addSignature(onceSignedTx)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
SignedTransaction twiceSignedTx = getServiceHub().addSignature(onceSignedTx);

```
{{% /tab %}}

{{< /tabs >}}

Or you can choose to sign using another one of our public keys:

{{< tabs name="tabs-35" >}}
{{% tab name="kotlin" %}}
```kotlin
val twiceSignedTx2: SignedTransaction = serviceHub.addSignature(onceSignedTx, otherIdentity2.owningKey)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
SignedTransaction twiceSignedTx2 = getServiceHub().addSignature(onceSignedTx, otherIdentity2.getOwningKey());

```
{{% /tab %}}

{{< /tabs >}}

You can also generate a signature over the transaction without adding it to the transaction directly.

This is done using the legal identity key:

{{< tabs name="tabs-36" >}}
{{% tab name="kotlin" %}}
```kotlin
val sig: TransactionSignature = serviceHub.createSignature(onceSignedTx)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TransactionSignature sig = getServiceHub().createSignature(onceSignedTx);

```
{{% /tab %}}

{{< /tabs >}}

Or using another one of the public keys:

{{< tabs name="tabs-37" >}}
{{% tab name="kotlin" %}}
```kotlin
val sig2: TransactionSignature = serviceHub.createSignature(onceSignedTx, otherIdentity2.owningKey)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
TransactionSignature sig2 = getServiceHub().createSignature(onceSignedTx, otherIdentity2.getOwningKey());

```
{{% /tab %}}

{{< /tabs >}}


### Notarising and recording

Notarising and recording a transaction is handled by a built-in flow called `FinalityFlow`. See [API: Flows](api-flows.md) for
more details.
