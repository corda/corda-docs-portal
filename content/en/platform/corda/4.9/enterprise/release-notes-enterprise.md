---
title: Corda Enterprise Edition 4.9 release notes
date: '2022-11-28'

menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-release-notes
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 1
---

# Corda Enterprise Edition 4.9 release notes

## Corda Enterprise Edition 4.9.5 release notes

Corda Enterprise Edition 4.9.5 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, see [Upgrading a CorDapp or node](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

### Fixed issues

* Previously, a memory leak in the transaction cache occurred due to weight of in-flight entries being undervalued. Improvements to prevent in-flight entry weights from being undervalued and estimated more correctly means a large decrease in the total size of cached entities. 

* A rare condition was found, when database transactions are rolled back under heavy load, that causes flow state machine threads to stop processing flows, leading to eventual node lock up in certain circumstances. This fix prevents this from happening.

## Corda Enterprise Edition 4.9.4 release notes

Corda Enterprise Edition 4.9.4 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, see [Upgrading a CorDapp or node](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

### Fixed issues

* The closing of AttachmentClassLoaders is now delayed until all SerializationContexts that refer to them have gone out of scope. This fixes an issue where they were being closed too early when evicted from the cache.
* Flow draining mode no longer acknowledges P2P in-flight messages that have not yet been committed to the database. Previously, flow draining mode acknowledged all in-flight messages as duplicate.
* A periodic check is now performed to determine if the state machine thread pool seems to be blocked. A warning is logged if the thread pool is blocked. A thread dump is now also logged periodically (every five minutes).

## Corda Enterprise Edition 4.9.3 release notes

Corda Enterprise Edition 4.9.3 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

### Fixed issues

The following issues were resolved in this patch release:

* Previously, both Corda Nodes certificates possessed Certificate Authority power because the CA attribute was set to true. The node registration tool now has a new  option, ```-C, --node-identity-cert-not-ca```, allowing a node legal identity certificate to be created where it is not a CA.

* For CENM 1.4+, the `getNodeInfos()` bulk fetch mechanism now retrieves NodeInfos from the network map via an HTTP proxy, if a proxy has been configured.

## Corda: Enterprise Edition 4.9.2 release notes

Corda Enterprise Edition 4.9.2 is a patch release of Corda Enterprise which includes the addition of a new Gradle 7 plugin, security upgrades, and fixes for minor bugs.

* As part of this patch a new Gradle plugin is provided that supports CorDapp development using Gradle 7. This is in addition to the existing Gradle support. The plugin has been uploaded to Artifactory.
  * Samples demonstrating Gradle 7 usage are available for:
    * [Kotlin](https://github.com/corda/samples-kotlin/tree/chrisr3-gradle7)
    * [Java](https://github.com/corda/samples-java/tree/chrisr3-gradle7)
  * A readme describing the Gradle 7 plugin is also available on [Github](https://github.com/corda/corda-gradle-plugins/tree/release/5.1/cordapp).
* Artemis messaging has been implemented to indicate when disk space is low (below 10%).
* AMQP frame tracing can now be enabled in the Corda node when running embedded Artemis or bridges. This is in addition to the previous ability to turn it on via firewall configuration.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

### Fixed issues

The following issues were resolved in this patch release:

* The `corda-shell --version` command has been updated to always return the correct version.
* The time it takes for first-time flows to be run in a signed CorDapp has been significantly reduced.
* Java serialization has been disabled in the Corda firewall, closing a potential security vulnerability.

### Third party component upgrades

{{< table >}}

|Library|Version 4.9.2|Previous version|
|---------|-------|-------|
|Caffeine|2.9.3|2.7.0-r3-fifty|
|Jackson|2.13.3|2.13.1|
|Netty|4.1.77.Final|4.1.68.Final|
|Quasar|0.7.15_r3|0.7.14_r3|
|Shiro|1.8.0|1.4.1|

{{< /table >}}

## Corda: Enterprise Edition 4.9.1 release notes

Corda Enterprise Edition 4.9.1 is a patch release of Corda Enterprise which includes dependency upgrades and fixes for minor bugs.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this patch release:

* Fixing of a bug where `SuspensionMeta` in `FlowInfo` shows as null even when a runnable flow has previously been hospitalized.
* Official Artemis binaries implemented.
* Oracle JDK version 8u322 now supported.

## Corda: Enterprise Edition 4.9 release notes

Corda: Enterprise Edition  4.9 features many security improvements, along with a stand alone Shell for controlling the node via command line. You can also now access the `flowrpcops` API.

* The `flowrpcops` API is available and documented. You can use this to start, pause, and retry flows and hospitalized flows.
* Access to node health data and node status.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda: Enterprise Edition  release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this release:

* Corda Shell has been removed to its own repository for improved security. You can now use a standalone shell outside of the node, or from within the node's drivers. You can read more about using the standalone shell [here](./node/operating/shell.html#the-standalone-shell). For information on adding the shell to the node's drivers, see [Upgrading a node to Corda Enterprise Edition 4.9](node-upgrade-notes.html).
* Security updates to prevent possibility of Denial of Service attacks.
* Improvements to demos and sample code.
* Improvements to improve compatibility with Intel Macs.
* An issue affecting Node JVM deadlocks is resolved.
* An issue with failed attachments from a notary has been fixed.
* An issue preventing attachments to subflows in certain circumstances has been fixed.

### Database Schema Changes

* The `node_named_identities` table has been re-introduced. It was removed in Corda Enterprise Edition 4.7 following updates to certificate rotation functionality.
  * The reintroduction of this table ensures the behavior of `rpcOps.wellKnownPartyFromX500Name` is identical for both revoked and non-revoked identities.
