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

## Corda: Enterprise Edition 4.9.2

Corda Enterprise 4.9.2 is a patch release of Corda Enterprise which includes the addition of a new Gradle 7 plugin, security upgrades, and fixes for minor bugs.

* A new version of the Gradle plug-in that works with [Gradle 7](https://docs.gradle.org/7.0/release-notes.html) has been released as part of this patch. The plugin can be found in [Jenkins](https://ci01.dev.r3.com/blue/organizations/jenkins/Corda-Gradle-Build-Plugins%2Fcorda-gradle-plugins/detail/release%2F5.1.0-RC01/1/pipeline/).
For more information on how to use the plugin, visit its [GitHub repository](https://github.com/corda/samples-kotlin/tree/chrisr3-gradle7).

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this patch release:

* The `corda-shell --version` command now always returns the correct version.
* The time it takes for first-time flows to be run in a signed CorDapp has been significantly reduced.
* Java serialization has been disabled in the Corda firewall, closing a potential security vulnerability.
* Artemis messaging has been implemented to indicate when disk space is low (below 10%).
* AMQP frame tracing can now be turned on in the Corda node when running embedded Artemis or bridges. This is in addition to the previous ability to turn it on via firewall configuration.

### Database schema changes

* The `node_named_identities` table has been re-introduced. The table was removed in 4.7 following updates to certificate rotation functionality.
  * The reintroduction of the table means the behaviour of `rpcOps.wellKnownPartyFromX500Name` no longer functions differently for revoked and non-revoked identities.

## Corda: Enterprise Edition 4.9.1

Corda Enterprise 4.9.1 is a patch release of Corda Enterprise which includes dependency upgrades and fixes for minor bugs.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this patch release:

* Fixing of a bug where `SuspensionMeta` in `FlowInfo` shows as null even when a runnable flow has previously been hospitalized.
* Official Artemis binaries implemented.
* Oracle JDK version 8u322 now supported.

## Corda: Enterprise Edition 4.9

Corda: Enterprise Edition  4.9 features many security improvements, along with a stand alone Shell for controlling the node via command line. You can also now access the `flowrpcops` API.

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
* An issue preventing attachments to sub-flows in certain circumstances has been fixed.
