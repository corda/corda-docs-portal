---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    identifier: "corda-enterprise-4-5-release-notes"
    name: "Release notes"
tags:
- release
- notes
- enterprise
title: Corda Enterprise release notes
weight: 1

---


# Corda Enterprise release notes

## Corda Enterprise 4.5.2

Corda Enterprise 4.5.2 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise 4.5.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](https://docs.corda.net/docs/corda-enterprise/release-notes-enterprise.html).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by Corda Enterprise Network Manager (CENM) was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in [CENM 1.2](https://docs.corda.net/docs/cenm/1.2.html)) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [CENM PKI Tool](https://docs.corda.net/docs/cenm/pki-tool.html) now generates certificates with serial number sizes of up to 16 octets/bytes. This fix provides better support for Node and HA tools.
* We have fixed an issue where the Corda node would not start up (when not in `dev` mode) if a Network Map Service instance was not running.
* We have fixed an issue where the [Health Survey Tool](health-survey.md) would hang after performing all its checks if at the same time the external Artemis server was stopped during the "Received ECHO from bridge" step.
* We have fixed an issue where [Health Survey Tool](health-survey.md) would stall on node RPC invocation check when the node was started while the [CENM Network Map Service](https://docs.corda.net/docs/cenm/network-map.html) was down.
* We have fixed an issue where some existing customer CorDapps that were working on Corda Enterprise 4.3 could not be registered successfully when Corda Enterprise was upgraded to version 4.5.

## Corda Enterprise 4.5.1

Corda Enterprise 4.5.1 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise 4.5.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](https://docs.corda.net/docs/corda-enterprise/release-notes-enterprise.html).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* Fixed an issue where the Classloader failed to find a Command class when Optional generic was used on Type definition.
* The [Configuraton Obfuscator tool](tools-config-obfuscator.md) has been fixed to work for HSM configuration files.
* Fixed an issue where retrying session inits could fail due to database connectivity.
* The H2 version has been reverted to 1.4.197 to avoid a dependency issue introduced after the previous upgrade.
* The CPU usage of the `NodeMeteringBackground` process has been decreased.
* A security update to prevent AMQP header spoofing has been applied.
* Fixed an issue where passing two sessions with the same counterparty to the `CollectSignaturesFlow` led to both counterparties' flows having to wait infinitely for messages from the other party.
* A previously unhandled exception in `FlowStateMachineImpl.run().initialiseFlow()` is now handled correctly.
* Fixed an issue where Corda Firewall did not start if its main configuration and its HSM configuration were obfuscated.
* Fixed an issue where a TLS handshake timeout led to blacklisting endpoint.
* Added support to the spent state audit command for specifying state references in the form `txId(outputIdx)` in addition to the existing `txId:outputIdx`.

## Corda Enterprise 4.5 release overview

This release extends the [Corda Enterprise 4.4 release](../4.4/release-notes-enterprise.md) with further performance, resilience, and operational improvements.

Corda Enterprise 4.5 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. See the Corda Enterprise [platform support matrix](platform-support-matrix.md) for more information.

Corda Enterprise 4.5 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.4, 4.3, 4.2, 4.1, 4.0, and 3.x. See the [Corda (open source) release notes](../../corda-os/4.5/release-notes.md) for more information.

## New features and enhancements

### Performance improvements

As part of Corda Enterprise 4.5 we have introduced significant performance enhancements. Our main focus was to improve latency across multiple areas of the platform.

We have reduced the latency of `FinalityFlow` and `CollectSignaturesFlow`. This was achieved by parallelising various areas of the platform, such as backchain resolution, collection of signatures, and broadcast of finalised transaction to peers. Note that no CorDapp changes are required to benefit from these changes.

We have introduced [new flow framework APIs](cordapps/api-flows.md#communication-between-parties) (`sendAll`/`sendAllMap`), which can be used to send messages to multiple counterparties with improved performance. Previously, a flow was able to send messages to multiple counterparties by using the [send API](cordapps/api-flows.md#send) once for each counterparty. These new APIs can now be used to achieve the same with better performance, which comes from a smaller number of suspensions and checkpoints.

{{< note >}}
Existing CorDapps will have to be updated to benefit from the new API.
{{< /note >}}

We have introduced compression of messages exchanged between nodes during flows which can improve performance in terms of both latency and throughput. The performance improvement gained depends upon environmental factors, such as network configuration or hardware specification. This option is enabled by default but can be disabled if desired via the `enableP2PCompression` [node configuration option](node/setup/corda-configuration-fields.md#enablep2pcompression).


### Corda Enterprise images on DockerHub

Official Corda Enterprise Docker images are now available directly on [DockerHub](https://hub.docker.com/u/corda).

Furthermore, we have updated our `Dockerform` [local development task](node/deploy/generating-a-node.md) to make use of the new Docker images and to default to using PostgreSQL as the chosen node database.

{{< note >}}
To run the Corda Enterprise images, the Corda Enterprise evaluation must be programmatically accepted via a dedicated environment variable. See the [official Corda Docker image](docker-image.md) documentation section for more information.
{{< /note >}}

### Further Hardware Security Module (HSM) support

Corda Enterprise 4.5 introduces the ability to use AWS CloudHSM to secure the cryptographic keys used by a node. Legal identity, TLS Firewall and Confidential Identity keys can now all be stored in an AWS HSM.

See the [platform support matrix](platform-support-matrix.md) documentation section for more information.

### Collaborative Recovery CorDapps for disaster recovery

Corda Enterprise 4.5 introduces a new suite of utility CorDapps that can help you safely, and privately reconcile and recover ledger data lost in a disaster scenario.

The `LedgerSync` CorDapp can be used to routinely check the ledger for data inconsistencies between nodes, without compromising security. In the rare event that an inconsistency is discovered, the CorDapp `LedgerRecover` can be deployed in either Automatic recovery or Manual recovery mode (for more serious data loss) to securely recover the missing data from nodes across the network.

See the [Collaborative Recovery](node/collaborative-recovery/introduction-cr.md) documentation section for more information.

#### The `LedgerSync` CorDapp as a stand alone tool

The `LedgerSync` CorDapp is part of the Collaborative Recovery CorDapps, however it can be run as a standalone tool as well.

It safely and privately highlights the differences between the common ledger data held by two nodes in the same Business Network.
A peer running the CorDapp can be alerted to missing transactions. This procedure is called **Reconciliation**.

The CorDapp is designed to diagnose ledger inconsistencies caused by either of the following two events:
* A disaster affecting a node’s relational datastore.
* More rarely, a hardware or connectivity fault.

`LedgerSync` can be run either on demand or on a regular basis. The app contacts all peers of the initiating node that are on the same business network, and produces a report detailing all transactions relevant to both the node and the target peers, held in the initiating node’s ledger (transactions are considered relevant to a node if it was involved as either state participant or owner). If `LedgerSync` finds that the initiating tool is missing any relevant transaction, it flags the discrepancy to the operator, who can then proceed to recover the missing data.

`LedgerSync` is designed to be compliant with the Corda privacy model. It does not share any transaction information with network peers that shouldn’t already have access to it.

See the `LedgerSync` [documentation section](node/collaborative-recovery/ledger-sync.md) for more information.

### HA Notary readback queue

Each Notary worker now has a readback queue. This queue collects recently-spent states, then double-checks that they have correctly been recorded as spent in the Notary database. If this mechanism detects an inconsistency, an error is recorded in the worker’s log file, and a JMX metric for unpersisted DB records is updated.

See the [database monitoring agent](notary/notary-monitoring.md) documentation section for more information.

### Notary double-spend tool

A double-spend occurs when a state that the notary has marked as spent is used as input to a new transaction. Notaries will reject transactions that attempt double-spends.

Corda Enterprise 4.5 introduces the `Spent State Audit Tool` - a new command-line tool that enables notary operators to obtain a list of transactions that attempted to double-spend a state. The information provided by the tool can be used to undertake root cause analysis on a double-spend attempt that has occurred on the network.

Please consult the `Spent State Audit Tool` [documentation](notary/spent-state.md) section for more information.

{{< note >}}
A change in the notary database schema is required to run the tool - see the [documentation](notary/spent-state.md) for details.
{{< /note >}}

#### Metering improvements

The [Metering Collector CorDapps](metering-collector.md) have been extended to request a summary of Corda Enterprise usage from one or more other participants on the network via the flow framework. This feature is designed to support Business Network Operators (BNOs) and comes with strong built-in privacy controls to ensure that each user has to opt in to sharing their information.

### RPC auditing

Corda Enterprise nodes now maintain an audit trail of RPC usage. Whenever a user attempts to perform an RPC call, the information will be recorded by the node in an off-ledger database table. The information can be downloaded locally in CSV or JSON format by an authorised user via a dedicated RPC operation.

See the [RPC Audit Collection Tool](rpc-audit-collector.md) documentation section for more information.

### Monitoring

Our documentation on monitoring has been revamped and now includes [improved guidance](node/operating/node-administration.md#monitoring-your-node) for node operators.

Furthermore, Corda Enterprise nodes expose additional metrics. The list of all metrics exposed by the node is available [here](node-metrics.md).

We have also provided a list of [common node monitoring scenarios](node/operating/monitoring-scenarios.md).

### Corda Enterprise Configuration Obfuscator

We have unified the [configuration obfuscation](tools-config-obfuscator.md) tools for Corda Enterprise and the Corda Enterprise Network Manager under a single `.jar` file. The new tool provides the same level of functionality of its predecessors.

#### Security updates

The following libraries have been updated:

* `netty` updated to [4.1.46.Final](https://github.com/netty/netty/releases/tag/netty-4.1.46.Final)
* `tcnative` updated to [2.0.29.Final](https://github.com/netty/netty-tcnative/releases/tag/netty-tcnative-parent-2.0.29.Final)

### Improved Tokens SDK along with new documentation and training

The Tokens SDK has been extended to provide a consistent API for use in both Java and Kotlin.

The documentation has been relocated to the main Corda and Corda Enterprise documentation site, and a comprehensive training module for developers added to the Corda training site.
[Read the documentation](cordapps/token-sdk-introduction.md).
[Explore the training module](https://training.corda.net/libraries/tokens-sdk/).

### Other improvements

* All database columns containing datestamps have been standardised to use UTC (the time zone used was previously inconsistent).
* The HSM name used in the HA Utilities `--bridge-hsm-name` and `--float-hsm-name` command-line parameters should now exactly match `cryptoServiceName`, as described [here](cryptoservice-configuration.md).

## Platform version change

The platform version of Corda Enterprise 4.5 has been bumped up from 6 to 7 due to the addition of the new flow framework APIs `sendAll` and `sendAllMap`, which can be used to send messages to multiple counterparties with improved performance.

For more information about platform versions, see [Versioning](../../corda-os/4.5/versioning.md).

## Fixed issues

* Fixed an issue where the implementation of `FieldInfo.notEqual` in `QueryCriteriaUtils` was the same as `FieldInfo.Equal`.
* We have fixed an issue where CorDapp custom serialisers were not supported in `MockNetwork`, causing unit tests of flows to fail without using `Driver`.
* We have fixed an issue where serialising a `FlowExternalOperation`, which had maintained a reference to a `FlowLogic`, could throw an `IndexOutOfBoundsException` error when constructing a `FlowAsyncOperation` from a `FlowExternalOperation`.
* We have fixed an issue where `ServiceHub.signInitialTransaction()` threw undeclared checked exceptions (`TransactionDeserialisationException` and `MissingAttachmentsException`.
* We have standardised all node database timestamps to use the UTC time zone.
* We have fixed issues with the existing checkpoint iterator serialisers related to null handling and the use of `equals` when restoring the iterator position.
* We have fixed an issue where Corda failed to deserialise Enums with custom `toString()` methods into the DJVM sandbox.
* We have fixed an issue where Corda's internal `providerMap` field in `core`, which is supposed to be private, was both public and mutable.
* We have fixed an issue with failing session init messages when the state machine replayed them from the Artemis queue in order to retry flows that had not yet persisted their first checkpoint, due to problems with database connectivity.
* We have fixed an issue where the `com.r3.corda.enterprise.settlementperftestcordapp.flows.SwapStockForCashFlowTest` failed for Oracle 11 due to failed migration.
* We have fixed an issue where `Level.WARN` and `Level.FATAL` logs did not include the original log message after updating them to extract more information from the stack traces.
* We have fixed an issue where a race condition would occur when a flow hung while waiting for the ledger to commit a transaction with hash even when that transaction was present in the database.
* We have fixed an issue where no CRL check was done when using embedded Artemis, which could cause nodes to continue to be involved in transactions after they had been blacklisted.
* We have fixed an issue with inconsistent error messages on starting components if HSM was not available.
* We have fixed an issue where a Vault Query using `LinearStateQueryCriteria(linearId = emptyList())` would translate into an illegal SQL statement on PostgreSQL and would throw an exception.
* We have added a custom serialiser (`IteratorSerializer`) that can fix broken iterators in order to resolve an issue with a `ConcurrentModificationException` in `FetchDataFlow`.
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
* We have fixed an issue where sensitive information was exposed as plain text in logs and the shell terminal when using the [Database Management Tool](database-management-tool.md).
