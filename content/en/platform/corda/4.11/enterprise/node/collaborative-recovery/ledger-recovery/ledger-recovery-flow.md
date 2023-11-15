---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery flow
- ledger recovery flow parameters
title: Ledger Recovery flow parameters
weight: 100
---

# Ledger Recovery flow parameters

The Ledger Recovery flow takes the following parameters:

```
val recoveryPeers: Collection<Party>,
val timeWindow: RecoveryTimeWindow? = null,
val useAllNetworkNodes: Boolean = false,
val dryRun: Boolean = false,
val useTimeWindowNarrowing: Boolean = true,
val verboseLogging: Boolean = false,
val recoveryBatchSize: Int = 1000,
val alsoFinalize: Boolean = false
```

#### `recoveryPeers`

`recoveryPeers` refers to a list of peer nodes to use for recovery. This parameter is mandatory unless using `useAllNetworkNodes`.

#### `timeWindows`

`timeWindow` refers to the recovery time window and defines a `fromTime` and `untilTime`. This parameter is mandatory,
if not explicitly defined in configuration.

If a value is not specified by the user, the flow will attempt to use the Corda Network or node configuration configured time window.
The precedence order for this parameter is user-specified first, then node configuration, then Corda Network parameter.

#### `useAllNetworkNodes`

`useAllNetworkNodes` specifies if all peer nodes in the network map (excluding notary nodes) are to be used for recovery.
This parameter is optional. The default value is *false*. If set to *true*, this parameter overrides the `recoveryPeers` list.

#### `dryRun`

`dryRun` can be used to identify missing transactions without performing actual recovery. This parameter is optional. It defaults to *false*.

#### `useTimeWindowNarrowing`

`useTimeWindowNarrowing` specifies whether to use a window narrowing algorithm to determine the optimal time window of transactions
that are recoverable from a peer. It defaults to *true*.
For example, if the original time window specifies 30 days and there are only 3 consecutive days of missing transactions
from day 10 to day 12, a narrowed time window will determine that reconciliation only needs to take place for that 3-day time period.

#### `verboseLogging`

`verboseLogging` specifies whether to log details of each recovered transaction. By default, the flow only reports
total counts of recovered records. It defaults to *false*.

#### `recoveryBatchSize`

`recoveryBatchSize` is a performance-tuning parameter that specifies how many records should be recovered in each interaction with
a recovery peer. It has been fine-tuned to a value of 1000 and can be tweaked to take into account the amount of physical memory
available on a node host.

#### `alsoFinalize`

`alsoFinalize` specifies whether to attempt recovery of any `IN_FLIGHT` transactions recovered from a peer.
It defaults to *false*. See also [Finality Flow Recovery]({{< relref "../../../finality-flow-recovery.md" >}}).
{{< note >}}
This option attempts to finalize any `FAILED` in-flight transactions (either recovered as part of the previous
ledger recovery step or already existent within the local database) within the recovery `timeWindow`.
{{< /note >}}

#### `LedgerRecoverFlow`

`LedgerRecoverFlow` returns a `LedgerRecoveryResult` which includes the following information:

* `totalRecoveredRecords`: Long; total number of recovered transaction Distribution Records. For the purpose of recovery counting,
  there is a one-to-one association with a single transaction on a node.
* `totalRecoveredTransactions`: Long; total number of recovered transactions. This may be less than the total number of distribution records
  if there are any transactions that already exist in the recovering node's database.
* `totalRecoveredInFlightTransactions`: Long; total number of in-flight transactions recovered where the `alsoFinalize` option has been specified.
* `totalErrors`: Long; total number of errors encountered upon attempting recovery. See the node logs for details of these errors.

A `LedgerRecoveryException` is thrown if a fatal error occurs upon attempting recovery; for example, if no time window is
specified and no time window configuration is defined.

{{< warning >}}
This flow only works with transactions that are persisted with recovery metadata.
This is everything that originated on Corda 4.11 onwards, involving peer nodes that are Corda 4.11 onwards.
Transactions distributed prior to 4.11 are not included, and neither are distributions involving nodes prior to 4.11.
{{< /warning >}}
