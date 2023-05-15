---
title: "Database Connection Configuration"
date: '2023-05-12'
menu:
  corda5:
    identifier: corda5-cluster-database
    parent: corda5-cluster-config
    weight: 2000
section_menu: corda5
---

Database connection details must be configured differently than the standard dynamic configuration process. This is necessary not only because the details are sensitive but also to maintain operation separation between the different types of workers. For example, the flow worker process should not have access to the database connection details. This section describes how the connection details of the following are mantained:
* [Configuration Database]({{< relref "#configuration-database" >}})
* [All Other Databases]({{< relref "#all-other-databases" >}})

## Configuration Database

The configuration database contains all configuration for the Corda cluster and so the database worker process must be able to connect to this database when it starts. As a result, the connection details for this database must be passed to the database worker process in the deployment configuration. For example:

```
-ddatabase.user=db-user
-ddatabase.pass=a-db-password
-ddatabase.jdbc.url=jdbc:postgresql://db-address:5432/cordacluster
-ddatabase.jdbc.directory=/opt/corda/drivers
```

{{< note >}}
Credentials can be encrypted. See [Configuration Secrets]({{< relref "./secrets.md">}}), for more information.
{{< /note >}}

## All Other Databases

Connection details for the RBAC, Crypto, and virtual node databases are stored in the `db_connection` table of the configuration database and never published to the Kafka message bus.