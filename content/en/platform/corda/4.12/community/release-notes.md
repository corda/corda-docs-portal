---
title: Corda Community Edition 4.12 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2024-06-04'
menu:
  corda-community-4-12:
    identifier: corda-community-4-12-release-notes
    parent: about-corda-landing-4-12-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Community Edition 4.12 release notes

The Corda Community Edition 4.12 release introduces upgrades to the JDK and Kotlin versions, along with associated upgrade support. Besides the features supporting the JDK/Kotlin upgrade, no other major new features have been introduced.

When a CorDapp(s) and a node are successfully upgraded to 4.12, you are able to seamlessly interoperate 4.12 and 4.11 (or earlier) nodes on the same network, including the existing transactions on the ledger.

Supporting new JDK and Kotlin versions is a major feature, as we must also handle legacy contracts from existing backchains. The upgraded JDK and Kotlin versions also have implications for CorDapp developers. Simply replacing the Corda JAR without introducing other changes is not possible.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../community/_index.md" >}}) as soon as possible. The latest Corda Community release notes are on this page, and for the latest upgrade guide, refer to Corda Enterprise Edition 4.11 to 4.12 upgrade guide (LINK TO THE UPGRADE GUIDE).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 and below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

## Platform version change

Corda 4.12 uses platform version 140.

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

## New features and enhancements

### Java upgrade

Java version was upgraded to Java 17.

### Kotlin upgrade

Kotlin version was upgraded to Kotlin 1.9.

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

## Known issues

## Third party component upgrades

The following table lists the dependency version changes between 4.11.1 and 4.12 Community Editions:

| Dependency                         | Name                | Version 4.11.1 Enterprise | Version 4.12 Enterprise|
|------------------------------------|---------------------|---------------------------|------------------------|
| org.bouncycastle                   | Bouncy Castle       | bcprov-jdk18on:1.75       |     |
| co.paralleluniverse:quasar-core    | Quasar              | 0.7.16_r3                 |               |
| org.hibernate                      | Hibernate           | 5.6.14.Final              |           |
| com.h2database                     | H2                  | 2.2.2241                  |                |
| org.liquibase                      | Liquibase           | 4.20.0                    |                  |
|                       | Log4j           |                     | 2.23.1                 |
|                       | SLF4J           |                     | 2.0.12                 |

