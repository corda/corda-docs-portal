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

The Corda Enterprise Edition 4.12 release introduces upgrades to the JDK and Kotlin versions, along with associated upgrade support. Besides the features supporting the JDK/Kotlin upgrade, no other major new features have been introduced.

When a CorDapp(s) and a node are successfully upgraded to 4.12, you are able to seamlessly interoperate 4.12 and 4.11 (or earlier) nodes on the same network, including the existing transactions on the ledger.

Supporting new JDK and Kotlin versions is a major feature, as we must also handle legacy contracts from existing backchains. The upgraded JDK and Kotlin versions also have implications for CorDapp developers. Simply replacing the Corda JAR without introducing other changes is not possible.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to Corda Enterprise Edition 4.11 to 4.12 upgrade guide (LINK TO THE UPGRADE GUIDE).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 and below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

## Platform version change

Corda 4.12 uses platform version 140.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features and enhancements

### Java and Kotlin upgrade

Corda 4.12 requires Java 17 and Kotlin 1.9.20. This means that you must recompile any legacy CorDapps written for 4.11 or earlier to work with Java 17 and Kotlin 1.9 to be compatible with Corda 4.12. These upgrades enhance the supportability and security of Corda.

### Java 17 compatible releases of Corda SDKs

A number of SDKs and libraries are provided with the base Corda package. These are their Java 17 and Kotlin 1.9 versions:

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

### Transaction Validator Utility

Corda 4.12 introduces Transaction Validator Utility (TVU), a tool that validates transactions committed to the database to avoid post-migration errors when upgrading to Corda 4.12. For more information, see Transaction Validator Utility (LINK TO TVU).

### Support for signature constraints only

Only CorDapps using signature constraints are supported in Corda 4.12; hash constraints are not supported. Using signature constraints has been recommended in previous releases of Corda as it eases the CorDapp upgrade process. If you have any 4.11 CorDapps using hash constraints, you must migrate them to signature constraints on 4.11 before upgrading to 4.12.

### Corda 4.11 and 4.12 CorDapps must be signed by the same set of keys

Once you have recompiled your 4.12 CorDapps for JSK17 and Kotlin 1.9.20, you must sign them using the same set of keys used by the 4.11 CorDapp.

### Explicit contract upgrade is not supported

Explicit contract upgrade is not supported in Corda 4.12.

### `toLedgerTransaction.verify` does not work for legacy transactions

You must review your CorDapps and checked for any making the following calls:
* `SignedTransaction.toLedgerTransaction().verify()`
* `WireTransaction.toLedgerTransaction().verify()`
* `TransactionBuilder.toLedgerTransaction().verify()`

CorDapps that make the above calls, will not work for legacy transactions. To have those CorDapps work, change them to `SignedTransaction.verify()`.

### No 4.12 JDK 17 node explorer

The node explorer has not been converted to use JDK17 and is not provided in the release packs. If you wish to use a node explorer, the only current option is to use a 4.11 node explorer and use it to connect to a 4.12 node.

### Samples Kotlin and Java support

