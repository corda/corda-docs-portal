---
aliases:
- /releases/release-V2.0/cordapp-overview.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-2-0:
    identifier: corda-os-2-0-cordapp-overview
    parent: corda-os-2-0-building-a-cordapp-index
    weight: 1010
tags:
- cordapp
- overview
title: What is a CorDapp?
---


# What is a CorDapp?

CorDapps (Corda Distributed Applications) are distributed applications that run on the Corda platform. The goal of a
CorDapp is to allow nodes to reach agreement on updates to the ledger. They achieve this goal by defining flows that
Corda node owners can invoke through RPC calls:

![node diagram](/en/images/node-diagram.png "node diagram")
CorDapps are made up of the following key components:


* States, defining the facts over which agreement is reached (see [Key Concepts - States](key-concepts-states.md))
* Contracts, defining what constitutes a valid ledger update (see
[Key Concepts - Contracts](key-concepts-contracts.md))
* Services, providing long-lived utilities within the node
* Serialisation whitelists, restricting what types your node will receive off the wire

Each CorDapp is installed at the level of the individual node, rather than on the network itself. For example, a node
owner may choose to install the Bond Trading CorDapp, with the following components:


* A `BondState`, used to represent bonds as shared facts on the ledger
* A `BondContract`, used to govern which ledger updates involving `BondState` states are valid
* Three flows: 

    * An `IssueBondFlow`, allowing new `BondState` states to be issued onto the ledger
    * A `TradeBondFlow`, allowing existing `BondState` states to be bought and sold on the ledger
    * An `ExitBondFlow`, allowing existing `BondState` states to be exited from the ledger




After installing this CorDapp, the node owner will be able to use the flows defined by the CorDapp to agree ledger
updates related to issuance, sale, purchase and exit of bonds.

