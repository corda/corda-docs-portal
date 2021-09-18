---
aliases:
- /head/key-concepts-transactions.html
- /HEAD/key-concepts-transactions.html
- /key-concepts-transactions.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-5:
    identifier: corda-os-4-5-key-concepts-transactions
    parent: corda-os-4-5-key-concepts
    weight: 1040
tags:
- concepts
- transactions
title: Transactions
---


# Transactions

# Summary

* *Transactions are proposals to update the ledger*
* *A transaction proposal will only be committed if:*
  * *It doesn’t contain double-spends*
  * *It is contractually valid*
  * *It is signed by the required parties*

## Video

{{% vimeo 213879807 %}}

## Overview

Corda uses a *UTXO* (unspent transaction output) model where every state on the ledger is immutable. The ledger
evolves over time by applying *transactions*. Transactions update the ledger by marking zero or more existing ledger states
as historic (the *inputs*), and producing zero or more new ledger states (the *outputs*). Transactions represent a
single link in the state sequences seen in [States](key-concepts-states.md).

Here is an example of an update transaction, with two inputs and two outputs:

![basic tx](/en/images/basic-tx.png "basic tx")
A transaction can contain any number of inputs, outputs and references of any type:

* They can include many different state types (states may represent cash or bonds, for example)
* They can be issuances (have zero inputs) or exits (have zero outputs)
* They can merge or split fungible assets (for example, they may combine a $2 state and a $5 state into a $7 cash state)

Transactions are *atomic*; either all of the transaction’s proposed changes are accepted, or none are.

There are two basic types of transactions:

* Notary-change transactions (used to change a state’s notary - see [Notaries](key-concepts-notaries.md))
* General transactions (used for everything else)

## Transaction chains

When creating a new transaction, the output states that the transaction proposes do not exist yet, and must
therefore be created by the proposer or proposers of the transaction. However, the input states already exist as the outputs of
previous transactions. We therefore include them in the proposed transaction by reference.

These input states references are a combination of:

* The hash of the transaction that created the input
* The input’s index in the outputs of the previous transaction

This situation can be illustrated as follows:

![tx chain](/en/images/tx-chain.png "tx chain")
These input state references link transactions together over time, forming what is known as a *transaction chain*.

## Committing transactions

Initially, a transaction is just a **proposal** to update the ledger. It represents the future state of the ledger
that is desired by the transaction builders:

![uncommitted tx](/en/images/uncommitted_tx.png "uncommitted tx")
To become reality, the transaction must receive signatures from all of the *required signers* (see **Commands**, below). Each
required signer appends their signature to the transaction to indicate that they approve the proposal:

![tx with sigs](/en/images/tx_with_sigs.png "tx with sigs")
If all of the required signatures are gathered, the transaction becomes committed:

![committed tx](/en/images/committed_tx.png "committed tx")
This means that:

* The transaction’s inputs are marked as historic, and cannot be used in any future transactions
* The transaction’s outputs become part of the current state of the ledger

## Transaction validity

Each required signer should only sign the transaction if the following two conditions hold:

* **Transaction validity**: For both the proposed transaction, and every transaction in the chain of transactions
that created the current proposed transaction’s inputs:>

  * The transaction is digitally signed by all the required parties
  * The transaction is *contractually valid* (see [Contracts](key-concepts-contracts.md))

* **Transaction uniqueness**: There exists no other committed transaction that has consumed any of the inputs to
our proposed transaction (see [Consensus](key-concepts-consensus.md))

If the transaction gathers all of the required signatures, but the preceding conditions do not hold, the transaction’s outputs
will not be valid and will not be accepted as inputs to subsequent transactions.

## Reference states

As mentioned in [States](key-concepts-states.md), some states need to be referred to by the contracts of other input or output
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

![full tx](/en/images/full-tx.png "full tx")

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

![commands](/en/images/commands.png "commands")

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

A notary pool is a network service that provides uniqueness consensus by attesting that, for a given transaction,
it has not already signed other transactions that consume any of the proposed transaction’s input states.
The notary pool provides the point of finality in the system.

Note that if the notary entity is absent then the transaction is not notarised at all. This is intended for
issuance/genesis transactions that don’t consume any other states and thus can’t double spend anything.
For more information on the notary services, see [Notaries](key-concepts-notaries.md).
