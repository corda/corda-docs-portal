---
date: '2022-11-15'
title: "Network Types"
menu:
  corda-5:
    identifier: corda-5-beta-deploy-network-types
    parent: corda-5-beta-deploy
    weight: 2000
section_menu: corda-5-beta
---

Corda supports the following types of networks:
* [Static](#static-networks)
* [Dynamic](#dynamic-networks)

## Static Networks

Static networks are intended for test purposes when the list of virtual nodes or members in the network are predetermined.
These networks are composed of only a single cluster as there is no instance of the [Membership Group Manager (MGM)](../introduction/key-concepts.html#membership-management) to distribute member data across clusters.
To run a static network, you must complete the following high-level steps:
1. [Start a Corda cluster](../deployment-tutorials/deploy-corda-cluster.html).
2. Define the members in the group in the `GroupPolicy.json` file.
3. Package the `GroupPolicy.json` file into a CPI.
4. Upload the CPI to your cluster.
5. Create a virtual node in your cluster for each member defined in the group policy file.
6. Register each member in the group.
<!--add cross-refs when ready-->

## Dynamic Networks

Dynamic networks are used for the following:
* Production networks
* Testing across multiple clusters
* Testing when the number of members are not predetermined in your test network

One of the main difference to static networks is that there is a running [MGM](../../introduction/key-concepts.html#membership-management) that all members must register with before they can transact among the group. The MGM is also responsible for distributing member data across clusters.

To run a dynamic network, you must complete the following high-level steps:
1. [Start a Corda cluster](../deployment-tutorials/deploy-corda-cluster.html).
2. Create an MGM `GroupPolicy.json` file.
3. Package the MGM `GroupPolicy.json` file into an MGM CPI.
4. Upload the CPI to your cluster.
5. Create a virtual node in your cluster for the MGM.
6. Assign required Hardware Security Modules (HSMs) for the MGM.
7. Create required keys and optionally import required certificates.
8. Use the register endpoint to finalise the MGM setup so that it is ready to accept members.
9. Export the `GroupPolicy.json` file that members require to join the group.
10. Package this `GroupPolicy.json` file into a member CPI.
11. Upload this CPI to the cluster.
12. Create the virtual node for the member.
13. Assign required HSMs for the MGM.
14. Create required keys, and optionally import required certificates.
15. Use the `register` endpoint to request membership from the MGM.
<!--add cross-refs when ready-->
