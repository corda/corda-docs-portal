---
date: '2023-12-15'
section_menu: corda-enterprise-4-12
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tuv-cli
    parent: corda-enterprise-4-12-tuv
tags:
- tuv cli
- tuv
- transaction validator utility
title: Transaction Validator Utility CLI parameters
weight: 200
---

# Transaction Validator Utility CLI parameters

The following section lists all the Transaction Validator Utility (TUV) CLI parameters. You can use them to perform various actions on transactions present in your database.

### -b, --base-directory

Absolute path to node's base directory for reading configuration directly from a node. If this option is not supplied, then the current directory is taken as the node's base directory.

{{< note >}}
If `-b` or `--base-directory` is specified, then CorDapps are also loaded from the supplied `base-directory/cordapps` directory and transaction deserialization is enabled by default.
{{< /note >}}

Example: `-b /corda/cordapp-template-java/build/nodes/PartyA`

### -c, --class-load

Full class name used for transaction processing. Class must implement `(SignedTransactionWithTimestamp) -> Unit` and should be placed under node's drivers directory: `/drivers`. The node's base-directory is taken as specified by the configuration in `-b` or `--base-directory` parameter.

If this option is not provided, then the utility proceeds with default transaction validation which includes transaction verification and deserialization.

Example: `-c net.corda.tvu.SampleApp`

### --cordapp-dir

Give absolute path to a directory containing CorDapps. You can provide this option zero or more times in the following way: `--cordapp-dir --cordappp-dir --cordapp-dir ...`. Provided path must be a directory. Specifying this parameter enables full transaction deserialization validation.

### -d, --datasource

Consists of all the properties required by [HikariCP](https://github.com/brettwooldridge/HikariCP) to establish a database connection. Check the required Hikari properties in the [Corda node configuration](({{< relref "../node-database-developer.html#2-corda-node-configuration" >}})) section.

{{< note >}}
Specifying `-d` or `--datasource` properties overrides the node configuration's datasource properties.
{{< /note >}}

{{< note >}}
The `-d` or `--datasource` pre-argument specifies that following properties define Hikari properties. The `dataSource.url` is an essential property as the utility needs JDBC URL to connect to the database. Failing to specify this property throws an `IllegalArgumentException`.
{{< /note >}}

Example: `-d dataSource.url=jdbc:h2:~/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA/persistence;IFEXISTS=TRUE -d  dataSource.user=sa -d dataSource.password= -d dataSourceClassName=org.h2.jdbcx.JdbcDataSource`

### -e, --error-dir-path

Takes a directory path and registers errors into this path. The value for this parameters must be a directory. The utility can register errors in the provided file path and create separate error-registration files for all verification and deserialization errors for every `signedTransactionId` in a `<signedTransactionId>.dat` file. These files are then zipped as an `ErrorDirPath/<currentTimestamp>.zip`. If this parameter is missing, then current directory is taken as the `ErrorDirPath` value.

{{< note >}}
`--error-dir-path` must be a directory or an exception is thrown.
{{< /note >}}

### -f, --config-file

Absolute path to node's configuration file for reading configuration directly from a node. It requires `-b` or `--base-directory` option. If this parameter is not supplied, the default is `node.conf`.

Example: `-b /corda/cordapp-template-java/build/nodes/PartyA -f /corda/cordapp-template-java/build/nodes/PartyA/some-other-node.conf`

### -i, --id-load-file

The utility can re-verify transactions supplied by the user. This parameter takes a file path to a text file containing transaction IDs or to a `.zip` file containing files with file names as transaction IDs. ID reverification does not happen if this option is absent.

{{< note >}}
`--id-load-file` must not be a directory or an exception is thrown.
{{< /note >}}

{{< note >}}
Since the utility does not support transaction ID re-verification with progress loading and registration, the `-i` or `--id-load-file` parameter cannot be specified with `-l` or `--load-tx-time`.
{{< /note >}}

### -l, --load-file-path

Takes a file path where the current progress will be stored and the last progress can be loaded from. If the given file is empty, then progress is not loaded from the file and the utility only writes the progress to it.

If this parameter is not provided, then progress is logged on-screen and the utility starts processing transactions starting with the earliest transaction in the database as per transaction time.

### --load-tx-time

The utility can resume the transaction verification from transaction time provided using this parameter. The provided transaction time is compared against transaction recorded time. The utility loads transactions which have a transaction timestamp greater than or equal to the provided time.

If this parameter is not provided, then the utility starts processing transactions from the earliest transaction in the database as per transaction time or loads progress from file if the `-f` option is specified.

{{< note >}}
`--load-tx-time` takes preference over the `-f` option in terms of progress loading.
{{< /note >}}

You can create a new time instant using any of the following:

1. Provide seconds and nanos without spaces (remember, no spaces), for example, give information as:
    * seconds=10
    * seconds10
    * seconds=10,nanos10
    * seconds10,nanos=10
    * seconds=10,nanos=10
    * seconds10,nanos10
    * seconds10nanos10
2. Provide UTC timestamp in format: 2007-12-03T10:15:30.00Z. The string must represent a valid instant in UTC and is parsed using `DateTimeFormatter.ISO_INSTANT`.

{{< note >}}
When using H2 database, if the utility is not able to find the database from the provided `dataSource.url`, then H2's default behavior is to create a database at the `dataSource.url location`. To avoid this, append `;IFEXISTS=TRUE` to your `dataSource.url`.
{{< /note >}}


## TUV CLI command examples

You can modify and use the following TUV CLI command examples in your project.

### Deserialize transactions using a CorDapp

Intent:
* Connect to the datasource given (`-d` option).
* Register and reload progress from the `register.txt` file (`-l` option).
* Use CorDapp in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs` directory to deserialize transactions (`--cordapp-dir` option).

Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=postgres -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource -l register.txt --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs`

### Load transactions for a given timestamp

Intent:
* Connect to the node database from reading `node.conf` in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Load transactions having transaction time greater than or equal to `2023-10-10T10:41:39.808179Z` (`--load-tx-time` option).

Command: `-b /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA --load-tx-time 2023-10-10T10:41:39.808179Z`

### Load transactions from a specific file

Intent:
* Connect to the node database from reading `node.conf` in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Only load transactions given in `/Users/suhas.srivastava/IdeaProjects/corda/enterprise/Ids.txt` file (`-i` option).

Command: `-b /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA  -i /Users/suhas.srivastava/IdeaProjects/corda/enterprise/Ids.txt`

### Perform user-supplied task

Intent:
* Connect to the node database from reading `node.conf` in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Do not validate transactions but perform a user-supplied task defined in the `net.corda.tvu.LogTransaction` class for each transaction.

Command: `-b /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA -c net.corda.tvu.LogTransaction`
