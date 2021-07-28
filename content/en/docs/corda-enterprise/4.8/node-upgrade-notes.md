---
date: '2021-07-07'
menu:
  corda-enterprise-4-8:
    identifier: "corda-enterprise-4-8-node-upgrade"
    parent: corda-enterprise-4-8-upgrading-menu
tags:
- upgrading
- node
- upgrade
- notes
title: Upgrade a node to Corda Enterprise 4.8
aliases: /docs/corda-enterprise/4.8/node/operating/cm-upgrading-node.html
weight: 10
---

# Upgrade a node to Corda Enterprise 4.8

Follow these steps to upgrade a node from Corda Enterprise 4.x to Corda Enterprise 4.8.

If you are upgrading from Corda Enterprise 3.x, you must first:
1. Upgrade your node to Corda Enterprise 3.3, if you haven't already. If your node is running on an earlier version, follow the steps in [Upgrade a Corda 3.X Enterprise Node](../3.3/node-operations-upgrading.html#upgrading-a-corda-enterprise-node).
2. Upgrade from Corda Enterprise 3.3 to Corda Enterprise 4.5.
3. Upgrade from Corda 4.5 to Corda Enterprise 4.8.

{{< warning >}}
Corda Enterprise 4.8 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise 4.8, read the guidance on [upgrading your notary service](notary/upgrading-the-ha-notary-service.md/).
{{< /warning >}}

Most of Corda's public, non-experimental APIs are backwards compatible. See the [full list of stable APIs](https://docs.corda.net/docs/corda-os/4.8/api-stability-guarantees.html). If you are working with a stable API, you don't need to update your CorDapps. To upgrade:

1. Drain the node.
1. Make a backup of your node's directories and database.
1. Update the database (manually).
1. Replace the `corda.jar` file with the new version.
1. Update configuration.
1. Update the database (automatically).
1. Start the node.
1. Undrain the node.

{{< note >}}
The protocol tolerates node outages. Peers on the network wait for your node to become available after upgrading.
{{< /note >}}

## Step 1: Drain the node

Node operators must drain nodes (or CorDapps on nodes) before they can upgrade them. Draining brings all [flows](cordapps/api-flows.md/) that are currently running to a smooth halt. The node finishes any work already in progress, and queues any new work. This process frees CorDapps from the requirement to migrate workflows from an arbitrary point to another arbitrary point—a task that would rapidly become unfeasible as workflow
and protocol complexity increases.

You can drain a node by running `gracefulShutdown`. This waits for the node to drain and then shuts it down once the drain
is complete.


{{< warning >}}
The length of time a node takes to drain varies. It depends on how your CorDapps are designed and whether any CorDapps are
communicating with network peers that are offline or slow to respond. In
an environment with well written CorDapps and counterparties who are online, drains may only take a few seconds.

{{< /warning >}}



## Step 2: Make a backup of your node's directories and database

Back up your data before upgrading, in case you need to roll back if there’s a problem. Make a copy of the node’s data directory or, if you use an external non-H2 database, consult your database user guide to learn how to make backups.

