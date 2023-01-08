---
date: '2023-01-05'
title: "Ledger"
menu:
  corda-5-beta:
    identifier: corda-5-beta-ledger
    parent: corda-5-beta-develop
    weight: 3000
section_menu: corda-5-beta
---

A distributed ledger is a database of facts that is replicated, shared, and synchronized across multiple participants on a network. We call an entity that can start or be involved in a transaction a *participant*. 
Participants are members in the same [application network](../../introduction/key-concepts.html#application-networks), represented by [virtual nodes](../../introduction/key-concepts.html#virtual-nodes). Participants require a public/private key pair: they are identified by their public key, and use the private key to sign transactions. In the current implementation in Corda 5.0 Beta 1, all participants must be members, and they use the ledger key that has been generated when joining the network.

Each participant's copy of the ledger is held in their [vault](vault.html). Each participant has a different view of the ledger, depending on the facts it shares. Participants who share a fact must reach consensus before it is committed to the ledger. Two participants always see the exact same version of any on-ledger facts that they share.

Corda does not have a central store of data. Each participant maintains its own database of [states](states.html) in their vault. This is information the particiapnt knows to be true based on its interactions. For example, if there are virtual nodes representing Alice and Bob on the network and Alice loans Bob some money, both Alice and Bob store an identical record of the facts about that loan. If the only parties involved with the loan are Alice and Bob, then they are the only nodes that ever see or store this data.

This diagram shows a network with five participants (Alice, Bob, Carl, Demi, and Ed). Each numbered circle on an intersection represents a fact shared between two or more nodes:

{{< 
  figure
	 src="ledger-venn.png"
	 figcaption="Facts Shared Among Participants"
>}}

In the diagram, facts 1 and 7 are known by both Alice and Bob. Alice only shares facts with Bob, Alice does not share any facts with Carl, Demi, or Ed. Each node only sees a subset of facts — their own facts and those that they share with others. No single node can view the ledger in its entirety. For example, in the diagram Alice and Demi do not share any facts, so they see a completely different set of facts from each other. When multiple participants on a network share an evolving fact, the changes to the fact update at the same time in each participant’s vault. This means that Alice and Bob both see an identical version of shared facts 1 and 7. On-ledger facts do not have to be shared between participants. Facts that are not shared are unilateral facts.

Although there is no central ledger, you can broadcast a basic fact to all nodes of a network using the list of participants from the [MGM](../../introduction/key-concepts.html#membership-management).