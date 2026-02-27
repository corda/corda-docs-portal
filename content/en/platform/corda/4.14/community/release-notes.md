---
title: Corda Open Source Edition 4.14 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.ht3
menu:
  corda-community-4-14:
    identifier: corda-community-4-14-release-notes
    parent: about-corda-landing-4-14-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Open Source Edition 4.14 release notes

The Corda Open Source Edition 4.14 release introduces new functionality and third-party component upgrades.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Open Source release notes are on this page, and for the latest upgrade guide, refer to [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) and [Upgrading your node]({{< relref "node-upgrade-notes.md" >}}).

## Platform version change

Corda 4.14 uses platform version 160.

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

## New features, enhancements and restrictions

### Notary instructions

Corda 4.14 introduces `NotaryInstruction`, an extensible mechanism for attaching additional directives to a
transaction that a specialised notary can act on during notarisation. Notary instructions are stored in a new
transaction component group (`NOTARY_INSTRUCTIONS_GROUP`), are covered by the transaction's Merkle tree, and are
available to contracts for verification.

New `TransactionBuilder` and `LedgerTransaction` APIs support notary instructions:

* `TransactionBuilder.addNotaryInstruction(instruction)` — attaches a notary instruction to the transaction being
  built.
* `LedgerTransaction.notaryInstructionsOfType<T>()` — retrieves all notary instructions of a given type, allowing
  contracts to verify them.

Standard notaries reject any transaction that contains notary instructions. Only specialised notaries — such as the
[Solana notary]({{< relref "../enterprise/notary/solana-notary.md" >}}) (Enterprise only) — accept and process them.

### Notary change flow

The transaction hierarchy, [FinalityFlow]({{< relref "api-flows.md#finalityflow" >}}), and NotaryChangeFlow have been generalized so that they can be used with NotaryChange transactions as well as with WireTransaction.

### RPC thread pool

The RPC clients ([CordaRPCClient](../../../../../../../en/api-ref/corda/4.14/community/javadoc/net/corda/client/rpc/CordaRPCClient.html), [RPCClient](../../../../../../../en/api-ref/corda/4.14/community/javadoc/net/corda/client/rpc/internal/RPCClient.html), and [MultiRPCClient](../../../../../../../en/api-ref/corda/4.14/community/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html)) can now be configured to use Artemis global thread pools by setting their `useGlobalThreadPools` Boolean parameter to true. This allows multiple connections to share a bounded set of scheduler and worker threads, rather than creating dedicated pools per client.

(For Kotlin Docs, see [CordaRPCClient](../../../../../../../en/api-ref/corda/4.14/community/kotlin/docs/net.corda.client.rpc/-corda-r-p-c-client/index.html), [RPCClient](../../../../../../../en/api-ref/corda/4.14/community/kotlin/docs/net.corda.client.rpc.internal/-r-p-c-client/index.html), and [MultiRPCClient](../../../../../../../en/api-ref/corda/4.14/community/kotlin/docs/net.corda.client.rpc.ext/-multi-r-p-c-client/index.html).

## Third-party component upgrades

The following table lists the dependency version changes for 4.14 Open Source Editions:

| Dependency                                      | Name                    | New Version   |
|-------------------------------------------------|-------------------------|---------------|
| org.apache.activemq:*                           | Apache ActiveMQ Artemis | 2.44.0        |
| com.azure:azure-identity:*                      | Azure Identity          | 1.18.1        |
| org.apache.commons:commons-lang3                | Commons Lang            | 3.19.0        |
| org.glassfish.jersey.*                          | Jersey                  | 3.1.11        |
| org.apache.logging.log4j:*                      | Log4j                   | 2.25.1        |
| io.netty:*                                      | Netty                   | 4.1.128.Final |
| io.netty:netty-tcnative-boringssl-static        | Netty TCNative          | 2.0.74.Final  |
| org.apache.qpid:proton-j                        | ProtonJ                 | 0.34.1        |

