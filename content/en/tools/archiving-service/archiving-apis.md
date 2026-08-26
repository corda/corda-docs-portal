---
date: '2026-06-03T12:00:00Z'
menu:
  tools:
    parent: tools-archiving
tags:
- archive
- backup schema
- archive install
- archive transactions


title: Archive Service APIs
weight: 730
---


# Archive Service APIs

{{< note >}}
Archive Service 2.0 introduces an iterative archiving model that replaces the previous LedgerGraph-based filtering approach. Runtime filters (`filterList`, `filterConfig`) have been removed from all flows. Transaction eligibility is now controlled via the `archivableContractClassStatePrefixes` CorDapp configuration parameter.
{{< /note >}}

## Transaction Filtering

The Archive Service supports filtering which transactions are eligible for archiving based on their
contract class names. This is configured via the `archivableContractClassStatePrefixes` CorDapp
configuration entry.

When this list is set, a transaction is only considered archivable if **all** of its states' (inputs,
outputs, and references) contract class names start with at least one of the configured prefixes.
The matching is case-insensitive.

Non-archivable transactions are still tracked in the iterative archiving tables (so the dependency
graph remains correct), but they act as barriers that prevent walkback propagation — they will never
be marked for deletion.

If the list is empty or not configured, all transactions are archivable (default behavior).

The filter is evaluated live at walkback time rather than at discovery time. Note that, like any
Archive Service CorDapp configuration change, the node must be restarted before a change to this
list is picked up at all — but once picked up, it takes effect immediately for any transaction
still awaiting walkback, with no reset or reprocessing of already-tracked transactions required.

## Flows

The following flows are exposed by the Archive Service:

