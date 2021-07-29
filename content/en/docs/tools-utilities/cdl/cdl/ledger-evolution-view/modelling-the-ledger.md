---
title: Modelling the ledger
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-ledger-evolution-view"
    identifier: "cdl-ledger-evolution-view-modelling-the-ledger"
    weight: 10

tags:
- cdl
- cordapp design language
- ledger evolution
- cordapp diagram
---

# Modelling the Ledger

The Corda Ledger can be considered as a Directed Acyclic Graph (DAG) in which:

* States are created as outputs to a transaction.
* States are consumed as inputs to transactions.
* Commands are properties of transactions.
* Parties sign transactions.

You could illustrate this as follows:

{{< figure zoom="../resources/cdl-ledger-dag.png" width="800" title="Click to zoom image in new tab/window" >}}

However, it is difficult to get all the information you may want to show into this format. To convey more information, you can use a similar form but modify the graph's nodes to align more closely to the representations of states already introduced in the Smart Contract view.

In the following examples, the diagrams do not show the signers to the transaction as separate nodes, instead they are attached to the transactions directly.
