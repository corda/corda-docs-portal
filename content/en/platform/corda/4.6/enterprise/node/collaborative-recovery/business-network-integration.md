---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-collaborative-recovery
tags:
- disaster recovery
- collaborative recovery
- install
- node operator


title: Implementing Collaborative Recovery
weight: 200
---

# Collaborative Recovery for Business Network operations

**Who this documentation is for:**
* Node operators
* Business Network Operators (BNOs)

In a disaster recovery scenario, you need to be sure you can recover data from the nodes you have transacted with on each Business Network you are a part of.

Unless Business Network Operators (BNOs) make Collaborative Recovery part of the disaster recovery plan for their network, Collaborative Recovery cannot be used. If you are a node operator, you need to seek an agreement at the governance level with all relevant BNOs before implementing Collaborative Recovery on your own node.

Once you have this agreement in place on your Business Network, you can create the wrapping flows that make recovery possible with all participants.


## Wrapping flows

The Collaborative Recovery CorDapps use flows to initiate and execute the recovery process. Before this can happen, you need validation that the parties specified as input to each disaster recovery flow are members of the Business Network.

To validate these parties, you need to write and distribute simple wrapping flows for these reconciliation and recovery flows:

- [ScheduleReconciliationFlow](ledger-sync.md#schedule-reconciliation-flow) - This flow schedules regular reconciliation checks.
- [AutomaticRecoveryFlow](ledger-recovery-automatic.md#automatic-ledger-recover-flow) - This flow initiates automatic data recovery.
- [InitiateManualRecoveryFlow](ledger-recovery-manual.md#initiate-manual-recovery-flow) - This flow initiates manual data recovery.

These wrapping flows should be bundled into a single CorDapp that can be distributed to relevant parties on your network.

## Example flows

How you implement the wrapping flows will depend on your own requirements and those of your Business Network. In the following examples, you will find reference implementations of Business Network-enabled Disaster Recovery flows. You can use these as the basis to create wrapping flows appropriate to your own Business Networks.

### Initiating Business Network-enabled flows

Each flow in the examples below contains the private function `getMembers`. The implementation of this function is the responsibility of either the node operator or Business Network operator. It is used throughout the code snippets to demonstrate how membership of a party might be validated using a retrieved list of Business Network members.

### Business Network-initiated LedgerSync

In order to determine whether or not ledger data is synchronised with the rest of the network after a disaster scenario, use `ScheduleReconciliationFlow` to schedule and eventually execute reconciliation with a specified list of parties. In this case, that list will be verified using a retrieved set of the Business Network members.

In order to enable overriding of the LedgerSync reconciliation responder flows, they must be manually specified
in the configuration of the responding node. This can be done by adding the following config block to the node.conf.

```none
flowOverrides {
    overrides=[
        {
            initiator="ReconcileWithPartyFlowInitiator"
            responder="ReconcileWithPartyFlowResponderWithBusinessNetwork"
        }
    ]
}
```

{{< note >}}

After reconciling with all necessary parties, the node operator should then proceed with either automatic or manual recovery.

{{< /note >}}


```kotlin
// Kotlin
    @InitiatingFlow
    @StartableByRPC
    class InitiateReconciliationWithBusinessNetwork(
        private val reconciliationParties: List<Party>
    ): FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // Retrieve the list of identities with which you could have shared transaction data
            val businessNetworkMembers: List<Party> = getMembers()

            // Check that all parties you wish to reconcile with are part of the Business Network
            if (businessNetworkMembers.containsAll(reconciliationParties)) {
                throw LedgerSyncException("Only parties in this Business Network are eligible for reconciliation.")
            }

            // Initiate a subFlow to kick off reconciliation with all parties retrieved
            subFlow(ScheduleReconciliationFlow(reconciliationParties))
        }

        @Suspendable
        private fun getMembers(): List<Party> {
            // Implementation specific retrieval of membership list.
        }
    }

    @InitiatedBy(ReconcileWithPartyFlowInitiator::class)
    class ReconcileWithPartyFlowResponderWithBusinessNetwork(
        private val session: FlowSession
    ): FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // Retrieve the list of identities with which you COULD have shared transaction data
            val businessNetworkMembers: List<Party> = getMembers()

            // Check that the counterparty is part of the Business Network
            if (!businessNetworkMembers.contains(session.counterparty)) {
                throw LedgerSyncException("Only parties in this Business Network are eligible for reconciliation.")
            }

            // Kick off the responding flow to continue to reconcile with the initiating part
            subFlow(ReconcileWithPartyFlowResponder(session))
        }

        @Suspendable
        private fun getMembers(): List<Party> {
            // Implementation specific retrieval of membership list.
        }
    }

```
```java
// Java
    @InitiatingFlow
    @StartableByRPC
    public class InitiateReconciliationWithBusinessNetwork extends FlowLogic<Unit> {

        private final List<Party> reconciliationParties;
        public InitiateReconciliationWithBusinessNetwork(List<Party> reconciliationParties) {
            this.reconciliationParties = reconciliationParties;
        }

        @Suspendable
        @Override
        public void call() throws FlowException {
            // Retrieve the list of identities with which you COULD have shared transaction data
            List<Party> businessNetworkMembers = getMembers();

            // Check that all parties you wish to reconcile with are part of the Business Network
            if (!businessNetworkMembers.containsAll(reconciliationParties)) {
                throw new LedgerSyncException("Only parties in this Business Network are eligible for reconciliation.");
            };

            // Initiate a subFlow to kick off reconciliation with all parties retrieved
            subFlow(new ScheduleReconciliationFlow(reconciliationParties));
        }

        @Suspendable
        public List<Party> getMembers() throws FlowException {
            // Implementation specific retrieval of membership list.
        }
    }

    @InitiatedBy(ReconcileWithPartyFlowInitiator.class)
    public static class ReconcileWithPartyFlowResponderWithBusinessNetwork extends FlowLogic<SignedTransaction> {

        private final FlowSession session;
        public InitiateReconciliationWithBusinessNetworkResponder(session flowSession) {
            this.session = session;
        }

        @Suspendable
        @Override
        public SignedTransaction call() throws FlowException {
            // Retrieve the list of identities with which you COULD have shared transaction data
            List<Party> businessNetworkMembers = getMembers();

            // Check that all parties you wish to reconcile with are part of the Business Network
            if (!businessNetworkMembers.contains(session.counterparty)) {
                throw new LedgerSyncException("Only parties in this Business Network are eligible for reconciliation.");
            }

            // Initiate a subFlow to kick off reconciliation with all parties retrieved
            subFlow(new ReconcileWithPartyFlowResponder(session));
        }

        @Suspendable
        public List<Party> getMembers() throws FlowException {
            // Implementation specific retrieval of membership list.
        }
    }
```

### Business Network-enabled automatic recovery

The simplest form of recovering ledger data is executed using `AutomaticLedgerRecover` which, on the
basis of a previous reconciliation record or `ReconciliationStatus`, uses built-in Corda processes
to request and retrieve the appropriate transactions from a counterparty.

For more information on this process and how it may be further configured, see the
[docs](ledger-recovery-automatic.md).


```kotlin
// Kotlin
    @InitiatingFlow
    @StartableByRPC
    class InitiateAutomaticRecoveryWithBusinessNetwork(
        private val recoveryParty: Party
    ): FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // Retrieve the list of identities with which you COULD have shared transaction data
            val businessNetworkMembers: List<Party> = getMembers()

            // Check that all parties you wish to reconcile with are part of the Business Network
            if (businessNetworkMembers.contains(recoveryParty)) {
                throw AutomaticRecoveryException("Only parties in this Business Network are eligible for recovery.")
            }

            // Initiate a subFlow to kick off recovery with all Business Network members
            subFlow(AutomaticLedgerRecover(recoveryParty))
        }

        @Suspendable
        private fun getMembers(): List<Party> {
            // Implementation specific retrieval of membership list.
        }
    }

    @InitiatedBy(InitiateAutomaticRecoveryWithBusinessNetwork::class)
    class InitiateAutomaticRecoveryResponderWithBusinessNetwork(
        private val session: FlowSession
    ): FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // Retrieve the list of identities with which you COULD have shared transaction data
            val businessNetworkMembers: List<Party> = getMembers()

            // Check that the counterparty is part of the Business Network
            if (!businessNetworkMembers.contains(session.counterparty)) {
                throw AutomaticRecoveryException("Only parties in this Business Network are eligible for recovery.")
            }

            // Kick off the responding flow to continue to reconcile with the initiating part
            subFlow(AutomaticLedgerRecoverFlowResponder(session))
        }

        @Suspendable
        private fun getMembers(): List<Party> {
            // Implementation specific retrieval of membership list.
        }
    }
```
```java
// Java
    @InitiatingFlow
    @StartableByRPC
    public class InitiateAutomaticRecoveryWithBusinessNetwork extends FlowLogic<Unit> {

        private final List<Party> recoveryParties;
        public InitiateReconciliationWithBusinessNetwork(Party recoveryParty) {
            this.recoveryParty = recoveryParty;
        }

        @Suspendable
        @Override
        public void call() throws FlowException {
            // Retrieve the list of identities with which you COULD have shared transaction data
            List<Party> businessNetworkMembers = getMembers();

            // Check that all parties you wish to recover from are part of the Business Network
            if (!businessNetworkMembers.contains(recoveryParty)) {
                throw new AutomaticRecoveryException("Only parties in this Business Network are eligible for recovery.");
            }

            // Initiate a subFlow to kick off recovery with all Business Network members
            subFlow(new AutomaticLedgerRecover(recoveryParty));
        }

        @Suspendable
        public List<Party> getMembers() throws FlowException {
            // Implementation specific retrieval of membership list.
        }
    }

    @InitiatedBy(InitiateAutomaticRecoveryWithBusinessNetwork.class)
    public static class InitiateAutomaticRecoveryResponderWithBusinessNetwork extends FlowLogic<SignedTransaction> {

        private final FlowSession session;
        public InitiateReconciliationWithBusinessNetworkResponder(session flowSession) {
            this.session = session;
        }

        @Suspendable
        @Override
        public SignedTransaction call() throws FlowException {
            // Retrieve the list of identities with which you COULD have shared transaction data
            List<Party> businessNetworkMembers = getMembers();

            // Check that the party who wishes to engage in automatic recovery is part of the Business Network
            if (!businessNetworkMembers.contains(session.counterparty)) {
                throw AutomaticRecoveryException("Only parties in this Business Network are eligible for recovery.");
            }

            // Initiate a subFlow to kick off reconciliation with all parties retrieved
            subFlow(new ReconcileWithPartyFlowResponder(session));
        }

        @Suspendable
        public List<Party> getMembers() throws FlowException {
            // Implementation specific retrieval of membership list.
        }
    }
```

### Business Network-enabled manual recovery

Another option available to node operators is to initiate manual recovery of ledger data. The code snippet below
outlines a simple wrapping flow that initiates manual recovery, persisting a record or `RecoveryRequest`
on both the initiating and responding nodes.

The participating nodes may then continue with the processes described [here](ledger-recovery-manual.md)
to export, transfer and eventually import the missing transaction data.

```kotlin
// Kotlin
    @InitiatingFlow
    @StartableByRPC
    class InitiateManualRecoveryWithBusinessNetwork(
        private val recoveryParty: Party
   ): FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // Retrieve the list of identities with which you COULD have shared transaction data
            val businessNetworkMembers: List<Party> = getMembers()

            // Check that all parties you wish to reconcile with are part of the Business Network
            if (!businessNetworkMembers.contains(recoveryParty)) {
                throw ManualRecoveryException("Only parties in this Business Network are eligible for recovery.")
            }

            // Initiate a subFlow to kick off recovery with all Business Network members
            subFlow(InitiateManualRecoveryFlow(recoveryParty))
        }

        @Suspendable
        private fun getMembers(): List<Party> {
            // Implementation specific retrieval of membership list.
        }
    }

    @InitiatedBy(InitiateManualRecoveryWithBusinessNetwork::class)
    class InitiateManualRecoveryResponderWithBusinessNetwork(
        private val session: FlowSession
    ): FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // Retrieve the list of identities with which you COULD have shared transaction data
            val businessNetworkMembers: List<Party> = getMembers()

            // Check that the counterparty is part of the Business Network
            if (!businessNetworkMembers.contains(session.counterparty)) {
                throw ManualRecoveryException("Only parties in this Business Network are eligible for recovery.")
            }

            // Kick off the responding flow to continue to reconcile with the initiating part
            subFlow(InitiateManualRecoveryFlowResponder(session))
        }

        @Suspendable
        private fun getMembers(): List<Party> {
            // Implementation specific retrieval of membership list.
        }
    }
```
```java
// Java
    @InitiatingFlow
    @StartableByRPC
    public class InitiateManualRecoveryWithBusinessNetwork extends FlowLogic<Unit> {

        private final Party recoveryParties;
        public InitiateReconciliationWithBusinessNetwork(Party recoveryParty) {
            this.recoveryParty = recoveryParty;
        }

        @Suspendable
        @Override
        public void call() throws FlowException {
            // Retrieve the list of identities with which you COULD have shared transaction data
            List<Party> businessNetworkMembers = getMembers();

            // Check that all parties you wish to recover from are part of the Business Network
            if (!businessNetworkMembers.contains(recoveryParty)) {
                throw new ManualRecoveryException("Only parties in this Business Network are eligible for recovery.");
            }

            // Initiate a subFlow to kick off recovery with all Business Network members
            subFlow(new InitiateManualRecoveryFlow(recoveryParty));
        }

        @Suspendable
        public List<Party> getMembers() throws FlowException {
            // Implementation specific retrieval of membership list.
        }
    }

    @InitiatedBy(InitiateAutomaticRecoveryWithBusinessNetwork.class)
    public static class InitiateAutomaticRecoveryResponderWithBusinessNetwork extends FlowLogic<SignedTransaction> {

        private final FlowSession session;
        public InitiateReconciliationWithBusinessNetworkResponder(session flowSession) {
            this.session = session;
        }

        @Suspendable
        @Override
        public SignedTransaction call() throws FlowException {
            // Retrieve the list of identities with which you COULD have shared transaction data
            List<Party> businessNetworkMembers = getMembers();

            // Check that the party who wishes to engage in automatic recovery is part of the Business Network
            if (!businessNetworkMembers.contains(session.counterparty)) {
                throw AutomaticRecoveryException("Only parties in this Business Network are eligible for recovery.");
            }

            // Initiate a subFlow to kick off reconciliation with all parties retrieved
            subFlow(new ReconcileWithPartyFlowResponder(session));
        }

        @Suspendable
        public List<Party> getMembers() throws FlowException {
            // Implementation specific retrieval of membership list.
        }
    }

```

## Schedule recurring reconciliation

It is best practice to prevent against loss of data during a disaster by scheduling reconciliation checks across your network. This allows every node to ensure they have a backup record of each node they have transacted with. While everyone's data remains secure, discrepancies between parties can be safely detected. You can use Collaborative Recovery to schedule reconciliation flows, so you can be sure your vault data is consistent with that of all other parties on the network.

The flow in the code snippet below represents a wrapping flow that schedules reconciliation with every member of a Business Network on a recurring basis. Using this wrapper means you can safely see when discrepancies occur between your vault data and those of counterparties.

Communicating with all nodes on the network imposes network load. If you are on a smaller network, you may be able to schedule reconciliation more frequently. For larger networks, you can reconcile less frequently or potentially with a random subset of available peers.

The implementation below reconciles with all parties (best for a smaller network) once daily. As a node operator, you must also determine whether or not you wish to run reconciliation during operating business hours, or as a routine maintenance activity to be performed when there is reduced network traffic.

{{< note >}}
In general, a node's vault is expected to be consistent with the network (such is the major benefit of DLT). This process is similar to running database replication technology - an added layer of resiliency and reliability for on-ledger data.
{{< /note >}}

```kotlin
// Kotlin
    @StartableByRPC
    class ScheduleReconciliationWithBusinessNetwork(
        private val stateRef: StateRef
    ): FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // PART 1: Scheduling Reconciliation With The Business Network
            // Start by building a transaction to schedule the next reconciliation.
            val input = serviceHub.toStateAndRef<BusinessNetworkReconSchedulerState>(stateRef)
            val output = BusinessNetworkReconSchedulerState(ourIdentity)
            val reconCmd = Command(ReconcileWithNetwork(), ourIdentity.owningKey)

            // Build, sign and finalize the transaction.
            // Note: you are selecting the first notary ONLY for simplicities sake. This should be
            // made explicit in a configuration file for production use.
            val txBuilder = TransactionBuilder(serviceHub.networkMapCache.notaryIdentities.first())
                    .addInputState(input)
                    .addOutputState(output)
                    .addCommand(reconCmd)
            val signedTx = serviceHub.signInitialTransaction(txBuilder)
            subFlow(FinalityFlow(signedTx, listOf()))

            // PART 2: Reconcile With all Members of The Business Network
            // Retrieve the list of identities with which you could have shared transaction data
            val businessNetworkMembers: List<Party> = getMembers()

            // Initiate a subFlow to kick off recovery with all Business Network members
            subFlow(InitiateReconciliationWithBusinessNetwork(getMembers()))
        }

        @Suspendable
        private fun getMembers(): List<Party> {
            // Implementation specific retrieval of membership list.
        }
    }

    /**
     * The schedulable state that will be used to kick off reconciliation with all other parties on a Business Network
     * at a regular interval. Defaults to executing once daily.
     */
    @BelongsToContract(BusinessNetworkReconSchedulerContract::class)
    class BusinessNetworkReconSchedulerState(
        private val ourIdentity: Party,
        private val interval: ChronoUnit = ChronoUnit.DAYS,
        private val nextActivityTime: Instant = Instant.now().plus(1, interval)
    ): SchedulableState {
        override val participants get() = listOf(ourIdentity)
        override fun nextScheduledActivity(thisStateRef: StateRef, flowLogicRefFactory: FlowLogicRefFactory): ScheduledActivity? {
            return ScheduledActivity(flowLogicRefFactory.create(ScheduleReconciliationWithBusinessNetwork::class.java), nextActivityTime)
        }
    }

    /**
     * A simple, no-check contract that will be referenced in the issuance of a schedulable state.
     */
    class BusinessNetworkReconSchedulerContract : Contract {
        companion object {
            const val CONTRACT_ID = "com.your.package.name.BusinessNetworkReconSchedulerContract"
        }

        override fun verify(tx: LedgerTransaction) {
            // Omitted for the purpose of this sample.
        }

        interface Commands : CommandData {
            class ReconcileWithNetwork : Commands
        }
    }
```

```java
// Java
    @InitiatingFlow
    @StartableByRPC
    public class ScheduleReconciliationWithBusinessNetwork extends FlowLogic<Unit> {

        private final StateRef stateRef;
        public InitiateReconciliationWithBusinessNetwork(stateRef StateRef) {
            this.stateRef = stateRef;
        }

        @Suspendable
        @Override
        public void call() throws FlowException {
            // PART 1: Scheduling Reconciliation With The Business Network
            // Start by building a transaction to schedule the next reconciliation.
            BusinessNetworkReconSchedulerState input = serviceHub.toStateAndRef<BusinessNetworkReconSchedulerState>(stateRef);
            BusinessNetworkReconSchedulerState output = BusinessNetworkReconSchedulerState(ourIdentity);
            Command<ReconcileWithNetwork> reconCmd = new Command(
                new ReconcileWithNetwork(),
                getOurIdentity.owningKey
            );

            // Build, sign and finalize the transaction.
            // Note: first notary is selected here ONLY for the sake of simplicity. This should be
            // made explicit in a configuration file for production use.
            TransactionBuilder txBuilder = TransactionBuilder(getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0))
                    .addInputState(input)
                    .addOutputState(output)
                    .addCommand(reconCmd);
            val signedTx = getServiceHub.signInitialTransaction(txBuilder);
            subFlow(new FinalityFlow(signedTx, listOf()));

            // PART 2: Reconcile With All Members of The Business Network
            // Retrieve the list of identities with which you COULD have shared transaction data
            List<Party> businessNetworkMembers = getMembers();

            // Initiate a subFlow to kick off recovery with all Business Network members
            subFlow(new InitiateReconciliationWithBusinessNetwork(getMembers()));
        }

        @Suspendable
        public List<Party> getMembers() throws FlowException {
            // Implementation specific retrieval of membership list.
        }
    }

    /**
     * The schedulable state that will be used to kick off reconciliation with all other parties on a Business Network
     * at a regular interval. Defaults to executing once daily.
     */
    @BelongsToContract(BusinessNetworkReconSchedulerContract.class)
    class BusinessNetworkReconSchedulerState implements SchedulableState {
        private final Party ourIdentity;
        private final ChronoUnit interval;
        private final Instant nextActivityTime;

        @ConstructorForDeserialization
        private BusinessNetworkReconSchedulerState(Party ourIdentity, ChronoUnit interval, Instant nextActivityTime) {
            this.ourIdentity = ourIdentity;
            this.interval = interval;
            this.nextActivityTime = nextActivityTime;
        }

        public BusinessNetworkReconSchedulerState(Party ourIdentity, ChronoUnit interval) {
            this.ourIdentity = ourIdentity;
            this.interval = interval;
            this.nextActivityTime = Instant.now().plus(1, interval);
        }

        public BusinessNetworkReconSchedulerState(Party ourIdentity) {
            this.ourIdentity = ourIdentity;
            this.interval = ChronoUnit.DAYS;
            this.nextActivityTime = Instant.now().plus(1, interval);
        }

        @NotNull
        @Override
        public List<AbstractParty> getParticipants() {
            return Collections.singletonList(ourIdentity);
        }

        @Nullable
        @Override
        public ScheduledActivity nextScheduledActivity(@NotNull StateRef thisStateRef, @NotNull FlowLogicRefFactory flowLogicRefFactory) {
            return new ScheduledActivity(flowLogicRefFactory.create(ScheduleReconciliationWithBusinessNetwork.class), nextActivityTime);
        }
    }

    /**
     * A simple, no-check contract that will be referenced in the issuance of a schedulable state.
     */
    class BusinessNetworkReconSchedulerContract implements Contract {
        public static final String CONTRACT_ID = "com.your.package.name.BusinessNetworkReconSchedulerContract";
        public interface Commands extends CommandData {
            class ReconcileWithNetwork extends TypeOnlyCommandData implements Commands{}
        }
        @Override
        public void verify(LedgerTransaction tx) {
            // Omitted for the purpose of this sample.
        }
    }
```
