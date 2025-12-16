---
title: Corda Enterprise Edition 4.10 release notes
date: '2023-05-08'

menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-10-release-notes
    parent: about-corda-landing-4-10-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.10 release notes

{{< note >}}
If you are using the Archive Service with Corda Enterprise Edition 4.10, you must use the 1.0.x stream of the Archive Service release. For more details, see [Archive Service]({{< relref "../../../../tools/archiving-service/archiving-release-notes.md" >}}).
{{< /note >}}

## Corda Enterprise Edition 4.10.7 release notes

Corda Enterprise Edition 4.10.7 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

- The Corda [Network Builder]({{< relref "network-builder.md" >}}) now correctly deploys a Corda network both via CLI in Docker and Azure environments.

### Third-party components upgrade

The following table lists the dependency upgrades for 4.10.7 Enterprise Edition. Dependencies with unchanged versions are omitted.

| Dependency                                            | New Version        |
|-------------------------------------------------------|--------------------|
| com.github.docker-java:docker-java                    | 3.5.2              |
| com.github.docker-java:docker-java-transport-httpclient5 | 3.5.2           |
| io.netty:tcnative*                                    | 2.0.74.Final       |
| com.fasterxml.jackson.core:jackson-annotations        | 2.17.3             |
| io.netty:*                                            | 4.1.128.Final      |
| commons-beanutils:commons-beanutils                   | 1.11.0             |
| org.apache.commons:commons-lang3                      | 3.19.0             |
| org.controlsfx:controlsfx                             | 11.2.2             |
| com.azure.resourcemanager:azure-resourcemanager       | 2.52.0             |
| com.azure:azure-identity                              | 1.18.1             |

## Corda Enterprise Edition 4.10.6 release notes

Corda Enterprise Edition 4.10.6 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* When deploying a test node using DriverDSL, the node now starts successfully without encountering a `NoSuchMethodError` exception.
* You can now create two nodes with identical `O` field values but different `OU` values in their X.500 names when using the DriverDSL for testing.
* There is no longer a memory leak when creating a series of mock networks for testing purposes.
* Transactions with the in-flight transaction state, introduced in Corda version 4.11 to support transaction recovery, are no longer included when the Ledger Graph CorDapp builds a transaction graph. Instead, the CorDapp now ignores any transactions with an in-flight status.

### New features, enhancements and restrictions

* Contract JAR signing key rotation of R3-provided CorDapps is included in this patch release.
* Docker images are now based on Java 8 build 432.
* An OpenTelemetry span has been added to the "send to multiple parties" and "receive from multiple parties" operations.

### Third-party components upgrade

The following table lists the dependency version changes between 4.10.5 and 4.10.6 Enterprise Editions:

| Dependency                   | Name                | Version 4.10.5 Enterprise   | Version 4.10.6 Enterprise      |
|------------------------------|---------------------|-----------------------------|--------------------------------|
| org.eclipse.jetty:*          | Jetty               | 9.4.53.v20231009            | 9.4.56.v20240826               |
| commons-io:commons-io        | commons IO          | 2.6                         | 2.17.0                         |
| com.fasterxml.jackson.\*:\*  | Jackson             | 2.17.2                      | 2.14.0                         |
| com.zaxxer:HikariCP          | Hikari              | 3.3.1                       | 4.0.3                          |
| org.apache.sshd:sshd-common  | sshd                | 2.9.2                       | 2.13.2                         |
| org.apache.commons:commons-configuration2   | commonsConfiguration2       | 2.10.0          | 2.11.0              |

## Corda Enterprise Edition 4.10.5 release notes

Corda Enterprise Edition 4.10.5 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* `ReceiveTransactionFlow` was checking that the network parameters on the transaction existed before `ResolveTransactionFlow` was executed.
  This could cause a problem in certain scenarios; for example, when sending a top-level transaction to a new node in a migrated network, as the old network parameters would not exist on this new node. This has now been fixed.
* When resolving a party, in some code paths, `wellKnownPartyFromAnonymous` did not consider notaries from network parameters when trying to resolve an X.500 name. This scenario could occur when introducing a new node to a newly-migrated network as the new node would not have the old notary in its network map. This has now been fixed. Notaries from network parameters are now considered in the check.

