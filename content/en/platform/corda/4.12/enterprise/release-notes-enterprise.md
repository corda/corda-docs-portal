---
title: Corda Enterprise Edition 4.12 release notes
date: '2023-05-08'

menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-release-notes
    parent: about-corda-landing-4-12-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.12 release notes

## Corda Enterprise Edition 4.12.6 release notes

Corda Enterprise Edition 4.12.6 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation



### Fixed issues

### Third-party components upgrade

The following table lists the dependency version changes between 4.12.5 and 4.12.6 Enterprise Editions:



## Corda Enterprise Edition 4.12.5 release notes

Corda Enterprise Edition 4.12.5 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

{{< important >}}
When upgrading a node to Corda 4.12, it is extremely important that you run the Transaction Validator Utility on your node database to verify that the transactions in the old node are compatible with 4.12 nodes.

To ensure compatibility of the transactions, you must also run the Transaction Validator Utility on any older nodes that are not being upgraded and will likely interact with any upgraded nodes.

For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "upgrade-guide.md" >}}).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 or below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

### Fixed issues

* In Corda 4.11 and earlier, when the node verified contracts, they were all verified within the Corda node process. This meant that any custom command line attributes defined on the node process via the capsule would be visible to contract verification; for example, system properties. In Corda 4.12, the 4.12 contracts are still verified in the Corda node process, but legacy (that is, 4.11 and earlier) contracts are now verified in the new external verifier process. This external verifier is a separate process, so it does not receive the custom command line attributes set on the Corda node process. To rectify this, a new configuration field has been defined to allow custom command line attributes to be passed to the external verifier process. This new configuration field is `custom.externalVerifierJvmArgs`.

  For more information, see the `custom` configuration field in the [Configuration fields]({{< relref "node/setup/corda-configuration-fields.md#custom" >}}) section.

## Corda Enterprise Edition 4.12.4 release notes

Corda Enterprise Edition 4.12.4 is a patch release of Corda Enterprise Edition focused on upgrading dependencies to address security updates.

### Upgrade recommendation

{{< important >}}
When upgrading a node to Corda 4.12, it is extremely important that you run the Transaction Validator Utility on your node database to verify that the transactions in the old node are compatible with 4.12 nodes.

To ensure compatibility of the transactions, you must also run the Transaction Validator Utility on any older nodes that are not being upgraded and will likely interact with any upgraded nodes.

For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "upgrade-guide.md" >}}).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 or below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

### Fixed issues

* Log4j has been downgraded from version 2.23.1 to 2.23.0 to avoid a defect in Log4j that could cause excessive messages to be written to the log file. This will be updated to a later version when a fixed Log4j is available.

### Third-party components upgrade

The following table lists the dependency version changes between 4.12.3 and 4.12.4 Enterprise Editions:

| Dependency                   | Name                | Version 4.12.3 Enterprise   | Version 4.12.4 Enterprise      |
|------------------------------|---------------------|-----------------------------|--------------------------------|
| io.netty:netty-buffer <br> io.netty:netty-codec* <br> io.netty:netty-common <br> io.netty:netty-handler* <br> io.netty:netty-resolver <br> io.netty:netty-transport* | Netty               | 4.1.109.Final         | 4.1.115.Final             |
| org.apache.logging.log4j:*   | Apache                | 2.23.1           | 2.23.0          |

## Corda Enterprise Edition 4.12.3 release notes

Corda Enterprise Edition 4.12.3 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

{{< important >}}
When upgrading a node to Corda 4.12, it is extremely important that you run the Transaction Validator Utility on your node database to verify that the transactions in the old node are compatible with 4.12 nodes.

To ensure compatibility of the transactions, you must also run the Transaction Validator Utility on any older nodes that are not being upgraded and will likely interact with any upgraded nodes.

For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "upgrade-guide.md" >}}).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 or below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

### Fixed issues

* Fixed an issue where CorDapp builds may fail to build with the error `java.lang.NoSuchFieldError: id_ml_dsa_44`. This issue arose from a version mismatch in Bouncy Castle libraries. A new LTS version of Bouncy Castle introduced this field, and it was being picked up due to version ranges specified in the Bouncy Castle dependencies. The issue has now been resolved by locking the Bouncy Castle dependencies to a specific version within Corda.

