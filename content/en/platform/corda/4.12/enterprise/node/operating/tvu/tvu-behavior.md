---
date: '2023-12-15'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tvu-behavior
    parent: corda-enterprise-4-12-tvu
tags:
- tvu
- transaction validator utility
title: Transaction Validator Utility behavior
weight: 100
---

# Transaction Validator Utility behavior

This section describes the steps that the TVU goes through when validating transactions present in a specified database.

1. Upon startup, the utility connects to the specified database.
2. If it is not able to connect to the database, it exits with an error message.
3. It executes distinct actions based on the specified CLI option. If nothing specified, the following happens:
    * The present working directory is treated as the node’s base directory. The utility proceeds to read the node’s configuration (`node.conf`), CorDapps (CorDapps directory), drivers (drivers directory), and network parameters (`network-parameters` file) from the present working directory.
Reason: `-b` option not provided.
    * The present working directory is treated as the error registration directory. Any transaction verification, deserialization, or processing errors are registered in the `present-working-directory/yyyy-MM-dd-HH-mm-ss` directory where `yyyy-MM-dd-HH-mm-ss` is the current timestamp.
Reason: `-e` option not provided.
    * No progress is registered or reloaded as no file is provided for progress registration and reloading. If the utility is restarted at a later point in time, then it starts processing from the first transaction in the database with respect to transaction time.
Reason: `-l` option not provided.
    * As the ID reverification file is absent, the ID reverification process does not happen.
Reason: `-i` option not provided.
    * The utility processes all the transactions in the provided database, starting from the transaction that was recorded earliest with respect to the transaction timestamp.
Reason: `--load-tx-time` option not provided.
    * Transactions are only validated (verified and deserialized) as the user-defined process class to process the transactions is absent.
Reason: `-c` option not provided.
4. It loads transaction processing class to process transactions.
5. It starts reading transactions from the database.
6. It submits transactions to an executor which processes them in separate threads using the loaded process class.
7. It registers progress as per given CLI parameters.
8. It registers any processing-related errors.
9. It waits for all transaction processing to complete.
10. It disconnects cleanly from the database, shuts down the executor when all transactions are verified and writes progress and errors to underlying resources.
11. It exits upon completion or can be stopped. See the [Stopping Transaction Validator Utility](({{< relref "stopping-tvu" >}})) section.

## User-defined transaction processing

You can provide a user-defined class to process transactions at runtime using the `-c` or `--class-load` CLI option. If you do not provide the `-c` CLI option, then the utility defaults to load the process which performs transaction verification and deserialization.
To learn how to create your own pluggable class, follow the steps in the [Creating Transaction Validator Utility classes](({{< relref "testing-tvu" >}})) section.
