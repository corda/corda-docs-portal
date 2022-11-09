---
title: Corda Enterprise Edition 4.4 release notes
aliases:
- /releases/4.4/release-notes-enterprise.html
- /docs/corda-enterprise/head/release-notes-enterprise.html
- /docs/corda-enterprise/release-notes-enterprise.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-release-notes
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.4 release notes

Corda 4.4 lays the foundation of a new open-core approach for the Corda codebase. This involved a refactoring of the main functional components of Corda. Please consult cordapp-overview.rst to get an overview of the practical impact on CorDapp development.

Furthermore, Corda 4.4 introduces improvements to the flow framework API, a new diagnostic `ServiceHub` call and includes a number of security enhancements.


## Corda Enterprise Edition 4.4.12 release notes

Corda Enterprise Edition 4.4.12 is a patch release of Corda Enterprise focused on security improvements.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.9/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.9/enterprise/upgrading-index.md).

### Fixed issues

In this patch release:
* Java serialization has been disabled in the Corda firewall, closing a potential security vulnerability.

### Third party component upgrades

{{< table >}}

|Library|Version 4.4.12|Previous version|
|---------|-------|-------|
|Bean Utils|1.9.4|1.9.3|
|Bouncy Castle|1.68|1.66|
|Hibernate|5.4.32.Final|5.4.3.Final|
|Netty|4.1.77.Final|4.1.29.Final|
|Quasar|0.7.15_r3|0.7.13_r3|
|Shiro|1.8.0|1.4.1|
|TCNative|2.0.48.Final|2.0.14.Final|

{{< /table >}}


## Corda Enterprise Edition 4.4.11 release notes

Corda Enterprise Edition 4.4.11 is a patch release of Corda Enterprise that fixes an urgent security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. The latest Corda Enterprise release notes are on this page, and you can find the latest upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/upgrading-index.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html).

### Fixed issues

In this patch release:

Log4j dependency updated to version 2.17.1 to fix pre-existing Log4j issues.

## Corda Enterprise Edition 4.4.10 release notes

{{< note >}}
This is a direct upgrade from 4.4.8. No version 4.4.9 was released.
{{< /note >}}

Corda Enterprise Edition 4.4.10 is a patch release of Corda Enterprise that fixes an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version 2.16.0.

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


## Corda Enterprise Edition 4.4.8 release notes

Corda Enterprise Edition 4.4.8 is a patch release of Corda Enterprise that fixes an invalid notarization response being sent
after an internal notary flow retry.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* A fix has been added to prevent a rare invalid notarization response after internal notary flow retry.

## Corda Enterprise Edition 4.4.7 release notes

Corda Enterprise Edition 4.4.7 is a patch release of Corda Enterprise that fixes a memory issue in Corda Enterprise Edition 4.4.6.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issue listed below is relevant to your work.

### Fixed issue

* We have fixed an issue that caused unbounded memory consumption for batched transaction resolution.

## Corda Enterprise Edition 4.4.6 release notes

Corda Enterprise Edition 4.4.6 is a patch release of Corda Enterprise that fixes a security vulnerability in Corda Enterprise Edition 4.4.5.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

A security issue has been fixed that affects notary systems that use the JPA notary implementation in an HA configuration, and when the notary backing database has been set up using the Corda database management tool. The new version of the Corda database management tool must be re-run for the fix to take effect.


## Corda Enterprise Edition 4.4.5 release notes

Corda Enterprise Edition 4.4.5 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise Edition 4.4.4.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* The `attachmentPresenceCache` has been removed. The functionality is duplicated in the `attachmentContent` cache in the `NodeAttachmentService`.
* We have fixed an issue that caused the Corda Firewall to throw an error when version information was requested.
* We have fixed an issue that caused the float to not reactivate after a bridge restart.
* We have fixed an issue that could cause a float to handle two connection attempts from the same bridge simultaneously.
* We have fixed an issue that misinterpreted an internal error as a bad certificate error, preventing future connection attempts.
* We have fixed an issue that can cause failure at node startup.
* We have fixed several issues that caused memory leaks. As a result, we have added two new node configuration fields - `attachmentClassLoaderCacheSize` and `enableURLConnectionCache`. See the [node configuration fields page](../../../../../en/platform/corda/4.4/enterprise/node/setup/corda-configuration-file.md) for details.

## Corda Enterprise Edition 4.4.4 release notes

