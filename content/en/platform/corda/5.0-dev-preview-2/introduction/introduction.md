---
date: '2020-07-15T12:00:00Z'
title: "Introduction"
menu:
  corda-5-dev-preview2:
    identifier: corda-5-dev-preview-intro
    weight: 1050
section_menu: corda-5-dev-preview2
---

Corda is a platform that enables you to build permissioned blockchain networks, create applications that solve a business problem requiring parties to come to some agreement, and interact in a completely secure ecosystem.
Corda 5 was designed with an understanding that it is the job of a platform to serve those running software on it.

As a developer, Corda 5 is an accessible toolbox with well-defined layers that enables you to create solutions.
It does not force complexity or concepts, but rather it gives a streamlined iteration for the testing and development loop. It is drivable by standard, restful APIs.

As an operator of a network, Corda 5 places the control in your hands, acknowledging that the rules governing access to a network are best set and managed by the operator. Deployment can match the scale of the problem and then grow and adapt as the problem changes. It is cloud-native; behaving as any other modern application, with the tooling to match.

## Start Small
Corda 5 is designed to enable anyone to start small and scale as needed. An entire application network can run on a single laptop, with many self-sovereign identities sharing the compute resources. When required, Corda 5 supports scaling out to the data center, enabling true decentralization of execution as identities progressively move to their own clusters. The network grows without losing control over what is important; i.e. the rules allowing people into the network and the rules governing the exchange of information. Whether running ten identities or many thousands, Corda 5 handles it.

## Highly Available
The worker architecture means that Corda 5 can be deployed in a HH/AA configuration, which ensures continuity of execution under fault scenarios. If a worker crashes, another can simply pick up the check-pointed flow and continue execution.

## Scale Out
That architecture enables horizontal scaling to facilitate parallel execution of thousands of flows. It has the ability to add or remove capacity as required, via the scaling of the worker community.

## No Work, No Cost
Identities are not tied to a single executing compute instance when idle. Aside from some small costs associated with static storage, identity does not incur overhead. This allows the interleaving of many identities on a much smaller system than previously available, which dramatically reduces the cost per identity.

## Progressive Decentralisation
