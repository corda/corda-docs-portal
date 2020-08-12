---
aliases:
- /releases/4.3/release-notes-enterprise.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-release-notes-enterprise
    weight: 20
tags:
- release
- notes
- enterprise
title: Release notes
---


# Release notes

## Corda Enterprise 4.3.4


Corda Enterprise 4.3.4 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise 4.3.3.


### Upgrade recommendation


As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](https://docs.corda.net/docs/corda-enterprise/release-notes-index.html).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issues listed below are relevant to your work.


### Fixed issues

* The handling of default cases in Vault Query has been checked for consistency.
* The CPU usage of the `NodeMeteringBackground` process has been decreased.
* The memory management for `AttachmentClassLoader` and `AttachmentURLStreamHandlerFactory` has been improved.
* `hashLookup` command help has been corrected.
* A security update to prevent AMQP header spoofing has been applied.


## Corda Enterprise 4.3.3


Corda Enterprise 4.3.3 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise 4.3.1 and a fix to a new issue related to a recent third-party dependency update.


### Upgrade recommendation


As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](https://docs.corda.net/docs/corda-enterprise/release-notes-index.html).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issues listed below are relevant to your work.


### Fixed issues

* A recent JDK update has broken the way we used delegated signatures for TLS (Transport Layer Security) handshakes. We have fixed this issue through patches on all affected Corda Enterprise versions (4.2+) to allow users to upgrade to the latest versions of compatible JDK distributions. If you have not upgraded to one of the patched releases yet, do not upgrade to Java 8 version `8u252` or higher.
* Fixed an issue that prevents operations run on the node’s external thread pool from being executed multiple times [[CORDA-3686](https://r3-cev.atlassian.net/browse/CORDA-3686)].
* Database indexes have been added for the `NODE_MESSAGE_IDS` and `VAULT_STATES` table to speed up frequently-used queries.
* A number of problems with the JPA notary have been addressed:
    * Ensure that notarisation succeeds when committing large batches of states using CockroachDB.
    * Prevent database connection leak on unexpected DB exceptions.
    * Prevent incorrect handling of scenarios where a successful transaction containing an input state and an unspent reference state is retried.
* Resolved a race condition in `FlowLogic.waitForLedgerCommit`.
* Fixed an issue in the [IRS sample app](contract-irs.md) where a checkpoint could not be restored.
* Made `recordTransaction` idempotent, preventing constraint violation errors when trying to add a transaction that is already in the vault.
* Fixed an issue to prevent notarisation batches containing duplicate transactions from getting stuck.
* Fixed an issue to allow the CRaSH shell to use the built-in "dashboard" command in a safe way.
* Published the metering collection tool as part of the Corda Enterprise distribution.
* Fixed an issue in DNS resolution when using the Corda Health Survey.
* Fixed an issue to allow the Corda Health Survey Tool to follow HTTP to HTTPS redirects when resolving Identity Manager/Network Map addresses.


## Corda Enterprise 4.3.1

Corda Enterprise 4.3.1 is a patch release of Corda Enterprise that includes fixes for several issues identified post development of Corda Enterprise 4.3.

We recommend that developers upgrade to the latest version of Corda as soon as possible. Node operators should upgrade if they believe they might be affected by one or more of the issues listed below.


### Issues Fixed


* Functionality of CollectSignaturesFlow restored to 4.2 behaviour [[CORDA-3485](https://r3-cev.atlassian.net/browse/CORDA-3485)]
* Creation of CordaRPCClient hangs [[CORDA-3501](https://r3-cev.atlassian.net/browse/CORDA-3501)]
* Scanning for Custom Serializers in the context of transaction verification doesn’t work [[CORDA-3464](https://r3-cev.atlassian.net/browse/CORDA-3464)]
* JPA notary doesn’t work with the Oracle recommended JDBC driver
* RPC client retries failed operation with java.io.NotSerializableException
* Node is unable to start up with RSA based TLS key


## Corda Enterprise 4.3

This release extends the [Corda Enterprise 4.2 release](https://docs.corda.net/docs/corda-enterprise/4.2/release-notes-enterprise.html) with new mission-critical enterprise capabilities to enhance support for HSM (hardware security module) signing devices and improved logging for profiling time spent outside of Corda.

Corda Enterprise 4.3 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. Please refer to product documentation for details.

Corda Enterprise 4.3 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.2, 4.1, 4.0 and 3.x, while providing enterprise-grade features and performance.

{{< note >}}
The compatibility and interoperability assurances apply to nodes running at the latest patch level for any given integer version.
For example, at the time of writing, the Corda Enterprise 4.3 interoperability and compatibility assurance is with respect to X, Y, Z.

{{< /note >}}

### Key new features and components


#### Corda Health Survey

To support operators with node commissioning tasks, we have introduced a number of improvements to the Corda Health Survey tool. The tool now provides:


* Basic connectivity checks on HTTP endpoints (Doorman, Network map) and firewall components (Bridge, Float)
* Sanity checking of node and firewall configuration files


#### JPA notary interface

Corda Enterprise 4.3 introduces a Java Persistence API (JPA) interface for highly-available notaries. This allows the notary
operator to fully configure which backend database their notary workers connect to in order to store consensus results.

The supported databases when using this interface are CockroachDB 19.1.2 and Oracle RAC 12cR2.

For more information, see [Configuring the notary backend - JPA](running-a-notary-cluster/installing-jpa.md).


#### Notary key storage

The shared key that is used by a highly-available notary cluster can now be stored in Securosys and Azure Keyvault HSMs. In a highly available notary configuration, multiple notary workers are able to share a single HSM.


#### Support for Metering

Allows node operators to understand the amount of signing events which have taken place within the node. All the information is collected and stored locally. At no point is the information exposed to any network participants or R3.

Learn more at: [https://docs.corda.net/docs/corda-enterprise/4.3/metering-collector.html](https://docs.corda.net/docs/corda-enterprise/4.3/metering-collector.html)


#### Hardware Security Module (HSM) improvements

Corda Enterprise 4.3 gracefully handles instances where one or all HSMs are not available. This addresses where both the HSM fails or there is an HSM session timeout either at node start-up or during node operation.
Additionally, users can now use HSMs to store the TLS keys used in p2p connections between the Node and a standalone Artemis MQ


#### Improved database migration tooling

Improved tooling for monitoring progress and managing outcomes of database migrations.


#### Corda Firewall Improvements

In previous versions of Corda Enterprise, nodes running the Corda Firewall checked the CRL endpoint directly through the Float. This ran counter to the Float’s original design (it should never perform outbound calls). In Corda Enterprise 4.3, the Float delegates the CRL check to the Bridge, which has the ability to perform outgoing communications either directly or via SOCKS/HTTP proxy.


#### Support for PostgreSQL 10.10 and 11.5


#### Optimisation of heap memory sizing

To help minimise the chance of out-of-memory errors, the default minimum heap size when devMode is set to false is now 4GB. This can be overridden via the node configuration or command-line argument.


### Deprecations

With the introduction of the notary JPA interface, we are deprecating Percona Server as a supported database for
highly-available notaries.


### Known issues

There are currently three known issues:


* The process that creates the *CordaRPCClient* requires more memory than in previous versions. It is recommended to increase the RPC memory allocation to 1024MB.
* In Corda Enterprise 4.3 *CollectSignaturesFlow* works slightly differently. In previous releases, any number of sessions with the same parties could be provided. In Corda Enterprise 4.3 one session for each of the relevant parties should be provided.
* Corda Enterprise 4.3 requires Gradle 5. Gradle 5 has reduced memory allocation, which can cause problems when running tests. Memory allocated to Gradle 5 must be explicitly increased.


### Upgrade notes

As per previous major releases, we have provided a comprehensive upgrade notes ([Upgrading CorDapps to Corda Enterprise 4.3](app-upgrade-notes-enterprise.md)) to ease the upgrade
of CorDapps to Corda Enterprise 4.3. In line with our commitment to API stability, code level changes are fairly minimal.

For **developers**, switching CorDapps built using Corda (open source) 4.x to Corda Enterprise 4.3 is mostly effortless,
and simply requires making the Corda Enterprise binaries available to Gradle, and changing two variables in the build file:

```shell
ext.corda_release_version = '4.3'
ext.corda_release_distribution = 'com.r3.corda'
```

For **node operators**, it is advisable to follow the instructions outlined in [Upgrading a Corda Node](node-upgrade-notes.md).

{{< note >}}
If the finance CorDapp is being used in a mixed-distribution network, the open source finance contract CorDapp should be deployed on both Corda 4.x (open source) and Corda Enterprise 4.3 nodes.

{{< /note >}}
Visit the [https://www.r3.com/corda-enterprise](https://www.r3.com/corda-enterprise/) for more information about Corda Enterprise.
Customers that have purchased support can access it online at  [https://support.r3.com](https://support.r3.com/).
