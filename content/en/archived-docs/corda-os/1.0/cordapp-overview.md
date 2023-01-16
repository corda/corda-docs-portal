---
aliases:
- /releases/release-V1.0/cordapp-overview.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-1-0:
    identifier: corda-os-1-0-cordapp-overview
    parent: corda-os-1-0-building-a-cordapp-index
    weight: 1010
tags:
- cordapp
- overview
title: What is a CorDapp?
---


# What is a CorDapp?

Corda is a platform. Its functionality is extended by developers through the writing of Corda distributed
applications (CorDapps). CorDapps are installed at the level of the individual node, rather than on the network
itself.

Each CorDapp allows a node to handle new business processes, for example asset trading (see [IRS demo](running-the-demos.md#irs-demo)).
It does so by defining new flows on the node that, once started by the node owner, conduct the process of negotiating
a specific ledger update with other nodes on the network. The node’s owner can then start these flows as required,
either through remote procedure calls (RPC) or HTTP requests that leverage the RPC interface.

![node diagram](/en/images/node-diagram.png "node diagram")
CorDapp developers will usually define not only these flows, but also any states and contracts that these flows use.
They will also have to define any web APIs that will run on the node’s standalone web server, any static web content,
and any new services that they want their CorDapp to offer.

CorDapps are made up of definitions for the following components:


* States
* Contracts
* Flows
* Web APIs and static web content
* Services

