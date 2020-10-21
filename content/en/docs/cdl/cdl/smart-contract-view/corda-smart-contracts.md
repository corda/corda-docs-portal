---
title: Corda Smart Contracts
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-corda-smart-contracts"
    weight: 20

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
---


# Corda Smart Contracts

*Smart contract* is a term that is often used in the distributed ledger/ blockchain space but not often used in the context of discussing Corda. Corda has the building blocks of other blockchains' smart contracts, but they are chopped up and split into different parts:

* The data of a smart contract is stored in the `ContractState`s on ledger.
* The functions or things you can do to that data are defined in the Contract.
* The way which those functions are enacted is via building new transactions in the Flows which uses the states and conform to the Corda Contracts.

So it's all there, but not in a neat encapsulated package. This is an intended benefit because this approach leads to a great deal of flexibility. For example, the flows are not limited to enacting a transition on the Ledger, they are a powerful messaging framework which allows you to confidently send anything you like to counterparties.

For the purposes of CDL you will see how to define a Corda smart contract as the combination of one or more types of `ContractState` which are constrained by a Corda Contract. The flows are not included in this process as you can be agnostic as to how the transactions get built up: you only need to concern yourself with the validity of the final transaction.

So, Corda smart contracts are basically a combination of data (ContractStates) and what a party is permitted to do with it (Contracts).

As you follow these examples, when drawing a Smart Contract view diagram, you will always specify the `ContractState`(s) and the contract which will implement the behaviour we are articulating.
