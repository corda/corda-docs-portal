---
aliases:
- /releases/4.0/node-operations-upgrading-os-to-ent.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-node-operations-upgrading-os-to-ent
    parent: corda-enterprise-4-0-corda-nodes-index
    weight: 1080
tags:
- node
- operations
- upgrading
- os
- ent
title: Upgrading a Corda (open source) Node to Corda Enterprise
---


# Upgrading a Corda (open source) Node to Corda Enterprise


## Upgrading the version of Corda on a node

CorDapps, contracts and states written for Corda 3.x and Corda 4.x are compatible with Corda Enterprise Edition 4.0, so upgrading
existing open source Corda nodes should be a simple case of updating the Corda JAR. For developer information on recompiling
CorDapps against Corda Enterprise, see upgrade-notes.


### Upgrading the Node

See [Upgrading your node to Corda 4](node-upgrade-notes.md) for general instructions on upgrading your node.



### Database upgrades

When upgrading an existing node from Corda 3.x or Corda 4.x to Corda Enterprise, the node operator has the option of using one of the enterprise
database engines that are supported (see [Node database](node-database.md)).
We highly recommend moving away from the default H2 database when setting up a production node.

Corda Enterprise uses [Liquibase](database-management.md#liquibase-ref) for database schema management.
See [Database management](database-management.md) for more info.



### Migrating existing data from a Corda 4.0 H2 database to a Corda Enterprise Edition 4.0 supported database

{{< note >}}
Switching from an H2 development database to a commercial production database requires migrating across both schemas and data.
Specialist third party tools are available on the market to facilitate this activity. Please contact R3 for advice on specialised tooling
we have validated to work well for this upgrade exercise.

{{< /note >}}
The procedure for migrating from H2 to a commercial database is as follows:



* [Create a database user with schema permissions](node-database.md#db-setup-step-1-ref)
* Configure a Corda node to connect to the new database following [Corda node configuration changes](node-database.md#db-setup-step-3-ref)
and specific options for [you database vendor](node-database.md#db-setup-vendors-ref)
* Create database schema following one of 3 possible procedures,
depending on the database user permissions and preferred database upgrade policy> 

* [Database schema management upon node startup](node-operations-database-schema-setup.md#db-setup-auto-upgrade-ref)
* [Database Management Tool applies schema changes directly](node-operations-database-schema-setup.md#db-setup-database-management-direct-execution-ref)
* [Database Management Tool generates DDL script to be run manually](node-operations-database-schema-setup.md#db-setup-database-management-ddl-execution-ref)Execute the first 3 steps: *Essential preparation before the first installation*, *Extract DDL script using Database Management Tool*,
*Apply DDL scripts on a database*.



* Migrate data from H2 databaseThe migration from H2 database requires a third party specialized tool.
Your organisation may need to purchase a licence to use it.
Please contact R3 for further advice.




### Migrating existing data from a Corda 3.3 H2 database to a Corda Enterprise Edition 4.0 supported database

{{< note >}}
The migration from H2 database to a Corda Enterprise Edition 4.0 supported database requires a third party specialized tool.
Please contact R3 for further advice.

{{< /note >}}
Update Corda (open source) 3.3 node to Corda (open source) Corda Enterprise Edition 4.0 node first.
Then follow the [procedure migration from H2 database](#migrate-4-to-enterprise-database).


### Migrating existing data from a Corda 3.0, 3,1 or 3.2 H2 database to a Corda Enterprise Edition 4.0 supported database

{{< note >}}
The migration from H2 database to a Corda Enterprise Edition 4.0 supported database requires a third party specialized tool.
Please contact R3 for further advice.

{{< /note >}}
Please ensure you follow the instructions in [Upgrade Notes](https://docs.corda.net/releases/release-V3.3/upgrade-notes.html) to upgrade your database
to the latest minor release of Corda (3.3 as time of writing), and then proceed with upgrading following the instructions [above](#migrate-3-to-enterprise-database)

