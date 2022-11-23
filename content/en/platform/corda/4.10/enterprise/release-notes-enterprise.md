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

Corda: Enterprise Edition 4.10 features 

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.10/enterprise.html) as soon as possible. The latest Corda: Enterprise Edition  release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.10/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.10/enterprise.html).

### Fixed issues

In this release:

* During startup the node publishes a new service lifecycle event BEFORE_STATE_MACHINE_START immediately prior to starting the state machine, and will not start the state machine until all recipients of the event have handled it.
 
* Some RPCs provided by the node are now “quick” in that they bypass the standard RPC thread pool and will return relatively quickly even if the node is busy servicing a backlog of RPC requests. The affected RPCs are currentNodeTime(), and fetching the protocol version.

### Database Schema Changes




### Third party component upgrades

