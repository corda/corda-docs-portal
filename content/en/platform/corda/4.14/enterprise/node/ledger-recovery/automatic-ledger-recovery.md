---
date: '2023-11-20'
menu:
  corda-enterprise-4-14:
    identifier: corda-enterprise-4-14-corda-ledger-recovery-automatic
    name: "Automatic ledger recovery"
    parent: corda-enterprise-4-14-corda-ledger-recovery
tags:
- ledger recovery

title: Automatic ledger recovery
weight: 900
---

# Automatic ledger recovery

[Ledger recovery]({{< relref "ledger-recovery.md" >}}) was introduced to complement the normal backup and recovery process. Ledger recovery involves using [the Ledger Recovery flow]({{< relref "ledger-recovery-flow.md" >}}) to enable a node to restore transactions from its peer nodes in the event of local data loss.

*Automatic ledger recovery* enables ledger recovery to automatically run as a `EnterpriseLedgerRecoveryFlow` [system flow]({{< relref "../../cordapps/system-flows.md" >}}) at the startup of a node. This is done to ensure that the node will synchronize with the rest of its network on a regular basis, at startup, before proceeding to process user and customer CorDapp flows. Any time a node is restarted and automatic ledger recovery is enabled, the first thing it will do is identify any inconsistencies and repair them automatically (where possible). Any other flows are deferred until the ledger recovery flow is complete.

To turn on automatic ledger recovery, you must at a minimum:

1. For the [node configuration]({{< relref "../setup/corda-configuration-fields.md" >}}), inside *[enterpriseConfiguration]({{< relref "../setup/corda-configuration-fields.md#enterpriseconfiguration" >}})*, configure `runSystemFlowsAtStartup` to be `true`.
2. Specify a value for `recoveryMaximumBackupInterval`.

The following example shows the minimum configuration required to enable automatic ledger recovery:

```json
enterpriseConfiguration = {
    runSystemFlowsAtStartup = true
    ledgerRecoveryConfiguration = {
        recoveryMaximumBackupInterval = 10d
    }
}
```

Note that instead of using the `recoveryMaximumBackupInterval` node parameter, the `recoveryMaximumBackupInterval` [network parameter]({{< relref "../../network/available-network-parameters#recoverymaximumbackupinterval" >}}) can be used if you are using CENM 1.6 or later. If you are using CENM 1.5 then the parameter must be specified as shown above.

The metric `EnterpriseLedgerRecoveryFlow.RecoveryResults` is returned at the end of automatic ledger recovery:

- `EnterpriseLedgerRecoveryFlow.RecoveryResults.TotalRecoveredRecords` - Long; total number of recovered transaction distribution records. For the purpose of recovery counting,
  there is a one-to-one association with a single transaction on a node.
- `EnterpriseLedgerRecoveryFlow.RecoveryResults.TotalRecoveredTransactions` - Long; total number of recovered transactions. This may be less than the total number of distribution records
  if there are any transactions that already exist in the recovering node's database.
- `EnterpriseLedgerRecoveryFlow.RecoveryResults.TotalRecoveredInFlightTransactions` - Long; total number of in-flight transactions recovered where the `alsoFinalize` option has been specified.
- `EnterpriseLedgerRecoveryFlow.RecoveryResults.TotalErrors` -
