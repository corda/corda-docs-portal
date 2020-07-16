---
aliases:
- /releases/release-V4.0/cordapp-overview.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-cordapp-overview
    parent: corda-os-4-0-building-a-cordapp-index
    weight: 1010
tags:
- cordapp
- overview
title: What is a CorDapp?
---


# What is a CorDapp?

CorDapps (Corda Distributed Applications) are distributed applications that run on the Corda platform. The goal of a
CorDapp is to allow nodes to reach agreement on updates to the ledger. They achieve this goal by defining flows that
Corda node owners can invoke over RPC:

![node diagram](/en/images/node-diagram.png "node diagram")

## CorDapp components

CorDapps take the form of a set of JAR files containing class definitions written in Java and/or Kotlin.

These class definitions will commonly include the following elements:


* Flows: Define a routine for the node to run, usually to update the ledger
(see [Key Concepts - Flows](key-concepts-flows.md)). They subclass `FlowLogic`
* States: Define the facts over which agreement is reached (see [Key Concepts - States](key-concepts-states.md)).
They implement the `ContractState` interface
* Contracts, defining what constitutes a valid ledger update (see
[Key Concepts - Contracts](key-concepts-contracts.md)). They implement the `Contract` interface
* Services, providing long-lived utilities within the node. They subclass `SingletonSerializationToken`
* Serialisation whitelists, restricting what types your node will receive off the wire. They implement the
`SerializationWhitelist` interface

But the CorDapp JAR can also include other class definitions. These may include:


* APIs and static web content: These are served by Corda’s built-in webserver. This webserver is not
production-ready, and should be used for testing purposes only
* Utility classes


## An example

Suppose a node owner wants their node to be able to trade bonds. They may choose to install a Bond Trading CorDapp with
the following components:


* A `BondState`, used to represent bonds as shared facts on the ledger
* A `BondContract`, used to govern which ledger updates involving `BondState` states are valid
* Three flows: 

    * An `IssueBondFlow`, allowing new `BondState` states to be issued onto the ledger
    * A `TradeBondFlow`, allowing existing `BondState` states to be bought and sold on the ledger
    * An `ExitBondFlow`, allowing existing `BondState` states to be exited from the ledger




After installing this CorDapp, the node owner will be able to use the flows defined by the CorDapp to agree ledger
updates related to issuance, sale, purchase and exit of bonds.

