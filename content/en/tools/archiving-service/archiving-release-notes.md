---
date: '2026-06-03T12:00:00Z'
menu:
  tools:
    identifier: release-notes-archiving
    parent: tools-archiving
    name: "Release notes"
title: Archive Service 2.x release notes
weight: 705
---

# Archive Service 2.x release notes

The Archive Service is a standalone service that operates on a different release cadence to the Corda platform.

The following table shows the compatibility of the Archive Service versions with Corda Enterprise:

| Archive Service version | Corda Enterprise version | JDK version |
|------------------------|--------------------------|-------------|
| 2.0.1                  | 4.12.x and above         | JDK 17      |
| 2.0                    | 4.12.x to 4.14.x         | JDK 17      |

The [Archive Service 1.x series]({{< relref "../archiving-service-1.x/archiving-release-notes.md" >}}) supports Corda Enterprise versions up to and including 4.12.

{{< note >}}
If you deviate from the above compatibility guidelines, the Archive Service will not work. In particular, Archive Service 2.0 does not start on a Corda Enterprise 4.15 node; use 2.0.1 or later.
{{< /note >}}

## Archive Service 2.0.1

Archive Service 2.0.1 is a compatibility release for Corda Enterprise 4.15. It runs on Corda Enterprise 4.12.x and later, so the same Archive Service version serves a node before and after its upgrade to 4.15.

Upgrading from 2.0 is a replacement of the two JAR files (the CorDapp and the command-line tool). The CorDapp configuration file follows the name of the CorDapp JAR, so rename `cordapps/config/archive-service-2.0.conf` to `archive-service-2.0.1.conf`; its contents need no change. There is no database schema change: 2.0.1 adds no Liquibase change sets and alters none of the existing ones, so the Database Management Tool has nothing to apply for the Archive Service itself. The upgrade of the node to Corda Enterprise 4.15 has its own database migration step, which also re-validates the Archive Service change sets already recorded in `DATABASECHANGELOG`; see the Corda Enterprise 4.15 upgrade notes.

### Corda Enterprise 4.15 support

Corda Enterprise 4.15 upgrades the node's Hibernate from version 5 to version 7. The node converts CorDapps built for the earlier `javax.persistence` API as it loads them, but it refuses a CorDapp that refers to Hibernate 5 classes that Hibernate 7 no longer has. Archive Service 2.0 did so in the [App Entity Manager]({{< relref "app-entity-manager.md" >}}), which the Archive Service uses for its [backup schema]({{< relref "archiving-service-index.md#using-the-backup-schema" >}}). In 2.0.1:

* The App Entity Manager starts its own Hibernate session factory on Hibernate 5 and Hibernate 7 nodes alike. On a Hibernate 7 node it applies the node's own Hibernate compatibility settings, so that it reads and writes the node's tables exactly as the node does. The configuration is unchanged, including the `javax.persistence.jdbc.*` property names. See [Hibernate 7 nodes]({{< relref "app-entity-manager.md#hibernate-7-nodes-corda-enterprise-415-and-later" >}}).
* The Archive Service reads the date, time and binary columns that Hibernate 7 returns as different Java types than Hibernate 5. Exported transaction timestamps and the CSV exports of queryable state tables read the same whichever Corda Enterprise version produced them.

### Changed behaviour

* The App Entity Manager accepts a new property, `hibernate.jdbc.time_zone`. It has no default, so the behaviour is unchanged: a CorDapp that uses the library for an off-ledger database of its own stores and reads its `Instant` and timestamp values in the JVM's time zone, as before. Set the property to `UTC`, the Corda node's own setting, to store and read them as the node does, for example in a CorDapp that reads the node's tables through the library. The Archive Service itself does not depend on it: its own queries run through the node's session factory, and the session factory of the backup schema only runs SQL statements that copy, restore and delete rows within the database.

## Archive Service 2.0

Archive Service 2.0 is a major release supporting Java 17 and Kotlin 1.9.25. The minimum supported Corda Enterprise version is 4.12.

### Key changes in 2.0

