---
aliases:
- /releases/3.3/release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-release-notes
    parent: corda-enterprise-3-3-release-process-index
    weight: 1010
tags:
- release
- notes
title: Release notes
---


# Release notes

## Corda Enterprise 3.3.1

Corda Enterprise 3.3.1 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise 3.3.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](https://docs.corda.net/docs/corda-enterprise/release-notes-index.html).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* We have fixed a security issue relating to potential signature forgery. To do so, we have introduced batch signing capability in the `signTransactionAndSendResponse` of the `NotaryServiceFlow` flow so that a Merkle Tree is built with a single transaction to be signed, and then the transaction signature is constructed with the partial Merkle tree containing that single transaction.

## Corda Enterprise 3.3

Corda Enterprise 3.3 combines a selection of bug fixes in response to customer support tickets, miscellaneous fixes and
small improvements, and an important serialization framework update required to enable forwards compatibility with Corda 4 and Corda Enterprise 4.


### Key new features and components


* **Serialization engine update** [[CORDA-2422](https://r3-cev.atlassian.net/browse/CORDA-2422)]Adjusted the serialization process such that interfaces (included in the AMQP schema) are loaded on-demand only when they are needed (i.e. implemented by some class).
As a result, any interfaces coming from the future (i.e. version 4) will be ignored (if not used), thus maintaining interoperability between
this and future versions.
* **Improved Notary retry support**  [[CORDA-2304](https://r3-cev.atlassian.net/browse/CORDA-2304)]Client-side notarisation flows have special retry logic that enables failover in case a member of the notary cluster goes down while processing the request.
This release includes a fix that disables retries when talking to a single-node notary, as it does not provide any benefit.
Additionally, the maximum retry limit has been dropped, and notarisations will be retried indefinitely. This is to prevent potential transaction
loss in case of network issues or misconfiguration where the notary is unable to send back a response to the client.


### Customer fixes


* Duplicate message IDs seemingly not de-duplicated. [[ENT-2785](https://r3-cev.atlassian.net/browse/ENT-2785)]
* Perform de-duplicated message cleanup on node shutdown. [[ENT-2823](https://r3-cev.atlassian.net/browse/ENT-2823)]
* Fix a bug that prevents consecutive multiparty contract upgrades. [[CORDA-2109](https://r3-cev.atlassian.net/browse/CORDA-2109)]
* Completed flow got hospitalised during node shutdown. [[ENT-2949](https://r3-cev.atlassian.net/browse/ENT-2949)]
* V3 evolution with carpentry: We change the pipeline of TypeNotation resolution in processSchemas so that all local serializers
are found, and all types needing carpentry are synthesized, before we attempt evolution on any of them. [[CORDA-2314](https://r3-cev.atlassian.net/browse/CORDA-2314)]
* Transactions recorded in the wrong order can result in incorrect vault state [[CORDA-2402](https://r3-cev.atlassian.net/browse/CORDA-2402)]
* Disable DNS resolution of target addresses when connecting via a proxy.
* Adds a pipeline logger ahead of the proxy stage if trace is set. [[ENT-2693](https://r3-cev.atlassian.net/browse/ENT-2693)]
* Introduce option for HTTP proxy for outbound Bridge connectivity. [[ENT-2669](https://r3-cev.atlassian.net/browse/ENT-2669)]
* Introduce healthCheckPhrase which can be used for TCP Echo check. [[ENT-2636](https://r3-cev.atlassian.net/browse/ENT-2636)]
* Fixing the CRL issuer cert lookup. [[ENT-2706](https://r3-cev.atlassian.net/browse/ENT-2706)]
* Include PNM (private network map) ID in CSR. If a Compatibility Zone operator is using private networks and the node should be joining one,
optionally the ID (a UUID) of that network can be included as part of the node’s CSR to to the Doorman. [[CORDA-2113](https://r3-cev.atlassian.net/browse/CORDA-2113)]
* Fix to deserialization engine which can mix together the object trees of two threads when passing through evolution.
Problem manifested by Vault queries returning a state from other queries (when invoked concurrently via RPC client). [[ENT-2608](https://r3-cev.atlassian.net/browse/ENT-2608)]

Also includes a number of fixes to messaging logic to help with stabilization of customer environments: small fixes to artemis start, stop, disconnect and
acknowledge logic which has been shown to fix messaging stability in unreliable conditions. It also reduces retransmission of duplicate messages from the artemis journal.


### Miscellaneous improvements, additions and changes

Miscellaneous minor firewall fixes and troubleshooting aids:


* Suppress core.server.lambda$channelActive$0 - AMQ224088 errors from load balancers.
* Add ability to silence logging of messages associated with load balancer health checks in the bridge.
* Add ability to set proxy timeout in bridge.

Additional diagnostics logging support within Corda Firewall components.


### Upgrade notes

For **developers**, switching CorDapps built using Corda Enterprise 3.2 to Corda Enterprise 3.3 simply requires updating the Corda
Enterprise release version variable in the CorDapp’s main Gradle build file:

```shell
ext.corda_release_version = '3.3'
```


Please consult the comprehensive upgrade notes ([Upgrading a CorDapp to a new platform version](upgrade-notes.md)) for general upgrade guidelines for CorDapps built using
other versions of Corda. In line with our commitment to API stability, there are no code level changes required to upgrade
to Corda Enterprise 3.3 from the previous Corda Enterprise 3.2 release.

For **node operators**, it is advisable to follow the instructions outlined in [Upgrading a Corda Enterprise Node](node-operations-upgrading-enterprise.md).

Visit the [https://www.r3.com/corda-enterprise](https://www.r3.com/corda-enterprise/) for more information about Corda Enterprise.
Customers that have purchased support can access it online at  [https://support.r3.com](https://support.r3.com/).



## Corda Enterprise 3.2

Corda Enterprise 3.2 combines a selection of bug fixes in response to customer support tickets, miscellaneous fixes and
small improvements, and two important functional changes which enable the platform to evolve and scale in line with
industry standards and best practices.


### Key new features and components


* **Certificate Hierarchy**After consultation, collaboration, and discussion with industry experts, we have decided to alter the default Certificate Hierarchy (PKI) utilized by
Corda and the Corda Network. To facilitate this, the nodes have had their certificate path verification logic made much more flexible. All existing
certificate hierarchy, certificates, and networks will remain valid. The possibility now exists for nodes to recognize a deeper certificate chain and
thus Compatibility Zone operators can deploy and adhere to the PKI standards they expect and are comfortable with.Practically speaking, the old code assumed a 3-level hierarchy of Root -> Intermediate CA (Doorman) -> Node, and this was hard coded. From Corda Enterprise 3.2 onward an
arbitrary depth of certificate chain is supported. For the Corda Network, this means the introduction of an intermediate layer between the root and the
signing certificates (Network Map and Doorman). This has the effect of allowing the root certificate to *always* be kept offline and never retrieved or
used. Those new intermediate certificates can be used to generate, if ever needed, new signing certs without risking compromise of the root key.
* **Server Name Indication (SNI)**Server Name Indication provides an industry standard means of supporting operators of multiple nodes/identities that are
exposed to peer nodes through a restricted number of public IP addresses and ports. This future-proofing feature is
required to enable continued wire-level interoperability of existing Corda 3.x nodes with new SNI-enabled Corda 4.x Networks
(that will enable sharing of Corda Firewall across nodes; multi-identity support).


### Customer fixes


* NodeVaultService bug. Start node, issue cash, stop node, start node, getCashBalances() will not show any cash. [[ENT-2419](https://r3-cev.atlassian.net/browse/ENT-2419)]
* AMQP Channel Handler should handle hand-shake timeout exceptions as timeouts, not certificate errors. [[ENT-2391](https://r3-cev.atlassian.net/browse/ENT-2391)]
* Transaction failing to store correctly in tables, after transaction SQL failure. [[CORDA-1847](https://r3-cev.atlassian.net/browse/CORDA-1847)]
* Spring Boot related fix: proxy Serializers fail for Generics [[CORDA-1747](https://r3-cev.atlassian.net/browse/CORDA-1747)]
* Double flush: a flush is triggered inside a flush resulting in a *Unique index or primary key violation* [[CORDA-1866](https://r3-cev.atlassian.net/browse/CORDA-1866)]
* Change type of the checkpoint_value column to bytea to avoid database bloat on postgres [[CORDA-1813](https://r3-cev.atlassian.net/browse/CORDA-1813)]


### Miscellaneous improvements, additions and changes


* Updated repository lists to reduce dependency on Jitpack and removed unused repositories.
* Allow Corda’s shell to deserialise using generic type information. [[CORDA-1907](https://r3-cev.atlassian.net/browse/CORDA-1907)]
* Add Servlet 3.1 implementation into the WebServer. [[CORDA-1906](https://r3-cev.atlassian.net/browse/CORDA-1906)]
* Extend JSON deserialisation to handle Amount<T> for any T. [[CORDA-1905](https://r3-cev.atlassian.net/browse/CORDA-1905)]
* It is not possible to run stateMachinesSnapshot from the shell (fixed) [[CORDA-1681](https://r3-cev.atlassian.net/browse/CORDA-1681)]
* HPE MVP: NonStop fixes and ports of coin selection and Liquibase plugin [[ENT-2504](https://r3-cev.atlassian.net/browse/ENT-2504)]
* Full binary compatibility with all Open Source versions of the bundled finance CorDapp


### Upgrade notes

From a build perspective, switching CorDapps built using Corda Enterprise 3.1 to Corda Enterprise 3.2 simply requires updating the Corda
Enterprise release version variable in the CorDapps main Gradle build file:

```shell
ext.corda_release_version = '3.2'
```


Please consult the comprehensive upgrade notes ([Upgrading a CorDapp to a new platform version](upgrade-notes.md)) for general upgrade guidelines for CorDapps built using
other versions of Corda. In line with our commitment to API stability, there are no code level changes required to upgrade
to Corda Enterprise 3.2 from the previous Corda Enterprise 3.1 release.

Visit the [https://www.r3.com/corda-enterprise](https://www.r3.com/corda-enterprise/) for more information about Corda Enterprise.
Customers that have purchased support can access it online at  [https://support.r3.com](https://support.r3.com/).



## Corda Enterprise 3.1

Corda Enterprise 3 is the first official release of Corda Enterprise - a commercial distribution of the open source Corda blockchain platform, designed for mission critical enterprise deployments. It is operationally compatible with Corda 3.x release line while additionally providing enterprise-grade features and performance.

Corda Enterprise 3.1 resolves an issue that caused developer-mode certificates generated with Corda Enterprise 3.0 to fail revocation checks. See below for [more details](#improve).

Corda Enterprise 3.1 supports Linux for production deployments, with Windows and Mac OS support for development and demonstration purposes only.


### Key new features and components

**High Availability**


This release introduces the Hot-Cold High Availability configuration for Corda Enterprise nodes, which addresses the following requirements:


* A logical Corda node continues to be available as long as at least one of the clustered physical nodes is available.
* No loss, corruption or duplication of data on the ledger due to component outages.
* Continuity of flows throughout node failures.
* Support for rolling software upgrades in a live network.

See [here](hot-cold-deployment.md#hot-cold-ref) for further details on how to set-up and operate Hot-Cold node HA.


**Additional Supported SQL Databases**


[PostgreSQL 9.6](node-database.md#postgres-ref), [Azure SQL and SQL Server 2017](node-database.md#sql-server-ref) and [Oracle 11g and 12c](node-database.md#oracle-ref) are now supported SQL databases.
Database settings can be specified as part of the node configuration file.
See [Node database](node-database.md) for further details.


**Database Management and Migration Tool**


Corda Enterprise 3.1 ships with a tool for tracking, managing and applying database schema migrations.
A framework for data migration provides a way to upgrade the version of Corda Enterprise or installed CorDapps while preserving data integrity and service continuity. It is also used to prepare a database for first use with Corda Enterprise.
Based on [Liquibase](http://www.liquibase.org/), the tool also allows exporting DDL and data to a file, allowing DBAs to inspect the SQL or apply the SQL statements and to apply them manually if necessary.
See database migration for further details.


**Multi-threaded Flow Processing**


Corda Enterprise 3.1 enables multi-threaded processing of flows, resulting in vastly higher performance than Corda 3.0. In Corda flows are processed on a single thread and
thus individual flow steps are not processed concurrently. Corda Enterprise is able to process multiple flow steps concurrently, the number of which is only limited by
available CPU cores, memory and database configuration.  This allows Corda Enterprise to process a greater number
of flows and transactions in a given time frame than Open Source Corda and to truly take advantage of large server
/ VM configurations. The number of operating system threads that are used is determined by the `flowThreadPoolSize` configuration property.
See [Node configuration](corda-configuration-file.md) for further details.


**New Network Map Architecture**


This release introduces the new network map architecture. The network map service has been redesigned to enable future increased network scalability and redundancy, reduced runtime operational overhead,
support for multiple notaries, and administration of network compatibility zones (CZ) and business networks.

A Corda Compatibility Zone (CZ) is defined as a grouping of participants and services (notaries, oracles,
doorman, network map server) configured within an operational Corda network to be interoperable and compatible with
each other.
See [Network Map](network-map.md) and bootstrapping the network for further details.


**Corda Firewall**


Corda Enterprise 3.1 introduces the Bridge and Corda Firewall components to enable secure setup of a Corda Node in a DMZ environment.
See [Corda Firewall Overview](corda-firewall.md) for further details.


**Improved Operational Metrics**


Corda Enterprise 3.1 provides additional metrics compared to Corda. A richer collection of information is exported through JMX via Jolokia for monitoring.


**Operational Compatibility With Open Source Corda**


Corda Enterprise 3.1 provides a baseline for wire stability and compatibility with open-source releases of Corda from version 3.0 onwards.

It delivers forward compatibility with future versions of Corda Enterprise:


* Is operationally compatible with future versions of Corda Enterprise.
* Is upgradeable to future version of Corda Enterprise, preserving transaction and other data.

It delivers operational compatibility with open-source Corda:


* Can be used in networks seamlessly transacting with nodes running Corda 3.x and future versions.
* Can run CorDapps developed on Corda 3.x and future versions. Note that some database changes may be required to achieve this. See [Upgrade a Corda (open source) Node to Corda Enterprise](node-operations-upgrading.md) for more information.
* Is compatible with ledger data created using Corda 3.x and future versions.

Furthermore, the RPC client-server communications transport protocol is now fully AMQP based.


{{< note >}}
RPC clients communicating with Corda Enterprise nodes must be linked against the enterprise RPC client binaries, because open-source Corda *3.x* does not yet use the AMQP serialisation protocol for RPC communication.
From Corda open-source version *4.x* onwards, the RPC client binaries will be compatible with the enterprise distribution.

{{< /note >}}


### Further improvements, additions and changes


* This release addresses the issue in Corda Enterprise 3.0 which causes generated developer-mode certificates to fail revocation checks. It affects developer mode of operation of Corda Enteprise 3.0, i.e. production deployments of Corda Enterprise 3 and all Corda (open source distribution) releases are not affected. This issue can now be resolved by upgrading to Corda Enterprise 3.1 and regenerating any developer certificates that were used (e.g. via `deployNodes`).
* Built-in flows have been improved to automatically utilise the new ‘hospital’ and retry functionality. For example, the [FinalityFlow](api-contract-constraints.md#finality-flow-contract-constraints-ref) now enables a node operator to easily address contract constraints validation errors when using mixed CorDapp versions. Furthermore, flows will attempt to automatically replay from their last saved checkpoint when, for example, a race condition has occurred for writing into the database or a database deadlock has been encountered. Flows will also retry notarisation attempts if a Highly Available Notary cluster member does not respond within the acceptable time period. There are configuration options which affect the behaviour of the retry functionality. See [Node configuration](corda-configuration-file.md) for further details.
* Corda Enterprise 3.1 nodes will now fail to start if unknown property keys are found in configuration files. Any unsupported property can be moved to the newly introduced “custom” section. See [Node configuration](corda-configuration-file.md) for further details.
* Property keys with double quotes (e.g. *“key”*) in `node.conf` are no longer allowed. See [Node configuration](corda-configuration-file.md) for further details.
* Corda’s web server now has its own `web-server.conf` file, separate from the `node.conf` used by the Corda node. See [Node configuration](corda-configuration-file.md) for further details. *Note that this module is deprecated and we intend to remove it in the future.*
* Corda Enterprise 3.1 includes a new ‘Blob Inspector’ tool for viewing the contents of custom binary serialised files (such as `node-info`, `network-parameters`) in a human-readable format.
See [Blob Inspector](blob-inspector.md) for further details.
* Corda Enterprise 3.1 introduces additional network parameters (event horizon) and component run-time validation (maximum allowed message size).
The event horizon is the span of time that is allowed to elapse before an offline node is considered to be permanently gone.
* Corda Enterprise 3.1 adds certificate revocation list checking when running a node in a fully operational Corda Network environment backed by Network Services.
See [Certificate revocation list](certificate-revocation.md) for further details.
* Corda Enterprise 3.1 nodes support separate configuration parameters for specifying the location of the Doorman and the NetworkMap services independently of each other.
* RPC Server now masks internal errors in responses returned to RPC clients for enhanced privacy.
* Miscellaneous changes to the operation of the network bootstrapper tool, and node configuration changes.


### Known issues

The following list contains important known issues identified in this release. We will endeavour to fix these in future
releases of Corda.


* Certificate revocation revokes identities, not keys, and is currently irreversible. If your keys are lost or compromised,
new keys cannot be re-issued with the same X.500/legal entity name. It is strongly advised to backup your certificates
appropriately and to apply sensible policy for management of private keys.
* The finance CorDapp from Corda 3.0 and 3.1 cannot be used with Corda Enterprise 3.1.
In a mixed-distribution network the finance CorDapp from Corda Enterprise 3.1 should be deployed on both Corda 3.0/3.1 and Corda Enterprise 3.1 nodes.
This will be fixed in the next release of open source Corda.
* Explorer GUI does not display correctly HA notaries or multiple notaries.
* Certain characters in X500 party names prevent flows from being started from the shell [CORDA-1635].
* Missing configuration files for a network bootstrapper cause an exception [CORDA-1643].
Network bootstrapper should gracefully exit with a helpful error message.
* Java Lambda expressions with named parameters can cause flows to become not startable from shell [CORDA-1658].
* Some `java.time.*` types cannot be used in mapped (JPA) schemas [CORDA-1392].
* Corda Enterprise 3.1 does not support class evolution using non-nullable properties [CORDA-1702].


### Upgrade notes

As per previous major releases, we have provided a comprehensive upgrade notes ([Upgrading a CorDapp to a new platform version](upgrade-notes.md)) to ease the upgrade
of CorDapps to Corda Enterprise 3.1. In line with our commitment to API stability, code level changes are fairly minimal.

From a build perspective, switching CorDapps built using Corda 3.x to Corda Enterprise 3.1 is mostly effortless,
and simply requires making the Corda Enterprise binaries available to Gradle, and changing two variables in the build file:

```shell
ext.corda_release_version = '3.1'
ext.corda_release_distribution = 'com.r3.corda'
```


Visit the [https://www.r3.com/corda-enterprise](https://www.r3.com/corda-enterprise/) for more information about Corda Enterprise. Customers that have purchased support can access it online at  [https://support.r3.com](https://support.r3.com/).