## Corda Enterprise Edition 4.10.4 release notes

Corda Enterprise Edition 4.10.4 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* In the default log4j2.xml file, the Delete action in the DefaultRolloverStrategy policy for log files beginning with `diagnostic-*` or `checkpoints_agent-*` was incorrect. It erroneously compared against the wrong file names. This issue has been rectified, ensuring that files are now deleted in accordance with the policy.
* Resolved a TLS connection issue regression when using a HSM to store TLS private keys.
* Previously, a rare error scenario could occur where a node would erroneously perceive a valid connection to a peer when, in fact, it was not connected. This issue typically arose when the peer node was disconnecting/connecting. This issue has now been resolved.

### Third party component upgrades

* Jetty version was upgraded from 9.4.51.v20230217 to 9.4.53.v20231009.
* Apache Tomcat was upgraded from 9.0.82 to 9.0.83 in the node management plugin, which is now at version 1.0.6.

## Corda Enterprise Edition 4.10.3 release notes

Corda Enterprise Edition 4.10.3 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Some log messages at warning level relating to failed SSL handshakes were accidentally introduced as part of improvements to SSL certificate handling in the previous patch release, and would appear frequently in the logs as part of connectivity tests of traffic load balancers and system monitoring.  These log messages have been silenced to reduce “noise” in the logs.
* Vault queries have been optimised to avoid the extra SQL query for the total state count where possible.
* Previously, the order of the states in vault query results would sometimes be incorrect if they belonged to the same transaction. This issue has been resolved.
* Added improvements to node thread names to make logging and debugging clearer.
* Delays when performing a SSL handshake with new nodes no longer impacts existing connections with other nodes.
* An issue has been resolved where, previously, an incorrect value for `Page.totalStatesAvailable` was returned for queries on `externalIds`, when there where external IDs mapped to multiple keys.

## Corda Enterprise Edition 4.10.2 release notes

Corda Enterprise Edition 4.10.2 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Flow checkpoint dumps now include a `status` field which shows the status of the flow; in particular, whether it is hospitalized or not.

* Debug logging of the Artemis server has been added.

* The default value for the node configuration value cryptoServiceTimeout has been increased from 1 second to 10 seconds.

* During recovery from a transport layer connection break in peer-to-peer connectivity, a workaround to a bug in the Artemis message broker would only be taken during the first break in connectivity. This lead to a rare failure to re-establish connectivity between two peers until the node was restarted.  The workaround is now taken on every loss of connectivity, and thus peer-to-peer connectivity should now always be re-established without operator intervention.

* Previously, if a node was configured to use two different slots on the Luna HSM (for example using one slot for node identities and a separate slot for the confidential identities), this failed. This issue has now been resolved.

  {{< warning >}}
  However as a result of this fix you need to make sure the Luna client your are using is version 10.4.0 or later.
  {{</ warning >}}

* When FIPS mode is activated in the Luna HSM, version 7.7.1 of the firmware does not allow the mechanism AES/CBC/PKCS5Padding to use wrap functionality. This has resulted in flow errors with confidential identities when using "wrapped" mode.

  A new mechanism (AES/KWP/NoPadding) has been enabled that allows wrapping when in FIPS mode. To switch to this new mechanism, a new Boolean configuration parameter, `usekwp`, has been added to the Luna HSM configuration file. If this parameter is set to true, then the new mechanism is used. If false or the parameter does not exist in the configuration file, then the existing mechanism is used.

* Updated documentation for both `.startNodes()` and `.stopNodes()` of MockNetwork to indicate that restarting nodes is not supported.

* Previously, when configured to use confidential identities and the Securosys PrimusX HSM, it was possible for Corda to fail to generate a wrapped key-pair for a new confidential identity. This would cause a temporary key-pair to be leaked, consuming resource in the HSM. This issue occurred when:

  * the Securosys HSM was configured in a master-clone cluster

  * the master HSM had failed and Corda had failed-over to use the clone HSM

  * there was an attempt to create a transaction using confidential identities

  The issue is now resolved. When generating a wrapped key-pair the temporary key-pair is not persisted in the HSM and thus cannot be leaked.

  On applying this update the PrimusX JCE should be upgraded to version 2.3.4 or later.

  There is no need to upgrade the HSM firmware version for this update but R3 recommends to keep the firmware up to date as a matter of course. Currently the latest firmware version if 2.8.50.

