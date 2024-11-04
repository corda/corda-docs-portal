---
description: "The steps that TVU goes through when verifying pre-4.12 database of transactions."
date: '2024-11-04'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-running-tvu
    parent: corda-enterprise-4-12-tvu
tags:
- tvu
- transaction validator utility
title: Running the TVU
weight: 150
---

# Running the TVU

This section describes the requirements to run the Transaction Validator Utility (TVU) to verify a pre-4.12 database of transactions. Please read this section in conjunction with [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "../../../upgrade-guide.md" >}}) which describes in more detail the upgrade process.

The TVU is compatible only with 4.11 database schemas. To verify transactions on a pre-4.11 database, you must first upgrade the database to version 4.11. You must run the TVU in the same environment as a 4.12 node, in terms of `cordapps`, `legacy-contract`, and `legacy-jar` folders, except that the database it connects to is the 4.11 database being checked. Before performing the following steps, ensure everything is backed up, as changes will be made to folders as described below.

1. Place the TVU JAR in your Corda 4.11 node directory.
2. In the `cordapps` directory, remove the existing JARs and replace them with the 4.12 JDK17/Kotlin 1.9 equivalent JARs.
3. Create a `legacy-contracts` directory that contains the 4.11 contract JARs (the ones that were previously in the `cordapps` directory).
4. If needed, create a `legacy-jars` directory and place into this directory third-party dependencies and any JARs you were dependent upon located in the `drivers` directory. See [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "../../../upgrade-guide.md" >}}) for details.

You can now run the TVU using the command lines described in the [TVU CLI parameters]({{< relref "tvu-cli.md" >}}) section.
