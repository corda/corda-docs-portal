---
title: Corda Enterprise Edition 4.14 release notes
date: '2025-03-19'

menu:
  corda-enterprise-4-14:
    identifier: corda-enterprise-4-14-release-notes
    parent: about-corda-landing-4-14-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.14 release notes

The Corda Enterprise Edition 4.14 release introduces new functionality and third-party component upgrades.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

## Platform version change

Corda 4.14 uses platform version 160.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features, enhancements and restrictions

### Solana notary

Corda Enterprise 4.14 introduces the Solana notary, a new notary type that records notarisation results on the
[Solana](https://solana.com/) blockchain. The Solana notary enables CorDapps to perform atomic cross-chain operations — a Corda
transaction is only notarised if a corresponding Solana program instruction (such as an SPL token transfer) also
succeeds, and vice versa. This makes it possible to build use cases such as atomic delivery-versus-payment where a
Corda asset is exchanged for a Solana-based stablecoin in a single, indivisible operation.

For more information, see [Solana notary]({{< relref "notary/solana-notary.md" >}}).

## Known issues

### Solana notary

The Solana notary does not accept `StateRef` indices greater than 127. This has a knock-on effect on Corda
transactions which have more than 128 output states. Any output state which has an index of 128 or greater will not
be consumable by the Solana notary. Currently the platform does not check and prevent such a transaction from being
notarised. CorDapps must do this check themselves.

## Third-party component upgrades

The following table lists the dependency version changes for 4.14 Enterprise Editions:

| Dependency                               | Name         | New Version             |
| ---------------------------------------- | ------------ | ----------------------- |
| org.apache.activemq:*                    | Artemis      | 2.44.0                  |
| org.apache.commons:commons-lang3         | Commons Lang | 3.19.0                  |
| org.glassfish.jersey.*                   | Jersey       | 3.1.11                  |
| org.apache.logging.log4j:*               | Log4J        | 2.25.1                  |
| io.netty:*                               | netty        | 4.1.128.Final           |
| io.netty:netty-tcnative-boringssl-static | tcnative     | 2.0.74.Final            |