* **LedgerGraph dependency removed**: The Archive Service no longer requires LedgerGraph. It now builds its own internal transaction dependency graph using the vault database directly.
* **Iterative archiving model**: A new iterative approach processes transactions incrementally, tracking dependencies and walking back through chains to identify archivable items. This replaces the previous in-memory LedgerGraph-based approach.
* **Runtime filters removed**: The `filterList` and `filterConfig` parameters have been removed from all flows and library APIs. Transaction eligibility is now controlled via the `archivableContractClassStatePrefixes` configuration parameter.
* **New configuration parameter `archivableContractClassStatePrefixes`**: An optional list of contract class name prefixes that controls which transactions are eligible for archiving. When set, only transactions where all states' contract classes match at least one prefix are considered archivable.
* **New CLI commands**:
  * `process-all-pending` — refreshes the archiving database by processing pending transactions and collecting archivable items.
  * `statistics` — displays iterative archiving statistics (unprocessed count, pending walkback, pending delete, sizes).
  * `status` — displays current archiving database maintenance operation status and history.
  * `recalculate-filtering` — re-applies a changed `archivableContractClassStatePrefixes` filter to the transactions an earlier run already stopped because of the previous filter, which a configuration change alone does not reach. Run it after widening the filter and restarting the node, followed by `process-all-pending`. See the [Recalculate Filtering command]({{< relref "archiving-cli.md#recalculate-filtering-command" >}}).
  * `delete-transactions` — marks specific transactions, identified by their ids, together with every transaction that depends on them, for deletion from the vault — for example, because they hold data that should not be in the ledger. The job is completed with the unchanged `export-snapshot` and `delete-vault` commands. See the [Delete Transactions command]({{< relref "archiving-cli.md#delete-transactions-command" >}}) for the consistency checks and caveats.
* **New flows**:
  * `ProcessAllPendingFlow` — processes pending transactions and collects archivable items with configurable time limit, batch size, and age filtering.
  * `StatisticsFlow` — returns iterative archiving statistics.
  * `StatusFlow` — returns current operation status and history.
  * `RecalculateFilteringFlow` — re-arms walkback for transactions stopped by a previous `archivableContractClassStatePrefixes` filter (the flow behind the `recalculate-filtering` command).
  * `DeleteTransactionsFlow` — marks specific transactions and their forward dependency closure for deletion (the flow behind the `delete-transactions` command).
  * `PerformanceStatsFlow` and `ResetPerformanceStatsFlow` — retrieve and reset per-step performance statistics (wall-clock time, CPU time, throughput). These flows are subject to change and are not a final part of the Archive Service API.
* **Updated flow signatures**: `ListItemsFlow` and `MarkItemsFlow` now accept iterative processing parameters (`bypassProcessAllPending`, `timeLimit`, `notNewerThan`, `batchSize`, `skipSafetyIntervalCheck`) instead of filter parameters. `CreateSnapshotFlow` no longer accepts `additionalTransactionTables` or `additionalAttachmentTables` (these are now auto-detected).
* **Updated library APIs**: New library classes `ProcessAllPending`, `RecalculateFiltering`, `DeleteTransactions`, `Statistics` and `Status`. Updated `ListItems` and `MarkItems` to match the new flow signatures.
* **Archive manifest**: The `ZippedFileExporter` now writes a manifest file `manifest-<snapshot>.csv` next to the zip files, listing each exported transaction and attachment with its vault timestamp, size, and the participants of the transaction's states. The participants cover both the states created by the transaction and the states it consumes; those of the consumed states are recorded on the archive log when the items are marked, by joining the iterative archiving model to the vault's `state_party` table, and the export reads the recorded value. Consumed states the vault holds no participants for, because the node knows them only through the back chain, are resolved by loading the transactions which created them. The manifest allows the contents of an archive to be audited without opening the zip files. Recording the participants can be turned off with the new `exporter.extractParticipants` configuration property, which avoids the consumed-state lookup when marking the items and the deserialization of each exported transaction. The `TransactionExporter` and `AttachmentExporter` interfaces gained optional overloads carrying the timestamp and participants; existing custom exporters are unaffected.
* **Index on the node's transaction table**: The CorDapp's schema migration now creates `node_transactions_status_timestamp_tx_id_idx` on `node_transactions (status, timestamp, tx_id)`, and the query that reads new transactions was rewritten so that the database serves each batch from it as a single index range scan. Without the index, every batch was a full scan and a sort of the transaction table, so processing a large ledger took time proportional to the square of its size (301 ms per 1,000-row batch on a 3 million-row PostgreSQL table). The index costs about 110 bytes per transaction and is the same one the Corda Enterprise transaction validation utility requires for parallel reading; the change set skips itself if an equivalent index already exists. Apply the migration with the Database Management Tool before starting the node with the new version; see [Database migration]({{< relref "archiving-service-index.md#database-migration" >}}).

The 1.x series release notes can be found in the [Archive Service 1.x release notes]({{< relref "../archiving-service-1.x/archiving-release-notes.md" >}}) page.
