---
cascade:
  version: 'Enterprise 4.12'
  project: Corda
  section_menu: corda-enterprise-4-12
description: "Documentation for the 4.12 Enterprise Edition release of Corda"
title: "Corda Enterprise 4.12"
date: '2020-04-07'
menu:
  versions:
    weight: -900
  corda-enterprise-4-12:
    identifier: about-corda-landing-4-12-enterprise
    weight: -30
---

# Corda Enterprise 4.12

Corda is the world’s first private, permissioned distributed ledger technology (DLT) platform designed to work with today’s financial services industry. Regulated companies may start on public blockchains. However, they soon realize that when they get to production they require capabilities native to Corda: privacy, security, scalability, and ease-of-integration with existing systems. That is why R3 is also exploring interoperability with assets that originate on a non-Corda-based network.

Corda Enterprise is a commercial edition of the Corda platform, specifically optimized to meet the privacy, security, and
throughput demands of modern-day business. Corda Enterprise is interoperable and compatible with [Corda Open Source Edition]({{< relref "../community/_index.md" >}}) and
is designed for organizations with exacting requirements around quality of service and the network infrastructure in
which they operate.

A Corda network is a peer-to-peer network of [nodes]({{< relref "node/component-topology.md" >}}), each representing a party on the network.
These nodes run Corda applications ([CorDapps]({{< relref "cordapps/cordapp-overview.md" >}})), and transact between nodes using public or
confidential identities.

When one or more nodes are involved in a transaction, the transaction must be notarized. [Notaries]({{< relref "notary/ha-notary-service-overview.md" >}}) are a specialized type
of node that provides uniqueness consensus by attesting that, for a given transaction, it has not already signed other
transactions that consumes any of the proposed transaction’s input states.

Corda Enterprise contains all the core Corda functionality, but also includes the [Corda Firewall]({{< relref "node/corda-firewall-component.md" >}}),
support for [high-availability for nodes]({{< relref "node/deploy/hot-cold-deployment.md" >}}) and [notaries]({{< relref "notary/ha-notary-service-setup.md" >}}), and compatibility with hardware security modules ([HSMs]({{< relref "node/operating/cryptoservice-configuration.md" >}})).
