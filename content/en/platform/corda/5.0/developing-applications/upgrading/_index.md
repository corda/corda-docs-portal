---
date: '2023-05-18'
title: "Upgrading CorDapps"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-upgrading
    parent: corda5-develop
    weight: 9000
section_menu: corda5

---

# Upgrading CorDapps

This topic describes how to upgrade a Corda-deployed CorDapp to a newer version. This must be done in such a way that Corda will interpret the upgrade as a new version of the same application. Typically you might want to upgrade your CorDapp to fix bugs, create new functionality, or change existing functionality. 

Corda must be able to interpret that the two versions are considered to be the same application. This is done in order to maintain continuity of any state it has preserved internally relating to that application's operation.

Note that the scope of this topic does not include migrating application data persisted by any of the Corda persistence APIs. Nor does it include ensuring that different versions of flow implementations are compatible with one another.

## Identifying CorDapps Across Versions

Corda packages (CPKs) are identified across versions by the value of their `Corda CPK CorDapp Name` metadata field. Keeping the same value for `Corda CPK CorDapp Name` while making other changes to the CPK indicates to Corda that you consider the CPK to be a new version of the same CPK. As well as the value of  `Corda CPK CorDapp Name`, the set of CPK signers must also be kept the same across versions.

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