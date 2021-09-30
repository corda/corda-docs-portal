---
date: '2021-04-24T00:00:00Z'
section_menu: tools
menu:
  tools:
    name: LedgerGraph
    weight: 800
    identifier: tools-ledgergraph
title: LedgerGraph
---

# LedgerGraph

LedgerGraph is a CorDapp you can use to get in-memory access to transaction data. Transaction information is kept in a graph structure on any node where LedgerGraph is installed. As not all transactions are related to all other transactions, there can actually be multiple components in the graph: each a directed acyclic graph (DAG).

LedgerGraph enables other CorDapps, such as the set of Collaborative Recovery CorDapps, to have near real-time access to data concerning all of a node’s transactions and their relationships. Without it, many operations would be unacceptably slow and impractical.

{{< warning >}}
LedgerGraph is a dependency for the set of [Collaborative Recovery](../../../en/tools/collaborative-recovery/ci-index.md) CorDapps V1.1 and above. If you are using an earlier version of Collaborative Recovery, you should not install the stand-alone LedgerGraph.
{{< /warning >}}

Read the full documentation about [LedgerGraph](../../../en/platform/corda/4.8/enterprise/node/operating/ledger-graph.md).
