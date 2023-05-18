---
title: "Background"
date: 2023-04-21
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-background
    parent: corda5-intro
    weight: 2000
section_menu: corda5
---

## What is DLT?
DLT stands for Distributed Ledger Technology. It is a digital system for recording, storing, and processing digital data in a decentralized way across a network of computers, perhaps in different locations and involving multiple organisations. 
The technology uses cryptographic techniques to secure data and validate modifications. Every participant in the network has a view of the shared global state of data (the extent of that view depends on its visibility restrictions), which is updated in real-time as changes occur. 
This ensures that the data is accurate, transparent, and tamper-proof.

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

* **You see what I see** - Once an update is agreed and verified, its validity is incontestable. This removes the need for post hoc reconciliation between organisations.


## What is Corda’s take on DLT?
There are some approaches that differentiate Corda from other DLTs. The following summarises what Corda does differently:

* **Identity** - Knowing who you are transacting with and knowing that their identity was attested to a given level of assurance is important for establishing trust. This identity validation is handled when onboarding a participant identity to a business network.

* **Privacy** - People who want to communicate with each other on Corda can install the same set of CorDapps, which lets them define the parameters of their interactions and exchange information and assets, within the bounds of what the network operator has permitted around rules for visibility of states. In these private networks, only the parties involved can see the details of that state. This is important in financial services, where confidentiality is required.

* **Compliance** - Corda, being designed with the financial services industry in mind, works seamlessly with existing financial systems, allowing banks and other financial institutions to integrate it into their existing processes.

* **Scalability** - Corda is designed to be highly scalable, allowing it to handle large volumes of operations without sacrificing performance or security. This is especially suitable for the financial services industry, which processes huge volumes of financial transactions per minute.

* **Consensus mechanisms** - Corda uses smart contracts to automate complex agreements between parties. These contracts are written in common programming languages, making them easier to create and manage than some other DLT platforms. Smart contracts on Corda are compatible with existing and future regulations and grounded in legal constructs. They record and manage the evolution of agreements (for example financial agreements) and other shared data between two or more verified and identifiable parties. Supervisory and regulatory bodies can be given access to the network as observers to verify the contract.

* **Workflow** - Corda flows are an important feature of Corda. They help to simplify and automate often complex business processes on the Corda network. Flows simply define the steps required to complete a specific business process, such as a trade or a settlement and they use a messaging system to allow communication and updates between relevant parties. Flows are designed to be modular, meaning that each step in the flow can be executed independently and in parallel with other steps, which makes Corda efficient, with fast processing times.
