---
date: '2023-11-20'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-corda-nodes-collaborative-recovery
    name: "Collaborative Recovery"
    parent: corda-enterprise-4-12-corda-nodes
tags:
- disaster recovery
- collaborative recovery
- install
- node operator

title: Collaborative Recovery
weight: 100
---

# Collaborative Recovery

[Ledger Recovery flow]({{< relref "ledger-recovery/ledger-recovery-flow.md" >}}) (`LedgerRecoveryFlow`) tool was introduced as part of the Corda 4.11 release. It enables a node to identify and recover transactions from peer recovery nodes to which it was a party and which are missing from its own ledger. In Corda 4.11 and above, you can use both [Ledger Recovery]({{< relref "ledger-recovery/overview.md" >}}) or [Collaborative Recovery V1.2.1]({{< relref "collaborative-recovery-121/introduction-cr.md" >}}) to re-instate a Corda database.

If you are using a pre-4.11 Corda, use [Collaborative Recovery V1.2.1]({{< relref "collaborative-recovery-121/introduction-cr.md" >}}) CorDapps to identify and retrieve your data.
