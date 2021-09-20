---
aliases:
- /head/tutorial-observer-nodes.html
- /HEAD/tutorial-observer-nodes.html
- /tutorial-observer-nodes.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-tutorial-observer-nodes
    parent: corda-os-4-6-supplementary-tutorials-index
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

Adding support for observer nodes to your application is easy. The [IRS (interest rate swap) demo](https://github.com/corda/corda/blob/release/os/4.6/samples/irs-demo/cordapp/contracts-irs/src/main/kotlin/net/corda/irs/contract/IRS.kt) shows to do it.

Just define a new flow that wraps the `SendTransactionFlow/ReceiveTransactionFlow`, as follows:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
    @InitiatedBy(Requester::class)
    class AutoOfferAcceptor(otherSideSession: FlowSession) : Acceptor(otherSideSession) {
        @Suspendable
        override fun call(): SignedTransaction {
            val finalTx = super.call()
            // Our transaction is now committed to the ledger, so report it to our regulator. We use a custom flow
            // that wraps SendTransactionFlow to allow the receiver to customise how ReceiveTransactionFlow is run,
            // and because in a real life app you'd probably have more complex logic here e.g. describing why the report
            // was filed, checking that the reportee is a regulated entity and not some random node from the wrong
            // country and so on.
            val regulator = serviceHub.identityService.partiesFromName("Regulator", true).single()
            subFlow(ReportToRegulatorFlow(regulator, finalTx))
            return finalTx
        }
    }

    @InitiatingFlow
    class ReportToRegulatorFlow(private val regulator: Party, private val finalTx: SignedTransaction) : FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            val session = initiateFlow(regulator)
            subFlow(SendTransactionFlow(session, finalTx))
        }
    }

    @InitiatedBy(ReportToRegulatorFlow::class)
    class ReceiveRegulatoryReportFlow(private val otherSideSession: FlowSession) : FlowLogic<Unit>() {
        @Suspendable
        override fun call() {
            // Start the matching side of SendTransactionFlow above, but tell it to record all visible states even
            // though they (as far as the node can tell) are nothing to do with us.
            subFlow(ReceiveTransactionFlow(otherSideSession, true, StatesToRecord.ALL_VISIBLE))
        }
    }

```
{{% /tab %}}

{{< /tabs >}}


[AutoOfferFlow.kt](https://github.com/corda/corda/blob/release/os/4.6/samples/irs-demo/cordapp/workflows-irs/src/main/kotlin/net.corda.irs/flows/AutoOfferFlow.kt)

In this example, the `AutoOfferFlow` is the business logic, and we define two very short and simple flows to send
the transaction to the regulator. There are two important aspects to note here:


* The `ReportToRegulatorFlow` is marked as an `@InitiatingFlow` because it will start a new conversation, context
free, with the regulator.
* The `ReceiveRegulatoryReportFlow` uses `ReceiveTransactionFlow` in a special way - it tells it to send the
transaction to the vault for processing, including all states even if not involving our public keys. This is required
because otherwise the vault will ignore states that don’t list any of the node’s public keys, but in this case,
we do want to passively observe states we can’t change. So overriding this behaviour is required.

If the states define a relational mapping (see [API: Persistence](api-persistence.md)) then the regulator will be able to query the
reports from their database and observe new transactions coming in via RPC.


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
