---
date: '2020-07-15T12:00:00Z'
title: "Introduction"
menu:
  corda-5-dev-preview2:
    identifier: corda-5-dev-preview-intro
    weight: 1050
section_menu: corda-5-dev-preview2
---

Corda is a platform that enables you to build permissioned blockchain networks, create applications that solve a business problem that requires parties to come to some agreement, and interact in a completely secure ecosystem.
Corda 5 was designed with an understanding that it is the job of a platform job to serve those running software on it.

As a developer, Corda 5 is an accessible toolbox with well-defined layers for you to pull a solution together.
It does not force complexity or concepts but gives a streamlined iteration for the testing and development loop.
It is drivable by standard, restful APIs.

As an operator of a network, Corda 5 places the control in your hands, acknowledging that the rules governing access to a network are best set and managed by the operator. Deployment can match the scale of the problem and grow and adapt as that changes.
It is cloud-native, behaving as one would expect any modern application to with the tooling to match.

## Start Small
Corda 5 is designed to enable anyone to start small and scale as needed. An entire application network can run on a single laptop, with many self-sovereign identities sharing the compute resources. When required, Corda supports scaling out to the data center, allowing true decentralization of execution as identities progressively move to their own clusters. The network grows without losing control over what is important; the rules allowing people into the network and the rules governing the exchange of information. Whether running ten identities or many thousands, Corda 5 handles it.

## Highly Available
The worker architecture means Corda 5 can be deployed in a HH/AA configuration that ensures continuity of execution under fault scenarios. If a worker crashes, another can simply pick up the check-pointed flow and continue execution.
## Scale Out
That same architecture allows horizontal scaling to facilitate the parallel execution of thousands of flows, with capacity able to be added and removed as needed through the scaling of the worker community.

## No Work, No Cost
Identities are not tied to a single executing compute instance, when idle, aside from some small costs associated with static storage, identity doesn’t incur overhead. This allows the interleaving of many identities on a much smaller system than previously available, dramatically reducing the cost per identity.

## Progressive Decentralisation
True decentralisation is hard, whilst the end state for many systems attempting to force it on people or industries too soon just relates in friction of adoption. Corda 5 with its Virtual Node concept allows for what we term progressive decentralisation. That is systems that allow themselves to start in a manged, centralized fashion, whilst retaining digital sovereignty that then allows migration of those nodes onto their own infrastructure when the time is right.

## A global database
One of the “go to” models for describing Corda has been that of one big global database where the rules for updating rows and columns are encapsulated within a smart contract that defers control to those who currently hold access to those elements without requiring input from a central point of control. Only those who need to see or have access to a record do so, and the evolution of that record is constrained in the ways the initator felt was apropriate.

Corda 5 changes this model slightly as it brings the concept of schemas to that global model. Where as in earlier versions, all applications could evolve all records, this required all applications have knowledge of all other applications rules. Essentially, it is possible to build an application in this way, but the complexity soon spirtals out of control and the ability to make mistakes compounds.

Corda 5, through Applicaiton Netowkrs, introduces scehmas into that Database. Apps can still interact with any record, only now they must go through an interoperability layer that removes the need for themto understand the inner workings of the other app. That scheams puts rules in place as to how others can mutate the global state of another chain in a much cleaner, easier to reason about, way than before.
