---
aliases:
- /head/key-concepts-states.html
- /HEAD/key-concepts-states.html
- /key-concepts-states.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-states
    parent: corda-os-4-8-key-concepts
    weight: 1030
tags:
- concepts
- states
title: States
---


# States

## Summary

* States represent facts on the **[ledger](key-concepts-ledger.md)**.
* Facts evolve on the ledger when participants create new states and mark outdated states as historic.
* Each node has a vault where it stores the states it shares with other nodes.

## Video

{{% vimeo 213812054 %}}

## Overview

A state is an immutable object representing a fact known by one or more nodes at a specific point in time.
You can use states to represent any type of data, and any kind of fact. For example, a financial instrument, Know Your Customer (KYC) data, or identity information.

This state represents an IOU—an agreement that Alice owes Bob £10:

{{< figure alt="state" width=80% zoom="/en/images/state.png" >}}

In addition to information about the fact, the state contains a reference to the
**[contract](key-concepts-contracts.md)**. Contracts govern the evolution of states.

## State sequences

States are immutable: you can't change them. Corda uses **state sequences** to track the evolution of facts.
When a fact changes, one of the state's participants creates a new state and marks the outdated state as historic.

For example, if Alice pays Bob £5, the state sequence would be:

{{< figure alt="state sequence" width=80% zoom="/en/images/state-sequence.png" >}}

## The vault

Each node on the network maintains a **vault**. This is the node's database used to store current and historic states
where the node is a participant. For example:

{{< figure alt="vault simple" width=80% zoom="/en/images/vault-simple.png" >}}

From each node's point of view, the ledger is the current (non-historic) states where that node is a participant.

## Reference states

Not all states need to be updated by the parties which use them. In the case of reference data, one party can create
a state containing reference data. This state can be used (but not updated) by other parties. For this use-case, the
states containing reference data are referred to as **reference states**. Reference states are no different
to regular states. However, they are handled differently in Corda **[transactions](key-concepts-transactions.md)**.

## Reissuing states

Corda uses a state reissuance mechanism that allows you to break transaction backchains. Read about
**[reissuing states](reissuing-states.md)** with a guaranteed state replacement.
