---
aliases:
- /releases/3.0/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: -100
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
> 
>     * SQL Server 2017
>     * Azure SQL
>     * Oracle 11g RC2
>     * Oracle 12c
>     * PostgreSQL 9.6



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








Design docs

* [Design review process](design/design-review-process.md)
    * [Design doc template](design/template/design.md)


* [Certificate hierarchies](design/certificate-hierarchies/design.md)
    * [Overview](design/certificate-hierarchies/design.md#overview)
    * [Background](design/certificate-hierarchies/design.md#background)
    * [Scope](design/certificate-hierarchies/design.md#scope)
    * [Requirements](design/certificate-hierarchies/design.md#requirements)
    * [Design Decisions](design/certificate-hierarchies/design.md#design-decisions)
    * [**Target** Solution](design/certificate-hierarchies/design.md#target-solution)


* [Failure detection and master election](design/failure-detection-master-election/design.md)
    * [Background](design/failure-detection-master-election/design.md#background)
    * [Constraints/Requirements](design/failure-detection-master-election/design.md#constraints-requirements)
    * [Design decisions](design/failure-detection-master-election/design.md#design-decisions)
    * [Proposed solutions](design/failure-detection-master-election/design.md#proposed-solutions)
    * [Recommendations](design/failure-detection-master-election/design.md#recommendations)
    * [Conclusions](design/failure-detection-master-election/design.md#conclusions)


* [Float Design](design/float/design.md)
    * [Overview](design/float/design.md#overview)
    * [Scope](design/float/design.md#scope)
    * [Timeline](design/float/design.md#timeline)
    * [Requirements](design/float/design.md#requirements)
    * [Design Decisions](design/float/design.md#design-decisions)
    * [Target Solution](design/float/design.md#target-solution)
    * [Implementation plan](design/float/design.md#implementation-plan)


* [High availability support](design/hadr/design.md)
    * [Overview](design/hadr/design.md#overview)
    * [Requirements](design/hadr/design.md#requirements)
    * [Timeline](design/hadr/design.md#timeline)
    * [Design Decisions](design/hadr/design.md#design-decisions)
    * [Target Solution](design/hadr/design.md#target-solution)
    * [Implementation plan](design/hadr/design.md#implementation-plan)
    * [The Future](design/hadr/design.md#the-future)


* [High Performance CFT Notary Service](design/kafka-notary/design.md)
    * [Overview](design/kafka-notary/design.md#overview)
    * [Background](design/kafka-notary/design.md#background)
    * [Scope](design/kafka-notary/design.md#scope)
    * [Timeline](design/kafka-notary/design.md#timeline)
    * [Requirements](design/kafka-notary/design.md#requirements)
    * [Design Decisions](design/kafka-notary/design.md#design-decisions)
    * [Target Solution](design/kafka-notary/design.md#target-solution)
    * [Design Decisions](design/kafka-notary/design.md#id1)
    * [TECHNICAL DESIGN](design/kafka-notary/design.md#technical-design)
    * [Functional](design/kafka-notary/design.md#functional)
    * [Non-Functional](design/kafka-notary/design.md#non-functional)
    * [Operational](design/kafka-notary/design.md#operational)
    * [Security](design/kafka-notary/design.md#security)
    * [APPENDICES](design/kafka-notary/design.md#appendices)
    * [Kafka throughput scaling via partitioning](design/kafka-notary/design.md#kafka-throughput-scaling-via-partitioning)


* [Monitoring and Logging Design](design/monitoring-management/design.md)
    * [Overview](design/monitoring-management/design.md#overview)
    * [Background](design/monitoring-management/design.md#background)
    * [Scope](design/monitoring-management/design.md#scope)
    * [Requirements](design/monitoring-management/design.md#requirements)
    * [Design Decisions](design/monitoring-management/design.md#design-decisions)
    * [Proposed Solution](design/monitoring-management/design.md#proposed-solution)
    * [Complementary solutions](design/monitoring-management/design.md#complementary-solutions)
    * [Technical design](design/monitoring-management/design.md#technical-design)
    * [Software Development Tools and Programming Standards to be adopted.](design/monitoring-management/design.md#software-development-tools-and-programming-standards-to-be-adopted)
    * [Appendix A - Corda exposed JMX Metrics](design/monitoring-management/design.md#appendix-a-corda-exposed-jmx-metrics)
    * [Appendix B - Corda Logging and Reporting coverage](design/monitoring-management/design.md#appendix-b-corda-logging-and-reporting-coverage)
    * [Appendix C - Apache Artemis JMX Event types and Queuing Metrics.](design/monitoring-management/design.md#appendix-c-apache-artemis-jmx-event-types-and-queuing-metrics)