Corda Enterprise Edition 4.4.4 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise Edition 4.4.3.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by Corda Enterprise Network Manager (CENM) was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in [CENM 1.2](../../../../../en/platform/corda/1.2/cenm.html)) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [CENM PKI Tool](../../../../../en/platform/corda/1.2/cenm/pki-tool.md) now generates certificates with serial number sizes of up to 16 octets/bytes. This fix provides better support for Node and HA tools.
* We have fixed an issue where the Corda node would not start up (when not in `dev` mode) if a Network Map Service instance was not running.

## Corda Enterprise Edition 4.4.3 release notes

Corda Enterprise Edition 4.4.3 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise Edition 4.4.2.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* Session rollbacks are now allowed inside an entity manager.
* Sensitive information is no longer exposed as clear text on logs and terminal when using the [Database Management Tool](database-management-tool.md).
* Fixed an issue where the Classloader failed to find a Command class when Optional generic was used on Type definition.
* The [Configuraton Obfuscator tool](../../../../../en/platform/corda/4.4/enterprise/tools-config-obfuscator.md) has been fixed to work for HSM configuration files.
* The H2 version has been reverted to 1.4.197 to avoid a dependency issue introduced after the previous upgrade.
* A security update to prevent AMQP header spoofing has been applied.
* A previously unhandled exception in `FlowStateMachineImpl.run().initialiseFlow()` is now handled correctly.
* The CPU usage of the `NodeMeteringBackground` process has been decreased.
* The `backchainFetchBatchSize` option has been moved to the tuning section of the node configuration file.
* Fixed an error in DNS name resolution when using the [Corda Health Survey tool](../../../../../en/platform/corda/4.4/enterprise/health-survey.md).
* Fixed an issue where Corda Firewall did not start if its main configuration and its HSM configuration were obfuscated.
* Fixed an issue where deobfuscation options were missing from [HA Utilities](../../../../../en/platform/corda/4.4/enterprise/ha-utilities.md) in `generate-internal-tunnel-ssl-keystores` mode.
* Some Corda Enterprise Edition 4.5 features have been backported to allow Azure Kubernetes Service deployment in Corda Enterprise Edition 4.4.3.
* Fixed `vaultService.updates.subscribe` errors when running inside `STATE_MACHINE_STARTED` event handler.
* In the `graphiteOptions` section of `node.conf`, `sampleInvervallSeconds` has been changed to `sampleIntervalSeconds`.


## Corda Enterprise Edition 4.4.2 release notes

Corda Enterprise Edition 4.4.2 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise Edition 4.4 and a fix to a new issue related to a recent third-party dependency update.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

As a node operator, you should upgrade to the [latest released version of Corda](../../../../../en/platform/corda/4.8/enterprise.html) if any of the fixed issues listed below is relevant to your work.

### Fixed issues

