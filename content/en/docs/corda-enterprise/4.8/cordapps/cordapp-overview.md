---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-cordapps
    name: "Developing CorDapps"
tags:
- cordapp
- overview
title: What is a CorDapp?
weight: 20
---

This document:

* Explains what a CorDapp is and what it does
* Defines CorDapp components and their functions
* Gives an example of a CorDapp, so you can see how the components work together

# What is a CorDapp?

Corda Distributed Applications (CorDapps) are apps that are stored and executed on the Corda platform. This *distributes* the app, allowing it to run on multiple systems simultaneously—unlike traditional apps, which utilize one dedicated system to achieve an assigned task. CorDapps let nodes communicate with each other to reach agreement on updates to the ledger by defining flows that Corda node owners can invoke over RPC:

{{< figure alt="node diagram" zoom="../resources/node-diagram.png" >}}

## Glossary

*Flows*
  FLows are routines for nodes to run. They can perform a variety of tasks, usually involving ledger updates. Flows
  subclass `FlowLogic`. For more information on flows, see [Writing CorDapp Flows](api-flows.md).

*States*
  States define the facts that parties use to agree and transact. States implement the `ContractState` interface. For more
  information on states, see [Writing CorDapp States](api-states.md).

*Contracts*
  Contracts define the shared rules for updating the ledger. Contracts implement the `Contract` interface. To learn
  more about implementing contracts, see [Writing CorDapp Contracts](api-contracts.md).

*Services*
  Services provide long-lived utilities that don’t need to run on the network. Services subclass `SingletonSerializationToken`.

*Serialization whitelists*
  Serialization whitelists restrict the objects a node can deserialize when it receives messages from other nodes.
  Serialization whitelists implement the `SerializationWhitelist` interface.


## CorDapp components

CorDapps are a set of `.jar` files containing class definitions written in Java and/or Kotlin. These definitions function as a blueprint or prototype from which objects are created. It represents the set of properties or methods that are common to all objects of one type.

These class definitions usually include:

* Flows
* States
* Contracts
* Services
* Serialization whitelists

These components work together to let the CorDapp communicate with other nodes and reach an agreement. If the transactions the node processes require additional functionality, it may also include:

* APIs and static web content
* Utility classes


## An example CorDapp

In this example, we’ll examine the components of a CorDapp designed to trade bonds. This CorDapp would be deployed by all
node owners wishing to establish a business network to trade bonds.

There are several components required for the minimum implementation of this CorDapp. First are the three required flows:

* An *issuance flow*, for example `IssueBondFlow`, to allow new bonds to be issued onto the ledger
* A *bond trading flow*, `TradeBondFlow`, where bonds already issued can be exchanged between parties
* An *exit flow*, `ExitBondFlow` where bonds can be exited from the ledger

These three flows enable a basic lifecycle of bond creation, trading, and exiting between the transacting parties.
However, we must create two more components to implement this CorDapp:

* A *state* to represent the bonds, `BondState`. This state is what will be issued, traded, and exited by the flows.
* A *bond contract* that defines the rules for valid transactions, `BondContract`.

Each node owner installs this CorDapp onto their node. They can then issue, trade, and exit bonds with other node owners.

## Key takeaways

CorDapps are:

* Distributed applications that can run on multiple systems simultaneously.
* A set of `.jar` files containing Java or Kotlin class definitions.
* Made up of components that work together to let nodes communicate and agree on updates to the shared ledger.

## Next steps

Ready to get started with CorDapps?

* [Get set up for CorDapp development](getting-set-up.md)
* [Run a sample CorDapp](tutorial-cordapp.md)
