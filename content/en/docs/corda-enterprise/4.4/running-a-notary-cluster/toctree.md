---
title: "Corda Enterprise notary services"
date: 2020-01-08T09:59:25Z
---


# Corda Enterprise notary services
This section contains information on deploying and operating Corda Enterprise notary services,
            including in a highly-available configuration.


* [Corda Enterprise notary service overview]({{< relref "ha-notary-service-overview" >}})
    * [Notary implementations]({{< relref "ha-notary-service-overview#notary-implementations" >}})

    * [Notary configuration]({{< relref "ha-notary-service-overview#notary-configuration" >}})

    * [Legal names and identities]({{< relref "ha-notary-service-overview#legal-names-and-identities" >}})

    * [Keys and certificates]({{< relref "ha-notary-service-overview#keys-and-certificates" >}})

    * [Expected data volume]({{< relref "ha-notary-service-overview#expected-data-volume" >}})


* [Corda Enterprise HA notary service set-up]({{< relref "ha-notary-service-setup" >}})
    * [Prerequisites]({{< relref "ha-notary-service-setup#prerequisites" >}})

    * [HA Notary registration process]({{< relref "ha-notary-service-setup#ha-notary-registration-process" >}})


* [Configuring the notary backend - JPA]({{< relref "installing-jpa" >}})
    * [Supported databases for highly available mode]({{< relref "installing-jpa#supported-databases-for-highly-available-mode" >}})

    * [Database Tables]({{< relref "installing-jpa#database-tables" >}})

    * [Configuring the notary backend - CockroachDB]({{< relref "installing-jpa#configuring-the-notary-backend-cockroachdb" >}})

    * [Configuring notary backend - Oracle RAC 12cR2]({{< relref "installing-jpa#configuring-notary-backend-oracle-rac-12cr2" >}})


* [Configuring the notary backend - MySQL notary]({{< relref "installing-percona" >}})
    * [MySQL driver]({{< relref "installing-percona#mysql-driver" >}})

    * [Networking]({{< relref "installing-percona#networking" >}})

    * [Setup]({{< relref "installing-percona#setup" >}})

    * [Installation]({{< relref "installing-percona#installation" >}})

    * [Configuration]({{< relref "installing-percona#configuration" >}})


* [Highly available database setup guidelines]({{< relref "db-guidelines" >}})
    * [Consistency over availability]({{< relref "db-guidelines#consistency-over-availability" >}})

    * [Synchronous replication]({{< relref "db-guidelines#synchronous-replication" >}})

    * [Impact of latency on performance]({{< relref "db-guidelines#impact-of-latency-on-performance" >}})

    * [Transaction isolation]({{< relref "db-guidelines#transaction-isolation" >}})


* [Configuring the notary worker nodes]({{< relref "installing-the-notary-service" >}})
    * [MySQL notary (deprecated)]({{< relref "installing-the-notary-service#mysql-notary-deprecated" >}})

    * [Configuration Obfuscation]({{< relref "installing-the-notary-service#configuration-obfuscation" >}})

    * [Obtaining the notary service identity]({{< relref "installing-the-notary-service#obtaining-the-notary-service-identity" >}})


* [Joining a bootstrapped network]({{< relref "installing-the-notary-service-bootstrapper" >}})
    * [Expected Outcome]({{< relref "installing-the-notary-service-bootstrapper#expected-outcome" >}})


* [Upgrading the notary to a new version of Corda Enterprise]({{< relref "upgrading-the-ha-notary-service" >}})
    * [Version 4.3]({{< relref "upgrading-the-ha-notary-service#version-4-3" >}})

    * [Version 4.2]({{< relref "upgrading-the-ha-notary-service#version-4-2" >}})

    * [Version 4.0]({{< relref "upgrading-the-ha-notary-service#version-4-0" >}})


* [Highly-available notary backup and restore]({{< relref "backup-restore" >}})

* [Notary database migration]({{< relref "notary-db-migration" >}})
    * [When to migrate]({{< relref "notary-db-migration#when-to-migrate" >}})

    * [Migration steps]({{< relref "notary-db-migration#migration-steps" >}})


* [Notary worker migration]({{< relref "machine-migration" >}})

* [Highly-available notary metrics]({{< relref "notary-metrics" >}})
    * [Available metrics]({{< relref "notary-metrics#available-metrics" >}})

    * [Notary monitoring recommendations]({{< relref "notary-metrics#notary-monitoring-recommendations" >}})


* [Behaviour Under Excessive Load]({{< relref "notary-load-handling" >}})
    * [Flow Engine Behaviour]({{< relref "notary-load-handling#flow-engine-behaviour" >}})

    * [Artemis Messaging Layer Behaviour]({{< relref "notary-load-handling#artemis-messaging-layer-behaviour" >}})


* [Notary sizing considerations]({{< relref "notary-sizing" >}})
    * [Notary disk space requirements]({{< relref "notary-sizing#notary-disk-space-requirements" >}})

    * [Notary performance considerations]({{< relref "notary-sizing#notary-performance-considerations" >}})


* [Notary HSM support]({{< relref "hsm-support" >}})
    * [Overview]({{< relref "hsm-support#overview" >}})

    * [Detailed instructions to deploy to Azure Key Vault]({{< relref "hsm-support#detailed-instructions-to-deploy-to-azure-key-vault" >}})

    * [Using Multiple HSMs]({{< relref "hsm-support#using-multiple-hsms" >}})


* [Handling flag days]({{< relref "handling-flag-days" >}})
    * [Consequences of flag days for the notary]({{< relref "handling-flag-days#consequences-of-flag-days-for-the-notary" >}})

    * [Single notary]({{< relref "handling-flag-days#single-notary" >}})

    * [HA notary cluster]({{< relref "handling-flag-days#ha-notary-cluster" >}})


* [Frequently-Asked-Questions]({{< relref "faq/toctree" >}})
    * [ETA Mechanism Overview]({{< relref "faq/eta-mechanism" >}})

    * [Notary Load Balancing]({{< relref "faq/notary-load-balancing" >}})

    * [Notary Failover]({{< relref "faq/notary-failover" >}})