```kotlin
/**
 * Invoke the list jobs flow to return details on the archive jobs.
 *
 * @property jobCount If set, return details on the current and previous jobs
 */
@InitiatingFlow
@StartableByRPC
class ListJobsFlow(
    private val jobCount: Int? = null
) : FlowLogic<List<ArchivingJob>>()

/**
 * Flow to process all pending transactions and then collect all archivable items.
 * This flow drives the same internal operations as the `AddTransactionsFlow` and `CollectArchivableFlow`
 * building blocks (running the first until completion, then the second until pendingWalkBack reaches 0).
 * Those two flows, along with `StopFlow`, are internal (`@CordaInternal`) and not intended to be started
 * directly — `ProcessAllPendingFlow` is the supported entry point for this workflow.
 *
 * @param timeLimit Maximum time to run both operations. Default is 8 hours.
 * @param notNewerThan Only collect transactions older than this timestamp. Default is now minus the grace period.
 * @param batchSize Batch size for the internal transaction-processing step. Default is 1,000.
 * @param skipSafetyIntervalCheck Whether to skip the safety interval check when collecting archivable items. Default is false.
 */
@InitiatingFlow
@StartableByRPC
class ProcessAllPendingFlow(
    private val timeLimit: Duration = Duration.ofHours(8),
    private val notNewerThan: Instant? = null,
    private val batchSize: Int = 1_000,
    private val skipSafetyIntervalCheck: Boolean = false
) : FlowLogic<Unit>()

/**
 * Flow to get statistics about the iterative archiving process.
 *
 * This flow is subject to change — its signature and result fields may change in later versions —
 * and should not be relied on as a stable, versioned API.
 */
@InitiatingFlow
@StartableByRPC
class StatisticsFlow : FlowLogic<StatisticsResult>()

/**
 * Result data for the iterative archiving statistics.
 */
@CordaSerializable
data class StatisticsResult(
    val unprocessedTransactionCount: Long,
    val pendingWalkbackCount: Long,
    val pendingDeleteCount: Long,
    val minAgeSeconds: Long,
    val transactionBeforeMinAgeCount: Long,
    val transactionAfterMinAgeCount: Long,
    val archivableTransactionSize: Long,
    val archivableAttachmentSize: Long
)

/**
 * Flow to get the current status and operation history of the maintenance of the archive database.
 * Corda keeps this history in memory, so only the history since the last restart of the node will be returned.
 *
 * This flow is subject to change — its signature and result fields may change in later versions —
 * and should not be relied on as a stable, versioned API.
 *
 * @property maxHistoryItems Maximum number of history items to return (default 10)
 */
@InitiatingFlow
@StartableByRPC
class StatusFlow(
    private val maxHistoryItems: Int = 10
) : FlowLogic<StatusResult>()

/**
 * Result data for the archive service status.
 */
@CordaSerializable
data class StatusResult(
    val currentOperation: ArchiveOperation,
    val recentHistory: List<OperationHistoryEntry>
)

/**
 * Represents a completed operation in the archive service history.
 */
@CordaSerializable
data class OperationHistoryEntry(
    val operationType: ArchiveOperation,
    val startTime: Instant,
    val finishTime: Instant,
    val processedItemCount: Int
)

/**
 * Invoke the list items flow to return details on the archivable items.
 * First it refreshes the archiving data structures by processing all pending transactions.
 *
 * @property listArchivableItems if true return list of item IDs
 * @property bypassProcessAllPending if true, bypass refreshing the archiving data structures. Default is false.
 * @property timeLimit maximum duration to process the pending transactions. Default is 8 hours.
 * @property notNewerThan only collect transactions older than this timestamp (ISO-8601 format). Default is null which means now minus grace period.
 * @property batchSize number of transactions to process in a batch (default: 1000, min: 10, max: 1000000)
 * @property skipSafetyIntervalCheck whether to skip the safety interval check when collecting items. Default is false.
 */
@InitiatingFlow
@StartableByRPC
class ListItemsFlow(
    private val listArchivableItems: Boolean,
    private val bypassProcessAllPending: Boolean = false,
    private val timeLimit: Duration = Duration.ofHours(8),
    private val notNewerThan: Instant? = null,
    private val batchSize: Int = 1_000,
    private val skipSafetyIntervalCheck: Boolean = false
) : FlowLogic<ListItemsResults>()

/**
 * Mark items as archivable using the iterative archive service's model.
 * First it refreshes the archiving data structures by processing all pending transactions,
 * then it marks all archivable items with the provided snapshot name.
 *
 * @property snapshot name of the archive snapshot recorded in the archive log tables
 * @property bypassProcessAllPending if true, bypass refreshing the archiving data structures. Default is false.
 * @property timeLimit maximum duration to process the pending transactions. Default is 8 hours.
 * @property notNewerThan only collect transactions older than this timestamp (ISO-8601 format). Default is null which means now minus grace period.
 * @property batchSize number of transactions to process in a batch (default: 1000, min: 10, max: 1000000)
 * @property skipSafetyIntervalCheck whether to skip the safety interval check when collecting items. Default is false.
  */
 @InitiatingFlow
 @StartableByRPC
 class MarkItemsFlow(
    private val snapshot: String?,
    private val bypassProcessAllPending: Boolean = false,
    private val timeLimit: Duration = Duration.ofHours(8),
    private val notNewerThan: Instant? = null,
    private val batchSize: Int = 1_000,
    private val skipSafetyIntervalCheck: Boolean = false
 ) : FlowLogic<MarkItemsResults>()

/**
 * Mark specific transactions, identified by their ids, for deletion from the vault - together
 * with every transaction that depends on them - without requiring the iterative archiving model
 * to be populated.
 *
 * The transactions actually deleted are the requested ones plus their forward dependency closure:
 * every transaction that consumes any of their outputs, transitively, as recorded by the vault
 * and by the iterative model's consumption records. Deleting a transaction while a dependent
 * remains would leave the dependent with a broken backchain, so every output of every selected
 * transaction must be provably consumed within the closure, and no transaction the iterative
 * model records as referencing a closure output may survive. Outputs that are unconsumed or
 * whose consumption cannot be proven, and surviving referencers, fail the flow and are reported;
 * the operator can find the related transactions through their CorDapp's own queries (for
 * example by linear id) and include those ids in the request.
 *
 * The archivableContractClassStatePrefixes filter is deliberately ignored: it selects what
 * automatic archiving may take, whereas here the operator names the transactions explicitly.
 *
 * This flow only marks the transactions under an archive job, exactly as MarkItemsFlow does for
 * the normal archiving path. The snapshot, export and deletion are then performed by the
 * unchanged CreateSnapshotFlow, ExportSnapshotFlow and DeleteMarkedFlow. Note that aborting the
 * job afterwards with RestoreSnapshotFlow restores the data but not the model state: the closure
 * stays pending delete in the iterative model, so the next normal archiving job archives it -
 * the same way walkback decisions survive an aborted normal job.
 *
 * @property transactionIds ids of the transactions to delete
 * @property snapshot name of the archive snapshot recorded in the archive log tables
 * @property dryRun if true, only compute and report the dependency closure; nothing is marked
 * @property skipSafetyIntervalCheck whether to skip the safety interval check on the newest
 *   transaction of the closure. Default is false.
 */
@InitiatingFlow
@StartableByRPC
class DeleteTransactionsFlow(
    private val transactionIds: List<String>,
    private val snapshot: String? = null,
    private val dryRun: Boolean = false,
    private val skipSafetyIntervalCheck: Boolean = false
) : FlowLogic<DeleteTransactionsResults>()

/**
 * Copy the marked items from the vault schema to the archive schema.
 *
 * @property additionalQueryableTables List of any queryable tables to copy
 * @property record If true then record SQL rather than execute it
 */
@InitiatingFlow
@StartableByRPC
class CreateSnapshotFlow(
    private val additionalQueryableTables: List<Pair<String, String>>,
    private val record: Boolean
) : FlowLogic<CreateSnapshotResults>()

/**
 * Export the archived items to long-term storage.
 *
 * @property exporterList list of exporters to execute
 * @property exporterConfig exporter configuration data
 */
@InitiatingFlow
@StartableByRPC
class ExportSnapshotFlow(
    private val exporterList: List<String>?,
    private val exporterConfig: Map<String, Any>
) : FlowLogic<ExportSnapshotResults>()

/**
 * Import the archived items from long-term storage.
 * The value of [importer] can be null if the importer is specified in [importerConfig]
 * or in the CorDapp configuration.
 *
 * @property snapshot Snapshot to import
 * @property importer Importer to execute
 * @property importerConfig Importer configuration data
 * @property record Record SQL
 */
@InitiatingFlow
@StartableByRPC
class ImportSnapshotFlow(
    private val snapshot: String,
    private val importer: String?,
    private val importerConfig: Map<String, Any>,
    private val record: Boolean
) : FlowLogic<ImportSnapshotResults>()

/**
 * Delete the marked items from the vault schema.
 *
 * @property record If true then record SQL rather than execute it
 */
@InitiatingFlow
@StartableByRPC
class DeleteMarkedFlow(
    private val record: Boolean = false
) : FlowLogic<DeleteMarkedResults>()

/**
 * Delete the marked items from the archive schema.
 *
 * @property record If true then record SQL rather than execute it
 */
@InitiatingFlow
@StartableByRPC
class DeleteSnapshotFlow(
    private val record: Boolean = false
) : FlowLogic<DeleteSnapshotResults>()

/**
 * Restore any items deleted from the vault as part of an archive job.
 * There should never be more than one pending job, however
 * this flow must restore all pending jobs to guarantee that the vault is consistent.
 *
 * @property record If true then record SQL rather than execute it
 */
@InitiatingFlow
@StartableByRPC
class RestoreSnapshotFlow(
    private val record: Boolean
) : FlowLogic<RestoreSnapshotResults>()
```

