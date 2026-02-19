---
title: Corda Enterprise Edition 4.13 release notes
date: '2025-06-30'

menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-release-notes
    parent: about-corda-landing-4-13-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.13 release notes

## Corda Enterprise Edition 4.13.1 release notes

Corda Enterprise Edition 4.13.1 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

- TODO

### Third-party components upgrade

TODO

## Corda Enterprise Edition 4.13 release notes

The Corda Enterprise Edition 4.13 release introduces new functionality and third-party component upgrades.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

## Platform version change

Corda 4.13 uses platform version 150.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features, enhancements and restrictions

### Segregated thread pools

Segregated thread pools can now be defined and have flows assigned to them.
Thread pools enable operators to prioritize particular flows and to segregate them from other flows.
Corda Enterprise targets the flow thread pools directly when it starts a flow. Therefore, there is no conflict between
starting flows if one pool is performing badly and has a big queue.

For more information, see [Segregated thread pools]({{< relref "cordapps/thread-pools.md" >}}).

### Automatic ledger recovery
Ledger recovery flow can now be launched automatically at node startup. For more information see [Automatic ledger recovery]({{< relref "node/ledger-recovery/automatic-ledger-recovery.md" >}}). To facilitate this, a new phase has been added to the node where only system flows run. The only supported runnable system flow is
Ledger Recovery.

For more information, see [System flows]({{< relref "cordapps/system-flows.md" >}}).

### Read-only nodes

Nodes can now be configured to be read-only. Making a node read-only is a feature that is used for many reasons, including for regulatory reasons and to provide scalable reporting solutions.

For more information, see [Read-only nodes]({{< relref "node/setup/read-only-nodes.md" >}}).

### Additional monitoring metrics

Additional metrics have been implemented.

For the latest list, see [Node metrics]({{< relref "node/operating/monitoring-and-logging/node-metrics.md" >}}).

### RPC thread pool

The RPC clients ([CordaRPCClient](../../../../../../../en/api-ref/corda/4.13/enterprise/javadoc/net/corda/client/rpc/CordaRPCClient.html), [RPCClient](../../../../../../../en/api-ref/corda/4.13/enterprise/javadoc/net/corda/client/rpc/internal/RPCClient.html), and [MultiRPCClient](../../../../../../../en/api-ref/corda/4.13/enterprise/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html)) can now be configured to use Artemis global thread pools by setting their `useGlobalThreadPools` Boolean parameter to true. This allows multiple connections to share a bounded
set of scheduler and worker threads, rather than creating dedicated pools per client.

(For Kotlin Docs, see [CordaRPCClient](../../../../../../../en/api-ref/corda/4.13/enterprise/kotlin/docs/net.corda.client.rpc/-corda-r-p-c-client/index.html), [RPCClient](../../../../../../../en/api-ref/corda/4.13/enterprise/kotlin/docs/net.corda.client.rpc.internal/-r-p-c-client/index.html), and [MultiRPCClient](../../../../../../../en/api-ref/corda/4.13/enterprise/kotlin/docs/net.corda.client.rpc.ext/-multi-r-p-c-client/index.html).

### Notary change flow

The transaction hierarchy, [FinalityFlow]({{< relref "cordapps/api-flows.md#finalityflow" >}}), and NotaryChangeFlow have been generalized so that they can be used with NotaryChange transactions as well as with WireTransaction.

### Changes in Log4j plugin discovery

From 4.13, the following JARs contain Log4j2Plugins.dat files, which are required for registering newer Log4j2 plugins:

- corda-common-logging-4.13.jar
- corda-node-api-4.13.jar

If these JARs are used with other sources using Log4j Core, the correct handling of the potentially
conflicting files is required to guarantee correct behavior.

For more information, see:

https://logging.apache.org/log4j/2.x/faq.html#single-jar

For example, if you use Gradle Shadow plugin, you need to use the relevant transformer:

https://gradleup.com/shadow/configuration/merging/#merging-log4j2-plugin-cache-files-log4j2pluginsdat

### CENM compatibility

Except for exceptions stated in CENM release notes, this version of Corda is compatible with all currently released versions of CENM.

## Known issues

### Automatic ledger recovery and finalization

Automatic ledger recovery is run with `alsoFinalize` set to false. This means when recovering transactions if any are in the IN_FLIGHT status
they are not automatically recovered to Verified status. To have your in-flight transactions recovered, you need to manually run the flow ledger finality recovery.

## Third-party component upgrades

The following table lists the dependency version changes for 4.13 Enterprise Editions:

| Dependency                               | Name         | New Version             |
| ---------------------------------------- | ------------ | ----------------------- |
| org.apache.activemq:*                    | Artemis      | 2.44.0                  |
| org.apache.commons:commons-lang3         | Commons Lang | 3.19.0                  |
| org.glassfish.jersey.*                   | Jersey       | 3.1.11                  |
| org.apache.logging.log4j:*               | Log4J        | 2.25.1                  |
| io.netty:*                               | netty        | 4.1.128.Final           |
| io.netty:netty-tcnative-boringssl-static | tcnative     | 2.0.74.Final            |
