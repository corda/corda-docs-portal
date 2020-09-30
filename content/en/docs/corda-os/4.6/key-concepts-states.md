---
aliases:
- /head/key-concepts-states.html
- /HEAD/key-concepts-states.html
- /key-concepts-states.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-key-concepts-states
    parent: corda-os-4-6-key-concepts
    weight: 1030
tags:
- concepts
- states
title: States
---


# States

## Summary

* *States represent on-ledger facts*
* *States are evolved by marking the current state as historic and creating an updated state*
* *Each node has a vault where it stores any relevant states to itself*

## Video

{{% vimeo 213812054 %}}

## Overview

A *state* is an immutable object representing a fact known by one or more Corda nodes at a specific point in time.
States can contain arbitrary data, allowing them to represent facts of any kind (e.g. stocks, bonds, loans, KYC data,
identity information…).

For example, the following state represents an IOU - an agreement that Alice owes Bob an amount X:

{{< figure alt="state" zoom="/en/images/state.png" >}}
Specifically, this state represents an IOU of £10 from Alice to Bob.

As well as any information about the fact itself, the state also contains a reference to the *contract* that governs
the evolution of the state over time. We discuss contracts in [Contracts](key-concepts-contracts.md).

## State sequences

As states are immutable, they cannot be modified directly to reflect a change in the state of the world.

Instead, the lifecycle of a shared fact over time is represented by a **state sequence**. When a state needs to be
updated, we create a new version of the state representing the new state of the world, and mark the existing state as
historic.

This sequence of state replacements gives us a full view of the evolution of the shared fact over time. We can
picture this situation as follows:

{{< figure alt="state sequence" zoom="/en/images/state-sequence.png" >}}

## The vault

Each node on the network maintains a *vault* - a database where it tracks all the current and historic states that it
is aware of, and which it considers to be relevant to itself:

{{< figure alt="vault simple" zoom="/en/images/vault-simple.png" >}}
We can think of the ledger from each node’s point of view as the set of all the current (i.e. non-historic) states that
it is aware of.

## Reference states

Not all states need to be updated by the parties which use them. In the case of reference data, there is a common pattern
where one party creates reference data, which is then used (but not updated) by other parties. For this use-case, the
states containing reference data are referred to as “reference states”. Syntactically, reference states are no different
to regular states. However, they are treated different by Corda transactions. See [Transactions](key-concepts-transactions.md) for
more details.
