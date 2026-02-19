---
date: '2023-11-08'
menu:
  corda-enterprise-4.14:
    parent: corda-enterprise-4.14-corda-ledger-recovery
tags:
- ledger recovery
title: Ledger Recovery using the shell
weight: 800
---

# Ledger recovery using the shell

The following examples show the different ways to use the Ledger Recovery flow from the Corda node shell.

* Run Ledger Recovery for a given time window and using all available nodes in the network:

  ```bash
  flow start LedgerRecoveryFlow timeWindow: { fromTime: "2023-07-19T09:00:00Z", untilTime: "2023-07-19T09:00:00Z" }, useAllNetworkNodes: true
  ```

* Run Ledger Recovery without actually performing reconciliation (for example, `dryRun = true`) with detailed
  record/transaction-level output (`verboseLogging = true`) for a given time window and using all available nodes in the network:

  ```bash
  flow start LedgerRecoveryFlow timeWindow: { fromTime: "2023-07-19T09:00:00Z", untilTime: "2023-07-19T09:00:00Z" }, dryRun: true, verboseLogging: true, useAllNetworkNodes: true
  ```

* Run Ledger Recovery for a given time window and specifying a single specific peer recovery node:

  ```bash
  flow start LedgerRecoveryFlow timeWindow: { fromTime: "2023-10-12T19:00:00Z", untilTime: "2023-12-12T22:00:00Z" }, recoveryPeer:  "O=Bank B, L=New York, C=US"
  ```

* Run Ledger Recovery for a given time window and specifying several peer recovery nodes:

  ```bash
  flow start LedgerRecoveryFlow timeWindow: { fromTime: "2023-10-12T19:00:00Z", untilTime: "2023-12-12T22:00:00Z" }, recoveryPeers: ["O=Bank B, L=New York, C=US", "O=Bank C, L=Chicago, C=US"]
  ```

* Run Ledger Recovery for a given time window and single peer recovery node, and perform finality flow recovery of any encountered `IN_FLIGHT` transactions:

  ```bash
  flow start LedgerRecoveryFlow timeWindow: { fromTime: "2023-10-12T19:00:00Z", untilTime: "2023-12-12T22:00:00Z" }, recoveryPeer:  "O=Bank B, L=New York, C=US", alsoFinalize: true
  ```

## Corda node shell sample output

```bash
>>> flow start LedgerRecoveryFlow  recoveryPeer: "O=Bob Plc, L=Rome, C=IT", timeWindow: {  fromTime:  "2023-10-30T12:00:00Z",  untilTime:  "2023-10-30T19:45:00Z" }, dryRun: false
	@@ -246,6 +246,60 @@ The following examples show the different ways to use the ledger recovery flow f
 ✅   Validating recovery peers
 ✅   Performing window narrowing with peers
 ✅   Performing reconciliation with peers
 ✅   Performing finality recovery of in flight transactions
➡️   Done
Flow completed with result: LedgerRecoveryResult(totalRecoveredRecords=2, totalRecoveredTransactions=2, totalRecoveredInFlightTransactions=0, totalErrors=0))
```
