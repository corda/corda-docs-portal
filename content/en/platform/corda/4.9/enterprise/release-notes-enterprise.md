---

date: '2021-07-01'

menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-release-notes
    name: "Release notes"
tags:
- release
- notes
- enterprise
title: Corda Enterprise Edition  release notes
weight: 1
---


# Corda: Enterprise Edition release notes

## Corda: Enterprise Edition 4.9.1

Corda Enterprise 4.9.1 is a patch release of Corda Enterprise which includes dependency upgrades and fixes for minor bugs.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this patch release:

* Fixing of a bug where `SuspensionMeta` in `FlowInfo` shows as null even when a runnable flow has previously been hospitalized.
* Official Artemis binaries implemented.
* Oracle JDK version 8u322 now supported.
*
## Corda: Enterprise Edition 4.9

Corda: Enterprise Edition  4.9 features many security improvements, along with a stand alone Shell for controlling the node via command line. You can also now access the `flowrpcops` API

* The `flowrpcops` API is available and documented. You can use this to start, pause, and retry flows and hospitalized flows.
* Access to node health data and node status.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda: Enterprise Edition  release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this release:

* Corda Shell has been removed to its own repository for improved security. You can now use a standalone shell outside of the node, or from within the node's drivers. You can read more about using the standalone shell [here](./node/operating/shell.html#the-standalone-shell).
* Security updates to prevent possibility of Denial of Service attacks.
* Improvements to demos and sample code.
* Improvements to improve compatibility with Intel Macs.
* An issue affecting Node JVM deadlocks is resolved.
* An issue with failed attachments from a notary has been fixed.
* An issue preventing attachments to subflows in certain circumstances has been fixed.

### Database Schema Changes

* The `node_named_identities` table has been re-introduced. It was removed in Corda Enterprise 4.7 following updates to certificate rotation functionality.
  * The reintroduction of this table ensures the behavior of `rpcOps.wellKnownPartyFromX500Name` is identical for both revoked and non-revoked identities.
