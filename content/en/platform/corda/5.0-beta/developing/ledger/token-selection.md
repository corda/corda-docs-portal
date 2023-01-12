---
date: '2023-01-12'
title: "States"
menu:
  corda-5-beta:
    parent: corda-5-beta-ledger
    identifier: corda-5-beta-token-selection
    weight: 8500
section_menu: corda-5-beta
---

## Token Selection

The [Token Selection API] enables a flow to exclusively select a set of states to potentially use as input states in a UTXO transaction. Although this can be achieved with simple vault queries, the selection API offers the following key features that improve the performance and reliability of the flows:

* **Exclusivity** In an environment where multiple instances of a flow are running in parallel, it is important that each flow can exclusively claim states to spend. Without this, there is a high chance that multiple flows could attempt to spend the same states at the same time, causing transactions to fail during notarization, due to an attempt to spend a state that has already been spent.

* **Target Amount Selection** When selecting fungible states to spend it is usual to select multiple states that sum to at least the target value of the proposed transaction. The selection API provides an explicit model for achieving this, which would be difficult to achieve using standard vault queries.

* **Performance** Providing a dedicated API for this specific type of state selection allows implementations that are not coupled to the vault query API and therefore can be optimized for the specific query patterns.