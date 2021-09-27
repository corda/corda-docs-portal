---
title: "Contracts"
date: '2021-09-20'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-contracts
    weight: 1300
section_menu: corda-5-dev-preview
---

A **contract** governs the evolution of a <a href="key-concepts-states.md">**state**</a> over time and is used to
verify proposed <a href="key-concepts-transactions.md">**transactions**</a>.

### States in the Corda 5 Developer Preview

In the Corda 5 Developer Preview, the main principles of states, transactions, and contracts remain the same as they were
in Corda 4. However, as your CorDapp's external interactions are performed via HTTP-RPC REST APIs (and the node returns information
in the same way), when writing states you must add a `JsonRepresentable`.

## Transaction verification

A transaction is only valid if:
* It is digitally signed by all required signers.
* Each transaction state specifies a *contract* type.
* A contract takes a transaction as input and validates it based on its constraints.
* The contract of *every input state* and *every output state* considers it to be valid.

If a transaction does not meet these criteria, then it is not a valid proposal to update the ledger, and it will not be
committed to the ledger. Contracts impose rules on the evolution of states that are independent of the willingness of
the required signers to sign a given transactions.

The contract code has the ability to:

* Check the number of inputs, outputs, commands, and attachments.
* Check whether there is a time window or not.
* Check the contents of the transaction's components.
* Use looping constructs, variable assignment, function calls, helper methods, and so on.
* Group similar states to validate them as a group; for example, to impose a rule on the combined value of all the cash
states.

Transaction verification must be *deterministic*. A contract should either *always accept* or *always reject* a
given transaction. For example, transaction validity cannot depend on the time at which validation is conducted or
the amount of information the peer running the contract holds. This is a necessary condition to ensure that all peers
on the network reach consensus regarding the validity of a given ledger update.

## Contract limitations

Since a contract only has access to the information provided in a transaction, it can only check the transaction for internal
validity. It cannot check, for example, that the transaction is in accordance with what was originally agreed with the
counterparties.

Peers should therefore check the contents of a transaction before signing it, *even if the transaction is
contractually valid*, to see whether they agree with the proposed ledger update. A peer is under no obligation to
sign a transaction just because it is contractually valid. For example, they may be unwilling to take on a loan that
is too large, or may disagree on the amount of cash offered for an asset.

## Oracles

Sometimes, transaction validity may depend on external information, such as an exchange rate. In
these cases, an **Oracle** is required.

## Legal prose

Each contract refers to a *legal prose document* which details the rules governing the evolution of the state over
time in a way that is compatible with traditional legal systems. This document can be relied upon in the case of
legal disputes.
