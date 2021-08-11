---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-notary-operate
tags:
- scaling
- notary
- cluster
title: Scaling a notary cluster
weight: 8
---


# Scaling a notary cluster

As described in the [Corda Enterprise notary service overview](ha-notary-service-overview.md), a HA notary cluster is made up of two main components, each of which can be scaled
up or down to facilitate the operators needs.


## Scaling the notary worker cluster

A notary Corda node can be added or removed to horizontally scale the worker cluster. This involves adding a new worker node along with an
accompanying DB. Note that this is separate from scaling the DB cluster - see section below on [Scaling up the DB cluster](#scaling-up-the-db-cluster) for more
information.

Scaling the worker cluster can have several benefits:
* Possibly performance increase - If the bottleneck in the system is the speed at which the workers can process and relay the messages to


the DB cluster, then adding a worker node can increase performance.



* Increased resiliency - More worker nodes means increased tolerance to single node failures.

A large cluster can also have some drawbacks, mainly:
* Increasing bottleneck - If the underlying DB cluster is the bottleneck in the system then adding another worker node will not improve


performance, and could even hinder it via increasing the requests to the DB.



* Unnecessary cost and maintenance - A large cluster can increase the running costs and maintenance without providing any significant
improvement in performance or resiliency.


### Steps to add a worker


* Setup the worker’s individual DB
* Copy the notary identity key store over to the new node to ensure the worker shares the same service identity as the other workers.
* Ensure the node configuration specifies the shared Notaries service legal name.
* Register with the identity manager.
* Start the node.


### Steps to remove a worker

As the HA Notary is designed to be able to handle notary worker nodes going down, removing a worker is simply a case of tearing down the
node and associated DB (not the DB cluster).


## Scaling up the DB cluster

Alternatively, the underlying DB cluster can be scaled up and down. In general, scaling the DB cluster up will increase resiliency, but at
the cost of decreased performance. Detailed steps to achieve this is out of scope for this document. Please refer to the documentation of
the underlying DB cluster provider.

