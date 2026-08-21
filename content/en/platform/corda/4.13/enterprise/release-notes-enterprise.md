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

## Corda Enterprise Edition 4.13.4 release notes

Corda Enterprise Edition 4.13.4 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* The following Critical vulnerabilities in dependencies have been addressed. High, medium and low severity CVE's have also been addressed but not listed here.

| Vulnerability  | Component |
|----------------|-----------|
| CVE-2026-54512 | Jackson   |
| CVE-2026-58062| BouncyCastle |
| CVE-2026-8763 | BouncyCastle |
| CVE-2026-59650 | BouncyCastle |
| CVE-2026-54513 | BouncyCastle |
| CVE-2026-44249 | Netty     |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.13.4. Dependencies with unchanged versions are omitted.

| Dependency | Name | 4.13.3 Enterprise | 4.13.4 Enterprise |
| ---------- | ---- | ----------------- | ----------------- |
| org.apache.activemq:artemis-\* | Artemis | 2.52.0 | 2.55.0 |
| org.bouncycastle:\*-lts8on | Bouncy Castle | 2.73.9 | 2.73.12 |
| com.fasterxml.jackson.\* | Jackson | 2.18.6 | 2.21.5 |
| com.fasterxml.jackson.module:jackson-module-kotlin | Jackson for Kotlin | 2.17.2 | 2.19.4 |
| org.eclipse.jetty.ee10:jetty-ee10-\* | Jetty | 12.0.33 | 12.0.36 |
| io.netty:netty-\* | Netty | 4.1.132.Final | 4.1.136.Final |
| org.apache.logging.log4j:\* | Log4j | 2.25.3 | 2.25.5 |
| org.apache.shiro:shiro-core | Shiro | 2.1.0 | 3.0.0 |
| org.hibernate:hibernate-\* | Hibernate | 5.6.14.Final | 5.6.15.Final |
| com.github.ben-manes.caffeine:caffeine | Caffeine | 3.1.8 | 3.2.3 |
| io.opentelemetry:\* | OpenTelemetry | 1.20.1 | 1.63.0 |
| io.opentelemetry.semconv:opentelemetry-semconv | OpenTelemetry SemConv | 1.20.1-alpha | 1.41.1 |
| com.azure:azure-identity | Azure Identity | 1.18.1 | 1.18.3 |
| com.azure.resourcemanager:azure-resourcemanager | Azure Resource Manager | 2.52.0 | 2.62.0 |
| org.apache.commons:commons-configuration2 | Commons Configuration2 | 2.11.0 | 2.15.0 |
| com.github.docker-java:docker-java | Docker Java | 3.6.0 | 3.7.0 |
| io.projectreactor.netty:reactor-netty-http | Reactor Netty | 1.2.10 (transitive) | 1.2.18 |
| io.micrometer:micrometer-core | Micrometer | 1.16.5 (transitive) | 1.16.6 |
| com.azure:azure-security-keyvault-keys | Azure Key Vault Keys | - | 4.10.6 |
| org.apache.httpcomponents.core5:httpcore5-h2 | HttpCore5 H2 | - | 5.3.6 |
| org.jsoup:jsoup | jsoup | - | 1.23.1 |

## Corda Enterprise Edition 4.13.3 release notes

Corda Enterprise Edition 4.13.3 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Revert the fix to handle stuck messages in Artemis. Previously on extremely rare occasions messages could become stuck in Artemis. This has now been resolved in Artemis.
* The following table shows the vulnerabilities addressed in this patch release.

| Vulnerability  | Component |
|----------------|-----------|
| CVE-2026-33870 | Netty     |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.13.3. Dependencies with unchanged versions are omitted.

| Dependency                          | Name    | Version |
|-------------------------------------|---------|--------|
| io.netty:netty-*                    | Netty   | 4.1.132.Final       |

## Corda Enterprise Edition 4.13.2 release notes

Corda Enterprise Edition 4.13.2 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Improved error reporting in RPCClientProxyHandler, for example when the user does not have sufficient permissions to perform an operation.
* The following table shows the vulnerabilities addressed in this patch release.

|Vulnerability| Component |
|-------------|-----------|
|CVE-2026-27446| Artemis   |
|CVE-2026-1605| Jetty     |
|CVE-2025-11143| Jetty     |
| CVE-2026-24400 | AssertJ   |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.12.10. Dependencies with unchanged versions are omitted.

| Dependency                          | Name           | Version       |
|-------------------------------------|----------------|---------------|
| com.fasterxml.jackson..*            | Jackson        | 2.18.6        |
| org.apache.activemq:artemis-*       | Artemis        | 2.52.0        |
| org.eclipse.jetty.ee10:jetty-ee10-* | Jetty          | 2.25.3        |

## Corda Enterprise Edition 4.13.1 release notes

Corda Enterprise Edition 4.13.1 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Fixed an issue where the Transaction Validator Utility failed when the logs directory was a symbolic link.
* The Transacton Validator Utility now has an option to vary the number of threads it uses when processing transactions. See the --help option of the
  tool or [Transaction Validator Utility]({{< relref "node/operating/tvu/tvu-cli.md" >}}) for more details.
* The Transaction Validator Utility can now vary the location of its log file via a system property. See [Transaction Validator Utility]({{< relref "node/operating/tvu/tvu-cli.md" >}}) for more details.
* The RPC listener of a Corda node can now be protected from brute-force login attempts and abusive authentication activity. For details of this and how
  to enable it see [rateLimit]({{< relref "node/setup/corda-configuration-fields.md#ratelimit" >}}).
* Quasar has been reverted back to version 0.9.0_r3. This being due to instrumentation issues being reported since version 4.12.6 when quasar was updated.
* Extra logging has been added if a node is unable to serialise an exception.

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.13.1. Dependencies with unchanged versions are omitted.

|Dependency|Name|Version|
|-----|-----|-----|
|org.glassfish.jersey.*|Jersey|2.21.0|
|org.assertj:assertj-core|AssertJ|3.27.7|
|io.netty:netty-*|Netty|4.1.130.Final|
|commons-io:commons-io|Commons IO|2.21.0|
|org.controlsfx:controlsfx|Controls FX|11.2.3|
|io.netty:netty-tcnative-*|TCNative|2.0.74.Final|
|org.apache.activemq:artemis-*|Artemis|2.44.0|
|org.apache.shiro:shiro-core|Shiro|2.1.0|
|com.azure:azure-identity|Azure Identity|1.18.1|
|org.apache.commons:commons-lang3|Commons Lang3|3.19.0|

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