* A recent JDK update has broken the way we used delegated signatures for TLS (Transport Layer Security) handshakes. We have fixed this issue through patches on all affected Corda Enterprise versions (4.2+) to allow users to upgrade to the latest versions of compatible JDK distributions. If you have not upgraded to one of the patched releases yet, do not upgrade to Java 8 version `8u252` or higher.
* Fixed an issue to prevent `IndexOutOfBoundsException` from being thrown when serialising a `FlowAsyncOperation` that has maintained a reference to a `FlowLogic`. This issue occurred when constructing a `FlowAsyncOperation` from a `FlowExternalOperation` [[CORDA-3704](https://r3-cev.atlassian.net/browse/CORDA-3704)].
* Removed references to unavailable `man` command in CRaSH and fixed syntax of `output-format` command [[CORDA-3688](https://r3-cev.atlassian.net/browse/CORDA-3688)].
* Resolved a race condition in `FlowLogic.waitForLedgerCommit`.
* Addressed the following problems with the JPA notary:
    * Prevent database connection leak on unexpected DB exceptions.
    * Prevent incorrect handling of scenarios where a successful transaction containing an input state and an unspent reference state is retried.
* "In-process" Driver nodes used in testing now support custom CorDapp serialisers.

## Corda Enterprise Edition 4.4

This release extends the [Corda Enterprise Edition 4.3 release](../../../../../en/platform/corda/4.3/enterprise/release-notes-enterprise.md)
with further performance, resilience and operational improvements.

Corda Enterprise Edition 4.4 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. Please refer to product documentation for details.

Corda Enterprise Edition 4.4 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise Edition 4.3, 4.2, 4.1, 4.0 and 3.x, while providing enterprise-grade features and performance.

### Key new features and components

#### Corda Open Core

Starting with Corda Enterprise Edition 4.4, Corda Enterprise and Open Source share the same core and API libraries - the Enterprise version
now has a binary dependency on the matching Open Source release. This reduces maintenance overhead, and improves API compatibility
and interoperability between the Open Source and Enterprise versions.

This change has some implications on the upgrade process (see “Upgrade Notes” section later on).

#### Further Hardware Security Module (HSM) support

This release adds support for storing the node’s CA and legal identity key in a [nCipher nShield Connect](https://www.ncipher.com/products/general-purpose-hsms/nshield-connect) HSM.
Please refer to the associated section in [Using an HSM with Corda Enterprise](../../../../../en/platform/corda/4.4/enterprise/node/operating/cryptoservice-configuration.md) for more details.

We also have extended the set of HSMs available for the storage of a highly-available notary’s shared service key. The notary’s shared service key can now be stored in the following HSM types:

* Utimaco
* Gemalto Luna
* nCipher

#### Performance improvements

This release introduces an optimisation for sharing transaction backchains. Corda Enterprise nodes can request backchain items in bulk instead of one at a time (the configuration property `backchainFetchBatchSize` can be used to define the size of the batch).

Responding nodes (Enterprise or Open Source) running at platform version >= 6 will supply backchain items in bulk up to half of the network’s allowed maximum message size (minimum one item; items exceeding the limit are sent in subsequent batches). Nodes running on older platform version will still supply backchain items one at a time.

The release also includes the ability to configure the timeout and buffer size that ActiveMQ Artemis uses to flush produced messages to disk and send acknowledgements back to the client. This is exposed via a set of additional node configuration properties (`journalBufferTimeout`, `journalBufferSize` and `brokerConnectionTtlCheckIntervalMs`). Optimizing these values for your particular use case may result in improved latency depending on the characteristics of the hardware infrastructure.

#### HA Notary registration process improvements

We have introduced a set of improvements to make it easier to register a highly-available notary onto a Corda network:

* The keystore containing the notary identity key that is generated during registration is given a name that clearly disambiguates it from a regular node keystore
* The notary can now be registered using its X500 name, as an alternative to providing a node info file. This allows the notary to be added to the network parameters before the notary is registered, and avoids the need to copy the node info file around between notary workers
* HA notary workers can retrieve the notary’s service certificate from the network map service, avoiding the need to manually copy it around between the various workers
* HA notary workers check they have access to the shared notary service key and certificate before they register with the notary
#
### Corda Health Survey improvements

We have improved the Corda Health Survey tool to support a fuller range of node commissioning tasks, including:

* Verifying connectivity with other peers and Notaries
* Validating more complex deployments of Corda Enterprise (including HA node-Firewall combinations)
* Further connectivity checks on network infrastructure (check CRL endpoint via the Bridge)
* Further validation of node functionality (RPC connectivity)
* Warning operators that the node or Firewall configuration files are not obfuscated

Furthermore, we have improved the overall usability of the tool by adding support for running the tool via RPC.

The new version of the tool can only be used on Corda Enterprise Edition 4.4 (and above) nodes. Peer connectivity checks can target any node or Notary running on the same network.

#### Configuration Obfuscator improvements

The Configuration Obfuscator has been improved to:

* Use a more robust key derivation function (PBKDF2 with HMAC-SHA256)

    * keyboard input (stdin)
    * Command-line
    * Environment variables

The new version of the tool is also able to de-obfuscate files obfuscated with older versions.

The new version of the tool can only be used with Corda Enterprise Edition 4.4 (and above) node and Firewall configuration files.

### Changes for developers in Corda 4.4

#### Flows API improvements

Corda 4.4 introduces a new `FlowLogic.await` API that allows a CorDapp developer to suspend their flow when executing user-defined long-running operations (e.g. call-outs to external services). This prevents these long-running operations from blocking the flow thread, allowing other flows to progress in the interim. Previously, these operations had to be executed synchronously, blocking the flow thread.

The CorDapp developer can decide whether to run these asynchronous flow operations in a dedicated thread pool, or to handle the threading themselves directly.

Note that as before, the flow framework suspends automatically for certain operations (e.g. when waiting to receive a message from a counterparty). These suspensions do not have to be triggered explicitly.

The node operator can configure the number of threads in the threadpool to dedicate to external operations.

Corda 4.4 also introduces a new `HospitalizeFlowException` exception type that, when thrown, causes a flow to halt execution and send itself to the flow hospital for observation. The flow will automatically be retried on the next node start.

This exception gives user code a way to retry a flow from its last checkpoint if a known intermittent failure occurred.

#### New utility APIs

Corda 4.4 introduces a new call (`ServiceHub.DiagnosticsService`) available to CorDapp developers that allows them to access:

* The edition of Corda being run (e.g. Open Source, Enterprise)
* The version of Corda being run including the patch number (eg. 3.2.20190215)

Corda 4.4 also provides a callback (`AppServiceHub.register`) to allow Corda services to register custom actions to be performed once the node is fully started-up. This pattern prevents issues caused by the service trying to immediately access a part of the node that hadn’t yet been initialised .

#### Security enhancements

* The SSH server in the [Embedded Shell](shell.md) has been updated to remove outdated weak ciphers and algorithms.
* The ability to SSH into the standalone shell has been removed
* A new read-only RPC user role template has been documented in [Embedded Shell](shell.md)

#### Changes to integration testing

The “out-of-process” nodes spawned through Driver DSL (see tutorial-integration-testing) will no longer accidentally contain your CorDapps on their application classpath. The list of items that will be automatically filtered out include:

* Directories (only regular files are allowed)
* Jars with Maven classifiers `tests` or `test`
* Jars with any Cordapp attributes in their manifests (any of those listed in cordapp-build-systems or `Target-Platform-Version` and `Min-Platform-Version` if both are present)
* Jars with the `Corda-Testing` attribute in their manifests. The manifest of the following artifacts has been updated to include the `Corda-Testing` attribute:

    * `corda-node-driver`
    * `corda-test-utils`
    * `corda-test-common`
    * `corda-test-db`
    * `corda-mock`

* Files whose names start with `corda-mock`, `junit`, `testng` or `mockito`

Some of your existing integration tests might implicitly be relying on the presence of the above files, so please keep this in mind when upgrading your version of Corda.

### Platform version change

Given the addition of new APIs, the platform version of Corda 4.4 has been bumped up from 5 to 6. This is to prevent CorDapps that use it being deployed onto nodes unable to host them. Note that the minimum platform version has not been changed - this means that older Corda nodes can still interoperate with Corda 4.4 nodes. Since the APIs added do not affect the wire protocol or have other zone-level implications, applications can take advantage of these new platform version 6 features even if the Corda 4.4 node is running on a network whose minimum platform version is 4.

For more information on platform version, please see [Versioning](../../../../../en/platform/corda/4.4/open-source/versioning.md).

For more details on upgrading a CorDapp to use platform version 5, please see [Upgrading CorDapps to newer Platform Versions](../../../../../en/platform/corda/4.4/open-source/app-upgrade-notes.md).

### Fixed issues

* A failure response from Doorman during initial registration causes a class cast exception [[CORDA-2744](https://r3-cev.atlassian.net/browse/CORDA-2744)]
* Add an exception for Unrecoverable RPC errors [[CORDA-3192](https://r3-cev.atlassian.net/browse/CORDA-3192)]
* Fix the misleading Flow has been waiting message [[CORDA-3197](https://r3-cev.atlassian.net/browse/CORDA-3197)]
* Update Quasar agent so that we can exclude entire ClassLoaders from being instrumented [[CORDA-3228](https://r3-cev.atlassian.net/browse/CORDA-3228)]
* Don’t fail on liquibase errors when using H2 [[CORDA-3302](https://r3-cev.atlassian.net/browse/CORDA-3302)]
* Exceptions thrown in raw vault observers can cause critical issues [[CORDA-3329](https://r3-cev.atlassian.net/browse/CORDA-3329)]
* Migration from Corda 3.x to 4.x for PostgreSQL require a manual workaround [[CORDA-3348](https://r3-cev.atlassian.net/browse/CORDA-3348)]
* Prepare DJVM library for 1.0 release [[CORDA-3377](https://r3-cev.atlassian.net/browse/CORDA-3377)]
* Improve node configuration override documentation [[CORDA-3386](https://r3-cev.atlassian.net/browse/CORDA-3386)]
* Allow EvolutionSerializer to handle primitive types becoming nullable [[CORDA-3390](https://r3-cev.atlassian.net/browse/CORDA-3390)]
* Fix caching of local AMQPSerializer [[CORDA-3392](https://r3-cev.atlassian.net/browse/CORDA-3392)]
* Fixed NPE in BlobInspector [[CORDA-3396](https://r3-cev.atlassian.net/browse/CORDA-3396)]
* Update DemoBench so that using the DJVM is configurable [[CORDA-3406](https://r3-cev.atlassian.net/browse/CORDA-3406)]
* Scanning for Custom Serializers in the context of transaction verification is broken [[CORDA-3464](https://r3-cev.atlassian.net/browse/CORDA-3464)]
* Allow EvolutionSerializer to handle boxed types becoming primitive [[CORDA-3469](https://r3-cev.atlassian.net/browse/CORDA-3469)]
* Create interface to perform transactional operations from custom CordaServices [[CORDA-3471](https://r3-cev.atlassian.net/browse/CORDA-3471)]
* Fix typo in node database table documentation [[CORDA-3476](https://r3-cev.atlassian.net/browse/CORDA-3476)]
* Fix node database page [[CORDA-3477](https://r3-cev.atlassian.net/browse/CORDA-3477)]
* Add timestamp column to NODE_TRANSACTIONS table [[CORDA-3479](https://r3-cev.atlassian.net/browse/CORDA-3479)]
* Support adding new mandatory field and removal of optional [[CORDA-3489](https://r3-cev.atlassian.net/browse/CORDA-3489)]
* Fix link to network builder [[CORDA-3495](https://r3-cev.atlassian.net/browse/CORDA-3495)]
* Provide option for user to specify custom serializers without classpath scanning [[CORDA-3501](https://r3-cev.atlassian.net/browse/CORDA-3501)]
* The CordaRPCClientConfiguration is not respected when GracefulReconnect is used [[CORDA-3507](https://r3-cev.atlassian.net/browse/CORDA-3507)]
* Fix for Could not start flow as connection failed error on starting flow via ShellCli if user is not authorized to use this flow [[CORDA-3513](https://r3-cev.atlassian.net/browse/CORDA-3513)]
* Support whitelists and custom serializers inside the DJVM [[CORDA-3523](https://r3-cev.atlassian.net/browse/CORDA-3523)]
* Load DJVM serialization types more precisely to avoid runtime warnings [[CORDA-3536](https://r3-cev.atlassian.net/browse/CORDA-3536)]
* Use the config values for reconnecting retry interval and max reconnect attempts [[CORDA-3542](https://r3-cev.atlassian.net/browse/CORDA-3542)]
* SSH memory leak and security [[CORDA-3520](https://r3-cev.atlassian.net/browse/CORDA-3520)]
* Remove support for outdated ciphers and algorithms from SSH [[CORDA-3550](https://r3-cev.atlassian.net/browse/CORDA-3550)]
* Deserialization using the DJVM creates too many SerializerFactory objects [[CORDA-3552](https://r3-cev.atlassian.net/browse/CORDA-3552)]
* Allow initial registration errors to propagate up so the node exits with a failure code [[CORDA-3558](https://r3-cev.atlassian.net/browse/CORDA-3558)]
* Remove reference to man run [[CORDA-3559](https://r3-cev.atlassian.net/browse/CORDA-3559)]
* Always add TestCordapps to the classpath when building _driverSerializationEnv [[CORDA-3566](https://r3-cev.atlassian.net/browse/CORDA-3566)]
* Use the connectionMaxRetryInterval configuration when reconnection the RPC client [[CORDA-3576](https://r3-cev.atlassian.net/browse/CORDA-3576)]
* Update docs for X500 name and SSH hostkey [[CORDA-3585](https://r3-cev.atlassian.net/browse/CORDA-3585)]
* hashLookup command help misspelling [[CORDA-3587](https://r3-cev.atlassian.net/browse/CORDA-3587)]
* Exit the InteractiveShell on shutdown command [[CORDA-3593](https://r3-cev.atlassian.net/browse/CORDA-3593)]

### Known issues

Changes introduced in Corda 4.4 to increase ledger integrity have highlighted limitations regarding database transactions. To prevent flows from continuing to process after a database transaction has failed to commit or suffered from a pre-commit persistence exception, extra database flushes have been added. These extra flushes can cause exceptions to be thrown where they were not before (or cause different exception types to be raised compared to Corda 4.3 or previous versions). In general, CorDapp developers should not expect to be able to catch exceptions thrown during a database transaction and then continue with further DB operations as part of the same flow. A safer pattern involves allowing the flow to fail and be retried

### Upgrade notes

From Corda Enterprise Edition 4.4 onwards, we are moving towards an open core strategy. Common APIs shared by Corda Enterprise will only be available in Corda Open Source. Therefore, any CorDapps written against Corda Enterprise Edition 4.4 or later will have to depend on the open source version of `corda-core`.

As per previous major releases, we have provided a [comprehensive upgrade guide](../../../../../en/platform/corda/4.4/enterprise/app-upgrade-notes-enterprise.md) to ease the upgrade of CorDapps to Corda Enterprise Edition 4.4.