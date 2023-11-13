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

You can perform Ledger Recovery by using one of the following methods:

* Node shell commands
* Directly invoking the recovery flow, either from the node shell or programmatically within a CorDapp:

  ```kotlin
  net.corda.core.flows.LedgerRecoveryFlow
  ```

All recovery operations return a `LedgerRecoveryResult`.
Use `verboseLogging` to generate detailed information in the Corda node logs for individual records and transactions recovered.

{{< important >}}
You must restart the recovering node before calling the `LedgerRecoveryFlow.`
This is to ensure that in-memory state, such as transaction caches, does not interfere with the recovery process.
{{</ important >}}
