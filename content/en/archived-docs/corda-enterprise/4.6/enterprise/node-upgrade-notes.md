---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: "corda-enterprise-4-6-node-upgrade"
    parent: corda-enterprise-4-6-upgrading-menu
tags:
- upgrading
- node
- upgrade
- notes
title: Upgrading a node to Corda 4.6
aliases: /docs/corda-enterprise/4.6/node/operating/cm-upgrading-node.html
weight: 10
---

# Upgrading a node to Corda 4.6

{{< warning >}}
Corda Enterprise Edition 4.6.3 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise Edition 4.6.3 please read the guidance on [upgrading your notary service](notary/upgrading-the-ha-notary-service.md).
{{< /warning >}}

Corda releases strive to be backwards compatible, so upgrading a node is fairly straightforward and should not require changes to applications. Upgrading from 4.x  consists of the following steps:

1. Drain the node.
1. Make a backup of your node directories and database.
1. Update the database (manual).
1. Replace the `corda.jar` file with the new version.
1. Update configuration.
1. Update the database (automatic) .
1. Start the node in the normal way.
1. Undrain the node.

{{< note >}}
The protocol is designed to tolerate node outages. During the upgrade process, peers on the network will wait for your node to come back.
{{< /note >}}

{{< warning >}}
If upgrading from Corda Enterprise 3.x:
* First ensure your node has been upgraded to the latest point release of that distribution. See [upgrading the HA notary service](notary/upgrading-the-ha-notary-service.md) for information on upgrading Corda 3.x versions.
* Then, upgrade to 4.5.
* Finally, upgrade to 4.6.
{{< /warning >}}

## Step 1. Drain the node

Before a node, or an application on a node, can be upgraded, the node must be put in draining-mode. This brings the currently running
[Flows](cordapps/api-flows.md) to a smooth halt (existing work is finished, and new work is queued rather than being processed).

Draining flows is a key task for node administrators to perform. It exists to simplify applications by ensuring apps don’t have to be
able to migrate workflows from any arbitrary point to other arbitrary points, a task that would rapidly become unfeasible as workflow
and protocol complexity increases.

To drain the node, run the `gracefulShutdown` command. This will wait for the node to drain and then shut it down once the drain
is complete.


{{< warning >}}
The length of time a node takes to drain depends both on how your applications are designed, and whether any apps are currently
talking to network peers that are offline or slow to respond. It is, therefore, difficult to give guidance on how long a drain should take. In
an environment with well written apps and in which your counterparties are online, it is possible that drains may only need a few seconds.

{{< /warning >}}



## Step 2. Make a backup of your node directories and database

It’s always a good idea to back up your data before upgrading any server. This will make it easy to roll back if there’s a problem.
You can simply make a copy of the node’s data directory to enable this. If you use an external non-H2 database, consult your database
user guide to learn how to make backups.

