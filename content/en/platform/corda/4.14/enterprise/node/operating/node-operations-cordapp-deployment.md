---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4.14:
    parent: corda-enterprise-4.14-corda-nodes-operating
tags:
- node
- operations
- cordapp
- deployment
title: Installing CorDapps on a node
weight: 10
---


# Deploying CorDapps on a node

To deploy a new CorDapp on a node:

1. Stop the node.
2. Make any database changes required to any custom vault tables for the upgraded CorDapp. Depending on the Corda node setup,
you should either:
   - **Production environment:** Follow [Updating the database]({{< relref "#updating-the-database" >}})
   - **Development/test environment:** described in node-development-cordapp-deployment
which contains a simplified database upgrade process.
3. Copy the CorDapp JARs to the `cordapps` directory of the node.
4. Restart the node.


## Updating the database

For a Corda node connecting to a database with **restricted permissions**, any tables need to be created manually with the
help of the Corda database management tool. This requires that a custom table used by a CorDapp
is created before the CorDapp is deployed.

A CorDapp that stores data in a custom table contains an embedded Liquibase database migration script.
This follows the [Liquibase](http://www.liquibase.org) functionality used by Corda for the database schema management.

Creating a new database table requires a similar procedure to creating a Corda database schema using Corda database management tool.
Because of that, most of the steps are similar to those described in [Database schema setup]({{< relref "node-database-admin.md" >}}).


### Step 1: Check if the CorDapp requires custom tables

Refer to the CorDapp documentation or consult a CorDapp provider if the CorDapp requires custom backing tables.
You can verify a CorDapp JAR manually to check the presence of script files inside *migration* director; for example, for Linux:


```bash
jar -tf <cordapp.jar> | grep -E 'migration.*\.(xml|yml|sql)'
```



If the CorDapps do not contain any migration scripts, then they do not require custom tables and you can skip this step.


{{< note >}}
It is possible that a CorDapp is shipped without a database migration script when it should contain one.
If a CorDapp has been tested on a node running against a non-default database (H2),
this would have already been detected in your test environment.

{{< /note >}}


### Step 2: Configure the database management tool

The Corda database management tool needs access to a running database.
The tool is configured in a similar manner to a Corda node.
A base directory needs to be provided with the following content:

- A `node.conf` file with database connection settings
- A `drivers` directory in which to place the JDBC driver
- A `cordapps` directory containing the CorDapps being deployed

The process is as follows:

1. Copy the CorDapp JARs to the `cordapps` subdirectory. This is required to collect and run any database migration scripts for CorDapps.
2. Create `node.conf` with properties for your database. The `node.conf` templates for each database vendor are shown below:
   * [Azure SQL](#nodeconf-for-azure-sql)
   * [SQL Server](#nodeconf-for-sql-server)
   * [Oracle](#nodeconf-for-oracle)
   * [PostgreSQL](#nodeconf-for-postgresql)
3. Copy the respective driver into the `drivers` directory.

#### `node.conf` for Azure SQL

The following extract shows the database management tool settings in `node.conf` for Azure SQL:

```groovy
dataSourceProperties = {
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=<my_database>;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    dataSource.user = my_admin_login
    dataSource.password = "my_password"
}
database = {
    schema = my_schema
}
```



Replace placeholders *<database_server>* and *<my_database>* with appropriate values (*<my_database>* is a user database).
The `database.schema` is the database schema name assigned to both administrative and restrictive users.

Microsoft SQL JDBC driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
Extract the archive, and copy the single file *mssql-jdbc-6.4.0.jre8.jar* into the `drivers` directory.



#### `node.conf` for SQL Server

The following extract shows the database management tool settings in `node.conf` for SQL Server:


```groovy
dataSourceProperties = {
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://<host>:<port>;databaseName=my_database"
    dataSource.user = my_admin_login
    dataSource.password = "my_password"
}
database = {
    schema = my_schema
}
```



Replace placeholders *<host>* and *<port>* with appropriate values. The default SQL Server port is 1433.

Microsoft JDBC 6.4 driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615).
Extract the archive, and copy the single file *mssql-jdbc-6.4.0.jre8.jar* into the `drivers` directory.



#### `node.conf` for Oracle

The following extract shows the database management tool settings in `node.conf` for Oracle:

```groovy
dataSourceProperties = {
    dataSourceClassName = "oracle.jdbc.pool.OracleDataSource"
    dataSource.url = "jdbc:oracle:thin:@<host>:<port>:<sid>"
    dataSource.user = my_admin_user
    dataSource.password = "my_password"
}
database = {
    schema = my_admin_user
}
```



Replace the placeholder values *<host>*, *<port>* and *<sid>* with appropriate values.
For a basic Oracle installation, the default *<sid>* value is *xe*.
If the user was created with *administrative* permissions the schema name `database.schema` equal to the user name (*my_user*).

Copy Oracle JDBC driver *ojdbc6.jar* for 11g RC2 or *ojdbc8.jar* for Oracle 12c into the `drivers` directory.



#### `node.conf` for PostgreSQL

The following extract shows the database management tool settings in `node.conf` for PostgreSQL:

```groovy
dataSourceProperties = {
    dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
    dataSource.url = "jdbc:postgresql://<host>:<port>/<database>"
    dataSource.user = my_user
    dataSource.password = "my_password"
}
database = {
    schema = my_schema
}
```



Replace placeholders *<host>*, *<port>* and *<database>* with appropriate values.
The `database.schema` is the database schema name assigned to the user.
The value of `database.schema` is automatically wrapped in double quotes to preserve case-sensitivity.

Copy PostgreSQL JDBC Driver *42.2.8* version *JDBC 4.2* into the `drivers` directory.


### Step 3: Extract DDL script using database management tool

To run the tool, use the following command:


```shell
java -jar tools-database-manager-|release|.jar create-migration-sql-for-cordapp -b path_to_configuration_directory
```



The option `-b` points to the base directory with a `node.conf` file and *drivers* and *cordapps* subdirectories.

A generated script named *migration/*.sql* will be present in the base directory.
This script contains all statements to create data structures (for example, tables/indexes) for CorDapps
and inserts to the Liquibase management table *DATABASECHANGELOG*.
The command doesn’t alter any tables.
Refer to [Corda database management tool]({{< relref "node-database.md#database-management-tool" >}})manual for a description of the options.


### Step 4: Apply DDL scripts on a database

The generated DDL script can be applied by the database administrator using their tooling of choice.
The script needs to be executed by a database user with *administrative* permissions,
with a *<schema>* set as the default schema for that user and matching the schema used by a Corda node.
(for example, for Azure SQL or SQL Server you should not use the default database administrator account).

{{< note >}}
You may connect as a different user to the one used by a Corda node (for example, when a node connects via
a user with *restricted permissions*), so long as the user has the same default schema as the node
(the generated DDL script may not add schema prefix to all the statements).

{{< /note >}}
The whole script needs to be run. Running the script partially will cause the database schema content to have inconsistent versions.


{{< warning >}}
The DDL scripts don’t contain any check preventing running them twice.
An accidental re-run of the scripts will fail (as the tables are already there) but may leave some old, orphan tables.

{{< /warning >}}




### Step 5: Add permission to use tables

For some databases, the permission to use tables can only be assigned after the tables are created.
This step is required for the Oracle database only.


#### Oracle

Connect to the database as administrator
and grand *SELECT*, *INSERT*, *UPDATE*, *DELETE* permissions to *my_user* for all CorDapps custom tables:


```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.<cordapp_table> TO my_user;
```



Change *<cordapp_table>*  to a CorDapp table name.
