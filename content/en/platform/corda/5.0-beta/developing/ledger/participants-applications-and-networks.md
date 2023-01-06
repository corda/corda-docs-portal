---
date: '2023-01-05'
title: "Participants, Applications and Networks"
draft: true
menu:
  corda-5-beta:
    parent: corda-5-beta-ledger
    identifier: corda-5-beta-participants-apps-networks
    weight: 9000
section_menu: corda-5-beta
---

## Participants

We call an entity that can start or be involved in a transaction a *participant*. Participants need to have a public/private key pair: they are identified by their public key, and use the private key to sign transactions.

In the current implementation in Corda 5 beta 1, all participants need to be members, and they use the ledger key that has been generated when joining the network

## Application Networks

Corda 5 is organized into *application networks*. Each network has:

* a set of applications packaged into a CPB (Corda package bundle)
* a network ID and a network policy; these are bundled with the CPB into a CPI (Corda package installer)
* a Membership Group Manager (MGM); this is a member that controls membership in the network
* (optionally) one or more notaries; these are required to use the UTXO ledger

## Applications

An *application* consists of workflow code (the user code that is actually run), and contract code (defining states, contracts, encumbrances, verification logic and so on).

An application is bundled with a network group policy and a network ID into a CPI (Corda package installer). This CPI can be installed onto a Corda 5 cluster, which enables the cluster to host members of said network.

## Members

*Members* are identified by a holding ID, which is a combination of a network group ID (or the hash thereof) and an X.500 name. The X.500 name must be unique within a single network. 

The holding ID gets created when a virtual node for a member is created on a cluster that has the CPI for the desired network installed.

After creation of the virtual node, the member needs to be registered with the MGM. Only after registration with the MGM will the member:

* have a valid public/private ledger key pair to sign transactions and identify themselves as participants.

* be visible to other members for interactions.

* be able to use flow session to communicate to other members.

## Virtual Nodes

A *virtual node* is the runtime environment that is required for a member to run application code. It gets created on a Corda 5 cluster, and will be identified by the short hash of the member’s holding ID. It consists of all the required configuration to create the various sandboxes that are required to run the virtual node’s code on the workers of the cluster, plus database tables and cryptographic keys so that the virtual node can store data and sign and verify transactions.