* A `ClassNotFound` error, causing transaction verification to fail, does no longer occur when deserializing commands from a legacy transaction in the external verifier. This would sometimes happen because the class loader used during deserialization did not include any CorDapps and the missing class could not be auto-constructed. In cases where it did work, it was only because Corda managed to construct the missing class. This issue has now been resolved by ensuring that CorDapp classes are available during deserialization. Additionally, the external verifier's ability to auto-construct missing classes has been disabled.

* Transactions with the in-flight transaction state, introduced in Corda version 4.11 to support transaction recovery, are no longer included when the Ledger Graph CorDapp builds a transaction graph. Instead, the CorDapp now ignores any transactions with an in-flight status.

* The notary health check client tool now starts without any issues.

* The Transaction Validator Utility (TVU) with a provided reverification file accurately reports the number of discovered transactions, even when the provided reverification file includes blank lines.

## Corda Enterprise Edition 4.12.2 release notes

Corda Enterprise Edition 4.12.2 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

{{< important >}}
When upgrading a node to Corda 4.12, it is extremely important that you run the Transaction Validator Utility on your node database to verify that the transactions in the old node are compatible with 4.12 nodes.

To ensure compatibility of the transactions, you must also run the Transaction Validator Utility on any older nodes that are not being upgraded and will likely interact with any upgraded nodes.

For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "upgrade-guide.md" >}}).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 or below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

### Transaction Validator Utility Updates

The following section describes the updated requirements for running the Transaction Validator Utility (TVU) and Corda 4.12 nodes. It clarifies and enhances the previous documentation. The current patch release documentation has been updated to reflect the following:

* Legacy contracts directory: The legacy contracts directory is no longer required when running the TVU or when running 4.12 nodes, provided all nodes on the network are version 4.12 nodes.

* 4.12 environment requirement: You must run the TVU in a 4.12 environment (excluding the database). Specifically, the `cordapps` directory must contain only 4.12-compatible CorDapps. See point 1 below.

* Purpose of legacy contracts directory: The legacy contracts directory is now only needed for enabling 4.12 nodes to build transactions that include legacy contracts. This is only applicable in a mixed network of 4.12 nodes and pre-4.12 nodes.

* Legacy JARs directory: You may need to include a `legacy-jars` directory when running both the TVU and the node. See point 4 below for further details.

#### Transaction Validator Utility

The purpose of the TVU is to mimic what a 4.12 node would do when verifying a legacy transaction, and report any errors found.

1. You must run the TVU in a 4.12 node directory, using the 4.11 database to be validated (or a database upgraded to 4.11). Ensure that the CorDapps directory contains 4.12 CorDapps, and include any pre-4.12 dependencies in the `legacy-jars` directory if required by existing contract attachments on the ledger (see point 4 below). Note that the `legacy-contracts` directory is not necessary.

#### Corda 4.12 nodes

2. If your network includes a mix of 4.12 nodes and pre-4.12 nodes, each 4.12 node must have a `legacy-contracts` directory containing pre-4.12 contract CorDapps. This allows 4.12 nodes to build transactions that include pre-4.12 contracts, enabling interoperability with pre-4.12 nodes. In this scenario, you may also need a `legacy-jars` directory - see point 4 below.

3. If your network consists solely of upgraded 4.12 nodes, there is no need for the `legacy-contracts` directory. The 4.12 nodes will create transactions without legacy contracts, which is fine as there are no pre-4.12 nodes in the network. In this scenario, since the ledger already contains pre-4.12 transactions, you may still need a `legacy-jars` directory - see point 4 below.

4. Pre-4.12 transactions are verified in an external verifier process when encountered. This process does not, by default, include all third-party libraries that shipped with Corda 4.11 and earlier, nor does it have the `drivers` directory on the classpath. If your contracts in the ledger attachments depend on such third-party libraries or any contents from the `drivers` directory in Corda 4.11 or earlier, you can place the necessary JAR files in a directory called `legacy-jars` within the node directory. Any JARs in this directory will be added to the classpath of the external verifier. The TVU will assist you in identifying and verifying the resolution of such issues.

### Fixed issues

