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


title: Archive Service Library
weight: 725
---

# The Archive Service library

The Archive Service Library provides programmatic access to the Archive Service. The library provides the following Archive Service APIs:

* `ListJobs`.
* `ProcessAllPending`.
* `Statistics`.
* `Status`.
* `ListItems`.
* `MarkItems`.
* `DeleteTransactions`.
* `CreateSnapshot`.
* `ExportSnapshot`.
* `ImportSnapshot`.
* `DeleteMarked`.
* `DeleteSnapshot`.
* `RestoreSnapshot`.

{{< note >}}
Archive Service 2.0 no longer uses runtime filters. The `filterList` and `filterConfig` parameters have been removed from `ListItems` and `MarkItems`. Transaction eligibility is now controlled via the `archivableContractClassStatePrefixes` CorDapp configuration parameter.
{{< /note >}}

## Remote Procedure Call (RPC) connection

The first step in using the library is to establish a RPC connection to the Corda node:

```kotlin
val context = RPCClientService(rpcAddress.toString(), user, password)
```

The RPC credentials must contain the RPC settings URL and a user account with
sufficient privileges to run the Archive Service flows.

## Archive Service APIs

The following APIs are provided by the Archive Service Library.

### List jobs

Returns the list of active Archive Service jobs.

```kotlin
/**
 * Invoke the list jobs command to retrieve details on the current archive job.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property jobCount Report on completed jobs if set
 * @property progressTree Callback used to report progress
 */
class ListJobs(
    private val rpcClient: RPCClientService,
    private val jobCount: Int? = null,
    private val progressTree: ProgressTree? = null
) {
    /**
     * Execute the list jobs command
     *
     * @return List of active archive jobs
     */
    fun execute(): List<ArchivingJob>
}
```

### Process all pending

Processes all pending transactions and collects all archivable items in the iterative archive service.

```kotlin
/**
 * Invoke the process all pending command to process all pending transactions
 * and collect all archivable items in the iterative archive service.
 *
 * This command can only be called when the node is online.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property timeLimit Maximum time to run both operations
 * @property notNewerThan Only collect transactions older than this timestamp
 * @property batchSize Number of transactions to process in a batch
 * @property skipSafetyIntervalCheck Whether to skip the safety interval check when collecting archivable items
 */
class ProcessAllPending(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val timeLimit: Duration = Duration.ofHours(8),
    private val notNewerThan: Instant? = null,
    private val batchSize: Int = 1000,
    private val skipSafetyIntervalCheck: Boolean = false
) {
    /**
     * Execute the process all pending command by invoking the ProcessAllPendingFlow
     *
     */
    fun execute(): Unit
}
```

### Statistics

Retrieves statistics about the iterative archiving process.

{{< note >}}
The underlying `StatisticsFlow` is subject to change — its output fields may change in later versions — and should not be relied on as a stable, versioned API.
{{< /note >}}

```kotlin
/**
 * Retrieve statistics about the iterative archiving process.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 */
class Statistics(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null
) {
    /**
     * Retrieve statistics about the iterative archiving process.
     *
     * @return Iterative archive statistics results
     */
    fun execute(): StatisticsResult
}
```

### Status

Retrieves the current status and operation history of the iterative archive database. Corda keeps this history in memory, so only the history since the last restart of the node will be returned.

{{< note >}}
The underlying `StatusFlow` is subject to change — its output fields may change in later versions — and should not be relied on as a stable, versioned API.
{{< /note >}}

```kotlin
/**
 * Retrieve the current status and operation history of the iterative archive database.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property maxHistoryItems Maximum number of history items to return (default 10)
 */
class Status(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val maxHistoryItems: Int = 10
) {
    /**
     * Retrieve the current status and operation history of the iterative archive database.
     *
     * @return Iterative archive status results
     */
    fun execute(): StatusResult
}
```

### List items

Returns the list of archivable items.

