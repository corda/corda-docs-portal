---
aliases:
- /head/key-concepts-contracts.html
- /HEAD/key-concepts-contracts.html
- /key-concepts-contracts.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-contracts
    parent: corda-os-4-8-key-concepts
    weight: 1050
tags:
- concepts
- contracts
title: Contracts
---


# Contracts

## Summary

* *A transaction is contractually valid if all of its input and output states are acceptable according to the contract.*
* *Contracts are written in Java or Kotlin.*
* *Contract execution is deterministic, and transaction acceptance is based on the transaction’s contents alone.*

## Video

{{% vimeo 214168839 %}}

{{< note >}}
See [Reissuing states](reissuing-states.md) for information about reissuing states with a guaranteed state replacement, which allows you to break transaction backchains.
{{< /note >}}

## Transaction verification

Recall that a transaction is only valid if it is digitally signed by all required signers. However, even if a
transaction gathers all the required signatures, it is only valid if it is also **contractually valid**.

**Contract validity** is defined as follows:

* Each transaction state specifies a *contract* type
* A *contract* takes a transaction as input, and states whether the transaction is considered valid based on the
contract’s rules
* A transaction is only valid if the contract of **every input state** and **every output state** considers it to be
valid

We can picture this situation as follows:

{{< figure alt="tx validation" width=80% zoom="/en/images/tx-validation.png" >}}
The contract code has access to the full capabilities of the language,
including:

* Checking the number of inputs, outputs, commands, or attachments
* Checking whether there is a time window or not
* Checking the contents of any of these components
* Looping constructs, variable assignment, function calls, helper methods, and so on
* Grouping similar states to validate them as a group; for example, imposing a rule on the combined value of all the cash
states

A transaction that is not contractually valid is not a valid proposal to update the ledger, and thus can never be
committed to the ledger. In this way, contracts impose rules on the evolution of states over time that are
independent of the willingness of the required signers to sign a given transaction.

## The contract sandbox

Transaction verification must be *deterministic* - a contract should either **always accept** or **always reject** a
given transaction. For example, transaction validity cannot depend on the time at which validation is conducted, or
the amount of information the peer running the contract holds. This is a necessary condition to ensure that all peers
on the network reach consensus regarding the validity of a given ledger update.

Future versions of Corda will evaluate transactions in a strictly deterministic sandbox. The sandbox has a whitelist that
prevents the contract from importing libraries that could be a source of non-determinism. This includes libraries
that provide the current time, random number generators, libraries that provide file system access or networking
libraries, for example. Ultimately, the only information available to the contract when verifying the transaction is
the information included in the transaction itself.

**Tip:** Developers can pre-verify that their CorDapps are deterministic by linking their CorDapps against the deterministic modules
(see the [Deterministic Corda Modules](deterministic-modules.md)).

## Contract limitations

Since a contract has no access to information from the outside world, it can only check the transaction for internal
validity. It cannot check, for example, that the transaction is in accordance with what was originally agreed with the
counterparties.

Peers should therefore check the contents of a transaction before signing it, *even if the transaction is
contractually valid*, to see whether they agree with the proposed ledger update. A peer is under no obligation to
sign a transaction just because it is contractually valid. For example, they may be unwilling to take on a loan that
is too large, or may disagree on the amount of cash offered for an asset.

## Oracles

Sometimes, transaction validity will depend on some external piece of information, such as an exchange rate. In
these cases, an oracle is required. See [Oracles](key-concepts-oracles.md) for further details.

## Legal prose

{{% vimeo 213879293 %}}

Each contract also refers to a legal prose document that states the rules governing the evolution of the state over
time in a way that is compatible with traditional legal systems. This document can be relied upon in the case of
legal disputes.

## Encumbrances

All contract states can be *encumbered* by up to one other state. This is called an **encumbrance**. The encumbrance reference is optional in the `ContractState` interface.

The encumbrance state, if present, forces additional controls over the encumbered state, since the encumbrance state
contract will also be verified during the execution of the transaction. For example, a contract state could be
encumbered with a time-lock contract state; the state is then only processable in a transaction that verifies that the
time specified in the encumbrance time-lock has passed.

The encumbered state refers to its encumbrance by index, and the referred encumbrance state is an output state in a
particular position on the same transaction that created the encumbered state. Note that an encumbered state that is
being consumed must have its encumbrance consumed in the same transaction, otherwise the transaction is not valid.

When you construct a transaction that generates the encumbered state, you must place the encumbrance in the corresponding output
position of that transaction. And when you subsequently consume that encumbered state, the same encumbrance state must be
available somewhere within the input set of states.

See an example of an encumbrance in the <a href="https://github.com/corda/reissue-cordapp/blob/master/contracts/src/main/kotlin/com/r3/corda/lib/reissuance/contracts/ReissuanceLockContract.kt">`ReissuanceLockContract`</a> and <a href="https://github.com/corda/reissue-cordapp/blob/master/workflows/src/main/kotlin/com/r3/corda/lib/reissuance/flows/ReissueStates.kt">`ReissueStatesFlow`</a> of the [Reissuance CorDapp](https://github.com/corda/reissue-cordapp).
