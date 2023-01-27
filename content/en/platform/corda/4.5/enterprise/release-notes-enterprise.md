---
title: Corda Enterprise Edition 4.5 release notes
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    identifier: "corda-enterprise-4-5-release-notes"
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 1

---


# Corda Enterprise Edition 4.5 release notes

## Corda Enterprise Edition 4.5.11

Corda Enterprise Edition 4.5.11 is a patch release of Corda Enterprise focused on security improvements and fixing an issue with the `gracefulShutdown`.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

### Fixed issues

In this patch release:
* Java serialization has been disabled in the Corda firewall, closing a potential security vulnerability.
* Fixed an issue where the `gracefulShutdown` command intermittently would fail to shut the node down.

### Third party component upgrades

{{< table >}}

|Library|Version 4.5.11|Previous version|
|---------|-------|-------|
|Bean Utils|1.9.4|1.9.3|
|Class Graph|4.8.135|4.8.90|
|Hibernate|5.4.3.Final|5.4.32.Final/
|Jackson|2.13.3|2.9.7|
|Netty|4.1.77.Final|4.1.46.Final|
|Quasar|0.7.15_r3|0.7.13_r3|
|Shiro|1.8.0|1.4.1|
|TCNative|2.0.48.Final|2.0.14.Final|

{{< /table >}}

## Corda Enterprise Edition 4.5.10 release notes

Corda Enterprise Edition 4.5.10 is a patch release of Corda Enterprise that fixes an urgent security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html).

### Fixed issues

In this patch release:
* Backwards compatibility option (accessibility) for `RestrictedConnection` class, ensuring it respects `TargetVersion` correctly.

## Corda Enterprise Edition 4.5.9 release notes

Corda Enterprise Edition 4.5.9 is a patch release of Corda Enterprise that fixes an urgent security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html).

### Fixed issues

In this patch release:

* Log4j dependency updated to version 2.17.1 to fix pre-existing Log4j issues.

## Corda Enterprise Edition 4.5.8 release notes

{{< note >}}

This is a direct upgrade from 4.5.6. No version 4.5.7 was released.

{{< /note >}}

Corda Enterprise Edition 4.5.8 is a patch release of Corda Enterprise that fixes an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version 2.16.0.

To get started with this upgrade, request the download link by raising a ticket with [support](https://r3-cev.atlassian.net/servicedesk/customer/portal/2).

{{< warning >}}

Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.

{{< /warning >}}

### Upgrade recommendation

As a developer, you should urgently upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md).

As a node operator, you should urgently upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html).

### Fixed issues

In this patch release:

Log4j dependency updated to version 2.16.0 to mitigate CVE-2021-44228.

## Corda Enterprise Edition 4.5.6 release notes

Corda Enterprise Edition 4.5.6 is a patch release of Corda Enterprise that fixes an invalid notarization response being sent
after an internal notary flow retry.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* A fix has been added to prevent a rare invalid notarization response after internal notary flow retry.

## Corda Enterprise Edition 4.5.5 release notes

Corda Enterprise Edition 4.5.5 is a patch release of Corda Enterprise that fixes a security vulnerability in Corda Enterprise Edition 4.5.3.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

In this patch release:

* Corda dependency vulnerability CVE-2020-28052 has been fixed.
* A fix has been introduced to reduce memory consumption during batched transaction resolution of large backchains.

## Corda Enterprise Edition 4.5.4 release notes

Corda Enterprise Edition 4.5.4 is a patch release of Corda Enterprise that fixes a security vulnerability in Corda Enterprise Edition 4.5.3.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../..//en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../..//en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

A security issue has been fixed that affects notary systems that use the JPA notary implementation in an HA configuration, and when the notary backing database has been set up using the Corda database management tool. The new version of the Corda database management tool must be re-run for the fix to take effect.

## Corda Enterprise Edition 4.5.3 release notes

