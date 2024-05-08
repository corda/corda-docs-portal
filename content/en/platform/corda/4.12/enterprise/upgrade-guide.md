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

{{< figure alt="basic tx" width=80% zoom="/en/images/corda412vs411.png" >}}
