---
aliases:
- /docs/corda-enterprise/head/index.html
- /docs/corda-enterprise/index.html
date: '2020-04-07T12:00:00Z'
menu:
  versions:
    weight: 10
  corda-enterprise-4-6:
    weight: 1
    name: Corda Enterprise Edition 4.6
project: corda
section_menu: corda-enterprise-4-6
title: Corda Enterprise Edition 4.6
version: 'Enterprise 4.6'
---

# Introduction to Corda

A Corda Network is a peer-to-peer network of [Nodes](../../../../../en/platform/corda/4.6/enterprise/node/component-topology.html), each representing a party on the network.
These Nodes run Corda applications [(CorDapps)](../../../../../en/platform/corda/4.6/enterprise/cordapps/cordapp-overview.html), and transact between Nodes using public or
confidential identities.

When one or more Nodes are involved in a transaction, the transaction must be notarised. [Notaries](../../../../../en/platform/corda/4.6/enterprise/notary/ha-notary-service-overview.html) are a specialised type
of Node that provides uniqueness consensus by attesting that, for a given transaction, it has not already signed other
transactions that consumes any of the proposed transaction’s input states.

{{< note >}}
**Release notes**

* For the latest Corda Enterprise release notes, see the [Corda Enterprise Edition 4.6 release notes](../../../../../en/platform/corda/4.6/enterprise/release-notes-enterprise.md) page. You can view release notes for previous versions of Corda Enterprise in the relevant documentation section for each version, accessible from the left-hand side menu.
* For all Corda open source release notes, see the [Corda release notes](/en/archived-docs/corda-os/4.6/release-notes.md) page.
* For all Corda Enterprise Network Manager release notes, see the [Corda Enterprise Network Manager release notes](../../../../../en/platform/corda/1.4/cenm/release-notes.md) page.
{{< /note >}}

## Corda Enterprise

Corda Enterprise is a commercial edition of the Corda platform, specifically optimised to meet the privacy, security and
throughput demands of modern day business. Corda Enterprise is interoperable and compatible with Corda open source and
is designed for organisations with exacting requirements around quality of service and the network infrastructure in
which they operate.

Corda Enterprise contains all the core Corda functionality, but also includes the [Corda Firewall](../../../../../en/platform/corda/4.6/enterprise/node/corda-firewall-component.html),
support for high-availability Node and Notary deployments, and compatibility with hardware security modules [(HSMs)](../../../../../en/platform/corda/4.6/enterprise/node/operating/cryptoservice-configuration.html).

## Corda Enterprise vs Corda open source: feature comparison

More details on Corda Enterprise features compared to Corda open source features follow below.

### Corda Functionality

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Corda ledger|&#10003;|&#10003;|
|Flow framework|&#10003;|&#10003;|
|Immutable states|&#10003;|&#10003;|
|Vault|&#10003;|&#10003;|
|Smart contracts|&#10003;|&#10003;|
|Atomic transactions (with input, output and reference states)|&#10003;|&#10003;|
|Multiple accounts|&#10003;|&#10003;|
|Supported development languages|Java, Kotlin|Java, Kotlin|
|Standard Corda APIs|&#10003;|&#10003;|
|Compatible with any Corda network (including the Corda Network)|&#10003;|&#10003;|

{{< /table >}}

### Node

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Single node|&#10003;|&#10003;|
|Multiple nodes for high availability/disaster recovery|&#10007;|&#10003;|

{{< /table >}}

### Connectivity

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|In-process Artemis MQ|&#10003;|&#10003;|
|External Artemis MQ|&#10007;|&#10003;|
|Corda firewall|&#10007;|&#10003;|
|Multi-node use of a shared external Artemis MQ and a shared Corda firewall|&#10007;|&#10003;|

{{< /table >}}

### Key storage

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Java keystore file|&#10003;|&#10003;|
|HSM support|&#10007;|&#10003;|

{{< /table >}}

### Vault databases

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|H2 (development use only)|&#10003;|&#10003;|
|Postgres|&#10003; Please note that this has been harmonised with Corda Enterprise in Corda 4.5 to allow for in-place upgrades|&#10003;|
|SQL Server|Experimental only|&#10003;|
|Oracle|&#10007;|&#10003;|

{{< /table >}}

### Notaries

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Simple notary|&#10003;|&#10003;|
|Oracle RAC connectivity|&#10007;|&#10003;|
|CockroachDB connectivity|&#10007;|&#10003;|
|Clustered notary (for high availability)|&#10007;|&#10003;|

{{< /table >}}

### Performance

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Dynamic database caching and performance enhancements|&#10007;|&#10003;|
|Multi-threaded flow state machine|&#10007;|&#10003;|

{{< /table >}}

### Tooling

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Node health check tool|&#10007;|&#10003;|
|Configuration obfuscation tool|&#10007;|&#10003;|
|HA admin tool|&#10007;|&#10003;|

{{< /table >}}

### Support

{{< table >}}

|Feature|Corda open source|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Developer mailing lists (no SLA)|&#10003;|&#10003;|
|Cordaledger slack (no SLA)|&#10003;|&#10003;|
|Software maintenance|&#10007;|&#10003;|
|Support by R3 Support Engineering|&#10007;|&#10003;|
|Access to R3 Professional Services|Upgrading to Corda Enterprise only |&#10003;|

{{< /table >}}
