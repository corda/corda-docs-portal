---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery
title: Corda node shell sample output
weight: 900
---

# Corda node shell sample output

```bash
>>> flow start EnterpriseLedgerRecoveryFlow  recoveryPeer: "O=Bob Plc, L=Rome, C=IT", timeWindow: {  fromTime:  "2023-10-30T12:00:00Z",  untilTime:  "2023-10-30T19:45:00Z" }, dryRun: false
	@@ -246,6 +246,60 @@ The following examples show the different ways to use the ledger recovery flow f
 ✅   Validating recovery peers
 ✅   Performing window narrowing with peers
 ✅   Performing reconciliation with peers
 ✅   Performing finality recovery of in flight transactions
➡️   Done
Flow completed with result: LedgerRecoveryResult(totalRecoveredRecords=2, totalRecoveredTransactions=2, totalRecoveredInFlightTransactions=0, totalErrors=0))
```
