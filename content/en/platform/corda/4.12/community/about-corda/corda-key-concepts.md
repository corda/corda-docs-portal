---
title: "Corda Community Edition Key Concepts"
date: '2021-07-02'
menu:
  corda-community-4-12:
    parent: about-corda-landing-4-12-community
    identifier: corda-key-concepts-4-12-community
    weight: 100
    name: "Key concepts"
tags:
- concepts
- community
- key

---

# Corda key concepts

Familiarize yourself with the key concepts and features of the Corda platform in the pages listed below. You should follow the suggested order of reading.

This content is intended for readers who are new to Corda and who want to understand its architecture and main building blocks. It does not contain any code and is suitable for non-developers.

## The Corda distributed ledger

Read an **overview** of the Corda distributed ledger:

* [The network]({{< relref "../key-concepts-ecosystem.md" >}}) - the ecosystem that Corda exists in.
* [The ledger]({{< relref "../key-concepts-ledger.md" >}}), and how facts on the ledger are shared between nodes.

## Core CorDapp concepts

Read about the core **CorDapp concepts**:

* [States]({{< relref "../key-concepts-states.md" >}}) - represent shared facts on the ledger.
* [Transactions]({{< relref "../key-concepts-transactions.md" >}}) - update the ledger states.
* [Contracts]({{< relref "../key-concepts-contracts.md" >}}) - govern the ways in which states can evolve over time.
* [Flows]({{< relref "../key-concepts-flows.md" >}}) - describe the interactions that must occur between parties to achieve consensus (to satisfy some business requirement).

{{< note >}}
When you build a custom CorDapp, your CorDapp will have state, transaction, contract, and flow classes.
{{< /note >}}

## Advanced Corda concepts

The following **advanced Corda concepts** describe important conceptual information:

* [Consensus]({{< relref "../key-concepts-consensus.md" >}}) - how parties on the network reach consensus about shared facts on the ledger.
* [Notaries]({{< relref "../key-concepts-notaries.md" >}}) - the component that assures uniqueness consensus (prevents double spends).
* [Vault]({{< relref "../key-concepts-vault.md" >}}) - the component that stores on-ledger shared facts for a node.

## More key concepts

Finally, some concepts that expand on other areas:

* [Time-windows]({{< relref "../key-concepts-time-windows.md" >}}) - transactions can be validated as having fallen after, before or within a particular time-window.
* [Oracles]({{< relref "../key-concepts-oracles.md" >}}) - transactions can include off-ledger facts retrieved using Oracles.
* [Nodes]({{< relref "../key-concepts-node.md" >}}) - each node contains an instance of Corda, one or more CorDapps, and so on.
* [Transaction tear-offs]({{< relref "../key-concepts-tearoffs.md" >}}) - transactions can be signed by parties who have access to only a limited view of the transaction parts.
* [Trade-offs]({{< relref "../key-concepts-tradeoffs.md" >}}) that have been made in designing Corda and CorDapps.

## CorDapps tutorial 

After you've become familiar with the key concepts of Corda, see them in action by [running a sample CorDapp]({{< relref "../tutorial-cordapp.md" >}}).

## Corda white papers

The detailed thinking and rationale behind the above concepts are presented in two white papers:

* [Corda: An Introduction](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/).
* [Corda: A Distributed Ledger](https://www.r3.com/white-papers/corda-technical-whitepaper/).

Explanations of the key concepts are also available as [a series of webinars]({{< relref "../key-concepts-webinars.md" >}}).
