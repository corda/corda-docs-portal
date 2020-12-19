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


title: Archive Service CLI
weight: 300
---

# Archive Service Command-Line Interface (CLI)

The Archive Service can be used to archive transactions and attachments from the Corda vault which can no longer be part of an ongoing or new transaction flow. These archivable transactions and attachments are only associated with transactions which have no unconsumed transaction outputs (UTXOs).

You can use the Archive Service CLI to interact with the Archive Service.

CLI help screen:

```text
$ java -jar corda-tools-archive-service-1.0.jar --help
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

  list-jobs                 display status of archiving jobs
  list-items                list transactions/attachments for archiving
  create-snapshot           marks transactions/attachments for archiving
  delete-vault              delete archived items from the vault
  export-snapshot           export snapshot to offline storage
  delete-snapshot           delete the snapshot from backup schema
  import-snapshot           import an archive to the vault
  restore-snapshot          restore items from backup schema to the vault

```

## Authentication

You must use the Archive Service CLI to execute commands from a machine that can issue Corda RPC commands to the node.

Use the command line argument `--node-configuration` to specify a file giving the necessary RPC settings to connect to the node, as shown below.

```kotlin
myLegalName="O=Node	ABC,L=London,C=GB"

p2pAddress="<IP:PORT>"

rpcSettings {
    address = "<host-name>:<port>"
}

security {
    authService {
        dataSource {
            type = INMEMORY
            users = [
                {
                    password = "<password>"
                    permissions = [
                        ALL
                    ]
                    username="<user-name>"
                }
            ]
        }
    }
}
```

If the Archive Service is executed from the same directory as the node then the settings are automatically collected from the node's `node.conf` file.

{{< note >}}
If the configuration file uses obfuscated passwords and the service is executed from different machine
then the obfuscation passphase and seed will need to be given on the command line.
{{< /note >}}

Use the command line options `--rpc-url`, `--rpc-user`, and `--rpc-password` to specify the RPC connection string, user name and password if the RPC credentials are encrypted or recorded in a database.

## Workflow

The archive process consists of a sequence of steps which are executed as commands from the command line.

The archive process starts with the `list-items` command and completes with the `delete-vault` command or the `delete-snapshot` command if the optional backup schema is used.

If the process has to be aborted, you can use the `restore-snapshot` command.

The workflow is as follows:

1. `list-items`: used to view which transactions and attachments will be archived.
2. `create-snapshot`: marks the transactions and attachments that will be archived.
3. `export-snapshot`: exports the archivable items to a long-term archive.
4. `delete-vault`: deletes the archived items from the vault.

If using a backup schema:

5. `delete-snapshot`: cleans up the backup schema if a backup schema has been configured.

To revert any steps up to `delete-vault` or `delete-snapshot`, use:

* `restore-snapshot` - restores the vault and deletes the snapshot

Commands which access or update the transaction and attachment tables on the Corda vault have an optional
`--record` parameter to record the SQL to a file rather than execute it immediately.

## List Jobs command

```text
Usage:
archive-service list-jobs
Description:
display status of archiving jobs
```

Displays the status of the current archive job.
```text
Job name:              <job-name>
Vault archived time:   <date and time>
Snapshot export time:  <date and time>
Vault purge time:      <date and time>
Snapshot purge time:   <date and time>
```
There can only be one active archive job in progress. If there are multiple jobs then
use the `restore-snapshot` command to rollback or abort the incomplete jobs.

## List Items command

```text
Usage:
archive-service list-items [--write=<path>] [--filter-config=<path>] [--filters=<list>]
Description:
list transactions/attachments for archiving
Options:
      --write=<path>          Save output to file
      --filters=<list>        Comma separated list of filters
      --filter-config=<path>  Path to filter configuration file
```
Displays the number of transactions and attachments that will be marked for archiving
using the given filters and filter configuration file.

```text
Number of archivable transactions: 27
Number of archivable attachments: 0
```

Optionally record to a file the IDs of transactions and attachments which will
be marked for archiving if the `--write` option is given.

This command does not update any archive log tables.

## Create Snapshot command

```text
Usage:
archive-service create-snapshot [--filter-config=<path>] [--filters=<list>] [--record=<path>] [<snapshot>]
Description:
marks transactions/attachments for archiving
Options:
      --filters=<list>          Comma separated list of filters
      --filter-config=<path>    Path to filter configuration file
Parameters:
      [<snapshot>]   archive job name (default today's date)
```

