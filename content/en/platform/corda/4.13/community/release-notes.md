---
title: Corda Open Source Edition 4.13 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2024-06-04'
menu:
  corda-community-4-13:
    identifier: corda-community-4-13-release-notes
    parent: about-corda-landing-4-13-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Open Source Edition 4.13 release notes

## Corda Open Source Edition 4.13.3 release notes

Corda Open Source Edition 4.13.3 is a patch release of Corda Community Edition focused on resolving issues and upgrading dependencies to address security updates.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Open Source release notes are on this page, and for the latest upgrade guide, refer to [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) and [Upgrading your node]({{< relref "node-upgrade-notes.md" >}}).

### Fixed issues

* The following vulnerabilities in dependencies have been addressed:

| Vulnerability  | Component |
|----------------|-----------|
| CVE-2026-33870 | Netty     |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Open Source 4.13.3. Dependencies with unchanged versions are omitted.

| Dependency                          | Name    | Version |
|-------------------------------------|---------|--------|
| io.netty:netty-*                    | Netty   | 4.1.132.Final       |

## Corda Open Source Edition 4.13.2 release notes

Corda Open Source Edition 4.13.2 is a patch release of Corda Community Edition focused on resolving issues and upgrading dependencies to address security updates.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Open Source release notes are on this page, and for the latest upgrade guide, refer to [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) and [Upgrading your node]({{< relref "node-upgrade-notes.md" >}}).

### Fixed issues

* Improved error reporting in RPCClientProxyHandler, for example when the user does not have sufficient permissions to perform an operation.
* The following vulnerabilities in dependencies have been addressed:

| Vulnerability   | Component |
|-----------------|----------|
| CVE-2026-27446  | Artemis  |
| CVE-2026-1605   | Jetty    |
| CVE-2025-11143  | Jetty    |
| CWE-770| Jackson |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Open Source 4.13.2. Dependencies with unchanged versions are omitted.

| Dependency                          | Name           | Version       |
|-------------------------------------|----------------|---------------|
| com.fasterxml.jackson..*            | Jackson        | 2.18.6        |
| org.apache.activemq:artemis-*       | Artemis        | 2.52.0        |
| org.eclipse.jetty.ee10:jetty-ee10-* | Jetty          | 2.25.3        |

## Corda Open Source Edition 4.13.1 release notes

Corda Open Source Edition 4.13.1 is a patch release of Corda Community Edition focused on resolving issues and upgrading dependencies to address security updates.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Open Source release notes are on this page, and for the latest upgrade guide, refer to [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) and [Upgrading your node]({{< relref "node-upgrade-notes.md" >}}).

### Fixed issues

* Improved error reporting in RPCClientProxyHandler, for example when the user does not have sufficient permissions to perform an operation.
* The following vulnerabilities in dependencies have been addressed:

| Vulnerability   | Component |
|-----------------|----------|
| CVE-2026-27446  | Artemis  |
| CVE-2026-1605   | Jetty    |
| CVE-2025-11143  | Jetty    |
| CWE-770| Jackson |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Open Source 4.12.10. Dependencies with unchanged versions are omitted.

| Dependency                          | Name           | Version       |
|-------------------------------------|----------------|---------------|
| com.fasterxml.jackson..*            | Jackson        | 2.18.6        |
| org.apache.activemq:artemis-*       | Artemis        | 2.52.0        |
| org.eclipse.jetty.ee10:jetty-ee10-* | Jetty          | 2.25.3        |

## Corda Open Source Edition 4.13 release notes

The Corda Open Source Edition 4.13 release introduces new functionality and third-party component upgrades.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Open Source release notes are on this page, and for the latest upgrade guide, refer to [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) and [Upgrading your node]({{< relref "node-upgrade-notes.md" >}}).

## Platform version change

Corda 4.13 uses platform version 150.

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

## New features, enhancements and restrictions

### Notary change flow

The transaction hierarchy, [FinalityFlow]({{< relref "api-flows.md#finalityflow" >}}), and NotaryChangeFlow have been generalized so that they can be used with NotaryChange transactions as well as with WireTransaction.

### RPC thread pool

The RPC clients ([CordaRPCClient](../../../../../../../en/api-ref/corda/4.13/community/javadoc/net/corda/client/rpc/CordaRPCClient.html), [RPCClient](../../../../../../../en/api-ref/corda/4.13/community/javadoc/net/corda/client/rpc/internal/RPCClient.html), and [MultiRPCClient](../../../../../../../en/api-ref/corda/4.13/community/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html)) can now be configured to use Artemis global thread pools by setting their `useGlobalThreadPools` Boolean parameter to true. This allows multiple connections to share a bounded set of scheduler and worker threads, rather than creating dedicated pools per client.

(For Kotlin Docs, see [CordaRPCClient](../../../../../../../en/api-ref/corda/4.13/community/kotlin/docs/net.corda.client.rpc/-corda-r-p-c-client/index.html), [RPCClient](../../../../../../../en/api-ref/corda/4.13/community/kotlin/docs/net.corda.client.rpc.internal/-r-p-c-client/index.html), and [MultiRPCClient](../../../../../../../en/api-ref/corda/4.13/community/kotlin/docs/net.corda.client.rpc.ext/-multi-r-p-c-client/index.html).

## Third-party component upgrades

The following table lists the dependency version changes for 4.13 Open Source Editions:

| Dependency                                      | Name                    | New Version   |
|-------------------------------------------------|-------------------------|---------------|
| org.apache.activemq:*                           | Apache ActiveMQ Artemis | 2.44.0        |
| com.azure:azure-identity:*                      | Azure Identity          | 1.18.1        |
| org.apache.commons:commons-lang3                | Commons Lang            | 3.19.0        |
| org.glassfish.jersey.*                          | Jersey                  | 3.1.11        |
| org.apache.logging.log4j:*                      | Log4j                   | 2.25.1        |
| io.netty:*                                      | Netty                   | 4.1.128.Final |
| io.netty:netty-tcnative-boringssl-static        | Netty TCNative          | 2.0.74.Final  |
| org.apache.qpid:proton-j                        | ProtonJ                 | 0.34.1        |