The following two public repositories provide various CorDapp samples:
* [Samples Kotlin repository](https://github.com/corda/samples-kotlin/tree/release/4.12)
* [Samples Java repository](https://github.com/corda/samples-java/tree/release/4.12)

Most (but not all) samples have been converted over to JDK17, Kotlin 1.9.20 and Gradle 7.6.4.

The samples have been written to work with Corda OS, to have them use Corda ENT do the following:

| CorDapp type       | CorDapp                              | Status samples-kotlin     | Status samples-java  |
|--------------------|--------------------------------------|---------------------------|----------------------|
| Accounts           | obligation-accounts                  | FULLY WORKING             | N/A                  |
|                    | sharestatewithaccount                | FULLY WORKING             | N/A                  |
|                    | supplychain                          | FULLY WORKING             | FULLY WORKING        |
|                    | worldcupticketbooking                | N/A                       | FULLY WORKING        |
| Advanced           | duediligence-cordapp                 | FULLY WORKING             | FULLY WORKING        |
|                    | negotiation-cordapp                  | FULLY WORKING             | FULLY WORKING        |
|                    | obligation-cordapp                   | FULLY WORKING             | FULLY WORKING        |
|                    | superyacht-cordapp                   | FULLY WORKING             | N/A                  |
|                    | syndicated-lending                   | FULLY WORKING             | FULLY WORKING        |
| Basic              | cordapp-example                      | FULLY WORKING             | FULLY WORKING        |
|                    | flow-database-access                 | FULLY WORKING             | FULLY WORKING        |
|                    | flow-http-access                     | FULLY WORKING             | FULLY WORKING        |
|                    | opentelemetry-cordapp-example        | FULLY WORKING             | N/A                  |
|                    | ping-pong                            | FULLY WORKING             | FULLY WORKING        |
|                    | tutorial-applestamp                  | FULLY WORKING             | FULLY WORKING        |
|                    | tutorial-jarsigning                  | FULLY WORKING             | FULLY WORKING        |
|                    | tutorial-networkbootrstrapper        | FULLY WORKING             | FULLY WORKING        |
| Features           | attachment-blacklist                 | FULLY WORKING             | FULLY WORKING        |
|                    | attachment-sendfile                  | FULLY WORKING             | FULLY WORKING        |
|                    | confidentialIdentity-whistleblower   | FULLY WORKING             | FULLY WORKING        |
|                    | contractsdk-recordplayers            | FULLY WORKING             | FULLY WORKING        |
|                    | cordaService-autopayroll             | FULLY WORKING             | FULLY WORKING        |
|                    | customlogging-yocordapp              | FULLY WORKING             | FULLY WORKING        |
|                    | customquery-carinsurance             | FULLY WORKING             | FULLY WORKING        |
|                    | dockerform-yocordapp                 | FULLY WORKING             | FULLY WORKING        |
|                    | encumbrance-avatar                   | FULLY WORKING             | FULLY WORKING        |
|                    | multioutput-transaction              | N/A                       | FULLY WORKING        |
|                    | notarychange-iou                     | FULLY WORKING             | FULLY WORKING        |
|                    | observableStates-tradereporting      | FULLY WORKING             | FULLY WORKING        |
|                    | oracle-primenumber                   | FULLY WORKING             | FULLY WORKING        |
|                    | postgres-cordapp                     | FULLY WORKING             | FULLY WORKING        |
|                    | queryableState-carinsurance          | FULLY WORKING             | FULLY WORKING        |
|                    | referenceStates-sanctionsBody        | FULLY WORKING             | FULLY WORKING        |
|                    | schedulableState-heartbeat           | FULLY WORKING             | FULLY WORKING        |
|                    | state-reissuance                     | FULLY WORKING             | FULLY WORKING        |
| Tokens             | bikemarket                           | FULLY WORKING             | FULLY WORKING        |
|                    | dollartohousetoken                   | FULLY WORKING             | FULLY WORKING        |
|                    | fungiblehousetoken                   | FULLY WORKING             | FULLY WORKING        |
|                    | stockpaydividend                     | FULLY WORKING             | FULLY WORKING        |

### Kotlin and Java CorDapp templates

The following Kotlin and Java CorDapp templates have been converted to JDK17, Kotlin 1.9.20 and Gradle 7.6.4. They have been written to work with Corda Community Edition:
* [Kotlin CorDapp template](https://github.com/corda/cordapp-template-kotlin/tree/release/4.12)
* [Java CorDapp template](https://github.com/corda/cordapp-template-java/tree/release/4.12)

### No optional gateway plugins release pack

The optional gateway plugins release pack contains the flow and node management plugins used by the CENM gateway service. These plugins provide GUI-based flow and node management functionality. Since CENM has not yet been converted to use JDK17, these plugins are not included in the 4.12 release. Once CENM and plugins have been converted, they will be added in a future release. If you wish to use flow and node management functionality, you can obtain the plugins from the 4.11 `optional-gateway-plugins` release pack and use them with the CENM gateway service.

## Known issues

## Third party component upgrades

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
