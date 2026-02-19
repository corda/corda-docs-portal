---
description: "The steps that TVU goes through when validating transactions."
date: '2023-12-15'
menu:
  corda-enterprise-4.14:
    identifier: corda-enterprise-4.14-tvu-behavior
    parent: corda-enterprise-4.14-tvu
tags:
- tvu
- transaction validator utility
title: TVU behavior
weight: 100
---

# TVU behavior

This section describes the steps that the Transaction Validator Utility (TVU) goes through when validating transactions present in a specified database.

1. Upon startup, the utility connects to the specified database.
2. If it is not able to connect to the database, it exits with an error message.
3. It executes distinct actions based on the specified CLI option. See [TVU CLI parameters]({{< relref "tvu-cli.md" >}}).
4. It loads a transaction processing class:
    * If the `-c` or `--class-load` option is provided, then the user-defined transaction processing class is loaded. For more information, see [User-defined transaction processing]({{< relref "#user-defined-transaction-processing" >}}).
    * If the `-c` or `--class-load` option is not provided, then the utility uses the default transaction processing class which includes transaction verification and deserialization.
5. It starts reading transactions from the database.
6. It submits transactions to an executor which processes them in separate threads using the loaded process class.
7. It registers progress as per given CLI parameters.
8. It registers any processing-related errors.
9. It waits for all transaction processing to complete.
10. It disconnects cleanly from the database, shuts down the executor when all transactions are verified and writes progress and errors to underlying resources.
11. It exits upon completion or can be stopped. See the [Stopping TVU]({{< relref "stopping-tvu.md" >}}) section.

## User-defined transaction processing

You can provide a user-defined class to process transactions at runtime using the `-c` or `--class-load` CLI option. If you do not provide the `-c` CLI option, then the utility defaults to load the process which performs transaction verification and deserialization.
To learn how to create your own pluggable class, follow the steps in the [Creating TVU classes]({{< relref "testing-tvu.md" >}}) section.
