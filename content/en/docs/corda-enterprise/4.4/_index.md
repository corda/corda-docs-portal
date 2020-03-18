---
aliases:
- /releases/4.4/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: -240
project: corda-enterprise
section_menu: corda-enterprise-4-4
title: Corda Enterprise 4.4
version: '4.4'
---


# Introduction to Corda

A Corda Network is a peer-to-peer network of [Nodes](../nodedocs.html), each representing a party on the network.
These Nodes run Corda applications ([CorDapps](../cordapps.html)), and transact between Nodes using public or
confidential identities.

When one or more Nodes are involved in a transaction, the transaction must be notarised. [Notaries](../notarydocs.html) are a specialized type
of Node that provides uniqueness consensus by attesting that, for a given transaction, it has not already signed other
transactions that consumes any of the proposed transaction’s input states.

For all Corda release notes, see the [Release Notes](release-notes-index.md) index page.


## Corda Offerings

There are several commercial Corda offerings available for different solutions requirements. Corda is an open-source platform,
with several enterprise offerings.


### Corda Enterprise

Corda Enterprise is a commercial edition of the Corda platform, specifically optimized to meet the privacy, security and
throughput demands of modern day business. Corda Enterprise is interoperable and compatible with Corda open source and
is designed for organizations with exacting requirements around quality of service and the network infrastructure in
which they operate.

Corda Enterprise contains all the core Corda functionality, but also includes the [Corda Firewall](../firewalldocs.html),
support for [high-availability Node and Notary](../hadocs.html) deployments, and compatibility with hardware security modules ([HSMs](../hsmdoc.html)).


### Corda Enterprise Network Manager

[Corda Enterprise Network Manager](../cenmdocs.html) empowers Corda Network operators, giving greater control over all
aspects of deployment, operation, and consensus rules.

Corda Enterprise Network Manager encompasses three main services:


* The Identity Manager Service. This service enables Nodes to join the network, and handles Node certificate revocation
* The Network Map Service. This service provides a global view of the Network. The public identity of each Node in the Network is registered with the Network Map Service.
* The Signing Service. This service signs approved requests to join the network (CSRs) or revoke a certificate (CRRs), and is also responsible for updating the Network Map Service.











