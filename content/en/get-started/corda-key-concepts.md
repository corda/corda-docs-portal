---
date: '2020-07-15T12:00:00Z'
menu:
  get-started:
    identifier: get-started-concepts
    name: Corda key concepts
title: Corda key concepts
weight: 200
---

# Corda key concepts

Familiarize yourself with the [key concepts](../platform/corda/4.8/open-source/key-concepts.md) and features of the Corda platform in the pages listed below. You should follow the suggested order of reading.

This content is intended for readers who are new to Corda and who want to understand its architecture and main building blocks. It does not contain any code and is suitable for non-developers.

## 1. The Corda distributed ledger

Read an **overview** of the Corda distributed ledger:

* [The network](../platform/corda/4.8/open-source/key-concepts-ecosystem.md) - the ecosystem that Corda exists in.
* [The ledger](../platform/corda/4.8/open-source/key-concepts-ledger.md), and how facts on the ledger are shared between nodes.

## 2. Core CorDapp concepts

Read about the core **CorDapp concepts**:

* [States](../platform/corda/4.8/open-source/key-concepts-states.md) - represent shared facts on the ledger.
* [Transactions](../platform/corda/4.8/open-source/key-concepts-transactions.md) - update the ledger states.
* [Contracts](../platform/corda/4.8/open-source/key-concepts-contracts.md) - govern the ways in which states can evolve over time.
* [Flows](../platform/corda/4.8/open-source/key-concepts-flows.md) - describe the interactions that must occur between parties to achieve consensus (to satisfy some business requirement).

{{< note >}}
When you build a custom CorDapp, your CorDapp will have state, transaction, contract, and flow classes.
{{< /note >}}

## 3. Advanced Corda concepts

The following **advanced Corda concepts** describe important conceptual information:

* [Consensus](../platform/corda/4.8/open-source/key-concepts-consensus.md) - how parties on the network reach consensus about shared facts on the ledger.
* [Notaries](../platform/corda/4.8/open-source/key-concepts-notaries.md) - the component that assures uniqueness consensus (prevents double spends).
* [Vault](../platform/corda/4.8/open-source/key-concepts-vault.md) - the component that stores on-ledger shared facts for a node.

## 4. More key concepts

Finally, some concepts that expand on other areas:

* [Time-windows](../platform/corda/4.8/open-source/key-concepts-time-windows.md) - transactions can be validated as having fallen after, before or within a particular time-window.
* [Oracles](../platform/corda/4.8/open-source/key-concepts-oracles.md) - transactions can include off-ledger facts retrieved using Oracles.
* [Nodes](../platform/corda/4.8/open-source/key-concepts-node.md) - each node contains an instance of Corda, one or more CorDapps, and so on.
* [Transaction tear-offs](../platform/corda/4.8/open-source/key-concepts-tearoffs.md) - transactions can be signed by parties who have access to only a limited view of the transaction parts.
* [Trade-offs](../platform/corda/4.8/open-source/key-concepts-tradeoffs.md) that have been made in designing Corda and CorDapps.
* [Deterministic JVM](../platform/corda/4.8/open-source/key-concepts-djvm.md) - information about the importance and details of the deterministic JVM.

## 5. Corda white papers

The detailed thinking and rationale behind these concepts are presented in two white papers:

* [Corda: An Introduction](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/).
* [Corda: A Distributed Ledger](https://www.r3.com/white-papers/corda-technical-whitepaper/).

Explanations of the key concepts are also available as [videos](https://vimeo.com/album/4555732/).
