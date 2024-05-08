---
date: '2024-05-07'
menu:
  corda-enterprise-4-12:
    identifier: "corda-enterprise-4-12-upgrade-guide"
    parent: corda-enterprise-4-12-upgrading-menu
tags:
- upgrading
- node
- upgrade
- cordapps
title: Corda Enterprise Edition 4.12 upgrade guide
weight: 8
---

# Corda Enterprise Edition 4.12 upgrade guide

This upgrade guide outlines the steps for migrating your Corda 4.11 node to version 4.12 while maintaining backwards compatibility with earlier Corda 4 versions.

{{< note >}}
The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 and below, you must upgrade them to 4.11 first. To do that, consult the relevant upgrade documentation.
{{< /note >}}

### Background

Corda 12 uses upgraded versions of Kotlin 1.9 and Java 17. When designing Corda 4.12, we tackled the issue of having a backchain of transactions verified using Kotlin 1.2 and Java 8 by the earlier versions of Corda.

If a Corda 4.12 node were to be part of a network of mixed Corda 4.x versions, a Corda 4.12 node would not be able to verify a contract verified by an earlier Corda node compiled using Kotlin 1.2. Similarly, an earlier version of Corda node would not be able to verify a new Corda 4.12 contract that was using Kotlin 1.9.

### The solution

To address verification issues, both earlier versions of Corda 4.x and Corda 4.12 had to have a way of verifying the correct contract attachment, depending on the Corda version. This is where the External Verifier, a component of Corda 4.12, comes in.

The External Verifier is an external process started by Corda 4.12, running Kotlin 1.2 (with Java 17). This enables Corda 4.12 to run independently of Java 8. Whenever Corda 4.12 detects an old contract version, it externally verifies this contract within the External Verifier process.

When upgrading to Corda 4.12, the old contract CorDapp JAR is preserved and relocated to a new directory named `legacy-contracts`. This directory is essential as it provides the legacy contract for Corda 4.12 nodes to maintain backward compatibility, as required by the External Verifier.

To ensure compatibility of all existing transactions in the node’s backchain with the External Verifier, and consequently with Corda 4.12, a new utility tool has been introduced: the Transaction Validator Utility. This tool runs the External Verifier on the existing backchain as a sanity check.

{{< figure alt="Corda 4.12 vs Corda 4.11" zoom="/resources/corda412vs411.png" >}}

## Upgrade scenarios

This section describes three possible upgrade paths to a network operating on Corda 4.12. In these scenarios a network is a collection of Corda nodes that are all running the same CorDapp.

All scenarios involving the upgrade of existing node versions from a previous version of Corda 4.x to Corda 4.12 assume the existence of 4.11 (or earlier) transactions in the node’s backchain.

### Upgrading selected network nodes to 4.12

In this scenario, you have a mixed network where only selected nodes are upgraded to Corda 4.12, while others remain on previous versions of Corda 4.x. This scenario requires you to perform the following actions:
* Upgrade any existing CorDapps to run on Java 17 and Kotlin 1.9.
* Keep a copy of the old CorDapp contract JAR file in the new `legacy-contracts` folder placed inside all upgraded 4.12 nodes.

Any future Corda 4.12 nodes added to the network will also require the `legacy-contracts` folder, unless all nodes have been updated by that time. In the latter case, you are adding new Corda 4.12 nodes to a non-mixed network and this requirement is unnecessary.

### Upgrading all network nodes to 4.12

In this scenario, you are creating a non-mixed network a non-mixed network composed solely of nodes operating on Corda 4.12. Transactions occurring within this newly-upgraded network have only the 4.12 contract component group and therefore, you do not need the `legacy-contracts` folder. This is because nodes trust existing old contract attachments if the new CorDapp locally installed on the node is signed by the same key. However, it is still important that you keep a copy of the old contract JAR for reference.

If any new Corda 4.12 nodes are added to this network in the future, a problem arises wherein nodes won’t trust old contract attachments. For example, this happens if a new transaction contains a backchain of old Corda 4.x transactions. For this reason, you need to upload the old contract JAR needs via RPC to the new node, ensuring it trusts the old contract version.

### Adding 4.12 nodes to a new network

This scenario is the simplest, as it does not require any complex update procedures. In this scenario, all CorDapps are developed for Java 17 and Kotlin 1.9, and the process for adding new nodes is the same as setting up a new network of any previous Corda version.
