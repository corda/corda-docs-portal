---
title: "Transactions"
date: '2021-09-20'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-transactions
    weight: 1600
project: corda-5
section_menu: corda-5-dev-preview
---

The Corda 5 Developer Preview uses a *UTXO* (unspent transaction output) model, where every state on the ledger is immutable. The ledger
evolves over time by applying **transactions**. Transactions update the ledger by marking zero or more existing ledger states
as historic (the *inputs*), and producing zero or more new ledger states (the *outputs*). Transactions represent a
single link in the state sequences as described in **[states](key-concepts-states.md)**.

### States in the Corda 5 Developer Preview

In the Corda 5 Developer Preview, the main principles of states, transactions, and contracts remain the same as they were
in Corda 4. However, as your CorDapp's external interactions are performed via HTTP-RPC REST APIs (and the node returns information
in the same way), when writing states you must add a `JsonRepresentable`.

## Transaction components and types

Here's an example of a transaction, with two inputs and two outputs:

{{< figure alt="basic tx" width=80% zoom="/en/images/basic-tx.png" >}}

A transaction can contain any number of inputs, outputs, and references. They can:

* Include different state types. States may represent cash or bonds, for example.
* Be issuances (have no inputs) or exits (have no outputs).
* Merge or split fungible assets. For example, they may combine a $2 state and a $5 state into a $7 state.

Transactions are *atomic*; either all of the transaction’s proposed changes are accepted, or none are.

There are two basic types of transactions:

* Notary-change transactions, which are used to change a state’s **Notary**.
* General transactions, which are used for everything else.

## Transaction chains

When you create a new transaction, you need to propose output states as these don't yet exist. Input
states are outputs of previous transactions, and you include them by adding their reference.

Input state references are a combination of:

* The hash of the transaction that created the input.
* The input’s index in the outputs of the previous transaction.

These input state references link transactions together, forming a *transaction chain*:

{{< figure alt="tx chain" width=80% zoom="/en/images/tx-chain.png" >}}

## Committing transactions

Initially, a transaction is just a *proposal* to update the ledger. It represents the future state of the ledger
that is desired by the transaction builders:

{{< figure alt="uncommitted tx" width=80% zoom="/en/images/uncommitted_tx.png" >}}

To become reality, the transaction must receive signatures from all *required signers*
(see **[commands](#commands)**). Each required signer appends their signature to the transaction to indicate that
they accept the proposal:

{{< figure alt="tx with sigs" width=80% zoom="/en/images/tx_with_sigs.png" >}}

If all required signatures are gathered, the transaction becomes committed:

{{< figure alt="committed tx" width=80% zoom="/en/images/committed_tx.png" >}}

This means that the transaction's:

* Inputs are marked as historic, and cannot be used in any future transactions.
* Outputs become part of the current state of the ledger.

## Transaction validity

Signers should only sign the transaction if these conditions are met:

* **Transaction validity**
  * Transactions in the transaction chain are digitally signed by all the required parties.
  * The proposed transaction is **[contractually valid](key-concepts-contracts.md)**.

* **Transaction uniqueness**. There exists no other committed transaction that has consumed any of the inputs to
the proposed transaction.

If the transaction gathers all required signatures, but the preceding conditions are not met, the transaction’s outputs
will not be valid and will not be accepted as inputs to subsequent transactions.

## Reference states

Not all states need to be updated by the parties that use them. In the case of reference data, a party creates it,
and it is then used (but not updated) by other parties. For this use-case, the
states containing reference data are referred to as **reference states**. Syntactically, reference states are no different
than regular states. However, they are treated differently by Corda transactions.

There are two important differences between regular states and reference states:

* Notaries *do* check whether a reference state is current. However, reference
states are not consumed when the transaction containing them is committed to the ledger.
* The contracts for reference states are not executed for the transaction containing them.

## Other transaction components

As well as input states and output states, transactions contain:

* Commands
* Attachments
* A time-window
* A notary

For example, a transaction where Alice uses a £5 cash payment to pay off £5 of an IOU with Bob comprises two commands:
* A settlement command which reduces the amount outstanding on the IOU.
* A payment command which changes the ownership of £5 from Alice to Bob.

It also has two supporting attachments, and will only be notarised by NotaryClusterA if the notary pool
receives it within the specified time-window. This transaction would look like:

{{< figure alt="full tx" width=80% zoom="/en/images/full-tx.png" >}}

### Commands

Suppose a transaction has a cash state and a bond state as inputs, and a cash state and a bond state as
outputs. This transaction could represent two different scenarios:

* A bond purchase.
* A coupon payment on a bond.

Different rules and constraints are likely to apply depending on whether this is a purchase or a coupon payment.
For example, in the case of a purchase, there would be a change in the bond’s
current owner. Whereas in the case of a coupon payment, the ownership of the bond would not change.

**Commands** are included in a transaction to indicate the transaction’s intent,
affecting how the transaction is validated.

Each command is also associated with a list of one or more **signers**. By taking the union of all the public keys
listed in the commands, you get the list of the transaction’s required signers. In this example, it could be that:

* In a coupon payment on a bond, only the owner of the bond is required to sign.
* In a cash payment, only the owner of the cash is required to sign.

Here's a visualization of this example.

{{< figure alt="commands" width=80% zoom="/en/images/commands.png" >}}

### Attachments

A large piece of data may need to be reused across multiple transactions. For example:

* A calendar of public holidays.
* Supporting legal documentation.
* A table of currency codes.

In these instances, use an **attachment**. Each transaction can refer to zero or more attachments by hash. These
attachments are `.zip`/`.jar` files containing arbitrary content. The information in these files can then be
used when checking the transaction’s validity.

### Time-window

In some cases, a proposed transaction must be approved during a certain time-window. For example:

* An option can only be exercised after a certain date.
* A bond may only be redeemed before its expiry date.

In such cases, you can add a *time-window* to the transaction. Time-windows specify the time period during which the
transaction can be committed. The notary pool enforces time-window validity.

### Notary

A notary pool is a network service that provides uniqueness consensus by attesting that, for a given transaction,
it has not already signed other transactions that consume any of the proposed transaction’s input states.
The notary pool provides the point of finality in the system.

If the notary entity is absent, then the transaction is not notarised at all. This is intended for
issuance/genesis transactions that don’t consume any other states, where there is no possibility of double spend.
