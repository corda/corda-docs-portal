---
title: Corda Enterprise Edition 4.9 release notes
date: '2023-09-04'

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

{{< note >}}
If you are using the Archive Service with Corda Enterprise Edition 4.9, you must use the 1.0.x stream of the Archive Service release. For more details, see [Archive Service]({{< relref "../../../../tools/archiving-service/archiving-release-notes.md" >}}).
{{< /note >}}

## Corda Enterprise Edition 4.9.11 release notes

Corda Enterprise Edition 4.9.11 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* When deploying a test node using DriverDSL, the node now starts successfully without encountering a `NoSuchMethodError` exception.
* You can now create two nodes with identical `O` field values but different `OU` values in their X.500 names when using the DriverDSL for testing.
* There is no longer a memory leak when creating a series of mock networks for testing purposes.
* Transactions with the in-flight transaction state, introduced in Corda version 4.11 to support transaction recovery, are no longer included when the Ledger Graph CorDapp builds a transaction graph. Instead, the CorDapp now ignores any transactions with an in-flight status.

### New features, enhancements and restrictions

* Contract JAR signing key rotation of R3-provided CorDapps is included in this patch release.
* Docker images are now based on Java 8 build 432.

### Third-party components upgrade

The following table lists the dependency version changes between 4.9.10 and 4.9.11 Enterprise Editions:

| Dependency                   | Name                | Version 4.9.10 Enterprise   | Version 4.9.11 Enterprise      |
|------------------------------|---------------------|-----------------------------|--------------------------------|
| org.eclipse.jetty:*          | Jetty               | 9.4.53.v20231009            | 9.4.56.v20240826               |
| commons-io:commons-io        | commons IO          | 2.6                         | 2.17.0                         |
| com.fasterxml.jackson.\*:\*  | Jackson             | 2.17.2                      | 2.14.0                         |
| com.zaxxer:HikariCP          | Hikari              | 3.3.1                       | 4.0.3                          |
| org.apache.sshd:sshd-common  | sshd                | 2.9.2                       | 2.13.2                         |

## Corda Enterprise Edition 4.9.10 release notes

Corda Enterprise Edition 4.9.10 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* `ReceiveTransactionFlow` was checking that the network parameters on the transaction existed before `ResolveTransactionFlow` was executed.
  This could cause a problem in certain scenarios; for example, when sending a top-level transaction to a new node in a migrated network, as the old network parameters would not exist on this new node. This has now been fixed.
* When resolving a party, in some code paths, `wellKnownPartyFromAnonymous` did not consider notaries from network parameters when trying to resolve an X.500 name. This scenario could occur when introducing a new node to a newly-migrated network as the new node would not have the old notary in its network map. This has now been fixed. Notaries from network parameters are now considered in the check.

## Corda Enterprise Edition 4.9.9 release notes

Corda Enterprise Edition 4.9.9 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* In the default log4j2.xml file, the Delete action in the DefaultRolloverStrategy policy for log files beginning with `diagnostic-*` or `checkpoints_agent-*` was incorrect. It erroneously compared against the wrong file names. This issue has been rectified, ensuring that files are now deleted in accordance with the policy.
* Resolved a TLS connection issue regression when using a HSM to store TLS private keys.
* Previously, a rare error scenario could occur where a node would erroneously perceive a valid connection to a peer when, in fact, it was not connected. This issue typically arose when the peer node was disconnecting/connecting. This issue has now been resolved.

### Third party component upgrades

* Jetty version was upgraded from 9.4.51.v20230217 to 9.4.53.v20231009.
* Apache Tomcat was upgraded from 9.0.82 to 9.0.83 in the node management plugin, which is now at version 1.0.6.

## Corda Enterprise Edition 4.9.8 release notes

Corda Enterprise Edition 4.9.8 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed Issues

