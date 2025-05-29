---
date: '2023-11-08'
menu:
  corda-enterprise-4-13:
    parent: corda-enterprise-4-13-corda-ledger-recovery
tags:
- ledger recovery
title: Usage
weight: 700
---

# Usage

You can perform Ledger Recovery using one of the following methods:

* Node shell commands
* Directly invoking the recovery flow, either from the node shell or programmatically within a CorDapp:

  ```kotlin
  net.corda.core.flows.LedgerRecoveryFlow
  ```

All recovery operations return a `LedgerRecoveryResult`.
Use `verboseLogging` to generate detailed information in the Corda node logs for individual records and transactions recovered.
Enable verbose logging with caution as it will increase the size of your logs.

{{< important >}}
A Corda node maintains internal caches that could become out of synch with the database if a Corda node is not brought down during
restoration of a database to a prior backup. If the node has not been brought down, it should be restarted prior to commencing use
of the recovery features.
This is to ensure that in-memory state, such as transaction caches, does not interfere with the recovery process.
{{</ important >}}