* There is no need for the external verifier to use the `legacy-contracts` folder anymore. The external verifier verifies pre-4.12 transactions and now solely uses the database to retrieve the contract attachments.
* An open telemetry span has been added around the Send to Multiple Parties and Receive from Multiple Parties operations.
* Previously, the transaction builder would log any failed verification attempts when trying to add missing dependencies. Now, these failed attempts are no longer logged if they occur while determining the missing dependencies.
* This release contains AMQP serialisation performance improvements.
* It is now possible to create two nodes whose X.500 names have the same Organisation (O) field value but different Organisation Unit (OU) values when using the driver DSL for testing.
* There is no longer a memory leak when creating a series of mock networks for testing purposes.
* The transaction builder no longer attaches legacy attachments to a transaction if the minimum platform version is 140 (i.e., 4.12).
* If the expected subject name does not match the actual subject name and the Float disconnects, a warning is logged.
* The TVU now includes the CorDapps class loader when deserializing output states as part of its deserialization test. Additionally, the TVU now also includes the same set of add-opens options as the node.
* The TVU is no longer writing the JDK17 attachments to the database when verifying transactions.
* A memory leak in the TVU has been resolved.
* A null pointer exception from the TVU (when resolving some parent paths) has been resolved.
* The TVU is no longer raising an exception when outputting a JSON representation of another exception.
* The TVU now parses configuration files in the same way as the node.
* A new `legacy-jars` directory has been introduced to improve backward compatibility with earlier versions of Corda. See the description above and the upgrade guide for details.
* Contract JAR signing key rotation of R3-provided CorDapps is included in this patch release.

### Known issues

* The Finance Contracts CorDapp was inadvertently embedded in the Corda Enterprise 4.12 node JAR, causing issues with various tests and potentially affecting anyone using these contracts in transactions. If you are using the Finance CorDapp, R3 strongly recommends upgrading to this patch release, preferably before going live on version 4.12.

### Third party components upgrade

The following table lists the dependency version changes between 4.12.1 and 4.12.2 Enterprise Editions:

| Dependency                                     | Name                   | Version 4.12.1 Enterprise   | Version 4.12.2 Enterprise      |
|------------------------------------------------|------------------------|-----------------------------|--------------------------------|
| org.eclipse.jetty:*                            | Jetty                  | 12.0.7                      | 12.0.14                        |
| commons-io:commons-io                          | commons IO             | 2.7                         | 2.17.0                         |
| org.apache.commons:commons-configuration2      | commonsConfiguration2  | 2.10.1                      | 2.11.0                         |
| org.apache.sshd:sshd-common                    | sshd                   | 2.12.1                      | 2.13.2                         |
| org.apache.zookeeper:*                         | Zookeeper              | 3.8.3                       |  3.8.4                         |

## Corda Enterprise Edition 4.12.1 release notes

Corda Enterprise Edition 4.12.1 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

{{< important >}}
When upgrading a node to Corda 4.12, it is extremely important that you run the Transaction Validator Utility on your node database to verify that the transactions in the old node are compatible with 4.12 nodes.

To ensure compatibility of the transactions, you must also run the Transaction Validator Utility on any older nodes that are not being upgraded and will likely interact with any upgraded nodes.

For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "upgrade-guide.md" >}}).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 or below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

### Fixed issues

* `ReceiveFinalityFlow` was returning a transaction that was missing the notary signature. This has now been fixed. The returned transaction now includes the notary signature.
* `ReceiveTransactionFlow` was checking that the network parameters on the transaction existed before `ResolveTransactionFlow` was executed.
    This could cause a problem in certain scenarios; for example, when sending a top-level transaction to a new node in a migrated network, as the old network parameters would not exist on this new node. This has now been fixed.
* When resolving a party, in some code paths, `wellKnownPartyFromAnonymous` did not consider notaries from network parameters when trying to resolve an X.500 name. This scenario could occur when introducing a new node to a newly-migrated network as the new node would not have the old notary in its network map. This has now been fixed. Notaries from network parameters are now considered in the check.

## Corda Enterprise Edition 4.12 release notes

The Corda Enterprise Edition 4.12 release introduces upgrades to the Java and Kotlin versions, along with associated upgrade support. Apart from the features supporting the Java and Kotlin upgrade, no other major new features have been introduced. In this release, Java has been upgraded to Java 17 from Java 8 and Kotlin has been upgraded to Kotlin 1.9.20 from 1.2.71.

When a CorDapp(s) and a node are successfully upgraded to 4.12, you are able to seamlessly interoperate 4.12 and 4.11 (or earlier) nodes on the same network, including the existing transactions on the ledger.

Supporting new Java and Kotlin versions is a major feature, as we must also handle legacy contracts from existing backchains. The upgraded Java and Kotlin versions also have implications for CorDapp developers. Simply replacing the Corda JAR without introducing other changes is not possible.

