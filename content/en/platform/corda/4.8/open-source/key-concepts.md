---
aliases:
- /head/key-concepts.html
- /HEAD/key-concepts.html
- /key-concepts.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts
    parent: corda-os-4-8-development
    weight: 80
tags:
- concepts
title: Key concepts
---



# Key concepts

Learn about the concepts and features that power Corda, so you can make the best of it. These articles provide an overview suitable for beginners and non-developers. The topics build on each other, so you should read them in order.

{{< note >}}
You can dive deeper into these topics in our introductory [webinar series](key-concepts-webinars.md). For a more academic approach, see the [Corda Whitepaper](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/) and the [Corda Technical Whitepaper](https://www.r3.com/white-papers/corda-technical-whitepaper/).
{{< /note >}}

First, you'll learn about the Corda ecosystem, and how people and businesses in it represent themselves, find each other.

* [Networks, discovery, and identity](key-concepts-ecosystem.md) tells you how Corda networks work, and how members identify themselves and find each other on networks.
* [Nodes](key-concepts-node.md) represent people and businesses on Corda.

Next, you'll learn how information is shared and stored on Corda.

* The [ledger](key-concepts-ledger.md) is the record of transactions on Corda.
* [Flows](key-concepts-flows.md) let nodes communicate with each other.
* [States](key-concepts-states.md) represent shared facts on the ledger.
* [Vaults](key-concepts-vault.md) are where nodes store on-ledger shared facts.

Then, learn how you can exchange assets on Corda.
* [Smart contracts](key-concepts-contracts.md) digitize agreements between nodes.
* [Transactions](key-concepts-transactions.md) - The transactions update the ledger states.




* [Consensus](key-concepts-consensus.md) - How parties on the network reach consensus about shared facts on the ledger
* [Notaries](key-concepts-notaries.md) - The component that assures uniqueness consensus (prevents double spends)


Finally, some concepts that expand on other areas:

* [Time-windows](key-concepts-time-windows.md) - Transactions can be validated as having fallen after, before or within a particular time window
* [Oracles](key-concepts-oracles.md) - Transactions can include off-ledger facts retrieved using Oracles
* [Transaction tear-offs](key-concepts-tearoffs.md) - Transactions can be signed by parties who have access to only a limited view of the transaction parts
* [Deterministic JVM](key-concepts-djvm.md) - Information about the importance and details of the deterministic JVM

Want to dive deeper? Check out the [Corda whitepaper](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/) and the [Corda Technical Whitepaper](https://www.r3.com/white-papers/corda-technical-whitepaper/).

