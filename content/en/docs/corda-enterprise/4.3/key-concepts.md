---
title: "Key concepts"
date: 2020-01-08T09:59:25Z
---


# Key concepts
This section describes the key concepts and features of the Corda platform. It is intended for readers who are new to
            Corda, and want to understand its architecture. It does not contain any code, and is suitable for non-developers.


{{< note >}}
The pages in this section should be read in order.


{{< /note >}}

The first topics in this section provide an **overview** of the Corda Distributed Ledger:

> 
> 
> * [The network]({{< relref "key-concepts-ecosystem" >}}) - The ecosystem that Corda exists in
> 
> 
> * [The ledger]({{< relref "key-concepts-ledger" >}}) - The ledger, and how facts on the ledger are shared between nodes
> 
> 
The second set of topics describe the core **CorDapp Concepts**:

> 
> 
> * [States]({{< relref "key-concepts-states" >}}) - The states represent shared facts on the ledger
> 
> 
> * [Transactions]({{< relref "key-concepts-transactions" >}}) - The transactions update the ledger states
> 
> 
> * [Contracts]({{< relref "key-concepts-contracts" >}}) - The contracts govern the ways in which states can evolve over time
> 
> 
> * [Flows]({{< relref "key-concepts-flows" >}}) - The flows describe the interactions that must occur between parties to achieve consensus (to satisfy some business requirement)
> 
> 

{{< note >}}
When you build a custom CorDapp, your CorDapp will have state, transaction, contract and flow classes.


{{< /note >}}
The following **Adavnced Corda Concepts** describe important conceptual information:

> 
> 
> * [Consensus]({{< relref "key-concepts-consensus" >}}) - How parties on the network reach consensus about shared facts on the ledger
> 
> 
> * [Notaries]({{< relref "key-concepts-notaries" >}}) - The component that assures uniqueness consensus (prevents double spends)
> 
> 
> * [Vault]({{< relref "key-concepts-vault" >}}) - The component that stores on-ledger shared facts for a node
> 
> 
Finally, some concepts that expand on other areas:

> 
> 
> * [Time-windows]({{< relref "key-concepts-time-windows" >}}) - Transactions can be validated as having fallen after, before or within a particular time window
> 
> 
> * [Oracles]({{< relref "key-concepts-oracles" >}}) - Transactions can include off-ledger facts retrieved using Oracles
> 
> 
> * [Nodes]({{< relref "key-concepts-node" >}}) - Each node contains an instance of Corda, one or more CorDapps, and so on
> 
> 
> * [Transaction tear-offs]({{< relref "key-concepts-tearoffs" >}}) - Transactions can be signed by parties who have access to only a limited view of the transaction parts
> 
> 
> * [Trade-offs]({{< relref "key-concepts-tradeoffs" >}}) - Trade-offs that have been made in designing Corda and CorDapps
> 
> 
> * [Deterministic JVM]({{< relref "key-concepts-djvm" >}}) - Information about the importance and details of the deterministic JVM
> 
> 
The detailed thinking and rationale behind these concepts are presented in two white papers:

> 
> 
> * [Corda: An Introduction](_static/corda-introductory-whitepaper.pdf)
> 
> 
> * [Corda: A Distributed Ledger](_static/corda-technical-whitepaper.pdf) (A.K.A. the Technical White Paper)
> 
> 
Explanations of the key concepts are also available as [videos](https://vimeo.com/album/4555732/).


