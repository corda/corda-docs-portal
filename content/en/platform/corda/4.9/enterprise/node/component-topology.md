---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-corda-nodes
    name: "Corda Nodes"
tags:
- node
- overview
- concept
title: What is a Corda node
weight: 30
---

A Corda node is an entity in a Corda network that usually represents one party in a business network. One party operates the node, which contains the CorDapps that the party uses to interact with other peers on the network.

This document contains:

* A description of node components.
* Node communication protocols.
* An example of typical node deployment architecture.

## What makes up a node?

Nodes represent parties in a network. They host and manage the operation of all the CorDapps the party uses to interact with other nodes. Each node runs within a Java Virtual Machine (JVM). Nodes have a public address, which serves as an endpoint for communication with other nodes in the network. To find a node's information on the network map, you can look up its X.509 name (called `myLegalName`) and key pair.

The key node components and services are:

* CorDapps
* A node configuration file
* The node database
* Node services
* The Corda firewall


{{< figure alt="node architecture" width=80% zoom="/en/images/node-architecture.png" figcaption="Node internal architecture.">}}

### CorDapps

CorDapps solve specific problems using the Corda framework. CorDapps are stored on Corda nodes and executed on the Corda network. From the perspective of a node operator, CorDapps are the functional element of Corda that define the operations and interactions of a business network.

CorDapps are installed on a node as JAR files located in the `cordapps` directory. For information on building and installing CorDapps on a node, see the [Building and installing CorDapps](../../../../../../en/platform/corda/4.9/enterprise/cordapps/cordapp-build-systems.md) documentation. For information on writing your own CorDapps, see the [CorDapp documentation](../../../../../../en/platform/corda/4.9/enterprise/cordapps/cordapp-overview.md).

### The node configuration file

The node configuration file is a single Human-Optimized Config Object Notation (HOCON) file that controls many aspects of a node. Node configuration files are hosted in the root node directory, and must be configured before the node can be started. Correctly configuring your node is an important part of optimizing the performance of your Corda solution.

You can find an exhaustive list of node configuration options and defaults in the [Node configuration reference](../../../../../../en/platform/corda/4.9/enterprise/node/setup/corda-configuration-fields.md) documentation, and an example configuration file in the [Node configuration](../../../../../../en/platform/corda/4.9/enterprise/node/setup/corda-configuration-file.md) documentation.

### Node database

All nodes require a relational SQL database to store operational data and the Corda vault. Corda supports a variety of node databases. See the [Platform support matrix](../../../../../../en/platform/corda/4.9/enterprise/platform-support-matrix.md) for a full list.

You can find a range of information in the tables on the node database. Some of the most important database tables are:

* Flow checkpoints: If the node encounters a problem during a flow, it can recover it from a checkpoint.
* Network parameters: Network parameters are the configuration settings of a business network, and are common to all parties on the network.
* States: States are outputs of transactions, and are stored in tables within the Corda Vault.
* Transactions: The node database stores all transactions that the node has created or used in transaction resolution.

### Node services

Nodes contain services that support the operation of Corda business networks. Some services are core node functions; others you can access through the `ServiceHub` API. CorDapps can access some node services using flows.

The key node services are:

* Key management and identity services
* Messaging and network management services
* Storage and persistence services
* Flow framework and event scheduling services

### Corda firewall

The Corda firewall is a CorDapp-level firewall and protocol break on all internet-facing endpoints. The firewall is made up of two components: the float and the bridge. The float handles inbound connections, while the bridge handles outbound connections.

The float safeguards the node by acting as the point of contact for all other parties. The float exposes a port and an address, which other parties on the network can connect to. When other parties connect to the float, the float bundles their messages and transmits them to the bridge across an internal firewall.

The bridge is the internal component of the firewall. It initiates all connections to the float, and runs health checks on the message bundles it receives before adding them to the node's Artemis queue.

## Node communication protocols

Nodes communicate with other nodes using asynchronous AMQP/TLS 1.2 protocols. HTTP communication is used for the initial registration of a node on a network, and for sharing the node address locations via the network map. JDBC is used for communications between the node and the vault.

Nodes communicate with client applications using RPC calls.

{{< figure alt="overview" width=80% zoom="../resources/overview.png" >}}


## Typical node deployments

In most cases, nodes are deployed with this architecture:

{{< figure alt="nodebridgefloat nbrs" width=80% zoom="../resources/nodebridgefloat_nbrs.png" figcaption="A typical node deployment.">}}

Most production deployments of Corda Enterprise include nodes, vaults, and firewalls.

The diagram highlights that:

1. CorDapps are the functional aspect of Corda that define the operations of a business network for a given use case.
2. Corda nodes store states in a database (the Vault) using JDBC.
3. Corda Nodes communicate in peer-to-peer fashion using AMQP/TLS 1.2.
4. The Corda firewall is an optional reverse proxy extension of the Corda node intended to reside in the DMZ, enabling secure AMQP/TLS 1.2 interaction with peer Corda nodes.
5. Client applications interact with Corda nodes using RPC/TLS 1.2.
6. Administrators interact with Corda nodes over SSH.
7. Corda nodes attain an identity certificate via a doorman service using HTTPS.
8. Corda nodes learn about other trusted Corda nodes and their addresses via a network map service using HTTPS.
9. Corda nodes and the Corda firewall check a certificate revocation list using HTTP/HTTPS.

## Related content

Learn more about:

* [The Corda firewall](../../../../../../en/platform/corda/4.9/enterprise/node/corda-firewall-component.md)
* [The node database](../../../../../../en/platform/corda/4.9/enterprise/node/operating/node-database.md)
* [Node configuration](../../../../../../en/platform/corda/4.9/enterprise/node/setup/corda-configuration-fields.md)