Marks all archivable transactions and attachments that match the filters as part
of this archive snapshot. If a backup schema has been configured then the items are
copied from the vault schema to the backup schema.

Displays the number of items and the database tables copied as part of the snapshot.

```text
Number of transactions marked: 27
Number of attachments marked: 0
Transaction Tables
  <table name>: <row count>
  <table name>: <row count>
Attachment Tables
  <table name>: <row count>
  <table name>: <row count>
```

## Export command

```text
Usage:
archive-service export-snapshot [--exporter-config=<path>] [--exporters=<list>] [--skip-binary-export]
Description:
export snapshot to long-term storage
Options:
      --exporters=<list>        Comma separated list of exporters
      --exporter-config=<path>  Path to exporter configuration file
      --skip-binary-export      Mark step as complete even if no binary export was created
```
Copy the archived items from the vault to permanent storage using the listed exporters.

Displays the results of the export.

```text
SomeExporter:
  Completed export of 5 states to CONTRACT_NODE_STATES-snapshot-name.csv
```

## Import command

```text
Usage:
archive-service import-snapshot [--importer-config=<path>] [--importer=<name>]
Description:
export snapshot to long-term storage
Options:
      --importer=<name>         Importer to use
      --importer-config=<path>  Path to importer configuration file
```
Copy the archived items from a snapshot archive back to the vault.

Displays the results of the import.

## Delete Vault command

```text
Usage:
archive-service delete-vault [--record=<path>]
Description:
delete archived items from the vault
Options:
      --record=<path>   Record SQL to file
```
Delete all archived transactions and attachments from the Corda vault.

If the `--record` option is given then the SQL is written to the file and no
database updates are executed.

If the Corda database user has not been granted rights to delete items from the vault schema then the
`--record` option must be used.

## Delete Snapshot command

```text
Usage:
archive-service delete-snapshot [--record=<path>]
Description:
delete archived items from backup schema
Options:
      --record=<path>   Record SQL to file
```

If the `--record` option is given then the SQL is written to the file and no
database updates are executed.

This command can only be used if a backup schema has been configured.

## Restore Snapshot command

Use the restore snapshot command to:

* Restore archived transactions from the archive schema to the node schema, to undo an archive job.
* Cancel out early from running an Archive job,  before completing it. In which case it restores the vault to its original state and clears the archiving job.

```text
Usage:
archive-service restore-snapshot [--record=<path>]
Description:
restore marked items to the vault
Options:
      --record=<path>   Record SQL to file
Abort all incomplete archive jobs and restore the Corda vault.
If the --record option is given then the SQL is written to the file and no database updates are executed.
```

Abort all incomplete archive jobs and restore the Corda vault.

If the `--record` option is given then the SQL is written to the file and no
database updates are executed.

## Filters

Filters can be applied to limit which transactions and attachments are available for archiving. The filters to be
applied can be given on the command line of the `list-items` or `create-snapshot` commands, or recorded in the
CorDapp configuration file.

Each filter has its own configuration requirements, which it takes either from the HOCON file given on
the command line or from the CorDapp configuration file.

Custom filters can be implemented by using the Archive Service Library. For more details see
the [Archive Service Library documentation](archive-library.md).

### Filter configuration

The following is a sample HOCON configuration file that can be used to configure the standard
`TransactionIdFilter` filter.

```text
filter: {
    // A list of filters to be applied
    filters: [
        "TransactionIdFilter"
    ]

    // Configuration for the TransactionId filter
    transactionIdFilter: {
        transactions: [
            "1234567812345678123456781234567812345678123456781234567812345678"
        ]
    }
}
```

## Tracking progress
The `-t` or `--tracker` option can be used on the command to display progress as each command executes.

