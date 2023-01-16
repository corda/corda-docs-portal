---
aliases:
- /releases/3.0/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: 60
project: corda-enterprise
section_menu: corda-enterprise-3-0
title: Corda Enterprise 3.0
version: '3.0'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Corda Enterprise 3.0

Welcome to the documentation website for **Corda Enterprise 3.0**, based on the Corda 3.1 open source release. Corda Enterprise adds:


* High performance, thanks to multi-threaded flow execution and extensive tuning.
* Support for more database backends:>

    * SQL Server 2017
    * Azure SQL
    * Oracle 11g RC2
    * Oracle 12c
    * PostgreSQL 9.6



* The Corda Firewall, for termination of TLS connections within your network’s DMZ.
* High availability features to support node-to-node failover.
* Support for advanced database migrations.

You can learn more in the [Release notes](release-notes.md).

Corda Enterprise is binary compatible with apps developed for the open source node. This docsite is intended for
administrators and advanced users who wish to learn how to install and configure an enterprise deployment. For
application development please continue to refer to [the main project documentation website](https://docs.corda.net/).

{{< note >}}
Corda Enterprise provides platform API version 3, which matches the API available in open source Corda 3.x releases.
Although the shipped JARs may contain new classes and methods that do not appear in API level 3, these should be considered
preliminary and not for use by application developers at this time.

{{< /note >}}


Corda Enterprise

* [Hot-cold deployment](hot-cold-deployment.md)
* [Database Management](database-management.md)
* [Corda Firewall](corda-firewall.md)




Development

* [Quickstart](quickstart-index.md)
* [Key concepts](key-concepts.md)
* [CorDapps](building-a-cordapp-index.md)
* [Tutorials](tutorials-index.md)
* [Tools](tools-index.md)
* [Node internals](node-internals-index.md)
* [Component library](component-library-index.md)
* [Serialization](serialization-index.md)
* [JSON](json.md)
* [Troubleshooting](troubleshooting.md)




Operations

* [Nodes](corda-nodes-index.md)
    * [Node structure](node-structure.md)
    * [Creating nodes locally](generating-a-node.md)
    * [Running nodes locally](running-a-node.md)
    * [Deploying a node](deploying-a-node.md)
    * [Node configuration](corda-configuration-file.md)
    * [Client RPC](clientrpc.md)
    * [Shell](shell.md)
    * [Node database](node-database.md)
    * [Node administration](node-administration.md)
    * [Node upgrades](node-operations-upgrading.md)


* [Networks](corda-networks-index.md)
    * [Setting up a Corda network](setting-up-a-corda-network.md)
    * [Network permissioning](permissioning.md)
    * [Network Map](network-map.md)
    * [Versioning](versioning.md)
    * [Supported cipher suites](cipher-suites.md)


* [Azure Marketplace](azure-vm.md)
    * [Pre-requisites](azure-vm.md#pre-requisites)
    * [Deploying the Corda Network](azure-vm.md#deploying-the-corda-network)
    * [Using the Yo! CorDapp](azure-vm.md#using-the-yo-cordapp)
    * [Viewing logs](azure-vm.md#viewing-logs)
    * [Next Steps](azure-vm.md#next-steps)


* [AWS Marketplace](aws-vm.md)
    * [Pre-requisites](aws-vm.md#pre-requisites)
    * [Deploying a Corda Network](aws-vm.md#deploying-a-corda-network)
    * [Build and Run a Sample CorDapp](aws-vm.md#build-and-run-a-sample-cordapp)
    * [Next Steps](aws-vm.md#next-steps)


* [Certificate Revocation List](certificate-revocation.md)
    * [HTTP certificate revocation protocol](certificate-revocation.md#http-certificate-revocation-protocol)
    * [Node Configuration](certificate-revocation.md#node-configuration)
