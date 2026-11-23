---
description: "The steps that TVU goes through when validating transactions."
date: '2023-12-15'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tvu-behavior
    parent: corda-enterprise-4-12-tvu
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

## Performance options

{{< note >}}
The performance options in this section are available from Corda Enterprise 4.12.13 only.
{{< /note >}}

By default, the TVU reads transactions through a single database cursor and verifies transactions that require external verification using a single external verifier process. You can change this behavior if either of these becomes a bottleneck.

### Parallel reading

When reading from the database, rather than verification, is the bottleneck, use the `-r` or `--readers` option to read transactions through several database cursors at once. The TVU divides the transactions into slices of about 25,000 transactions, and each reader uses its own database connection. See [TVU CLI parameters]({{< relref "tvu-cli.md" >}}).

Slices finish out of order, so the progress the TVU records always names the newest transaction for which all older transactions have been verified. If you resume a run, the TVU may re-verify some transactions that were already verified, at most about one slice for each reader.

Parallel reading requires an index on `node_transactions (status, timestamp, tx_id)`, which the node schema does not create. If the index is missing, the TVU does not start and prints the statement that creates the index, because without the index every slice would scan the whole table twice. The node does not use this index and it adds work to every write to the table, so drop the index when you have finished using the TVU. See [parallel reading CLI example]({{< relref "tvu-cli-examples.md#parallel-reading" >}}).

### External verifiers

A transaction that the node cannot verify in its own process, such as a transaction created by an older version of Corda, is verified by an external verifier. This is a separate JVM that verifies one transaction at a time. When most transactions take this route, a single external verifier limits the throughput of the whole run, regardless of the number of verification threads set with `-s`.

Use the `-x` or `--verifiers` option to start several external verifiers. Each verifier handles one transaction at a time, so the number of verifiers is the number of transactions that can be verified in parallel. Each verifier is a full JVM that loads the CorDapps, so `n` verifiers use `n` times the memory of one. Set the heap size of each verifier with `custom.externalVerifierJvmArgs` in the `node.conf` file, for example `custom { externalVerifierJvmArgs = ["-Xmx1g"] }`. See [TVU CLI parameters]({{< relref "tvu-cli.md" >}}).

If you start more than one verifier, verifier `<n>`, numbered from 0, runs in `<base-directory>/verifier-pool/<n>` and writes its logs to the `logs` directory in that directory. These directories remain after the run.

## User-defined transaction processing

You can provide a user-defined class to process transactions at runtime using the `-c` or `--class-load` CLI option. If you do not provide the `-c` CLI option, then the utility defaults to load the process which performs transaction verification and deserialization.
To learn how to create your own pluggable class, follow the steps in the [Creating TVU classes]({{< relref "testing-tvu.md" >}}) section.
