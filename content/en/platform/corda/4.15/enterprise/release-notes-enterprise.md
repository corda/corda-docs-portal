---
title: Corda Enterprise Edition 4.15 release notes
date: '2025-03-19'

menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-release-notes
    parent: about-corda-landing-4-15-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.15 release notes

## Corda Enterprise Edition 4.15.2 release notes

Corda Enterprise Edition 4.15.2 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Revert the fix to handle stuck messages in Artemis. Previously on extremely rare occasions messages could become stuck in Artemis. This has now been resolved in Artemis.
* The following table shows the vulnerabilities addressed in this patch release.

| Vulnerability  | Component |
|----------------|-----------|
| CVE-2026-33870 | Netty     |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.15.2. Dependencies with unchanged versions are omitted.

| Dependency                          | Name    | Version |
|-------------------------------------|---------|--------|
| io.netty:netty-*                    | Netty   | 4.1.132.Final       |

## Corda Enterprise Edition 4.15.1 release notes

Corda Enterprise Edition 4.15.1 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Improved error reporting in RPCClientProxyHandler, for example when the user does not have sufficient permissions to perform an operation.
* The following table shows the vulnerabilities addressed in this patch release.

|Vulnerability| Component |
|-------------|-----------|
|CVE-2026-27446| Artemis   |
|CVE-2026-1605| Jetty     |
|CVE-2025-11143| Jetty     |
| CVE-2026-24400 | AssertJ   |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.12.10. Dependencies with unchanged versions are omitted.

| Dependency                          | Name           | Version       |
|-------------------------------------|----------------|---------------|
| com.fasterxml.jackson..*            | Jackson        | 2.18.6        |
| org.apache.activemq:artemis-*       | Artemis        | 2.52.0        |
| org.eclipse.jetty.ee10:jetty-ee10-* | Jetty          | 2.25.3        |

## Corda Enterprise Edition 4.15 release notes

The Corda Enterprise Edition 4.15 release introduces new functionality and third-party component upgrades.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

## Platform version change

Corda 4.15 uses platform version 160.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features, enhancements and restrictions

### Solana notary

Corda Enterprise 4.15 introduces the Solana notary, a new notary type that records notarisation results on the
[Solana](https://solana.com/) blockchain. The Solana notary enables CorDapps to perform atomic cross-chain operations — a Corda
transaction is only notarised if a corresponding Solana program instruction (such as an SPL token transfer) also
succeeds, and vice versa. This makes it possible to build use cases such as atomic delivery-versus-payment where a
Corda asset is exchanged for a Solana-based stablecoin in a single, indivisible operation.

For more information, see [Solana notary]({{< relref "notary/solana-notary.md" >}}).

### Notary instructions

Corda 4.15 introduces `NotaryInstruction`, an extensible mechanism for attaching additional directives to a
transaction that a specialised notary can act on during notarisation. Notary instructions are stored in a new
transaction component group (`NOTARY_INSTRUCTIONS_GROUP`), are covered by the transaction's Merkle tree, and are
available to contracts for verification.

New `TransactionBuilder` and `LedgerTransaction` APIs support notary instructions:

* `TransactionBuilder.addNotaryInstruction(instruction)` — attaches a notary instruction to the transaction being
  built.
* `LedgerTransaction.notaryInstructionsOfType<T>()` — retrieves all notary instructions of a given type, allowing
  contracts to verify them.

For backwards compatibility, standard notaries reject any transaction that contains notary instructions. Only
specialised notaries — such as the Solana notary — accept and process them.

## Known issues

### Solana notary

The Solana notary program only supports a maximum `StateRef` index of 127. However, this is currently not
checked and enforced in the platform when output states are created. CorDapps must ensure they do not create more
than 128 output states in a transaction.

## Third-party component upgrades

The following table lists the dependency version changes for 4.15 Enterprise Editions:

| Dependency                               | Name         | New Version             |
| ---------------------------------------- | ------------ | ----------------------- |
| org.apache.activemq:*                    | Artemis      | 2.44.0                  |
| org.apache.commons:commons-lang3         | Commons Lang | 3.19.0                  |
| org.glassfish.jersey.*                   | Jersey       | 3.1.11                  |
| org.apache.logging.log4j:*               | Log4J        | 2.25.1                  |
| io.netty:*                               | netty        | 4.1.128.Final           |
| io.netty:netty-tcnative-boringssl-static | tcnative     | 2.0.74.Final            |
