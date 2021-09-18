---
date: '2020-09-08T12:00:00Z'
title: "CorDapps"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-cordapps
    weight: 1100
project: corda-5
section_menu: corda-5-dev-preview
---

# CorDapp guides and references for developers

Use these resources to help build and locally deploy your own CorDapps using the Corda 5 Developer Preview. If you have not yet completed the tutorials section, and are looking for the best place to start, try the [Build your own CorDapp tutorial](../tutorials/building-cordapp).

If you have completed the tutorials and want to experiment further, you can use these docs. Please keep in mind that the dev preview is for local deployment and testing only, and should not be used in a commercial setting.

## Overview of CorDapps in Corda 5 Dev Preview

CorDapps(Corda Distributed Applications) are applications that run on the Corda platform. They contain the business logic and functionality required to perform transactions between participants on a network - allowing agreement to be reached on updates to the ledger.

In Corda 5 Dev Preview, your CorDapps are structured to contain:

* Flows. Flows are the actions your CorDapp can perform on a network - they represent the business logic of your CorDapp. For example, if you are writing a CorDapp to enable the creation of an IOU, you may need write flows that add the IOU to the network, update who has borrowed and who has lent money, record repayments, update contracts, and update the balance of the loan as the IOU is repayed or moved to another party.

If you are already familiar with developing on Corda, writing flows in Corda 5 Dev Preview is likely to be the most substantial change. Contracts and States remain largely unchanged.

* Contracts. Contracts define rules that are used to verify transaction inputs and outputs. A CorDapp can have one more contracts, and each contract defines rules for one or more states. The goal of a contract is to ensure that input and output states in transactions are valid and to prevent invalid transactions.

* States. In Corda, a contract state (or just ‘state’) contains data used by a CorDapp. It can be thought of as a disk file that the CorDapp can use to persist data across transactions. States are immutable: once created they are never updated, instead, any changes must generate a new successor state. States can be updated (consumed) only once: the notary is responsible for ensuring there is no “double spending” by only signing a transaction if the input states are all free.

## Corda Services and modular API

When building your CorDapps, you will use the suite of APIs, or Corda Services, which can be injected into your flows. In Corda 5 Dev Preview, these APIs are modulated to enable you to build quickly, and only use the services your business logic requires. 
