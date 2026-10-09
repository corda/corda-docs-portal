---
date: '2026-06-03T12:00:00Z'
description: "Documentation for the Corda Archive Service; this is used to make an archive of transactions and attachments from the Corda vault which can no longer be part of an ongoing or new transaction flow"
section_menu: tools
menu:
  tools:
    name: Archive Service
    weight: 700
    identifier: tools-archiving
tags:
- archive
- backup schema
- archive install
- archive transactions

title: Archive Service
---

# Archive Service

The Archive Service allows you to make an archive of transactions and attachments from the Corda vault which can no longer
be part of an ongoing or new transaction flow. This can reduce pressure on your node's database, and declutter your vault.

You can use Archive service commands to mark archivable items in your vault, archive them, and restore transactions from the archive when necessary.

{{< note >}}
Archive Service 2.0 introduces a new **iterative archiving model** that replaces the previous LedgerGraph-based approach. The Archive Service now builds its own internal graph of transactions and attachments using the vault database directly. LedgerGraph is no longer required.

Archive Service 2.x requires Corda Enterprise 4.12 or newer. For earlier Corda Enterprise versions, use [Archive Service 1.x]({{< relref "../archiving-service-1.x/archiving-service-index.md" >}}), which supports Corda Enterprise versions up to and including 4.12.
{{< /note >}}

The Archive Service consists of the following:

