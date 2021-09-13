---
aliases:
- /releases/4.2/node-operations-upgrading-os-to-ent.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-node-operations-upgrading-os-to-ent
    parent: corda-enterprise-4-2-corda-nodes-index
    weight: 1110
tags:
- node
- operations
- upgrading
- os
- ent
title: Upgrading a Corda (open source) Node to Corda Enterprise
---


# Upgrading a Corda (open source) Node to Corda Enterprise

A Corda (open source) node can be upgraded to Corda Enterprise.
If the same database is to be reused, the most complicated steps are ensuring custom CorDapps contain
Liquibase database management scripts and adding these scripts into the database change log table.

The migration from an H2 database to a 3rd party commercial database, while upgrading to Corda Enteprise,
requires a third party tool to migrate data.

An upgrade from the older Corda (open source) release (3.x) is also feasible,
but you need to upgrade the Corda node to the latest 3.x version first (3.3, at time of writing).



## Upgrade from Corda (open source) to Corda Enterprise

To upgrade Corda (open source) to Corda Enterprise within the same major release version, follow the Corda node upgrade procedure.
The database upgrade steps need to be replaced by those specified below,
depending if you are [reusing the same database](#node-operations-upgrading-os-to-ent-1)
or [moving away from H2](#node-operations-upgrading-os-to-ent-2).



### Reusing an existing database


* Ensure CorDapps contain Liquibase database management scripts.
You can check if the CorDapp JAR contains Liquibase scripts as described in [here](node-operations-cordapp-deployment.md#cordapp-deploymnet-database-setup-ref).
If the Cordapp stores data in the custom tables (consult with the CorDapp developer/provider)
and it doesn’t contain Liquibase scripts, follow the procedure
[to add the script retrospectively](database-management.md#database-management-add-liquibase-retrospectively-ref).{{< note >}}
Adding a Liquibase migration script to a CorDapp should be done by a CorDapp developer.{{< /note >}}

* Generate CorDapp changesets against an empty database.Any custom tables required by CorDapps will have been created manually or by Hibernate upon node startup.
Because of this, the database doesn’t contain an entry in the *DATABASECHANGELOG* table (usually created by the Liquibase runner).
This step aims to add the required log as if these tables were created by Liquibase.First, you need to run Corda Database Management Tool to obtain DDL statements created by Liquibase.
You should run the tool against an empty database, not the database you are reusing.To run the tool use the following command:

```shell
java -jar tools-database-manager-|release|.jar dry-run -b path_to_configuration_directory
```

The option `-b` points to the base directory (the directory containing a `node.conf` file, and the *drivers* and *cordapps* subdirectories).The generated script (*migration/*.sql*) will be present in the base directory.
This script contains all of the statements to create the data structures (e.g. tables/indexes) for CorDapps,
and inserts to the Liquibase management table *DATABASECHANGELOG*.
For a description of the options, refer to the [Corda Database Management Tool](node-database.md#database-management-tool-ref) manual.
* Run selected insert statements to update Liquibase database change logIn the generated script, find all inserts into *DATABASECHANGELOG* table related to your CorDapp,
you can search for *– Changeset migration/<file-name>* lines, where <file-name> references the Liquibase Script file name from the CorDapp.
The SQL insert related to a changeset will follow the *– Changeset migration/<file-name>* comment, e.g.:

```sql
-- Changeset migration/yo-schema-v1.changelog-master.sql::initial_schema_for_YoSchemaV1::R3.Corda.Generated
INSERT INTO PUBLIC.DATABASECHANGELOG (ID, AUTHOR, FILENAME, DATEEXECUTED, ORDEREXECUTED, MD5SUM, DESCRIPTION, COMMENTS, EXECTYPE, CONTEXTS, LABELS, LIQUIBASE, DEPLOYMENT_ID) VALUES ('initial_schema_for_YoSchemaV1', 'R3.Corda.Generated', 'migration/yo-schema-v1.changelog-master.sql', NOW(), 74, '7:2d4e1d5d7165a8edc848208d0707eb24', 'sql', '', 'EXECUTED', NULL, NULL, '3.5.3', '2862877878');
```

Copy selected insert statements and execute them on the database, using the correct schema name.



### Migrating from the H2 database to another database vendor

{{< note >}}
Switching from an H2 development database to a commercial production database requires migrating both schemas and data.
Specialist third party tools are available on the market to facilitate this activity. Please contact R3 for advice on specialised tooling
we have validated for this upgrade exercise.

{{< /note >}}
The procedure for migrating from H2 to a commercial database is as follows:


* Create a database schema and configure a Corda node to connect to the new database following [Database schema setup](node-database-admin.md) instructions
for a production system, or [Simplified database schema setup for development](node-database-developer.md) instructions for development/testing purposes.
Refer to [Node database](node-database.md) to decide which setup is more suitable.
* Migrate data from H2 databaseThe migration from the H2 database requires a third party specialized tool.
Your organisation may need to purchase a licence to use the tool.
Please contact R3 for further advice.
* Follow the same CorDapp database upgrade steps (1-3) in [reusing an existing database](#node-operations-upgrading-os-to-ent-1).



## Upgrade from an older Corda (open source) release to Corda Enterpise

CorDapps, contracts and states written for Corda 3.x and Corda 4.x are compatible with Corda Enterprise 4.2, so upgrading
existing open source Corda nodes should be a simple case of updating the Corda JAR.
See [Upgrading your node to Corda 4](node-upgrade-notes.md) for general instructions on upgrading your node.
For developer information on recompiling CorDapps against Corda Enterprise, see upgrade-notes.

Please ensure you follow the instructions in [Upgrade Notes](https://docs.corda.net/releases/release-V3.3/upgrade-notes.html)
to upgrade your database to the latest minor release of Corda (3.3 as time of writing),
and then proceed with the upgrade following the instructions in [above](#node-operations-upgrading-os-to-ent-1).


### Reusing an existing database

To reuse an existing database, follow the same database instructions as
[upgrading within the same Corda version](#node-operations-upgrading-os-to-ent-1).


### Migrating from H2 database to other database vendor

{{< note >}}
Switching from an H2 development database to a commercial production database requires the migration of both schema and data.
Specialist third party tools are available that facilitate this activity. Please contact R3 for advice on specialised tooling
that we have validated for this upgrade exercise.

{{< /note >}}
To migrate from a H2 database to another database, follow the same database instructions as
[upgrading within the same Corda version](#node-operations-upgrading-os-to-ent-2).


## Using a third-party tool to migrate data from a H2 database

R3 has trialled the third-party commercial tool [Full Convert](https://www.spectralcore.com/fullconvert) for migrating from a H2 database
to a 3rd party commercial databases.
It can be used via the GUI application or from the command-line, however it only runs on Windows: Vista SP2 and later, as well as Windows Server 2008 and later.
The tool works by connecting to both databases simultaneously and migrates tables, their data, and other schema objects form one database to the other.
It can be used to migrate from a H2 database by connecting to its database file.

