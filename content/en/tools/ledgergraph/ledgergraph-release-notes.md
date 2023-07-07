---
date: '2022-09-15'
menu:
  tools:
    parent: tools-ledgergraph
    identifer: ledger-graph-release-notes
title: Release notes
weight: 801
---

# LedgerGraph release notes

LedgerGraph is a standalone service that operates on a different release cadence to the Corda platform. 

## LedgerGraph 1.2.5 release notes

In this release:

* It is now possible to enable `inboundReferencesOnly` when checking if a DAG object is related to any other DAG that is unconsumed using the `isRelatedToUnconsumedDAG` method. This ignores DAGs that have an outbound reference to an unconsumed DAG.

## LedgerGraph 1.2.4 release notes

In this release:

* A configuration option has been added which allows LedgerGraph to handle transactions that cause failures during initialization. For more information, see the [LedgerGraph]({{< relref "ledgergraph-index.md#in-v124" >}}) documentation.

## LedgerGraph 1.2.3 release notes
 
In this release:

* Logging of the Archiving tool has been increased to aid in troubleshooting.