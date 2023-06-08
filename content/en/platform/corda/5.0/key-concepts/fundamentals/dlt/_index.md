---
title: "Distributed Ledger Technology"
date: 2023-06-07
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-fundamentals-DLT
    parent: corda5-fundamentals
    weight: 4000
section_menu: corda5
---

# Distributed Ledger Technology

As described in the [Privacy Key Concepts section]({{< relref "../privacy/_index.md">}}), Corda offers a single, global, source of truth that can be shared by multiple untrusting individuals. 
Corda provides this utilizing a distributed ledger.
DLT has the following characteristics:
* A distributed ledger is a database of facts that are replicated, shared, and synchronized across multiple participants on a network.
* Participants are known as identities and represent a real-world entity within the context of an application network.
* Each identity has a different view of the ledger, depending on the facts it shares.
* Identities that share a fact must reach a consensus before it is committed to the ledger.
* All Identities always see the exact same version of any on-ledger facts they share.