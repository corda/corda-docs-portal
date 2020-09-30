---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-cordapps
    name: "Developing CorDapps"
tags:
- cordapp
- overview
title: What is a CorDapp?
weight: 20
---


# What is a CorDapp?

CorDapps (Corda Distributed Applications) are distributed applications that run on the Corda platform. The goal of a
CorDapp is to allow nodes to reach agreement on updates to the ledger. They achieve this goal by defining flows that
Corda node owners can invoke over RPC:

{{< figure alt="node diagram" zoom="../resources/node-diagram.png" >}}

## CorDapp components

CorDapps take the form of a set of JAR files containing class definitions written in Java and/or Kotlin.

These class definitions will commonly include the following elements:



* Flows
* States
* Contracts
* Services
* Serialization whitelists


But may also include:



* APIs and static web content
* Utility classes


Flows are routines for nodes to run. They can perform a variety of tasks, but usually involve ledger updates. Flows
subclass `FlowLogic`. For more information on flows, see [Writing CorDapp Flows](api-flows.md).

States define the facts that parties agree and transact over. States implement the `ContractState` interface. For more
information on states, see [Writing CorDapp States](api-states.md).

Contracts define the shared rules for updating the ledger. Contracts implement the `Contract` interface``. To learn
more about implementing contracts, see [Writing CorDapp Contracts](api-contracts.md).

Services are intended to provide long-lived utilities that don’t need to run on the network. Services subclass `SingletonSerializationToken`

Serialization whitelists restrict the objects a node can deserialize when being sent messages from other nodes.
Serialization whitelists implement the `SerializationWhitelist` interface.


## An example CorDapp

In this example, we’ll go over the components of a CorDapp designed to trade bonds. This CorDapp would be deployed by all
Node owners wishing to establish a business network to trade bonds.

There are several components required for the minimum implementation of this CorDapp. First are the three required flows:


* An issuance flow, for example `IssueBondFlow`, to allow new bonds to be issued onto the ledger
* A bond trading flow, `TradeBondFlow`, where bonds already issued can be exchanged between parties
* An exit flow, `ExitBondFlow` where bonds can be exited from the ledger

These three flows allow for a basic lifecycle of bond creation, trading, and exiting between the transacting parties.
However, there are several more components that are required in order to implement this CorDapp:


* A state must be created to represent the bonds, `BondState`, this state is what will be issued, traded, and exited by the flows
* A `BondContract` must also be created to define the rules defining valid transactions

Each node owner will install this CorDapp onto their node, and can then issue, trade, and exit bonds with other node owners.

