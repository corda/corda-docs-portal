---
title: "Corda Enterprise 4.3"
date: 2020-01-08T09:59:25Z
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


You can learn more about all new features in the [Enterprise]({{< relref "release-notes-enterprise" >}}) and [Open Source]({{< relref "release-notes" >}}) release notes.


{{< note >}}
You can read this site offline by [downloading the PDF](_static/corda-developer-site.pdf).


{{< /note >}}
Corda Enterprise is binary compatible with apps developed for the open source node. This docsite is intended for
            administrators and advanced users who wish to learn how to install and configure an enterprise deployment. For
            application development please continue to refer to [the main project documentation website](https://docs.corda.net/).


{{< note >}}
Corda Enterprise provides platform API version 4, which matches the API available in open source Corda 4.x releases.


{{< /note >}}

* [Release notes]({{< relref "release-notes-enterprise" >}})
    * [Corda Enterprise 4.3]({{< relref "release-notes-enterprise#release" >}})
        * [Key new features and components]({{< relref "release-notes-enterprise#key-new-features-and-components" >}})
            * [Corda Health Survey]({{< relref "release-notes-enterprise#corda-health-survey" >}})

            * [JPA notary interface]({{< relref "release-notes-enterprise#jpa-notary-interface" >}})

            * [Notary key storage]({{< relref "release-notes-enterprise#notary-key-storage" >}})

            * [Support for Metering]({{< relref "release-notes-enterprise#support-for-metering" >}})

            * [Hardware Security Module (HSM) improvements]({{< relref "release-notes-enterprise#hardware-security-module-hsm-improvements" >}})

            * [Improved database migration tooling]({{< relref "release-notes-enterprise#improved-database-migration-tooling" >}})

            * [Corda Firewall Improvements]({{< relref "release-notes-enterprise#corda-firewall-improvements" >}})

            * [Support for PostgreSQL 10.10 and 11.5]({{< relref "release-notes-enterprise#support-for-postgresql-10-10-and-11-5" >}})

            * [Optimisation of heap memory sizing]({{< relref "release-notes-enterprise#optimisation-of-heap-memory-sizing" >}})


        * [Deprecations]({{< relref "release-notes-enterprise#deprecations" >}})

        * [Known issues]({{< relref "release-notes-enterprise#known-issues" >}})

        * [Upgrade notes]({{< relref "release-notes-enterprise#upgrade-notes" >}})



* [Upgrading CorDapps to Corda Enterprise 4.3]({{< relref "app-upgrade-notes-enterprise" >}})
    * [Upgrading from Open Source]({{< relref "app-upgrade-notes-enterprise#upgrading-from-open-source" >}})
        * [Running on Corda Enterprise 4.3]({{< relref "app-upgrade-notes-enterprise#running-on-release" >}})

        * [Re-compiling for Corda Enterprise 4.3]({{< relref "app-upgrade-notes-enterprise#re-compiling-for-release" >}})


    * [Upgrading from Enterprise 3.x]({{< relref "app-upgrade-notes-enterprise#upgrading-from-enterprise-3-x" >}})
        * [Example]({{< relref "app-upgrade-notes-enterprise#example" >}})



* [Upgrading your node to Corda 4]({{< relref "node-upgrade-notes" >}})
    * [Step 1. Drain the node]({{< relref "node-upgrade-notes#step-1-drain-the-node" >}})

    * [Step 2. Make a backup of your node directories and database]({{< relref "node-upgrade-notes#step-2-make-a-backup-of-your-node-directories-and-database" >}})

    * [Step 3. Update database]({{< relref "node-upgrade-notes#step-3-update-database" >}})
        * [3.1. Configure the Database Management Tool]({{< relref "node-upgrade-notes#configure-the-database-management-tool" >}})
            * [Azure SQL]({{< relref "node-upgrade-notes#azure-sql" >}})

            * [SQL Server]({{< relref "node-upgrade-notes#sql-server" >}})

            * [Oracle]({{< relref "node-upgrade-notes#oracle" >}})

            * [PostgreSQL]({{< relref "node-upgrade-notes#postgresql" >}})


        * [3.2. Extract DDL script using Database Management Tool]({{< relref "node-upgrade-notes#extract-ddl-script-using-database-management-tool" >}})

        * [3.3. Apply DDL scripts on a database]({{< relref "node-upgrade-notes#apply-ddl-scripts-on-a-database" >}})

        * [3.4. Apply data updates on a database]({{< relref "node-upgrade-notes#apply-data-updates-on-a-database" >}})


    * [Step 4. Replace `corda.jar` with the new version]({{< relref "node-upgrade-notes#step-4-replace-corda-jar-with-the-new-version" >}})

    * [Step 5. Start up the node]({{< relref "node-upgrade-notes#step-5-start-up-the-node" >}})

    * [Step 6. Undrain the node]({{< relref "node-upgrade-notes#step-6-undrain-the-node" >}})


* [Corda and Corda Enterprise compatibility]({{< relref "version-compatibility" >}})

* [Platform support matrix]({{< relref "platform-support-matrix" >}})
    * [JDK support]({{< relref "platform-support-matrix#jdk-support" >}})

    * [Operating systems supported in production]({{< relref "platform-support-matrix#operating-systems-supported-in-production" >}})

    * [Operating systems supported in development]({{< relref "platform-support-matrix#operating-systems-supported-in-development" >}})

    * [Node databases]({{< relref "platform-support-matrix#node-databases" >}})

    * [MySQL notary databases]({{< relref "platform-support-matrix#mysql-notary-databases" >}})

    * [JPA notary databases]({{< relref "platform-support-matrix#jpa-notary-databases" >}})

    * [Hardware Security Modules (HSM)]({{< relref "platform-support-matrix#hardware-security-modules-hsm" >}})


* [Cheat sheet]({{< relref "cheat-sheet" >}})



Corda API
* [API: Contracts]({{< relref "api-contracts" >}})

* [API: Contract Constraints]({{< relref "api-contract-constraints" >}})

* [API: Core types]({{< relref "api-core-types" >}})

* [API: Flows]({{< relref "api-flows" >}})

* [API: Identity]({{< relref "api-identity" >}})

* [API: Persistence]({{< relref "api-persistence" >}})

* [API: RPC operations]({{< relref "api-rpc" >}})

* [API: Service Classes]({{< relref "api-service-classes" >}})

* [API: ServiceHub]({{< relref "api-service-hub" >}})

* [API: States]({{< relref "api-states" >}})

* [API: Testing]({{< relref "api-testing" >}})

* [API: Transactions]({{< relref "api-transactions" >}})

* [API: Vault Query]({{< relref "api-vault-query" >}})



