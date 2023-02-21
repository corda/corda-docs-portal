---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    parent: corda-enterprise-4-7-cordapps-contracts
tags:
- contract
- upgrade
title: Upgrading contracts
weight: 20
---




# Upgrading contracts

You may need to upgrade your contract code to fix bugs (in either
design or implementation). You can substitute one version of the contract code for another, or
change to a contract that can migrate the existing state objects. When state objects are
added as outputs to transactions, they are linked to the revelant contract code using the
`StateAndContract` type. To change a state's contract, substitute one `ContractClassName` for another.


## Workflow

To upgrade a contract:

1. The contract developer develops a new version (Y) of an existing contract (X).
2. The developer notifies all existing users (for example, via a mailing list or CorDapp store) to stop their nodes from
issuing further states with contract X.
3. The parties that signed the existing contract review the new contract, and identify the contract states they
agree to upgrade. They may decide not to upgrade some contract states.
4. The signing parties instruct their Corda nodes (via RPC) to upgrade state objects with contract X to state
objects with contract Y, using the agreed upgrade path.
5. One of the parties (the `Initiator`) initiates a flow to replace state objects referring to contract X with new
state objects referring to contract Y.
6. A proposed transaction (the `Proposal`), with the old states as inputs and the reissued states as outputs, is
created and signed with the node’s private key.
7. The `Initiator` node sends the proposed transaction, along with details of the new contract upgrade path that it
is proposing, to all participants of the state object.
8. Each counterparty (the `Acceptor`s) verifies the proposal, signs or rejects the state reissuance accordingly, and
sends a signature or rejection notification back to the initiating node.
9. If the `Initiator` receives signatures from all parties, it assembles the complete signed transaction and sends
it to the notary.


## Authorizing an upgrade

Each of the participants in the state for which the contract is being upgraded must instruct their node that
they agree to the upgrade before the upgrade can take place. The `ContractUpgradeFlow` manages the
authorization process. Each node administrator can use RPC to trigger either an `Authorize` or a `Deauthorize` flow
for the state in question.

```kotlin
@StartableByRPC
class Authorise(
        val stateAndRef: StateAndRef<*>,
        private val upgradedContractClass: Class<out UpgradedContract<*, *>>
) : FlowLogic<Void?>() {

```

[ContractUpgradeFlow.kt](https://github.com/corda/corda/blob/release/os/4.8/core/src/main/kotlin/net/corda/core/flows/ContractUpgradeFlow.kt)

```kotlin
@StartableByRPC
class Deauthorise(val stateRef: StateRef) : FlowLogic<Void?>() {
    @Suspendable
    override fun call(): Void? {

```

[ContractUpgradeFlow.kt](https://github.com/corda/corda/blob/release/os/4.8/core/src/main/kotlin/net/corda/core/flows/ContractUpgradeFlow.kt)


## Proposing an upgrade

After all parties have authorized the contract upgrade for the state, one of the contract participants can initiate the
upgrade process by triggering the `ContractUpgradeFlow.Initiate` flow. `Initiate` creates a transaction including
the old state and the updated state, and sends it to each of the participants. Each participant will verify the
transaction, create a signature over it, and send the signature back to the initiator. Once all the signatures are
collected, the transaction will be notarised and persisted to every participant’s vault.


## Example

Suppose Bank A has entered into an agreement with Bank B which is represented by the state object
`DummyContractState`, and governed by the contract code `DummyContract`. A few days after the exchange of contracts,
the developer of the contract code discovers a bug in the contract code.

Bank A and Bank B decide to upgrade the contract to `DummyContractV2`.


The developer creates a new contract, `DummyContractV2` extending the `UpgradedContract` class. A new state
object `DummyContractV2.State` references the new contract:

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

[DummyContractV2.kt](https://github.com/corda/corda/blob/release/os/4.4/testing/test-utils/src/main/kotlin/net/corda/testing/contracts/DummyContractV2.kt)


Bank A instructs its node to accept the contract upgrade to `DummyContractV2` for the contract state.

{{< tabs name="tabs-1" >}}
{{% tab name="none" %}}
```none
val rpcClient : CordaRPCClient = << Bank A's Corda RPC Client >>
val rpcA = rpcClient.proxy()
rpcA.startFlow(ContractUpgradeFlow.Authorise(<<StateAndRef of the contract state>>, DummyContractV2::class.java))
```
{{% /tab %}}

{{< /tabs >}}


Bank B initiates the upgrade flow, which will send an upgrade proposal to all contract participants. Each of the
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
