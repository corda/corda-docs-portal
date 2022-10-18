---
aliases:
- /head/key-concepts-consensus.html
- /HEAD/key-concepts-consensus.html
- /key-concepts-consensus.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-9-key-concepts-consensus
    parent: corda-community-4-9-key-concepts
    weight: 1070
tags:
- concepts
- consensus
title: Consensus
---

# Consensus

## Summary

* Transactions must achieve *validity consensus* **and** *uniqueness consensus* to be committed to the ledger.
* Validity consensus determines if a transaction is accepted by the [smart contracts](key-concepts-contracts.md) it references.
* Uniqueness consensus prevents double-spends.

## Video

{{% vimeo 214138438 %}}

## Consensus on Corda
There must be *consensus* that a proposed transaction is valid before you can add it to the ledger. Blockchains use *consensus mechanisms* to achieve agreement, trust, and security across decentralized networks. You may be familiar with popular mechanisms such as [proof-of-work](https://www.investopedia.com/terms/p/proof-work.asp) or [proof-of-stake](https://www.investopedia.com/terms/p/proof-stake-pos.asp).

Corda is different. You can achieve consensus by proving a transaction is both *valid* and *unique*.

## Validity consensus

Validity consensus checks that, for the proposed transaction and for every transaction in the backchain that generated the inputs to the proposed transaction:

* The transaction is accepted by the contracts of every input and output state.
* The transaction has all the required signatures.

This called *walking the chain*.

For example, if a node proposes a transaction
transferring a treasury bond, the bond transfer is only valid if:

* The treasury bond was issued by the central bank in a valid issuance transaction.
* Every subsequent transaction in which the bond changed hands was also valid.

Walking the chain for this transaction would look like this:

{{< figure alt="validation consensus" width=80% zoom="/en/images/validation-consensus.png" >}}

When verifying a proposed transaction, a node may not have every transaction in the transaction chain that they
need to verify. In this case, they can request the missing transactions from the transaction proposer. The
transaction proposer always has the full transaction chain, because they must request it when
verifying the transaction that created the proposed transaction’s input states.

## Uniqueness consensus

Uniqueness consensus is when a [notary](key-concepts-notaries.md) checks that a [node](key-concepts-node.md) hasn't used the same input for multiple transactions.

Imagine that Alice holds a valid central-bank-issued cash state of $1,000,000. Alice can create two transaction
proposals:

* A transaction transferring the $1,000,000 to Bob in exchange for £800,000.
* A transaction transferring the $1,000,000 to Charlie in exchange for €900,000.

Both transactions will achieve validity consensus, yet Alice has managed to “double-spend” her USD to get double the amount of GBP and EUR:

{{< figure alt="uniqueness consensus" width=80% zoom="/en/images/uniqueness-consensus.png" >}}

To prevent this, a valid transaction proposal must also achieve uniqueness consensus. Uniqueness consensus is the
requirement that none of the inputs to a proposed transaction have already been consumed in another transaction.

If one or more of the inputs have already been consumed in another transaction, this is known as a *double spend*,
and the [notary](key-concepts-notaries.md) marks the transaction proposal as invalid.


