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

1. Adding new (unprocessed) transactions to its internal dependency tracking structures. For each transaction, the service records its input and reference-state dependencies, a counter of its not-yet-consumed outputs, a counter of transactions referencing its outputs, and the attachments it uses.
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
record a temporary snapshot of the vault data.

The following are keys for configuring the Archive Service:

* `generator` - SQL generator, defaults to vault's database type.
* `driver` - JDBC driver, defaults to vault's database driver.
* `source.user` - Vault database user, defaults to vault database user.
* `source.schema` - Vault schema name, defaults to vault database schema.
* `target.schema` - Backup schema name, optional, indicates that a backup schema should be created.
* `target.url` - Backup schema archive URL, required if a backup schema is used.
* `target.user` - Backup schema archive database user, required if a backup schema is used.
* `target.password` - Backup schema archive database password, required if a backup schema is used.
* `archivableContractClassStatePrefixes` - Optional list of contract class name prefixes used to filter which transactions are eligible for archiving. When set, only transactions where **all** input, output, and reference states' contract classes match at least one of the given prefixes are considered archivable. Non-matching transactions are tracked in the iterative archiving model but will never be walked back or marked for deletion. If not set or empty, all transactions are archivable (default behavior).

Passwords can be obfuscated using Corda's Config Obfuscator tool.

The following is a sample configuration file:

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

{{< note >}}
This filter is evaluated when a transaction is walked back, not when it is first discovered. As with any Archive Service CorDapp configuration change, the node must be restarted before a change to this list is picked up at all — but once picked up, it takes effect immediately for any transaction still awaiting walkback, with no reset or reprocessing of already-tracked transactions required.
{{< /note >}}

## Threshold parameters

The new algorithm uses two threshold parameters:

* **MinAgeToAdd** — Add only transactions older than this threshold to the internal graphs. Anything newer is treated as potentially in-flight. This period is **60 seconds**.

