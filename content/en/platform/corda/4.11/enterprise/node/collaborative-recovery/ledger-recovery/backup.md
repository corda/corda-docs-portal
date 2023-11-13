---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery backup
title: Backup policy and confidential identities
weight: 400
---

# Backup policy and confidential identities

Ledger Recovery is intended to be used in conjunction with a holistic Corda Network backup policy. The `LedgerRecoveryFlow`
defaults to using the ledger `transactionRecoveryPeriod` parameter value for its `TimeRecoveryWindow`.

For more information on the `transactionRecoveryPeriod` network parameter, see
[Available Network Parameters]({{< relref "../../../network/available-network-parameters.md" >}}).

Recovering transactions using confidential identities requires the successful backup of the previous window of auto-generated
CIs.The `confidentialIdentityPreGenerationPeriod` network parameter must be configured to specify the cut-off time after
which we assume keys have not been backed up.

For more information on the `confidentialIdentityPreGenerationPeriod` network parameter, see
[Available Network Parameters]({{< relref "../../../network/available-network-parameters.md" >}}).
