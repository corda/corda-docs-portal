---
aliases:
- /releases/4.3/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: -230
project: corda-enterprise
section_menu: corda-enterprise-4-3
title: Corda Enterprise 4.3
version: 4.3
---


# Corda Enterprise 4.3

Welcome to the documentation website for Corda Enterprise 4.3, based on the Corda 4.0 open source release.

Corda Enterprise 4.3 builds on the performance, scalability, high-availability, enhanced DMZ security, and multiple database vendor support
introduced in Corda Enterprise 3.0 with the following important new additions:


* **Multiple nodes behind a single firewall**:
multi-tenancy of Corda Firewall (float and bridge) components enables multiple Corda nodes to multiplex all remote peer-to-peer message traffic
through a single Corda Firewall.
* **Hardware Security Module (HSM) support**:
for Node CA and Legal Identity signing keys in hardware security modules provides increased security.
This release includes full integration with Azure Key Vault, Gemalto Luna and Utimaco HSM devices.
* **High Availability improvements**:
this release builds on the Hot-Cold High Availability configuration available in Corda Enterprise 3.x with improved deployment
configurations to simplify operational management and reduce overall VM footprint.
* **Operational Deployment improvements**:
introduces improvements that optimize larger scale deployments, reduce the cost of infrastructure, and minimize the operational complexity
of multi-node hosting.
* **Performance Test Suite for benchmarking**:
a toolkit to allow customers to test and validate Corda for their infrastructure performance and determine whether or not improvements are needed
before going live.

Corda Enterprise 4.3 also includes the new features of Corda 4, notably:


* **Reference input states**:
these allow smart contracts to read data from the ledger without simultaneously updating it.
* **State pointers**:
these work together with the reference states feature to make it easy for data to point to the latest version of any other piece of data
on the ledger by `StateRef` or linear ID.
* **Signature constraints**:
facilitate upgrading CorDapps in a secure manner using standard public key signing mechanisms and controls.
* **Security upgrades** to include:
    * Sealed JARs are a security upgrade that ensures JARs cannot define classes in each other’s packages, thus ensuring Java’s package-private
visibility feature works.
    * `@BelongsToContract` annotation: allows annotating states with which contract governs them.
    * Two-sided `FinalityFlow` and `SwapIdentitiesFlow` to prevent nodes accepting any finalised transaction, outside of the context of a containing flow.
    * Package namespace ownership: allows app developers to register their keys and Java package namespaces
with the zone operator. Any JAR that defines classes in these namespaces will have to be signed by those keys.


* **Versioning**:
applications can now specify a **target version** in their JAR manifest that declares which version of the platform the app was tested against.
They can also specify a **minimum platform version** which specifies the minimum version a node must be running on
to allow the app to start using new features and APIs of that version.

You can learn more about all new features in the [Enterprise](release-notes-enterprise.md) and [Open Source](release-notes.md) release notes.

Corda Enterprise is binary compatible with apps developed for the open source node. This docsite is intended for
administrators and advanced users who wish to learn how to install and configure an enterprise deployment. For
application development please continue to refer to [the main project documentation website](https://docs.corda.net/).

{{< note >}}
Corda Enterprise provides platform API version 4, which matches the API available in open source Corda 4.x releases.

{{< /note >}}
