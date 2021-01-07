---
aliases:
- /head/tutorial-observer-nodes.html
- /HEAD/tutorial-observer-nodes.html
- /tutorial-observer-nodes.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-7:
    identifier: corda-os-4-7-tutorial-observer-nodes
    parent: corda-os-4-7-supplementary-tutorials-index
    weight: 1100
tags:
- tutorial
- observer
- nodes
title: Posting transactions to observer nodes
---




# Posting transactions to observer nodes

This tutorial will take you through the steps involved in adding support for observer nodes to your CorDapp.

## Introduction

Posting transactions to an observer node is a common requirement in finance, where regulators often want
to receive comprehensive reporting on all actions taken. By running their own node, regulators can receive a stream
of digitally signed, de-duplicated reports useful for later processing.

## Adding support for observer nodes

Adding support for observer nodes to your application is easy. The Trade reporting demo ([Kotlin](https://github.com/corda/samples-kotlin/tree/master/Features/observableStates-tradereporting), [Java](https://github.com/corda/samples-java/tree/master/Features/observablestates-tradereporting)) shows how to do so.

{{< tabs name="tabs-1" >}}
{{< tab name="kotlin" >}}
```kotlin
@InitiatingFlow
@StartableByRPC
class TradeAndReport(val buyer: Party, val stateRegulator: Party, val nationalRegulator: Party) : FlowLogic<Unit>() {
    override val progressTracker = ProgressTracker()

    @Suspendable
    override fun call() {
        // Obtain a reference from a notary we wish to use.
        /**
         *  METHOD 1: Take first notary on network, WARNING: use for test, non-prod environments, and single-notary networks only!*
         *  METHOD 2: Explicit selection of notary by CordaX500Name - argument can by coded in flow or parsed from config (Preferred)
         *
         *  * - For production you always want to use Method 2 as it guarantees the expected notary is returned.
         */
        val notary = serviceHub.networkMapCache.notaryIdentities.single() // METHOD 1
        // val notary = serviceHub.networkMapCache.getNotary(CordaX500Name.parse("O=Notary,L=London,C=GB")) // METHOD 2

        val transactionBuilder = TransactionBuilder(notary)
                .addOutputState(HighlyRegulatedState(buyer, ourIdentity), HighlyRegulatedContract.ID)
                .addCommand(HighlyRegulatedContract.Commands.Trade(), ourIdentity.owningKey)

        val signedTransaction = serviceHub.signInitialTransaction(transactionBuilder)

        val sessions = listOf(initiateFlow(buyer), initiateFlow(stateRegulator))
        // We distribute the transaction to both the buyer and the state regulator using `FinalityFlow`.
        subFlow(FinalityFlow(signedTransaction, sessions))

        // We also distribute the transaction to the national regulator manually.
        subFlow(ReportManually(signedTransaction, nationalRegulator))
    }
}

@InitiatingFlow
class ReportManually(val signedTransaction: SignedTransaction, val regulator: Party) : FlowLogic<Unit>() {
    override val progressTracker = ProgressTracker()

    @Suspendable
    override fun call() {
        val session = initiateFlow(regulator)
        session.send(signedTransaction)
    }
}

@InitiatedBy(ReportManually::class)
class ReportManuallyResponder(val counterpartySession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val signedTransaction = counterpartySession.receive<SignedTransaction>().unwrap { it }
        // The national regulator records all of the transaction's states using
        // `recordTransactions` with the `ALL_VISIBLE` flag.
        serviceHub.recordTransactions(StatesToRecord.ALL_VISIBLE, listOf(signedTransaction))
    }
}
```
{{< /tab >}}


{{< tab name="java" >}}
```java
@InitiatingFlow
@StartableByRPC
public class TradeAndReport extends FlowLogic<Void> {

    private final Party buyer;
    private final Party stateRegulator;
    private final Party nationalRegulator;

    public TradeAndReport(Party buyer, Party stateRegulator, Party nationalRegulator) {
        this.buyer = buyer;
        this.stateRegulator = stateRegulator;
        this.nationalRegulator = nationalRegulator;
    }

    @Suspendable
    @Override
    public Void call() throws FlowException {

        // Obtain a reference to a notary we wish to use.
        /** METHOD 1: Take first notary on network, WARNING: use for test, non-prod environments, and single-notary networks only!*
         *  METHOD 2: Explicit selection of notary by CordaX500Name - argument can by coded in flow or parsed from config (Preferred)
         *
         *  * - For production you always want to use Method 2 as it guarantees the expected notary is returned.
         */
        final Party notary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0); // METHOD 1
        // final Party notary = getServiceHub().getNetworkMapCache().getNotary(CordaX500Name.parse("O=Notary,L=London,C=GB")); // METHOD 2

        HighlyRegulatedState outputState = new HighlyRegulatedState(buyer, getOurIdentity());

        TransactionBuilder transactionBuilder = new TransactionBuilder(notary)
                .addOutputState(outputState, HighlyRegulatedContract.ID)
                .addCommand(new HighlyRegulatedContract.Commands.Trade(), getOurIdentity().getOwningKey());

        SignedTransaction signedTransaction = getServiceHub().signInitialTransaction(transactionBuilder);

        List<FlowSession> sessions = ImmutableList.of(initiateFlow(buyer), initiateFlow(stateRegulator));
        // We distribute the transaction to both the buyer and the state regulator using `FinalityFlow`.
        subFlow(new FinalityFlow(signedTransaction, sessions));

        // We also distribute the transaction to the national regulator manually.
        subFlow(new ReportManually(signedTransaction, nationalRegulator));

        return null;
    }
}

@InitiatingFlow
public class ReportManually extends FlowLogic<Void> {
    private final ProgressTracker progressTracker = new ProgressTracker();
    private final SignedTransaction signedTransaction;
    private final Party regulator;

    public ReportManually(SignedTransaction signedTransaction, Party regulator) {
        this.signedTransaction = signedTransaction;
        this.regulator = regulator;
    }

    @Override
    public ProgressTracker getProgressTracker() {
        return progressTracker;
    }

    @Suspendable
    @Override
    public Void call() throws FlowException {
        FlowSession session = initiateFlow(regulator);
        session.send(signedTransaction);
        return null;
    }
}

@InitiatedBy(ReportManually.class)
public class ReportManuallyResponder extends FlowLogic<Void> {
    private final FlowSession counterpartySession;

    public ReportManuallyResponder(FlowSession counterpartySession) {
        this.counterpartySession = counterpartySession;
    }

    @Suspendable
    @Override
    public Void call() throws FlowException {
        SignedTransaction signedTransaction = counterpartySession.receive(SignedTransaction.class).unwrap(it -> it);
        // The national regulator records all of the transaction's states using
        // `recordTransactions` with the `ALL_VISIBLE` flag.
        getServiceHub().recordTransactions(StatesToRecord.ALL_VISIBLE, ImmutableList.of(signedTransaction));
        return null;
    }
}
```
{{< /tab >}}

{{< /tabs >}}

## How observer nodes operate

* By default, vault queries do not differentiate between states you recorded as a participant/owner, and states you
recorded as an observer. You will have to write custom vault queries that only return states for which you are a
participant/owner. See the [Example usage](api-vault-query.md#example-usage) section of the [API: Vault Query](api-vault-query.md) page for information on how to do this.
This also means that `Cash.generateSpend` should not be used when recording `Cash.State` states as an observer.

* When an observer node is sent a transaction with the `ALL_VISIBLE` flag set, any transactions in the transaction history
that have not already been received will also have `ALL_VISIBLE` states recorded. This mean a node that is both an observer
and a participant may have some transactions with all states recorded and some with only relevant states recorded, even
if those transactions are part of the same chain. As a result, there may be more states present in the vault than would be
expected if just those transactions sent with the `ALL_VISIBLE` recording flag were processed in this way.

* Nodes may re-record transactions if they have previously recorded them as a participant and wish to record them as an observer. However,  if this is done,
the node cannot resolve a forward chain of transactions. This means that if you wish to re-record a chain of transactions
and get the new output states to be correctly marked as consumed, the full chain must be sent to the node *in order*.
