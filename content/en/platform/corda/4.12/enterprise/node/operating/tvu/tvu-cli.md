---
Description: "List of the Transaction Validator Utility parameters."
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

{{< note >}}
The following examples assume you have a node installation available with transactions in the database and the associated CorDapps in the node's CorDapps directory.
{{< /note >}}


### `-b`, `--base-directory`

Path to the node's base directory for reading configuration directly from a node. If this option is not supplied, then the current directory is taken as the node's base directory.

If this option is specified, then CorDapps are also loaded from the supplied `base-directory/cordapps` directory and transaction deserialization is enabled by default.

Example:
```
java -jar transaction-validator.jar -b /corda/cordapp-template-java/build/nodes/PartyA
```

### `-c`, `--class-load`

The full user-defined class name used for transaction processing. The class must implement `(SignedTransactionWithTimestamp) -> Unit` and should be placed under the node's drivers directory: `/drivers`. The node's base directory is taken as specified by the configuration in `-b` or `--base-directory` parameter.

If this option is not provided, then the utility proceeds with default transaction validation which includes transaction verification and deserialization.

Example:
```
java -jar transaction-validator.jar -c net.corda.tvu.SampleApp
```

### `-e`, `--error-dir-path`

A directory path where the utility registers errors. The utility can register errors in a provided file path as well as create separate error-registration files for all verification and deserialization errors for every `signedTransactionId` in a `<signedTransactionId>.dat` file. These files are then zipped as an `ErrorDirPath/<currentTimestamp>.zip`. If this parameter is missing, then the current directory is taken as the `ErrorDirPath` value.

{{< note >}}
`-e` or `--error-dir-path` must be a directory or an exception is thrown.
{{< /note >}}

### `-f`, `--config-file`

Path to the node's configuration file for reading configuration directly from a node. Can have the `-b` or `--base-directory` option. If this parameter is not supplied, the default is `node.conf`.

Example:
```
java -jar transaction-validator.jar -b /corda/cordapp-template-java/build/nodes/PartyA -f /corda/cordapp-template-java/build/nodes/PartyA/some-other-node.conf
```

### `-h`, `--help`

Provides the information about and the list of all the TVU CLI options.

### `-i`, `--id-load-file`

File path to the location containing the IDs of the transactions to be reprocessed. The reverification does not happen if this option is absent. The file containing IDs of the transactions to be reprocessed can be either:
* A text file containing newline-separated list of transaction IDs.
* A `.zip` file that is created automatically when the TVU encounters errors. This error `.zip` file stores erroneous transactions’ raw data.

{{< note >}}
* `--id-load-file` must not be a directory or an exception is thrown.
* Since the utility does not support transaction ID reverification with progress loading and registration, the `-i` or `--id-load-file` parameter cannot be specified with `-l` or `--load-tx-time`.
{{< /note >}}

### `-l`, `--load-file-path`

A file path where the current progress will be stored and the last progress can be loaded from. If the given file is empty, then the utility starts processing transactions from the beginning.

If this parameter is not provided, then progress is logged on-screen and the utility starts processing transactions starting with the earliest transaction in the database as per transaction time.

### `--load-tx-time`

The transaction time from which the utility resumes transaction verification. The provided transaction time is compared against transaction recorded time. The utility loads transactions which have a transaction timestamp greater than or equal to the provided time.

If this parameter is not provided, then the utility starts processing transactions from the earliest transaction in the database as per transaction time or loads progress from file if the `-f` option is specified.

{{< note >}}
* `--load-tx-time` takes preference over the `-f` option in terms of progress loading.
* `--load-tx-time` takes preference over the `-l` option in terms of progress reloading. If both are provided, then the utility starts processing transactions from the provided transaction time and any progress is recorded in the file specified with the `-l` option. In this way, when the utility is restarted later without providing the `–load-tx-time` option but still specifying the `-l` option, it can resume processing transactions from the last stop point.
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
2. Provide UTC timestamp in format: `2007-12-03T10:15:30.00Z`. The string must represent a valid instant in UTC and is parsed using `DateTimeFormatter.ISO_INSTANT`.