```kotlin
/**
 * Invoke the list items command to retrieve details on the archivable items.
 * First it refreshes the archiving data structures by processing all pending transactions.
 *
 * This command can only be called when the node is online,
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property listItems if true return list of item IDs
 * @property bypassProcessAllPending if true, bypass refreshing the archiving data structures. Default is false.
 * @property timeLimit maximum duration to process the pending transactions. Default is 8 hours.
 * @property notNewerThan only collect transactions older than this timestamp (ISO-8601 format). Default is null which means now minus grace period.
 * @property batchSize number of transactions to process in a batch (default: 1000, min: 10, max: 1000000)
 * @property skipSafetyIntervalCheck whether to skip the safety interval check when collecting items. Default is false.
 */
class ListItems(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val listItems: Boolean = false,
    private val bypassProcessAllPending: Boolean = false,
    private val timeLimit: Duration = Duration.ofHours(8),
    private val notNewerThan: Instant? = null,
    private val batchSize: Int = 1_000,
    private val skipSafetyIntervalCheck: Boolean = false
) {
    /**
     * Execute the list items command by invoking the ListItemsFlow
     *
     * @return List items results
     */
    fun execute(): ListItemsResults
}
```

### Mark items

Marks all archivable items with the snapshot name.

```kotlin
/**
 * Invoke the mark items command to mark all archivable items with the snapshot name.
 * First it refreshes the archiving data structures by processing all pending transactions,
 * then it marks all archivable items with the provided snapshot name.
 *
 * This command can only be called when the node is online,
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property snapshot the job name
 * @property bypassProcessAllPending if true, bypass refreshing the archiving data structures. Default is false.
 * @property timeLimit maximum duration to process the pending transactions. Default is 8 hours.
 * @property notNewerThan only collect transactions older than this timestamp (ISO-8601 format). Default is null which means now minus grace period.
 * @property batchSize number of transactions to process in a batch (default: 1000, min: 10, max: 1000000)
 * @property skipSafetyIntervalCheck whether to skip the safety interval check when collecting items. Default is false.
 */
class MarkItems(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val snapshot: String? = null,
    private val bypassProcessAllPending: Boolean = false,
    private val timeLimit: Duration = Duration.ofHours(8),
    private val notNewerThan: Instant? = null,
    private val batchSize: Int = 1_000,
    private val skipSafetyIntervalCheck: Boolean = false
) {
     /**
      * Execute the mark items command by invoking the MarkItemsFlow
      *
      * @return Mark items results
      */
   fun execute(): MarkItemsResults
}
```

### Delete transactions

Marks specific transactions - and every transaction that depends on them - for deletion,
identified by their ids.

```kotlin
/**
 * Invoke the delete transactions command to mark specific transactions - and every transaction
 * that depends on them - for deletion from the vault, identified by their ids. The snapshot,
 * export and deletion are then performed by the unchanged create-snapshot, export-snapshot and
 * delete-vault commands.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property transactionIds ids of the transactions to delete
 * @property snapshot the job name
 * @property dryRun if true, only compute and report the dependency closure; nothing is marked
 * @property skipSafetyIntervalCheck whether to skip the safety interval check on the newest
 *   transaction of the closure. Default is false.
 */
class DeleteTransactions(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val transactionIds: List<String>,
    private val snapshot: String? = null,
    private val dryRun: Boolean = false,
    private val skipSafetyIntervalCheck: Boolean = false
) {
    /**
     * Execute the delete transactions command by invoking the DeleteTransactionsFlow
     *
     * @return Delete transactions results
     */
    fun execute(): DeleteTransactionsResults
}
```

### Create snapshot

Copies marked items from the Corda vault to the archive schema.

```kotlin
/**
 * Invoke the create snapshot flow to copy the marked items to the archive schema.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property queryableTables List of any queryable tables to copy
 */
class CreateSnapshot(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val queryableTables: List<Pair<String, String>> = emptyList()
) {
    /**
     * Execute the create snapshot command by invoking the CreateSnapshotFLow
     *
     * @return Create snapshot results
     */
    fun execute(): CreateSnapshotResults
}
```

### Export snapshot

Exports the marked items in the vault to an external archive.

