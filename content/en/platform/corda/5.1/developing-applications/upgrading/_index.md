---
date: '2023-11-20'
title: "Creating a New Version of a CorDapp"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-upgrading
    parent: corda51-develop
    weight: 9000
section_menu: corda51

---

# Creating a New Version of a CorDapp

This section describes how to create a new version of a Corda-deployed {{< tooltip >}}CorDapp{{< /tooltip >}}. This must be done in such a way that Corda can interpret the upgrade as a new version of the same application. Typically you might want to upgrade your CorDapp to fix bugs, create new functionality, or change existing functionality.

Corda must be able to interpret that the two versions are considered to be the same application. This maintains continuity of any state it has preserved internally relating to that application's operation.

This section contains the following:

* []
* 
* 

{{< note >}}
The scope of this topic does not include migrating application data persisted by any of the Corda persistence APIs. Nor does it include ensuring that different versions of {{< tooltip >}}flow{{< /tooltip >}} implementations are compatible with one another.
{{< /note >}}

## CorDapp Upgrade Overview

The following users are involved in upgrading a Corda-deployed CorDapp:

1. **CorDapp Developer**: makes the required changes to the code and [creates a new CPK](), ensuring that the CPK is [identifiable across versions]().
2. **Network Operator**: [creates the new CPI](), incrementing the `--cpi-version`.
3. **Cluster Administrator**: [uploads the new CPI]({{< relref "../../deploying-operating/vnodes/upgrade-cpi.md" >}}) to the virtual nodes.

For information about how a Cluster Administrator upgrades the CPI of a virtual node, see [Upgrading a CPI].

## Identifying CorDapps Across Versions

{{< tooltip >}}CPKs{{< /tooltip >}} are identified across versions by the value of their `Corda CPK CorDapp Name` metadata field. Keeping the same value for `Corda CPK CorDapp Name` while making other changes to the CPK indicates to Corda that you consider the CPK to be a new version of the same CPK. As well as the value of  `Corda CPK CorDapp Name`, the set of CPK signers must also be kept the same across versions.

Any data internally serialized by Corda is tagged with both `Corda CPK CorDapp Name` and the set of signers that signed the CPK. On deserialization, the tag will be checked against the current version of the CPK’s `Corda CPK CorDapp Name` and set of signers. If both of these match, Corda will consider this data as deserializable for the CPK.

How `Corda CPK CorDapp Name` is set differs between Corda 5.0 and subsequent versions.

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