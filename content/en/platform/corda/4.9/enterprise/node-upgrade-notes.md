---
date: '2021-08-02'
menu:
  corda-enterprise-4-9:
    identifier: "corda-enterprise-4-9-node-upgrade"
    parent: corda-enterprise-4-9-upgrading-menu
tags:
- upgrading
- node
- upgrade
- notes
title: Upgrading a node to Corda Enterprise Edition 4.9
aliases: /docs/4.9/enterprise/node/operating/cm-upgrading-node.html
weight: 10
---

# Upgrading a node to Corda Enterprise Edition 4.9

Follow these steps to upgrade a node from Corda Enterprise Edition 4.x to Corda Enterprise Edition 4.9.

If you are upgrading from Corda Enterprise 3.x, you must first:
1. Upgrade your node to Corda Enterprise 3.3, if you haven't already. If your node is running on an earlier version, follow the steps in Upgrade a Corda 3.X Enterprise Node (available in the [archived-docs](https://github.com/corda/corda-docs-portal/tree/main/content/en/archived-docs) directory of the [corda/corda-docs-portal](https://github.com/corda/corda-docs-portal) repo).
2. Upgrade from Corda Enterprise 3.3 to Corda Enterprise Edition 4.5.
3. Upgrade from Corda 4.5 to Corda Enterprise Edition 4.9.

{{< warning >}}
Corda Enterprise Edition 4.9 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise Edition 4.9, read the guidance on [upgrading your notary service](notary/upgrading-the-ha-notary-service.md).
{{< /warning >}}

Most of Corda's public, non-experimental APIs are backwards compatible. See the [full list of stable APIs](../../../../api-ref/api-ref-corda-4.md). If you are working with a stable API, you don't need to update your CorDapps. To upgrade:

