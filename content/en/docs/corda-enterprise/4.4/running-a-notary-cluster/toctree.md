---
aliases:
- /releases/4.4/running-a-notary-cluster/toctree.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-corda-enterprise
title: Corda Enterprise notary services
---


# Corda Enterprise notary services

This section contains information on deploying and operating Corda Enterprise notary services,
including in a highly-available configuration.



* [Corda Enterprise notary service overview](ha-notary-service-overview.md)
    * [Notary high-availability mode](ha-notary-service-overview.md#notary-high-availability-mode)
    * [Notary configuration](ha-notary-service-overview.md#notary-configuration)
    * [Legal names and identities](ha-notary-service-overview.md#legal-names-and-identities)
    * [Keys and certificates](ha-notary-service-overview.md#keys-and-certificates)
    * [Expected data volume](ha-notary-service-overview.md#expected-data-volume)


* [Corda Enterprise HA notary service set-up](ha-notary-service-setup.md)
    * [Prerequisites](ha-notary-service-setup.md#prerequisites)
    * [HA Notary registration process](ha-notary-service-setup.md#ha-notary-registration-process)


* [Configuring the notary backend - JPA](installing-jpa.md)
    * [Supported databases for highly available mode](installing-jpa.md#supported-databases-for-highly-available-mode)
    * [Database Tables](installing-jpa.md#database-tables)
    * [Configuring the notary backend - CockroachDB](installing-jpa.md#configuring-the-notary-backend-cockroachdb)
    * [Configuring notary backend - Oracle RAC 12cR2](installing-jpa.md#configuring-notary-backend-oracle-rac-12cr2)


* [Configuring the notary backend - MySQL notary](installing-percona.md)
    * [MySQL driver](installing-percona.md#mysql-driver)
    * [Networking](installing-percona.md#networking)
    * [Setup](installing-percona.md#setup)
    * [Installation](installing-percona.md#installation)
    * [Configuration](installing-percona.md#configuration)


* [Highly available database setup guidelines](db-guidelines.md)
    * [Consistency over availability](db-guidelines.md#consistency-over-availability)
    * [Synchronous replication](db-guidelines.md#synchronous-replication)
    * [Impact of latency on performance](db-guidelines.md#impact-of-latency-on-performance)
    * [Transaction isolation](db-guidelines.md#transaction-isolation)


* [Configuring the notary worker nodes](installing-the-notary-service.md)
    * [MySQL notary (deprecated)](installing-the-notary-service.md#mysql-notary-deprecated)
    * [Configuration Obfuscation](installing-the-notary-service.md#configuration-obfuscation)
    * [Obtaining the notary service identity](installing-the-notary-service.md#obtaining-the-notary-service-identity)


* [Joining a bootstrapped network](installing-the-notary-service-bootstrapper.md)
    * [Expected Outcome](installing-the-notary-service-bootstrapper.md#expected-outcome)


* [Upgrading the notary to a new version of Corda Enterprise](upgrading-the-ha-notary-service.md)
    * [Version 4.4](upgrading-the-ha-notary-service.md#version-4-4)
    * [Version 4.2](upgrading-the-ha-notary-service.md#version-4-2)
    * [Version 4.0](upgrading-the-ha-notary-service.md#version-4-0)


* [Highly-available notary backup and restore](backup-restore.md)
* [Notary database migration](notary-db-migration.md)
    * [When to migrate](notary-db-migration.md#when-to-migrate)
    * [Migration steps](notary-db-migration.md#migration-steps)


* [Notary worker migration](machine-migration.md)
* [Highly-available notary metrics](notary-metrics.md)
    * [Available metrics](notary-metrics.md#available-metrics)
    * [Notary monitoring recommendations](notary-metrics.md#notary-monitoring-recommendations)


* [Behaviour Under Excessive Load](notary-load-handling.md)
    * [Flow Engine Behaviour](notary-load-handling.md#flow-engine-behaviour)
    * [Artemis Messaging Layer Behaviour](notary-load-handling.md#artemis-messaging-layer-behaviour)


* [Notary sizing considerations](notary-sizing.md)
    * [Notary disk space requirements](notary-sizing.md#notary-disk-space-requirements)
    * [Notary performance considerations](notary-sizing.md#notary-performance-considerations)


* [Notary HSM support](hsm-support.md)
    * [Overview](hsm-support.md#overview)
    * [Detailed instructions to deploy to Azure Key Vault](hsm-support.md#detailed-instructions-to-deploy-to-azure-key-vault)
    * [Using Multiple HSMs](hsm-support.md#using-multiple-hsms)


* [Handling flag days](handling-flag-days.md)
    * [Consequences of flag days for the notary](handling-flag-days.md#consequences-of-flag-days-for-the-notary)
    * [Single notary](handling-flag-days.md#single-notary)
    * [HA notary cluster](handling-flag-days.md#ha-notary-cluster)


* [Frequently-Asked-Questions](faq/toctree.md)
    * [ETA Mechanism Overview](faq/eta-mechanism.md)
    * [Notary Load Balancing](faq/notary-load-balancing.md)
    * [Notary Failover](faq/notary-failover.md)





