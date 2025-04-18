---
description: "Learn how to create a new version of a Corda-deployed CorDapp to upgrade your CorDapp to fix bugs, create new functionality, or change existing functionality."
date: '2023-05-18'
title: "Creating a New Version of a CorDapp"
menu:
  corda51:
    identifier: corda51-upgrading
    parent: corda51-develop
    weight: 9000
---

# Creating a New Version of a CorDapp

This section describes how to create a new version of a Corda-deployed {{< tooltip >}}CorDapp{{< /tooltip >}}. You must do this in such a way that Corda can recognize the upgrade as a new version of the same application. Typically, you might want to upgrade your CorDapp to fix bugs, create new functionality, or change existing functionality.

Corda must be able to interpret that the two versions are considered the same application. This maintains continuity of any state it has preserved internally relating to that application's operation.

This section contains the following:

* [CorDapp Upgrade Overview](#cordapp-upgrade-overview)
* [Identifying CorDapps Across Versions](#identifying-cordapps-across-versions)

{{< note >}}
The scope of this topic does not include migrating application data persisted by any of the Corda persistence APIs. Nor does it include ensuring that different versions of flow implementations are compatible with one another.
{{< /note >}}

## CorDapp Upgrade Overview

The following users are involved in upgrading a Corda-deployed CorDapp:

1. **CorDapp Developer**: makes the required changes to the code and creates a new {{< tooltip >}}CPK{{< /tooltip >}}, ensuring that the CPK is [identifiable across versions](#identifying-cordapps-across-versions). The CorDapp Developer [builds a CPB]({{< relref "../../developing-applications/packaging/cpb.md" >}}) from the CPK files to enable the Network Operator to create a CPI.
2. **Network Operator**: [creates the new CPI]({{< relref "../../application-networks/cpi/_index.md" >}}), incrementing the `--cpi-version`.
3. **Cluster Administrator**: [uploads the new CPI]({{< relref "../../deploying-operating/vnodes/upgrade-cpi.md" >}}) to the virtual nodes.

## Identifying CorDapps Across Versions

{{< tooltip >}}CPKs{{< /tooltip >}} are identified across versions by the value of their `Corda CPK CorDapp Name` metadata field. Keeping the same value for `Corda CPK CorDapp Name` while making other changes to the CPK indicates to Corda that you consider the CPK to be a new version of the same CPK. As well as the value of  `Corda CPK CorDapp Name`, the set of CPK signers must also be kept the same across versions.

Any data internally serialized by Corda is tagged with both `Corda CPK CorDapp Name` and the set of signers that signed the CPK. On deserialization, the tag is checked against the current version of the CPK’s `Corda CPK CorDapp Name` and set of signers. If both of these match, Corda considers this data as deserializable for the CPK.
