---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-7:
    parent: corda-enterprise-4-7-corda-nodes-archive-service
tags:
- archive
- backup schema
- archive install
- archive transactions


title: Archive Service Library
weight: 200
---

# The Archive Service library

The Archive Service Library provides programmatic access to the Archive Service. The library provides the following Archive Service APIs:

* `ListJobs`.
* `ListItems`.
* `MarkItems`.
* `CreateSnapshot`.
* `ExportSnapshot`.
* `ImportSnapshot`.
* `DeleteMarked`.
* `DeleteSnapshot`.
* `RestoreSnapshot`.

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
 * @property progressTree Callback used to report progress
 */
class ListJobs(
    private val rpcClient: RPCClientService,
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

### List items

Returns the list of archivable items.

```kotlin
/**
 * Invoke the list items command to retrieve details on the archivable items.
 * The [filterConfig] should be a map that can be parsed into a TypeSafe
 * config object containing the necessary filter configuration details.
 *
 * This command can only be called when the node is online,
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property filterList list of DAG filters to apply
 * @property filterConfig filter configuration data
 * @property listItems if true return list of item IDs
 */
class ListItems(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val filterList: List<String>? = null,
    private val filterConfig: Map<String, Any> = emptyMap(),
    private val listItems: Boolean = false
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
 * The [filterConfig] should be a map that can be parsed into a TypeSafe
 * config object containing the necessary filter configuration details.
 *
 * This command can only be called when the node is online,
 *
 * @property rpcClient RPC connection to Archive Service node
 * @property progressTree Callback used to report progress
 * @property snapshot the job name
 * @property filterList list of DAG filters to apply
 * @property filterConfig filter configuration data
 */
class MarkItems(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val snapshot: String? = null,
    private val filterList: List<String>? = null,
    private val filterConfig: Map<String, Any> = emptyMap()
) {
     /**
      * Execute the mark items command by invoking the MarkItemsFlow
      *
      * @return Mark items results
      */
   fun execute(): MarkItemsResults
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
 * @property additionalTransactionTables List of any addition transaction tables to copy
 * @property additionalAttachmentTables List of any additional attachment tables to copy
 * @property queryableTables List of any queryable tables to copy
 */
class CreateSnapshot(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val additionalTransactionTables: List<Pair<String, String>> = emptyList(),
    private val additionalAttachmentTables: List<Pair<String, String>> = emptyList(),
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
 * @property record If true then record SQL rather than execute it
 */
class ImportSnapshot(
    private val rpcClient: RPCClientService,
    private val progressTree: ProgressTree? = null,
    private val snapshot: String,
    private val importer: String? = null,
    private val importerConfig: Map<String, Any> = emptyMap(),
    private val record: Boolean = false
) {
    /**
     * Execute the import snapshot command by invoking the ImportSnapshotFLow
     *
     * @return Import snapshot results
     */
    fun execute(): ImportSnapshotResults
}
```
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

## Filter interface

Custom filters can be implemented by extending the `AbstractDAGFilter`, `AbstractTransactionFilter`, or `AbstractContractStateFilter` classes.

```kotlin
/**
 * Filter interface for checking which DAGs from [ledgerGraphService] can be archived.
 *
 * All DAG filters must implement a public constructor that
 * accepts [serviceHub] and [configuration] as parameters.
 *
 * @property serviceHub Access to Corda services and vault
 * @property configuration Configuration parameters
 */
abstract class AbstractDAGFilter(
    val serviceHub: ServiceHub,
    val configuration: ServiceConfiguration
) {

    /**
     * Invoked before the filter function is first used
     */
    open fun initialiseFilter() { }

    /**
     * Return true if the transaction sub-graph [graph] can be included for archiving
     */
    abstract fun filter(graph: DAG<SecureHash>): Boolean
}

/**
 * Abstract filter to verify whether each transaction within a transaction sub-graph
 * is suitable for archiving.
 *
 * Each implementation of this class should use values in [configuration] to control
 * the transaction filtering.
 */
abstract class AbstractTransactionFilter(
    serviceHub: ServiceHub,
    configuration: ServiceConfiguration
) : AbstractDAGFilter(serviceHub, configuration) {

    /**
     * Return true if the transaction [vertex] is suitable for archiving
     */
    abstract fun matches(vertex: TransactionVertex): Boolean
}

/**
 * Abstract class that provides a framework for filtering transactions based on their contract states.
 *
 * Implementors of this class must provide the contract states type and a filter to indicate which
 * states should be preserved.
 *
 * @property serviceHub Access to Corda services and vault
 * @property configuration Configuration parameters
 */
abstract class AbstractContractStateFilter(
    serviceHub: ServiceHub,
    configuration: ServiceConfiguration
) : AbstractTransactionFilter(serviceHub, configuration) {

    /** Type of states to filter */
    abstract val contractStateType: Class<out ContractState>

    /**
     * Return true if the transaction containing [state] is suitable for archiving
     */
    abstract fun <T : ContractState> matches(state: StateAndRef<T>): Boolean
}

```

The package containing the custom filter must be declared in the Archive Service
CorDapp configuration file using the key `filter.scanPackages` when the node is started.

```hocon
filter.scanPackages: "com.org.cordapp.filters"
```

## Exporter interface
Custom exporters can be implemented by extending the `AbstractExporter` class and
implementing one or more of the `AttachmentExporter`, `TransactionExporter`, and
`QueryableTableExporter` interfaces depending on whether the exporter should export
transaction, attachment and/or state table data.

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
    fun exportAttachment(attachmentId: String, attachment: ByteArray)
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
}

/**
 * Interface to indicate the exporter can export queryable state data
 */
interface QueryableTableExporter {
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
