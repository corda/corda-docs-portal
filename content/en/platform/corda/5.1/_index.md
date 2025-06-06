---
description: "CorDapp Developer, Cluster Administrator, and Network Operator documentation for Corda 5.1."
date: '2022-08-17'
title: Corda 5.1
version: 'Corda 5.1'
# project: Corda
section_menu: corda51
menu:
  versions:
    weight: -4000
  corda51:
    weight: -100    
---
# {{< version >}}

Corda is a {{< tooltip >}}DLT{{< /tooltip >}} application platform for the creation and operation of decentralized applications, written using a rich Java {{< tooltip >}}API{{< /tooltip >}}.
These applications are created using standard Java development tools and packaged using Corda tooling.
Once packaged, applications are deployed onto Corda, which executes both applications and ledger update workflows on behalf of organizational entities.

## Why DLT?

DLT is a digital system for recording, storing, and processing digital data in a decentralized way across a network of computers, perhaps in different locations and involving multiple organizations.
Some of the many benefits of DLT are:

* **Decentralization** - There is no centralized authority of control dictating what {{< tooltip >}}state{{< /tooltip >}} changes can and cannot occur. Instead, parties come to a consensus about changes to the global state and this is controlled by consensus rules.
* **Security** - State changes are attested via signature to prevent unauthorized access and protect against tampering. Three foundational principles apply:
  * **Confidentiality**, which is the ability of two actors to keep the data that they share with each other private from others on a network.
  * **Integrity**, which ensures that data shared between parties is accurate, consistent, and valid over its lifecycle.
  * **Availability**, which guarantees some level of uptime, by being resilient to faults that may occur during operation.
* **Transparency** - All changes to states are audited, which instils more trust between participants and also removes the chance of error.
* **Immutability** - Records of state changes cannot be changed or deleted, but stand as a permanent record.
* **You see what I see** - Once an update is agreed and verified, its validity is incontestable.
This removes the need for post hoc reconciliation between organizations.
Consensus simply means that a threshold has been passed that establishes (within the problem domain) that a proposed modification will be valid and can be applied.
More importantly, once applied and accepted, no parties within that domain can repudiate it.

## Why Corda?

There are several approaches that differentiate Corda from other DLTs:

* **Identity** - Knowing who you are transacting with and knowing that their identity was attested to a given level of assurance is important for establishing trust.
Many other DLT and blockchain systems offer anonymity as a feature.
However, for use cases where trust is absolutely critical, Corda layers its platform with the concept of granting permissions to identities.
Corda does not mandate specific levels of attestation; rather, each network is able to set its own rules. Without permissions, access to the state of a network and other members of that network is impossible.
* **Privacy** - People who want to communicate with each other on Corda can install the same set of distributed applications, known as {{< tooltip >}}CorDapps{{< /tooltip >}}.
These define the parameters of their interactions and exchange information and assets, all within the bounds of what the network operator has permitted around rules for visibility of states.
In these private networks, only the parties involved can see the details of that state.
* **Compliance** - Corda, being designed with the financial services industry in mind, works seamlessly with existing financial systems, allowing banks and other financial institutions to integrate it into their existing processes.
* **Scalability** - Corda is designed to be highly scalable, allowing it to handle large volumes of operations without sacrificing performance or security. This is especially suitable for the financial services industry, which processes huge volumes of financial transactions in short periods of time.
* **Consensus mechanisms** - Corda uses smart contracts to automate complex agreements between parties. These contracts are written in common programming languages, making them easier to create and manage than some other DLT platforms. Smart contracts on Corda are compatible with existing and future regulations and grounded in legal constructs. They record and manage the evolution of agreements (for example, financial agreements) and other shared data between two or more verified and identifiable parties. Supervisory and regulatory bodies can be given access to the network as observers to verify the contract.
* **Workflow** - Corda flows are an important feature of Corda. They help to simplify and automate often complex business processes on the Corda network. Flows define the steps required to complete a specific business process, such as a trade or a settlement.
Flows use a messaging system to allow communication and updates between relevant parties. Flows are designed to be modular, meaning that each step in the flow can be executed independently and in parallel with other steps, which makes Corda efficient, with fast processing times.

To learn more about DLT and Corda's take on DLT, see the [Key Concepts]({{< relref "./key-concepts/_index.md" >}}) section.

### The Evolution of Corda

R3 began the creation of Corda to deliver the above capabilities, creating the first privately permissioned DLT/Blockchain platform, with version 1 released in 2017.
Today, Corda (Corda 5) represents the next step for the platform, evolving the underlying technology to better meet the needs of our customers running Corda in production.
This evolution focuses on scaling, throughput, and availability, whilst retaining its position as a market-leading DLT solution.

## Learn More

The {{< version >}} documentation addresses the following collections of people:

* **Architects** — As an Architect working with Corda, all sections of the Corda documentation are of interest to you, but particularly the [Key Concepts]({{< relref "./key-concepts/_index.md" >}}).
* **CorDapp Developers** — To get started developing CorDapps, see the [Developing Applications]({{< relref "./developing-applications/_index.md">}}) section.
* **Cluster Administrators** — To learn how to deploy and configure Corda, see the [Administering Corda Clusters]({{< relref "./deploying-operating/_index.md">}}) section.
* **Network Operators** — To begin creating application networks and managing the members, see the [Operating Application Networks]({{< relref "./application-networks/_index.md">}}) section.

For more information about the roles of these personas, see [About the Docs]({{< relref "../../../about-the-docs/_index.md" >}}).
