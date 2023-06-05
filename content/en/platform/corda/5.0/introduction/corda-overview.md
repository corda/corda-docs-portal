---
title: "Corda Overview"
date: 2023-04-21
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-background
    parent: corda5-intro
    weight: 2000
section_menu: corda5
---
# Corda Overview

## Decentralized Applications
In recent decades, business processes have been transformed via the progressive adoption of new technologies.
Each step has brought improvements and economies in terms of speed, capacity, connectivity, communication, and predictability.
Systems have grown to the extent that single instances can no longer successfully deliver adequate solutions, leading to the rise of decentralization and a move to the cloud.

However, these solutions are all limited by an implicit boundary that exists, yet is rarely recognized or included in architecture diagrams - trust.
Distributed systems are designed to operate within a single trust zone where updates are applied and accepted, mutating the global state, without question.
For example, when a bilateral agreement is executed between two parties, both must run their own reconciliation system to ensure that the exchange occurred and was done correctly.
This adds friction to all transactions and adds considerable cost. 
The challenge in solving this is that the two parties in our example have no ability to simply accept the word of the other party, without costly reconciliation. 
Decentralized applications are the solution to this problem.

## What is DLT?
DLT stands for Distributed Ledger Technology. It is a digital system for recording, storing, and processing digital data in a decentralized way across a network of computers, perhaps in different locations and involving multiple organisations. 

Decentralized applications are a new paradigm of application where the source of truth, represented by the application's state, can cross trust boundaries without the requirement for a central, overarching, point of control.
This is achieved through the use of DLT, which allows for the creation of stateful data that can be updated by any number of interested parties through the reaching of consensus between them that a proposed change is valid.

The technology uses cryptographic techniques to secure data and validate modifications.
The validity of an update or modification is determined by a set of rules established within an application domain, which all members recognize as binding when an update is proposed.
An update can only be applied when there is consensus within the domain that it is a valid proposal.
These rules are expressed as smart contracts that are intrinsically linked with the chosen representation of the global state.
Every participant in the network has a view of the shared global state of data (the extent of that view depends on its visibility restrictions), which is updated in real-time as changes occur.
This ensures that the data is accurate, transparent, and tamper-evident.

Blockchain is one popular type of DLT that is commonly used for cryptocurrencies such as Bitcoin, but there are many other types of DLT besides blockchain.  


## Why DLT?
Some of the many benefits of DLT are:
* **Decentralization** - There is no centralized authority of control dictating what state changes can and cannot occur. Instead, parties come to a consensus about changes to the global state and this is controlled by consensus rules.

* **Security** - State changes are attested via signature to prevent unauthorised access and tampering is protected against. Three foundational principles apply:

  * **Confidentiality**, which is the ability of two actors to keep the data that they share private from others on a network.

  * **Integrity**, which ensures that data shared between parties is accurate, consistent, and valid over its lifecycle.

  * **Availability**, which importantly guarantees some level of uptime, by being resilient to faults that may occur during operation.

* **Transparency** - All changes to states are audited, which instills more trust between participants and also leads to no errors.

* **Immutability** - Records of state changes cannot be changed or deleted, but stand as a permanent record.

* **You see what I see** - Once an update is agreed and verified, its validity is incontestable.
This removes the need for post hoc reconciliation between organizations. 
Consensus simply means that a threshold has been passed that establishes (within the problem domain) that a proposed modification will be valid and can be applied.
More importantly, once applied and accepted, no parties within that domain can repudiate it.


## What is Corda’s take on DLT?
Corda is a distributed application platform for the creation and operation of decentralized applications, which are written using a rich Java API.
These applications are created using standard Java development tools and packaged using Corda tooling.
Once packaged, applications are deployed onto Corda which executes those both applications and ledger update workflows on behalf of organizational entities.

There are some approaches that differentiate Corda from other DLTs. Identity (along with associated permissions) and privacy are especially important in order to serve the needs of highly regulated financial institutions. The following summarizes what Corda does differently:

* **Identity** - Knowing who you are transacting with and knowing that their identity was attested to a given level of assurance is important for establishing trust.
This is especially the case for regulated industries that need to perform some level of KYC (Know Your Customer).
Often this is because of Anti-Money Laundering (AML) legislation that requires you to know who you are transacting with, but it can also be for other reasons such as avoiding the legal consequences of engaging with an entity on a sanction list.
Identity validation is handled when onboarding a participant identity to a business network.
Many other DLT and blockchain systems offer anonymity as a feature, especially for cases where true censor-resistant mutation of some global state is a requirement.
However, for use cases where trust is absolutely critical, Corda layers its platform with the concept of granting permissions to identities.
These permissions can be granted during onboarding of identities and it is simply a case of attesting that supplied credentials prove that an entity is who they claim to be.
Corda does not mandate certain levels of attestation, but rather each network is able to set their own rules. Without permissions, access to the state of a network and other members of that network is impossible.

* **Privacy** - People who want to communicate with each other on Corda can install the same set of distributed applications or CorDapps.
These define the parameters of their interactions and exchange information and assets; all within the bounds of what the network operator has permitted around rules for visibility of states.
In these private networks, only the parties involved can see the details of that state.
This is important in financial services, where confidentiality is required.
Unlike more public DLT offerings, where the entire ledger state is shared between all members, Corda enables the restriction of sharing to those who “need to know” and have visibility of updates.
This removes the ability for information to leak out through the observation of anonymous state changes in more public systems where, despite the potential anonymity of participants, the entire state is visible.

* **Compliance** - Corda, being designed with the financial services industry in mind, works seamlessly with existing financial systems, allowing banks and other financial institutions to integrate it into their existing processes.

* **Scalability** - Corda is designed to be highly scalable, allowing it to handle large volumes of operations without sacrificing performance or security. This is especially suitable for the financial services industry, which processes huge volumes of financial transactions in short periods of time.

* **Consensus mechanisms** - Corda uses smart contracts to automate complex agreements between parties. These contracts are written in common programming languages, making them easier to create and manage than some other DLT platforms. Smart contracts on Corda are compatible with existing and future regulations and grounded in legal constructs. They record and manage the evolution of agreements (for example, financial agreements) and other shared data between two or more verified and identifiable parties. Supervisory and regulatory bodies can be given access to the network as observers to verify the contract.

* **Workflow** - Corda flows are an important feature of Corda. They help to simplify and automate often complex business processes on the Corda network. Flows define the steps required to complete a specific business process, such as a trade or a settlement.
They use a messaging system to allow communication and updates between relevant parties. Flows are designed to be modular, meaning that each step in the flow can be executed independently and in parallel with other steps, which makes Corda efficient, with fast processing times.

## The Evolution of Corda
R3 began the creation of Corda to deliver the above capabilities, creating the first privately permissioned DLT/Blockchain platform, with version 1 released in 2017.
Today, the Next-Gen Corda (Corda 5) represents the next step for the platform, evolving the underlying technology to better meet the needs of our customers running Corda in production.
This evolution focuses on scaling, throughput, and availability, whilst retaining its position as a market-leading DLT solution.