For a detailed explanation of Corda backup and recovery guarantees, see [Backup recommendations](node/operating/node-administration.md#backup-recommendations).



## Step 3: Update the database

The database update can be performed automatically or manually.

You can perform an automatic database update when:

* Your database setup is for testing/development purposes and your node connects with *administrative permissions* (in essence, it can modify database schema).
* You are upgrading a production system, your policy allows a node to auto-update its database, and your node connects with *administrative permissions*.

If you met the above criteria, then skip steps 3.1 to 3.4 and go directly to [Step 4](#step-4-replace-cordajar-with-the-new-version). You'll perform the automatic update in [Step 6](#step-6-update-database-automatic).


If you can't perform an automatic update, then you must perform a manual update by following steps 3.1 to 3.4 below, before moving on to [Step 4](#step-4-replace-cordajar-with-the-new-version).


### 3.1. Configure the Database Management Tool

The Corda Database Management Tool needs access to a running database. You can set up the tool using a similar process to configuring a node.
You must provide a base directory that includes:


* A `node.conf` file with database connection settings.
* A `drivers` directory. You will place the JDBC driver here.

`node.conf` template files and details on where to find the JDBC driver for each database vendor can be found below.


#### Azure SQL

The required `node.conf` settings for the Database Management Tool using Azure SQL:


```groovy
dataSourceProperties = {
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://<server>.database.windows.net:1433;databaseName=<database>;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    dataSource.user = <login>
    dataSource.password = <password>
}
database = {
    schema = <schema>
}
myLegalName = <node_legal_name>
```

Complete the template:

* Replace the placeholders `<server>`, `<login>`, `<password>`, and `<database>` with appropriate values.
* `<database>` is a user database and `<schema>` is a schema namespace.
* Ensure `<login>` and `<password>` are for a database user with visibility of the `<schema>`.
* The `myLegalName` field is obligatory, however, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

You can download the Microsoft SQL JDBC driver from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
Extract the archive and copy the single file `mssql-jdbc-6.4.0.jre8.jar` into the `drivers` directory.


#### SQL Server

The required `node.conf` settings for the Database Management Tool using SQL Server:

```groovy
dataSourceProperties = {
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://<host>:1433;databaseName=<database>"
    dataSource.user = <login>
    dataSource.password = <password>
}
database = {
    schema = <schema>
}
myLegalName = <node_legal_name>
```

Complete the template:

* Replace placeholders `<server>`, `<login>`, `<password>`, and `<database>` with appropriate values.
* `<database>` is a database name and `<schema>` is a schema namespace.
* Ensure `<login>` and `<password>` are for a database user with visibility of the `<schema>`.
* The `myLegalName` field is obligatory, however, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

You can download the Microsoft JDBC 6.4 driver from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
Extract the archive and copy the single file `mssql-jdbc-6.4.0.jre8.jar` into the `drivers` directory.


#### Oracle

The required `node.conf` settings for the Database Management Tool using Oracle:

```groovy
dataSourceProperties = {
    dataSourceClassName = "oracle.jdbc.pool.OracleDataSource"
    dataSource.url = "jdbc:oracle:thin:@<host>:<port>:<sid>"
    dataSource.user = <user>
    dataSource.password = <password>
}
database = {
    schema = <schema>
}
myLegalName = <node_legal_name>
```

Complete the template:

* Replace placeholders `<host>`, `<port>`, `<sid>`, `<user>`, `<password>`, and `<schema>` with appropriate values.
* `<schema>` is a database schema namespace, for a basic setup the schema name equals `<user>`.
* The `myLegalName` field is obligatory, however, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

Copy the Oracle JDBC driver `ojdbc6.jar` for 11g RC2 or `ojdbc8.jar` for Oracle 12c into the `drivers` directory.


#### PostgreSQL

The required `node.conf` settings for the Database Management Tool using PostgreSQL:

```groovy
dataSourceProperties = {
    dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
    dataSource.url = "jdbc:postgresql://<host>:<port>/<database>"
    dataSource.user = <user>
    dataSource.password = <password>
}
database = {
    schema = <schema>
}
myLegalName = <node_legal_name>
```

Complete the template:

* Replace placeholders `<host>`, `<port>`, `<database>`, `<user>`, `<password>`, and `<schema>` with appropriate values.
* `<schema>` is the database schema name assigned to the user.
The value of `database.schema` is automatically wrapped in double quotes to preserve case-sensitivity.
* The `myLegalName` field is obligatory, however, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

Copy the PostgreSQL JDBC Driver *42.2.8* version *JDBC 4.2* into the `drivers` directory.


### 3.2. Extract the DDL and DML scripts using the Database Management Tool

To run the tool, use the command:

```shell
java -jar tools-database-manager-<release number>.jar dry-run -b path_to_configuration_directory --core-schemas --app-schemas
```

Option `-b` points to the base directory, which contains a `node.conf` file, and `drivers` and `cordapps` subdirectories.

`--core-schemas` is required to adopt the changes made in the new version of Corda, and `--app-schemas` is related to the CorDapps changes.

A script named `migrationYYYYMMDDHHMMSS.sql` containing DDL and DML statements will be generated in the current directory.
This script contains all the statements required to modify and create data structures, for example tables/indexes,
and updates the Liquibase management table **DATABASECHANGELOG**.
The command doesn't alter any tables itself.


{{< note >}}

If you run the DDL and DML statements separately, for example, if the DB admin runs DDL, and a CorDapp user runs DML, you need to manually separate the DDL and DML statements into separate scripts.

{{< /note >}}

For more information about the Database Management Tool, including available options and commands, see [Corda Database Management Tool](database-management-tool.md).


### 3.3. Apply DDL scripts on a database

The database administrator applies the generated DDL script using their tooling of choice.
A database user with *administrative permissions*, and whose default schema matches `<schema>` and the schema used by the node, runs the script.
For example, for Azure SQL or SQL Server, you should not use the default database administrator account.

{{< note >}}
You can connect as a different user to the one used on the node, for example, a user with *restricted permissions*, as long as your user has the same default schema as the node.
The generated DDL script adds the schema prefix to most of the statements, but not all of them.

{{< /note >}}

The whole script needs to be run. Partially running the script causes the database schema content to be inconsistently versioned.


{{< warning >}}
The DDL scripts don’t contain any checks to prevent them from running twice.
An accidental re-run of the scripts will fail (as the tables are already there), but may leave some old, orphan tables.

{{< /warning >}}



### 3.4. Apply data updates on the H2 database

{{< note >}}

You only need to perform this step for the H2 database.

{{< /note >}}

The schema structure changes in Corda 4.0 require data to be propagated to new tables and columns based on the existing rows and specific node configuration, for example, node legal name. Such migrations cannot be expressed by the DDL script, so they need to be performed by the Database Management Tool or a node. These updates are required any time you are upgrading either from an earlier version to 4.0 or from 4.x to 4.x, for example, upgrading from 4.5 to 4.8.

The Database Management Tool can execute the remaining data upgrade.
As the schema structure has already been created in the third step, the tool can connect with *restricted* database permissions.
The only activities in this step are inserting/upgrading data rows, and does not apply any alterations to the schema.

You can modify the tool configuration directory created in Step 3.1, or you can run the tool
accessing the base directory of a node for which the data update is being performed.
In the latter case, no configuration modification is needed,
however, the Database Migration Tool needs to be run from within the same machine as a node.

If you are reusing the tool configuration directory:

1. Set the `myLegalName` setting in `node.conf` to the name of the node you are running the data update for.  For example, if you are upgrading the database schema used by node `O=PartyA,L=London,C=GB`, assign the same value to `myLegalName`.

{{< warning >}}
The value of `myLegalName` must exactly match the node name used in the database schema. Any `node.conf` misconfiguration may cause data row migration to be wrongly applied. This may happen silently, without throwing an error.

{{< /warning >}}

2. Create a `cordapps` subdirectory and copy the CorDapps used by the node.

3. Change the database user to one with *restricted permissions*. This ensures the database cannot be altered. To complete the data migration, run:

```shell
java -jar tools-database-manager-4.8-RC03.jar execute-migration -b . --core-schemas --app-schemas
```





Option `-b` points to the base directory, which contains a `node.conf` file, and `drivers` and `cordapps` subdirectories.

`--core-schemas` is required to adopt the changes made in the new version of Corda, and `--app-schemas` is related to the CorDapps changes.


## Step 4. Replace `corda.jar` with the new version

Replace the `corda.jar` with the latest version of Corda.

Download the latest version of Corda from [our Artifactory site](https://software.r3.com/artifactory/webapp/#/artifacts/browse/simple/General/corda/net/corda/corda-node).
Make sure it’s available on your path, and that you’ve read the [Corda release notes](release-notes-enterprise.md). Pay particular attention to which version of Java the
node requires.


{{< important >}}
Corda 4 requires Java 8u171 or any higher Java 8 patch level. Java 9+ is not currently supported.


{{< /important >}}


## Step 5: Update configuration

{{< note >}}

You only need to perform this step if you are updating from version 4.5 or older.

{{< /note >}}

Remove any `transactionIsolationLevel`, `initialiseSchema`, or `initialiseAppSchema` entries from the database section of your configuration.

## Step 6: Update the database (automatic)

{{< note >}}

Do not perform this step if you have already updated the database manually in [Step 3](#step-3-update-the-database-manual).

{{< /note >}}

Start your node using the following command.

```bash
java -jar corda.jar run-migration-scripts --core-schemas --app-schemas
```

The node will perform any automatic data migrations required, which may take some
time. If the migration process is interrupted, restart the node to continue. The node stops automatically when migration is complete.

## Step 7: Start the node

Start your node in the normal way.

## Step 8: Undrain the node

You may now do any checks, such as reading the logs. When you are ready, use this command at the shell.

`run setFlowsDrainingModeEnabled enabled: false`

Your upgrade is complete.

## Notes

{{< warning >}}
You must align the multi-RPC client version with the node version. That means that both must be running the same version of Corda Enterprise. See [Querying flow data](node/operating/querying-flow-data.md) for more information.
{{< /warning >}}
