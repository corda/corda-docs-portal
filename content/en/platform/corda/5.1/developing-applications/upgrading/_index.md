---
date: '2023-08-10'
title: "Upgrading CorDapps"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-upgrading
    parent: corda51-develop
    weight: 9000
section_menu: corda51

---

# Upgrading CorDapps

This section describes how to upgrade a Corda-deployed {{< tooltip >}}CorDapp{{< /tooltip >}} to a newer version. This must be done in such a way that Corda can interpret the upgrade as a new version of the same application. Typically you might want to upgrade your CorDapp to fix bugs, create new functionality, or change existing functionality.

Corda must be able to interpret that the two versions are considered to be the same application. This is done in order to maintain continuity of any state it has preserved internally relating to that application's operation.

This section contains the following:

* []
* 
* 

{{< note >}}
The scope of this topic does not include migrating application data persisted by any of the Corda persistence APIs. Nor does it include ensuring that different versions of {{< tooltip >}}flow{{< /tooltip >}} implementations are compatible with one another.
{{< /note >}}

For information about how a Cluster Administrator upgrades the CPI of a virtual node, see [Upgrading a CPI]({{< relref "../../deploying-operating/vnodes/upgrade-cpi.md" >}}).

## Identifying CorDapps Across Versions

{{< tooltip >}}CPKs{{< /tooltip >}} are identified across versions by the value of their `Corda CPK CorDapp Name` metadata field. Keeping the same value for `Corda CPK CorDapp Name` while making other changes to the CPK indicates to Corda that you consider the CPK to be a new version of the same CPK. As well as the value of  `Corda CPK CorDapp Name`, the set of CPK signers must also be kept the same across versions.

Any data internally serialized by Corda is tagged with both `Corda CPK CorDapp Name` and the set of signers that signed the CPK. On deserialization, the tag will be checked against the current version of the CPK’s `Corda CPK CorDapp Name` and set of signers. If both of these match, Corda will consider this data as deserializable for the CPK.

How `Corda CPK CorDapp Name` is set differs between Corda 5.0 and subsequent versions.

## Identifying CorDapps in Corda 5.0

In Corda 5.0, `Corda CPK CorDapp Name` is not configurable, but it is set using the concatenation of the following properties defined by the Corda build system:

* `project.group`
* `archiveBaseName`
* `archiveAppendix`
* `archiveClassifier`

These properties need to remain stable in your application CPK for `Corda CPK CorDapp Name` to remain stable.

`project.group` and `archiveBaseName` are set to a value if not explicitly specified. These  will reflect the name of the Gradle module that your CorDapp sits under. To keep these properties the same across versions, you have two options:

* Explicitly set the properties in your project.

* Manage your software versions so that the properties never change.

For example, the second option is the case if you manage subsequent versions using git branches, so that the application resides in the same git module. This means that you can simply leave these fields and project structure alone in all versions.

## Ledger Implications of Upgrading CorDapps

When upgrading a CorDapp you should consider the following implications for the ledger:

* Contract upgrade
The contract code executed during contract verification of new transactions always uses the
contract of the current CPI. The verification rule for the contract upgrade can be the
different than the previous one. It is important that newer contracts can still verify states
that already exist on the ledger, potentially created with an older version of the contract.
* State upgrade
State upgrades have specific requirements. To ensure smooth functioning across different
versions of states within CPI, it’s essential to serialize states using AMQP serialization.
Default Class Evolution page provides details on how to make your states serializable across
versions. Neglecting this guideline might lead to deserialization issues when attempting to
access states from the vault such as querying with API, getting from transaction and
accessing in contract code.
* Impact on Ledger Service API
The retrieved states from APIs will use the state class of the new version / current CPI.
* Backchain upgrade
The backchain is designed to work seamlessly with transactions from various versions,
ensuring compatibility across different versions.