* A fix for cache eviction has been applied where an issue resulted in an incorrect contract verification status while a database transaction was in progress during contract verification.

* Corda provides the NodeDriver to help developers write integration tests. Using the NodeDriver, developers can bring up nodes locally to run flows and inspect state updates. Previously, there was an issue with build pipelines with tests failing, as on some occasions, notaries took more than one minute (the default timeout value) to start.

  To resolve this, the NodeDriver now has a new parameter, `notaryHandleTimeout`. This parameter specifies how long to wait (in minutes) for a notary handle to come back after the notary has been started.

* When a notary worker is shut down, message ID cleanup is now performed as the last shutdown activity, rather than the first; this prevents a situation where the notary worker might still appear to be part of the notary cluster and receiving client traffic while shutting down.

* Previously, where nodes had invoked a very large number of flows, the cache of client IDs that had not been removed were taking up significant heap space. A solution has been implemented where the space taken up has been reduced by 170 bytes per entry. For example, 1 million unremoved client IDs now take up 170,000,000 bytes less heap space than before.

* A new or restarted peer node coming online and connecting to a node for the first time can significantly slow message processing from other peers on the node it connects to.  Now new peers coming online get a dedicated thread on the node they connect to and do not delay message processing for existing peer-to-peer connections on the receiving node.

* Previously, a new node configuration option, `cryptoServiceFlowRetryCount`, was introduced. The absolute value of `cryptoServiceFlowRetryCount` determines the number of times (N) a flow is retried. This fix resolves an issue where, instead, N+1 retries were being performed.

* The default SSL handshake timeout for inbound connections has been increased to 60 seconds. If during SSL handshake, certificate revocation lists (CRLs) take a long time to download, or are unreachable, then this 60 seconds gives the node enough time to establish the connection if `crlCheckSoftFail` is enabled.

* Previously, when loading checkpoints, the only log messages recorded were at the end of the process, recording the total number of checkpoints loaded.

  Now, the following additional logging has been added:

  * Checkpoints: Logging has been added for the two types of checkpoints—runnable and paused flows—being loaded; log messages show the number of checkpoints loaded every 30 seconds until all checkpoints have been loaded.

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

* The certificate revocation checking has been improved with the introduction of a read timeout on the download of the certificate revocation lists (CRLs). The default CRL connect timeout has also been adjusted to better suit Corda nodes. The caching of CRLs has been increased from 30 seconds to 5 minutes.

* Improved compatibility when using the performance test suite from Apple silicon Macs.

## Corda Enterprise Edition 4.10.1 release notes

Corda Enterprise Edition 4.10.1 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

The following issues were resolved in Corda Enterprise Edition 4.10.1:

* A `StackOverflowException` was thrown when an attempt was made to store a deleted party in the vault.

## Corda Enterprise Edition 4.10 release notes

Corda Enterprise Edition 4.10 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.10 uses platform version 12.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features and enhancements

### New service lifecycle event

During startup, a node publishes a new service lifecycle event BEFORE_STATE_MACHINE_START immediately prior to starting the state machine. The node does not start the state machine until all recipients of the event have handled it.

### Quick RPC for node health check

Some RPCs provided by the node are now “quick” in that they bypass the standard RPC thread pool and return relatively quickly even if the node is busy servicing a backlog of RPC requests. The affected RPCs are currentNodeTime() and getProtocolVersion().

### Peer nodes not permanently blocked

Previously, if a node failed to open an AMQP connection to a peer node because there was a failure due to a problem with the TLS handshake, it was possible for the peer to be permanently blocked such that further connection attempts would not be attempted unless the node was restarted. With this update, peer nodes are now not permanently blocked but connections are retried using longer intervals - 5x 5 minutes, and then once a day.

### New crypto service configuration option introduced

A new node configuration option, `cryptoServiceFlowRetryCount`, has been introduced.

Previously, flows that suffered a `CryptoServiceException` were admitted to the flow hospital for processing. The flow was retried a maximum of two times, and if it still failed then the exception was propagated back to the code that invoked the flow and the flow was failed.

