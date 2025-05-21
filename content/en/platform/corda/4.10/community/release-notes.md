---
title: Corda Community Edition 4.10 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2023-05-08'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-release-notes
    parent: about-corda-landing-4-10-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Community Edition 4.10 release notes

## Corda Community Edition 4.10.6 release notes

Corda Community Edition 4.10.6 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* When deploying a test node using DriverDSL, the node now starts successfully without encountering a `NoSuchMethodError` exception.
* You can now create two nodes with identical `O` field values but different `OU` values in their X.500 names when using the DriverDSL for testing.

### New features, enhancements and restrictions

* Contract JAR signing key rotation of R3-provided CorDapps is included in this patch release.
* Docker images are now based on Java 8 build 432.

### Third-party components upgrade

The following table lists the dependency version changes between 4.10.5 and 4.10.6 Community Editions:

| Dependency                   | Name                | Version 4.10.5 Community    | Version 4.10.6 Community       |
|------------------------------|---------------------|-----------------------------|--------------------------------|
| org.eclipse.jetty:*          | Jetty               | 9.4.53.v20231009            | 9.4.56.v20240826               |
| commons-io:commons-io        | commons IO          | 2.6                         | 2.17.0                         |
| com.fasterxml.jackson.\*:\*  | Jackson             | 2.17.2                      | 2.14.0                         |
| com.zaxxer:HikariCP          | Hikari              | 3.3.1                       | 4.0.3                          |

## Corda Community Edition 4.10.5 release notes

Corda Community Edition 4.10.5 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* `ReceiveTransactionFlow` was checking that the network parameters on the transaction existed before `ResolveTransactionFlow` was executed.
  This could cause a problem in certain scenarios; for example, when sending a top-level transaction to a new node in a migrated network, as the old network parameters would not exist on this new node. This has now been fixed.
* When resolving a party, in some code paths, `wellKnownPartyFromAnonymous` did not consider notaries from network parameters when trying to resolve an X.500 name. This scenario could occur when introducing a new node to a newly-migrated network as the new node would not have the old notary in its network map. This has now been fixed. Notaries from network parameters are now considered in the check.

## Corda Community Edition 4.10.4 release notes

Corda Community Edition 4.10.4 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* In the default log4j2.xml file, the Delete action in the DefaultRolloverStrategy policy for log files beginning with `diagnostic-*` or `checkpoints_agent-*`  was incorrect. It erroneously compared against the wrong file names. This issue has been rectified, ensuring that files are now deleted in accordance with the policy.
* Previously, a rare error scenario could occur where a node would erroneously perceive a valid connection to a peer when, in fact, it was not connected. This issue typically arose when the peer node was disconnecting/connecting.

### Third party component upgrades

* Jetty version was upgraded from 9.4.51.v20230217 to 9.4.53.v20231009.

## Corda Community Edition 4.10.3 release notes

Corda Community Edition 4.10.3 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* Some log messages at warning level relating to failed SSL handshakes were accidentally introduced as part of improvements to SSL certificate handling in the previous patch release, and would appear frequently in the logs as part of connectivity tests of traffic load balancers and system monitoring.  These log messages have been silenced to reduce “noise” in the logs.
* Vault queries have been optimised to avoid the extra SQL query for the total state count where possible.
* Previously, the order of the states in vault query results would sometimes be incorrect if they belonged to the same transaction. This issue has been resolved.
* Added improvements to node thread names to make logging and debugging clearer.
* Delays when performing a SSL handshake with new nodes no longer impacts existing connections with other nodes.
* An issue has been resolved where, previously, an incorrect value for `Page.totalStatesAvailable` was returned for queries on `externalIds`, when there where external IDs mapped to multiple keys.

## Corda Community Edition 4.10.2 release notes

Corda Community Edition 4.10.2 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* Flow checkpoint dumps now include a `status` field which shows the status of the flow; in particular, whether it is hospitalized or not.

* Debug logging of the Artemis server has been added.

* Corda provides the NodeDriver to help developers write integration tests. Using the NodeDriver, developers can bring up nodes locally to run flows and inspect state updates. Previously, there was an issue with build pipelines with tests failing, as on some occasions, notaries took more than one minute (the default timeout value) to start.

  To resolve this, the NodeDriver now has a new parameter, `notaryHandleTimeout`. This parameter specifies how long to wait (in minutes) for a notary handle to come back after the notary has been started

