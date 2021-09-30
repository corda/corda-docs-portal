---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-corda-nodes-archive-service
tags:
- archive
- backup schema
- archive install
- archive transactions


title: Archive Service APIs
weight: 300
---


# Archive Service APIs

The following APIs are exposed by the Archive Service:

```kotlin
    /**
     * Return the number of archived transactions including their
     * backchain from the archive log tables for a given well known party.
     *
     * @param party Party whose transaction count to return
     * @param withBackchain Include all transactions in the backchain
     */
    fun getArchivedTransactionCount(party: Party, withBackchain: Boolean = false): Int {
        return BackchainIterator(archivableJobManager, party, withBackchain).getCount()
    }

    /**
     * Returns an iterator to retrieve the list of transactions including their
     * backchain from the archive log tables for a given well known party.
     *
     * @param party Party whose transactions to return
     * @param withBackchain Include all transactions in the backchain
     */
    fun getArchivedTransactions(party: Party, withBackchain: Boolean = false): Iterable<String> {
        return BackchainIterator(archivableJobManager, party, withBackchain)
    }
```

## Flows

The following flows are exposed by the Archive Service:

```kotlin
/**
 * Invoke the list jobs flow to return details on the current archive job.
 */
@InitiatingFlow
@StartableByRPC
class ListJobsFlow: FlowLogic<List<ArchivingJob>>()

/**
 * Invoke the list items flow to return details on the archivable items.
 *
 * If [filterList] is null then use the default list of filters, if the list is empty
 * then apply no filters. The [filterConfig] should be a map that can be parsed into a TypeSafe
 * config object containing the necessary filter configuration details.
 *
 * An additional configuration for the selected filters can also be provided in the cordapp's conf file.
 *
 * @property filterList list of filter names
 * @property filterConfig configuration parameters for the filters
 * @property listArchivableItems return transaction and attachment IDs
 */
@InitiatingFlow
@StartableByRPC
class ListItemsFlow(
    private val filterList: List<String>?,
    private val filterConfig: Map<String, Any>,
    private val listArchivableItems: Boolean
) : FlowLogic<ListItemsResults>()

/**
  * Invoke the mark items flow to mark list items as archivable.
  *
  * If [filterList] is null then use the default list of filters, if the list is empty
  * then apply no filters. The [filterConfig] should be a map that can be parsed into a TypeSafe
  * config object containing the necessary filter configuration details.
  *
  * An additional configuration for the selected filters can also be provided in the cordapp's conf file.
  *
  * @property snapshot name of the archive snapshot recorded in the archive log tables
  * @property filterList list of filter names
  * @property filterConfig configuration parameters for the filters
  */
 @InitiatingFlow
 @StartableByRPC
 class MarkItemsFlow(
     private val snapshot: String?,
     private val filterList: List<String>?,
     private val filterConfig: Map<String, Any>
 ) : FlowLogic<MarkItemsResults>()

/**
 * Copy the marked items from the vault schema to the archive schema.
 *
 * @property additionalTransactionTables List of any addition transaction tables to copy
 * @property additionalAttachmentTables List of any additional attachment tables to copy
 * @property additionalQueryableTables List of any queryable tables to copy
 * @property record If true then record SQL rather than execute it
 */
@InitiatingFlow
@StartableByRPC
class CreateSnapshotFlow(
    private val additionalTransactionTables: List<Pair<String, String>>,
    private val additionalAttachmentTables: List<Pair<String, String>>,
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
