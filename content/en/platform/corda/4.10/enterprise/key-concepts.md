---
aliases:
- /head/key-concepts.html
- /HEAD/key-concepts.html
- /key-concepts.html
date: '2023-01-30'
menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-10-key-concepts
    parent: corda-enterprise-4-10-cordapps
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

First, you'll learn about the Corda ecosystem, and how people and businesses in it represent themselves and find each other.

* [Networks, discovery, and identity](key-concepts-ecosystem.md) tells you how Corda networks work, and how members identify themselves and find each other on networks.
* [Nodes](key-concepts-node.md) represent people and businesses on Corda.

Next, you'll learn how nodes share and store information.

* The [ledger](key-concepts-ledger.md) is the record of transactions on Corda.
* [Flows](key-concepts-flows.md) let nodes communicate with each other.
* [States](key-concepts-states.md) represent shared facts on the ledger.
* [Vaults](key-concepts-vault.md) are where nodes store on-ledger shared facts.

Then, learn how nodes can exchange assets on Corda.
* [Smart contracts](key-concepts-contracts.md) digitize agreements between nodes.
* You can bring off-ledger data into a smart contract using [oracles](key-concepts-oracles.md).
* [Transactions](key-concepts-transactions.md) update the ledger.
* The ledger is only updated if the nodes reach [consensus](key-concepts-consensus.md).
* [Notaries](key-concepts-notaries.md) assure uniqueness consensus—meaning they prevent double-spends.
* You can use [Merkle trees](key-concepts-tearoffs.md) to add additional security to transactions that use oracles and non-validating notaries.
* [Time windows](key-concepts-time-windows.md) let you validate that a transaction happened before, after, or during a specific time.

After you're familiar with the key concepts of Corda, see them in action by [running a sample CorDapp](tutorial-cordapp.md).