```kotlin
/**
 * Invoke the export snapshot flow to export the archived items to permanent storage.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property exporterList list of exporters to execute
 * @property exporterConfig exporter configuration data
 * @property skipBinaryExport Mark step as complete even if no binary export was created
 */
class ExportSnapshot(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val exporterList: List<String>? = null,
    private val exporterConfig: Map<String, Any> = emptyMap(),
    private val skipBinaryExport: Boolean = false
) {
    /**
     * Execute the export snapshot command by invoking the ExportSnapshotFlow
     *
     * @return Export snapshot results
     */
    fun execute(): ExportSnapshotResults
}
```

### Import snapshot

Imports a snapshot from an external archive.

```kotlin
/**
 * Invoke the import snapshot flow to import transactions and attachments into the vault.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property snapshot Snapshot to import
 * @property importer Importer to execute
 * @property importerConfig Importer configuration data
 */
class ImportSnapshot(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val snapshot: String,
    private val importer: String? = null,
    private val importerConfig: Map<String, Any> = emptyMap()
) {
    /**
     * Execute the import snapshot command by invoking the ImportSnapshotFLow
     *
     * @return Import snapshot results
     */
    fun execute(): ImportSnapshotResults
}
```

> **Warning:** Import does not check or enforce that a transaction's own input and reference transactions are imported together with it. If a transaction is reimported while one or more of its dependencies are not, it ends up in a half-visible, unverifiable, and inconsistent state. It is the responsibility of operators to ensure that all related dependencies are imported back together. See [Restore, import, and the iterative tracking data]({{< relref "archiving-service-index.md#restore-import-and-the-iterative-tracking-data" >}}).

### Delete marked

Deletes the marked items from the Corda vault.

```kotlin
/**
 * Invoke the delete marked flow to delete the marked items from the vault schema.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property record If true then record SQL rather than execute it
 */
class DeleteMarked(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val record: Boolean = false
) {
    /**
     * Execute the delete marked items command by invoking the DeleteMarkedFlow
     *
     * @return Delete marked results
     */
    fun execute(): DeleteMarkedResults
}
```

### Delete snapshot

Deletes the snapshot from the archive schema.

```kotlin
/**
 * Invoke the delete snapshot flow to delete the marked items from the archive schema.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property record If true then record SQL rather than execute it
 */
class DeleteSnapshot(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val record: Boolean = false
) {
    /**
     * Execute the delete snapshot items command by invoking the DeleteSnapshotFlow
     *
     * @return Delete snapshot results
     */
    fun execute(): DeleteSnapshotResults
}
```
### Restore snapshot

Restores the snapshot to the Corda vault.

```kotlin
/**
 * Invoke the restore snapshot flow to restore failed jobs.
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property record If true then record SQL rather than execute it
 */
class RestoreSnapshot(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val record: Boolean = false
) {
    /**
     * Execute the restore snapshot flow
     *
     * @return Restore snapshot results
     */
    fun execute(): RestoreSnapshotResults
}
```

## Exporter interface
Custom exporters can be implemented by extending the `AbstractExporter` class and
implementing one or more of the `AttachmentExporter`, `TransactionExporter`, and
`QueryableExporter` interfaces depending on whether the exporter should export
transaction, attachment and/or state table data.

An exporter that holds resources until its export completes - open output streams,
thread pools or partially written output files - should also override `abortExport()`
to release them, so that a failed export does not leak them into the node JVM. The
method is invoked from a `finally` block around the export, so it also runs after a
successful export: implementations must be idempotent and must leave the output of
any export phase that completed normally untouched.

