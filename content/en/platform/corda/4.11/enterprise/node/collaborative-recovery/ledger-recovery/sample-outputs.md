---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery
title: Ledger recovery using the shell
weight: 900
---

# Sample outputs

```bash
>>> flow start EnterpriseLedgerRecoveryFlow  recoveryPeer: "O=Bob Plc, L=Rome, C=IT", timeWindow: {  fromTime:  "2023-10-30T12:00:00Z",  untilTime:  "2023-10-30T19:45:00Z" }, dryRun: false

 ✅   Starting
 ✅   Validating recovery peers
 ✅   Performing window narrowing with peers
 ✅   Performing reconciliation with peers
➡️   Done
Flow completed with result: LedgerRecoveryResult(totalRecoveredRecords=2, totalRecoveredTransactions=-1, totalErrors=-1)
```
