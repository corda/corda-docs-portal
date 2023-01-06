---
date: '2023-01-06'
title: "Transactions"
menu:
  corda-5-beta:
    parent: corda-5-beta-ledger
    identifier: corda-5-beta-transactions
    weight: 2000
section_menu: corda-5-beta
---

A transaction is a proposal to update the ledger. It is only committed to the ledger if it:

* does not contain double-spends.
* is contractually valid.
* is signed by the required parties.

You can not edit the Corda ledger. The only way to change it is to add new transactions to it. A transaction updates the ledger by consuming existing input states and outputting new states. The states the transaction consumes are marked “consumed”.

Every state is immutable. It can not be changed. This is called an UTXO (unspent transaction output) model.

The following is an example of a transaction with two inputs and two outputs:

{{< 
  figure
	 src="basic-tx.png"
	 figcaption="Basic Transaction"
>}}

A transaction can contain any number of inputs, outputs, and references of any type. Transactions can:

* include different types of states representing multiple financial instruments, such as cash or bonds.
* issue states, by creating a transaction without inputs. These states do not replace any existing states because none are marked “consumed”.
* exit states by creating transactions without outputs. This does not create any new states to replace the ones consumed.
* merge or split fungible assets. For example, they may combine a $2 state and a $5 state into a $7 cash state.

Transactions are atomic. Either all of the transaction’s proposed changes are accepted or none.

There are two basic types of transactions:

* Notary-change transactions, to change a state’s notary. 
* General transactions, for everything else.

{{< note >}}
Notary-change transactions will be implemented in a future release.
{{< /note >}}