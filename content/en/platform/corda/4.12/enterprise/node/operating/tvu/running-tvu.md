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

This section describes the requirements to run the Transaction Validator Utility (TVU) to verify a pre-4.12 database of transactions. Please read this section in conjunction with [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "../../../upgrade-guide.md" >}}) which describes the upgrade process in more detail.

{{< important >}}
The 4.12 version of TVU is compatible only with 4.11 and 4.12 database schemas. To verify transactions on a pre-4.11 database, you must first upgrade the database to version 4.11. 
{{</ important >}}

You must run the TVU in the same environment as a 4.12 node, in terms of `cordapps` and `legacy-jars` folders, with the exception that the database it connects to is the 4.11 database being checked. Note that you do not need to create a `legacy-contracts` folder when running the TVU. The TVU will extract what it needs from the database. Before performing the following steps, ensure everything is backed up, as changes will be made to folders as described below.

1. Place the TVU JAR in your Corda 4.11 node directory.
2. In the `cordapps` directory, remove the existing JARs and replace them with the 4.12 JDK17/Kotlin 1.9 equivalent JARs.
3. If needed, create a `legacy-jars` directory, then copy the third-party dependencies and any JARs you were dependent upon from the `drivers` directory to the `legacy-jars` directory . See [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "../../../upgrade-guide.md" >}}) for details.

You can now run the TVU using the command lines described in the [TVU CLI parameters]({{< relref "tvu-cli.md" >}}) section.
