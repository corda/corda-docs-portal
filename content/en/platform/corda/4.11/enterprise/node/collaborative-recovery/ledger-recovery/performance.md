---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery performance
title: Performance
weight: 1100
---

# Performance

The Ledger Recovery flow has been optimised to support large-scale recovery of transactions (internal testing has been conducted
using tens of thousands of transactions). This has been accomplished using a combination of:
* parallelism: when recovering against more than one peer.
* batching at several layers: reconciliation window, across-the-wire transfer of records and transactions,
and database transactional updates.

Window narrowing uses a cryptographic hashing algorithm to rapidly determine the optimal recovery
window for any given peer. Furthermore, internal state is kept to a minimum, thus enabling recovery to be resumed from the
point it left off, should there be any interruption in service.
