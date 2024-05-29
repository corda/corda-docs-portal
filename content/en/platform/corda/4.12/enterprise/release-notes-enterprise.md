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

Corda Enterprise Edition 4.12 includes several new features, enhancements, and fixes.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to Corda Enterprise Edition 4.11 to 4.12 upgrade guide (LINK TO THE UPGRADE GUIDE).

The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 and below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.

## Platform version change

Corda 4.12 uses platform version 140.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features and enhancements

### Java upgrade

Java version was upgraded to Java 17.

### Kotlin upgrade

Kotlin version was upgraded to Kotlin 1.9.

### Transaction Validator Utility

Corda 4.12 introduces Transaction Validator Utility (TVU), a tool that validates transactions committed to the database to avoid post-migration errors when upgrading to Corda 4.12. For more information, see Transaction Validator Utility (LINK TO TVU).

## Fixed issues

* Previously, there was a rare error scenario where the node would think it had a valid connection to a peer but actually did not. This would potentially occur when the peer node was disconnecting/connecting. This issue has now been resolved.

## Known issues

## Third party component upgrades

The following table lists the dependency version changes between 4.11.1 and 4.12 Enterprise Editions:

| Dependency                         | Name                | Version 4.11.1 Enterprise | Version 4.12 Enterprise|
|------------------------------------|---------------------|---------------------------|------------------------|
| org.bouncycastle                   | Bouncy Castle       | bcprov-jdk18on:1.75       |     |
| co.paralleluniverse:quasar-core    | Quasar              | 0.7.16_r3                 |               |
| org.hibernate                      | Hibernate           | 5.6.14.Final              |           |
| com.h2database                     | H2                  | 2.2.2241                  |                |
| org.liquibase                      | Liquibase           | 4.20.0                    |                  |