Corda Enterprise Edition 4.5.3 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise Edition 4.5.2.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../..//en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).
As a node operator, you should upgrade to the [latest released version of Corda](../../../../..//en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.


### Fixed issues

* We have fixed several issues that caused memory leaks. As a result, we have added two new node configuration fields - `attachmentClassLoaderCacheSize` and `enableURLConnectionCache`. See the [node configuration fields page](../../../../../en/platform/corda/4.5/enterprise/node/setup/corda-configuration-fields.html#enterpriseconfiguration) for details.
* We have fixed an issue where the HA utilities tool does not write the correct log file.
* We have fixed an issue that prevented the HA utilities tool loading third-party HSM `.jar` files from the `drivers` directory when the `generate-internal-tunnel-ssl-keystores` command is run.
* Corda Enterprise Edition 4.5.3 now supports version 3.2.1 of the AWS CloudHSM client library.
* We have fixed an issue that could cause flow execution to hang.
* The `attachmentPresenceCache` has been removed. The functionality is duplicated in the `attachmentContent` cache in the `NodeAttachmentService`.
* We have fixed an issue that caused the Corda Firewall to throw an error when version information was requested.
* We have fixed an issue that can cause failure at node startup.
* We have fixed an issue that caused Jmeter to be unable to deserialize CorDapps if they were not listed as Jmeter dependencies.
* We have fixed an issue that caused the float to not reactivate after a bridge restart.
* We have fixed an issue that could cause a float to handle two connection attempts from the same bridge simultaneously.
* We have fixed an issue that misinterpreted an internal error as a bad certificate error, preventing future connection attempts.

## Corda Enterprise Edition 4.5.2 release notes

Corda Enterprise Edition 4.5.2 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise Edition 4.5.1.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../..//en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../..//en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by Corda Enterprise Network Manager (CENM) was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in [CENM 1.2](../../../../../en/platform/corda/1.2/cenm.html)) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [CENM PKI Tool](../../../../../en/platform/corda/1.2/cenm/pki-tool.md) now generates certificates with serial number sizes of up to 16 octets/bytes. This fix provides better support for Node and HA tools.
* We have fixed an issue where the Corda node would not start up (when not in `dev` mode) if a Network Map Service instance was not running.
* We have fixed an issue where the [Health Survey Tool](../../../../../en/platform/corda/4.5/enterprise/health-survey.md) would hang after performing all its checks if at the same time the external Artemis server was stopped during the "Received ECHO from bridge" step.
* We have fixed an issue where [Health Survey Tool](../../../../../en/platform/corda/4.5/enterprise/health-survey.md) would stall on node RPC invocation check when the node was started while the [CENM Network Map Service](../../../../../en/platform/corda/1.2/cenm/network-map.html) was down.
* We have fixed an issue where some existing customer CorDapps that were working on Corda Enterprise Edition 4.3 could not be registered successfully when Corda Enterprise was upgraded to version 4.5.

## Corda Enterprise Edition 4.5.1 release notes

Corda Enterprise Edition 4.5.1 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise Edition 4.5.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* Fixed an issue where the Classloader failed to find a Command class when Optional generic was used on Type definition.
* The [Configuraton Obfuscator tool](../../../../../en/platform/corda/4.5/enterprise/tools-config-obfuscator.md) has been fixed to work for HSM configuration files.
* Fixed an issue where retrying session inits could fail due to database connectivity.
* The H2 version has been reverted to 1.4.197 to avoid a dependency issue introduced after the previous upgrade.
* The CPU usage of the `NodeMeteringBackground` process has been decreased.
* A security update to prevent AMQP header spoofing has been applied.
* Fixed an issue where passing two sessions with the same counterparty to the `CollectSignaturesFlow` led to both counterparties' flows having to wait infinitely for messages from the other party.
* A previously unhandled exception in `FlowStateMachineImpl.run().initialiseFlow()` is now handled correctly.
* Fixed an issue where Corda Firewall did not start if its main configuration and its HSM configuration were obfuscated.
* Fixed an issue where a TLS handshake timeout led to blacklisting endpoint.
* Added support to the spent state audit command for specifying state references in the form `txId(outputIdx)` in addition to the existing `txId:outputIdx`.

## Corda Enterprise Edition 4.5 release notes

This release extends the [Corda Enterprise Edition 4.4 release](../../../../../en/platform/corda/4.4/enterprise/release-notes-enterprise.md) with further performance, resilience, and operational improvements.

Corda Enterprise Edition 4.5 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. See the Corda Enterprise [platform support matrix](../../../../../en/platform/corda/4.5/enterprise/platform-support-matrix.md) for more information.

Corda Enterprise Edition 4.5 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise Edition 4.4, 4.3, 4.2, 4.1, 4.0, and 3.x. See the [Corda (open source) release notes](/en/archived-docs/corda-os/4.5/release-notes.md) for more information.

## New features and enhancements

### Performance improvements

As part of Corda Enterprise Edition 4.5 we have introduced significant performance enhancements. Our main focus was to improve latency across multiple areas of the platform.

We have reduced the latency of `FinalityFlow` and `CollectSignaturesFlow`. This was achieved by parallelising various areas of the platform, such as backchain resolution, collection of signatures, and broadcast of finalised transaction to peers. Note that no CorDapp changes are required to benefit from these changes.

We have introduced [new flow framework APIs](../../../../../en/platform/corda/4.5/enterprise/cordapps/api-flows.html#communication-between-parties) (`sendAll`/`sendAllMap`), which can be used to send messages to multiple counterparties with improved performance. Previously, a flow was able to send messages to multiple counterparties by using the [send API](../../../../../en/platform/corda/4.5/enterprise/cordapps/api-flows.html#send) once for each counterparty. These new APIs can now be used to achieve the same with better performance, which comes from a smaller number of suspensions and checkpoints.

{{< note >}}
Existing CorDapps will have to be updated to benefit from the new API.
{{< /note >}}

We have introduced compression of messages exchanged between nodes during flows which can improve performance in terms of both latency and throughput. The performance improvement gained depends upon environmental factors, such as network configuration or hardware specification. This option is enabled by default but can be disabled if desired via the `enableP2PCompression` [node configuration option](../../../../../en/platform/corda/4.5/enterprise/node/setup/corda-configuration-fields.html#enablep2pcompression).


### Corda Enterprise images on DockerHub

Official Corda Enterprise Docker images are now available directly on [DockerHub](https://hub.docker.com/u/corda).

Furthermore, we have updated our `Dockerform` [local development task](../../../../../en/platform/corda/4.5/enterprise/node/deploy/generating-a-node.md) to make use of the new Docker images and to default to using PostgreSQL as the chosen node database.

{{< note >}}
To run the Corda Enterprise images, the Corda Enterprise evaluation must be programmatically accepted via a dedicated environment variable. See the [official Corda Docker image](../../../../../en/platform/corda/4.5/enterprise/docker-image.md) documentation section for more information.
{{< /note >}}

### Further Hardware Security Module (HSM) support

Corda Enterprise Edition 4.5 introduces the ability to use AWS CloudHSM to secure the cryptographic keys used by a node. Legal identity, TLS Firewall and Confidential Identity keys can now all be stored in an AWS HSM.

See the [platform support matrix](../../../../../en/platform/corda/4.5/enterprise/platform-support-matrix.md) documentation section for more information.

### Collaborative Recovery CorDapps for disaster recovery

Corda Enterprise Edition 4.5 introduces a new suite of utility CorDapps that can help you safely, and privately reconcile and recover ledger data lost in a disaster scenario.

The `LedgerSync` CorDapp can be used to routinely check the ledger for data inconsistencies between nodes, without compromising security. In the rare event that an inconsistency is discovered, the CorDapp `LedgerRecover` can be deployed in either Automatic recovery or Manual recovery mode (for more serious data loss) to securely recover the missing data from nodes across the network.

See the [Collaborative Recovery](../../../../../en/platform/corda/4.5/enterprise/node/collaborative-recovery/introduction-cr.md) documentation section for more information.

#### The `LedgerSync` CorDapp as a stand alone tool

The `LedgerSync` CorDapp is part of the Collaborative Recovery CorDapps, however it can be run as a standalone tool as well.

It safely and privately highlights the differences between the common ledger data held by two nodes in the same Business Network.
A peer running the CorDapp can be alerted to missing transactions. This procedure is called **Reconciliation**.

The CorDapp is designed to diagnose ledger inconsistencies caused by either of the following two events:
* A disaster affecting a node’s relational datastore.
* More rarely, a hardware or connectivity fault.

`LedgerSync` can be run either on demand or on a regular basis. The app contacts all peers of the initiating node that are on the same business network, and produces a report detailing all transactions relevant to both the node and the target peers, held in the initiating node’s ledger (transactions are considered relevant to a node if it was involved as either state participant or owner). If `LedgerSync` finds that the initiating tool is missing any relevant transaction, it flags the discrepancy to the operator, who can then proceed to recover the missing data.

`LedgerSync` is designed to be compliant with the Corda privacy model. It does not share any transaction information with network peers that shouldn’t already have access to it.

See the `LedgerSync` [documentation section](../../../../../en/platform/corda/4.5/enterprise/node/collaborative-recovery/ledger-sync.md) for more information.

### HA Notary readback queue

Each Notary worker now has a readback queue. This queue collects recently-spent states, then double-checks that they have correctly been recorded as spent in the Notary database. If this mechanism detects an inconsistency, an error is recorded in the worker’s log file, and a JMX metric for un-persisted DB records is updated.

See the [database monitoring agent](../../../../../en/platform/corda/4.5/enterprise/notary/notary-monitoring.md) documentation section for more information.

### Notary double-spend tool

A double-spend occurs when a state that the notary has marked as spent is used as input to a new transaction. Notaries will reject transactions that attempt double-spends.

Corda Enterprise Edition 4.5 introduces the `Spent State Audit Tool` - a new command-line tool that enables notary operators to obtain a list of transactions that attempted to double-spend a state. The information provided by the tool can be used to undertake root cause analysis on a double-spend attempt that has occurred on the network.

Please consult the `Spent State Audit Tool` [documentation](../../../../../en/platform/corda/4.5/enterprise/notary/spent-state.md) section for more information.

{{< note >}}
A change in the notary database schema is required to run the tool - see the [documentation](../../../../../en/platform/corda/4.5/enterprise/notary/spent-state.md) for details.
{{< /note >}}

#### Metering improvements

The [Metering Collector CorDapps](../../../../../en/platform/corda/4.5/enterprise/metering-collector.md) have been extended to request a summary of Corda Enterprise usage from one or more other participants on the network via the flow framework. This feature is designed to support Business Network Operators (BNOs) and comes with strong built-in privacy controls to ensure that each user has to opt in to sharing their information.

### RPC auditing

Corda Enterprise nodes now maintain an audit trail of RPC usage. Whenever a user attempts to perform an RPC call, the information will be recorded by the node in an off-ledger database table. The information can be downloaded locally in CSV or JSON format by an authorised user via a dedicated RPC operation.

See the [RPC Audit Collection Tool](../../../../../en/platform/corda/4.5/enterprise/rpc-audit-collector.md) documentation section for more information.

### Monitoring

Our documentation on monitoring has been revamped and now includes [improved guidance](../../../../../en/platform/corda/4.5/enterprise/node/operating/node-administration.html#monitoring-your-node) for node operators.

Furthermore, Corda Enterprise nodes expose additional metrics. The list of all metrics exposed by the node is available [here](../../../../../en/platform/corda/4.5/enterprise/node-metrics.md).

We have also provided a list of [common node monitoring scenarios](../../../../../en/platform/corda/4.5/enterprise/node/operating/monitoring-scenarios.md).

### Corda Enterprise Configuration Obfuscator

We have unified the [configuration obfuscation](../../../../../en/platform/corda/4.5/enterprise/tools-config-obfuscator.md) tools for Corda Enterprise and the Corda Enterprise Network Manager under a single `.jar` file. The new tool provides the same level of functionality of its predecessors.

#### Security updates

The following libraries have been updated:

* `netty` updated to [4.1.46.Final](https://github.com/netty/netty/releases/tag/netty-4.1.46.Final)
* `tcnative` updated to [2.0.29.Final](https://github.com/netty/netty-tcnative/releases/tag/netty-tcnative-parent-2.0.29.Final)

### Improved Tokens SDK along with new documentation and training

The Tokens SDK has been extended to provide a consistent API for use in both Java and Kotlin.

The documentation has been relocated to the main Corda and Corda Enterprise documentation site, and a comprehensive training module for developers added to the Corda training site.
[Read the documentation](../../../../../en/platform/corda/4.5/enterprise/cordapps/token-sdk-introduction.md).
[Explore the training module](https://training.corda.net/libraries/tokens-sdk/).

### Other improvements

* All database columns containing datestamps have been standardised to use UTC (the time zone used was previously inconsistent).
* The HSM name used in the HA Utilities `--bridge-hsm-name` and `--float-hsm-name` command-line parameters should now exactly match `cryptoServiceName`, as described [here](../../../../../en/platform/corda/4.5/enterprise/node/operating/cryptoservice-configuration.md).

## Platform version change

The platform version of Corda Enterprise Edition 4.5 has been bumped up from 6 to 7 due to the addition of the new flow framework APIs `sendAll` and `sendAllMap`, which can be used to send messages to multiple counterparties with improved performance.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## Fixed issues

* Fixed an issue where the implementation of `FieldInfo.notEqual` in `QueryCriteriaUtils` was the same as `FieldInfo.Equal`.
* We have fixed an issue where CorDapp custom serializers were not supported in `MockNetwork`, causing unit tests of flows to fail without using `Driver`.
* We have fixed an issue where serializing a `FlowExternalOperation`, which had maintained a reference to a `FlowLogic`, could throw an `IndexOutOfBoundsException` error when constructing a `FlowAsyncOperation` from a `FlowExternalOperation`.
* We have fixed an issue where `ServiceHub.signInitialTransaction()` threw undeclared checked exceptions (`TransactionDeserialisationException` and `MissingAttachmentsException`.
* We have standardised all node database timestamps to use the UTC time zone.
* We have fixed issues with the existing checkpoint iterator serializers related to null handling and the use of `equals` when restoring the iterator position.
* We have fixed an issue where Corda failed to deserialize Enums with custom `toString()` methods into the DJVM sandbox.
* We have fixed an issue where Corda's internal `providerMap` field in `core`, which is supposed to be private, was both public and mutable.
* We have fixed an issue with failing session init messages when the state machine replayed them from the Artemis queue in order to retry flows that had not yet persisted their first checkpoint, due to problems with database connectivity.
* We have fixed an issue where the `com.r3.corda.enterprise.settlementperftestcordapp.flows.SwapStockForCashFlowTest` failed for Oracle 11 due to failed migration.
* We have fixed an issue where `Level.WARN` and `Level.FATAL` logs did not include the original log message after updating them to extract more information from the stack traces.
* We have fixed an issue where a race condition would occur when a flow hung while waiting for the ledger to commit a transaction with hash even when that transaction was present in the database.
* We have fixed an issue where no CRL check was done when using embedded Artemis, which could cause nodes to continue to be involved in transactions after they had been blacklisted.
* We have fixed an issue with inconsistent error messages on starting components if HSM was not available.
* We have fixed an issue where a Vault Query using `LinearStateQueryCriteria(linearId = emptyList())` would translate into an illegal SQL statement on PostgreSQL and would throw an exception.
* We have added a custom serializer (`IteratorSerializer`) that can fix broken iterators in order to resolve an issue with a `ConcurrentModificationException` in `FetchDataFlow`.
* We have fixed an issue with failing `VaultObserverExceptionTest` tests on Oracle.
* We have fixed an issue where the “Registering as a new participant with a Corda network” message during node registration using the node shell was not centred.
* We have fixed an issue with licensing for the Collaborative Recovery CorDapps.
* We have removed stack trace for `level.INFO` and `level.WARN` logs while running `LedgerRecover` with `LedgerSync`.
* We have fixed an issue where an unhandled exception was thrown when a user attempted to start the `InitiateManualRecoveryFlow` flow from the node when the recovery had already been initialised.
* We have fixed an issue where an unhandled exception was thrown when `isRequester` had a wrong value while running `LedgerRecover`.
* We have fixed an issue where Corda Enterprise did not provide information about the flow when a non-started manual `LedgerRecover` was requested by the node.
* We have ensured that the documentation about `LedgerRecover` clearly explains that `TimeStamps` for recovered transactions are changed compared to the original transactions.
* We have fixed an issue where the `ExportTransactionsFlow` flow could get stuck while `LedgerRecover` was running.
* We have fixed an issue where manual `LedgerRecover` did not work for PostgreSQL 10.
* We have added a primary key to the `NODE_PROPERTIES` table in order to prevent duplicate inserts.
* We have fixed an issue where the Corda Firewall load was stuck when the connection between the Firewall Load Testing tool and Corda Firewall was disrupted.
* We have fixed a production environment issue occurring where notaries became unresponsive after a Java upgrade to Zulu 8.46.0.19.
* We have fixed an issue where the Corda Health Survey tool ignored HTTP 301 and 404 response codes when resolving network information.
* We have fixed an issue where the Corda Health Survey tool did not perform HTTP / HTTPS network map redirections.
* We have fixed an issue with a flaky test where `net.corda.coretests.transactions.AttachmentsClassLoaderTests.attachment` was still available in verify after forced garbage collection.
* We have moved the `backchainFetchBatchSize` option, used for bulk backchain resolution, into the correct Corda Enterprise-specific tuning section of the [Node configuration](node/setup/corda-configuration-file.md) (this section contains options that should be changed only in consultation with R3).
* We have fixed an issue where sensitive information was exposed as plain text in logs and the shell terminal when using the [Database Management Tool](../../../../../en/platform/corda/4.5/enterprise/database-management-tool.md).
