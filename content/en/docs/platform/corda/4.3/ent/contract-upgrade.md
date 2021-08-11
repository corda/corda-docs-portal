---
aliases:
- /releases/4.3/contract-upgrade.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-contract-upgrade
    parent: corda-enterprise-4-3-tutorials-index
    weight: 1060
tags:
- contract
- upgrade
title: Upgrading contracts
---




# Upgrading contracts

While every care is taken in development of contract code, inevitably upgrades will be required to fix bugs (in either
design or implementation). Upgrades can involve a substitution of one version of the contract code for another or
changing to a different contract that understands how to migrate the existing state objects. When state objects are
added as outputs to transactions, they are linked to the contract code they are intended for via the
`StateAndContract` type. Changing a state’s contract only requires substituting one `ContractClassName` for another.


## Workflow

Here’s the workflow for contract upgrades:


* Banks A and B negotiate a trade, off-platform
* Banks A and B execute a flow to construct a state object representing the trade, using contract X, and include it in
a transaction (which is then signed and sent to the consensus service)
* Time passes
* The developer of contract X discovers a bug in the contract code, and releases a new version, contract Y. The
developer will then notify all existing users (e.g. via a mailing list or CorDapp store) to stop their nodes from
issuing further states with contract X
* Banks A and B review the new contract via standard change control processes and identify the contract states they
agree to upgrade (they may decide not to upgrade some contract states as these might be needed for some other
obligation contract)
* Banks A and B instruct their Corda nodes (via RPC) to be willing to upgrade state objects with contract X to state
objects with contract Y using the agreed upgrade path
* One of the parties (the `Initiator`) initiates a flow to replace state objects referring to contract X with new
state objects referring to contract Y
* A proposed transaction (the `Proposal`), with the old states as input and the reissued states as outputs, is
created and signed with the node’s private key
* The `Initiator` node sends the proposed transaction, along with details of the new contract upgrade path that it
is proposing, to all participants of the state object
* Each counterparty (the `Acceptor` s) verifies the proposal, signs or rejects the state reissuance accordingly, and
sends a signature or rejection notification back to the initiating node
* If signatures are received from all parties, the `Initiator` assembles the complete signed transaction and sends
it to the notary


## Authorising an upgrade

Each of the participants in the state for which the contract is being upgraded will have to instruct their node that
they agree to the upgrade before the upgrade can take place. The `ContractUpgradeFlow` is used to manage the
authorisation process. Each node administrator can use RPC to trigger either an `Authorise` or a `Deauthorise` flow
for the state in question.

```kotlin
@StartableByRPC
class Authorise(
        val stateAndRef: StateAndRef<*>,
        private val upgradedContractClass: Class<out UpgradedContract<*, *>>
) : FlowLogic<Void?>() {

```

