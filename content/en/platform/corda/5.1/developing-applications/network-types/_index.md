---
date: '2023-08-10'
title: "Network Types"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-develop-networks
    parent: corda51-develop
    weight: 2000
section_menu: corda51
---
# Network Types
Corda supports the following types of networks:
* [Static](#static-networks)
* [Dynamic](#dynamic-networks)

## Static Networks

Static networks are intended for local testing when the list of virtual nodes or members in the network are predetermined.
These networks are composed of only a single cluster as there is no instance of the Membership Group Manager ({{< tooltip >}}MGM{{< /tooltip >}}) to distribute member data across clusters.
For information about deploying locally to a static network with the combined worker, see the [Getting Started Using the CSDE]({{< relref "../getting-started/_index.md" >}}) section.

## Dynamic Networks

Dynamic networks are used for the following:
* Production networks
* Testing across multiple clusters
* Testing when the number of members are not predetermined in your test network

One of the main differences to static networks is that there is a running MGM that all members must register with before they can transact among the group. The MGM is also responsible for distributing member data across clusters.