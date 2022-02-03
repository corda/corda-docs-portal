---
aliases:
- /head/key-concepts-transactions.html
- /HEAD/key-concepts-transactions.html
- /key-concepts-transactions.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-transactions
    parent: corda-os-4-8-key-concepts
    weight: 1040
tags:
- concepts
- transactions
title: Transactions
---


# Transactions

# Summary

* Transactions are proposals to update the ledger.
* A transaction proposal is only committed to the ledger it:
  * Ioesn’t contain double-spends.
  * It is contractually valid.
  * It is signed by the required parties.

## Video

{{% vimeo 213879807 %}}

## Overview

Transactions update the [ledger](key-concepts-ledger.md) by consuming [states](key-concepts-states.md) and creating new ones. You can't edit the ledger—the only way to change it is to add new transactions to it.

A transaction consists of [states](key-concepts-states.md), commands, [attachments](https://docs.r3.com/en/tutorials/corda/4.8/os/supplementary-tutorials/tutorial-attachments.html), and a [time window](key-concepts-time-windows.md).

Every [state](key-concepts-states.md) is *immutable*—it can't be changed. This is called an *UTXO* (unspent transaction output) model. Transactions update the ledger by marking zero or more existing ledger states "historic" (the *inputs*), and producing zero or more new ledger states (the *outputs*).

Here is an example of a transaction with two inputs and two outputs:

{{< figure alt="basic tx" width=80% zoom="/en/images/basic-tx.png" >}}
A transaction can contain any number of inputs, outputs and references of any type. Transactions can:

* Include different types of states representing multiple financial instruments, such as cash or bonds.
* *Issue* states, by creating a transaction without inputs. These states won't replace any existing states because none are marked "historic".
* *Exit* states, by creating transactions without outputs. This doesn't create any new states to replace existing ones.
* Merge or split fungible assets. For example, they may combine a $2 state and a $5 state into a $7 cash state.

Transactions are *atomic*. Either all of the transaction’s proposed changes are accepted, or none are.

There are two basic types of transactions:

* Notary-change transactions, to change a state’s [notary](key-concepts-notaries.md).
* General transactions, for everything else.

## Transaction backchains

Transaction backchains let a [node](key-concepts-node.md) verify that each input was generated from a valid series of transactions. This is called "walking the chain." If you need to break this chain (for example, because you want to increase performance by reducing the number of transactions the node has to check, or because you want to keep previous transactions private) you can [reissue states](reissuing-states.md).

Backchains are created as *input state references* link together over time. Input state references let you use the outputs of previous transactions as the inputs of new transactions.

Input state references consist of:

* The [hash](https://www.investopedia.com/terms/h/hash.asp) of the transaction that created the input.
* The input’s index (location in the backchain) in the outputs of the previous transaction.

You can see how this works in this example transaction:

{{< figure alt="tx chain" width=80% zoom="/en/images/tx-chain.png" >}}


## Committing transactions to the ledger

Initially, a transaction is just a proposal to update the ledger. It represents the future state of the ledger
that is desired by the transaction builders:

{{< figure alt="uncommitted tx" width=80% zoom="/en/images/uncommitted_tx.png" >}}
To become reality, the transaction must receive signatures from all of the *required signers*. Each
required signer appends their signature to the transaction to indicate that they approve the proposal:

{{< figure alt="tx with sigs" width=80% zoom="/en/images/tx_with_sigs.png" >}}
If all of the required signatures are gathered, the transaction becomes committed:

{{< figure alt="committed tx" width=80% zoom="/en/images/committed_tx.png" >}}
This means that:

* The transaction’s inputs are marked as historic, and cannot be used in any future transactions.
* The transaction’s outputs become part of the current state of the ledger.

## Transaction validity

Just gathering the required signatures is not enough to commit a transaction to the ledger. It must also be:

* *Valid*. The proposed transaction and every transaction the backchain of the proposed inputs must be signed by all the required parties and [contractually valid](key-concepts-contracts.md).
* *Unique*: No other committed transaction has consumed any of the inputs to
the proposed transaction. [Uniqueness](key-concepts-consensus.md#uniqueness-consensus) is determined by a [notary](key-concepts-notaries.md).

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
* Time-Window
* Notary

For example, suppose we have a transaction where Alice uses a £5 cash payment to pay off £5 of an IOU with Bob.
This transaction comprises two commands: a settlement command which reduces the amount outstanding on the IOU, and a payment command which changes the ownership of £5 from Alice to Bob. It also
has two supporting attachments, and will only be notarised by NotaryClusterA if the notary pool
receives it within the specified time-window. This transaction would look as follows:

{{< figure alt="full tx" width=80% zoom="/en/images/full-tx.png" >}}

### Commands

{{% vimeo 213881538 %}}

Suppose we have a transaction with a cash state and a bond state as inputs, and a cash state and a bond state as
outputs. This transaction could represent two different scenarios:

* A bond purchase
* A coupon payment on a bond

We can imagine that we’d want to impose different rules on what constitutes a valid transaction depending on whether
this is a purchase or a coupon payment. For example, in the case of a purchase, we would require a change in the bond’s
current owner, whereas in the case of a coupon payment, we would require that the ownership of the bond does not
change.

For this, we have *commands*. Including a command in a transaction allows us to indicate the transaction’s intent,
affecting how we check the validity of the transaction.

Each command is also associated with a list of one or more *signers*. By taking the union of all the public keys
listed in the commands, we get the list of the transaction’s required signers. In our example, we might imagine that:

* In a coupon payment on a bond, only the owner of the bond is required to sign
* In a cash payment, only the owner of the cash is required to sign

We can visualize this situation as follows:

{{< figure alt="commands" width=80% zoom="/en/images/commands.png" >}}

### Attachments

{{% vimeo 213879328 %}}

Sometimes, we have a large piece of data that can be reused across many different transactions. Some examples:

* A calendar of public holidays
* Supporting legal documentation
* A table of currency codes

For this use case, we have *attachments*. Each transaction can refer to zero or more attachments by hash. These
attachments are ZIP/JAR files containing arbitrary content. The information in these files can then be
used when checking the transaction’s validity.

### Time-window

In some cases, we want a proposed transaction to only be approved during a certain time-window. For example:

* An option can only be exercised after a certain date
* A bond may only be redeemed before its expiry date

In such cases, we can add a *time-window* to the transaction. Time-windows specify the time period during which the
transaction can be committed. The notary pool enforces time-window validity. We discuss time-windows in the section on [Time-windows](key-concepts-time-windows.md).

### Notary

A notary pool is a network service that provides uniqueness consensus by attesting that, for a given transaction, it has not already signed other transactions that consume any of the proposed transaction’s input states. The notary pool provides the point of finality in the system.

Note that if the notary entity is absent then the transaction is not notarised at all. This is intended for
issuance/genesis transactions that don’t consume any other states and thus can’t double spend anything.
For more information on the notary services, see [Notaries](key-concepts-notaries.md).
