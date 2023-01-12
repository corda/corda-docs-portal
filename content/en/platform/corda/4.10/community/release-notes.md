---
title: Corda Community Edition 4.10 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2021-06-29'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-release-notes
    weight: 1
    name: "Release notes"
tags:
- release
- notes
---

# Corda Community Edition 4.10 release notes

Corda Community Edition 4.10 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.10 uses platform version 12.

For more information about platform versions, see [Versioning](versioning.md).

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

The OpenTelemetry tracing signal is now supported in flows across nodes. For more information, see [OpenTelemetry](opentelemetry.md).

### Improved node diagnostics

This release includes improved node diagnostics:
* Every five minutes, there is a thread dump to the log file
* There is a periodic check to determine if the state machine thread pool seems to be blocked, and a warning is generated if so.
* Log messages are now output, on both nodes initiating flows on other flows and on the receiving nodes, to tie outgoing initiate sessions to their message ID and likewise for inbound initiate sessions to their message ID so logs across nodes can be more easily diagnosed.

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