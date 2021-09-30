---
aliases:
- /releases/4.1/node-database.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-node-database
    parent: corda-enterprise-4-1-corda-nodes-index
    weight: 1070
tags:
- node
- database
title: Database Migration Tool
---

# Database Migration Tool

By default, a node will *not* attempt to execute database migration scripts at startup (even when a new version has been deployed),
but will check the database "version" and halt if the database is not in sync with the node, to avoid data corruption.

This setup/procedure is recommended for production systems.

Running the migration at startup automatically can be configured by specifying true in the ``database.runMigration``
node configuration setting (default behaviour is false).
We recommend enabling database schema auto-creation/upgrade for development or test purposes only.
It is safe to run at startup if you have implemented the usual best practices for database management
(e.g. running a backup before installing a new version).

## Database Management Tool

The database management tool is distributed as a standalone JAR file named `tools-database-manager-${corda_version}.jar`.
It is intended to be used by Corda Enterprise node administrators.

The following sections document the available subcommands suitable for a node operator or database administrator.

### Executing a dry run of the SQL migration scripts

The `dry-run` subcommand can be used to output the database migration to the specified output file or to the console.
The output directory is the one specified by the `--base-directory` parameter.

Usage:

```shell
    database-manager dry-run [-hvV] [--doorman-jar-path=<doormanJarPath>]
                             [--logging-level=<loggingLevel>] [--mode=<mode>]
                             -b=<baseDirectory> [-f=<configFile>] [<outputFile>]
```

The `outputFile` parameter can be optionally specified determine what file to output the generated SQL to, or use
`CONSOLE` to output to the console.

Additional options:

* `--base-directory`, `-b`: (Required) The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. Defaults to `node.conf`.
* `--mode`: The operating mode. Possible values: NODE, DOORMAN. Default: NODE.
* `--doorman-jar-path=<doormanJarPath>`: The path to the doorman JAR.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.

### Executing SQL migration scripts

The `execute-migration` subcommand runs migration scripts on the node's database.

Usage:

```shell
    database-manager execute-migration [-hvV] [--doorman-jar-path=<doormanJarPath>]
                                       [--logging-level=<loggingLevel>]
                                       [--mode=<mode>] -b=<baseDirectory>
                                       [-f=<configFile>]
```

* `--base-directory`, `-b`: (Required) The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. Defaults to `node.conf`.
* `--mode`: The operating mode. Possible values: NODE, DOORMAN. Default: NODE.
* `--doorman-jar-path=<doormanJarPath>`: The path to the doorman JAR.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.

### Releasing database locks

