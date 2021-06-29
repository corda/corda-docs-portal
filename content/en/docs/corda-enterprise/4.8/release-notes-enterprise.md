---
date: '2021-06-29'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-release-notes
    name: "Release notes"
tags:
- release
- notes
- enterprise
title: Corda Enterprise release notes
weight: 1
---


# Corda Enterprise release notes

## Corda Enterprise 4.8 release overview

Corda Enterprise 4.8, released on April 21st 2021, includes several new features, enhancements, and fixes including:

* Support added for version 19c of the [Oracle database as a notary database](#notary-database-support-updates).
* Support added for Azure managed identities as authentication when using an [Azure Key Vault HSM](#azure-managed-identities-authentication).
* Metrics can now be configured to use [time-window reservoirs](#time-window-metrics-gathering) for data collection.
* Additional metrics added for [tracking notary latency](#additional-notary-metrics-added).
* Confidential identities now support [Utimaco and Gemalto Luna HSMs](#confidential-identity-key-on-hsms).

{{< note >}}
This page only describes functionality specific to Corda Enterprise 4.8. However, as a Corda Enterprise customer, you can also make full use of the features available as part of the Corda open source releases.

See the [Corda open source release notes](../../corda-os/4.8/release-notes.md) for information about new features, enhancements, and fixes shipped as part of Corda 4.8.
{{< /note >}}

{{< note >}}
You can use states and CorDapps valid in Corda 3.0 and above with Corda 4.8 and Corda Enterprise 4.8.


For the commitment Corda makes to wire and API stability, see [API stability guarantees](cordapps/api-stability-guarantees.md).
{{< /note >}}

## Long-term support release

[Corda 4.8](../../corda-os/4.8/release-notes.md) and Corda Enterprise 4.8 are our long-term support (LTS) platform versions.

R3 provides LTS for this release for 30 months starting April 21st 2021. This is 6 months longer than the support periods for previous releases, giving Corda customers extra time to plan for the next upgrade.

## Platform version change

The platform version of Corda 4.8 is 10.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## New features and enhancements

### Notary database support update

The [JPA notary](notary/installing-jpa.md) now supports [Oracle DB version 19c](platform-support-matrix.md#jpa-notary-databases). This database is supported until April 30th 2027.

### Azure managed identities authentication

When using an Azure Key Vault HSM with Corda Enterprise, you can now use an existing Azure Managed Identities service as authentication. See [Using an HSM with Corda Enterprise](node/operating/cryptoservice-configuration.md#azure-keyvault) for more information.

### Time-window metrics gathering

You can now configure timer and histogram metrics to use time-window data gathering. Time-window data gathering collects all data points for a given time window, allowing outlying data points to be properly represented.

See [Node metrics](node-metrics.md) for more information.

### Additional notary metrics added

You can use `StartupQueueTime` and `BatchSignLatency` metrics to help calculate notary latency and assess notary worker performance across a notary cluster.

* `StartupQueueTime` represents the time a flow has been queued before starting, in milliseconds.
* `BatchSignLatency` represents the time elapsed during a batch signature, in milliseconds.

See [Monitoring Notary Latency](notary/faq/notary-latency-monitoring.md) for more information.

### Confidential identity key on HSMs

* Confidential identities now support [Utimaco and Gemalto Luna HSMs](platform-support-matrix.md#hardware-security-modules-hsm).


## Fixed issues

Corda Enterprise 4.8 fixes:

* A security issue that affects notary systems that use the JPA notary implementation in an HA configuration, and when the notary backing database has been set up using the Corda database management tool. The new version of the Corda [database management tool](database-management-tool.md) must be re-run for the fix to take effect.
* Several issues that caused memory leaks. As a result, we have added a new node configuration field - `enableURLConnectionCache` - and we have modified the `attachmentClassLoaderCacheSize` node configuration field. See the [node configuration fields page](node/setup/corda-configuration-fields.md#enterpriseconfiguration) for details.
* An issue where the node is unable to resolve transaction chains that contained states or contracts that it did not relate to installed CorDapps.
* Flow state, invocation source, and suspension source filters to break in the node GUI.
* Transaction verification being performed outside of the attachments class loader.
* HA utilities not logging messages that state the master key is not needed when using a native mode HSM.
* HA utilities not logging information about the `freshIdentitiesConfiguration`.
* Log messages incorrectly stating that a confidential identity key has been created.
* An issue that causes the node to hang if shut down using `SIGTERM`.
* Attachment presence cache containing the attachment contents.
* The Corda Firewall threwing an error when retrieving version information.
* HA utilities creating erroneous logs when using confidential identities.

## Known issues

* When using the Oracle 12c database, the JDBC driver may hang if it is blocked by an empty entropy pool.

{{< note >}}
This issue is specific to Corda Enterprise 4.8. Known issues relating to other versions of Corda Enterprise are listed in the release notes for each version.  
{{< /note >}}