### Upgrade recommendation

{{< important >}}
When upgrading a node to Corda 4.12, it is extremely important that you run the Transaction Validator Utility on your node database to verify that the transactions in the old node are compatible with 4.12 nodes.

To ensure compatibility of the transactions, you must also run the Transaction Validator Utility on any older nodes that are not being upgraded and will likely interact with any upgraded nodes.

For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "upgrade-guide.md" >}}).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 and below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

### Platform version change

Corda 4.12 uses platform version 140.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

### New features, enhancements and restrictions

#### Java and Kotlin upgrade

Corda 4.12 requires Java 17 and Kotlin 1.9.20. This means that you must recompile any legacy CorDapps written for 4.11 or earlier to work with Java 17 and Kotlin 1.9.20 to be compatible with Corda 4.12. These upgrades enhance the supportability and security of Corda.

#### Java 17 compatible releases of Corda SDKs

The base Corda package includes several SDKs and libraries. These SDKs and libraries are compatible with Java 17 and Kotlin 1.9.20:

| SDK/library               | Java 17 compatible release    |
|---------------------------|-------------------------------|
| corda-shell               | 4.12                          |
| r3-libs                   | 1.4                           |
| confidential-identities   | 1.2                           |
| accounts                  | 1.1                           |
| token-sdk                 | 1.3                           |
| reissue-cordapp           | 1.1                           |
| archiving                 | 1.2                           |
| ledger-graph              | 1.3                           |
| r3-tools                  | 4.12                          |

#### Collaborative Recovery removed

The Collaborative Recovery solution, along with the associated CorDapps (LedgerSync and LedgerRecover), is deprecated, and has been removed in Corda 4.12. You are now advised to use the new recovery tools introduced in version 4.11, as described in the [Corda Enterprise Edition 4.11 release notes]({{< relref "../../4.11/enterprise/release-notes-enterprise.md#corda-enterprise-edition-411-release-notes-1" >}}).

#### Transaction Validator Utility

Corda 4.12 introduces the Transaction Validator Utility (TVU), a tool that validates transactions committed to the database to avoid post-migration errors when upgrading to Corda 4.12. For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).

#### Support for signature constraints only

Only CorDapps using signature constraints are supported in Corda 4.12; hash constraints are not supported. Using signature constraints has been recommended in previous releases of Corda as it eases the CorDapp upgrade process. If you have any 4.11 CorDapps using hash constraints, you must migrate them to signature constraints on 4.11 before upgrading to 4.12.

#### Corda 4.11 and 4.12 CorDapps must be signed by the same set of keys

Once you have recompiled your 4.12 CorDapps for Java 17 and Kotlin 1.9.20, you must sign them using the same set of keys used by the 4.11 CorDapp.

#### Explicit contract upgrade is not supported

Explicit contract upgrade is not supported in Corda 4.12.

#### `toLedgerTransaction.verify` does not work for legacy transactions

You must review your CorDapps and check for any making the following calls:
* `SignedTransaction.toLedgerTransaction().verify()`
* `WireTransaction.toLedgerTransaction().verify()`
* `TransactionBuilder.toLedgerTransaction().verify()`

CorDapps that make the above calls will not work for legacy transactions. To make those CorDapps compatible, change them to `SignedTransaction.verify()`.

#### Corda node explorer not supported on Java 17

The node explorer has not been converted to use Java 17 and is not provided in the release packs. If you wish to use a node explorer, the only current option is to use a 4.11 node explorer and use it to connect to a 4.12 node.

#### Samples Kotlin and Java support

