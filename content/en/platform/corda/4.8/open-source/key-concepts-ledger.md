---
aliases:
- /head/key-concepts-ledger.html
- /HEAD/key-concepts-ledger.html
- /key-concepts-ledger.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-ledger
    parent: corda-os-4-8-key-concepts
    weight: 1020
tags:
- concepts
- ledger
title: Ledger
---


# Ledger

## Summary

* *The ledger refers to all facts that are shared between the nodes of a network.*
* *Each node will have a different view of the ledger, depending on the facts in which it participates.*
* *Two nodes are always guaranteed to see the exact same version of any on-ledger facts that they share.*

## Video

{{% vimeo 213812040 %}}

## Visibility of data on the ledger

In Corda, there is *no single central store of data*. Instead, each node maintains its own database of facts in which it
participates. For example, if there are nodes representing Alice and Bob on the network and Alice loans Bob some money,
both Alice and Bob will store an identical record of the facts about that loan. If the only parties involved with the
loan are Alice and Bob, then they will be the only nodes that ever see or store this data.

This diagram shows a network with five nodes (Alice, Bob, Carl, Demi, and Ed). Each numbered circle on an intersection
represents a fact shared between two or more nodes:

{{< figure alt="ledger venn" width=80% zoom="/en/images/ledger-venn.png" >}}

In the diagram, facts 1 and 7 are known by both Alice and Bob. Alice only shares facts with Bob, Alice doesn't share
any facts with Carl, Demi, or Ed.

Each node only sees a subset of facts—their own facts and those that they share with others. No single node can view
the ledger in its entirety. For example, in the diagram Alice and Demi don’t share any facts, so they see a
completely different set of facts to each other.

## Shared facts

On Corda, there is no central or general agent which operates on behalf of all of the nodes on the network. Instead,
each node maintains its own vault which contains all of its known facts.

You can think of this vault as being a database or simple table. In this diagram, facts 1 and 7 appear on both Alice's
vault and Bob's vault, and are therefore shared facts:

{{< figure alt="ledger table" width=80% zoom="/en/images/ledger-table.png" >}}

Corda guarantees that when a fact is shared across multiple nodes on the network, it evolves in lockstep in each of
these nodes' vaults. This means that Alice and Bob will both see an *exactly identical version* of shared facts 1 and 7.

On-ledger facts don't have to be shared between nodes. For example, fact 11 in Alice's vault is not shared with Bob.
Facts that are not shared are *unilateral facts*.

{{< note >}}
Although there is no central ledger, you can broadcast a basic fact to all nodes of a network using the network map
service.
{{< /note >}}
