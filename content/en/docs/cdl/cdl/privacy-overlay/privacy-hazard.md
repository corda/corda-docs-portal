---
title: The privacy hazard
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-privacy-overlay"
    identifier: "cdl-privacy-overlay-privacy-hazard"
    weight: 10

tags:
- cdl
- cordapp design language
- ledger evolution
- privacy overlay
- cordapp diagram
---

# The Privacy Hazard

When constructing a transaction ensuring privacy is relatively straight forward: the required Parties to the states are added to the participants property of each state and Corda will make sure that the union of those participants across all the states in the transaction get a copy of the transaction. If you don't want to send a transaction to someone, don't include them in the participants.

For any transaction to be proved valid, the Corda node must establish that the input states are also valid. Corda does this by acquiring the transaction that created those input states and rerunning the verify() checks on that transaction. It is also possible that this transaction has input states which need verifying, so the Corda node must receive and verify the transaction that created those input states as well. This continues recursively back through the ledger DAG until there are no more input states to verify. This process is called transaction resolution and the states that are resolved are sometimes called the backchain.

This approach is powerful because it removes the need for all Parties on the ledger to hold a full copy of the ledger, which some blockchains require, leading to scalability issues. Instead Corda acts like a wallet where only the transactions required to validate a transaction are stored in a particular node's vault.

The hazard is that if there is anything in the backchain which the current node shouldn't see, then there is a privacy leak. This might include:

* Past asset owners.
* The details of assets previously exchanged for assets in the current transaction.
* The details of deals which lead to previous exchanges of assets in the current transaction.

By using an appropriate CorDapp design, these scenarios can be avoided. To help establish an appropriate CorDapp design we have the Ledger Evolution view Privacy Overlay.
