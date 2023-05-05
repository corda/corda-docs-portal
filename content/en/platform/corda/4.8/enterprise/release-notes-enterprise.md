---
title: Corda Enterprise Edition 4.8 release notes
date: '2023-05-05'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-release-notes
    parent: about-corda-landing-4-8-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise
weight: 10
---


# Corda Enterprise Edition 4.8 release notes

## Corda Enterprise Edition 4.8.11 release notes

Corda Enterprise Edition 4.8.11 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](upgrading-index.md).

# Fixed issues

* A rare condition was fixed relating to rollback of database transactions under heavy load, which caused flow state machine threads to stop processing flows, leading to eventual node lock up in certain circumstances.

* Previously, a memory leak in the transaction cache occurred due to the weight of in-flight entries being undervalued. Improvements have been made to prevent in-flight entry weights from being undervalued and because they are now estimated more correctly, this results in a large decrease in the total size of cached entities.




## Corda Enterprise Edition 4.8.10 release notes

Corda Enterprise Edition 4.8.10 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](upgrading-index.md).

### Fixed issues

* Previously, when configured to use confidential identities and the Securosys PrimusX HSM, it was possible for Corda to fail to generate a wrapped key-pair for a new confidential identity. This would cause a temporary key-pair to be leaked, consuming resources in the HSM. This issue occurred when:

  * The Securosys HSM was configured in a master-clone cluster.

  * The master HSM had failed and Corda had failed-over to use the clone HSM.

  * There was an attempt to create a transaction using confidential identities.

  The issue is now resolved. When generating a wrapped key-pair, the temporary key-pair is not persisted in the HSM and thus cannot be leaked.

  On applying this update, it is recommended that the PrimusX JCE should be upgraded to version 2.3.4 or later for optimum performance of the HSM. If the JCE is not updated, then no keys are leaked but they are temporarily created in the HSM and are then garbage-collected within 24 hours.

  There is no need to upgrade the HSM firmware version for this update, but it is recommended to keep the firmware up to date as a matter of course. Currently the latest firmware version is 2.8.50.

## Corda Enterprise Edition 4.8.9 release notes

Corda Enterprise Edition 4.8.9 is a patch release of Corda Enterprise focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](upgrading-index.md).

### Fixed issues

* For CENM 1.4+, the `getNodeInfos()` bulk fetch mechanism now retrieves NodeInfos from the network map via an HTTP proxy, if a proxy has been configured.

## Corda Enterprise Edition 4.8.8 release notes

Corda Enterprise Edition 4.8.8 is a patch release of Corda Enterprise focused on CorDapp response time and security improvements.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](upgrading-index.md).

### Fixed issues

In this patch release:
* Java serialization has been disabled in the Corda firewall, closing a potential security vulnerability.
* The time it takes for first-time flows to be run in a signed CorDapp has been significantly reduced. This was achieved by fixing a regression introduced in Corda Enterprise Edition 4.8 involving the `ServiceLoader` used to load the `SerializationWhitelist`.

### Third party component upgrades

{{< table >}}

|Library|Version 4.8.8|Previous version|
|---------|-------|-------|
|Jackson|2.13.3|2.9.7|
|Netty|4.1.77.Final|4.1.46.Final|
|Quasar|0.7.15_r3|0.7.13_r3|
|Shiro|1.8.0|1.4.1|
|TCNative|2.0.48.Final|2.0.42.Final|

{{< /table >}}

## Corda Enterprise Edition 4.8.7 release notes

Corda Enterprise Edition 4.8.7 is a patch release of Corda Enterprise that ensures class compatibility.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this patch release:
* Backwards compatibility option (accessibility) for `RestrictedConnection` class, ensuring it respects `TargetVersion` correctly.

## Corda Enterprise Edition 4.8.6 release notes

Corda Enterprise Edition 4.8.6 is a patch release of Corda Enterprise which includes dependency upgrades and fixes for minor flow and ledger issues.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html).

### Fixed issues

In this patch release:

* Artemis keystore details have been added to the bridge configuration example in the [Firewall component overview](node/corda-firewall-component.html#full-production-ha-dmz-ready-mode-hotcold-node-hotwarm-bridge).
* Serializer configuration updated to fix an issue where a node could not restore its flow from checkpoints in cases of failure.
* Instances of the `ValidatingNotaryFlow` being incorrectly marked as an `IdempotentFlow` has been fixed.
* A rare issue where records could show up in the vault in an inconsistent state has been resolved. On failed database entries, the vault cache is now invalidated and re-synced with the database.
* The notarization `runSender` task has been updated to always use `myLegalName` instead of `serviceLegalName`.
* Log4J dependency updated to v2.17.1.
* ClassGraph package upgraded to v4.8.135 to provide greater security against XML eXternal Entity (XXE) attacks.
* Netty package upgraded to v4.1.67.Final to provide greater security against Denial of Service (DoS) attacks.
* Contracts no longer reuse the same instance of the `LedgerTransaction` and therefore can no longer maliciously or accidentally mutate states within the ledger.

## Corda Enterprise Edition 4.8.5 release notes

Corda Enterprise Edition 4.8.5 is a patch release of Corda Enterprise that fixes an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version 2.16.0.

To get started with this upgrade, request the download link by raising a ticket with [support](https://r3-cev.atlassian.net/servicedesk/customer/portal/2).

{{< warning >}}

Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.

{{< /warning >}}

### Upgrade recommendation

As a developer, you should urgently upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md" >}}).

As a node operator, you should urgently upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html).

### Fixed issues

In this patch release:

* Log4j dependency updated to version 2.16.0 to mitigate CVE-2021-44228.

## Corda Enterprise Edition 4.8.4 release notes

{{< warning >}}
Patch 4.8.4 contains dependency Log4j 2.15.0. A new vulnerability has been discovered in version 2.15.0 of the log4j logging library, as described here: https://nvd.nist.gov/vuln/detail/CVE-2021-45046. Apache has released version 2.16.0 of the library to address the issue. Corda Enterprise Edition 4.8.5 is due for release December 17 2021.
{{< /warning >}}

Corda Enterprise Edition 4.8.4 is a patch release of Corda Enterprise that attempted to fix an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency.

### Upgrade recommendation

When available, update to the next patch release, **Corda Enterprise Edition 4.8.5**, as soon as possible.

## Corda Enterprise Edition 4.8.3 release notes

Corda Enterprise Edition 4.8.3 is a patch release of Corda Enterprise that fixes an issue affecting flows on counterparty nodes in the event of certain notary exceptions.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

In this patch release:

* A fix has been added to prevent exceptions from the notary leading to hospitalized flows on counterparty nodes.


## Corda Enterprise Edition 4.8.2 release notes

Corda Enterprise Edition 4.8.2 is a patch release of Corda Enterprise that fixes security vulnerabilities in Corda Enterprise Edition 4.8 and 4.8.1, and offers greater compatibility with recent versions of FutureX.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

In this patch release:

* Compatibility with FutureX versions FXPKCS11 4.40 and FXJCA 1.33.
* A new FutureX configuration option has been introduced: `loginOnce`. This allows users to login only once, to match JWT continuous-keep-alive functionality. To enable this setting, use the updated configuration documentation. By default, `loginOnce` is set to `false`.
* There are now additional log entries from configured FutureX crypto service detailing when operation on the crypto service starts and ends.
* Notary support for Cockroach DB version 21.1.7.
* A fix to prevent a rare invalid notarization response after internal notary flow retry.
* Vulnerability fixes have been added to protect against Denial of Service (DoS) attacks via unchecked attachment files.
* Vulnerability fixes have been added to prevent sensitive information being retrievable from MSSQL databases via DDL script using the Data Management Tool.
* Corda Archive Service has been updated to prevent sensitive information being exposed in log files.
* Corda now uses newer versions of the Netty library (4.1.67 for io.netty:netty-common and 2.0.42 for io.netty:netty-tcnative-boringssl-static), which resolves some security vulnerabilities.
* Improvements to Checkpoint tooling to prevent record inconsistencies in some use cases.
* An error was fixed when using `FlowHandleWithClientId` to get subflow status via a subflow.
* A fix to improve enforcement of RPC authorisation matrix.
* Default index added for `transaction_id` and `output_index` on `state_party` table.

## Corda Enterprise Edition 4.8.1 release notes

Corda Enterprise Edition 4.8.1 is a patch release of Corda Enterprise that fixes a security vulnerability in Corda Enterprise Edition 4.8.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here]({{< relref "../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md" >}}).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

In this patch release:

* Support for Oracle 19C database has been validated.
* A fix has been introduced to reduce memory consumption during batched transaction resolution of large backchains.
* Support has been introduced for RedHat Enterprise Linux 8.x in Corda 4.8.1.
* Performance verification of the HA Notary with CockroachDB 20.2.8 has been carried out - performance is not worse in comparison to the HA Notary configured on CockroachDB 20.1.6.
* Support for PostgreSQL 13.8 for node databases has been added.
* Hibernate ORM has been updated to version to 5.4.32 to remove a security concern.
* The [Node management console](../../../../../en/platform/corda/4.8/enterprise/node/management-console.html#node-management-console) configuration has been updated. Configuration is now set in `node.management.plugin.middleware`, no longer `node.admin.middleware`.
* The [Flow management console](../../../../../en/platform/corda/4.8/enterprise/node/node-flow-management-console.html#flow-management-console) configuration has been updated. Configuration is now set in `flow.management.plugin.middleware`, no longer `flow.admin.middleware`.
* LedgerGraph has been updated to version 1.2.2. This upgrade minimizes memory footprint, and is not a functional change.

## Corda Enterprise Edition 4.8  release notes

Corda Enterprise Edition 4.8, released on April 21st 2021, includes several new features, enhancements, and fixes.

* The [notary database now supports Oracle database version 19c](#notary-database-support-update).
* You can use Azure-managed identities to authenticate [Azure Key Vault HSM](#azure-managed-identities-authentication)s.
* You can configure metrics to use [time-window reservoirs](#time-window-metrics-gathering) for data collection.
* Additional metrics have been added for [tracking notary latency](#additional-notary-metrics).
* Confidential identities support has been added via [Utimaco and Gemalto Luna HSMs](platform-support-matrix.html#hardware-security-modules-hsm).

{{< note >}}
This page only describes functionality specific to Corda Enterprise Edition 4.8. However, as a Corda Enterprise customer, you can also make full use of the features available as part of the Corda open source releases.

See the [Corda open source release notes](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-os/4.8/release-notes.md) for information about new features, enhancements, and fixes shipped as part of Corda 4.8.
{{< /note >}}

{{< note >}}
You can use states and CorDapps valid in Corda 3.0 and above with Corda 4.8 and Corda Enterprise Edition 4.8.


For the commitment Corda makes to wire and API stability, see [API stability guarantees](cordapps/api-stability-guarantees.md).
{{< /note >}}

## Long-term support release

[Corda 4.8](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-os/4.8/release-notes.md) and Corda Enterprise Edition 4.8 are our long-term support (LTS) platform versions.

R3 provides LTS for this release for 30 months starting April 21st 2021. This is 6 months longer than the support periods for previous releases, giving Corda customers extra time to plan for the next upgrade.

## Platform version change

Corda 4.8 uses platform version 10.

For more information about platform versions, see [Versioning]({{< relref "../../../../../en/platform/corda/4.8/enterprise/cordapps/versioning.md" >}}).

## New features and enhancements

### Notary database support update

The [JPA notary]({{< relref "../../../../../en/platform/corda/4.8/enterprise/notary/installing-jpa.md" >}}) now supports [Oracle DB version 19c](../../../../../en/platform/corda/4.8/enterprise/platform-support-matrix.html#jpa-notary-databases). This database is supported until April 30th 2027.

### Azure managed identities authentication

If you use an Azure Key Vault HSM with Corda Enterprise, you can now use an existing Azure Managed Identities service as authentication.

See [Using an HSM with Corda Enterprise](../../../../../en/platform/corda/4.8/enterprise/node/operating/cryptoservice-configuration.html#azure-keyvault) for more information.

### Time-window metrics gathering

You can now configure timer and histogram metrics to use time-window data gathering. Time-window data gathering collects all data points for a given time window, allowing outlying data points to be properly represented.

See [Node metrics](node/operating/monitoring-and-logging/node-metrics.md) for more information.

### Additional notary metrics

You can use `StartupQueueTime` and `BatchSignLatency` metrics to help calculate notary latency and assess notary worker performance across a notary cluster.

* `StartupQueueTime` represents the time a flow has been queued before starting, in milliseconds.
* `BatchSignLatency` represents the time elapsed during a batch signature, in milliseconds.

See [Monitoring Notary Latency](notary/faq/notary-latency-monitoring.md) for more information.


## Fixed issues

Corda Enterprise Edition 4.8 fixes:

* A security issue that affects notary systems that use the JPA notary implementation in an HA configuration and when the notary backing database has been set up using the Corda database management tool. The new version of the Corda [database management tool]({{< relref "../../../../../en/platform/corda/4.8/enterprise/database-management-tool.md" >}}) must be re-run for the fix to take effect.
* Several issues that cause memory leaks. As a result, we have added a new node configuration field - `enableURLConnectionCache` - and we have modified the `attachmentClassLoaderCacheSize` node configuration field. See the [node configuration fields page](../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#enterpriseconfiguration) for details.
* An issue where the node is unable to resolve transaction chains that contain states or contracts that it did not relate to installed CorDapps.
* Flow state, invocation source, and suspension source filters breaking in the node GUI.
* Transaction verification being performed outside of the attachments class loader.
* HA utilities not logging messages that state that the master key is not needed when using a native mode HSM.
* HA utilities not logging information about the `freshIdentitiesConfiguration`.
* Log messages incorrectly stating that a confidential identity key has been created.
* An issue that causes the node to hang if shut down using `SIGTERM`.
* Attachment presence cache containing the attachment contents.
* The Corda Firewall throwing an error when retrieving version information.
* HA utilities creating erroneous logs when using confidential identities.

## Known issues

* An issue with the Oracle 12c database that causes the JDBC driver to hang if blocked by an empty entropy pool.

{{< note >}}
This issue is specific to Corda Enterprise Edition 4.8. Known issues relating to other versions of Corda Enterprise are listed in the release notes for each version.
{{< /note >}}

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
