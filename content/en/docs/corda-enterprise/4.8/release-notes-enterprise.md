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

Corda Enterprise 4.8, released on 21 April 2021, includes several new features, enhancements, and fixes.

{{< note >}}
States and CorDapps valid in Corda 3.0 and above, are usable in Corda 4.8 and Corda Enterprise 4.8.


For the commitment Corda makes to wire and API stability, see [API stability guarantees](cordapps/api-stability-guarantees.md).
{{< /note >}}

New features and enhancements in Corda Enterprise 4.8 include:

* Added support for version 19c of the [Oracle database as a notary database](#notary-database-support-updates).
* Added support for Azure managed identities as authentication when using an [Azure Key Vault HSM](#azure-managed-identities-authentication).
* Metrics can now be configured to use [time-window reservoirs](#time-window-metrics-gathering) for data collection.
* Additional metrics have been added for [tracking notary latency](#additional-notary-metrics).
* Confidential identities now support [Utimaco and Gemalto Luna HSMs](#confidential-identity-key-on-hsms).

{{< note >}}
This page only describes functionality specific to Corda Enterprise 4.8. However, as a Corda Enterprise customer, you can also make full use of the features available as part of the Corda open source releases.

See the [Corda open source release notes](../../corda-os/4.8/release-notes.md) for information about new features, enhancements, and fixes shipped as part of Corda 4.8.
{{< /note >}}

## Long-term support release

As part of our first major Corda release for 2021, [Corda 4.8](../../corda-os/4.8/release-notes.md) and Corda Enterprise 4.8 are our long-term support (LTS) platform versions, which bring improvements and stability fixes that continue to enhance the maturity of the platform as a whole.

LTS for this release will be provided for 30 months from 21 April 2021, 6 months more than our previous support period, giving Corda customers extra time to plan for the next upgrade.

## Platform version change

The platform version of Corda 4.8 is 10.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## New features and enhancements

### Notary database support updates

The [JPA notary](notary/installing-jpa.md) now supports [Oracle DB version 19c](platform-support-matrix.md#jpa-notary-databases). This database is supported until April 30th, 2027, providing long-term support for this Corda release.

### Azure managed identities authentication

When using an Azure Key Vault HSM with Corda Enterprise, you can now use an existing Azure Managed Identities service as authentication. See [Using an HSM with Corda Enterprise](node/operating/cryptoservice-configuration.md#azure-keyvault) for more information.

### Time-window metrics gathering

Timer and histogram metrics can now be configured to use time-window data gathering. Time-window data gathering collects all data points for a given time window, allowing outlying data points to be properly represented.

See [Node metrics](node-metrics.md) for more information.

### Additional notary metrics

Two new metrics have been added that can be used to help calculate notary latency. The `StartupQueueTime` and `BatchSignLatency` metrics can be used to help when calculating notary latency and assessing notary worker performance across a notary cluster.

* The `StartupQueueTime` represents the time a flow has been queued before starting, in milliseconds.
* The `BatchSignLatency` metric represents the time elapsed during a batch signature in milliseconds.

See [Monitoring Notary Latency](notary/faq/notary-latency-monitoring.md) for more information.

### Confidential identity key on HSMs

* Confidential identities now support [Utimaco and Gemalto Luna HSMs](platform-support-matrix.md#hardware-security-modules-hsm).


## Fixed issues

* We have fixed a security issue that affects notary systems that use the JPA notary implementation in an HA configuration, and when the notary backing database has been set up using the Corda database management tool. The new version of the Corda [database management tool](database-management-tool.md) must be re-run for the fix to take effect.
* We have fixed several issues that caused memory leaks. As a result, we have added a new node configuration field - `enableURLConnectionCache` - and we have modified the `attachmentClassLoaderCacheSize` node configuration field. See the [node configuration fields page](node/setup/corda-configuration-fields.md#enterpriseconfiguration) for details.
* We have fixed an issue where the node would be unable to resolve transaction chains that contained states or contracts that it did not relate to installed CorDapps.
* We have fixed an issue that caused flow state, invocation source, and suspension source filters to break in the node GUI.
* We have fixed an issue that caused transaction verification to be performed outside of the attachments class loader.
* We have fixed an issue where HA utilities did not log a message stating that the master key was not needed when using a native mode HSM.
* We have fixed an issue where HA utilities did not log information about the `freshIdentitiesConfiguration`.
* We have fixed an issue where a log message incorrectly stated that a confidential identity key was created.
* We have fixed an issue that could cause a node to hang if shut down using `SIGTERM`.
* We have fixed an issue where the attachment presence cache contained the attachment contents.
* We have fixed an issue where the Corda Firewall threw an error when retrieving version information.
* We have fixed an issue where the HA utilities created erroneous logs when using confidential identities.

## Known issues

* When using the Oracle 12c database, the JDBC driver can hang when it is blocked by an empty entropy pool at random times.

{{< note >}}
This issue is specific to Corda Enterprise 4.8. For known issues specific to a particular Corda Enterprise version, see the release notes for that version. 
{{< /note >}}
