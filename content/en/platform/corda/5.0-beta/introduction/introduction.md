---
date: '2020-07-15T12:00:00Z'
title: "Introduction"
menu:
  corda-5-beta:
    identifier: corda-5-beta-intro
    weight: 1050
section_menu: corda-5-beta
---

{{< warning >}}
Corda 5.0 Beta is, as the name suggests, a pre-release version for testing purposes only.
If you are not part of the Beta programme, the Corda 5.0 Beta documentation is for information only.
R3 will be running a public Beta program for Corda 5.0 beginning in 2023. Contact R3 to register your interest.
{{< /warning >}}

Corda is a platform that enables you to build permissioned networks, create applications that solve a business problem that requires parties to come to some agreement, and interact in a completely secure ecosystem. Corda 5 was designed with an understanding that it is the job of a platform to serve those running software on it.

For developers, Corda 5 is an accessible toolbox with well-defined layers that enables you to create solutions. It does not force complexity or concepts, but gives a streamlined iteration for the testing and development loop. It is supported by RESTful APIs

As an operator of a network, Corda 5 places the control in your hands, acknowledging that the rules governing access to a network are best set and managed by you. Deployments can match the scale of the problem and then grow and adapt as it changes. It is cloud-native; behaving as any other modern application, with the tooling to match.

## Start Small

Corda 5 is designed to enable anyone to start small and scale as needed. An entire application network can run on a single laptop, with many self-sovereign identities sharing the compute resources. When required, Corda supports scaling out to the data center, enabling true decentralization of execution as identities progressively move to their own clusters. The network grows without losing control over what is important; i.e., the rules allowing people into the network and the rules governing the exchange of information. Corda 5 can handle running ten identities or many thousands of them.

## Highly Available

The worker architecture means that Corda 5 can be deployed in a Hot-Hot/Active-Active configuration, which ensures continuity of execution under fault scenarios. If a worker crashes, another can pick up the checkpointed flow and continue execution.

## Scale Out

The architecture enables horizontal scaling to facilitate parallel execution of thousands of flows. Capacity can be added or removed as needed via the scaling of the worker community.

## No Work - No Cost

Identities are not tied to a single executing compute instance. When idle, aside from some small costs associated with static storage, identity does not incur overhead. This allows the interleaving of many identities on a much smaller system than previously available, dramatically reducing the cost per identity.

## Progressive Decentralization
True decentralization is difficult. Attempting to force it on people or industries too soon results in friction of adoption. Corda 5, with its concepts of *virtual nodes*, allows for what we term *progressive decentralization*. That is, systems that allow themselves to start in a managed, centralized fashion, whilst retaining digital sovereignty, which allows migration of those nodes to their own infrastructure when the time is right.

## A Global Database

One of the standard models for describing Corda has been that of a global database where the rules for updating rows and columns are encapsulated within a smart contract. This smart contract defers control to those who currently hold access to those elements, without requiring input from a central point of control. Only those who need to see or have access to a record have it. The evolution of that record is constrained in the ways that the initator felt was appropriate.

Corda 5 changes this model slightly, as it brings the concept of *schemas* to that global model. While in earlier versions, all applications could evolve all records, this required all applications to have knowledge of the rules of all other applications. Essentially, it is possible to build an application in this way, but the complexity soon spirals out of control and the ability to make mistakes increases.

Corda 5, through the concept of *application networks*, introduces schemas into that database. Applications can still interact with any record. However, now they must go through an interoperability layer that removes the need for them to understand the inner workings of the other application. A schema puts rules in place as to how others can mutate the global state of another chain in a much cleaner, easier way than before.