```kotlin
/**
 * Base class for all exporters. Each export should implement one or both
 * of the interfaces [TransactionExporter] or [AttachmentExporter]
 *
 * @property archiveJobName Name of the archive job
 * @property serviceConfiguration Configuration parameters
 * @property reporter Used by exporters to report the result of the export
 */
abstract class AbstractExporter(
    val archiveJobName: String,
    val serviceConfiguration: ServiceConfiguration,
    val reporter: ExporterReporter
) {
    /**
     * Allows an exporter to send messages back to the user.
     *
     * @param message Message to send
     */
    fun reportStatus(message: String) = reporter.report(this, message)

    /**
     * Release any resources still held after a failed export: thread pools, open output
     * streams and partial output files. Called from a `finally` block around the export,
     * so it also runs after a successful export. Implementations must therefore be
     * idempotent and leave the output of any export phase that completed normally
     * untouched, cleaning up only the phases that were interrupted.
     */
    open fun abortExport() {}
}

/**
 * Interface to indicate the exporter can export attachments
 */
interface AttachmentExporter {
    /**
     * Invoked before the first attachment is exported
     */
    fun initialiseAttachmentExport() { }

    /**
     * Invoked after the last attachment has been exported
     */
    fun completedAttachmentExport() { }

    /**
     * Invoked for each attachment
     */
    fun exportAttachment(attachmentId: String, attachment: ByteArray, filename: String? = null)

    /**
     * Invoked for each attachment together with the time the attachment was
     * inserted into the vault. Exporters that do not need the timestamp only
     * have to implement the three-argument variant.
     */
    fun exportAttachment(attachmentId: String, attachment: ByteArray, filename: String?, insertionDate: Instant?) =
        exportAttachment(attachmentId, attachment, filename)
}

/**
 * Interface to indicate the exporter can export transactions
 */
interface TransactionExporter {
    /**
     * Invoked before the first transaction is exported
     */
    fun initialiseTransactionExport() { }

    /**
     * Invoked after the last transaction has been exported
     */
    fun completedTransactionExport() { }

    /**
     * Invoked for each transaction
     */
    fun exportTransaction(transactionId: String, transaction: ByteArray)

    /**
     * Invoked for each transaction together with the time the transaction was
     * recorded in the vault and the participants of its output states.
     * Exporters that do not need the extra details only have to implement
     * the two-argument variant.
     */
    fun exportTransaction(
        transactionId: String,
        transaction: ByteArray,
        timestamp: Instant?,
        participants: List<String>? = null
    ) = exportTransaction(transactionId, transaction)
}

/**
 * Interface to indicate the exporter can export queryable states data
 */
interface QueryableExporter {
    /**
     * Invoked before the first row is exported
     *
     * @param table Table being exported
     */
    fun initialiseQueryableTableExport(table: QueryableTable) { }

    /**
     * Invoked after the last row has been exported
     *
     * @param table Table being exported
     */
    fun completedQueryableTableExport(table: QueryableTable) { }

    /**
     * Export the column header names and SQL types
     */
    fun exportHeader(table: QueryableTable, header: Array<Pair<String, Int>>)

    /**
     * Export a single row of the table
     */
    fun exportRow(table: QueryableTable, data: Array<Any?>)
}
```

The package containing the custom exporter must be declared in the Archive Service
CorDapp configuration file using the key `exporter.scanPackages` when the node is started.

```hocon
exporter.scanPackages: "com.org.cordapp.exporters"
```

## Importer interface
Custom importers can be implemented by extending the `AbstractImporter` class and
implementing the `retrieveTransactions()`, `retrieveAttachments()` methods.

An importer implementation would normally have to be paired with an exporter so
that they can agree on binary formats for recording transactions and attachments.

```kotlin
/**
 * Base class for all importers.
 *
 * @property archiveJobName Name of the archive job
 * @property serviceConfiguration Configuration parameters
 * @property reporter Used by importers to report the result of the import
 */
abstract class AbstractImporter(
    val archiveJobName: String,
    val serviceConfiguration: ServiceConfiguration,
    val reporter: ImporterReporter
) {
    /**
     * Allows an importer to send messages back to the user.
     *
     * @param message Message to send
     */
    fun reportStatus(message: String) = reporter.report(this, message)

    /**
     * Retrieve the transactions from the archive and pass them the recorder
     * for processing. If the transaction ID list is empty then retrieve all
     * transactions.
     *
     * @param transactionIds List of transactions to return
     * @param recorder Processes an archived transaction
     */
    abstract fun retrieveTransactions(transactionIds: List<SecureHash> = emptyList(), recorder: (SecureHash, ByteArray) -> Unit)

    /**
     * Retrieve the attachments from the archive and pass them the recorder
     * for processing. If the attachment ID list is empty then retrieve all
     * attachments.
     *
     * @param attachmentIds List of transactions to return
     * @param recorder Processes an archived attachment
     */
    abstract fun retrieveAttachments(attachmentIds: List<SecureHash> = emptyList(), recorder: (SecureHash, ByteArray) -> Unit)
}
```
