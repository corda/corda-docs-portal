---
aliases:
- /releases/4.3/tutorial-building-transactions.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-tutorial-building-transactions
    parent: corda-enterprise-4-3-tutorials-index
    weight: 1090
tags:
- tutorial
- building
- transactions
title: Building transactions
---


# Building transactions


## Introduction

Understanding and implementing transactions in Corda is key to building
and implementing real world smart contracts. It is only through
construction of valid Corda transactions containing appropriate data
that nodes on the ledger can map real world business objects into a
shared digital view of the data in the Corda ledger. More importantly as
the developer of new smart contracts it is the code which determines
what data is well formed and what data should be rejected as mistakes,
or to prevent malicious activity. This document details some of the
considerations and APIs used to when constructing transactions as part
of a flow.


## The Basic Lifecycle Of Transactions

Transactions in Corda contain a number of elements:


* A set of Input state references that will be consumed by the final
accepted transaction
* A set of Output states to create/replace the consumed states and thus
become the new latest versions of data on the ledger
* A set of `Attachment` items which can contain legal documents, contract
code, or private encrypted sections as an extension beyond the native
contract states
* A set of `Command` items which indicate the type of ledger
transition that is encoded in the transaction. Each command also has an
associated set of signer keys, which will be required to sign the
transaction
* A signers list, which is the union of the signers on the individual
Command objects
* A notary identity to specify which notary node is tracking the
state consumption (if the transaction’s input states are registered with different
notary nodes the flow will have to insert additional `NotaryChange`
transactions to migrate the states across to a consistent notary node
before being allowed to mutate any states)
* Optionally a time-window that can used by the notary to bound the
period during which the proposed transaction can be committed to the
ledger

A transaction is built by populating a `TransactionBuilder`. Once the builder is fully populated, the flow should freeze the `TransactionBuilder` by signing it to create a `SignedTransaction`. This is key to the ledger agreement process - once a flow has attached a node’s signature to a transaction, it has effectively stated that it accepts all the details of the transaction.

It is best practice for flows to receive back the `TransactionSignature` of other parties rather than a full
`SignedTransaction` objects, because otherwise we have to separately check that this is still the same
`SignedTransaction` and not a malicious substitute.

The final stage of committing the transaction to the ledger is to notarise the `SignedTransaction`, distribute it to
all appropriate parties and record the data into the ledger. These actions are best delegated to the `FinalityFlow`,
rather than calling the individual steps manually. However, do note that the final broadcast to the other nodes is
asynchronous, so care must be used in unit testing to correctly await the vault updates.


## Gathering Inputs

One of the first steps to forming a transaction is gathering the set of
input references. This process will clearly vary according to the nature
of the business process being captured by the smart contract and the
parameterised details of the request. However, it will generally involve
searching the vault via the `VaultService` interface on the
`ServiceHub` to locate the input states.

