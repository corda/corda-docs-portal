---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- archiving ledger recovery records
title: Archiving
weight: 1200
---

# Archiving

The [Archive Service](../../archiving/archiving-setup.md) archives Ledger Recovery distribution
records associated with the archived transactions. The tables `node_sender_distribution_records` and `node_receiver_distribution_records`
are included in the archiving process.
