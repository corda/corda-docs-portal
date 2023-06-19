---
title: "Transactions"
date: 2023-06-08
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-fundamentals-ledger-transactions
    parent: corda5-fundamentals-ledger
    weight: 2000
section_menu: corda5
---

# Transactions

You can not edit the Corda ledger. The only way to change it is to add new transactions to it. A transaction updates the ledger by consuming existing input states and outputting new states. The states the transaction consumes are marked “consumed”.
Every state is immutable. It can not be changed. This is called an UTXO (unspent transaction output) model.

The following is an example of a transaction with two inputs and two outputs:

{{< 
  figure
     width="50%"
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

## Transaction Backchains
Transaction backchains enable a participant to verify that each input was generated from a valid series of transactions. This is called backchain verification. If you need to break this chain (for example, because you want to increase performance by reducing the number of transactions the node has to check, or because you want to keep previous transactions private) you can reissue states.

Backchains are created as input state references (StateRefs) linked together over time. Input state references let you use the outputs of previous transactions as the inputs of new transactions.

Input state references (StateRefs) consist of:

* The hash of the transaction that created the input.
* The input’s index (location in the backchain) in the outputs of the previous transaction.

The following example transaction shows how this works:

{{< 
  figure
	 width="50%"
	 src="tx-chain.png"
	 figcaption="Transaction Backchain Example"
>}}

## Committing Transactions to the Ledger
Initially, a transaction is only a proposal to update the ledger. It represents the future state of the ledger desired by the transaction builders. It is only committed to the ledger if it:

* does not contain double-spends.
* is contractually valid.
* is signed by the required parties.

### Signatures

To be committed to the ledger, the transaction must receive signatures from all of the required signatories. Each required signatory appends their signature to the transaction to approve the proposal. For example, the following shows a proposed transaction:
{{< 
  figure
	 width="50%"
	 src="tx-with-sigs.png"
	 figcaption="Proposed Signed Transaction"
>}}

The transaction has the required signatures and so the inputs may be marked as consumed, and cannot be used in any future transactions. If otherwise valid, the transaction’s outputs become part of the current state of the ledger: 

{{< 
  figure
	 width="50%"
	 src="tx-chain.png"
	 figcaption="Transaction Backchain Example"
>}}

### Validity

Just gathering the required signatures is not enough to commit a transaction to the ledger. It must also be:

* Valid — the proposed transaction and every transaction on the backchain of the proposed inputs must be contractually valid.
* Unique — no other committed transaction has consumed any of the inputs to the proposed transaction. Uniqueness is determined by a [notary](#notary).

If the transaction gathers all of the required signatures without meeting these conditions, the transaction’s outputs are not valid and will not be accepted as inputs to subsequent transactions.

## Reference States
Some states need to be referred to by the contracts of other input or output states but not updated/consumed. These are known as reference states. When a state is added to the references list of a transaction, instead of the inputs or outputs list, it is treated as a reference state. There are two important differences between regular input states and reference states:
* The specified notary for the transaction does check whether the reference states are current. However, reference states are not consumed when the transaction containing them is committed to the ledger.
* The contracts for reference states are not executed for the transaction containing them.

## Other Transaction Components
As well as input states and output states, transactions contain:

* [Commands](#commands)
* [Attachments](#attachments)
* [Time windows](#time-windows)
* [A notary](#notary)

{{< note >}}
Attachments will be implemented in a future release.
{{< /note >}}

For example, suppose Alice uses $5 cash to pay off $5 of an IOU with Bob. This transaction contains a settlement command which reduces the amount outstanding on the IOU, and a payment command which changes the ownership of $5 from Alice to Bob. It also has two supporting attachments, and is notarized by `NotaryClusterA` if the notary pool receives it within the specified time window:

{{< 
  figure
	 width="50%"
	 src="full-tx.png"
	 figcaption="Transaction Backchain Example"
>}}

### Commands
Commands enable you to make adjustments to rules. Including a command in a transaction indicates the transaction’s intent, affecting how you check the validity of the transaction. For example, if you had a transaction with a cash state and a bond state as inputs, and a cash state and a bond state as outputs, it could represent either a bond purchase or a coupon payment on a bond. Different rules are required to define what constitutes a valid transaction depending on whether it is a purchase or a coupon payment. For example, in the case of a purchase, you would require a change in the bond’s current owner, but not for a coupon payment.

{{< 
  figure
	 width="50%"
	 src="commands.png"
	 figcaption="Commands"
>}}

### Time Windows

Each transaction requires a defined time window during which it can be approved and completed. The minimum requirement is an end date by which the transaction validation and notarization must be complete. You may also want a proposed transaction to be approved during a certain period of time. For example:

* An option that can only be exercised after a certain date.
* A bond that may only be redeemed before its expiry date.

This is enforced by adding a time window to the transaction, which specifies when the transaction can be committed. The notary enforces time window validity.

### Notary
Notaries provide uniqueness consensus by attesting that, for a given transaction, it has not already signed other transactions that consume any of the proposed transaction’s input states. This is the final check before a transaction is committed to the ledger.
Every transaction must be notarized, even if you are creating an issuance transaction that does not consume any other states and cannot double-spend, as this is required to enforce the time window validity. This allows for a much more efficient notary protocol where the notary tracks valid input states rather than spent states. For more information, see the [Notary section](notaries.html).