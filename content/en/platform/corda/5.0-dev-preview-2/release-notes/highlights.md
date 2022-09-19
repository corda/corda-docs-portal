---
date: '2022-06-29'
title: "Highlights"
draft: true
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-release-highlights
    parent: corda-5-dev-preview-release-notes
    weight: 10
section_menu: corda-5-dev-preview
---

Corda 5 Developer Preview (DP) 2 is a developer preview of the next major iteration of Corda, Corda 5. While this version enables you to solve the same problems as Corda 4, the new Corda 5 architecture and deployment methods are designed to deliver high availability and scalability. You care read more about the architecture of Cora 5 [here](../getting-started/architecture/architecture.html). Intended for local deployment, experimental development, and testing only, this preview includes:

*Brief paragraph of each of the highlights*

## Feature 1



## Feature 2

[..a virtual node is the virtual mapping between application processes, data and identity and keys to form the logical equivalent of a Corda 4 node (such as Alice in Network 1 with App A/B/C)...]: #

[enabling true (virtual) node multi-tenancy on a shared cluster - this is important for managed service providers or developers looking at progressive decentralisation. 2. enabling multi-network - Alice can join several application networks using the same “client” at no margin cost.3.reducing cost of ownership -  particularly for operating models where previously multiple nodes were deployed 4. improving development/test experience - particularly for production-like tests, dynamic configuration of a cluster (with several virtual nodes) allows for a much faster and simpler test set up/ run time. 5. Finally — as virtual nodes are just a mapping between processes, data, and keys, they can be…. portable. Virtual nodes makes it easy to join multiple networks. Rather than having multiple Corda deployments you can have multiple virtual nodes, allowing you to be easily represented in each network with separate identities.]: #
