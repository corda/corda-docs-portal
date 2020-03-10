---
aliases:
- /releases/4.3/index.html
- /index.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3: {}
  versions:
    weight: 157
project: corda-enterprise
section_menu: corda-enterprise-4-3
title: Corda Enterprise 4.3
version: '4.3'
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

{{< note >}}
You can read this site offline by [downloading the PDF](_static/corda-developer-site.pdf).

{{< /note >}}

Corda Enterprise is binary compatible with apps developed for the open source node. This docsite is intended for
administrators and advanced users who wish to learn how to install and configure an enterprise deployment. For
application development please continue to refer to [the main project documentation website](https://docs.corda.net/).

{{< note >}}
Corda Enterprise provides platform API version 4, which matches the API available in open source Corda 4.x releases.

{{< /note >}}



* [Release notes](release-notes-enterprise.md)
    * [Corda Enterprise 4.3.1](release-notes-enterprise.md#corda-enterprise-4-3-1)
        * [Issues Fixed](release-notes-enterprise.md#issues-fixed)


    * [Corda Enterprise 4.3](release-notes-enterprise.md#corda-enterprise-4-3)
        * [Key new features and components](release-notes-enterprise.md#key-new-features-and-components)
            * [Corda Health Survey](release-notes-enterprise.md#corda-health-survey)
            * [JPA notary interface](release-notes-enterprise.md#jpa-notary-interface)
            * [Notary key storage](release-notes-enterprise.md#notary-key-storage)
            * [Support for Metering](release-notes-enterprise.md#support-for-metering)
            * [Hardware Security Module (HSM) improvements](release-notes-enterprise.md#hardware-security-module-hsm-improvements)
            * [Improved database migration tooling](release-notes-enterprise.md#improved-database-migration-tooling)
            * [Corda Firewall Improvements](release-notes-enterprise.md#corda-firewall-improvements)
            * [Support for PostgreSQL 10.10 and 11.5](release-notes-enterprise.md#support-for-postgresql-10-10-and-11-5)
            * [Optimisation of heap memory sizing](release-notes-enterprise.md#optimisation-of-heap-memory-sizing)


        * [Deprecations](release-notes-enterprise.md#deprecations)
        * [Known issues](release-notes-enterprise.md#known-issues)
        * [Upgrade notes](release-notes-enterprise.md#upgrade-notes)




* [Upgrading CorDapps to Corda Enterprise 4.3](app-upgrade-notes-enterprise.md)
    * [Upgrading from Open Source](app-upgrade-notes-enterprise.md#upgrading-from-open-source)
        * [Running on Corda Enterprise 4.3](app-upgrade-notes-enterprise.md#running-on-release)
        * [Re-compiling for Corda Enterprise 4.3](app-upgrade-notes-enterprise.md#re-compiling-for-release)


    * [Upgrading from Enterprise 3.x](app-upgrade-notes-enterprise.md#upgrading-from-enterprise-3-x)
        * [Example](app-upgrade-notes-enterprise.md#example)




* [Upgrading your node to Corda 4](node-upgrade-notes.md)
    * [Step 1. Drain the node](node-upgrade-notes.md#step-1-drain-the-node)
    * [Step 2. Make a backup of your node directories and database](node-upgrade-notes.md#step-2-make-a-backup-of-your-node-directories-and-database)
    * [Step 3. Update database](node-upgrade-notes.md#step-3-update-database)
        * [3.1. Configure the Database Management Tool](node-upgrade-notes.md#configure-the-database-management-tool)
            * [Azure SQL](node-upgrade-notes.md#azure-sql)
            * [SQL Server](node-upgrade-notes.md#sql-server)
            * [Oracle](node-upgrade-notes.md#oracle)
            * [PostgreSQL](node-upgrade-notes.md#postgresql)


        * [3.2. Extract DDL script using Database Management Tool](node-upgrade-notes.md#extract-ddl-script-using-database-management-tool)
        * [3.3. Apply DDL scripts on a database](node-upgrade-notes.md#apply-ddl-scripts-on-a-database)
        * [3.4. Apply data updates on a database](node-upgrade-notes.md#apply-data-updates-on-a-database)


    * [Step 4. Replace `corda.jar` with the new version](node-upgrade-notes.md#step-4-replace-corda-jar-with-the-new-version)
    * [Step 5. Start up the node](node-upgrade-notes.md#step-5-start-up-the-node)
    * [Step 6. Undrain the node](node-upgrade-notes.md#step-6-undrain-the-node)


* [Corda and Corda Enterprise compatibility](version-compatibility.md)
* [Platform support matrix](platform-support-matrix.md)
    * [JDK support](platform-support-matrix.md#jdk-support)
    * [Operating systems supported in production](platform-support-matrix.md#operating-systems-supported-in-production)
    * [Operating systems supported in development](platform-support-matrix.md#operating-systems-supported-in-development)
    * [Node databases](platform-support-matrix.md#node-databases)
    * [MySQL notary databases](platform-support-matrix.md#mysql-notary-databases)
    * [JPA notary databases](platform-support-matrix.md#jpa-notary-databases)
    * [Hardware Security Modules (HSM)](platform-support-matrix.md#hardware-security-modules-hsm)


* [Cheat sheet](cheat-sheet.md)




Corda API

* [API: Contracts](api-contracts.md)
* [API: Contract Constraints](api-contract-constraints.md)
* [API: Core types](api-core-types.md)
* [API: Flows](api-flows.md)
* [API: Identity](api-identity.md)
* [API: Persistence](api-persistence.md)
* [API: RPC operations](api-rpc.md)
* [API: Service Classes](api-service-classes.md)
* [API: ServiceHub](api-service-hub.md)
* [API: States](api-states.md)
* [API: Testing](api-testing.md)
* [API: Transactions](api-transactions.md)
* [API: Vault Query](api-vault-query.md)




