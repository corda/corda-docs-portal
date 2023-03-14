---
date: '2022-11-15'
title: "Network Types"
menu:
  corda-5-beta:
    identifier: corda-5-beta-deploy-network-types
    parent: corda-5-beta-deploy
    weight: 2000
section_menu: corda-5-beta
---

Corda supports the following types of networks:
* [Static](#static-networks)
* [Dynamic](#dynamic-networks)

For information about onboarding to these types of networks see the [Operating Tutorials](../operating/operating-tutorials/onboarding/overview.md).

## Static Networks

Static networks are intended for test purposes when the list of virtual nodes or members in the network are predetermined.
These networks are composed of only a single cluster as there is no instance of the [Membership Group Manager (MGM)](../introduction/key-concepts.html#membership-management) to distribute member data across clusters.

## Dynamic Networks

Dynamic networks are used for the following:
* Production networks
* Testing across multiple clusters
* Testing when the number of members are not predetermined in your test network

One of the main difference to static networks is that there is a running MGM that all members must register with before they can transact among the group. The MGM is also responsible for distributing member data across clusters.