* The default SSL handshake timeout for inbound connections has been increased to 60 seconds. If during SSL handshake, certificate revocation lists (CRLs) take a long time to download, or are unreachable, then this 60 seconds gives the node enough time to establish the connection if crlCheckSoftFail is enabled.

* The certificate revocation checking has been improved with the introduction of a read timeout on the download of the certificate revocation lists (CRLs). The default CRL connect timeout has also been adjusted to better suit Corda nodes. The caching of CRLs has been increased from 30 seconds to 5 minutes.

## Corda Community Edition 4.10 release notes

Corda Community Edition 4.10 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.10 uses platform version 12.

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

## New features and enhancements

### New service lifecycle event

During startup, a node publishes a new service lifecycle event BEFORE_STATE_MACHINE_START immediately prior to starting the state machine. The node does not start the state machine until all recipients of the event have handled it.

### Quick RPC for node health check

Some RPCs provided by the node are now “quick” in that they bypass the standard RPC thread pool and return relatively quickly even if the node is busy servicing a backlog of RPC requests. The affected RPCs are `currentNodeTime()` and `getProtocolVersion()`.

### Peer nodes not permanently blocked

Previously, if a node failed to open an AMQP connection to a peer node because there was a failure due to a problem with the TLS handshake, it was possible for the peer to be permanently blocked such that further connection attempts would not be attempted unless the node was restarted. With this update, peer nodes are now not permanently blocked but connections are retried using longer intervals - 5x 5 minutes, and then once a day.

### Node status published via JMX

A node now publishes a status via JMX - net.corda.Node.Status - that indicates what it is currently doing. The status is only available if the node is configured to publish information/metrics via JMX.

### Postgres support

Postgres 13.8 is now supported.

### Flows can now generate OpenTelemetry spans

The OpenTelemetry tracing signal is now supported in flows across nodes. For more information, see [OpenTelemetry]({{< relref "opentelemetry.md" >}}).

### Improved node diagnostics

This release includes improved node diagnostics:
* There is a thread dump to the log file every five minutes.
* There is a periodic check to determine if the state machine thread pool is blocked and a warning is generated if so.
* Log messages are now output, both on the nodes initiating flows on other flows and also on the receiving nodes. This ties outgoing initiate sessions to their message ID and also inbound initiate sessions to their message ID. This enables easier diagnosis of logs across nodes.

## Fixed issues

This release includes the following fixes:

* Warning messages from Artemis are no longer written to the standard output when disconnecting an SSH client from the node. However, the warnings are still written to the node’s log file.

* Corda node memory usage has been improved when using the tokens SDK with inMemory token selection enabled.

* Corda can fetch users' credentials and permissions from an external data source (for example, from a remote RDBMS). Credentials of this database are configured in the file `node.conf`. Previously, when a node was run,  Corda logged the password of this database to the log file. This issue has been resolved and the password is no longer written to the log file.

* Previously, a memory leak in the transaction cache occurred due to the weight of in-flight entries being undervalued. Improvements have been made to prevent in-flight entry weights from being undervalued and, because they are now estimated more correctly, this results in a large decrease in the total size of cached entities.

* Flow draining mode no longer acknowledges P2P in-flight messages that have not yet been committed to the database. Previously, flow draining mode acknowledged all in-flight messages as duplicate.

* Previously, the attachment class loader was being closed too early if it was evicted from the cache. Now, closing of attachment class loaders is delayed until all SerializationContext that refer to them (from BasicVerifier) have gone out of scope.

* Occasionally, database transactions were rolled back under heavy load that caused flow state machine threads to stop processing flows. This resulted in eventual node lockup in certain circumstances.

### Database schema changes

There are no database changes between 4.9 and 4.10.

### Third party component upgrades

The following table lists the dependency version changes between 4.9.5 and 4.10 Community Editions:

| Dependency           | Name           | Version 4.9.5 Community | Version 4.10 Community |
|----------------------|----------------|-------------------------|------------------------|
| com.squareup.okhttp3 | OKHttp         | 3.14.2                  | 3.14.9                 |
| org.bouncycastle	   | Bouncy Castle  | 1.68                    | 1.70                   |
| io.opentelemetry	   | Open Telemetry | -                       | 1.20.1                 |

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