* Some log messages at warning level relating to failed SSL handshakes were accidentally introduced as part of improvements to SSL certificate handling in the previous patch release, and would appear frequently in the logs as part of connectivity tests of traffic load balancers and system monitoring.  These log messages have been silenced to reduce “noise” in the logs.
* Vault queries have been optimised to avoid the extra SQL query for the total state count where possible.
* Node thread names have been made more specific to make logging more descriptive and debugging easier.
* Delays when SSL handshaking with new nodes no longer impact existing connections with existing nodes.
* An issue has been resolved where, sometimes, the order of the states returned by a vault query would be incorrect if they belonged to the same transaction.
* An issue has been resolved where, previously, an incorrect value for `Page.totalStatesAvailable` was returned for queries on `externalIds`, when there where external IDs mapped to multiple keys.

## Corda Enterprise Edition 4.9.7 release notes

Corda Enterprise Edition 4.9.7 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* A new or restarted peer node coming online and connecting to a node for the first time can significantly slow message processing from other peers on the node to which it connects.  With this improvement, new peers coming online get a dedicated thread on the node they connect to and do not delay message processing for existing peer-to-peer connections on the receiving node.

* Debug logging of the Artemis server has been added.

* The thread dump on heartbeat feature was causing excess log output. This has now been improved: we now only log thread stack traces that appear to be stuck and no longer repeatedly log them.

* Previously, when configured to use confidential identities and the Securosys PrimusX HSM, it was possible for Corda to fail to generate a wrapped key-pair for a new confidential identity. This would cause a temporary key-pair to be leaked, consuming resource in the HSM. This issue occurred when:

  * the Securosys HSM was configured in a master-clone cluster
  * the master HSM had failed and Corda had failed-over to use the clone HSM
  * there was an attempt to create a transaction using confidential identities

  The issue is now resolved. When generating a wrapped key-pair the temporary key-pair is not persisted in the HSM and thus cannot be leaked.

  On applying this update the PrimusX JCE should be upgraded to version 2.3.4 or later.

  There is no need to upgrade the HSM firmware version for this update but R3 recommends to keep the firmware up to date as a matter of course. Currently the latest firmware version if 2.8.50.

* The default SSL handshake timeout for inbound connections has been increased to 60 seconds. If during SSL handshake, certificate revocation lists (CRLs) take a long time to download or are unreachable, then this 60 seconds gives the node enough time to establish the connection if `crlCheckSoftFail` is enabled.

* Previously, when loading checkpoints, the only log messages recorded were at the end of the process, recording the total number of checkpoints loaded.

  Now, the following additional logging has been added:

  * Checkpoints: Logging has been added for the two types of checkpoints - runnable and paused flows - being loaded; log messages show the number of checkpoints loaded every 30 seconds until all checkpoints have been loaded.

  * Finished flows: Log messages now show the number of finished flows.

  For example:

  ```
  [INFO ] 2023-02-03T17:00:12,767Z [main] statemachine.MultiThreadedStateMachineManager. - Loading checkPoints flows {}
  [INFO ] 2023-02-03T17:00:12,903Z [main] statemachine.MultiThreadedStateMachineManager. - Number of runnable flows: 0. Number of paused flows: 0 {}
  [INFO ] 2023-02-03T17:00:12,911Z [main] statemachine.MultiThreadedStateMachineManager. - Started loading finished flows {}
  [INFO ] 2023-02-03T17:00:28,437Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 9001 finished flows {}
  [INFO ] 2023-02-03T17:00:43,606Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 24001 finished flows {}
  [INFO ] 2023-02-03T17:00:46,650Z [main] statemachine.MultiThreadedStateMachineManager. - Number of finished flows : 27485 {}
  ```
* Previously, where nodes had invoked a very large number of flows, the cache of client IDs that had not been removed were taking up significant heap space. A solution has been implemented where the space taken up has been reduced by 170 bytes per entry. For example, 1 million un-removed client IDs now take up 170,000,000 bytes less heap space than before.

* When a notary worker is shut down, message ID cleanup is now performed as the last shutdown activity, rather than the first; this prevents a situation where the notary worker might still appear to be part of the notary cluster and receiving client traffic while shutting down.

* During recovery from a transport layer connection break in peer-to-peer connectivity, a workaround to a bug in the Artemis message broker would only be taken during the first break in connectivity. This lead to a rare failure to re-establish connectivity between two peers until the node was restarted. The workaround is now taken on every loss of connectivity, and thus peer-to-peer connectivity should now always be re-established without operator intervention.

