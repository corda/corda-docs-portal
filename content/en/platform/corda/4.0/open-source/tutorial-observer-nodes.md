---
aliases:
- /releases/release-V4.0/tutorial-observer-nodes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-tutorial-observer-nodes
    parent: corda-os-4-0-tutorials-index
    weight: 1170
tags:
- tutorial
- observer
- nodes
title: Observer nodes
---




# Observer nodes

Posting transactions to an observer node is a common requirement in finance, where regulators often want
to receive comprehensive reporting on all actions taken. By running their own node, regulators can receive a stream
of digitally signed, de-duplicated reports useful for later processing.

Adding support for observer nodes to your application is easy. The IRS (interest rate swap) demo shows to do it.

Just define a new flow that wraps the SendTransactionFlow/ReceiveTransactionFlow, as follows:

{{< tabs name="tabs-1" >}}
{{< /tabs >}}

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


## Caveats


* By default, vault queries do not differentiate between states you recorded as a participant/owner, and states you
recorded as an observer. You will have to write custom vault queries that only return states for which you are a
participant/owner. See [https://docs.corda.net/api-vault-query.html#example-usage](https://docs.corda.net/api-vault-query.html#example-usage) for information on how to do this.
This also means that `Cash.generateSpend` should not be used when recording `Cash.State` states as an observer
* Nodes only record each transaction once. If a node has already recorded a transaction in non-observer mode, it cannot
later re-record the same transaction as an observer. This issue is tracked here:
[https://r3-cev.atlassian.net/browse/CORDA-883](https://r3-cev.atlassian.net/browse/CORDA-883)
* When an observer node is sent a transaction with the ALL_VISIBLE flag set, any transactions in the transaction history
that have not already been received will also have ALL_VISIBLE states recorded. This mean a node that is both an observer
and a participant may have some transactions with all states recorded and some with only relevant states recorded, even
if those transactions are part of the same chain. As a result, there may be more states present in the vault than would be
expected if just those transactions sent with the ALL_VISIBLE recording flag were processed in this way.

