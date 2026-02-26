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

## Corda Open Source Edition 4.13.1 release notes

Corda Open Source Edition 4.13.1 is a patch release of Corda Community Edition focused on resolving issues and upgrading dependencies to address security updates.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Open Source release notes are on this page, and for the latest upgrade guide, refer to [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) and [Upgrading your node]({{< relref "node-upgrade-notes.md" >}}).

### Fixed issues

* The RPC listener of a Corda node can now be protected from brute-force login attempts and abusive authentication activity. For details of this and how
  to enable it see [rateLimit]({{< relref "corda-configuration-fields.md#ratelimit" >}}).
* Quasar has been reverted back to version 0.9.0_r3. This being due to instrumentation issues being reported since version 4.12.6 when quasar was updated.
* Extra logging has been added if a node is unable to serialise an exception.

### Third party components upgrade

- TODO

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

