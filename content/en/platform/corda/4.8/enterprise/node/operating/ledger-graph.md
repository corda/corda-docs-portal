---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-corda-nodes-operating
    identifer: corda-enterprise-4-8-ledger-graph
tags:
- in memory
- transaction data
- install
- node operator
- DAG
- ledger graph

title: LedgerGraph
weight: 500
---

# LedgerGraph

LedgerGraph is a CorDapp you can use to get in-memory access to transaction data. If you install LedgerGraph on a node, it keeps transaction information in a graph structure. As not all transactions are related to all other transactions, there can actually be multiple components in the graph: each a directed acyclic graph (DAG).

LedgerGraph enables other CorDapps, such as the set of Collaborative Recovery CorDapps, to have near real-time access to data concerning all of a node’s transactions and their relationships. Without it, many operations would be unacceptably slow and impractical.

{{< warning >}}
LedgerGraph is a dependency for the set of [Collaborative Recovery]({{< relref "../../../../../../tools/collaborative-recovery/cl-index.md" >}}) CorDapps V1.1 and above. If you are using an earlier version of Collaborative Recovery, you should not install the stand-alone LedgerGraph.
{{< /warning >}}

Read the full documentation about [LedgerGraph]({{< relref "../../../../../../tools/ledgergraph/ledgergraph-index.md" >}}).