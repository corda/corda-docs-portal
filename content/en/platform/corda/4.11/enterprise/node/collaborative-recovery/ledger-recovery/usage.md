---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery
title: Usage
weight: 700
---

# Usage

Ledger Recovery should be considered a tool to complement a standardised Corda Network operational backup and recovery process.
It should be used to re-instate a Corda database from the point of a consistent back-up, and should not be considered
a tool to recover a partially corrupt database (eg. where records may be missing from a subset of tables).
The Ledger Recovery process utilises new recovery distribution records in conjunction with the atomicity semantics
of recording corda transactions, which encompass recording the transaction to the `node_transactions` table, updating the
vault states tables and, optionally, updating any other custom contract state tables associated with the transaction.

{{< important >}}
You must restart the recovering node before calling the `LedgerRecoveryFlow.`
This is to ensure that in-memory state, such as transaction caches, does not interfere with the recovery process.
{{</ important >}}

You can perform ledger recovery by using one of the following methods:

* Node shell commands
* Directly invoking the recovery flow, either from the node shell or programmatically within a CorDapp:

```kotlin
net.corda.core.flows.LedgerRecoveryFlow
```

All recovery operations return a `LedgerRecoveryResult`.
Use `verboseLogging` to generate detailed information in the Corda node logs for individual records and transactions recovered.
