---
title: "The Corda Ledger"
date: 2023-06-08
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-fundamentals-ledger
    parent: corda5-fundamentals
    weight: 5000
section_menu: corda5
---

# The Corda Ledger

A distributed ledger is a database of facts that is replicated, shared, and synchronized across multiple participants on a network. We call an entity that can start or be involved in a transaction a *participant*. 
Participants are members in the same [application network]({{< relref "../application-networks/_index.md" >}}), represented by virtual nodes. Participants require a public/private key pair: they are identified by their public key, and use the private key to sign transactions. In the current implementation in Corda 5.0 Beta, all participants must be members, and they use the ledger key that has been generated when joining the network.

Each participant's copy of the ledger is held in their [vault]({{< relref "./vault/_index.md" >}}). Each participant has a different view of the ledger, depending on the facts it shares. Participants who share a fact must reach consensus before it is committed to the ledger. Two participants always see the exact same version of any on-ledger facts that they share.

Corda does not have a central store of data. Each participant maintains its own database of [states]({{< relref "./states/_index.md" >}}) in their vault. This is information the particiapnt knows to be true based on its interactions. For example, if there are virtual nodes representing Alice and Bob on the network and Alice loans Bob some money, both Alice and Bob store an identical record of the facts about that loan. If the only parties involved with the loan are Alice and Bob, then they are the only nodes that ever see or store this data.

This diagram shows a network with five participants (Alice, Bob, Carl, Demi, and Ed). Each numbered circle on an intersection represents a fact shared between two or more nodes:

{{< 
  figure
	 src="ledger-venn.png"
     width="50%"
	 figcaption="Facts Shared Among Participants"
>}}

In the diagram, facts 1 and 7 are known by both Alice and Bob. Alice only shares facts with Bob, Alice does not share any facts with Carl, Demi, or Ed. Each node only sees a subset of facts — their own facts and those that they share with others. No single node can view the ledger in its entirety. For example, in the diagram Alice and Demi do not share any facts, so they see a completely different set of facts from each other. When multiple participants on a network share an evolving fact, the changes to the fact update at the same time in each participant’s vault. This means that Alice and Bob both see an identical version of shared facts 1 and 7. On-ledger facts do not have to be shared between participants. Facts that are not shared are unilateral facts.

Although there is no central ledger, you can broadcast a basic fact to all nodes of a network using the list of participants from the MGM.