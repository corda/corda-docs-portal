---
date: '2020-04-07T12:00:00Z'
description: "Documentation for the 4.11 Enterprise Edition release of Corda"
menu:
  versions:
    weight: -800
  corda-enterprise-4-11:
    identifier: about-corda-landing-4-11-enterprise
    weight: -30
    name: Corda Enterprise 4.11
project: Corda
section_menu: corda-enterprise-4-11
title: Corda Enterprise 4.11
version: 'Enterprise 4.11'
aliases:
- /docs/corda-enterprise/index.html
---

# Corda Enterprise 4.11

Corda is the world’s first private, permissioned distributed ledger technology (DLT) platform designed to work with today’s financial services industry. While regulated companies may start on public blockchains, they soon realize when they get to production, that they require capabilities native to Corda such as privacy, security, scalability, and ease-of-integration with existing systems. That’s why R3 is also exploring interoperability with assets that originate on a non-Corda network.

Corda Enterprise is a commercial edition of the Corda platform, specifically optimised to meet the privacy, security, and
throughput demands of modern day business. Corda Enterprise is interoperable and compatible with Corda Community Edition and
is designed for organisations with exacting requirements around quality of service and the network infrastructure in
which they operate.

A Corda Network is a peer-to-peer network of [nodes]({{< relref "node/component-topology.md" >}}), each representing a party on the network.
These nodes run Corda applications ([CorDapps]({{< relref "cordapps/cordapp-overview.md" >}})), and transact between nodes using public or
confidential identities.

When one or more nodes are involved in a transaction, the transaction must be notarised. [Notaries]({{< relref "notary/ha-notary-service-overview.md" >}}) are a specialised type
of node that provides uniqueness consensus by attesting that, for a given transaction, it has not already signed other
transactions that consumes any of the proposed transaction’s input states.

Corda Enterprise contains all the core Corda functionality, but also includes the [Corda Firewall]({{< relref "node/corda-firewall-component.md" >}}),
support for high-availability node and notary deployments, and compatibility with hardware security modules ([HSMs]({{< relref "node/operating/cryptoservice-configuration.md" >}})).