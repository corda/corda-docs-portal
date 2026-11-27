---
date: '2021-04-24T00:00:00Z'
description: "Documentation for the Tokens SDK; this provides you with the fastest and easiest way to create tokens that represent any kind of asset on your network"
section_menu: tools
menu:
  tools:
    name: Tokens SDK
    weight: 100
    identifier: tools-tokens-sdk
title: Welcome to Tokens SDK
---

The Tokens SDK provides you with the fastest and easiest way to create tokens that represent any kind of asset on your network. This asset can be anything you want it to be—conceptual or physical, valuable or not. You can create a token to represent something outside the network, or something that only exists on the ledger—such as a Corda-native digital currency.

With the SDK, you can define your token and its attributes, then add functionality to a CorDapp so the token can be issued, moved, and redeemed on a ledger.

## Tokens SDK Documentation

Tokens SDK documentation can be found [here](../../../en/platform/corda/{{< latest-c4-version >}}/enterprise/cordapps/token-sdk-introduction.md).

## Upgrading

If you have developed a CorDapp that uses the Tokens SDK 1.1 or 1.2.1, you can upgrade to 1.2.3.

## Compatibility

Versions 1.2.1 and 1.2.3 of the Tokens SDK are compatible with **Corda release version 4.6** and higher.

Versions 1.2.4 and 1.2.5 of the Tokens SDK are compatible with **Corda release version 4.8** and higher.

Versions 1.3 to 1.3.5 of the Tokens SDK are built for **Corda release version 4.12** and higher (minimum platform version 140) and need JDK 17. Version 1.3.5 also runs on **Corda 4.15**, which moves the node to Hibernate 7; see [Changes in Tokens SDK 1.3.5](#changes-in-tokens-sdk-135).

## Changes in Tokens SDK 1.3.5

Tokens SDK 1.3.5 (17 November 2026) is the release for Corda 4.15, which upgrades the node from Hibernate 5 to Hibernate 7 and Jakarta Persistence. See [Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15]({{< relref "../../platform/corda/4.15/enterprise/hibernate-7-upgrade.md" >}}) for the node side.

* **One jar for Corda 4.12 to 4.14 and for 4.15.** The schema classes carry both the `javax.persistence` (Corda 4.14 and earlier) and the `jakarta.persistence` (Corda 4.15) annotations with the same attributes; the node reads the set its Hibernate understands and the JVM drops the other. The distribution record's `linear_id` keeps its mapping, a `VARCHAR` holding the 36-character UUID string, on both Hibernate versions. The tables and columns are unchanged.
* **No Hibernate dependency.** `tokens-workflows` no longer declares `org.hibernate:hibernate-core` at runtime scope, and the POMs declare the Corda modules the SDK is built against as `provided` rather than `runtime`. A CorDapp built against Corda 4.15 with `tokens-workflows` 1.3.4 or earlier got Hibernate 5 and `corda-node-api` 4.12 from the SDK, and Gradle failed with `Cannot select module with conflict on capability 'org.hibernate:hibernate-core'`.
* **Distribution list updates in in-process tests on 4.15.** The distribution list code, used by evolvable tokens, calls the node's entity manager through whichever persistence API the node implements, and its compiled classes refer to neither. With 1.3.4 and earlier, which bind to the `javax.persistence` `EntityManager`, a real 4.15 node converts the classes as it loads the jar, but a CorDapp's `MockNetwork`, `MockServices` and in-process driver tests on 4.15 load them unconverted and fail with `NoClassDefFoundError: javax/persistence/EntityManager`.
* **Building from source.** The Corda version to build and test against is the Gradle property `cordaReleaseVersion` (default 4.12.13); `-PcordaReleaseVersion=4.15` overrides it. Build against Corda 4.12 for a jar that runs on both lines: a build against 4.15 runs on 4.15 only.
* **Dependency updates:** Quasar 0.9.3_r3, Netty 4.1.138, Micrometer 1.17.1.

## Changes in Tokens SDK 1.3.4

Tokens SDK 1.3.4 (10 September 2026) is built against Corda 4.12.12 and updates dependencies: the PostgreSQL JDBC driver used by the tests to 42.7.12 and AssertJ to 3.27.7.

## Changes in Tokens SDK 1.3.3

Tokens SDK 1.3.3 (8 May 2026) contains security dependency updates.

## Changes in Tokens SDK 1.3.2

Tokens SDK 1.3.2 (15 April 2025) is built against Corda 4.12.5 and updates dependencies.

## Changes in Tokens SDK 1.3.1

Tokens SDK 1.3.1 (17 December 2024) is built against Corda 4.12.4 and updates dependencies. Its build no longer uses the retired JCenter repository.

## Changes in Tokens SDK 1.3

Tokens SDK 1.3 (25 June 2024) is the first release for Corda 4.12: it is built with JDK 17 and Kotlin 1.8, its minimum and target platform version is 140, and the contract version (`versionId`) is 3. The contract JARs are signed with the Corda development key, and the release contains security dependency updates.

## Changes in Tokens SDK 1.2.5

This release of the Tokens SDK contains security vulnerability updates.

## Changes in Tokens SDK 1.2.4

Previously, the in-memory token selector would start loading its tokens in parallel to the vault being initialised or during node startup, which may have resulted in some tokens not being loaded into the selector. This issue has now been resolved.

## Changes in Tokens SDK 1.2.3

In Tokens SDK 1.2.3, the `holder` column in the `fungible_token` and `non_fungible_token` tables is now nullable.

## Changes in Tokens SDK 1.2.2

In 1.2.2, a new [Token Selection](../../../../../../en/platform/corda/{{< latest-c4-version >}}/enterprise/cordapps/token-selection.md) feature allows the exception `InsufficientNotLockedBalanceException` to be thrown when sufficient funds appear to exist for a transaction to take place, but an excess of those funds are soft locked by other in-flight transactions. The warning tells you that there are insufficient funds that have not been soft locked to satisfy the transaction amount.

## Changes in Tokens SDK 1.2.1

The main changes in the Tokens SDK from 1.1 to 1.2.1 are designed to improve application of the SDK for those using a Java code base.

Overview of changes:

* All of the utility methods, subflows and RPC enabled flows have been annotated with @JVMOverloads to ensure the appropriate Java constructors are generated where the source Kotlin constructor contains nullable arguments. This ensures a seamless experience when using the Tokens SDK from a Java code base.
* The `selection` and `money` JAR files have been moved into the `workflows` JAR file.
* Upgraded database interaction for compatibility with Corda 4.6 and Corda Enterprise Edition 4.6.

