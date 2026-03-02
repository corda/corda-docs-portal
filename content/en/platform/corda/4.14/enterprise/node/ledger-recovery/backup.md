---
date: '2023-11-08'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-corda-ledger-recovery
tags:
- ledger recovery backup
title: Backup policy and confidential identities
weight: 400
---

# Backup policy and confidential identities

Ledger Recovery is intended to be used in conjunction with a holistic Corda network backup policy. The `LedgerRecoveryFlow`
defaults to using the ledger `recoveryMaximumBackupInterval` network parameter value for its `TimeRecoveryWindow`.
For more information on the `recoveryMaximumBackupInterval` network parameter, see
[Available network parameters]({{< relref "../../network/available-network-parameters.md#recoverymaximumbackupinterval" >}}).

Recovering transactions using confidential identities requires the successful backup of the previous window of auto-generated
confidential identities. The `confidentialIdentityMinimumBackupInterval` network parameter must be configured to specify the cut-off time after
which we assume keys have not been backed up.

For more information on the `confidentialIdentityMinimumBackupInterval` network parameter, see
[Available network parameters]({{< relref "../../network/available-network-parameters.md#confidentialidentityminimumbackupinterval" >}}).
