---
date: '2023-11-08'
menu:
  corda-enterprise-4-13:
    parent: corda-enterprise-4-13-corda-ledger-recovery
tags:
- monitoring ledger recovery
title: Monitoring ledger recovery process
weight: 1000
---

# Monitoring ledger recovery process

The Corda node log files provide initial informational messages and incremental updates on the number of records recovered at a given moment in time:

* Initial start-up:
  ```
  Ledger recovery for node O=Alice Corp, L=Madrid, C=ES synchronising with peers [O=Charlie Ltd, L=Athens, C=GR] over time window RecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, untilTime=2023-11-07T16:43:03Z).
  Ledger recovery parameters: LedgerRecoveryParameters(recoveryPeers=[O=Charlie Ltd, L=Athens, C=GR], timeWindow=RecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, untilTime=2023-11-07T16:43:03Z), useAllNetworkNodes=false, dryRun=false, useTimeWindowNarrowing=true, verboseLogging=false, recoveryBatchSize=1000, alsoFinalize=false)
  ```

* Per peer time window narrowing:
  ```
  Ledger reconciliation window flow for node O=Alice Corp, L=Madrid, C=ES synchronising with peer O=Charlie Ltd, L=Athens, C=GR over time window RecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, untilTime=2023-11-07T16:43:04Z)
  Performing time windowed hash reconciliation with peer: O=Charlie Ltd, L=Athens, C=GR
  Narrowest time window for O=Charlie Ltd, L=Athens, C=GR is RecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, untilTime=2023-11-07T16:43:04Z) [initial: RecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, untilTime=2023-11-07T16:43:04Z)]
  ```

* Per peer reconciliation:
  ```
  Performing reconciliation with peer O=Charlie Ltd, L=Athens, C=GR for SENDER records using recoveryBatchSize: 1000 and time window: ComparableRecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, fromTimestampDiscriminator=0, untilTime=2023-11-07T16:43:04Z, untilTimestampDiscriminator=2147483647) (dryRun = false)
  ```

* Per recovery batch iteration:
  ```
  Reconciliation flow received 2 SENDER recovery distribution record keys from peer O=Charlie Ltd, L=Athens, C=GR.
  Reconciliation flow has identified 2 missing SENDER records in local ledger for time window ComparableRecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, fromTimestampDiscriminator=0, untilTime=2023-11-07T16:43:04Z, untilTimestampDiscriminator=2147483647)
  Adjusting timestamp to ComparableRecoveryTimeWindow(fromTime=2023-11-07T16:43:01Z, fromTimestampDiscriminator=2, untilTime=2023-11-07T16:43:04Z, untilTimestampDiscriminator=2147483647) [latest batch record with latestTimestamp=2023-11-07T16:43:01Z]
  Reconciliation flow recovered 2 records so far.
  ```

* Final summary:
  ```
  Ledger recovery successfully recovered LedgerRecoveryResult(totalRecoveredRecords=2, totalRecoveredTransactions=2, totalRecoveredInFlightTransactions=0, totalErrors=0) records. {actor_id=mark, actor_owning_identity=O=Alice Corp, L=Madrid, C=ES
  ```
  or
  ```
  Ledger recovery completed without detecting any records missing within time window RecoveryTimeWindow(fromTime=2023-11-07T16:42:58Z, untilTime=2023-11-07T16:43:03Z)
  ```

* Furthermore, if `verboseLogging = true`, the reconciliation phase will include additional details of the progress:
  ```
  Peer returned distribution record keys: [List of distribution record keys]
  Recovery node identified missing distribution records: [List of distribution record keys]
  ```
