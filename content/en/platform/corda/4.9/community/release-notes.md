---
title: Corda Community Edition 4.9 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2023-05-05'
menu:
  corda-community-4-9:
    identifier: corda-community-4-9-release-notes
    weight: -5
    name: "Release notes"
tags:
- release
- notes
---

# Corda Community Edition 4.9 release notes

## Corda Community Edition 4.9.7 release notes

Corda Community Edition 4.9.7 is a patch release of Corda Community Edition which includes resolved issues.

### Fixed issues

* Corda provides the NodeDriver to help developers write integration tests. Using the NodeDriver, developers can bring up nodes locally to run flows and inspect state updates. Previously, there was an issue with build pipelines with tests failing, as on some occasions, notaries took more than one minute (the default timeout value) to start.

  To resolve this, the NodeDriver now has a new parameter, notaryHandleTimeout. This parameter specifies how long to wait (in minutes) for a notary handle to come back after the notary has been started.

* A fix for cache eviction has been applied where an issue resulted in an incorrect contract verification status while a database transaction was in progress during contract verification.

* The SSL handshake timeout has been increased to 60 seconds. If during SSL handshake, certificate revocation lists (CRLs) take a long time to download, or are unreachable, then the 60 seconds gives the node enough time to establish the connection if `crlCheckSoftFail` is enabled.

* The certificate revocation checking has been improved with the introduction of a read timeout on the download of the certificate revocation lists (CRLs). The default CRL connect timeout has also been adjusted to better suit Corda nodes. The caching of CRLs has been increased from 30 seconds to 5 minutes.

## Corda Community Edition 4.9.6 release notes

Corda Community Edition 4.9.6 is a patch release of Corda Community Edition to keep it synchronised with the release of Corda Enterprise Edition 4.9.6.

## Corda Community Edition 4.9.5 release notes

Corda Community Edition 4.9.5 is a patch release of Corda Community Edition which includes resolved issues.

### Fixed issues

* Previously, a memory leak in the transaction cache occurred due to the weight of in-flight entries being undervalued. Improvements have been made to prevent in-flight entry weights from being undervalued and because they are now estimated more correctly, this results in a large decrease in the total size of cached entities.

* A rare condition was fixed relating to roll back of database transactions under heavy load, which caused flow state machine threads to stop processing flows, leading to eventual node lock up in certain circumstances.

## Corda Community Edition 4.9.2 release notes

Corda Community 4.9.2 is a patch release of Corda Community which includes the addition of a new Gradle 7 plugin, security upgrades, and fixes for minor bugs.

### Fixed issues

* As part of this patch a new Gradle plugin is provided that supports CorDapp development using Gradle 7. This is in addition to the existing Gradle support. The plugin has been uploaded to Artifactory.
  * Samples demonstrating Gradle 7 usage are available for:
    * [Kotlin](https://github.com/corda/samples-kotlin/tree/chrisr3-gradle7)
    * [Java](https://github.com/corda/samples-java/tree/chrisr3-gradle7)
  * A readme describing the Gradle 7 plugin is also available on [Github](https://github.com/corda/corda-gradle-plugins/tree/release/5.1/cordapp).
* Artemis messaging has been implemented to indicate when disk space is low (below 10%).
* AMQP frame tracing can now be enabled in the Corda node when running embedded Artemis or bridges. This is in addition to the previous ability to turn it on via firewall configuration.

### Fixed issues

The following issues were resolved in this patch release:

* The `corda-shell --version` command has been updated to always return the correct version.
* The time it takes for first-time flows to be run in a signed CorDapp has been significantly reduced.
* Java serialization has been disabled in the Corda firewall, closing a potential security vulnerability.

### Third party component upgrades

{{< table >}}

|Library|Version 4.9.2|Previous version|
|---------|-------|-------|
|Caffeine|2.9.3|2.7.0|
|Jackson|2.13.3|2.13.1|
|Netty|4.1.77.Final|4.1.68.Final|
|Quasar|0.7.15_r3|0.7.14_r3|
|Shiro|1.9.1|1.4.1|

{{< /table >}}

## Corda Community Edition 4.9.1 release notes

Corda Community Edition 4.9.1 is a patch release of Corda Community Edition which includes minor bug fixes and dependency upgrades.

### Fixed issues

In this patch release:

* Fixing of a bug where `SuspensionMeta` in `FlowInfo` shows as null even when a runnable flow has previously been hospitalized.
* Update Hibernate version to a more secure version that matches Corda Enterprise.
* Oracle JDK version 8u322 now supported.

## Corda Community Edition 4.9 release notes

**Corda Community Edition** is here. This edition of Corda gives you the freedom of Corda's Community Edition platform, with the benefits of [affordable support](https://r3.com/support). All the same fundamentals of Corda 4.8 are included, along with security updates, newly available APIs and sample code improvements. You can upgrade your existing Corda projects to Community Edition any time to be eligible for our support packages.

## Highlights

The Corda Community Edition features:

* Support for your open source projects. [Find out more about available support and how to upgrade](https://docs.r3.com/en/platform/corda/4.9/community.html).
* An open source version of network map and doorman is available and recommended for Community Edition users, provided by Cordite.
* Community Edition Docker images are now available.
* Access to node health data and node status.

{{< note >}}
Support for Corda: Community Edition 4.9 does not include experimental notaries. Check the [Platform Support Matrix](release-platform-support-matrix.md) for more information.
{{< /note >}}

## Platform version change

Corda 4.9 uses platform version 11.

For more information about platform versions, see [Versioning](versioning.md).

## Fixed issues

Issues fixed in Corda Community 4.9:

* Corda Shell has been removed to its own repository for improved security. You can now use a standalone shell outside of the node, or from within the node's drivers.  You can read more about using the standalone shell [here](shell.html#the-standalone-shell).
* Security updates to prevent possibility of Denial of Service attacks.
* Improvements to demos and sample code.
* Improvements to improve compatibility with Intel Macs.
* An issue affecting Node JVM deadlocks is resolved.
* An issue with failed attachments from a notary has been fixed.
* An issue preventing attachments to subflows in certain circumstances has been fixed.

### Database Schema Changes

* The `node_named_identities` table has been re-introduced. It was removed in Corda Enterprise Edition 4.7 following updates to certificate rotation functionality.

  The reintroduction of this table ensures that the behavior of `rpcOps.wellKnownPartyFromX500Name` is identical for both revoked and non-revoked identities.