* **MinAgeToCollect** — Treat transactions as archivable only when they are older than this threshold (on top of the other factors). This period is **one hour**. The purpose of this threshold is to allow for peer recovery and to handle potentially incoming transactions with reference states via back-chain resolution. This configuration setting is a minimum limit for the new `notNewerThan` arguments. The related checks can be disabled for testing by setting `skipSafetyIntervalCheck` to `true`, although this is not recommended for general purposes. Increasing this value reduces the likelihood that transactions already archived will be used as reference states by later incoming transactions, which would break reference tracking. See [Late-arriving reference transactions](#late-arriving-reference-transactions) for what happens when a reference does arrive late.

## Late-arriving reference transactions

Corda transactions can arrive at a node out of notarisation order — most commonly through back-chain resolution, where receiving a transaction from a counterparty triggers the download of its dependency chain, including reference states. As a result, a new transaction can arrive that uses an output of an older transaction as a reference state *after* the iterative model has already judged that older transaction fully consumed and unreferenced.

The **MinAgeToCollect** threshold and the `notNewerThan` parameter make this scenario unlikely by keeping a safety interval between a transaction being recorded and it becoming collectable, but they cannot eliminate it entirely — a reference can, in principle, arrive arbitrarily late.

When the Archive Service processes a late-arriving transaction that references an already-condemned transaction, it reverts the archivability of the referenced transaction: its reference counter is incremented, and its pending walkback/delete markers are cleared, so it is no longer considered archivable. The overall effect depends on how far the referenced transaction had progressed through the archiving pipeline:

* **Collected, but not yet walked back**: the revert is fully consistent. No dependency counters had been modified yet, and the transaction simply returns to the tracked (non-archivable) state.
* **Already walked back (pending delete)**: only the referenced transaction itself is reverted. Its walkback had already decremented the counters of its parent transactions, so its own back-chain (ancestors) may remain condemned and can still be archived and deleted. In that case, the dependency chain of the late-arriving transaction is no longer complete on this node.
* **Already marked into an archive job** (`create-snapshot` has run): the revert does not remove the transaction from the snapshot that was already created — a subsequent `delete-vault` will still delete it. To pick up the revert, abort the job with `restore-snapshot` and re-run the archiving steps.
* **Already deleted from the vault**: there is nothing left to revert locally. When the transaction is needed again, Corda's back-chain resolution re-downloads it (and its chain) from peers, and the re-recorded transactions re-enter the iterative model as new. The exported archive (`import-snapshot`) is the ultimate backstop for restoring deleted chains.

Note that only the referenced transaction itself is reverted; any of its *descendants* that were already condemned remain condemned. This is correct behavior: resolving the late-arriving transaction requires the referenced transaction and its ancestors, not its other descendants.

To reduce the exposure to this edge case:

* Keep `notNewerThan` conservative and do not set `skipSafetyIntervalCheck` to `true` in production. Increase the grace period on networks that make heavy use of reference states or long-running flows.
* Keep the time between `create-snapshot` and `delete-vault` short, so that late arrivals have little opportunity to invalidate an in-flight job.
* Retain the exported archives, so that deleted chains can be restored with `import-snapshot` if they are ever needed again.

{{< warning >}}
The safety interval is the primary protection against late-arriving references. Setting an adequately high `notNewerThan` threshold for the network's traffic patterns is the responsibility of the system's operators.
{{< /warning >}}

{{< note >}}
The handling of late-arriving references described here reflects the current behavior and may be improved in future releases.
{{< /note >}}

## Restore, import, and the iterative tracking data

The `restore-snapshot` and `import-snapshot` commands bring previously archived data back into the vault. They interact with the iterative tracking tables in different ways. Neither command can run while the iterative archive service is processing transactions. In addition, while `import-snapshot` is running, the iterative archive service will not start processing a new batch until the import completes.

### Restoring a snapshot

`restore-snapshot` copies the rows of the aborted jobs back from the backup schema, including the iterative tracking rows of the restored transactions. The restored rows keep the state they had when the snapshot was created: the restored transactions are still classified as archivable, and the dependency counters remain consistent precisely because the restored transactions are not walked back a second time. As a consequence:

* Because restored transactions are not walked back again, they are not re-evaluated against the current `archivableContractClassStatePrefixes` configuration either — despite the filter now being applied live at walkback time for newly-discovered transactions, a restored transaction keeps whatever classification it had before it was archived, and is simply picked up by the next `mark-items`/`create-snapshot` run using that pre-existing classification. There is currently no supported way to force re-evaluation of a restored transaction after a filter change.
* If a late-arriving transaction referenced a restored transaction *while it was deleted from the vault*, the automatic revert described above could not run, because there was no tracking row to revert at that time. After the restore, such a transaction is picked up again by the next archiving run and may be deleted a second time even though it is now referenced. There is currently no supported way to rebuild the tracking state for this case; keep the safety interval conservative enough for your network's traffic patterns (see [Late-arriving reference transactions](#late-arriving-reference-transactions)) to avoid it.

### Importing an archive

`import-snapshot` records the archived transactions and attachments through the regular Corda APIs. For each recorded transaction, it also repopulates the iterative tracking tables directly, in the same terminal state the transaction was in immediately before it was deleted: not pending walkback, pending delete, and with its own consumption counters treated as zero.

Every transaction that can appear in an exported snapshot was, by construction, already fully walked back before it was archived and deleted — both its own consumption counters and its contribution to its source (parent) transactions' counters had already reached their final values. Reproducing that terminal state directly, instead of letting the transaction be picked up again as an ordinary new transaction, means it is never walked back a second time.

This matters because an archived snapshot is not necessarily a self-contained graph. An archived transaction may have consumed an output of a transaction that was **not** archived with it — a source transaction that stayed in the vault because:

* some of its other outputs were still unconsumed,
* it was pinned by a live reference state, or
* it was excluded from archiving by the `archivableContractClassStatePrefixes` filter.

Because the reimported transaction is never walked back again, such a retained source transaction's counters are left untouched by the import — its consumption was already accounted for once, when the transaction was originally walked back, and importing does not repeat it. This avoids the retained source transaction being incorrectly treated as fully consumed and archived while it still holds a live state.

Conversely, `import-snapshot` does not check or enforce that a transaction's own input and reference transactions are imported together with it. If a transaction is reimported while one or more of its input or reference transactions are not, the reimported transaction ends up in a half-visible, unverifiable, and inconsistent state — its backchain cannot be resolved or verified, since the dependency it points to is not present in the vault. It is the responsibility of operators to ensure that all of a transaction's related dependencies are imported back along with it.

**A dependency is not necessarily held in the same archive.** A transaction is only condemned once all of the transactions consuming or referencing it have been condemned, so in the normal flow a source (parent) transaction is archived either in the same snapshot as its consumers or in a *later* one. For example, if `A`'s second output is consumed only after `B` has already been archived, `B` is archived first and `A` follows in a subsequent job — so restoring `B` completely requires the later archive that holds `A`. The [late-arriving reference](#late-arriving-reference-transactions) revert can also produce the opposite order, leaving an ancestor condemned and archived while its descendant is not. Reconstructing a chain may therefore require importing more than one snapshot, and the archive holding a missing dependency is not always the one you would expect. Retain the exported archives as a set rather than individually.

**What an incomplete backchain does and does not affect.** Every transaction in an archive is fully consumed — that is a precondition for archiving it — so its output states cannot be used as inputs to new transactions whether or not its backchain is complete, and Corda does not re-verify transactions that are already recorded. The practical impact of a missing dependency is therefore on the operations that walk the chain: back-chain resolution requests from peers cannot be satisfied, and the chain cannot be re-verified or audited locally. Data already at rest in the vault continues to be readable.

## Performance tuning

The iterative archiving process is designed to work with large vaults. Its throughput is mainly influenced by two settings: the batch size and the parallelism of the node's JVM.

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

In addition, the `importer.batch.size` configuration parameter (default: 1,000) controls the import of snapshots: snapshots containing up to this many transactions are deserialized using the parallel importer, while larger snapshots fall back to a sequential import to bound memory usage.

### Parallelism

Within each batch, the Archive Service processes transactions in parallel using Java parallel streams. This applies to adding new transactions to the internal dependency structures, walking back the dependency chains, and serializing and compressing transactions during export.

Parallel streams run on the common `ForkJoinPool` of the node's JVM. By default, its parallelism is the number of available processors minus one. You can override this by setting the following system property on the Corda node's JVM (for example, in the `custom.jvmArgs` section of `node.conf`, or directly on the `java` command line used to start the node):

```text
-Djava.util.concurrent.ForkJoinPool.common.parallelism=8
```

Because the archiving work runs inside the node's JVM, it shares CPU with regular node operation. Lowering the parallelism leaves more headroom for other node activity while archiving is running; raising it (on machines with many cores) can speed up archiving during dedicated maintenance windows. Note that the common `ForkJoinPool` is shared by the whole JVM, so this setting also affects any other code in the node that uses parallel streams.

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
You must execute the commands to create backup schema after the node has set up the main schema using the `run-migration-scripts` command.
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
  statistics                         display iterative archiving statistics
  status                             display current archiving database maintenance operation status and history
  list-items                         list transactions/attachments for archiving
  create-snapshot                    marks transactions/attachments for archiving
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
each exported transaction and attachment with its vault timestamp, size, and participants. The manifest allows
the contents of an archive to be audited — for example, finding which archive holds a given transaction ID —
without opening the zip files. See the [Archive Service CLI documentation]({{< relref "archiving-cli.md#archive-manifest" >}})
for details.

Custom exporters can be implemented for individual archive solutions.
For more details see the [Archive Service Library documentation]({{< relref "archive-library.md" >}}).

## Queryable state tables

Queryable state tables can be exported to CSV format by listing the tables in
the configuration file under the property `queryableTables`.

```text
queryableTables: [
    "LOAN_STATES"
]
```

The property can be added to the Archive Service CorDapp configuration file, or passed within the
`create-snapshot` command configuration.

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
