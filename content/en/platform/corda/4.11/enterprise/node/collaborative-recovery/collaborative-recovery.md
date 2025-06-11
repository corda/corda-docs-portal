---
date: '2023-11-20'
menu:
  corda-enterprise-4-11:
    identifier: corda-enterprise-4-11-corda-nodes-collaborative-recovery
    name: "Ledger Recovery vs. Collaborative Recovery"
    parent: corda-enterprise-4-11-corda-nodes
tags:
- disaster recovery
- collaborative recovery
- install
- node operator

title: Ledger Recovery vs. Collaborative Recovery
weight: 100
---

# Ledger Recovery vs. Collaborative Recovery

[Ledger Recovery]({{< relref "ledger-recovery/overview.md" >}}) is introduced as part of the Corda 4.11 release. It enables a node to identify and recover transactions from peer recovery nodes to which it was a party and which are missing from its own ledger. 

In Corda 4.11 [Collaborative Recovery V1.2.1]({{< relref "collaborative-recovery-121/introduction-cr.md" >}}) is deprecated, and will be removed in Corda 4.12.

Therefore:

* If using Corda 4.11 or above, use Ledger[Ledger Recovery]({{< relref "ledger-recovery/overview.md" >}}) to recover your data.
* If using Corda 4.10 or earlier, use [Collaborative Recovery V1.2.1]({{< relref "collaborative-recovery-121/introduction-cr.md" >}}) to recover your data.
