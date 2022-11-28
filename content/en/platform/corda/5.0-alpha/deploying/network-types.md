---
date: '2022-11-15'
title: "Network Types"
menu:
  corda-5:
    identifier: corda-5-alpha-deploy-network-types
    parent: corda-5-alpha-deploy
    weight: 2000
section_menu: corda-5-alpha
---

Corda supports the following types of networks:
* [Static](#static-networks)
* [Dynamic](#dynamic-networks)

## Static Networks
Static networks are intended for test purposes when the list of virtual nodes or members in the network are predetermined.
These networks are composed of only a single cluster as there is no instance of the [Membership Group Manager (MGM)](../introduction/key-concepts.html#membership-management) to distribute member data across clusters.
To run a static network, you must complete the following high-level steps:
1. [Start a Corda cluster](deployment-tutorials/deploy-corda-cluster.html).
2. [Define the members in the group in the `GroupPolicy.json` file](deployment-tutorials/onboarding/static-onboarding.html#create-the-group-policy-file).
3. [Package the `GroupPolicy.json` file into a CPI](deployment-tutorials/onboarding/static-onboarding.html#create-a-cpi).
4. [Upload the CPI to your cluster](deployment-tutorials/onboarding/static-onboarding.html#upload-the-cpi).
5. [Create a virtual node in your cluster for each member defined in the group policy file](deployment-tutorials/onboarding/static-onboarding.html#create-virtual-nodes-for-each-member).
6. [Register each member in the group](deployment-tutorials/onboarding/static-onboarding.html#register-members).

## Dynamic Networks
Dynamic networks are used for the following:
* Production networks
* Testing across multiple clusters
* Testing when the number of members are not predetermined in your test network

One of the main difference to static networks is that there is a running [MGM](../../introduction/key-concepts.html#membership-management) that all members must register with before they can transact among the group. The MGM is also responsible for distributing member data across clusters.

To run a dynamic network, you must complete the following high-level steps:
1. [Start a Corda cluster](deployment-tutorials/deploy-corda-cluster.html).
2. [Create an MGM `GroupPolicy.json` file](deployment-tutorials/onboarding/mgm-onboarding.html#create-the-group-policy-file).
3. [Package the MGM `GroupPolicy.json` file into an MGM CPI](deployment-tutorials/onboarding/mgm-onboarding.html#build-the-cpi).
4. [Upload the CPI to your cluster](deployment-tutorials/onboarding/mgm-onboarding.html#upload-the-cpi).
5. [Create a virtual node in your cluster for the MGM](deployment-tutorials/onboarding/mgm-onboarding.html#create-a-virtual-node).
6. [Assign required Hardware Security Modules (HSMs) for the MGM](deployment-tutorials/onboarding/mgm-onboarding.html#assign-soft-hsm-and-generate-session-initiation-and-ecdh-key-pair).
7. [Create required keys and optionally import required certificates](deployment-tutorials/onboarding/mgm-onboarding.html#configure-the-cluster-tls-key-pair-and-certificate).
8. [Build the registration context](deployment-tutorials/onboarding/mgm-onboarding.html#build-registration-context).
9. [Use the register endpoint to finalise the MGM setup so that it is ready to accept members](deployment-tutorials/onboarding/mgm-onboarding.html#register-the-mgm).
10. [Export the `GroupPolicy.json` file that members require to join the group](deployment-tutorials/onboarding/dynamic-onboarding.html#generate-the-group-policy-file).
11. [Package this `GroupPolicy.json` file into a member CPI](deployment-tutorials/onboarding/dynamic-onboarding.html#build-the-cpi).
12. [Upload this CPI to the cluster](deployment-tutorials/onboarding/dynamic-onboarding.html#upload-the-cpi).
13. [Create the virtual node for the member](deployment-tutorials/onboarding/dynamic-onboarding.html#create-a-virtual-node).
14. [Assign required HSMs for P2P session initiation](deployment-tutorials/onboarding/dynamic-onboarding.html#configure-the-p2p-session-initiation-key-pair-and-certificate).
15. [Assign required HSMs for the ledger](deployment-tutorials/onboarding/dynamic-onboarding.html#configure-the-ledger-key-pair-and-certificate).
16. [Create required keys, and optionally import required certificates](deployment-tutorials/onboarding/dynamic-onboarding.html#configure-the-tls-key-pair-and-certificate).
17. [Build the registration context](deployment-tutorials/onboarding/dynamic-onboarding.html#build-registration-context).
18. [Use the `register` endpoint to request membership from the MGM](deployment-tutorials/onboarding/dynamic-onboarding.html#register-members).
