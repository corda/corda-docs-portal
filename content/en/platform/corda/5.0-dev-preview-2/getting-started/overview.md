---
date: '2020-07-15T12:00:00Z'
title: "Getting started"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-gettingstarted
    weight: 2000
section_menu: corda-5-dev-preview
---

What is Corda 5??? multi-tenancy - host multiple virtual nodes on one deployment of Corda - enabled by sandboxing
cross-ref to architecture section
* a more application centric model. - optimising the platform around a user journey that starts from the developer and puts applications at the center, rather than starting layering abstractions starting from the node and working our way up to a business network.
* Applications networks are now simplified Corda networks. They are still permissioned and the run time responsibilities of membership management moves from a dedicated series of services (Corda Enterprise Network Manager) to a simple, extensible application running on a node — removing the need to run dedicated infrastructure to manage a network of peers.
* We have rewritten our APIs to be interface-based and modular.

An intro to the basics needed to get started with Corda 5.
* Prerequisites
* Installing Corda

A Corda Network is a peer-to-peer network of Nodes , each representing a party on the network. These Nodes run Corda applications (CorDapps) , and transact between Nodes using public or confidential identities.

Corda is a ...
Corda has been completely redesigned for version 5.
