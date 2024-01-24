---
date: '2023-12-15'
section_menu: corda-enterprise-4-12
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tvu-cli
    parent: corda-enterprise-4-12-tvu
tags:
- tvu cli
- tvu
- transaction validator utility
title: Transaction Validator Utility CLI parameters
weight: 200
---

# Transaction Validator Utility CLI parameters

The following sections list the Transaction Validator Utility (TVU) CLI parameters. You can use these parameters to perform various actions on transactions present in your database.

### -b, --base-directory

The absolute path to the node's base directory for reading configuration directly from a node. If this option is not supplied, then the current directory is taken as the node's base directory.

{{< note >}}
If `-b` or `--base-directory` is specified, then CorDapps are also loaded from the supplied `base-directory/cordapps` directory and transaction deserialization is enabled by default.
{{< /note >}}

Example: `-b /corda/cordapp-template-java/build/nodes/PartyA`

### -c, --class-load

The full class name used for transaction processing. The class must implement `(SignedTransactionWithTimestamp) -> Unit` and should be placed under the node's drivers directory: `/drivers`. The node's base-directory is taken as specified by the configuration in `-b` or `--base-directory` parameter.

If this option is not provided, then the utility proceeds with default transaction validation which includes transaction verification and deserialization.

Example: `-c net.corda.tvu.SampleApp`

### --cordapp-dir

An absolute path to a directory containing CorDapps. Specifying this parameter enables full transaction deserialization validation. The `--cordapp-dir` CLI parameter always requires a value and provided path must be a directory. You can provide this option zero or more times in the following way:

`--cordapp-dir <first-absolute-path> --cordappp-dir <second-absolute-path> --cordapp-dir <third-absolute-path>`

There are three cases in absence of this option:
* If `--cordapp-dir` is not given and database connection is provided using the `-d` (or `--datasource`) CLI option, then no CorDapps are loaded and transaction deserialization is disabled.
* If `--cordapp-dir` is not given and node's configuration is provided using the `-b` (or `--base-directory`) CLI option, then CorDapps present only in the node's base directory's CorDapp directory are loaded. These loaded CorDapps enable transaction deserialization.
* If `--cordapp-dir` is not given and if `-b` and `-d` options are absent as well, then as per `-b` option's default configuration, the current directory is treated as the node's base directory. In this case, all the CorDapps contained within the current directory's CorDapps directory are loaded and transaction deserialization is enabled.

If both, node's-base-directory (see -b option configuration) and cordapps directory (--cordapp-dir) are provided then cordapps are loaded from both these sources and transaction deserialisation is enabled.

### -d, --datasource

All the properties required by [HikariCP](https://github.com/brettwooldridge/HikariCP) to establish a database connection. Check the required Hikari properties in the [Corda node configuration](({{< relref "../node-database-developer.html#2-corda-node-configuration" >}})) section.

{{< note >}}
* Specifying `-d` or `--datasource` properties overrides the node configuration's datasource properties.
* The `-d` or `--datasource` pre-argument specifies that following properties define Hikari properties. The `dataSource.url` is an essential property as the utility needs JDBC URL to connect to the database. Failing to specify this property throws an `IllegalArgumentException`.
{{< /note >}}

Example: `-d dataSource.url=jdbc:h2:~/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA/persistence;IFEXISTS=TRUE -d  dataSource.user=sa -d dataSource.password= -d dataSourceClassName=org.h2.jdbcx.JdbcDataSource`

### -e, --error-dir-path

A directory path where the utility registers errors. The value for this parameter must be a directory. The utility can register errors in the provided file path and create separate error-registration files for all verification and deserialization errors for every `signedTransactionId` in a `<signedTransactionId>.dat` file. These files are then zipped as an `ErrorDirPath/<currentTimestamp>.zip`. If this parameter is missing, then the current directory is taken as the `ErrorDirPath` value.

{{< note >}}
`--error-dir-path` must be a directory or an exception is thrown.
{{< /note >}}

### -f, --config-file

Absolute path to the node's configuration file for reading configuration directly from a node. It requires `-b` or `--base-directory` option. If this parameter is not supplied, the default is `node.conf`.

Example: `-b /corda/cordapp-template-java/build/nodes/PartyA -f /corda/cordapp-template-java/build/nodes/PartyA/some-other-node.conf`

### -h, --help

Provides the information about and the list of all the TVU CLI options.

### -i, --id-load-file

Transactions for reverification. These transactions are specified as a file path to a text file containing transaction IDs or to a `.zip` file containing files with file names as transaction IDs.
ID reverification does not happen if this option is absent.

{{< note >}}
`--id-load-file` must not be a directory or an exception is thrown.
{{< /note >}}

{{< note >}}
Since the utility does not support transaction ID re-verification with progress loading and registration, the `-i` or `--id-load-file` parameter cannot be specified with `-l` or `--load-tx-time`.
{{< /note >}}

### -l, --load-file-path

A file path where the current progress will be stored and the last progress can be loaded from. If the given file is empty, then progress is not loaded from the file and the utility only writes the progress to it.

If this parameter is not provided, then progress is logged on-screen and the utility starts processing transactions starting with the earliest transaction in the database as per transaction time.

### --load-tx-time

The transaction time from which the utility resumes transaction verification. The provided transaction time is compared against transaction recorded time. The utility loads transactions which have a transaction timestamp greater than or equal to the provided time.

If this parameter is not provided, then the utility starts processing transactions from the earliest transaction in the database as per transaction time or loads progress from file if the `-f` option is specified.

{{< note >}}
`--load-tx-time` takes preference over the `-f` option in terms of progress loading.
{{< /note >}}

You can create a new time instant using any of the following:

1. Provide seconds and nanos without spaces. For example:
    * seconds=10
    * seconds10
    * seconds=10,nanos10
    * seconds10,nanos=10
    * seconds=10,nanos=10
    * seconds10,nanos10
    * seconds10nanos10
2. Provide UTC timestamp in format: 2007-12-03T10:15:30.00Z. The string must represent a valid instant in UTC and is parsed using `DateTimeFormatter.ISO_INSTANT`.

{{< note >}}
When using a H2 database, if the utility is not able to find the database from the provided `dataSource.url`, then H2's default behavior is to create a database at the `dataSource.url location`. To avoid this, append `;IFEXISTS=TRUE` to your `dataSource.url`.
{{< /note >}}