```text
corda@CrimsonSolo:/opt/corda/node$ java -jar corda-tools-archive-service-1.0-SNAPSHOT.jar -t create-snapshot
  ✔ Starting
  ✔ Reading configuration
  ✔ Check workflow progress
  ✔ Loading filters
  ✔ Executing filters
  ✔ Clear previous result
  ✔ Marking transactions
  ✔ Marking attachments
  ✔ Create snapshot name
  ✔ Recording table schema
  ✔ Get expected row counts
  ✔   NODE_TRANSACTIONS
  ✔   VAULT_LINEAR_STATES
  ✔   VAULT_TRANSACTION_NOTES
  ✔   VAULT_STATES
  ✔   STATE_PARTY
  ✔   VAULT_FUNGIBLE_STATES
  ✔   VAULT_FUNGIBLE_STATES_PARTS
  ✔   VAULT_LINEAR_STATES_PARTS
  ✔   NODE_SCHEDULED_STATES
  ✔   CONTRACT_NODE_STATES
  ✔   NODE_ATTACHMENTS
  ✔   NODE_ATTACHMENTS_CONTRACTS
  ✔   NODE_ATTACHMENTS_SIGNERS
  ✔ Recording transactions
  ✔ Recording attachments
  ✔ Update job records
  ✔ Done
Number of transactions marked: 10
Number of attachments marked: 9
Transaction Tables
NODE_TRANSACTIONS: 10 rows
VAULT_LINEAR_STATES: 9 rows
VAULT_STATES: 9 rows
STATE_PARTY: 9 rows
CONTRACT_NODE_STATES: 9 rows

Attachment Tables
NODE_ATTACHMENTS: 9 rows

Queryable Tables
CONTRACT_NODE_STATES: 9 rows
```

## Exporters

Exporters are used to copy the archive snapshot from the backup schema to a permanent archive. The exporters to be applied can be given on the command line to the `export-snapshot` command, or recorded in the CorDapp configuration file.

```text
export: {
    exporters: [
        "ZippedFileExporter",
        "QueryableStateFileExporter"
    ]
}
```

By default, no exporters are applied.

Each exporter has its own configuration requirements, which it takes either from the HOCON file given on the command line or from the CorDapp configuration file.

Custom exporters can be implemented for individual archive solutions. For more details see the [Archive Service Library documentation](archive-library.md).

## Archive schema

The archiving process can be configured to create a temporary snapshot image of the archivable transactions and attachments from Corda vault on a backup schema within the same database. The snapshot can then be used to restore the vault should the database fail during the archive operation.   

The Corda vault schema and the archive schema must reside on the same database but be managed by different schema owners.

The Archive Service uses a separate JPA entity manager factory to manage the archive schema and copy data from the Corda schema to the archive schema.

## Archive Service configuration

The Archive Service can be configured through the CorDapp's configuration file in `cordapps/config` directory. The name of the configuration file must be identical to the Archive Service CorDapp file but with the suffix `conf` rather than `jar`.

The following are keys for configuring the Archive Service.

* `generator`: SQL generator, defaults to vault's database type.
* `driver`: JDBC driver, defaults to vault's database driver.
* `source.schema`: Vault schema name, defaults to vault database schema.
* `target.schema`: Backup schema name, optional, indicates that a backup schema should be created.
* `target.url`: Backup schema archive URL, required if a backup schema is used.
* `target.user`: Backup schema archive database user, required if a backup schema is used.
* `target.password`: Backup schema archive database password, required if a backup schema is used.

Passwords can be obfuscated using [Corda Configuration Obfuscator tool](../../tools-config-obfuscator.md).

A sample configuration file follows below:

```text
target: {
    url: "jdbc:postgresql:postgres"
    user: "archive"
    password: "<{HNtZpbrOGM6GhYA6foh5PCCBanUtaebCjauKL8ur9EE=:PolqmEJ7JOM+Sqj3ZNAE+Ew9bqG1wVE=}>"
    schema: "archive"
}
```

## Queryable state tables

Queryable state tables can be exported to CSV format by listing the tables by listing the tables in
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

Archive Service will automatically detect transaction and attachment tables which use the columns `TRANSACTION_ID` or `ATT_ID` within the vault schema and include them in the archive process.

Additional transaction and attachment tables which use different column names can be registered using the properties `additionalTransactionTables` and `additionalAttachmentTables` with the following format.

```text
additionalTransactionTables: [
    "ACCOUNT_STATE:TX_ID",
]
additionalAttachmentTables: [
    "ATTACHMENT_INFO:ATTACHMENT_ID"
]
```

Data from these tables will be recorded as part of the snapshot process and later deleted from the vault, but will not be exported to the permanent archive.

Tables should be excluded from the archive process can be registered using the properties `excludeTransactionTables` and `excludeAttachmentTables`.

## Schema permissions

If using a backup schema then the backup schema must have been granted select rights to the Corda vault.

For example:

```sql
grant usage on schema corda to archive;
grant select on all tables in schema corda TO archive;
```

An error message will be displayed when the `create-snapshot` command is executed if select rights have not been
granted.

If the Corda vault user does not have delete rights to the Corda vault then the `delete-vault` operation will fail. In this case the `--record` flag should be used and the resulting script executed by a DBA after the node has been shut down.