Now, *cryptoServiceFlowRetryCount* can be used to override the above default actions for when a CryptoServiceException exception has been thrown due to a timeout with the crypto service. Other causes of `CryptoServiceException` are unaffected by this update.

The *absolute value* of *cryptoServiceFlowRetryCount* determines the number of times a flow is retried. The *sign* of the value determines what happens when all retries are exhausted:

* If a *negative* value is specified, then a CryptoServiceException is propagated back to the calling code and the flow fails; this was the default behaviour in versions of Corda before 4.10.
* If a *positive* value is specified, then the flow is held in the flow hospital paused, until either:
  * the node is restarted
  * a node operator manually restarts the flow
  * a node operator manually kills the flow off

### Node status published via JMX

A node now publishes a status via JMX - net.corda.Node.Status - that indicates what it is currently doing. The status is only available if the node is configured to publish information/metrics via JMX.

### Java serialization disabled in the firewall

Java serialization is now disabled in the Corda firewall component, as a mitigation against attack should access be obtained maliciously to perform remote code execution.

### Postgres support

Postgres 13.8 is now supported.

### Flows can now generate OpenTelemetry spans

The OpenTelemetry tracing signal is now supported in flows across nodes. For more information, see [OpenTelemetry]({{< relref "node/operating/monitoring-and-logging/opentelemetry.md" >}}).

### Improved node diagnostics

This release includes improved node diagnostics:

* There is a thread dump to the log file every five minutes.
* There is a periodic check to determine if the state machine thread pool is blocked and a warning is generated if so.
* Log messages are now output, both on the nodes initiating flows on other flows and also on the receiving nodes. This ties outgoing initiate sessions to their message ID and also inbound initiate sessions to their message ID. This enables easier diagnosis of logs across nodes.

## Fixed issues

This release includes the following fixes:

* Warning messages from Artemis are no longer written to the standard output when disconnecting an SSH client from the node. However, the warnings are still written to the node’s log file.

* Corda node memory usage has been improved when using the tokens SDK with inMemory token selection enabled.

* Corda can fetch users' credentials and permissions from an external data source (for example, from a remote RDBMS). Credentials of this database are configured in the file `node.conf`. Previously, when a node was run, Corda logged the password of this database to the log file. This issue has been resolved and the password is no longer written to the log file.

* Previously, Archive Service commands did not write messages to the log files unless an error or issue occurred. An update now means that messages are also written when commands are run successfully. For more information, refer to [Archive Service Command-Line Interface (CLI)]({{< relref "../../../../tools/archiving-service/archiving-cli.md" >}})

* Previously, a memory leak in the transaction cache occurred due to the weight of in-flight entries being undervalued. Improvements have been made to prevent in-flight entry weights from being undervalued and, because they are now estimated more correctly, this results in a large decrease in the total size of cached entities.

* Flow draining mode no longer acknowledges P2P in-flight messages that have not yet been committed to the database. Previously, flow draining mode acknowledged all in-flight messages as duplicate.

* Previously, the attachment class loader was being closed too early if it was evicted from the cache. Now, closing of attachment class loaders is delayed until all SerializationContext that refer to them (from BasicVerifier) have gone out of scope.

* Occasionally, database transactions were rolled back under heavy load that caused flow state machine threads to stop processing flows. This resulted in eventual node lockup in certain circumstances.

### Database schema changes

There are no database changes between 4.9 and 4.10.

### Third party component upgrades

The following table lists the dependency version changes between 4.9.5 and 4.10 Enterprise Editions:

| Dependency                         | Name                | Version 4.9.5 Enterprise | Version 4.10 Enterprise|
|------------------------------------|---------------------|--------------------------|------------------------|
| com.squareup.okhttp3               | OKHttp              | 3.14.2                   | 3.14.9                 |
| org.bouncycastle                   | Bouncy Castle       | 1.68                     | 1.70                   |
| io.opentelemetry                   | Open Telemetry      | -                        | 1.20.1                 |
| org.apache.commons:commons-text    | Apache Commons-Text | 1.9                      | 1.10.0                 |
| org.apache.shiro                   | Apache Shiro        | 1.9.1                    | 1.10.0                 |

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