To give a few more specific details consider two simplified real world
scenarios. First, a basic foreign exchange cash transaction. This
transaction needs to locate a set of funds to exchange. A flow
modelling this is implemented in `FxTransactionBuildTutorial.kt`
(in the [main Corda repo](https://github.com/corda/corda)).
Second, a simple business model in which parties manually accept or
reject each other’s trade proposals, which is implemented in
`WorkflowTransactionBuildTutorial.kt` (in the
[main Corda repo](https://github.com/corda/corda)). To run and explore these
examples using the IntelliJ IDE one can run/step through the respective unit
tests in `FxTransactionBuildTutorialTest.kt` and
`WorkflowTransactionBuildTutorialTest.kt`, which drive the flows as
part of a simulated in-memory network of nodes.

{{< note >}}
Before creating the IntelliJ run configurations for these unit tests
go to Run -> Edit Configurations -> Defaults -> JUnit, add
`-javaagent:lib/quasar.jar`
to the VM options, and set Working directory to `$PROJECT_DIR$`
so that the `Quasar` instrumentation is correctly configured.

{{< /note >}}
For the cash transaction, let’s assume we are using the
standard `CashState` in the `:financial` Gradle module. The `Cash`
contract uses `FungibleAsset` states to model holdings of
interchangeable assets and allow the splitting, merging and summing of
states to meet a contractual obligation. We would normally use the
`Cash.generateSpend` method to gather the required
amount of cash into a `TransactionBuilder`, set the outputs and generate the `Move`
command. However, to make things clearer, the example flow code shown
here will manually carry out the input queries by specifying relevant
query criteria filters to the `tryLockFungibleStatesForSpending` method
of the `VaultService`.

```kotlin
// This is equivalent to the Cash.generateSpend
// Which is brought here to make the filtering logic more visible in the example
private fun gatherOurInputs(serviceHub: ServiceHub,
                            lockId: UUID,
                            amountRequired: Amount<Issued<Currency>>,
                            notary: Party?): Pair<List<StateAndRef<Cash.State>>, Long> {
    // extract our identity for convenience
    val ourKeys = serviceHub.keyManagementService.keys
    val ourParties = ourKeys.map { serviceHub.identityService.partyFromKey(it) ?: throw IllegalStateException("Unable to resolve party from key") }
    val fungibleCriteria = QueryCriteria.FungibleAssetQueryCriteria(owner = ourParties)

    val notaries = notary ?: serviceHub.networkMapCache.notaryIdentities.first()
    val vaultCriteria: QueryCriteria = QueryCriteria.VaultQueryCriteria(notary = listOf(notaries as AbstractParty))

    val logicalExpression = builder { CashSchemaV1.PersistentCashState::currency.equal(amountRequired.token.product.currencyCode) }
    val cashCriteria = QueryCriteria.VaultCustomQueryCriteria(logicalExpression)

    val fullCriteria = fungibleCriteria.and(vaultCriteria).and(cashCriteria)

    val eligibleStates = serviceHub.vaultService.tryLockFungibleStatesForSpending(lockId, fullCriteria, amountRequired.withoutIssuer(), Cash.State::class.java)

    check(eligibleStates.isNotEmpty()) { "Insufficient funds" }
    val amount = eligibleStates.fold(0L) { tot, (state) -> tot + state.data.amount.quantity }
    val change = amount - amountRequired.quantity

    return Pair(eligibleStates, change)
}

```

[FxTransactionBuildTutorial.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FxTransactionBuildTutorial.kt)

This is a foreign exchange transaction, so we expect another set of input states of another currency from a
counterparty. However, the Corda privacy model means we are not aware of the other node’s states. Our flow must
therefore ask the other node to carry out a similar query and return the additional inputs to the transaction (see the
`ForeignExchangeFlow` for more details of the exchange). We now have all the required input `StateRef` items, and
can turn to gathering the outputs.

For the trade approval flow we need to implement a simple workflow
pattern. We start by recording the unconfirmed trade details in a state
object implementing the `LinearState` interface. One field of this
record is used to map the business workflow to an enumerated state.
Initially the initiator creates a new state object which receives a new
`UniqueIdentifier` in its `linearId` property and a starting
workflow state of `NEW`. The `Contract.verify` method is written to
allow the initiator to sign this initial transaction and send it to the
other party. This pattern ensures that a permanent copy is recorded on
both ledgers for audit purposes, but the state is prevented from being
maliciously put in an approved state. The subsequent workflow steps then
follow with transactions that consume the state as inputs on one side
and output a new version with whatever state updates, or amendments
match to the business process, the `linearId` being preserved across
the changes. Attached `Command` objects help the verify method
restrict changes to appropriate fields and signers at each step in the
workflow. In this it is typical to have both parties sign the change
transactions, but it can be valid to allow unilateral signing, if for instance
one side could block a rejection. Commonly the manual initiator of these
workflows will query the Vault for states of the right contract type and
in the right workflow state over the RPC interface. The RPC will then
initiate the relevant flow using `StateRef`, or `linearId` values as
parameters to the flow to identify the states being operated upon. Thus
code to gather the latest input state for a given `StateRef` would use
the `VaultService` as follows:

```kotlin
val criteria = VaultQueryCriteria(stateRefs = listOf(ref))
val latestRecord = serviceHub.vaultService.queryBy<TradeApprovalContract.State>(criteria).states.single()

```

[WorkflowTransactionBuildTutorial.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/txbuild/WorkflowTransactionBuildTutorial.kt)


## Generating Commands

For the commands that will be added to the transaction, these will need
to correctly reflect the task at hand. These must match because inside
the `Contract.verify` method the command will be used to select the
validation code path. The `Contract.verify` method will then restrict
the allowed contents of the transaction to reflect this context. Typical
restrictions might include that the input cash amount must equal the
output cash amount, or that a workflow step is only allowed to change
the status field. Sometimes, the command may capture some data too e.g.
the foreign exchange rate, or the identity of one party, or the StateRef
of the specific input that originates the command in a bulk operation.
This data will be used to further aid the `Contract.verify`, because
to ensure consistent, secure and reproducible behaviour in a distributed
environment the `Contract.verify`, transaction is the only allowed to
use the content of the transaction to decide validity.

Another essential requirement for commands is that the correct set of
`PublicKey` objects are added to the `Command` on the builder, which will be
used to form the set of required signers on the final validated
transaction. These must correctly align with the expectations of the
`Contract.verify` method, which should be written to defensively check
this. In particular, it is expected that at minimum the owner of an
asset would have to be signing to permission transfer of that asset. In
addition, other signatories will often be required e.g. an Oracle
identity for an Oracle command, or both parties when there is an
exchange of assets.


## Generating Outputs

Having located a `StateAndRefs` set as the transaction inputs, the
flow has to generate the output states. Typically, this is a simple call
to the Kotlin `copy` method to modify the few fields that will
transitioned in the transaction. The contract code may provide a
`generateXXX` method to help with this process if the task is more
complicated. With a workflow state a slightly modified copy state is
usually sufficient, especially as it is expected that we wish to preserve
the `linearId` between state revisions, so that Vault queries can find
the latest revision.

For fungible contract states such as `cash` it is common to distribute
and split the total amount e.g. to produce a remaining balance output
state for the original owner when breaking up a large amount input
state. Remember that the result of a successful transaction is always to
fully consume/spend the input states, so this is required to conserve
the total cash. For example from the demo code:

```kotlin
// Gather our inputs. We would normally use VaultService.generateSpend
// to carry out the build in a single step. To be more explicit
// we will use query manually in the helper function below.
// Putting this into a non-suspendable function also prevents issues when
// the flow is suspended.
val (inputs, residual) = gatherOurInputs(serviceHub, lockId, sellAmount, request.notary)

// Build and an output state for the counterparty
val transferredFundsOutput = Cash.State(sellAmount, request.counterparty)

val outputs = if (residual > 0L) {
    // Build an output state for the residual change back to us
    val residualAmount = Amount(residual, sellAmount.token)
    val residualOutput = Cash.State(residualAmount, serviceHub.myInfo.singleIdentity())
    listOf(transferredFundsOutput, residualOutput)
} else {
    listOf(transferredFundsOutput)
}
return Pair(inputs, outputs)

```

[FxTransactionBuildTutorial.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FxTransactionBuildTutorial.kt)


## Building the SignedTransaction

Having gathered all the components for the transaction we now need to use a `TransactionBuilder` to construct the
full `SignedTransaction`. We instantiate a `TransactionBuilder` and provide a notary that will be associated with
the output states. Then we keep adding inputs, outputs, commands and attachments to complete the transaction.

Once the transaction is fully formed, we call `ServiceHub.signInitialTransaction` to sign the `TransactionBuilder`
and convert it into a `SignedTransaction`.

Examples of this process are:

```kotlin
// Modify the state field for new output. We use copy, to ensure no other modifications.
// It is especially important for a LinearState that the linearId is copied across,
// not accidentally assigned a new random id.
val newState = latestRecord.state.data.copy(state = verdict)

// We have to use the original notary for the new transaction
val notary = latestRecord.state.notary

// Get and populate the new TransactionBuilder
// To destroy the old proposal state and replace with the new completion state.
// Also add the Completed command with keys of all parties to signal the Tx purpose
// to the Contract verify method.
val tx = TransactionBuilder(notary).
        withItems(
                latestRecord,
                StateAndContract(newState, TRADE_APPROVAL_PROGRAM_ID),
                Command(TradeApprovalContract.Commands.Completed(),
                        listOf(ourIdentity.owningKey, latestRecord.state.data.source.owningKey)))
tx.setTimeWindow(serviceHub.clock.instant(), 60.seconds)
// We can sign this transaction immediately as we have already checked all the fields and the decision
// is ultimately a manual one from the caller.
// As a SignedTransaction we can pass the data around certain that it cannot be modified,
// although we do require further signatures to complete the process.
val selfSignedTx = serviceHub.signInitialTransaction(tx)

```

[WorkflowTransactionBuildTutorial.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/txbuild/WorkflowTransactionBuildTutorial.kt)

```kotlin
private fun buildTradeProposal(ourInputStates: List<StateAndRef<Cash.State>>,
                               ourOutputState: List<Cash.State>,
                               theirInputStates: List<StateAndRef<Cash.State>>,
                               theirOutputState: List<Cash.State>): SignedTransaction {
    // This is the correct way to create a TransactionBuilder,
    // do not construct directly.
    // We also set the notary to match the input notary
    val builder = TransactionBuilder(ourInputStates.first().state.notary)

    // Add the move commands and key to indicate all the respective owners and need to sign
    val ourSigners = ourInputStates.map { it.state.data.owner.owningKey }.toSet()
    val theirSigners = theirInputStates.map { it.state.data.owner.owningKey }.toSet()
    builder.addCommand(Cash.Commands.Move(), (ourSigners + theirSigners).toList())

    // Build and add the inputs and outputs
    builder.withItems(*ourInputStates.toTypedArray())
    builder.withItems(*theirInputStates.toTypedArray())
    builder.withItems(*ourOutputState.map { StateAndContract(it, Cash.PROGRAM_ID) }.toTypedArray())
    builder.withItems(*theirOutputState.map { StateAndContract(it, Cash.PROGRAM_ID) }.toTypedArray())

    // We have already validated their response and trust our own data
    // so we can sign. Note the returned SignedTransaction is still not fully signed
    // and would not pass full verification yet.
    return serviceHub.signInitialTransaction(builder, ourSigners.single())
}

```

[FxTransactionBuildTutorial.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FxTransactionBuildTutorial.kt)


## Completing the SignedTransaction

Having created an initial `TransactionBuilder` and converted this to a `SignedTransaction`, the process of
verifying and forming a full `SignedTransaction` begins and then completes with the
notarisation. In practice this is a relatively stereotypical process,
because assuming the `SignedTransaction` is correctly constructed the
verification should be immediate. However, it is also important to
recheck the business details of any data received back from an external
node, because a malicious party could always modify the contents before
returning the transaction. Each remote flow should therefore check as
much as possible of the initial `SignedTransaction` inside the `unwrap` of
the receive before agreeing to sign. Any issues should immediately throw
an exception to abort the flow. Similarly the originator, should always
apply any new signatures to its original proposal to ensure the contents
of the transaction has not been altered by the remote parties.

The typical code therefore checks the received `SignedTransaction`
using the `verifySignaturesExcept` method, excluding itself, the
notary and any other parties yet to apply their signature. The contents of the `SignedTransaction` should be fully
verified further by expanding with `toLedgerTransaction` and calling
`verify`. Further context specific and business checks should then be
made, because the `Contract.verify` is not allowed to access external
context. For example, the flow may need to check that the parties are the
right ones, or that the `Command` present on the transaction is as
expected for this specific flow. An example of this from the demo code is:

```kotlin
// First we receive the verdict transaction signed by their single key
val completeTx = sourceSession.receive<SignedTransaction>().unwrap {
    // Check the transaction is signed apart from our own key and the notary
    it.verifySignaturesExcept(ourIdentity.owningKey, it.tx.notary!!.owningKey)
    // Check the transaction data is correctly formed
    val ltx = it.toLedgerTransaction(serviceHub, false)
    ltx.verify()
    // Confirm that this is the expected type of transaction
    require(ltx.commands.single().value is TradeApprovalContract.Commands.Completed) {
        "Transaction must represent a workflow completion"
    }
    // Check the context dependent parts of the transaction as the
    // Contract verify method must not use serviceHub queries.
    val state = ltx.outRef<TradeApprovalContract.State>(0)
    require(serviceHub.myInfo.isLegalIdentity(state.state.data.source)) {
        "Proposal not one of our original proposals"
    }
    require(state.state.data.counterparty == sourceSession.counterparty) {
        "Proposal not for sent from correct source"
    }
    it
}

```

[WorkflowTransactionBuildTutorial.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/txbuild/WorkflowTransactionBuildTutorial.kt)

After verification the remote flow will return its signature to the
originator. The originator should apply that signature to the starting
`SignedTransaction` and recheck the signatures match.


## Committing the Transaction

Once all the signatures are applied to the `SignedTransaction`, the
final steps are notarisation and ensuring that all nodes record the fully-signed transaction. The
code for this is standardised in the `FinalityFlow`:

```kotlin
// Notarise and distribute the completed transaction.
subFlow(FinalityFlow(allPartySignedTx, sourceSession))

```

[WorkflowTransactionBuildTutorial.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/txbuild/WorkflowTransactionBuildTutorial.kt)


## Partially Visible Transactions

The discussion so far has assumed that the parties need full visibility
of the transaction to sign. However, there may be situations where each
party needs to store private data for audit purposes, or for evidence to
a regulator, but does not wish to share that with the other trading
partner. The tear-off/Merkle tree support in Corda allows flows to send
portions of the full transaction to restrict visibility to remote
parties. To do this one can use the
`SignedTransaction.buildFilteredTransaction` extension method to produce
a `FilteredTransaction`. The elements of the `SignedTransaction`
which we wish to be hide will be replaced with their secure hash. The
overall transaction id is still provable from the
`FilteredTransaction` preventing change of the private data, but we do
not expose that data to the other node directly. A full example of this
can be found in the `NodeInterestRates` Oracle code from the
`irs-demo` project which interacts with the `RatesFixFlow` flow.
Also, refer to the [Transaction tear-offs](tutorial-tear-offs.md).
