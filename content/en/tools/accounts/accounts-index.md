---
date: '2021-04-24T00:00:00Z'
description: "Documentation for the Corda Accounts Library"
section_menu: tools
menu:
  tools:
    name: Corda Accounts Library
    weight: 200
    identifier: tools-accounts
title: Corda Accounts Library
---

# Corda Accounts Library

In the context of Corda, the Corda Accounts Library allows a Corda node to partition the vault — a collection of state objects — into a number of subsets, where each subset represents an account. In other words, the Corda Accounts Library allows a Corda node operator to split the vault into multiple "logical" sub-vaults. This is advantageous for a couple of reasons:

1. Node operators can reduce costs by hosting multiple entities, as accounts, on one node.
2. Node operators can partition the vault on a per-entity basis.

Accounts are created by host nodes, which are just regular Corda nodes. Hosts can create accounts for a range of purposes, such as customer accounts, balance sheets or P&L accounts, employee accounts, and so on.

The Corda Accounts Library takes the form of a JAR file, which can be dropped into the CorDapps directory. It is optional to use - some nodes will support accounts but others will not. This functionality is intentional, as not all nodes will need to support accounts and the optional nature of accounts reduces the learning curve for new CorDapp developers.

You can access the Corda Accounts Library from the [public repository](https://github.com/corda/accounts).

## Compatibility

Versions 1.1 to 1.1.2 of the Corda Accounts Library are built for **Corda release version 4.12** and higher (minimum platform version 140) and need JDK 17. Version 1.1.2 also runs on **Corda 4.15**, which moves the node to Hibernate 7; see [Changes in Corda Accounts Library 1.1.2](#changes-in-corda-accounts-library-112).

## Changes in Corda Accounts Library 1.1.2

Corda Accounts Library 1.1.2 (17 November 2026) is the release for Corda 4.15, which upgrades the node from Hibernate 5 to Hibernate 7 and Jakarta Persistence. See [Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15]({{< relref "../../platform/corda/4.15/enterprise/hibernate-7-upgrade.md" >}}) for the node side.

* **One jar for Corda 4.12 to 4.14 and for 4.15.** The schema classes carry both the `javax.persistence` (Corda 4.14 and earlier) and the `jakarta.persistence` (Corda 4.15) annotations with the same attributes; the node reads the set its Hibernate understands and the JVM drops the other. The column mappings are unchanged: the `UUID` columns keep Hibernate's binary mapping, which the library's changelogs and Corda 4.15's settings preserve.
* **No Hibernate dependency.** `accounts-workflows` no longer declares `org.hibernate:hibernate-core`, which Corda 4.15 does not provide. The `javax.persistence` and `jakarta.persistence` APIs are compile-only dependencies; neither is bundled.
* **Sharing a state with an account in in-process tests on 4.15.** `ReceiveStateForAccountFlow` persists the account-to-state mapping through whichever persistence API the node's entity manager implements, and its compiled classes refer to neither. With 1.1.1 and earlier, which bind to the `javax.persistence` `EntityManager`, a real 4.15 node converts the class as it loads the jar, but a CorDapp's `MockNetwork`, `MockServices` and in-process driver tests on 4.15 load it unconverted: the host node failed with `NoClassDefFoundError: javax/persistence/EntityManager` and the sharing node with `UnexpectedFlowEndException`.
* **Building from source.** The Corda version to build and test against is the Gradle property `cordaReleaseVersion` (default 4.12.13); `-PcordaReleaseVersion=4.15` overrides it. Build against Corda 4.12 for a jar that runs on both lines: a build against 4.15 runs on 4.15 only, because its `withEntityManager` code binds to the Jakarta `EntityManager`. The Token SDK version the examples use is the property `tokensReleaseVersion` (default 1.3.5).
* **Examples.** The gold-trading example stores its `UUID` element collections through a JPA `AttributeConverter` (the same 36-character string as before) instead of the Hibernate-specific `@Type` annotation, and the examples use Tokens SDK 1.3.5.
* **Dependency updates:** Quasar 0.9.3_r3 and Log4j.

## Changes in Corda Accounts Library 1.1.1

Corda Accounts Library 1.1.1 (16 April 2025) is built against Corda 4.12.5 and updates dependencies. Its build no longer uses the retired JCenter repository.

## Changes in Corda Accounts Library 1.1

Corda Accounts Library 1.1 (25 June 2024) is the first release for Corda 4.12: it is built with JDK 17, and its minimum and target platform version is 140.

To learn how to install and use the Corda Accounts Library, check out the [readme](https://github.com/corda/accounts/blob/master/README.md) and [docs](https://github.com/corda/accounts/blob/master/docs.md) repo pages.
