---
date: '2022-09-15'
menu:
  tools:
    parent: tools-ledger-graph
    identifier: ledger-graph-release-notes
title: Release notes
weight: 801
---

# LedgerGraph release notes

LedgerGraph is a standalone service that operates on a different release cadence to the Corda platform.

The following table shows the compatibility of the LedgerGraph service versions with Corda Enterprise:

| LedgerGraph version          | Corda Enterprise version    | JDK version      |
|------------------------------|-----------------------------| -----------------|
| 1.2.x                        | 4.11.x and below            | JDK 8            |
| 1.3.x                        | 4.12.x                      | JDK 17           |

## LedgerGraph 1.3 release notes

LedgerGraph 1.3 is a major release supporting Java 17 and Kotlin 1.9.20. If you want to use LedgerGraph, this is the only release that works with Corda 4.12.

## LedgerGraph 1.2.5 release notes

In this release:

* It is now possible to enable `inboundReferencesOnly` when checking if a DAG object is related to any other DAG that is unconsumed using the `isRelatedToUnconsumedDAG` method. This ignores DAGs that have an outbound reference to an unconsumed DAG.

## LedgerGraph 1.2.4 release notes

In this release:

* A configuration option has been added which allows LedgerGraph to handle transactions that cause failures during initialization. For more information, see the [LedgerGraph]({{< relref "ledgergraph-index.md#in-v124" >}}) documentation.

## LedgerGraph 1.2.3 release notes

In this release:

* Logging of the Archiving tool has been increased to aid in troubleshooting.
