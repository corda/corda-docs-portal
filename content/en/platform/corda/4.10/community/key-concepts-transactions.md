---
aliases:
- /head/key-concepts-transactions.html
- /HEAD/key-concepts-transactions.html
- /key-concepts-transactions.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-key-concepts-transactions
    parent: corda-community-4-10-key-concepts
    weight: 1040
tags:
- concepts
- transactions
title: Transactions
---


# Transactions

# Summary

* A transaction is a proposal to update the ledger. It is only committed to the ledger if it:
  * Doesn’t contain double-spends.
  * Is contractually valid.
  * Is signed by the required parties.

## Video

{{% vimeo 213879807 %}}

## Transactions on Corda

You can't edit the Corda ledger—the only way to change it is to add new transactions to it. A transaction updates the [ledger](key-concepts-ledger.md) by consuming existing [input states](key-concepts-states.md) and outputting new states. The states the transaction consumes are marked "historic".

Every [state](key-concepts-states.md) is *immutable*—it can't be changed. This is called an *UTXO* (unspent transaction output) model.

Here is an example of a transaction with two inputs and two outputs:

{{< figure alt="basic tx" width=80% zoom="/en/images/basic-tx.png" >}}
A transaction can contain any number of inputs, outputs and references of any type. Transactions can:

* Include different types of states representing multiple financial instruments, such as cash or bonds.
* *Issue* states, by creating a transaction without inputs. These states won't replace any existing states because none are marked "historic".
* *Exit* states, by creating transactions without outputs. This doesn't create any new states to replace the ones consumed.
* Merge or split fungible assets. For example, they may combine a $2 state and a $5 state into a $7 cash state.

Transactions are *atomic*. Either all of the transaction’s proposed changes are accepted, or none are.

There are two basic types of transactions:

* Notary-change transactions, to change a state’s [notary](key-concepts-notaries.md).
* General transactions, for everything else.

## Transaction backchains

Transaction backchains let a [node](key-concepts-node.md) verify that each input was generated from a valid series of transactions. This is called "walking the chain." If you need to break this chain (for example, because you want to increase performance by reducing the number of transactions the node has to check, or because you want to keep previous transactions private) you can [reissue states](reissuing-states.md).

Backchains are created as *input state references* linked together over time. Input state references let you use the outputs of previous transactions as the inputs of new transactions.

Input state references consist of:

* The [hash](https://www.investopedia.com/terms/h/hash.asp) of the transaction that created the input.
* The input’s index (location in the backchain) in the outputs of the previous transaction.

You can see how this works in this example transaction:

{{< figure alt="tx chain" width=80% zoom="/en/images/tx-chain.png" >}}


## Committing transactions to the ledger

Initially, a transaction is only a proposal to update the ledger. It represents the future state of the ledger desired by the transaction builders.

{{< figure alt="uncommitted tx" width=80% zoom="/en/images/uncommitted_tx.png" >}}
To be committed to the ledger, the transaction must receive signatures from all the *required signers*. Each
required signer appends their signature to the transaction to approve the proposal.

{{< figure alt="tx with sigs" width=80% zoom="/en/images/tx_with_sigs.png" >}}
If the transaction gathers the required signatures, it is committed:

{{< figure alt="committed tx" width=80% zoom="/en/images/committed_tx.png" >}}
This means that:

* The transaction’s inputs are marked as historic, and cannot be used in any future transactions.
* The transaction’s outputs become part of the current state of the ledger.

## Transaction validity

Just gathering the required signatures is not enough to commit a transaction to the ledger. It must also be:

* *Valid:* The proposed transaction and every transaction the backchain of the proposed inputs must be signed by all the required parties and [contractually valid](key-concepts-contracts.md).
* *Unique:* No other committed transaction has consumed any of the inputs to
the proposed transaction. [Uniqueness](key-concepts-consensus.html#uniqueness-consensus) is determined by a [notary](key-concepts-notaries.md).

If the transaction gathers all the required signatures without meeting these conditions, the transaction’s outputs
are not valid and will not be accepted as inputs to subsequent transactions.


## Reference states

Some states need to be referred to by the contracts of other input or output
states but not updated/consumed. This is where reference states come in. When a state is added to the references list of
a transaction, instead of the inputs or outputs list, it is treated as a *reference state*. There are two important
differences between regular states and reference states:

* The specified notary for the transaction **does** check whether the reference states are current. However, reference
states are not consumed when the transaction containing them is committed to the ledger.
* The contracts for reference states are not executed for the transaction containing them.

## Other transaction components

As well as input states and output states, transactions contain:

* Commands
* Attachments
* Time windows
* A notary

For example, suppose Alice uses $5 cash to pay off $5 of an IOU with Bob.
This transaction contains a *settlement command* which reduces the amount outstanding on the IOU, and a *payment command* which changes the ownership of $5 from Alice to Bob. It also has two supporting attachments, and is notarized by `NotaryClusterA` if the notary pool
receives it within the specified time window:

{{< figure alt="full tx" width=80% zoom="/en/images/full-tx.png" >}}

### Commands

{{% vimeo 213881538 %}}

If you had a transaction with a cash state and a bond state as inputs, and a cash state and a bond state as
outputs, it could represent either a bond purchase or a coupon payment on a bond.

You would need to impose different rules for what constitutes a valid transaction depending on whether
it is a purchase or a coupon payment. For example, in the case of a purchase, you would require a change in the bond’s
current owner, but not for a coupon payment.

You can make these adjustments to the rules using *commands*. Including a command in a transaction lets you indicate the transaction’s intent,
affecting how you check the validity of the transaction.

Each command is associated with a list of *signers*. By taking the union of all the public keys
listed in the commands, you get the list of the transaction’s required signers. In this example:

* In a coupon payment on a bond, only the owner of the bond needs to sign.
* In a cash payment, only the owner of the cash needs to sign.

This situation would look like this:

{{< figure alt="commands" width=80% zoom="/en/images/commands.png" >}}

### Attachments

{{% vimeo 213879328 %}}

You might have a large piece of data that can be reused for several transactions, such as:

* A calendar of public holidays.
* Supporting legal documentation.
* A table of currency codes.

You can achieve this with *attachments*. Transactions can refer to attachments by the attachment's [hash](https://www.investopedia.com/terms/h/hash.asp). These
attachments are `.zip` or JAR files with content that the node can use when verifying a [smart contract](key-concepts-contracts.md).

### Time windows

You may only want a proposed transaction to be approved during a certain period of time. For example:

* An option that can only be exercised after a certain date.
* A bond that may only be redeemed before its expiry date.

You can enforce this by adding a [time window](key-concepts-time-windows.md) to the transaction, which specifies when the
transaction can be committed. The [notary](key-concepts-notaries.md) enforces time window validity.

### Notary

[Notaries](key-concepts-notaries.md) provide [uniqueness consensus](key-concepts-consensus.md) by attesting that, for a given transaction, it has not already signed other transactions that consume any of the proposed transaction’s input states. This is the final check before a transaction is committed to the ledger.

You may not need to include a notary if you are creating an issuance transaction, because they do not consume any other states and cannot double-spend.
