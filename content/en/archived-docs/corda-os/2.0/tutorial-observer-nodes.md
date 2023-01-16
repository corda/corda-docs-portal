---
aliases:
- /releases/release-V2.0/tutorial-observer-nodes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-2-0:
    identifier: corda-os-2-0-tutorial-observer-nodes
    parent: corda-os-2-0-tutorials-index
    weight: 1160
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


{{< warning >}}
Nodes which act as both observers and which directly take part in the ledger are not supported at this
time. In particular, coin selection may return states which you do not have the private keys to be able to sign
for. Future versions of Corda may address this issue, but for now, if you wish to both participate in the ledger
and also observe transactions that you can’t sign for you will need to run two nodes and have two separate
identities.

{{< /warning >}}


