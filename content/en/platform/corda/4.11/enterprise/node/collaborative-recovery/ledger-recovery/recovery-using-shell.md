---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery
title: Ledger recovery using the shell
weight: 800
---

# Ledger recovery using the shell

The following examples show the different ways to use the ledger recovery flow from the Corda node shell.

* Run ledger recovery for a given time window and using all available nodes in the network:

  ```bash
  flow start EnterpriseLedgerRecoveryFlow timeWindow: { fromTime: "2023-07-19T09:00:00Z", untilTime: "2023-07-19T09:00:00Z" }, useAllNetworkNodes: true
  ```

* Run ledger recovery without actually performing reconciliation (for example, `dryRun = true`) with detailed
  record/transaction-level output (`verboseLogging = true`) for a given time window and using all available nodes in the network:

  ```bash
  flow start EnterpriseLedgerRecoveryFlow timeWindow: { fromTime: "2023-07-19T09:00:00Z", untilTime: "2023-07-19T09:00:00Z" }, dryRun: true, verboseLogging: true, useAllNetworkNodes: true
  ```

* Run ledger recovery for a given time window and specifying a single specific peer recovery node:

  ```bash
  flow start EnterpriseLedgerRecoveryFlow timeWindow: { fromTime: "2023-10-12T19:00:00Z", untilTime: "2023-12-12T22:00:00Z" }, recoveryPeer:  "O=Bank B, L=New York, C=US"
  ```

* Run ledger recovery for a given time window and specifying several peer recovery nodes:

  ```bash
  flow start EnterpriseLedgerRecoveryFlow timeWindow: { fromTime: "2023-10-12T19:00:00Z", untilTime: "2023-12-12T22:00:00Z" }, recoveryPeers: ["O=Bank B, L=New York, C=US", "O=Bank C, L=Chicago, C=US"]
  ```

* Run ledger recovery for a given time window and single peer recovery node, and perform finality flow recovery of any encountered `IN_FLIGHT` transactions:

  ```bash
  flow start EnterpriseLedgerRecoveryFlow timeWindow: { fromTime: "2023-10-12T19:00:00Z", untilTime: "2023-12-12T22:00:00Z" }, recoveryPeer:  "O=Bank B, L=New York, C=US", alsoFinalize: true
  ```
