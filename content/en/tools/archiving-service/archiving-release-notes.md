---
date: '2026-06-03T12:00:00Z'
menu:
  tools:
    identifier: release-notes-archiving
    parent: tools-archiving
    name: "Release notes"
title: Archive Service release notes
weight: 705
---

# Archive Service release notes

The Archive Service is a standalone service that operates on a different release cadence to the Corda platform.

The following table shows the compatibility of the Archive Service versions with Corda Enterprise:

| Archive Service version | Corda Enterprise version | JDK version |
|------------------------|--------------------------|-------------|
| 2.x                    | 4.12.x and above         | JDK 17      |

The [Archive Service 1.x series]({{< relref "../archiving-service-1.x/archiving-release-notes.md" >}}) supports Corda Enterprise versions up to and including 4.12.

{{< note >}}
If you deviate from the above compatibility guidelines, the Archive Service will not work.
{{< /note >}}

## Corda Enterprise 4.12

### Archive Service 2.0

Archive Service 2.0 is a major release supporting Java 17 and Kotlin 1.9.20. This version works with Corda 4.12.

#### Key changes in 2.0

* **LedgerGraph dependency removed**: The Archive Service no longer requires LedgerGraph. It now builds its own internal transaction dependency graph using the vault database directly.
* **Iterative archiving model**: A new iterative approach processes transactions incrementally, tracking dependencies and walking back through chains to identify archivable items. This replaces the previous in-memory LedgerGraph-based approach.
* **Runtime filters removed**: The `filterList` and `filterConfig` parameters have been removed from all flows and library APIs. Transaction eligibility is now controlled via the `archivableContractClassStatePrefixes` configuration parameter.
* **New configuration parameter `archivableContractClassStatePrefixes`**: An optional list of contract class name prefixes that controls which transactions are eligible for archiving. When set, only transactions where all states' contract classes match at least one prefix are considered archivable.
* **New CLI commands**:
  * `process-all-pending` — refreshes the archiving database by processing pending transactions and collecting archivable items.
  * `statistics` — displays iterative archiving statistics (unprocessed count, pending walkback, pending delete, sizes).
  * `status` — displays current archiving database maintenance operation status and history.
* **New flows**:
  * `ProcessAllPendingFlow` — processes pending transactions and collects archivable items with configurable time limit, batch size, and age filtering.
  * `StatisticsFlow` — returns iterative archiving statistics.
  * `StatusFlow` — returns current operation status and history.
  * `PerformanceStatsFlow` and `ResetPerformanceStatsFlow` — retrieve and reset per-step performance statistics (wall-clock time, CPU time, throughput). These flows are subject to change and are not a final part of the Archive Service API.
* **Updated flow signatures**: `ListItemsFlow` and `MarkItemsFlow` now accept iterative processing parameters (`bypassProcessAllPending`, `timeLimit`, `notNewerThan`, `batchSize`, `skipSafetyIntervalCheck`) instead of filter parameters. `CreateSnapshotFlow` no longer accepts `additionalTransactionTables` or `additionalAttachmentTables` (these are now auto-detected).
* **Updated library APIs**: New library classes `ProcessAllPending`, `Statistics` and `Status`. Updated `ListItems` and `MarkItems` to match the new flow signatures.
* **Archive manifest**: The `ZippedFileExporter` now writes a manifest file `manifest-<snapshot>.csv` next to the zip files, listing each exported transaction and attachment with its vault timestamp, size, and the participants of the transaction's states. The participants cover both the states created by the transaction and the states it consumes. The manifest allows the contents of an archive to be audited without opening the zip files. Participant extraction can be disabled with the new `exporter.extractParticipants` configuration property (default `true`). The `TransactionExporter` and `AttachmentExporter` interfaces gained optional overloads carrying the timestamp and participants; existing custom exporters are unaffected.

The 1.x series release notes can be found in the [Archive Service 1.x release notes]({{< relref "../archiving-service-1.x/archiving-release-notes.md" >}}) page.