1. [Drain the node](#step-1-drain-the-node).
2. [Make a backup of the directories in your node and database](#step-2-make-a-backup-of-your-nodes-directories-and-database).
3. [Update the database](#step-3-update-the-database).
4. [Replace corda.jar with new version](#step-4-replace-cordajar-with-new-version)
5. [Install corda-shell.jar](#step-5-install-corda-shelljar).
6. [Update the configuration](#step-6-update-the-configuration).
7. [Start the node](#step-7-start-the-node).
8. [Undrain the node](#step-8-undrain-the-node).

{{< note >}}
The protocol tolerates node outages. Peers on the network wait for your node to become available after upgrading.
{{< /note >}}

## Step 1: Drain the node

Node operators must drain nodes (or CorDapps on nodes) before they can upgrade them. Draining brings all [flows](cordapps/api-flows.md) that are currently running to a smooth halt. The node finishes any work already in progress, and queues any new work. This process frees CorDapps from the requirement to migrate workflows from an arbitrary point to another arbitrary point—a task that would rapidly become unfeasible as workflow
and protocol complexity increases.

To drain a node, run `gracefulShutdown`. This waits for the all currently running flows to be completed and then shuts the node down.

{{< warning >}}
The length of time a node takes to drain varies. It depends on how your CorDapps are designed and whether any CorDapps are
communicating with network peers that are offline or slow to respond. If
the CorDapps are well-written and the required counterparties are online, drains may only take a few seconds.

For a smooth node draining process avoid long-running flows.
{{< /warning >}}

## Step 2: Make a backup of your node's directories and database

Back up your data before upgrading, in case you need to roll back if there’s a problem. Make a copy of the node’s data directory or, if you use an external non-H2 database, consult your database user guide to learn how to make backups.

For a detailed explanation of Corda backup and recovery guarantees, see [Backup recommendations](../../../../../en/platform/corda/4.9/enterprise/node/operating/node-administration.html#backup-recommendations).

## Step 3: Update the database

The database update can be performed automatically or manually.

You can perform an automatic database update when:

* Your database setup is for testing/development purposes and your node connects with *administrative permissions* (in essence, it can modify database schema).
* You are upgrading a production system, your policy allows a node to auto-update its database, and your node connects with *administrative permissions*.

If you meet the above criteria, then skip steps 3.1 to 3.4 and go directly to [Step 4](#step-4-replace-cordajar-with-the-new-version). You'll perform the automatic update in [Step 6](#step-6-start-the-node).

If you can't perform an automatic update, then you must perform a manual update by following steps 3.1 to 3.4 below. You can then move on to [Step 4](#step-4-replace-cordajar-with-the-new-version).

### 3.1. Configure the Database Management Tool

The Corda Database Management Tool needs access to a running database. You set the tool up using a similar process to how you configure a node.
You must provide a base directory that includes:

* A `node.conf` file with database connection settings.
* A `drivers` directory. You will place the JDBC driver here.

`node.conf` template files and details on where to find the JDBC driver for each database vendor can be found below.

#### Azure SQL: template file and JDBC driver

The required `node.conf` settings for the Database Management Tool using Azure SQL are:

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

1. Complete the template:

Replace the placeholders `<server>`, `<database>`, `<login>`, `<password>`, `<schema>`, and `<node_legal_name>`' with appropriate values:
* `<database>` is the user database.
* `<login>` and `<password>` must be for a database user with visibility of the `<schema>`.
* `<schema>` is the schema namespace.
* `myLegalName` is mandatory. However, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

2. Download the Microsoft SQL JDBC driver from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
3. Extract the archive and copy the single file `mssql-jdbc-6.4.0.jre8.jar` into the `drivers` directory.


#### SQL Server: template file and JDBC driver

The required `node.conf` settings for the Database Management Tool using SQL Server are:

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

1. Complete the template:

Replace the placeholders `<host>`, `<database>`, `<login>`, `<password>`, `<schema>`, and `<node_legal_name>`' with appropriate values:
* `<database>` is the user database.
* `<login>` and `<password>` must be for a database user with visibility of the `<schema>`.
* `<schema>` is the schema namespace.
* `myLegalName` is mandatory. However, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

2. Download the Microsoft JDBC 6.4 driver from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
3. Extract the archive and copy the single file `mssql-jdbc-6.4.0.jre8.jar` into the `drivers` directory.

#### Oracle: template file and JDBC driver

The required `node.conf` settings for the Database Management Tool using Oracle are:

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

1. Complete the template:

Replace the placeholders `<host>`, `<port>`, `<sid>`, `<user>`, `<password>`, `<schema>`, and `<node_legal_name>`' with appropriate values:
* `<schema>` is the database schema namespace. For a basic setup, the schema name equals `<user>`.
* `myLegalName` is mandatory. However, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

2. Copy the Oracle JDBC driver `ojdbc6.jar` for 11g RC2 or `ojdbc8.jar` for Oracle 12c into the `drivers` directory.

#### PostgreSQL: template file and JDBC driver

The required `node.conf` settings for the Database Management Tool using PostgreSQL are:

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

1. Complete the template:

Replace the placeholders `<host>`, `<port>`, `<database>`, `<user>`, `<password>`, and `<schema>`, and `<node_legal_name>`' with appropriate values:
* `<schema>` is the database schema name assigned to the user.
* The value of `database.schema` is automatically wrapped in double quotes to preserve case-sensitivity.
* `myLegalName` is mandatory. However, it is only used in Step 3.4. For this step you can replace `<node_legal_name>` with any valid dummy name, for example, `O=Dummy,L=London,C=GB`.

2. Copy the PostgreSQL JDBC Driver *42.2.8* version *JDBC 4.2* into the `drivers` directory.

### 3.2. Extract the DDL and DML scripts using the Database Management Tool

To run the tool, use the command:

```shell
java -jar tools-database-manager-<release number>.jar dry-run -b path_to_configuration_directory --core-schemas --app-schemas
```

Option `-b` points to the base directory. The directory contains a `node.conf` file and the `drivers` and `cordapps` subdirectories.

`--core-schemas` is required to adopt the changes made in the new version of Corda, and `--app-schemas` is related to the CorDapps changes.

A script named `migrationYYYYMMDDHHMMSS.sql` containing DDL and DML statements will be generated in the current directory.
This script contains all the statements required to modify and create data structures (for example tables/indexes),
and updates the Liquibase management table **DATABASECHANGELOG**.
The command doesn't alter any tables.

{{< note >}}

If you run the DDL and DML statements separately (for example, if the database administrator runs the DDL statements and a CorDapp user runs the DML statements) you need to manually separate the DDL and DML statements into separate scripts.

{{< /note >}}

For more information about the Database Management Tool including available options and commands, see [Corda Database Management Tool](database-management-tool.md).

### 3.3. Apply DDL scripts to a database

The database administrator can apply the DDL scripts to the database using their tooling of choice.
Then, any database user with *administrative permissions*, and whose default schema matches `<schema>` and the schema used by the node, can run the script.
For example, for Azure SQL or SQL Server you should not use the default database administrator account.

{{< note >}}
You can use a different user to connect to the server than the one you use to connect to the node. For example, you could connect as a user with *restricted permissions*, as long as that user has the same default schema as the node.
The generated DDL script adds the schema prefix to most of the statements, but not all of them.
{{< /note >}}

You need to run the whole script. Partially running the script causes the database schema content to be inconsistently versioned.

{{< warning >}}
The DDL scripts don’t contain any checks to prevent them from running twice.
If the scripts run a second time, they will fail because the tables are already there. However, this may generate orphan tables.
{{< /warning >}}

### 3.4. Apply data updates on the H2 database

{{< note >}}
You only need to perform this step for the H2 database.
{{< /note >}}

The schema structure changes in Corda 4.0 require data to be propagated to new tables and columns based on the existing rows and specific node configuration, for example, node legal name. Such migrations cannot be expressed by the DDL script, so they need to be performed by the Database Management Tool or a node. These updates are required any time you are upgrading either from an earlier version to 4.0 or from 4.x to 4.x. For example, if you're upgrading from 4.5 to 4.9.

The Database Management Tool can execute the remaining data upgrade.
The tool can connect with *restricted* database permissions as the schema structure was created in step three.
In this step, you will insert and upgrade the data rows. This process does not alter the schema.

You can modify and reuse the tool configuration directory you created in Step 3.1, or you can run the tool
by accessing the base directory of the node you are updating.
If you choose to update the data by accessing the base directory, you do not need to modify the tool configuration. However, you must run the tool from the same machine the node is running on.

If you are reusing the tool configuration directory:

1. Set the `myLegalName` setting in `node.conf` to the name of the node you are running the data update for.  For example, if you are upgrading the database schema used by node `O=PartyA,L=London,C=GB`, assign the same value to `myLegalName`.

{{< warning >}}
The value of `myLegalName` must exactly match the node name used in the database schema. Any `node.conf` misconfiguration may cause data row migration to be wrongly applied. This may happen silently, without throwing an error.
{{< /warning >}}

2. Create a `cordapps` subdirectory and copy the CorDapps used by the node.

3. Change the database user to one with *restricted permissions*. This ensures the database cannot be altered. To complete the data migration, run:

```shell
java -jar tools-database-manager-4.9-RC03.jar execute-migration -b . --core-schemas --app-schemas
```

Option `-b` points to the base directory which contains a `node.conf` file and `drivers` and `cordapps` subdirectories.

`--core-schemas` is required to adopt the changes made in the new version of Corda, and `--app-schemas` is related to the CorDapps changes.

## Step 4: Replace corda.jar with new version

Replace corda.jar with its latest version.

Download the latest version of Corda from [our Artifactory site](https://software.r3.com/artifactory/webapp/#/artifacts/browse/simple/General/corda/net/corda/corda-node).
Make sure it’s available on your path, and that you’ve read the [Corda release notes](release-notes-enterprise.md). Pay particular attention to which version of Java that the node requires.

{{< important >}}
Corda 4 requires Java 8u171 or any higher Java 8 patch level. Java 9+ is not currently supported.
{{< /important >}}

{{< important >}}
If you used Corda Shell in the previous version, put Corda Shell in the driver directory, or use the standalone type Corda Shell according to Node shell.
{{< /important >}}

## Step 5: Install corda-shell.jar

Install `corda-shell.jar` as a driver within your node.

Download the `corda-shell` JAR from the [Artifactory](https://software.r3.com/ui/native/r3-corda-releases/com/r3/corda/corda-shell/) and install it in a node's `/drivers` directory to run the shell in the same terminal that starts the node. By default, a Corda node does not run the shell.

For more information, see [Node Shell](node/operating/shell.html).


## Step 6: Update the configuration

{{< note >}}
You only need to perform this step if you are updating from version 4.5 or older.
{{< /note >}}

Remove any `transactionIsolationLevel`, `initialiseSchema`, or `initialiseAppSchema` entries from the database section of your configuration.

## Step 7: Start the node

If you manually updated the database in [Step 3](#step-3-update-the-database), start the node in the normal way.

However, if you need to automatically update the database as described in [Step 3](#step-3-update-the-database), then you need to start your node using the command:

```bash
java -jar corda.jar run-migration-scripts --core-schemas --app-schemas
```

The node will perform any automatic data migrations required, which may take some
time. If the migration process is interrupted, restart the node to continue. The node stops automatically when migration is complete.

## Step 8: Undrain the node

Run this command in the shell:

`run setFlowsDrainingModeEnabled enabled: false`

Your upgrade is complete.

## Notes

{{< warning >}}
You must align the multi-RPC client version with the node version. That means that both must be running the same version of Corda Enterprise. See [Querying flow data](node/operating/querying-flow-data.md) for more information.
{{< /warning >}}