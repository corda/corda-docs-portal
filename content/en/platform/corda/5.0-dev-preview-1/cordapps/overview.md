---
date: '2020-09-08T12:00:00Z'
title: "CorDapp references for developers"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-cordapps
    weight: 1100
project: corda-5
section_menu: corda-5-dev-preview
---
Use these resources to help build and locally deploy your own CorDapps using the Corda 5 Developer Preview. If you have not yet completed the tutorials section, and are looking for the best place to start, try the [Building a CorDapp tutorial](../tutorials/building-cordapp/c5-basic-cordapp-intro.md).

If you have completed the tutorials and want to experiment further, you can use these resources. Please keep in mind that the Corda 5 Developer Preview is for local deployment and testing only, and should not be used in a commercial setting.

## Overview of CorDapp development in the Corda 5 Developer Preview

Corda Distributed Applications (CorDapps) are applications that run on the Corda platform. They contain the business logic and functionality required to perform transactions between participants on a network - allowing agreement to be reached on updates to the ledger.

In the Corda 5 Developer Preview, you can follow step-by-step tutorials to create a simple CorDapp, including how to write:

* Flows. Flows are the actions your CorDapp can perform on a network and represent the business logic of your CorDapp. For example, if you are writing a CorDapp to enable the creation of an IOU, you may need to write flows that add the IOU to the network, update who has borrowed and who has lent money, record repayments, update contracts, and update the balance of the loan as the IOU is re-payed or moved to another party.

  If you are already familiar with developing on Corda, writing flows in the Corda 5 Developer Preview is likely to be the most substantial change. Contracts and states remain largely unchanged.

* Contracts. Contracts define rules that are used to verify transaction inputs and outputs. A CorDapp can have one or more contracts, and each contract defines rules for one or more states. The goal of a contract is to ensure that input and output states in transactions are valid and to prevent invalid transactions.

* States. In Corda, a contract state (or just ’state’) contains data used by a CorDapp. It can be thought of as a disk file that the CorDapp can use to persist data across transactions. States are immutable: once created they are never updated, instead, any changes must generate a new successor state. States can be updated (consumed) only once: the notary is responsible for ensuring there is no *double-spending* by only signing a transaction if the input states are all free.

## Corda Services and modular API

When building your CorDapps, you will make use of the suite of APIs, or [Corda Services](corda-services/overview.md), which can be injected into your flows and other Corda Services. In the Corda 5 Developer Preview, these APIs are modulated to enable you to build quickly, and only use the services your business logic requires.

You can also write your own [custom Corda Services](./corda-services/injectable-services.md).

## Changes from Corda 4

The most substantial changes in the way you create CorDapps are in the writing of flows. The `FlowLogic` abstract class used in Corda 4 has been broken up into a set of smaller interfaces. In place of `FlowLogic`, you should now implement the `Flow` interface which holds the `call` method you require.

The `progressTracker` has been removed, so you should use logging instead.

All methods that used to exist on the `FlowLogic` abstract class are now available as injectable services using property injection. An implementation of `FlowLogic` still exists to ease migration to Corda 5. It implements the `Flow` interface.

This move away from an abstract class to injectable services allows you, as a CorDapp developer, to use only what you need. Features that you don’t use do not need to be present on your flow classes.

Find out more about [writing flows](flows/writing-flows) before you get started.
