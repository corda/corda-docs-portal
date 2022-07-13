---
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2021-06-29'
menu:
  corda-community-4-9:
    identifier: corda-community-4-9-release-notes
    weight: 1
tags:
- release
- notes
title: Release notes
---

# Corda Community Edition release notes

## Corda Community Edition 4.9.2

Corda Community 4.9.2 is a patch release of Corda Enterprise which includes the addition of a new Gradle 7 plugin, security upgrades, and fixes for minor bugs.

* A new version of the Gradle plug-in that works with [Gradle 7](https://docs.gradle.org/7.0/release-notes.html) has been released as part of this patch. The plugin can be found in [Jenkins](https://ci01.dev.r3.com/blue/organizations/jenkins/Corda-Gradle-Build-Plugins%2Fcorda-gradle-plugins/detail/release%2F5.1.0-RC01/1/pipeline/).
  For more information on how to use the plugin, visit its [GitHub repository](https://github.com/corda/samples-kotlin/tree/chrisr3-gradle7).

### Fixed issues

In this patch release:

* The `corda-shell --version` command now always returns the correct version.
* The time it takes for first-time flows to be run in a signed CorDapp has been significantly reduced.
* Disabling Java serialization in the Corda firewall, closing a potential security vulnerability.
* Artemis messaging has been implemented to indicate when disk space is low (below 10%).
* AMQP frame tracing can now be turned on in the Corda node when running embedded Artemis or bridges. This is in addition to the previous ability to turn it on via firewall configuration.

## Corda Community Edition 4.9.1

Corda Community Edition 4.9.1 is a patch release of Corda Community Edition which includes minor bug fixes and dependency upgrades.

### Fixed issues

In this patch release:

* Fixing of a bug where `SuspensionMeta` in `FlowInfo` shows as null even when a runnable flow has previously been hospitalized.
* Update Hibernate version to a more secure version that matches Corda Enterprise.
* Oracle JDK version 8u322 now supported.

## Corda Community Edition 4.9

**Corda Community Edition** is here. This edition of Corda gives you the freedom of Corda's Open Source platform, with the benefits of [affordable support](https://r3.com/support). All the same fundamentals of Corda 4.8 are included, along with security updates, newly available APIs and sample code improvements. You can upgrade your existing Corda projects to Community Edition any time to be eligible for our support packages.

## Highlights

The Corda Community Edition features:

* Support for your open source projects. [Find out more about available support and how to upgrade](https://docs.r3.com/en/platform/corda/4.9/community.html).
* An Open Source version of network map and doorman is available and recommended for Community Edition users, provided by Cordite.
* Community Edition Docker images are now available.
* The `flowrpcops` API is available and documented. You can use this to start, pause, and retry flows and hospitalized flows.
* Access to node health data and node status.

{{< note >}}
Support for Corda: Community Edition 4.9 does not include experimental notaries. Check the [Platform Support Matrix](release-platform-support-matrix.md) for more information.
{{< /note >}}

## Platform version change

Corda 4.9 uses platform version 11.

For more information about platform versions, see [Versioning](../../../../../en/platform/corda/4.9/community/versioning.md).

## Fixed issues

Issues fixed in Corda Community 4.9:

* Corda Shell has been removed to its own repository for improved security. You can now use a standalone shell outside of the node, or from within the node's drivers.  You can read more about using the standalone shell [here](shell.html#the-standalone-shell).
* Security updates to prevent possibility of Denial of Service attacks.
* Improvements to demos and sample code.
* Improvements to improve compatibility with Intel Macs.
* An issue affecting Node JVM deadlocks is resolved.
* An issue with failed attachments from a notary has been fixed.
* An issue preventing attachments to subflows in certain circumstances has been fixed.