* Previously, if a node was configured to use two different slots on the Luna HSM (for example using one slot for node identities and a separate slot for the confidential identities), this failed. This issue has now been resolved.

  {{< warning >}}
  However as a result of this fix you need to make sure the Luna client your are using is version 10.4.0 or later.
  {{</ warning >}}

* The default value for the node configuration value cryptoServiceTimeout has been increased from 1 second to 10 seconds.

* Corda provides the NodeDriver to help developers write integration tests. Using the NodeDriver, developers can bring up nodes locally to run flows and inspect state updates. Previously, there was an issue with build pipelines with tests failing, as on some occasions, notaries took more than one minute (the default timeout value) to start.

  To resolve this, the NodeDriver now has a new parameter, `notaryHandleTimeout`. This parameter specifies how long to wait for a notary handle to come back after the notary has been started.

* A fix for cache eviction has been applied where an issue resulted in an incorrect contract verification status while a database transaction was in progress during contract verification.

* A `StackOverflowException` was thrown when an attempt was made to store a deleted party in the vault. This issue has been resolved.

* The certificate revocation checking has been improved with the introduction of a read timeout on the download of the certificate revocation lists (CRLs). The default CRL connect timeout has also been adjusted to better suit Corda nodes. The caching of CRLs has been increased from 30 seconds to 5 minutes.

* Improved compatibility when using the performance test suite from Apple silicon Macs.

## Corda Enterprise Edition 4.9.6 release notes

Corda Enterprise Edition 4.9.6 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* When FIPS mode is activated in the Luna HSM, version 7.7.1 of the firmware does not allow the mechanism AES/CBC/PKCS5Padding to use wrap functionality. This has resulted in flow errors with confidential identities when using "wrapped" mode.

  A new mechanism (AES/KWP/NoPadding) has been enabled that allows wrapping when in FIPS mode. To switch to this new mechanism, a new Boolean configuration parameter, `usekwp`, has been added to the Luna HSM configuration file. If this parameter is set to true, then the new mechanism is used. If false or the parameter does not exist in the configuration file, then the existing mechanism is used.

## Corda Enterprise Edition 4.9.5 release notes

Corda Enterprise Edition 4.9.5 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Previously, a memory leak in the transaction cache occurred due to weight of in-flight entries being undervalued. Improvements have been made to prevent in-flight entry weights from being undervalued and, because they are now estimated more correctly, this results in a large decrease in the total size of cached entities.

* A rare condition was fixed relating to roll back of database transactions under heavy load, which caused flow state machine threads to stop processing flows, leading to eventual node lock up in certain circumstances.

## Corda Enterprise Edition 4.9.4 release notes

Corda Enterprise Edition 4.9.4 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, see [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* The closing of AttachmentClassLoaders is now delayed until all SerializationContexts that refer to them have gone out of scope. This fixes an issue where they were being closed too early when evicted from the cache.
* Flow draining mode no longer acknowledges P2P in-flight messages that have not yet been committed to the database. Previously, flow draining mode acknowledged all in-flight messages as duplicate.
* A periodic check is now performed to determine if the state machine thread pool seems to be blocked. A warning is logged if the thread pool is blocked. A thread dump is now also logged periodically (every five minutes).

## Corda Enterprise Edition 4.9.3 release notes

Corda Enterprise Edition 4.9.3 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "upgrading-index.md" >}}).

### Fixed issues

The following issues were resolved in this patch release:

* Previously, both Corda nodes certificates possessed Certificate Authority power because the CA attribute was set to true. The node registration tool now has a new  option, ```-C, --node-identity-cert-not-ca```, allowing a node legal identity certificate to be created where it is not a CA.

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

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "upgrading-index.md" >}}).

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

As a developer, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}).

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

As a developer, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda: Enterprise Edition  release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}).

### Fixed issues

In this release:

* Corda shell has been removed to its own repository for improved security. You can now use a standalone shell outside of the node, or from within the node's drivers. For more information about using the standalone shell, see [The standalone shell]({{< relref "./node/operating/shell.md#the-standalone-shell" >}}). For information on adding the shell to the node's drivers, see [Upgrading a node to Corda Enterprise Edition 4.9]({{< relref "node-upgrade-notes.md" >}}).
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
