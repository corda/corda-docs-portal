---
aliases:
- /head/cordapp-overview.html
- /HEAD/cordapp-overview.html
- /cordapp-overview.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-cordapp-overview
    parent: corda-os-4-6-building-a-cordapp-index
    weight: 1010
tags:
- cordapp
- overview
title: What is a CorDapp?
---


# What is a CorDapp?

{{< figure alt="Powered by Corda" zoom="/en/images/powered-by-corda-logo.jpg" >}}

CorDapps (Corda Distributed Applications) are distributed applications that run on the Corda platform. The goal of a
CorDapp is to allow nodes to reach agreement on updates to the ledger. They achieve this goal by defining flows that
Corda node owners can invoke over RPC:

{{< figure alt="node diagram" zoom="/en/images/node-diagram.png" >}}

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


## Writing and building apps that run on both Corda (open source) and Corda Enterprise

Corda and Corda Enterprise are moving towards an Open Core approach, which means in practice that the APIs and dependencies for CorDapps
should all be open source, and all CorDapps (whether targeting Corda open source or Corda Enterprise) can now be compiled against the Open
Source Corda core library, as Corda Enterprise itself is compiled against the Open Source core library.
To make this work in practice you should follow these steps:


* Ensure your CorDapp is designed per [Structuring a CorDapp](writing-a-cordapp.md) and annotated according to [CorDapp separation](cordapp-build-systems.md#cordapp-separation-ref).
In particular, it is critical to separate the consensus-critical parts of your application (contracts, states and their dependencies) from
the rest of the business logic (flows, APIs, etc).
The former - the **CorDapp kernel** - is the Jar that will be attached to transactions creating/consuming your states and is the Jar
that any node on the network verifying the transaction must execute.

{{< note >}}
It is also important to understand how to manage any dependencies a CorDapp may have on 3rd party libraries and other CorDapps.
Please read [Setting your dependencies](cordapp-build-systems.md#cordapp-dependencies-ref) to understand the options and recommendations with regards to correctly Jar’ing CorDapp dependencies.

{{< /note >}}

* Compile this **CorDapp kernel** Jar once, and then depend on it from your workflows Jar. In terms of Corda depdendencies,this should only
depend on the `corda-core` package from the Corda Open Source distribution.

{{< note >}}
As of Corda 4 it is recommended to use [CorDapp Jar signing](cordapp-build-systems.md#cordapp-build-system-signing-cordapp-jar-ref) to leverage the new signature constraints functionality.

{{< /note >}}

* Your workflow Jar(s) should depend on the **CorDapp kernel** (contract, states and dependencies). Importantly, you can create different workflow
Jars for Corda and Corda Enterprise, because the workflows Jar is not consensus critical. For example, you may wish to add additional features
to your CorDapp for when it is run on Corda Enterprise (perhaps it uses advanced features of one of the supported enterprise databases or includes
advanced database migration scripts, or some other Enterprise-only feature).When building a CorDapp against Corda Enterprise, please note that the `corda-core` library still needs to come from the open source
distribution, so you will have dependencies on Corda Enterprise and a matching open core distribution. Specifically, any CorDapp targeted
to run on Corda Enterprise should have unit and integration tests using Corda Enterprise.

In summary, structure your app as kernel (contracts, states, dependencies) and workflow (the rest) and be sure to compile the kernel
against Corda open source. You can compile your workflow (Jars) against the distribution of Corda that they target.
