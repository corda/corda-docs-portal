---
title: Corda Enterprise Edition 4.10 release notes
date: '2021-07-01'

menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-10-release-notes
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 1
---

# Corda Enterprise Edition 4.10 release notes

Corda: Enterprise Edition 4.10 features a series of improvements over the previous version.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.10/enterprise.html) as soon as possible. The latest Corda: Enterprise Edition  release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.10/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.10/enterprise.html).

### Fixed issues

In this release:

* During startup the node publishes a new service lifecycle event BEFORE_STATE_MACHINE_START immediately prior to starting the state machine, and will not start the state machine until all recipients of the event have handled it.
 
* Some RPCs provided by the node are now “quick” in that they bypass the standard RPC thread pool and will return relatively quickly even if the node is busy servicing a backlog of RPC requests. The affected RPCs are currentNodeTime(), and fetching the protocol version.

* Previously, if a node failed to open an AMQP connection to a peer node, it was possible for the peer to be permanently blocked such that further connection attempts would not be attempted unless the node was restarted.

  With this update, peer nodes are now not permanently blocked but connections are retried using longer intervals - 5x 5 minutes, and then once a day.
  
* Warning messages from Artemis are no longer written to the standard output when disconnecting an SSH client from the node. The warnings are still written to the node’s log file though.

* Testing with the YourKit tool showed high memory usage when creating tokens in a CorDapp. High memory usage was also seen when a node is restarted and inMemory selection was activated in the node. A fix was implemented and the same tests afterwards showed a major decrease in memory usage.

* A new node configuration option, *cryptoServiceFlowRetryCount*, has been introduced.

  Previously, flows that suffered any variant of CryptoServiceException were admitted to the flow hospital for processing. The flow was retried a maximum of two times, and if it still failed then the exception was propagated back to the code that invoked the flow and the flow failed. 
  
  Now, *cryptoServiceFlowRetryCount* can be used to override the above default actions. 

  The *absolute value* of *cryptoServiceFlowRetryCount* determines the number of times a flow is retried. The *sign* of the value determines what happens when all retries are exhausted:

  * If a *negative* value is specified, then a CryptoServiceException is propagated back to the calling code and the flow fails; this was the default behaviour in versions of Corda before 4.10.
  * If a *positive* value is specified, then the flow is held in the flow hospital for overnight observation so that a node operator can review it.

* A node now publishes a status via JMX - net.corda.Node.Status - that indicates what it is currently doing. The status is only available if the node is configured to publish information/metrics via JMX.

### Database Schema Changes




### Third party component upgrades

