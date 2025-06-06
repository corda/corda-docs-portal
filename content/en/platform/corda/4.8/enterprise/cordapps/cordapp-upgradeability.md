---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-cordapps-versioning
tags:
- cordapp
- upgradeability
title: CorDapp upgradeability guarantees
weight: 5
---

# CorDapp upgradeability guarantees

## Corda 4.0

Corda 4 introduces a number of advanced features (such as signature constraints), and data security model improvements (such as attachments
trust checking and classloader isolation of contract attachments for transaction building and verification).

The following guarantees are made for CorDapps running on Corda 4.0


* Compliant CorDapps compiled with previous versions of Corda (from 3.0) will execute without change on Corda 4.0{{< note >}}
by “compliant”, we mean CorDapps that do not utilise Corda internal, non-stable or other non-committed public Corda APIs.{{< /note >}}
Recommendation: security hardening changes in flow processing, specifically the `FinalityFlow`, recommend upgrading existing CorDapp
receiver flows to use the new APIs and thus opting in to platform version 4. See [Step 5. Security: Upgrade your use of FinalityFlow]({{ relref "../app-upgrade-notes.md#5-improve-the-security-of-your-cordapp-by-upgrading-how-you-use-finalityflow" >}}) for more information.
* All constraint types (hash, CZ whitelisted, signature) are consumable within the same transaction if there is an associated contract attachment that satisfies all of them.
* CorDapp Contract states generated on ledger using hash constraints are not directly migratable to signature constraints in this release.
Your compatibility zone operator may whitelist a JAR previously used to issue hash constrained states, and then you can follow the manual
process described in the paragraph below to migrate these to signature constraints. See [CorDapp constraints migration]({{< relref "cordapp-constraint-migration.md" >}}) for more information.
* CorDapp Contract states generated on ledger using CZ whitelisted constraints are migratable to signature constraints using a manual process
that requires programmatic code changes. See [CZ whitelisted constraints migration]({{< relref "cordapp-constraint-migration.md#migrating-cz-whitelisted-constraints" >}}) for more information.
* Explicit Contract Upgrades are only supported for hash and CZ whitelisted constraint types. See [Performing explicit contract and state upgrades]({{< relref "upgrading-cordapps.md#performing-explicit-contract-and-state-upgrades" >}}) for more information.
* CorDapp contract attachments are not trusted from remote peers over the p2p network for the purpose of transaction verification.
A node operator must locally install *all* versions of a Contract attachment to be able to resolve a chain of contract states from its original version.
The RPC `uploadAttachment` mechanism can be used to achieve this (as well as conventional loading of a CorDapp by installing it in the nodes /cordapp directory).
See [Installing the CorDapp JAR]({{< relref "cordapp-build-systems.md#create-the-cordapp-jar" >}}) and [CorDapp Contract Attachments]({{< relref "cordapp-build-systems.md#cordapp-contract-attachments" >}}) for more information.
* CorDapp contract attachment classloader isolation has some important side-effects and edge cases to consider:
* Contract attachments should include all 3rd party library dependencies in the same packaged JAR - we call this a “Fat JAR”,
meaning that all dependencies are resolvable by the classloader by only loading a single JAR.
* Contract attachments that depend on other Contract attachments from a different packaged JAR are currently supported in so far as the Attachments Classloader
will attempt to resolve any external dependencies from the node’s application classloader. It is thus paramount that dependent Contract
Attachments are loaded upon node startup from the respective /cordapps directory.


* Rolling upgrades are partially supported.
A Node operator may choose to manually upload (via the RPC attachments uploader mechanism) a later version of a Contract Attachment than
the version their node is currently using for the purposes of transaction verification (received from remote peers). However, they will only
be able to build new transactions with the version that is currently loaded (installed from the nodes /cordapps directory) in their node.
* Finance CorDapp (v4)
Whilst experimental, our test coverage has confirmed that states generated with the Finance CorDapp are interchangeable across Open Source
and Enterprise distributions. This has been made possible by releasing a single 4.0 version of the Finance Contracts CorDapp.
Please note the Finance application will be superseded shortly by the new Tokens SDK ([https://github.com/corda/token-sdk](https://github.com/corda/token-sdk))


## Later releases

The following additional capabilities are under consideration for delivery in follow-up releases to Corda 4.0:


* CorDapp Contract states generated on ledger using hash constraints will be automatically migrated to signature constraints when building new transactions
where the latest installed contract Jar is signed as per [CorDapp Jar signing]({{relref "cordapp-build-systems.md#sign-the-cordapp" >}}).
* CorDapp Contract states generated on ledger using CZ whitelisted constraints will be automatically migrated to signature constraints when building new transactions
where the latest installed contract Jar is signed as per [CorDapp Jar signing]({{< relref "cordapp-build-systems.md#sign-the-cordapp" >}}).
* Explicit Contract Upgrades will be supported for all constraint types: hash, CZ whitelisted and signature.
In practice, it should only be necessary to upgrade from hash or CZ whitelisted to new signature constrained contract types.
signature constrained contracts are upgradeable seamlessly (through built in serialization and code signing controls) without requiring explicit upgrades.
* Contract attachments will be able to explicitly declare their dependencies on other Contract attachments such that these are automatically
loaded by the Attachments Classloader (rendering the 4.0 fallback to application classloader mechanism redundant).
This improved modularity removes the need to “Fat JAR” all dependencies together in a single jar.
* Rolling upgrades will be fully supported.
A Node operator will be able to pre-register (by hash or code signing public key) versions of CorDapps they are not yet ready to install locally,
but wish to use for the purposes of transaction verification with peers running later versions of a CorDapp.

{{< note >}}
Trusted downloading and execution of contract attachments from remote peers will not be integrated until secure JVM sand-boxing is available.

{{< /note >}}
