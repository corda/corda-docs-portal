---
title: Corda Enterprise Edition 4.9 release notes
date: '2023-05-05'

menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-release-notes
    parent: about-corda-landing-4-9-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.9 release notes

## Corda Enterprise Edition 4.9.7 release notes

Corda Enterprise Edition 4.9.7 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node](upgrading-index.md).

### Fixed issues

* Previously, where nodes had invoked a very large number of flows, the cache of client IDs that had not been removed were taking up significant heap space. A solution has been implemented where the space taken up has been reduced by 170 bytes per entry. For example, 1 million un-removed client IDs now take up 170,000,000 bytes less heap space than before.

* Previously, when configured to use confidential identities and the Securosys PrimusX HSM, it was possible for Corda to fail to generate a wrapped key-pair for a new confidential identity. This would cause a temporary key-pair to be leaked, consuming resource in the HSM. This issue occurred when:

  * the Securosys HSM was configured in a master-clone cluster

  * the master HSM had failed and Corda had failed-over to use the clone HSM

  * there was an attempt to create a transaction using confidential identities

  The issue is now resolved. When generating a wrapped key-pair the temporary key-pair is not persisted in the HSM and thus cannot be leaked.

  On applying this update the PrimusX JCE should be upgraded to version 2.3.4 or later.

  There is no need to upgrade the HSM firmware version for this update, but it is recommended to keep the firmware up to date as a matter of course. Currently, the latest firmware version is 2.8.50.

* Corda provides the NodeDriver to help developers write integration tests. Using the NodeDriver, developers can bring up nodes locally to run flows and inspect state updates. Previously, there was an issue with build pipelines with tests failing, as on some occasions, notaries took more than one minute (the default timeout value) to start.

  To resolve this, the NodeDriver now has a new parameter, notaryHandleTimeout. This parameter specifies how long to wait (in minutes) for a notary handle to come back after the notary has been started.

* Previously, when loading checkpoints, the only log messages recorded were at the end of the process, recording the total number of checkpoints loaded.

  Now, the following additional logging has been added:

  * Checkpoints: Logging has been added for the two types of checkpoints - runnable and paused flows - being loaded; log messages show the number of checkpoints loaded every 30 seconds until all checkpoints have been loaded.

  * Finished flows: Log messages now show the number of finished flows.

  For example:

  [INFO ] 2023-02-03T17:00:12,767Z [main] statemachine.MultiThreadedStateMachineManager. - Loading checkPoints flows {}
  [INFO ] 2023-02-03T17:00:12,903Z [main] statemachine.MultiThreadedStateMachineManager. - Number of runnable flows: 0. Number of paused flows: 0 {}
  [INFO ] 2023-02-03T17:00:12,911Z [main] statemachine.MultiThreadedStateMachineManager. - Started loading finished flows {}
  [INFO ] 2023-02-03T17:00:28,437Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 9001 finished flows {}
  [INFO ] 2023-02-03T17:00:43,606Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 24001 finished flows {}
  [INFO ] 2023-02-03T17:00:46,650Z [main] statemachine.MultiThreadedStateMachineManager. - Number of finished flows : 27485 {}

* A fix for cache eviction has been applied where an issue resulted in an incorrect contract verification status while a database transaction was in progress during contract verification.

* The default SSL handshake timeout for the embedded Artemis messaging server has been increased to 60 seconds. If during SSL handshake, certificate revocation lists (CRLs) take a long time to download, or are unreachable, then the 60 seconds gives the node enough time to establish the connection if `crlCheckSoftFail` is enabled.

* A `StackOverflowException` was thrown when an attempt was made to store a deleted party in the vault. This issue has been resolved.

## Corda Enterprise Edition 4.9.6 release notes

Corda Enterprise Edition 4.9.6 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node](upgrading-index.md).

### Fixed issues

* When FIPS mode is activated in the Luna HSM, version 7.7.1 of the firmware does not allow the mechanism AES/CBC/PKCS5Padding to use wrap functionality. This has resulted in flow errors with confidential identities when using "wrapped" mode.

  A new mechanism (AES/KWP/NoPadding) has been enabled that allows wrapping when in FIPS mode. To switch to this new mechanism, a new Boolean configuration parameter, `usekwp`, has been added to the Luna HSM configuration file. If this parameter is set to true, then the new mechanism is used. If false or the parameter does not exist in the configuration file, then the existing mechanism is used.

## Corda Enterprise Edition 4.9.5 release notes

Corda Enterprise Edition 4.9.5 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md" >}}).

### Fixed issues

* Previously, a memory leak in the transaction cache occurred due to weight of in-flight entries being undervalued. Improvements have been made to prevent in-flight entry weights from being undervalued and, because they are now estimated more correctly, this results in a large decrease in the total size of cached entities.

* A rare condition was fixed relating to roll back of database transactions under heavy load, which caused flow state machine threads to stop processing flows, leading to eventual node lock up in certain circumstances.

## Corda Enterprise Edition 4.9.4 release notes

Corda Enterprise Edition 4.9.4 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, see [Upgrading a CorDapp or node]({{< relref "../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md" >}}).

### Fixed issues

* The closing of AttachmentClassLoaders is now delayed until all SerializationContexts that refer to them have gone out of scope. This fixes an issue where they were being closed too early when evicted from the cache.
* Flow draining mode no longer acknowledges P2P in-flight messages that have not yet been committed to the database. Previously, flow draining mode acknowledged all in-flight messages as duplicate.
* A periodic check is now performed to determine if the state machine thread pool seems to be blocked. A warning is logged if the thread pool is blocked. A thread dump is now also logged periodically (every five minutes).

## Corda Enterprise Edition 4.9.3 release notes

Corda Enterprise Edition 4.9.3 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md" >}}).

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

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md" >}}).

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

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md" >}}).

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

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda: Enterprise Edition  release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this release:

* Corda shell has been removed to its own repository for improved security. You can now use a standalone shell outside of the node, or from within the node's drivers. For more information about using the standalone shell, see [The standalone shell](./node/operating/shell.html#the-standalone-shell). For information on adding the shell to the node's drivers, see [Upgrading a node to Corda Enterprise Edition 4.9](node-upgrade-notes.html).
{{< note >}}
The Corda shell has a dependency on Groovy that the Corda API does not. As a result, for any flows dependent on Groovy, you must now add the dependency to the CorDapp or the drivers' directory.
{{< /note >}}
* Security updates to prevent possibility of Denial of Service attacks.
* Improvements to demos and sample code.
* Improvements to improve compatibility with Intel Macs.
* An issue affecting Node JVM deadlocks is resolved.
* An issue with failed attachments from a notary has been fixed.
* An issue preventing attachments to subflows in certain circumstances has been fixed.

### Database Schema Changes

* The `node_named_identities` table has been re-introduced. It was removed in Corda Enterprise Edition 4.7 following updates to certificate rotation functionality.
  * The reintroduction of this table ensures that the behavior of `rpcOps.wellKnownPartyFromX500Name` is identical for both revoked and non-revoked identities.

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
