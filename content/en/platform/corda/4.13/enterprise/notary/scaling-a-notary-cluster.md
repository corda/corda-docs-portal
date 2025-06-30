---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-13:
    parent: corda-enterprise-4-13-corda-nodes-notary-operate
tags:
- scaling
- notary
- cluster
title: Scaling a notary cluster
weight: 8
---


# Scaling a notary cluster

As described in [Notary service overview]({{< relref "ha-notary-service-overview.md" >}}), a HA notary cluster is made up of two main components, each of which can be scaled
up or down to facilitate the operators needs.


## Scaling the notary worker cluster

A notary Corda node can be added or removed to horizontally scale the worker cluster. This involves adding a new worker node along with an
accompanying database. Note that this is separate from scaling the database cluster - see section below on [Scaling up the database cluster](#scaling-up-the-database-cluster) for more
information.

Scaling the worker cluster can have several benefits:

- **Possibly performance increase:** If the bottleneck in the system is the speed at which the workers can process and relay the messages to the database cluster, then adding a worker node can increase performance.
- **Increased resiliency:** More worker nodes means increased tolerance to single node failures.

A large cluster can also have some drawbacks, mainly:

- **Increasing bottleneck:** If the underlying database cluster is the bottleneck in the system then adding another worker node will not improve performance, and could even hinder it via increasing the requests to the database.
- **Unnecessary cost and maintenance:** A large cluster can increase the running costs and maintenance without providing any significant
improvement in performance or resiliency.


### Adding workers

To add a worker:

1. Set up the worker’s individual database.
2. Copy the notary identity key store over to the new node to ensure the worker shares the same service identity as the other workers.
3. Ensure the node configuration specifies the shared notaries service legal name.
4. Register with the identity manager.
5. Start the node.


### Removing workers

As the HA Notary is designed to be able to handle notary worker nodes going down, removing a worker is simply a case of tearing down the
node and associated database (not the database cluster).


## Scaling up the database cluster

Alternatively, the underlying database cluster can be scaled up and down. In general, scaling the database cluster up will increase resiliency, but at
the cost of decreased performance. Detailed steps to achieve this is out of scope for this document. Please refer to the documentation of
the underlying database cluster provider.