* [Archive Service CorDapp](#archive-service-cordapp) - contains the necessary flows to mark and archive transactions.
* [Archive Service Client Library]({{< relref "archive-library.md" >}}) - provides programmatic access to the archive service, and [exposes relevant APIs]({{< relref "archiving-apis.md" >}}).
* [Archive Service Command Line Interface]({{< relref "archiving-cli.md" >}}) - allows you to perform archiving tasks from the command line.

It also makes use of the [Application Entity Manager]({{< relref "app-entity-manager.md" >}}), which allows CorDapps to access off-ledger databases using JPA APIs.

The Archive Service archives distribution records associated with the archived transactions. (The tables `node_sender_distribution_records` and `node_receiver_distribution_records` are included in the archiving process.)

## What can be archived

The Archive Service uses an iterative model to track transaction dependencies and identify which transactions can be safely archived. A transaction will be marked as archivable when:

* It is fully consumed — all of its outputs have been consumed, and each consuming transaction is itself archivable.
* None of its outputs is used as a reference state by a transaction that is not itself archivable.
* All transactions in its dependency chain satisfy the same conditions — no transaction in the chain has unconsumed outputs or live references that could be needed by future transactions.

An attachment will be marked as archivable when:

* It is not a contract attachment.
* Every transaction that uses it is itself archivable.

The iterative archiving process works by:

1. Adding new (unprocessed) transactions to its internal dependency tracking structures. For each transaction, the service records its input and reference-state dependencies, a counter of its not-yet-consumed outputs, a counter of the reference states pointing at its outputs, and the attachments it uses.
2. Walking back through the dependency chains: transactions whose output and reference counters are both zero are condemned, and the corresponding counters of their source (parent) transactions are decremented. Any parent whose counters both reach zero is walked back in turn, so entire fully-consumed chains are condemned from the most recent transactions backwards.
3. Marking those transactions as available for archiving once the entire chain is confirmed to be fully consumed and unreferenced.

You can optionally restrict which transactions are eligible for archiving based on their contract class names using the `archivableContractClassStatePrefixes` configuration parameter. See [Configuration](#configuration) for details.

## When you can archive

Once the Archive Service has marked a transaction or attachment as archivable, you can safely archive it anytime without risk to any other member of your network. You do not need to inform other members of the network, and your archiving action will not affect their ledger.

### Archiving and Collaborative Recovery

The Collaborative Recovery solution, along with the associated CorDapps (LedgerSync and LedgerRecover), is deprecated, and has been removed in Corda 4.12. You are now advised to use the new recovery tools introduced in version 4.11, as described in the [Corda Enterprise Edition 4.11 release notes]({{< relref "../../platform/corda/4.11/enterprise/release-notes-enterprise.md#corda-enterprise-edition-411-release-notes-1" >}}).

## Making archive-friendly CorDapps

The more transactions within a dependency chain, the longer it may take for a related transaction to become archivable. If you wish to create CorDapps that produce regularly archivable transactions, there are some steps you can take in your design process to help this.

Some characteristics of a good 'archive-friendly' CorDapp are:

* Short transaction chains that will get consumed in their entirety.
* Consumes and redeems 'irrelevant states' – for example if you store evolvable data it should be consumed even if it is no longer directly queried or used in a transaction.
* Avoids consuming outputs of one transaction via multiple transactions. This could mean ensuring fungible assets are distributed as narrowly as possible – rather than from multiple cash supplies.
* Ends every business process by consuming its states. For the Archive Service, "removing" something from the ledger – offboarding a participant, closing an account, retiring a product – means a transaction that consumes the remaining states and produces no outputs (an exit or settle transaction). Merely ceasing to use a state, deleting off-ledger data, or revoking a party's access does not consume anything: a state that is never consumed keeps its transaction, and through it the whole chain that led to it, non-archivable for as long as the vault exists, however old it is.

## Archive Service CorDapp

The Archive Service CorDapp enables you to use the Archiving Service to identify and perform archiving tasks. Your configuration of the Archive Service CorDapp depends on your node database.

As part of the configuration process, you can choose to create a backup schema. This is a temporary snapshot image of archivable transactions that can be used to restore the vault if the archiving process fails.

### Requirements and compatibility

The Archive Service requires:

* Node minimum platform version 140.
* Corda Enterprise minimum version 4.12.
* JDK 17.
* Currently only supports PostgreSQL databases.

{{< warning >}}
Archive Service 2.0 does not support **Accounts** or **Confidential Identities** functionality in Corda.
{{< /warning >}}

## Installation

The Archive Service CorDapp JAR file should be copied to the node's `cordapps` directory.

```text
corda@CrimsonSolo:/opt/corda/node$ ls -l cordapps/
drwxr-xr-x 2 corda corda   4096 Aug 26 06:43 config
-rw-r--r-- 1 corda corda 504538 Aug 26 06:35 archive-service-2.0.jar
```

{{< note >}}
The Archive Service is distributed as two differently named JAR files. The CorDapp is `archive-service-<version>.jar` and goes into the node's `cordapps` directory, as shown above. The command-line tool is `corda-tools-archive-service-<version>.jar`; it is run with `java -jar` from any machine that can reach the node's RPC port and must not be copied into the `cordapps` directory. See [Archive Service command-line tool](#archive-service-command-line-tool).
{{< /note >}}

### Database migration

Like any CorDapp with custom schemas, the Archive Service CorDapp ships Liquibase change sets, which must be applied before the node is started with the new CorDapp version. There are two ways to do this:

* With the node's own `run-migration-scripts --app-schemas` sub-command, run while the node is stopped, if the node's database user is allowed to alter the schema. See [Node command-line options]({{< relref "../../platform/corda/4.12/enterprise/node/node-commandline.md#sub-commands" >}}).
* With the [Database Management Tool]({{< relref "../../platform/corda/4.12/enterprise/database-management-tool.md" >}}) (`execute-migration --app-schemas`, or `dry-run` to produce a script for your database administrator) when the node runs with a restricted database user, as described in [Database schema setup]({{< relref "../../platform/corda/4.12/enterprise/node/operating/node-database-admin.md" >}}).

If you use a [backup schema](#using-the-backup-schema), create it only after this migration has been applied, as the backup schema user needs grants on the tables the migration creates.

Besides the tables of the iterative archiving model, the migration adds one index to the node's own transaction table: `node_transactions_status_timestamp_tx_id_idx` on `node_transactions (status, timestamp, tx_id)`. The Archive Service reads the transaction table in batches ordered by `(timestamp, tx_id)`, continuing from the last processed transaction. Without the index, every batch is a full scan and a sort of the table, so processing a ledger takes time proportional to the square of its size (301 ms per 1,000-row batch measured on a 3 million-row PostgreSQL table). With the index, a batch is a single index range scan. The same index is the one the Corda Enterprise transaction validation utility requires for parallel reading. Expect about 110 bytes per transaction (323 MB for 3 million transactions, 2.5 seconds to build with the table cached in memory) and tens of microseconds of additional write cost per recorded transaction.

The change set builds the index with a plain `CREATE INDEX`, which blocks writes to the transaction table for the duration of the build. This costs nothing when the migration is run with the node stopped, which is the normal procedure. If the transaction table is too large to lock during the maintenance window, create the index beforehand on the running node with `CREATE INDEX CONCURRENTLY`, with exactly these columns and under any name. The change set detects an existing index on `(status, timestamp, tx_id)` or on `(timestamp, tx_id)` and records itself as applied instead of building a second one.

### Keeping the CorDapp installed between archiving runs

Archiving is typically run periodically, for example once a year. Keep the Archive Service CorDapp installed between runs. The CorDapp does no work on its own: its processing thread is idle until an archiving command arms it, so an installed but unused Archive Service costs the node nothing beyond the write cost of the transaction table index, which is part of the database schema and present whether or not the CorDapp is installed.

The Archive Service keeps all of its state in its own tables in the node database, not in the CorDapp JAR or in memory: the iterative tracking model, the position up to which the transaction table has been processed (`ITERATIVE_ARCHIVING_LAST_PROCESSED`), and the history of archive jobs. Because of this, the CorDapp can be removed from the `cordapps` directory and reinstalled later without consequences: it resumes from the last processed transaction and does not re-scan the ledger. Reinstall the same version together with its configuration file; a newer version requires its [database migration](#database-migration) like a first installation.

{{< warning >}}
Never drop or empty the Archive Service tables once transactions have been deleted from the vault. The model cannot be rebuilt from the vault alone: a transaction's output counter is set to the number of its outputs when it is first discovered and only decremented when the consuming transaction is itself processed. After a rebuild, the retained source transactions of already-archived consumers would be counted as fully unconsumed forever, as their consumers are no longer in the vault, and would never become archivable again. The job history is needed as well: `import-snapshot` identifies an archive by its job name and fails if the job record is missing.
{{< /warning >}}

## Configuration

The Archive Service CorDapp is configured using a HOCON configuration file located in the `config` sub-directory
of node's `cordapps` directory. The configuration file must have the same name and version as the CorDapp but
with the `jar` suffix changed to `conf`.

```text
corda@CrimsonSolo:/opt/corda/node$ ls -l cordapps/config
total 12
-rw-r--r-- 1 corda corda 469 Aug 26 06:43 archive-service-2.0.conf
```

The Archive Service configuration file provides the database connection details used by the service to
record a temporary snapshot of the vault data, the archiving filter, the table lists, and the exporter and
importer settings. Every key is optional. The exporter and importer keys can also be given in the file passed to
`export-snapshot --export-config` or `import-snapshot --importer-config`, where they override the CorDapp
configuration file for that run (with the exception noted for `exporter.extractParticipants`).

The following are keys for configuring the Archive Service, with their defaults.

Database:

* `generator` - SQL generator class name: `PostgresGenerator`, `H2Generator`, `OracleGenerator` or `MSSQLGenerator`. Default: derived from the product name of the node's database.
* `driver` - JDBC driver class used to connect to the backup schema. Default: derived from the generator; not used in single-schema mode.
* `source.user` - Vault database user. Default: the user of the node's database connection.
* `source.schema` - Vault schema name. Default: the schema of the node's database connection.
* `target.schema` - Backup schema name. Default: same as `source.schema`, which means no backup schema is used (single-schema mode). Setting it to a different schema enables the [backup schema](#using-the-backup-schema).
* `target.url` - JDBC URL of the backup schema database. No default; required if a backup schema is used.
* `target.user` - Backup schema database user. No default; required if a backup schema is used.
* `target.password` - Backup schema database password. No default; required if a backup schema is used.

Archiving:

* `ignoreSnapshotExportFailures` - Boolean, default `false`. Only consulted by the `FormattedTransactionExporter`: when `true`, a transaction that cannot be rendered as JSON is logged and skipped instead of failing the export.
* `archivableContractClassStatePrefixes` - Optional list of contract class name prefixes used to filter which transactions are eligible for archiving. When set, only transactions where **all** input, output, and reference states' contract classes match at least one of the given prefixes are considered archivable. Non-matching transactions are tracked in the iterative archiving model but will never be walked back or marked for deletion. If not set or empty, all transactions are archivable (default behavior). Entries must not be blank: because every contract class name starts with an empty string, a blank entry (for example, from a trailing comma) would silently make every transaction archivable, so the Archive Service rejects the configuration at node startup instead. The filter is evaluated when a transaction is walked back; after widening it, run `recalculate-filtering` to re-evaluate the transactions an earlier walkback had already stopped (see the note below). The `delete-transactions` command deliberately ignores this filter: it controls what automatic archiving may select, whereas that command deletes transactions the operator names explicitly.

Tables (each entry is `TABLE` or `TABLE:KEY_COLUMN`; the key column defaults to `TRANSACTION_ID` for transaction and queryable tables and to `ATT_ID` for attachment tables; all default to empty lists). See [Queryable state tables](#queryable-state-tables) and [Additional tables](#additional-tables):

* `additionalTransactionTables` - Transaction tables to archive in addition to the automatically detected ones.
* `excludeTransactionTables` - Automatically detected transaction tables to leave out of the archive process.
* `additionalAttachmentTables` - Attachment tables to archive in addition to the automatically detected ones.
* `excludeAttachmentTables` - Automatically detected attachment tables to leave out of the archive process.
* `queryableTables` - Queryable state tables whose rows are exported to CSV. Can also be given to `create-snapshot` and `delete-transactions` with `--filter-config`.
* `excludeQueryableTables` - Queryable state tables to leave out even if listed.

Exporters (see [Exporters](#exporters)):

* `exporter.exporters` - List of exporter class names to run on `export-snapshot`. Default: empty, no exporters. Also settable with `--exporters` on the command line.
* `exporter.scanPackages` - Additional packages to scan for custom exporter classes. Default: empty; the built-in package `com.r3.archive.exporters` is always scanned.
* `exporter.extractParticipants` - Boolean, default `true`. Record the participants of each exported transaction in the archive manifest. Read from the CorDapp configuration file when the items are marked and must be set there; see [Manifest participants](#manifest-participants).
* `exporter.zippedFileExporter.directory` - Directory the `ZippedFileExporter` writes to and the `ZippedFileImporter` reads from. Default: `.`, the node's working directory.
* `exporter.zippedFileExporter.chunkSize` - Items compressed per chunk, default `10000`; see [Zipped archive chunk size](#zipped-archive-chunk-size).
* `exporter.formattedTransactionExporter.directory` - Directory the `FormattedTransactionExporter` writes its JSON zip archives to. Default: `.`.
* `exporter.queryableStateFileExporter.directory` - Directory the `QueryableStateFileExporter` writes its CSV files to. Default: `.`.
* `exporter.queryableStateFileExporter.time.format` - Java date pattern for date and timestamp columns in those CSV files. Default: `yyyy-MM-dd'T'HH:mm:ssZ`.

Importers (see [Importers](#importers)):

* `importer.importer` - The importer class name to run on `import-snapshot`. Default: none; exactly one must be given, here or with `--importer`.
* `importer.scanPackages` - Additional packages to scan for custom importer classes. Default: empty; the built-in package `com.r3.archive.importers` is always scanned.
* `importer.batch.size` - Default `100000`. Snapshots with up to this many transactions are deserialized by the parallel importer; larger ones are imported sequentially to bound memory usage.

Passwords can be obfuscated using Corda's Config Obfuscator tool.

The following is a typical configuration file, enabling a backup schema and a contract filter:

```text
generator: PostgresGenerator
driver: "org.postgresql.Driver"

target: {
    url: "jdbc:postgresql:postgres"
    user: "archive"
    password: "<{HNtZpbrOGM6GhYA6foh5PCCBanUtaebCjauKL8ur9EE=:PolqmEJ7JOM+Sqj3ZNAE+Ew9bqG1wVE=}>"
    schema: "archive"
}

# Optional: Only archive transactions involving these contract types
archivableContractClassStatePrefixes: ["com.example.contracts", "net.corda.finance"]
```

The following file lists every key with its default value. It is equivalent to an empty configuration file,
except for the `target` block, which is shown commented out because setting any of its keys is what enables
the backup schema:

```text
# Database connection. The defaults are derived from the node's own database connection.
generator: "PostgresGenerator"              # PostgresGenerator | H2Generator | OracleGenerator | MSSQLGenerator
driver: "org.postgresql.Driver"             # only used when a backup schema is configured
source: {
    user: "corda"                           # default: the node's database user
    schema: "corda"                         # default: the node's database schema
}
# target: {
#     schema: "archive"                     # default: same as source.schema (no backup schema)
#     url: "jdbc:postgresql:postgres"       # no default, required with a backup schema
#     user: "archive"                       # no default, required with a backup schema
#     password: "archive"                   # no default, required with a backup schema
# }

# Archiving
archivableContractClassStatePrefixes: []    # empty: every transaction is archivable
ignoreSnapshotExportFailures: false

# Tables, as "TABLE" or "TABLE:KEY_COLUMN"
additionalTransactionTables: []
excludeTransactionTables: []
additionalAttachmentTables: []
excludeAttachmentTables: []
queryableTables: []
excludeQueryableTables: []

# Exporters
exporter: {
    exporters: []                           # none; ZippedFileExporter, FormattedTransactionExporter, QueryableStateFileExporter
    scanPackages: []
    extractParticipants: true
    zippedFileExporter: {
        directory: "."
        chunkSize: 10000
    }
    formattedTransactionExporter: {
        directory: "."
    }
    queryableStateFileExporter: {
        directory: "."
        time.format: "yyyy-MM-dd'T'HH:mm:ssZ"
    }
}

# Importers
importer: {
    importer: []                            # none; exactly one is required by import-snapshot, e.g. ["ZippedFileImporter"]
    scanPackages: []
    batch.size: 100000
}
```

{{< note >}}
This filter is evaluated when a transaction is walked back, not when it is first discovered. As with any Archive Service CorDapp configuration change, the node must be restarted before a change to this list is picked up at all — but once picked up, it takes effect immediately for any transaction still awaiting walkback, with no reset or reprocessing of already-tracked transactions required.

Transactions that an earlier run already walked back and stopped because of the filter in effect at that time are the exception. Stopping the walkback leaves such a transaction with its dependency counters at zero but neither pending walkback nor pending delete, and nothing re-triggers its walkback later — so a configuration change alone never reaches it. After widening the filter and restarting the node, run the [`recalculate-filtering`]({{< relref "archiving-cli.md#recalculate-filtering-command" >}}) command to re-arm these transactions, then `process-all-pending` to collect the ones the new filter admits; those it still rejects are simply stopped again. Narrowing the filter needs no such step.
{{< /note >}}

## Threshold parameters

The new algorithm uses two built-in threshold parameters. Both are fixed values that cannot be changed through configuration; the operator-facing lever for the grace period is the `notNewerThan` argument of the collecting commands.

* **MinAgeToAdd** — Add only transactions older than this threshold to the internal graphs. Anything newer is treated as potentially in-flight. This period is fixed at **60 seconds**.

* **MinAgeToCollect** — Treat transactions as archivable only when they are older than this threshold (on top of the other factors). This period is fixed at **one hour**. The purpose of this threshold is to allow for peer recovery and to handle potentially incoming transactions with reference states via back-chain resolution. This built-in threshold is a minimum limit for the new `notNewerThan` arguments. The related checks can be disabled for testing by setting `skipSafetyIntervalCheck` to `true` (CLI: `--skip-safety-interval-check`), although this is not recommended for general purposes. The flag bypasses only this MinAgeToCollect check, not MinAgeToAdd, and it acts inside the process-all-pending step: on `list-items` and `create-snapshot` it has no effect when `--bypass-process-all-pending` is also given, as the collection it would relax is then not run at all. A longer grace period — achieved by passing an older `notNewerThan` value — reduces the likelihood that transactions already archived will be used as reference states by later incoming transactions, which would break reference tracking. See [Late-arriving reference transactions](#late-arriving-reference-transactions) for what happens when a reference does arrive late.

## Late-arriving reference transactions

Corda transactions can arrive at a node out of notarisation order — most commonly through back-chain resolution, where receiving a transaction from a counterparty triggers the download of its dependency chain, including reference states. As a result, a new transaction can arrive that uses an output of an older transaction as a reference state *after* the iterative model has already judged that older transaction fully consumed and unreferenced.

The **MinAgeToCollect** threshold and the `notNewerThan` parameter make this scenario unlikely by keeping a safety interval between a transaction being recorded and it becoming collectable, but they cannot eliminate it entirely — a reference can, in principle, arrive arbitrarily late.

When the Archive Service processes a late-arriving transaction that references an already-condemned transaction, it reverts the archivability of the referenced transaction: its reference counter is incremented, and its pending walkback/delete markers are cleared, so it is no longer considered archivable. The overall effect depends on how far the referenced transaction had progressed through the archiving pipeline:

* **Collected, but not yet walked back**: the revert is fully consistent. No dependency counters had been modified yet, and the transaction simply returns to the tracked (non-archivable) state.
* **Already walked back (pending delete)**: only the referenced transaction itself is reverted. Its walkback had already decremented the counters of its parent transactions, so its own back-chain (ancestors) may remain condemned and can still be archived and deleted. In that case, the dependency chain of the late-arriving transaction is no longer complete on this node. The Archive Service remembers that the transaction has already been walked back: when the late-arriving transaction is itself archived later and the referenced transaction becomes archivable again, it is marked for deletion directly, **without being walked back a second time**. Its parents' and attachments' counters are therefore never decremented twice, so a parent transaction whose other outputs are still consumed or referenced by live transactions is never condemned as a side effect of the revert. An attachment shared between a reverted transaction and transactions that are being archived is exported with them but kept in the vault until the reverted transaction is archived too.
* **Already marked into an archive job** (`create-snapshot` has run): the revert does not remove the transaction from the snapshot that was already created — a subsequent `delete-vault` will still delete it. To pick up the revert, abort the job with `restore-snapshot` **before** running `delete-vault`, then re-run the archiving steps: the live tracking rows are intact at that point, so the reverted transaction is simply left out of the new job. Once `delete-vault` has run, the reverted transaction's tracking rows are gone along with it, and a `restore-snapshot` afterwards reinstates the copies taken when the snapshot was created — that is, from before the revert, still classified as deletable. The revert is lost and the next archiving job deletes the transaction again although it is referenced; see [Restoring a snapshot](#restoring-a-snapshot).
* **Already deleted from the vault**: there is nothing left to revert locally. When the transaction is needed again, Corda's back-chain resolution re-downloads it (and its chain) from peers, and the re-recorded transactions re-enter the iterative model as new — but only they do. Their consumers were archived earlier and are not re-downloaded, so nothing ever releases the re-recorded transactions' output counters: they are tracked as fully unconsumed and stay non-archivable for as long as the vault exists, even after the late-arriving transaction itself has been archived. The same applies to any re-downloaded ancestors. The vault likewise lists their outputs as unconsumed, as the consuming transactions are absent. Importing the archive that holds the consumers does not repair this on its own, as the reimported consumers are deliberately not walked back against their sources (see [Importing an archive](#importing-an-archive)). To remove such a transaction, import that archive and then delete it explicitly with `delete-transactions`: with the consumers present, their consumption of its outputs is provable, and the command reconciles the counters the normal pipeline cannot. This can only succeed once the late-arriving transaction referencing it has been archived, as a live referrer fails the command.

Note that only the referenced transaction itself is reverted; any of its *descendants* that were already condemned remain condemned. This is correct behavior: resolving the late-arriving transaction requires the referenced transaction and its ancestors, not its other descendants.

The same protection applies to transactions brought back by `import-snapshot` or marked by `delete-transactions`: they are recorded as already walked back when their tracking rows are created, so a late-arriving reference to them followed by a re-collection never disturbs the counters of their retained source transactions either. See [Restore, import, and the iterative tracking data](#restore-import-and-the-iterative-tracking-data).

To reduce the exposure to this edge case:

* Keep `notNewerThan` conservative and do not set `skipSafetyIntervalCheck` to `true` in production. On networks that make heavy use of reference states or long-running flows, extend the grace period by passing an older `notNewerThan` value.
* Keep the time between `create-snapshot` and `delete-vault` short, so that late arrivals have little opportunity to invalidate an in-flight job.
* Retain the exported archives, so that deleted chains can be restored with `import-snapshot` if they are ever needed again.

{{< warning >}}
The safety interval is the primary protection against late-arriving references. Setting an adequately high `notNewerThan` threshold for the network's traffic patterns is the responsibility of the system's operators.
{{< /warning >}}

{{< note >}}
The handling of late-arriving references described here reflects the current behavior; in particular, the ancestors of a reverted transaction are not restored, and this may be improved in future releases.
{{< /note >}}

## Restore, import, and the iterative tracking data

The `restore-snapshot` and `import-snapshot` commands bring previously archived data back into the vault. They interact with the iterative tracking tables in different ways. Neither command can run while the iterative archive service is processing transactions. In addition, while `import-snapshot` is running, the iterative archive service will not start processing a new batch until the import completes.

### Restoring a snapshot

`restore-snapshot` copies the rows of the aborted jobs back from the backup schema, including the iterative tracking rows of the restored transactions. The restored rows keep the state they had when the snapshot was created: the restored transactions are still classified as archivable, and the dependency counters remain consistent precisely because the restored transactions are not walked back a second time. Note that the iterative archive service keeps running between `create-snapshot` and `delete-vault` — `process-all-pending` is not blocked by a pending job — so the live tracking rows can move on from their snapshot copies in the meantime. Only the rows deleted by `delete-vault` are copied back, so a restore before `delete-vault` leaves the live rows untouched, whereas a restore after it replaces whatever had changed since the snapshot with the snapshot-time state. As a consequence:

* Because restored transactions are not walked back again, they are not re-evaluated against the current `archivableContractClassStatePrefixes` configuration either — despite the filter now being applied live at walkback time for newly-discovered transactions, a restored transaction keeps whatever classification it had before it was archived, and is simply picked up by the next `mark-items`/`create-snapshot` run using that pre-existing classification. There is currently no supported way to force re-evaluation of a restored transaction after a filter change: `recalculate-filtering` only re-arms transactions that a walkback *stopped* (not pending delete), so it does not touch restored transactions, which are already classified as deletable.
* If a late-arriving transaction referenced a restored transaction *while it was deleted from the vault*, the automatic revert described above could not run, because there was no tracking row to revert at that time. The same applies to a reference that arrived *between `create-snapshot` and `delete-vault`*: the revert did run on the live rows, but `delete-vault` removed those rows and the restore brought back the snapshot-time copies from before the revert. In both cases the restored transaction is picked up again by the next archiving run and may be deleted a second time even though it is now referenced. There is currently no supported way to rebuild the tracking state for this case through a restore (an [import](#importing-an-archive) of the exported archive does honour such a reference, as it reads the live reference counter); keep the `notNewerThan` grace period conservative enough for your network's traffic patterns (see [Late-arriving reference transactions](#late-arriving-reference-transactions)) to avoid it, and abort a job whose snapshot has been invalidated by a late reference before running `delete-vault`, while the live tracking rows still hold the revert.

### Importing an archive

`import-snapshot` records the archived transactions and attachments through the regular Corda APIs. For each recorded transaction, it also repopulates the iterative tracking tables directly, in the same terminal state the transaction was in immediately before it was deleted: not pending walkback, pending delete, and with its own consumption counters treated as zero.

Every transaction that can appear in an exported snapshot was, by construction, already fully walked back before it was archived and deleted — both its own consumption counters and its contribution to its source (parent) transactions' counters had already reached their final values. Reproducing that terminal state directly, instead of letting the transaction be picked up again as an ordinary new transaction, means it is never walked back a second time.

This matters because an archived snapshot is not necessarily a self-contained graph. An archived transaction may have consumed an output of a transaction that was **not** archived with it — a source transaction that stayed in the vault because:

* some of its other outputs were still unconsumed,
* it was pinned by a live reference state, or
* it was excluded from archiving by the `archivableContractClassStatePrefixes` filter.

Because the reimported transaction is never walked back again, such a retained source transaction's counters are left untouched by the import — its consumption was already accounted for once, when the transaction was originally walked back, and importing does not repeat it. This avoids the retained source transaction being incorrectly treated as fully consumed and archived while it still holds a live state. This holds even if a [late-arriving reference](#late-arriving-reference-transactions) to the reimported transaction later reverts its pending-delete classification: once it becomes archivable again, it is re-classified directly, still without being walked back.

The same rule has a consequence for a source transaction that was archived and later re-downloaded by back-chain resolution (see the *already deleted from the vault* case under [Late-arriving reference transactions](#late-arriving-reference-transactions)). Such a transaction re-entered the model as new, with a fresh, undecremented output counter, and reimporting its consumers does not decrement it either — the import cannot tell a source whose counter already accounts for the consumption from one whose counter was recreated from scratch, and decrementing the former would double-count. The re-downloaded transaction therefore remains non-archivable after the import; remove it with `delete-transactions` once its consumers have been imported and any live referrer has been archived.

A reference that arrived *while the transaction was deleted* is honoured as well. The automatic revert could not run at that time, as there was no tracking row to revert, but the reference counter was still recorded. The import reads it: a reimported transaction with a live reference count is repopulated as retained rather than pending delete, so the next archiving job leaves it in the vault until its referrers are archived — which then re-classifies it as deletable, again without walking it back. This is the one respect in which an import differs from a [restore](#restoring-a-snapshot), which copies the tracking rows back as they were and cannot take such a reference into account.

**Importing is a temporary restore — the next archiving run re-archives the imported data.** Repopulating the imported transactions directly in the pending-delete state means the next `mark-items`/`create-snapshot` run adopts all of them into its job, exactly as if they had just been condemned: the following `export-snapshot` writes them into the new archive again — duplicating data that already exists in the original archives, potentially the entire imported snapshot — and `delete-vault` then removes them from the vault again. This is the intended lifecycle: `import-snapshot` brings archived data back so it can be queried, audited, or serve back-chain resolution for a period, and the normal archiving cycle is the cleanup path that returns the vault to its archived state. Plan for two consequences:

* The imported data remains in the vault only until the next archiving job completes. If you need it available for a period, do not start a new archiving job until you are done with it. Bypassing the iterative refresh (`--bypass-process-all-pending`) does not change this — the imported transactions are already classified as pending delete, so any new job picks them up.
* The export of that next job duplicates data your existing archives already hold. Either keep or delete the duplicate archive according to your retention policy — the original archives remain valid — or avoid writing it altogether: if `list-items` confirms that the job contains only reimported transactions, complete the export step by running `export-snapshot --skip-binary-export` without specifying any exporters (and with none configured on the node), then proceed to `delete-vault`. Never skip the binary export if the job has also adopted transactions that were never archived before — in that case let the export run and accept the duplicated data, as that export is the only archive of the new transactions.

Conversely, `import-snapshot` does not check or enforce that a transaction's own input and reference transactions are imported together with it. If a transaction is reimported while one or more of its input or reference transactions are not, the reimported transaction ends up in a half-visible, unverifiable, and inconsistent state — its backchain cannot be resolved or verified, since the dependency it points to is not present in the vault. It is the responsibility of operators to ensure that all of a transaction's related dependencies are imported back along with it.

**A dependency is not necessarily held in the same archive.** A transaction is only condemned once all of the transactions consuming or referencing it have been condemned, so in the normal flow a source (parent) transaction is archived either in the same snapshot as its consumers or in a *later* one. For example, if `A`'s second output is consumed only after `B` has already been archived, `B` is archived first and `A` follows in a subsequent job — so restoring `B` completely requires the later archive that holds `A`. The [late-arriving reference](#late-arriving-reference-transactions) revert can also produce the opposite order, leaving an ancestor condemned and archived while its descendant is not. Reconstructing a chain may therefore require importing more than one snapshot, and the archive holding a missing dependency is not always the one you would expect. Retain the exported archives as a set rather than individually.

**What an incomplete backchain does and does not affect.** Every transaction in an archive is fully consumed — that is a precondition for archiving it — so its output states cannot be used as inputs to new transactions whether or not its backchain is complete, and Corda does not re-verify transactions that are already recorded. The practical impact of a missing dependency is therefore on the operations that walk the chain: back-chain resolution requests from peers cannot be satisfied, and the chain cannot be re-verified or audited locally. Data already at rest in the vault continues to be readable.

## Performance tuning

The iterative archiving process is designed to work with large vaults. Its throughput is mainly influenced by the batch size and the parallelism of the node's JVM, and on the export side by the manifest participants feature and the chunk size of the zipped archives. Reading new transactions from the vault relies on the [transaction table index](#transaction-table-index) that the CorDapp's schema migration creates.

### Batch size

The iterative archiving operations process transactions in batches. Each batch is fetched from the database, processed, and its results are written back as one unit of work.

The batch size can be set:

* On the flows `ProcessAllPendingFlow`, `ListItemsFlow`, and `MarkItemsFlow` using the `batchSize` parameter. `ProcessAllPendingFlow` applies this internally to the same processing/collection steps as the internal `AddTransactionsFlow` and `CollectArchivableFlow` building blocks.
* On the CLI commands `process-all-pending`, `list-items`, and `create-snapshot` using the `--batch-size` option.

The default batch size is **1,000**; the accepted range is **10** to **1,000,000**.

When choosing a batch size, consider the following trade-offs:

* Larger batches reduce the per-batch overhead (queries, database transaction commits, progress bookkeeping) and generally increase throughput, at the cost of higher memory usage on the node, as each batch is held in memory while it is processed.
* A stop request — whether issued via the internal `StopFlow` building block or by `ProcessAllPendingFlow` reaching its time limit — takes effect on a batch boundary — the batch currently being processed always runs to completion. Very large batch sizes therefore make stopping the archiving process less responsive.
* The default of 1,000 is a good starting point for most deployments. If you change it, benchmark against a representative copy of your data before using the new value in production.

In addition, the `importer.batch.size` configuration parameter (default: 100,000) controls the import of snapshots: snapshots containing up to this many transactions are deserialized using the parallel importer, while larger snapshots fall back to a sequential import to bound memory usage.

### Parallelism

Within each batch, the Archive Service processes transactions in parallel using Java parallel streams. This applies to adding new transactions to the internal dependency structures, walking back the dependency chains, and serializing and compressing transactions during export.

Parallel streams run on the common `ForkJoinPool` of the node's JVM. By default, its parallelism is the number of available processors minus one. You can override this by setting the following system property on the Corda node's JVM (for example, in the `custom.jvmArgs` section of `node.conf`, or directly on the `java` command line used to start the node):

```text
-Djava.util.concurrent.ForkJoinPool.common.parallelism=8
```

Because the archiving work runs inside the node's JVM, it shares CPU with regular node operation. Lowering the parallelism leaves more headroom for other node activity while archiving is running; raising it (on machines with many cores) can speed up archiving during dedicated maintenance windows. Note that the common `ForkJoinPool` is shared by the whole JVM, so this setting also affects any other code in the node that uses parallel streams.

### Transaction table index

Processing new transactions pages the node's transaction table by `(timestamp, tx_id)`, continuing from the last processed transaction, and the `statistics` command counts the unprocessed transactions with the same query. Both are served by the `node_transactions_status_timestamp_tx_id_idx` index that the CorDapp's schema migration creates, described under [Database migration](#database-migration). With it, each batch is a single index range scan and the time to process the pending transactions grows linearly with their number. Without it, every batch is a full scan and a sort of the whole transaction table, and the time grows with the square of the table size. If `process-all-pending` is unexpectedly slow on a large vault, check that the index, or an equivalent one on `(status, timestamp, tx_id)` or `(timestamp, tx_id)`, is present on the transaction table.

### Manifest participants

Recording the participants of each exported transaction in the [archive manifest]({{< relref "archiving-cli.md#archive-manifest" >}}) adds cost to two steps. Marking the items looks up the participants of the consumed states in the vault: on a ledger whose transactions consume many states, marking 120,000 transactions consuming 6,000,000 states measured 28 seconds on the lookup. Consumed states the vault holds no participants for, because the node knows them only through the back chain, are resolved by loading the transactions which created them, each once; that cost grows with the number of such states, not with the size of the job. The export deserializes each exported transaction once, to read the participants of the states it creates; without the feature, transactions are copied to the archive as binary blobs and are never deserialized.

Set `exporter.extractParticipants` to false in the CorDapp configuration file to turn the feature off if throughput matters more than the participants.

{{< note >}}
Set `exporter.extractParticipants` in the CorDapp configuration file, not in the exporter configuration file. The participants of the consumed states are looked up when the items are marked, and marking reads the property from the CorDapp configuration file only. Setting the property only in the exporter configuration passed to `export-snapshot` does not record them, so the manifest lists no consumed participants; the export logs a warning when it detects this.
{{< /note >}}

### Zipped archive chunk size

The `ZippedFileExporter` compresses items in chunks and writes each chunk to the archive as soon as it is complete. The items of a chunk are held in memory until it is written, so `exporter.zippedFileExporter.chunkSize` (default 10000) bounds the memory used by the exporter to roughly the chunk size multiplied by the average size of a transaction. Lower it if the node is short of heap when exporting, and raise it only if compression throughput turns out to be the limit. See [Zipped archive chunk size]({{< relref "archiving-cli.md#zipped-archive-chunk-size" >}}) for the configuration format.

### Performance tracking

The Archive Service collects performance statistics (wall-clock time, JVM CPU time, transaction counts, and throughput) for each archiving step. You can retrieve and reset these statistics using the `PerformanceStatsFlow` and `ResetPerformanceStatsFlow` flows. See [Performance tracking flows]({{< relref "archiving-apis.md#performance-tracking-flows" >}}) for details.

{{< note >}}
The performance tracking flows are provided as a troubleshooting and tuning aid. They are subject to change and are not a final part of the Archive Service API.
{{< /note >}}

## Using the backup schema

You can configure the archiving process to create a temporary snapshot image of the archivable transactions
and attachments from your Corda vault on a backup schema within the same database. This snapshot can then be used
to restore the vault should the database fail during the archiving operation.

For the backup schema to work, the Corda vault schema and the archive schema must reside on the same database but be
managed by different schema owners.

The Archive Service uses a separate JPA entity manager factory to manage the
archive schema and copy data from the Corda schema to the archive schema.

To create a copy of the vault on the backup schema the backup schema owner must have
`SELECT` rights to the vault schema.

To restore the vault from a copy on the backup schema the backup schema owner must
either have `INSERT` rights to the vault schema or the `restore-snapshot` command must be executed with the
`--record` option.

The `--record` option allows the user to capture the SQL to a file so that it can be
executed by a database administrator who has the sufficient rights.

The following sections contain sample SQL statements needed for creating a backup schema user.
In these examples the backup schema is called `archive` and the vault schema is `corda`.

### Postgres

The following DDL statements can be used to create a backup schema user `archive`:

```
create user archive password 'archive';
create schema archive AUTHORIZATION archive;
grant usage on schema corda to archive;
grant select on all tables in schema corda to archive;
grant insert on all tables in schema corda to archive;
```

{{< note >}}
You must execute the commands to create the backup schema after the main schema has been set up, including the Archive Service CorDapp's own tables, by the node's `run-migration-scripts` sub-command or the Database Management Tool, as described under [Database migration](#database-migration). The grants above only cover tables that exist when they are run.
{{< /note >}}

### Oracle

You can use the following DDL statements to create a backup schema user `archive`:

```
create user archive identified by archive2 DEFAULT TABLESPACE users QUOTA unlimited ON users;
grant CONNECT, RESOURCE to archive;
```

Oracle does not have a single grant option to provide rights to all the tables in a schema.
This means that rights have to be current on a per table basis.

```
grant select, insert on corda.NODE_TRANSACTIONS to archive;
```

{{< note >}}
This applies to Oracle databases only; other database types don't require table-by-table permissions updates.
{{< /note >}}

The following tables should be archived:
* `ARCHIVABLE_TX`
* `ARCHIVABLE_ATT`
* `NODE_ATTACHMENTS`
* `NODE_TRANSACTIONS`

There are also other archivable tables that contain data linked to `NODE_ATTACHMENTS` and `NODE_TRANSACTIONS`. An archivable table contains one of the following:
* A column named `transaction_id` (meaning it is linked to `NODE_TRANSACTIONS`).
* A column named `att_id` (meaning it is linked to `NODE_ATTACHMENTS`).

Corda provides multiple tables of this type and they vary between different Corda versions. You can also add your own tables. You must grant access to any tables that you want to include in the archiving process.

### MSSQL
The following DDL statements can be used to create a backup schema user `archive`:

```
create login archive with password = 'Archive123';
create schema archive;
create user archive for login archive with default_schema = archive;
grant SELECT, INSERT, UPDATE, DELETE, VIEW DEFINITION, ALTER, REFERENCES on schema::archive TO archive;
grant CREATE TABLE to archive;
grant CREATE VIEW to archive;
grant SELECT on schema ::corda to archive;
grant INSERT on schema ::corda to archive;
```

## Restarting the node

It is sometimes necessary to restart the node when carrying out an archiving job.

You need to restart the node in the following circumstances:

* Before running import-snapshot, having run 'delete-snapshot' (archive schema has been deleted, and now the vault is to be restored from file archive).
* After 'delete-vault' has been run using the '--record' option.
* After 'restore-snapshot' has been run using the '--record' option.

## Reclaiming vault storage on PostgreSQL

On PostgreSQL, Corda keeps the serialised bytes of each transaction (`node_transactions.transaction_value`) and the content of each attachment (`node_attachments.content`) as PostgreSQL *large objects*: the table row holds only an `oid` that refers to the data, which lives in the `pg_largeobject` system table. The large objects are the bulk of what is archived — in the Archive Service performance tests, 1 million transactions occupied about 2 GB in `node_transactions` and 5 to 7 GB in `pg_largeobject`.

PostgreSQL does not delete a large object when the row referring to it is deleted. `delete-vault` removes the archived transaction and attachment rows, but their large objects stay behind as orphans, and the vault database does not get smaller. The same applies when the SQL recorded with `--record` is executed by a database administrator, and to jobs created with `delete-transactions`.

To release that storage, run the `vacuumlo` utility that ships with PostgreSQL (in the `postgresql-contrib` package on most distributions) against the vault database, as a database superuser:

```text
vacuumlo -n -v -h <host> -U <superuser> <vault database>
vacuumlo -v -h <host> -U <superuser> <vault database>
```

The first command is a dry run (`-n`) that reports how many large objects would be removed; the second removes them. `vacuumlo` removes every large object that no `oid` column in the database refers to, so it is safe to run while other archiving jobs are in progress:

* With a backup schema, the snapshot copies carry the same `oid` values, so a job's large objects remain referenced until `delete-snapshot` drops the snapshot. Run `vacuumlo` after `delete-snapshot`; running it earlier does no harm, but releases nothing for that job.
* In single-schema mode, run it after `delete-vault`.

Like any deletion, removing large objects leaves dead rows in `pg_largeobject`, which autovacuum makes available for reuse by new transactions. If the space must be returned to the operating system, follow up with `VACUUM FULL pg_largeobject`, which takes an exclusive lock on the table and should be run while the node is stopped. When very many large objects are to be removed, `vacuumlo -l <number>` limits the number removed per database transaction.

{{< note >}}
`vacuumlo` and `VACUUM FULL` are PostgreSQL maintenance operations outside the Archive Service; they are not run by any of its commands. Include them in the runbook of every archiving job, or storage use on the vault database will only ever grow.
{{< /note >}}

## Archive Service command-line tool

The command-line tool is a 'fat-jar' that can be executed directly using the `java -jar` option.

```text
$ java -jar corda-tools-archive-service-2.0.jar --help
archive-service [--config-obfuscation-passphrase[=<cliPassphrase>]]
                [--config-obfuscation-seed[=<cliSeed>]]
				[--rpc-password[=<rpcPassword>]]
				[--rpc-url[=<rpcUrl>]]
                [--rpc-user=<rpcUser>]
                [--tracker]
                [-b=<baseDirectory>]
                [-f=<configurationFile>] [COMMAND]

Description:

Command line tool for performing archive operations on the Corda vault.

Options:

  -b, --base-directory=<baseDirectory>
                             Path to the base directory, default current directory
  -f, --config-file=<configurationFile>
                             Path to the configuration file, default node.conf
  -t, --tracker              Display progress tracking
      --config-obfuscation-passphrase[=<cliPassphrase>]
                             The passphrase used in the key derivation function when generating an AES key
      --config-obfuscation-seed[=<cliSeed>]
                             The seed used in the key derivation function to create a salt
      --rpc-user=<rpcUser>   Set RPC user
      --rpc-password[=<rpcPassword>]
                             Set RPC user password
      --rpc-url[=<rpcUrl>]   Set RPC connection URL
  -h, --help                 Show this help message and exit.
  -V, --version              Print version information and exit.

Commands:

  list-jobs                          display status of archiving jobs
  process-all-pending                refreshes the archiving database with processing the pending transactions and collecting archivable items
  recalculate-filtering              re-apply a changed contract class filter to transactions it previously stopped
  statistics                         display iterative archiving statistics
  status                             display current archiving database maintenance operation status and history
  list-items                         list transactions/attachments for archiving
  create-snapshot                    marks transactions/attachments for archiving
  delete-transactions                marks specific transactions and their dependents for deletion
  delete-vault                       delete archived items from the vault
  export-snapshot                    export snapshot to offline storage
  delete-snapshot                    delete the snapshot from backup schema
  import-snapshot                    import an archive to the vault
  restore-snapshot                   restore items from backup schema to the vault

```

{{< note >}}
A detailed explanation on each sub-command can be found in the [Archive Service CLI documentation]({{< relref "archiving-cli.md" >}}).
{{< /note >}}

## Exporters

Exporters are used to copy the archive snapshot from the vault to a permanent archive.
The exporters to be applied can be given on the command line to the `export-snapshot` command
or alternatively recorded in the CorDapp configuration file.

```
exporter: {
    exporters: [
        "ZippedFileExporter",
        "QueryableStateFileExporter"
    ]
}
```

By default no exporters are applied.

Each exporter has its own configuration requirements, which it takes either from the HOCON file given on the
command line or from the CorDapp configuration file.

The `ZippedFileExporter` also writes a manifest file `manifest-<snapshot>.csv` next to the zip files, listing
each exported transaction and attachment with its vault timestamp, size, and the participants of the states the
transaction creates and consumes. The manifest allows the contents of an archive to be audited — for example,
finding which archive holds a given transaction ID — without opening the zip files.
See the [Archive Service CLI documentation]({{< relref "archiving-cli.md#archive-manifest" >}}) for details.

Custom exporters can be implemented for individual archive solutions.
For more details see the [Archive Service Library documentation]({{< relref "archive-library.md" >}}).

## Importers

Importers read an archive written by an exporter back into the vault, using the `import-snapshot` command.
The Archive Service ships one importer, `ZippedFileImporter`, which reads the archive written by the
`ZippedFileExporter`. This is why `delete-vault` refuses to run unless a `ZippedFileExporter` export has
been made (or `--skip-binary-export` is given): it is the only archive format that can be imported.

The snapshot named on the command line is the **archive job name** that was given to `create-snapshot`
(or defaulted to the date), as displayed by `list-jobs`; it is not a file name. The job must be complete, and its
record must still exist in the node database, which is one reason not to drop the Archive Service tables between runs (see
[Keeping the CorDapp installed between archiving runs](#keeping-the-cordapp-installed-between-archiving-runs)).

```text
java -jar corda-tools-archive-service-2.0.jar import-snapshot --importer=ZippedFileImporter T1
```

The importer can alternatively be set with the property `importer.importer` in the CorDapp configuration
file or in the file given with `--importer-config`. Exactly one importer must be named, or the command fails.

A job counts as complete once its snapshot has been purged. In single-schema mode `delete-vault` does this, so
the job can be imported right after it. With a backup schema, only `delete-snapshot` does, so between
`delete-vault` and `delete-snapshot` the job is still pending and `import-snapshot` fails with a pending-job
error, for this job or any other incomplete one. That window is what `restore-snapshot` is for: it copies the
deleted rows back from the backup schema and clears the job, whereas `import-snapshot` is the way back once the
backup schema copy is gone.

The files that make up a snapshot for `ZippedFileImporter` are the two zip files the `ZippedFileExporter` wrote
for the job, `transaction-<job>.zip` and `attachment-<job>.zip`. It reads them from the directory configured
by `exporter.zippedFileExporter.directory`, the same property the exporter uses, taken from the CorDapp
configuration file or the `--importer-config` file. Both files must be present in that directory. The manifest
`manifest-<job>.csv` is an audit aid and is not read by the import, and neither are the files written by other
exporters, such as the CSV files of the `QueryableStateFileExporter`: the vault's queryable state tables are
repopulated by Corda as the imported transactions are recorded.

After a successful import, the job is removed from the job history, and the imported transactions are tracked as
pending delete again, so the next archiving job re-exports them under its own name. See
[Importing an archive](#importing-an-archive) for the consequences.

## Queryable state tables

Queryable state tables can be exported to CSV format by listing the tables in
the configuration file under the property `queryableTables`.

```text
queryableTables: [
    "LOAN_STATES"
]
```

The property can be added to the Archive Service CorDapp configuration file, or supplied to the
`create-snapshot` and `delete-transactions` commands in a separate configuration file given with
their `--filter-config` option.

A suitable exporter, such as `QueryableStateFileExporter`, must also be listed on the command line to `export-snapshot`.

## Additional tables

Archive Service automatically detects transaction and attachment tables that use the columns
`TRANSACTION_ID` or `ATT_ID` within the vault schema and include them in the archive process.

Additional transaction and attachment tables which use different column names can be registered using the
properties `additionalTransactionTables` and `additionalAttachmentTables` with the following format:

```text
additionalTransactionTables: [
    "ACCOUNT_STATE:TX_ID",
]
additionalAttachmentTables: [
    "ATTACHMENT_INFO:ATTACHMENT_ID"
]
```

Data from these tables will be recorded as part of the snapshot process and later deleted from the vault,
but will not be exported to permanent archive.

Tables that should be excluded from the archive process can be registered using the
properties `excludeTransactionTables` and `excludeAttachmentTables`.
