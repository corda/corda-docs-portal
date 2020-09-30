---
date: '2020-06-18T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-ops-project-planning
tags:
- operations
- deployment
- planning
title: Node operator project planning
weight: 200
---

# Node operator project planning

A node operator is a member of a Corda business network, but does not operate any of the network services. A Corda Node
is the component that hosts CorDapps, and executes transactions with other network parties.

A Corda node is highly configurable, and care must be taken to correctly configure your node for best performance.

For more information on node configuration, see [node configuration](../../node/setup/node-naming.md/).

## Node sizing

When defining the requirements of a node, it is important to define the resources that the node will require. While every
Corda deployment will have different requirements - depending on the CorDapps and business model of the parties - the
following table gives approximate sizings for typical node deployments.

{{< table >}}

|Size|JVM Heap|# Cores|Minimum Host RAM|
|------------|---------|-------|----------------|
|Small|1GB|1|2GB to 3GB|
|Medium|4GB|8|8GB|
|Large|32GB|32|64GB|
|X-Large|> 32GB|> 32|> 64GB|

{{< /table >}}

## Node databases

All Corda Nodes have a database. A range of third-party databases are supported by Corda, shown in the following table:

{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|------------------------|
|Microsoft|x86-64|Azure SQL,SQL Server 2017|Microsoft JDBC Driver 6.4|
|Oracle|x86-64|11gR2|Oracle JDBC 6|
|Oracle|x86-64|12cR2|Oracle JDBC 8|
|PostgreSQL|x86-64|9.6, 10.10 11.5|PostgreSQL JDBC Driver 42.1.4 / 42.2.8|

{{< /table >}}

The node database stores all data required by the node, including CorDapps and state definitions.

To learn more about the node database, see [understanding the node database](../../node/operating/node-database.md).

## Testing and production environments

There are two key environments that a node operator must access or maintain, a production environment hosting the live
node, and a testing environment for testing CorDapp updates, node upgrades, or other network changes.

## Production environment

A production environment should contain the node, an HA implementation of the [Corda Firewall](../../node/corda-firewall-component.md/),
and an HSM that conforms to your organisation's security policies.

The Corda Firewall consists of the Float and Bridge components. A high-availability implementation of Corda Firewall
requires Zookeeper v3.5.4 running as an external cluster and both the Float and Bridge components running as external clusters.

The following HSMs are compatible with Corda Enterprise:

{{< table >}}

|Device|Legal Identity & CA keys|TLS keys|Confidential Identity keys|Notary service keys|
|-------------------------------|----------------------------|----------------------------|----------------------------|--------------------------|
| Utimaco SecurityServer Se Gen2| * Firmware version 4.21.1  | * Firmware version 4.21.1  | Not supported              | Not supported            |
|                               | * Driver version 4.21.1    | * Driver version 4.21.1    |                            |                          |
| Gemalto Luna                  | * Firmware version 7.0.3   | * Firmware version 7.0.3   | Not supported              | Not supported            |
|                               | * Driver version 7.3       | * Driver version 7.3       |                            |                          |
| FutureX Vectera Plus          | * Firmware version 6.1.5.8 | * Firmware version 6.1.5.8 | Not supported              | Not supported            |
|                               | * PKCS#11 version 3.1      | * PKCS#11 version 3.1      |                            |                          |
|                               | * FXJCA version 1.17       | * FXJCA version 1.17       |                            |                          |
| Azure Key Vault               | * Driver version 1.2.1     | * Driver version 1.2.1     | Not supported              | * Driver version 1.2.1   |
| Securosys PrimusX             | * Firmware version 2.7.4   | * Firmware version 2.7.4   | * Firmware version 2.7.4   | * Firmware version 2.7.4 |
|                               | * Driver version 1.8.2     | * Driver version 1.8.2     | * Driver version 1.8.2     | * Driver version 1.8.2   |
| nCipher nShield Connect       | * Firmware version 12.50.11| * Firmware version 12.50.11| Not supported              | Not supported            |
|                               | * Driver version 12.60.2   | * Driver version 12.60.2   |                            |                          |
| AWS CloudHSM                  | * Driver version 3.0.0     | * Driver version 3.0.0     | * Driver version 3.0.0     | Not supported            |

{{< /table >}}

## UAT environment

In many cases, a business network operator will run a UAT and provide access to that environment to the node operator.
However, node operators may also run their own UAT or QA environment.

The architecture of a QA or UAT environment should mirror the production environment as closely as possible, in order to
provide the best testing environment.
