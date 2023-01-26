---
aliases:
- /head/key-concepts-ledger.html
- /HEAD/key-concepts-ledger.html
- /key-concepts-ledger.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-key-concepts-ledger
    parent: corda-enterprise-4-8-key-concepts
    weight: 1020
tags:
- concepts
- ledger
title: Ledger
---


# Ledger

## Summary

* A distributed ledger is a database of facts that's replicated, shared, and synchronized across multiple participants on a network.
* Participants are referred to as nodes and their copy of the ledger is held in their vault.
* Each node has a different view of the ledger, depending on the facts it shares.
* Nodes who share a fact must reach consensus before it’s committed to the ledger.
* Two nodes always see the exact same version of any on-ledger facts they share.

## Video

{{% vimeo 213812040 %}}

## Visibility of data on the ledger

Corda does not have a central store of data. Each node maintains its own database of *facts*–things it knows to be true based on its interactions. For example, if there are nodes representing Alice and Bob on the network and Alice loans Bob some money,
both Alice and Bob will store an identical record of the facts about that loan. If the only parties involved with the
loan are Alice and Bob, then they are the only nodes that ever see or store this data.

This diagram shows a network with five nodes (Alice, Bob, Carl, Demi, and Ed). Each numbered circle on an intersection
represents a fact shared between two or more nodes:

{{< figure alt="ledger venn" width=80% zoom="/en/images/ledger-venn.png" >}}

In the diagram, facts 1 and 7 are known by both Alice and Bob. Alice only shares facts with Bob, Alice doesn't share
any facts with Carl, Demi, or Ed.

Each node only sees a subset of facts—their own facts and those that they share with others. No single node can view
the ledger in its entirety. For example, in the diagram Alice and Demi don’t share any facts, so they see a
completely different set of facts from each other.

## Shared facts

On Corda, no central ledger records facts for all of the nodes on a network. Instead,
each node maintains its own vault, which contains all of its known facts.

You can think of a vault as being a database or simple table. In this diagram, facts 1 and 7 appear on both Alice's
vault and Bob's vault, and are therefore shared facts:

{{< figure alt="ledger table" width=80% zoom="/en/images/ledger-table.png" >}}

When multiple nodes on a network share an evolving fact, the changes to the fact update at the same time in each node's vault. This means that Alice and Bob will both see an *identical version* of shared facts 1 and 7.

On-ledger facts don't have to be shared between nodes. For example, fact 11 in Alice's vault is not shared with Bob.
Facts that are not shared are *unilateral facts*.

Although there is no central ledger, you can broadcast a basic fact to all nodes of a network using the [network map](network/network-map.md)
service.
