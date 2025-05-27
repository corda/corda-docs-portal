---
date: '2023-11-01'
title: "UTXO Ledger Example CorDapp"
description: Discover the UTXO chat example application in the CorDapp template.
menu:
  corda52:
    parent: "corda52-develop-get-started"
    identifier: corda52-utxo-example
    weight: 7000

---
# UTXO Ledger Example CorDapp

The CorDapp template includes example {{< tooltip >}}CorDapp{{< /tooltip >}} code for a simple {{< tooltip >}}UTXO{{< /tooltip >}} chat application. The chat CorDapp enables pairs of participants on an {{< tooltip >}}application network{{< /tooltip >}} to do the following:

* Create and name a unique bilateral chat between the two virtual nodes.
* Update chats with new messages from either {{< tooltip >}}virtual node{{< /tooltip >}}.
* Obtain a list of chats that the virtual node is a participant in.
* Retrieve a specified number of previous messages from a chat.

There is both a Kotlin and Java implementation of the Chat CorDapp in the respective `cordapp-template-kotlin` and `cordapp-template-java` repos.