The `release-lock` subcommand forces the release of database locks. Sometimes, when a node or the database management
tool crashes while running migrations, Liquibase will not release the lock. This can happen during some long
database operations, or when an admin kills the process (this cannot happen during normal operation of a node,
only [during the migration process](http://www.liquibase.org/documentation/databasechangeloglock_table.html).

Usage:

```shell
    database-manager release-lock [-hvV] [--doorman-jar-path=<doormanJarPath>]
                                  [--logging-level=<loggingLevel>] [--mode=<mode>]
                                  -b=<baseDirectory> [-f=<configFile>]
```
Additional options:

* `--base-directory`, `-b`: (Required) The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. Defaults to `node.conf`.
* `--mode`: The operating mode. Possible values: NODE, DOORMAN. Default: NODE.
* `--doorman-jar-path=<doormanJarPath>`: The path to the doorman JAR.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.

### Database Manager shell extensions

The `install-shell-extensions` subcommand can be used to install the `database-manager` alias and auto-completion for
bash and zsh. See [shell extensions](cli-application-shell-extensions.md) for more info.


{{< note >}}
When running the database management tool, it is preferable to use absolute paths when specifying the "base-directory".
{{</ note >}}

{{< warning >}}
It is good practice for node operators to back up the database before upgrading to a new version.
{{</ warning >}}

### Troubleshooting

Symptom: Problems acquiring the lock, with output like this:

```
Waiting for changelog lock....
Waiting for changelog lock....
Waiting for changelog lock....
Waiting for changelog lock....
Waiting for changelog lock....
Waiting for changelog lock....
Waiting for changelog lock....
Liquibase Update Failed: Could not acquire change log lock.  Currently locked by SomeComputer (192.168.15.X) since 2013-03-20 13:39
SEVERE 2013-03-20 16:59:liquibase: Could not acquire change log lock.  Currently locked by SomeComputer (192.168.15.X) since 2013-03-20 13:39
liquibase.exception.LockException: Could not acquire change log lock.  Currently locked by SomeComputer (192.168.15.X) since 2013-03-20 13:39
        at liquibase.lockservice.LockService.waitForLock(LockService.java:81)
        at liquibase.Liquibase.tag(Liquibase.java:507)
        at liquibase.integration.commandline.Main.doMigration(Main.java:643)
        at liquibase.integration.commandline.Main.main(Main.java:116)
```

Advice: See [this StackOverflow question](https://stackoverflow.com/questions/15528795/liquibase-lock-reasons).
You can run `java -jar tools-database-manager-4.1.jar --base-directory /path/to/node --release-lock` to force Liquibase to give up the lock.


## Node database tables

By default, the node database has the following tables:


{{< table >}}

|Table name|Columns|
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|DATABASECHANGELOG|ID, AUTHOR, FILENAME, DATEEXECUTED, ORDEREXECUTED, EXECTYPE, MD5SUM, DESCRIPTION, COMMENTS, TAG, LIQUIBASE, CONTEXTS, LABELS, DEPLOYMENT_ID|
|DATABASECHANGELOGLOCK|ID, LOCKED, LOCKGRANTED, LOCKEDBY|
|NODE_ATTACHMENTS|ATT_ID, CONTENT, FILENAME, INSERTION_DATE, UPLOADER|
|NODE_ATTACHMENTS_CONTRACTS|ATT_ID, CONTRACT_CLASS_NAME|
|NODE_ATTACHMENTS_SIGNERS|ATT_ID, SIGNER|
|NODE_CHECKPOINTS|CHECKPOINT_ID, CHECKPOINT_VALUE|
|NODE_CONTRACT_UPGRADES|STATE_REF, CONTRACT_CLASS_NAME|
|NODE_IDENTITIES|PK_HASH, IDENTITY_VALUE|
|NODE_INFOS|NODE_INFO_ID, NODE_INFO_HASH, PLATFORM_VERSION, SERIAL|
|NODE_INFO_HOSTS|HOST_NAME, PORT, NODE_INFO_ID, HOSTS_ID|
|NODE_INFO_PARTY_CERT|PARTY_NAME, ISMAIN, OWNING_KEY_HASH, PARTY_CERT_BINARY|
|NODE_LINK_NODEINFO_PARTY|NODE_INFO_ID, PARTY_NAME|
|NODE_MESSAGE_IDS|MESSAGE_ID, INSERTION_TIME, SENDER, SEQUENCE_NUMBER|
|NODE_NAMED_IDENTITIES|NAME, PK_HASH|
|NODE_NETWORK_PARAMETERS|HASH, EPOCH, PARAMETERS_BYTES, SIGNATURE_BYTES, CERT, PARENT_CERT_PATH|
|NODE_OUR_KEY_PAIRS|PUBLIC_KEY_HASH, PRIVATE_KEY, PUBLIC_KEY|
|NODE_PROPERTIES|PROPERTY_KEY, PROPERTY_VALUE|
|NODE_SCHEDULED_STATES|OUTPUT_INDEX, TRANSACTION_ID, SCHEDULED_AT|
|NODE_TRANSACTIONS|TX_ID, TRANSACTION_VALUE, STATE_MACHINE_RUN_ID|
|PK_HASH_TO_EXT_ID_MAP|ID, EXTERNAL_ID, PUBLIC_KEY_HASH|
|STATE_PARTY|OUTPUT_INDEX, TRANSACTION_ID, ID, PUBLIC_KEY_HASH, X500_NAME|
|VAULT_FUNGIBLE_STATES|OUTPUT_INDEX, TRANSACTION_ID, ISSUER_NAME, ISSUER_REF, OWNER_NAME, QUANTITY|
|VAULT_FUNGIBLE_STATES_PARTS|OUTPUT_INDEX, TRANSACTION_ID, PARTICIPANTS|
|VAULT_LINEAR_STATES|OUTPUT_INDEX, TRANSACTION_ID, EXTERNAL_ID, UUID|
|VAULT_LINEAR_STATES_PARTS|OUTPUT_INDEX, TRANSACTION_ID, PARTICIPANTS|
|VAULT_STATES|OUTPUT_INDEX, TRANSACTION_ID, CONSUMED_TIMESTAMP, CONTRACT_STATE_CLASS_NAME, LOCK_ID, LOCK_TIMESTAMP, NOTARY_NAME, RECORDED_TIMESTAMP, STATE_STATUS, RELEVANCY_STATUS, CONSTRAINT_TYPE, CONSTRAINT_DATA|
|VAULT_TRANSACTION_NOTES|SEQ_NO, NOTE, TRANSACTION_ID|
|V_PKEY_HASH_EX_ID_MAP|ID, PUBLIC_KEY_HASH, TRANSACTION_ID, OUTPUT_INDEX, EXTERNAL_ID|

{{< /table >}}

The node database for a Simple Notary has additional tables:

{{< table >}}

|Table name|Columns|
|----------|-------|
| NODE_NOTARY_COMMITTED_STATES | OUTPUT_INDEX, TRANSACTION_ID, CONSUMING_TRANSACTION_ID |
|  NODE_NOTARY_COMMITTED_TXS | TRANSACTION_ID  |
| NODE_NOTARY_REQUEST_LOG | ID, CONSUMING_TRANSACTION_ID, REQUESTING_PARTY_NAME, REQUEST_TIMESTAMP, REQUEST_SIGNATURE |

{{</ table >}}