The following two public repositories provide various CorDapp samples (branch: release/4.12):
* [Samples Kotlin repository](https://github.com/corda/samples-kotlin/tree/release/4.12)
* [Samples Java repository](https://github.com/corda/samples-java/tree/release/4.12)

Most samples have been converted over to Java 17, Kotlin 1.9.20, and Gradle 7.6.4.

The samples have been written to work with Corda Open Source. To convert a sample to work with Corda Enterprise, then at a minimum you need to point to a repository where your enterprise artifacts are installed. Also, the artifact group name for ENT (`com.r3`) must be different from OS `(net.corda`). For example, switch `net.corda:corda-node-driver:4.12` (Corda OS) to `com.r3.corda:corda-node-driver:4.12` (Corda ENT).

The following dependencies have been used in samples and can be switched from Corda OS to Corda Enterprise:
* corda
* corda-confidential-identities
* corda-core-test-utils
* corda-finance-workflows
* corda-jackson
* corda-node
* corda-node-api
* corda-node-driver
* corda-rpc
* corda-shell
* corda-test-utils
* corda-testserver-impl

The samples listed below have been converted to and tested with Java 17 and Kotlin 1.9.20:

| CorDapp type       | CorDapp                              |
|--------------------|--------------------------------------|
| Accounts           | obligation-accounts                  |
|                    | sharestatewithaccount                |
|                    | supplychain                          |
|                    | worldcupticketbooking                |
| Advanced           | duediligence-cordapp                 |
|                    | negotiation-cordapp                  |
|                    | obligation-cordapp                   |
|                    | superyacht-cordapp                   |
|                    | syndicated-lending                   |
| Basic              | cordapp-example                      |
|                    | flow-database-access                 |
|                    | flow-http-access                     |
|                    | opentelemetry-cordapp-example        |
|                    | ping-pong                            |
|                    | tutorial-applestamp                  |
|                    | tutorial-jarsigning                  |
|                    | tutorial-networkbootrstrapper        |
| Features           | attachment-blacklist                 |
|                    | attachment-sendfile                  |
|                    | confidentialIdentity-whistleblower   |
|                    | contractsdk-recordplayers            |
|                    | cordaService-autopayroll             |
|                    | customlogging-yocordapp              |
|                    | customquery-carinsurance             |
|                    | dockerform-yocordapp                 |
|                    | encumbrance-avatar                   |
|                    | multioutput-transaction              |
|                    | notarychange-iou                     |
|                    | observableStates-tradereporting      |
|                    | oracle-primenumber                   |
|                    | postgres-cordapp                     |
|                    | queryableState-carinsurance          |
|                    | referenceStates-sanctionsBody        |
|                    | schedulableState-heartbeat           |
|                    | state-reissuance                     |
| Tokens             | bikemarket                           |
|                    | dollartohousetoken                   |
|                    | fungiblehousetoken                   |
|                    | stockpaydividend                     |
|                    | tokentofriend                        |

#### Kotlin and Java CorDapp templates

The following Kotlin and Java CorDapp templates have been converted to Java 17, Kotlin 1.9.20, and Gradle 7.6.4. They have been written to work with Corda Open Source Edition (branch: release/4.12):
* [Kotlin CorDapp template](https://github.com/corda/cordapp-template-kotlin/tree/release/4.12)
* [Java CorDapp template](https://github.com/corda/cordapp-template-java/tree/release/4.12)

### No optional gateway plugins release pack

The optional gateway plugins release pack contains the flow and node management plugins used by the CENM gateway service. These plugins provide GUI-based flow and node management functionality. Since CENM has not yet been converted to use Java 17, these plugins are not included in the 4.12 release. Once CENM and plugins have been converted, they will be added in a future release. If you wish to use flow and node management functionality, you can obtain the plugins from the 4.11 `optional-gateway-plugins` release pack and use them with the CENM gateway service.

#### CorDapp using internal APIs or reflective access

If your CorDapp is using internal APIs or reflective access, then you may need to explicitly open the module on the command line. You can do this by adding one or more `–add-opens` options when starting Corda.

### Fixed issues

#### Thread.contextClassLoader set for resumed flow on node startup

Previously, if a flow was resuming on node startup, the thread context class loader was not set, potentially causing `ClassNotFound` issues for CorDapp classes. This has been fixed now.

### Known issues

#### Extra stack trace output when logging level is `TRACE`

If you start the node with log level set to trace via the command line option `--logging-level=TRACE`, then you will see some `Unable to format stack trace` outputs from Log4j caused by a bug in Artemis. These can be ignored and have no effect on node operation. They can be removed via a custom log4j.xml where trace output from the `org.apache.activemq.artemis.core.paging.cursor.impl.PageCursorProviderImpl` logger is removed.

#### Startup warnings from Log4j

At node startup with the default Log4j, the following message appears: `main WARN The use of package scanning to locate plugins is deprecated and will be removed in a future release.` This is a warning only and can be safely ignored. We are currently investigating alternatives.

#### `notaryhealthcheck-client` fails to start

The Corda 4.12 `notaryhealthcheck-client` fails to start. This will be fixed in a future patch release. As an alternative, you can use the `notaryhealthcheck-client` provided with the Corda 4.11 release.

#### Intermittent warning from Bouncy Castle when running `deployNodes`

When running the Gradle task `deployNodes`, you may occasionally see the following warning message:

```
exception in disposal thread: org/bouncycastle/util/dispose/DisposalDaemon$3
```

This is a warning message from the LTS version of Bouncy Castle we are currently using. There is no user impact and it is related to disposing of references with native code. This will be fixed in a future patch release.

### Third party component upgrades

The following table lists the dependency version changes between 4.11 and 4.12 Enterprise Editions:

| Dependency                                     | Name                   | Version 4.11 Enterprise   | Version 4.12 Enterprise  |
|------------------------------------------------|------------------------|---------------------------|------------------------- |
| com.google.guava:guava                         | Guava                  | 28.0-jre                  | 33.1.0-jre               |
| co.paralleluniverse:quasar-core	               | Quasar	                | 0.7.16_r3	                | 0.9.0_r3                 |
| org.bouncycastle	                             | Bouncy Castle	        | jdk18on:1.75	            | lts8on:2.73.6            |
| pro com.guardsquare:proguard-gradle	           | ProGuard	              | 6.1.1	                    | 7.3.1                    |
| org.yaml:snakeyaml	                           | SnakeYAML	            | 1.33	                    | 2.2                      |
| com.github.ben-manes.caffeine:caffeine         | Caffeine	              | 2.9.3	                    | 3.1.8                    |
| io.netty:netty-tcnative-boringssl-static	     | TC Native	            | 2.0.48.Final	            | 2.0.65.Final             |
| org.apache.commons:commons-configuration2      | Commons Configuration2	| 2.10.0	                  | 2.10.1                   |
| co.paralleluniverse:capsule	                   | Capsule	              | 1.0.3	                    | 1.0.4_r3                 |
| org.ow2.asm:asm	                               | ASM	                  | 7.1	                      | 9.5                      |
| org.apache.activemq:*	                         | Artemis	              | 2.19.1	                  | 2.32.0                   |
| com.fasterxml.jackson.*	                       | Jackson XML	          | 2.13.5	                  | 2.17.0                   |
| org.eclipse.jetty.ee10:jetty-ee10-*	           | Jetty	                | 9.4.53.v20231009	        | 12.0.7                   |
| org.glassfish.jersey.*	                       | Jersey	                | 2.25	                    | 3.1.6                    |
| javax.validation:validation-api	               | Validation	            | -	                        | 2.0.1.Final              |
| org.slf4j:*	Simpe                              | Log4J	                | 1.7.30	                  | 2.0.12                   |
| org.apache.logging.log4j:*	                   | Log4j	                | 2.17.1	                  | 2.23.1                   |
| com.squareup.okhttp3:okhttp	                   | OK HTTP	              | 3.14.9	                  | 4.12.0                   |
| io.netty:*	                                   | Netty                	| 4.1.77.Final	            | 4.1.109.Final            |
| org.apache.commons:commons-fileupload2-jakarta | File Upload	          | 1.4	                      | 2.0.0-M1                 |
| com.esotericsoftware:kryo	                     | Kryo	                  | 4.0.2	                    | 5.5.0                    |
| org.mockito:mockito-core	                     | Mockito	              | 2.28.2	                  | 5.5.0                    |
| org.mockito.kotlin:mockito-kotlin	             | Mockito for Kotlin	    | 1.6.0	                    | 5.2.1                    |
| org.jetbrains.dokka:dokka-gradle-plugin	       | Dokka for Gradle       | 0.10.1	                  | 1.8.20                   |
| net.i2p.crypto:eddsa	                         | EddSA	                | 0.3.0	                    | -                        |
| com.zaxxer:HikariCP	                           | Hikari	                | 3.3.1	                    | 5.1.0                    |
| org.iq80.snappy:snappy	                       | Snappy	                | 0.4	                      | 0.5                      |
| commons-io:commons-io	                         | Commons I/O	          | 2.6	                      | 2.7                      |
| org.javassist:javassist	                       | Java Assist	          | 3.27.0-GA	                | 3.29.2-GA                |
| org.jooq:joor	                                 | Joor	                  | -	                        | 0.9.15                   |
| org.apache.curator:*	                         | Apache Curator	        | 5.1.0	                    | 5.6.0                    |
| org.apache.zookeeper:zookeeper	               | Apache Zookeeper	      | -	                        | 3.8.3                    |
| org.apache.commons:commons-dbcp2	             | Apache Commons	        | -	                        | 2.12.0                   |
