---
date: '2023-01-27'
title: "UTXO Ledger Example CorDapp"
menu:
  corda5:
    parent: "corda5-develop-get-started"
    identifier: corda5-utxo-example
    weight: 7000
section_menu: corda5
---

The CSDE template includes example CorDapp code for a simple UTXO (Unspent Transaction Output) chat application. The chat CorDapp enables pairs of participants on a Corda application network to do the following:

* Create and name a unique bilateral chat between the two virtual nodes.
* Update chats with new messages from either virtual node.
* Obtain a list of chats that the virtual node is a participant in.
* Retrieve a specified number of previous messages from a chat.

There is both a Kotlin and Java implementation of the Chat CorDapp in the respective `csde-cordapp-template-kotlin` and `csde-cordapp-template-java` repos.
