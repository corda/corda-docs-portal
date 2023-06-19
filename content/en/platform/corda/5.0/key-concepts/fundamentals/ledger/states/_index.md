---
title: "States"
date: 2023-06-08
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-fundamentals-ledger-states
    parent: corda5-fundamentals-ledger
    weight: 1000
section_menu: corda5
---

# States

States represent facts on the ledger. Facts evolve on the ledger when participants create new states and mark outdated states as consumed. Each participant has a [vault]({{< relref "../vault/_index.md">}}) where it stores the states it shares with other nodes.

A state is an immutable object representing a fact known by one or more participants at a specific point in time. You can use states to represent any type of data, and any kind of fact. For example, a financial instrument, Know Your Customer (KYC) data, or identity information.

For example, this state represents an IOU; an agreement that Alice owes Bob £10:

{{< 
  figure
	 src="state.png"
     width="50%"
	 figcaption="IOU State"
>}}

In addition to information about the fact, the state contains a reference to the contract. Contracts govern the evolution of states.

## State Sequences

States are immutable: you can not change them. Corda uses state sequences to track the evolution of facts. When a fact changes, one of the state’s participants creates a new state and marks the outdated state as consumed. To make a clear distinction, the latest, relevant state is called unconsumed.

For example, if Alice pays Bob £5, the state sequence would be:

{{< 
  figure
	 src="state-sequence.png"
     width="50%"
	 figcaption="IOU State Sequence"
>}}

Each participant's vault stores the current and consumed states in which it is invovled. For example:

{{< 
  figure
	 src="vault-simple.png"
     width="50%"
	 figcaption="Consumed and Unconsumed States in the Vault"
>}}

## Reference States
Not all states need to be updated by the participants that use them. One participant can create a state containing reference data. This state can be used, but not updated, by other parties. For this use case, the states containing reference data are referred to as reference states. Reference states are no different to regular states. However, they are handled differently in Corda transactions. For more information, see the [Transactions section]({{< relref "../transactions/_index.md#reference-states" >}}).