For a detailed explanation of Corda backup and recovery guarantees, see [Backup recommendations](node/operating/node-administration.html#backup-recommendations).



## Step 3. Update the database (manual)

The database update can be performed automatically or manually.

You can perform an automatic database update when:

* A database setup is for testing/development purposes and a Corda node connects with *administrative permissions* (it can modify database schema).
* You are upgrading a production system and your policy allows a Corda node to auto-update its database and a Corda node connects with *administrative permissions*.

If you cannot perform an automatic update, you must perform a manual update.

* To perform a manual update, follow the instructions in [3.1](#31-configure-the-database-management-tool), [3.2](#32-extract-ddl-and-dml-script-using-database-management-tool), [3.3](#33-apply-ddl-scripts-on-a-database), and [3.4](#34-optional-apply-data-updates-on-the-h2-database) (below). Then go on to [Step 4](#step-4-replace-cordajar-with-the-new-version).
* To perform an automatic update, skip steps 3.1 to 3.4 and go directly to [Step 4](#step-4-replace-cordajar-with-the-new-version). The automatic update will be performed later in the update process ([Step 6](#step-6-update-the-database-automatic)).


### 3.1. Configure the Database Management Tool

The Corda Database Management Tool needs access to a running database.
The tool is configured in a similar manner to the Corda node.
A base directory needs to be provided with the following content:


* A `node.conf` file with database connection settings.
* A `drivers` directory (where the JDBC driver will be placed).

Create a `node.conf` with the properties for your database.
`node.conf` templates for each database vendor are shown below.


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



Replace placeholders `<server>`, `<login>`, `<password>`, and `<database>` with appropriate values.
`<database>` should be a user database and `<schema>` a schema namespace.
Ensure `<login>` and `<password>` are for a database user with visibility of the `<schema>`.
The `myLegalName` field is obligatory, however, it is used in Step 3.4 only
(the tool doesn’t understand the context of the run and always requires the field to be present).
For this step you can use any valid dummy name - for example, `O=Dummy,L=London,C=GB` for `<node_legal_name>`.

The Microsoft SQL JDBC driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
Extract the archive, and copy the single file `mssql-jdbc-6.4.0.jre8.jar` into the `drivers` directory.


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

Replace placeholders `<server>`, `<login>`, `<password>`, `<database>` with appropriate values.
`<database>` is a database name and `<schema>` is a schema namespace.
Ensure `<login>` and `<password>` are for a database user with visibility of the `<schema>`.
The `myLegalName` field is obligatory however it is used in Step 3.4 only
(the tool doesn’t understand the context of the run and always requires the field to be present).
For this step you can use any valid dummy name - for example, `O=Dummy,L=London,C=GB` for `<node_legal_name>`.

The Microsoft JDBC 6.4 driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
Extract the archive, and copy the single file `mssql-jdbc-6.4.0.jre8.jar` into the `drivers` directory.


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

Replace placeholders `<host>`, `<port>` and `<sid>`, `<user>`, `<password>` and `<schema>` with appropriate values.
`<schema>` is a database schema namespace, for a basic setup the schema name equals `<user>`.
The `myLegalName` field is obligatory however it is used in Step 3.4 only
(the tool doesn’t understand the context of the run and always requires the field to be present).
For this step you can use any valid dummy name - for example, `O=Dummy,L=London,C=GB` for `<node_legal_name>`.

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

Replace placeholders `<host>`, `<port>`, `<database>`, `<user>`, `<password>` and `<schema>` with appropriate values.
`<schema>` is the database schema name assigned to the user,
the value of `database.schema` is automatically wrapped in double quotes to preserve case-sensitivity.
The `myLegalName` field is obligatory however it is used in Step 3.4 only
(the tool doesn’t understand the context of the run and always requires the field to be present).
For this step you can use any valid dummy name - for example, `O=Dummy,L=London,C=GB` for `<node_legal_name>`.

Copy the PostgreSQL JDBC Driver *42.2.8* version *JDBC 4.2* into the `drivers` directory.


### 3.2. Extract DDL and DML script using Database Management Tool

To run the tool, use the following command:

```shell
java -jar tools-database-manager-<release number>.jar dry-run -b path_to_configuration_directory --core-schemas --app-schemas
```

The option `-b` points to the base directory (which contains a `node.conf` file, and `drivers` and `cordapps` subdirectories).

`--core-schemas` is required to adopt the changes made in the new version of Corda, and `--app-schemas` is related to the CorDapps changes.

A script named `migrationYYYYMMDDHHMMSS.sql` containing DDL and DML statements will be generated in the current directory.
This script will contain all the statements required to modify and create data structures (for example, tables/indexes),
and updates the Liquibase management table *DATABASECHANGELOG*.
The command doesn’t alter any tables itself.

{{< note >}}

If your DDL and DML statements are run separately (for example, if the DB admin runs DDL and an app user runs DML) you need to manually separate the DDL and DML statements into separate scripts.

{{< /note >}}

For descriptions of the options, refer to the [Corda Database Management Tool](database-management-tool.md) manual.


### 3.3. Apply DDL scripts on a database

The generated DDL script can be applied by the database administrator using their tooling of choice.
The script needs to be run by a database user with *administrative* permissions,
with a `<schema>` set as the default schema for that user and matching the schema used by a Corda node.
(for example, for Azure SQL or SQL Server you should not use the default database administrator account).

{{< note >}}
You may connect as a different user to the one used by a Corda node (for example, when a node connects via
a user with *restricted permissions*), as long as your user has the same default schema as the node has.
(The generated DDL script adds the schema prefix to most of the statements, but not to all of them.)

{{< /note >}}
The whole script needs to be run. Partially running the script causes the database schema content to be inconsistently versioned.


{{< warning >}}
The DDL scripts don’t contain any checks to prevent them from running twice.
An accidental re-run of the scripts will fail (as the tables are already there), but may left some old, orphan tables.

{{< /warning >}}



### 3.4. Optional: Apply data updates on the H2 database

{{< note >}}

You only need to perform this step for the H2 database.

{{< /note >}}

The schema structure changes in Corda 4.0 require data to be propagated to new tables and columns based on the existing rows and specific node configuration (for example, node legal name). Such migrations cannot be expressed by the DDL script, so they need to be performed by the Database Management Tool (or a Corda node). These updates are required any time you are upgrading either from an earlier version to 4.0 or from 4.x to 4.x - for example, upgrading from 4.5 to 4.6.

The Database Management Tool can execute the remaining data upgrade.
As the schema structure is already created in the 3rd step, the tool can connect with *restricted* database permissions.
The only activities in this step are inserts/upgrades data rows, and no alterations to the schema are applied.

You can reuse the tool configuration directory (with modifications) created in Step 3.1, or you can run the tool
accessing the base directory of a Corda node (for which the data update is being performed).
In the latter case no configuration modification is needed,
however the Database Migration Tool needs to be run from within the same machine as a Corda node runs.

If you are reusing the tool configuration directory:

1. Ensure `myLegalName` setting in `node.conf` is set with a node name for which the data update will be run
(for example, while upgrading database schema used by a node `O=PartyA,L=London,C=GB`, assign the same value to `myLegalName`).
{{< warning >}}
Any `node.conf` misconfiguration may cause data row migration to be wrongly applied. This may happen silently (without any error).
The value of `myLegalName` must exactly match the node name that is used in the given database schema.{{< /warning >}}

2. Create `cordapps` subdirectory and copy the CorDapps used by the Corda node.

3. Change the database user to one with *restricted permissions*. This ensures no database alteration is performed by this step.To run the remaining data migration, run:

```shell
java -jar tools-database-manager-4.6-RC03.jar execute-migration -b . --core-schemas --app-schemas
```





The option `-b` points to the base directory (with a `node.conf` file, and *drivers* and *cordapps* subdirectories).

`--core-schemas` is required to adopt the changes made in the new version of Corda, and `--app-schemas` is related to the CorDapps changes.


## Step 4. Replace `corda.jar` with the new version

Replace the `corda.jar` with the latest version of Corda.

Download the latest version of Corda from [our Artifactory site](https://software.r3.com/artifactory/webapp/#/artifacts/browse/simple/General/corda/net/corda/corda-node).
Make sure it’s available on your path, and that you’ve read the [Corda release notes](release-notes-enterprise.md). Pay particular attention to which version of Java this
node requires.


{{< important >}}
Corda 4 requires Java 8u171 or any higher Java 8 patch level. Java 9+ is not currently supported.


{{< /important >}}


## Step 5. Update configuration

Remove any `transactionIsolationLevel`, `initialiseSchema`, or `initialiseAppSchema` entries from the database section of your configuration

## Step 6. Update the database (automatic)

{{< note >}}Do not perform this step if you have already updated the database manually ([Step 3](#step-3-update-the-database-manual)).{{< /note >}}

Start the node with the `run-migration-scripts` sub-command with `--core-schemas` and `--app-schemas`.

```bash
java -jar corda.jar run-migration-scripts --core-schemas --app-schemas
```

The node will perform any automatic data migrations required, which may take some
time. If the migration process is interrupted it can be continued simply by starting the node again, without harm. The node will stop automatically when migration is complete.

## Step 7. Start the node in the normal way

Start the node in the normal way.

## Step 8. Undrain the node

You may now do any checks that you wish to perform, read the logs, and so on. When you are ready, use this command at the shell:

`run setFlowsDrainingModeEnabled enabled: false`

Your upgrade is complete.
