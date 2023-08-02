---
title: "Database Connection Configuration"
version: 'Corda 5.0'
date: '2023-05-16'
menu:
  corda5:
    identifier: corda5-cluster-database
    parent: corda5-cluster-config
    weight: 2000
section_menu: corda5
---

# Database Connection Configuration

Database connection details must be configured differently than the standard dynamic configuration process. This is necessary not only because the details are sensitive but also to maintain operation separation between the different types of workers. For example, the flow worker process should not have access to the database connection details. This section describes how the connection details of the following are maintained:
* [Configuration Database]({{< relref "#configuration-database" >}})
* [All Other Databases]({{< relref "#all-other-databases" >}})

## Configuration Database

<<<<<<< HEAD
The configuration database contains all configuration for the Corda cluster and so the database worker process must be able to connect to this database when it starts. As a result, the connection details for this database must be passed to the database worker process in the [deployment configuration]({{< relref "../deployment/deploying/_index.md#postgresql" >}}).
=======
The configuration database contains all configuration for the Corda {{< tooltip >}}cluster{{< /tooltip >}} and so the database worker process must be able to connect to this database when it starts. As a result, the connection details for this database must be passed to the database worker process in the [deployment configuration]({{< relref "../deployment/deploying/_index.md#postgresql" >}}). 
>>>>>>> main

{{< note >}}
Credentials can be encrypted. See [Configuration Secrets]({{< relref "./secrets.md">}}), for more information.
{{< /note >}}

## All Other Databases

<<<<<<< HEAD
By default, connection details for the RBAC, Crypto, and {{< tooltip >}}virtual node{{< /tooltip >}} databases are stored in the `db_connection` table of the configuration database and never published to the Kafka message bus. For more information about populating these values, see the [Manual Bootstrapping section]({{< relref "../deployment/deploying/manual-bootstrapping.md#database" >}}).
=======
By default, connection details for the {{< tooltip >}}RBAC{{< /tooltip >}}, Crypto, and virtual node databases are stored in the `db_connection` table of the configuration database and never published to the Kafka message bus. For more information about populating these values, see the [Manual Bootstrapping section]({{< relref "../deployment/deploying/manual-bootstrapping.md#database" >}}).
>>>>>>> main

{{< enterprise-icon noMargin="true" >}} If you are using HashiCorp Vault as an external secret management system, you must ensure the passwords for the RBAC, Crypto, and virtual node databases are stored correctly in vault. For more information, see [Encryption]({{< relref "../deployment/deploying/_index.md#external-secrets-service">}}) in the _Deploying_ section.
