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

A distributed ledger is a database of facts that’s replicated, shared, and synchronized across multiple participants on a network. 
Participants are members in the same [application network](../../introduction/key-concepts.html#application-networks), represented by [virtual nodes](../../introduction/key-concepts.html#virtual-nodes), and each participant's copy of the ledger is held in their [vault](**). Each participant has a different view of the ledger, depending on the facts it shares. Participants who share a fact must reach consensus before it is committed to the ledger. Two participants always see the exact same version of any on-ledger facts that they share.
