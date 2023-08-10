---
title: "Consensus"
date: 2023-06-08
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-fundamentals-ledger-consensus
    parent: corda51-fundamentals-ledger
    weight: 5000
section_menu: corda51
---

# Consensus

Transactions must achieve both *validity* consensus and *uniqueness* consensus to be committed to the ledger:

* Validity consensus determines if a transaction is accepted by the {{< tooltip >}}smart contracts{{< /tooltip >}} it references.
* Uniqueness consensus prevents double-spends.

## Consensus on Corda

There must be consensus that a proposed transaction is valid before you can add it to the ledger. Blockchains use consensus mechanisms to achieve agreement, trust, and security across decentralized networks. You may be familiar with popular mechanisms such as proof-of-work or proof-of-stake.

Corda is different. Corda's notary service enables you to achieve consensus by proving that a transaction is both valid and unique.

## Validity Consensus

Validity consensus checks that, for the proposed transaction and for every transaction in the backchain that generated the inputs to the proposed transaction:

* The transaction is accepted by the contracts of every input and output {{< tooltip >}}state{{< /tooltip >}}.
* The transaction has all the required signatures.

This is called *walking the chain*.

For example, if a participant proposes a transaction transferring a treasury bond, the bond transfer is only valid if:

* The treasury bond was issued by the central bank in a valid issuance transaction.
* Every subsequent transaction in which the bond changed hands was also valid.

Walking the chain for this transaction would look like this:

{{<
  figure
	 width="50%"
	 src="validation-consensus.png"
	 figcaption="Walking the Chain"
>}}

When verifying a proposed transaction, a {{< tooltip >}}virtual node{{< /tooltip >}} may not have every transaction in the transaction chain that they need to verify. In this case, they can request the missing transactions from the transaction proposer. The transaction proposer always has the full transaction chain, because they must request it when verifying the transaction that created the proposed transaction’s input states.

## Uniqueness Consensus

Uniqueness consensus is when a notary checks that a participant has not used the same input for multiple transactions.

Imagine that Alice holds a valid central-bank-issued cash state of $1,000,000. Alice can create two transaction proposals:

* A transaction transferring the $1,000,000 to Bob in exchange for £800,000.
* A transaction transferring the $1,000,000 to Charlie in exchange for €900,000.

Both transactions will achieve validity consensus, yet Alice has managed to “double-spend” her USD to get double the amount of GBP and EUR:

{{<
  figure
	 width="50%"
	 src="uniqueness-consensus.png"
	 figcaption="Uniqueness Consensus"
>}}

To prevent this, a valid transaction proposal must also achieve uniqueness consensus. Uniqueness consensus is the requirement that none of the inputs to a proposed transaction have already been consumed in another transaction.

If one or more of the inputs have already been consumed in another transaction, this is known as a double-spend, and the notary marks the transaction proposal as invalid.
