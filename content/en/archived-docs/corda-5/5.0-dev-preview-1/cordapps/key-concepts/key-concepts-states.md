---
title: "States"
date: '2021-09-20'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-states
    weight: 1350
section_menu: corda-5-dev-preview
expiryDate: '2022-09-28'
---

A **state** is an immutable object representing a fact known by one or more Corda nodes at a specific point in time.
States can contain arbitrary data, allowing them to represent facts of any kind, such as, stocks, bonds, loans, KYC data,
and identity information.

For example, this state represents an IOU—an agreement that Alice owes Bob £5:

{{< figure alt="state" width=80% zoom="/en/images/state.png" >}}

As well as any information about the fact itself, the state also contains a reference to
the <a href="key-concepts-contracts.md">**contract**</a> that governs the evolution of the state over time.

### States in the Corda 5 Developer Preview

In the Corda 5 Developer Preview, the main principles of states, transactions, and contracts remain the same as they were
in Corda 4. However, as your CorDapp's external interactions are performed via HTTP-RPC REST APIs (and the node returns information
in the same way), when writing states you must add a `JsonRepresentable`.

## State sequences

As states are immutable, they cannot be modified directly to reflect a change to a shared fact. Instead, the lifecycle
of a shared fact over time is represented by a **state sequence**. When a shared fact changes, you must create a new
version of the state (which represents the updated fact) and mark the existing state as historic. See **[transactions](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-transactions.md)** for more information.

This sequence of state replacements gives you a full view of the evolution of the shared fact over time:

{{< figure alt="state sequence" width=80% zoom="/en/images/state-sequence.png" >}}

## The vault

Each node on the network maintains a **vault**—a database which tracks all the current and historic states that the node
is aware of and considers to be relevant (to itself):

{{< figure alt="vault simple" width=80% zoom="/en/images/vault-simple.png" >}}

The **ledger** is all the current (non-historic) states that a particular node is aware of.

## Reference states

Not all states need to be updated by the parties which use them. In the case of reference data, a party creates it,
and it is then used (but not updated) by other parties. For this use-case, the
states containing reference data are referred to as **reference states**. Syntactically, reference states are no different
to regular states. However, they are treated differently by Corda transactions. See [transactions](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-transactions.md) for
more details.

## Reissuing states

You can break transaction backchains by reissuing states with a guaranteed state replacement.