[ContractUpgradeFlow.kt](https://github.com/corda/corda/blob/release/os/4.3/core/src/main/kotlin/net/corda/core/flows/ContractUpgradeFlow.kt)

```kotlin
@StartableByRPC
class Deauthorise(val stateRef: StateRef) : FlowLogic<Void?>() {
    @Suspendable
    override fun call(): Void? {

```

[ContractUpgradeFlow.kt](https://github.com/corda/corda/blob/release/os/4.3/core/src/main/kotlin/net/corda/core/flows/ContractUpgradeFlow.kt)


## Proposing an upgrade

After all parties have authorised the contract upgrade for the state, one of the contract participants can initiate the
upgrade process by triggering the `ContractUpgradeFlow.Initiate` flow. `Initiate` creates a transaction including
the old state and the updated state, and sends it to each of the participants. Each participant will verify the
transaction, create a signature over it, and send the signature back to the initiator. Once all the signatures are
collected, the transaction will be notarised and persisted to every participant’s vault.


## Example

Suppose Bank A has entered into an agreement with Bank B which is represented by the state object
`DummyContractState` and governed by the contract code `DummyContract`. A few days after the exchange of contracts,
the developer of the contract code discovers a bug in the contract code.

Bank A and Bank B decide to upgrade the contract to `DummyContractV2`:


* The developer creates a new contract `DummyContractV2` extending the `UpgradedContract` class, and a new state
object `DummyContractV2.State` referencing the new contract.

```kotlin
class DummyContractV2 : UpgradedContractWithLegacyConstraint<DummyContract.State, DummyContractV2.State> {
    companion object {
        const val PROGRAM_ID: ContractClassName = "net.corda.testing.contracts.DummyContractV2"

        /**
         * An overload of move for just one input state.
         */
        @JvmStatic
        fun move(prior: StateAndRef<State>, newOwner: AbstractParty) = move(listOf(prior), newOwner)

        /**
         * Returns a [TransactionBuilder] that takes the given input states and transfers them to the newOwner.
         */
        @JvmStatic
        fun move(priors: List<StateAndRef<State>>, newOwner: AbstractParty): TransactionBuilder {
            require(priors.isNotEmpty()) { "States to move to new owner must not be empty" }
            val priorState = priors[0].state.data
            val (cmd, state) = priorState.withNewOwner(newOwner)
            return TransactionBuilder(notary = priors[0].state.notary).withItems(
                    /* INPUTS  */ *priors.toTypedArray(),
                    /* COMMAND */ Command(cmd, priorState.owners.map { it.owningKey }),
                    /* OUTPUT  */ StateAndContract(state, DummyContractV2.PROGRAM_ID)
            )
        }
    }

    override val legacyContract: String = DummyContract::class.java.name
    override val legacyContractConstraint: AttachmentConstraint = AlwaysAcceptAttachmentConstraint

    data class State(val magicNumber: Int = 0, val owners: List<AbstractParty>) : ContractState {
        override val participants: List<AbstractParty> = owners

        fun withNewOwner(newOwner: AbstractParty): Pair<Commands, State> {
            val newState = this.copy(owners = listOf(newOwner))
            return Pair(Commands.Move(), newState)
        }
    }

    interface Commands : CommandData {
        class Create : TypeOnlyCommandData(), Commands
        class Move : TypeOnlyCommandData(), Commands
    }

    override fun upgrade(state: DummyContract.State): State {
        return State(state.magicNumber, state.participants)
    }

    override fun verify(tx: LedgerTransaction) {
        // Other verifications.
    }
}

```

[DummyContractV2.kt](https://github.com/corda/corda/blob/release/os/4.3/testing/test-utils/src/main/kotlin/net/corda/testing/contracts/DummyContractV2.kt)


* Bank A instructs its node to accept the contract upgrade to `DummyContractV2` for the contract state.

{{< tabs name="tabs-1" >}}
{{% tab name="none" %}}
```none
val rpcClient : CordaRPCClient = << Bank A's Corda RPC Client >>
val rpcA = rpcClient.proxy()
rpcA.startFlow(ContractUpgradeFlow.Authorise(<<StateAndRef of the contract state>>, DummyContractV2::class.java))
```
{{% /tab %}}

{{< /tabs >}}


* Bank B initiates the upgrade flow, which will send an upgrade proposal to all contract participants. Each of the
participants of the contract state will sign and return the contract state upgrade proposal once they have validated
and agreed with the upgrade. The upgraded transaction will be recorded in every participant’s node by the flow.

{{< tabs name="tabs-2" >}}
{{% tab name="none" %}}
```none
val rpcClient : CordaRPCClient = << Bank B's Corda RPC Client >>
val rpcB = rpcClient.proxy()
rpcB.startFlow({ stateAndRef, upgrade -> ContractUpgradeFlow(stateAndRef, upgrade) },
    <<StateAndRef of the contract state>>,
    DummyContractV2::class.java)
```
{{% /tab %}}

{{< /tabs >}}

{{< note >}}
See `ContractUpgradeFlowTest` for more detailed code examples.

{{< /note >}}