## Performance tracking flows

The Archive Service tracks performance statistics for each archiving step (`ProcessNewTransactions`, `CollectArchivable`, `MarkItems`, `CreateSnapshot`, `ExportSnapshot`, `DeleteMarked`, and `DeleteSnapshot`). For each step, the following metrics are collected:

* Wall-clock time spent in the step.
* JVM process CPU time consumed while the step was running.
* CPU utilization — the CPU time relative to the wall-clock time and the number of available processors. 100% means all processors were busy with the node's JVM for the whole duration of the step.
* Number of transactions processed.
* Throughput (transactions per second).

The output also includes the instantaneous system CPU load, the number of processors available to the JVM, the total transaction count, and the total elapsed and CPU times. The statistics are returned in a human-readable format, followed by a CSV representation of the same data, and are also written to the node's log.

The statistics are kept in memory, so they cover only the period since the last node restart (or the last reset).

{{< note >}}
The performance tracking flows are provided as a troubleshooting and tuning aid. They are subject to change and are not a final part of the Archive Service API.
{{< /note >}}

```kotlin
/**
 * A Corda flow that retrieves and formats performance statistics.
 *
 * This flow collects archiving step metrics such as wall-clock time, JVM process CPU time,
 * transactions processed, and throughput (transactions per second) for each archiving step,
 * formats them into a human-readable and CSV-compatible string, and logs the result.
 */
@InitiatingFlow
@StartableByRPC
class PerformanceStatsFlow : FlowLogic<String>()

/**
 * Resets all collected performance statistics.
 *
 * After execution, all per-step metrics (time spent, transactions processed) are cleared.
 */
@InitiatingFlow
@StartableByRPC
class ResetPerformanceStatsFlow : FlowLogic<String>()
```

For example, the flows can be started from the node shell:

```text
>>> flow start PerformanceStatsFlow
>>> flow start ResetPerformanceStatsFlow
```

A typical workflow is to run `ResetPerformanceStatsFlow` before an archiving run (for example, before changing the batch size or the parallelism settings described in [Performance tuning]({{< relref "archiving-service-index.md#performance-tuning" >}})), and then run `PerformanceStatsFlow` afterwards to compare the throughput of the individual steps.
