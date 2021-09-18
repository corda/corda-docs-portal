---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-operating-db
tags:
- node
- database
- developer
title: Simplified database schema setup for development
weight: 20
---


# Simplified database schema setup for development

This document provides instructions on how to create database schema
and configure a Corda node that is suitable for development and testing purposes.
This setup allows the auto-creation of database objects by the node upon startup
by connecting to a database with a user with **administrative permissions**.
Please refer to [Database schema setup](node-database-admin.md) if you are setting up a Corda database in a production environment.

The instructions cover all commercial third-party database vendors supported by Corda Enteprise
(Azure SQL, SQL Server, Oracle and PostgreSQL), and the default embedded H2 database:



* [Database setup for a new installation](#node-database-developer-database-schema-setup-ref)
* [Database update](#node-database-developer-database-schema-setup-ref)
* [Database setup when deploying a new CorDapp](#node-database-developer-database-schema-setup-when-deploying-a-new-cordapp-ref)
* [Database update when upgrading a new CorDapp](#node-database-developer-database-schema-update-when-upgrading-a-new-cordapp-ref)
* [Database cleanup](#node-database-developer-database-schema-cleanup-ref).




## Database schema setup

Setting up a Corda node to connect to a database requires:


* [Creating a database user with schema permissions](#db-setup-developer-step-1-ref)
* [Corda node configuration changes](#db-setup-developer-step-2-ref)
* [Run the node](#db-setup-developer-step-3-ref) to auto-create schema objects

Corda ships out of the box with an [H2 database](http://www.h2database.com) which doesn’t require any configuration
(see the documentation on [Database access when running H2](../../node-database-access-h2), hence when using H2 database it’s sufficient to [start the node](node-database-admin.md#db-setup-step-3-ref) and the database will be created.



### 1. Creating a database user with schema permissions

Before running a Corda node you must create a database user and schema namespace with **administrative permissions** (except H2 database).
This grants the database user full access to a Corda node, such that it can execute both DDL statements
(to define data structures/schema content e.g. tables) and DML queries (to manipulate data itself e.g. select/delete rows).
This permission set is more permissive and should be used with caution in production environments.

Variants of Data Definition Language (DDL) scripts to are provided for each supported database vendor.
The example permissions scripts have no group roles nor specify physical database settings e.g. max disk space quota for a user.
The scripts and node configuration snippets contain example values *my_login* for login, *my_user*/*my_admin_user* for user,
*my_password* for password, and *my_schema* for schema name. These values are for illustration purposes only.
Please substitute with actual values configured for your environment(s).


{{< warning >}}
Each Corda node needs to use a separate database user and schema where multiple nodes are hosted on the same database instance.

{{< /warning >}}


{{< note >}}
For developing and testing the node using the Gradle plugin `Cordform` `deployNodes` task you need to create
the database user/schema manually ([the first Step](#db-setup-developer-step-1-ref)) before running the task (deploying nodes).
Also note that during re-deployment existing data in the database is retained.
Remember to cleanup the database if required as part of the testing cycle.
The above restrictions do not apply to the default H2 database as the relevant database data file is
re-created during each `deployNodes` run.

{{< /note >}}
Creating database user with schema permissions for:


* [Azure SQL](#db-dev-setup-create-user-azure-ref)
* [SQL Server](#db-dev-setup-create-user-sqlserver-ref)
* [Oracle](#db-dev-setup-create-user-oracle-ref)
* [PostgreSQL](#db-dev-setup-create-user-postgresql-ref)



#### SQL Azure

Connect to the master database as an administrator
(e.g. *jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=master;[…]*).
Run the following script to create a user and a login:

```sql
CREATE LOGIN my_login WITH PASSWORD = 'my_password';
CREATE USER my_user FOR LOGIN my_login;
```

By default the password must contain characters from three of the following four sets: uppercase letters, lowercase letters, digits, and symbols,
e.g. *C0rdaAP4ssword* is a valid password. Passwords are delimited with single quotes.

Connect to a user database as the administrator (replace *master* with a user database in the connection string).
Run the following script to create a schema and assign user permissions:

```sql
CREATE SCHEMA my_schema;

CREATE USER my_user FOR LOGIN my_login WITH DEFAULT_SCHEMA = my_schema;
GRANT SELECT, INSERT, UPDATE, DELETE, VIEW DEFINITION, ALTER, REFERENCES ON SCHEMA::my_schema TO my_user;
GRANT CREATE TABLE TO my_user;
GRANT CREATE VIEW TO my_user;
```



#### SQL Server

Connect to the master database as an administrator (e.g. *jdbc:sqlserver://<host>:<port>;databaseName=master*).
Run the following script to create a database, a user and a login:

```sql
CREATE DATABASE my_database;

CREATE LOGIN my_login WITH PASSWORD = 'my_password', DEFAULT_DATABASE = my_database;
CREATE USER my_user FOR LOGIN my_login;
```

By default the password must contain characters from three of the following four sets: uppercase letters, lowercase letters, digits, and symbols,
e.g. *C0rdaAP4ssword* is a valid password. Passwords are delimited with single quotes.

You can create schemas for several Corda nodes within the same database (*my_database*),
in which case run the first DDL statement (*CREATE DATABASE my_database;*) only once.

Connect to a user database as the administrator (replace *master* with *my_database* in the connection string).
Run the following script to create a schema and assign user permissions:

```sql
CREATE SCHEMA my_schema;

CREATE USER my_user FOR LOGIN my_login WITH DEFAULT_SCHEMA = my_schema;
GRANT SELECT, INSERT, UPDATE, DELETE, VIEW DEFINITION, ALTER, REFERENCES ON SCHEMA::my_schema TO my_user;
GRANT CREATE TABLE TO my_user;
GRANT CREATE VIEW TO my_user;
```



#### Oracle

This script uses the default tablespace *users* with *unlimited* database space quota assigned to the user.
Revise these settings depending on your nodes sizing requirements.

```sql
CREATE USER my_user IDENTIFIED BY my_password DEFAULT TABLESPACE users QUOTA unlimited ON users;
GRANT CREATE SESSION TO my_user;
GRANT CREATE TABLE TO my_user;
GRANT CREATE VIEW TO my_user;
GRANT CREATE SEQUENCE TO my_user;
GRANT SELECT ON v_$parameter TO my_user;
```



#### PostgreSQL

Connect to the database as an administrator and run the following script to create a node user:

```sql
CREATE USER "my_user" WITH LOGIN PASSWORD 'my_password';
CREATE SCHEMA "my_schema";
GRANT USAGE, CREATE ON SCHEMA "my_schema" TO "my_user";
GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON ALL tables IN SCHEMA "my_schema" TO "my_user";
ALTER DEFAULT privileges IN SCHEMA "my_schema" GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON tables TO "my_user";
GRANT USAGE, SELECT ON ALL sequences IN SCHEMA "my_schema" TO "my_user";
ALTER DEFAULT privileges IN SCHEMA "my_schema" GRANT USAGE, SELECT ON sequences TO "my_user";
ALTER ROLE "my_user" SET search_path = "my_schema";
```

If you provide a custom schema name (different to the user name), then the last statement, setting the search_path,
prevents querying the different default schema search path
([default schema search path](https://www.postgresql.org/docs/9.3/static/ddl-schemas.html#DDL-SCHEMAS-PATH)).



### 2. Corda node configuration

The following updates are required to a nodes filesystem configuration:



* The Corda node configuration file `node.conf` needs to contain JDBC connection properties in the `dataSourceProperties` entry
and other database properties (passed to nodes’ JPA persistence provider or schema creation/upgrade flag) in the `database` entry.
For development convenience the properties are specified in the [deployNodes Cordform task](../../testing.md#testing-cordform-ref) task.

```none
dataSourceProperties = {
   ...
   dataSourceClassName = <JDBC Data Source class name>
   dataSource.url = <JDBC database URL>
   dataSource.user = <Database user>
   dataSource.password = <Database password>
}
database = {
   transactionIsolationLevel = <Transaction isolation level>
   schema = <Database schema name>
   runMigration = true
}
```


See [Node configuration](../setup/corda-configuration-file.md#database-properties-ref) for a complete list of database specific properties, it contains more options useful in case of testing Corda with unsupported databases.
* Set `runMigration` to `true` to allow a Corda node to create database tables upon startup.
* The Corda distribution does not include any JDBC drivers with the exception of the H2 driver.
It is the responsibility of the node administrator or a developer to download the appropriate JDBC driver.
Corda will search for valid JDBC drivers under the `./drivers` subdirectory of the node base directory.
Corda distributed via published artifacts (e.g. added as Gradle dependency) will also search for the paths specified by the `jarDirs`
field of the node configuration.
The `jarDirs` property is a list of paths, separated by commas and wrapped in single quotes e.g. `jarDirs = [ '/lib/jdbc/driver' ]`.
* Corda uses [Hikari Pool](https://github.com/brettwooldridge/HikariCP) for creating connection pools.
To configure a connection pool, the following custom properties can be set in the `dataSourceProperties` section, e.g.:

```groovy
dataSourceProperties = {
   ...
   maximumPoolSize = 10
   connectionTimeout = 50000
}
```





Configuration templates for each database vendor are shown below:


* [H2](#db-dev-setup-configure-node-h2-ref)
* [Azure SQL](#db-dev-setup-configure-node-azure-ref)
* [SQL Server](#db-dev-setup-configure-node-sqlserver-ref)
* [Oracle](#db-dev-setup-configure-node-oracle-ref)
* [PostgreSQL](#db-dev-setup-configure-node-postgresql-ref)



#### H2

By default, nodes store their data in an H2 database.
No database setup is needed. Optionally remote H2 access/port can be configured. See the documentation on [Database access when running H2](../../node-database-access-h2).



#### Azure SQL

Node configuration for Azure SQL:


```groovy
dataSourceProperties = {
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=<my_database>;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    dataSource.user = my_login
    dataSource.password = "my_password"
}
database = {
    transactionIsolationLevel = READ_COMMITTED
    schema = my_schema
    runMigration = true
}
```



Replace the placeholders *<database_server>* and *<my_database>* with appropriate values (*<my_database>* is a user database).
Do not change the default isolation for this database (*READ_COMMITTED*) as the Corda platform has been validated
for functional correctness and performance using this level.
The `database.schema` is the database schema name assigned to the user.
`runMigration` value should be set to *true* when using *administrative* permissions only, otherwise set the value to *false*.

The Microsoft SQL JDBC driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615),
extract the archive and copy the single file *mssql-jdbc-6.4.0.jre8.jar* as the archive comes with two JARs.
[Common Configuration Steps paragraph](#db-setup-developer-step-3-ref) explains the correct location for the driver JAR in the node installation structure.



#### SQL Server

Node configuration for SQL Server:


```groovy
dataSourceProperties = {
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://<host>:<port>;databaseName=my_database"
    dataSource.user = my_login
    dataSource.password = "my_password"
}
database = {
    transactionIsolationLevel = READ_COMMITTED
    schema = my_schema
    runMigration = true
}
```



Replace the placeholders *<host>*, *<port>* with appropriate values, the default SQL Server port is 1433.
By default the connection to the database is not SSL, for securing JDBC connection refer to
[Securing JDBC Driver Applications](https://docs.microsoft.com/en-us/sql/connect/jdbc/securing-jdbc-driver-applications?view=sql-server-2017).

Do not change the default isolation for the database (*READ_COMMITTED*) as the Corda platform has been validated
for functional correctness and performance using this level.
The `runMigration` value should be set to *true* when using *administrative* permissions only, otherwise set the value to *false*.
The `database.schema` is the database schema name assigned to the user.

Microsoft JDBC 6.2 driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=56615),
extract the archive and copy the single file `mssql-jdbc-6.4.0.jre8.jar` to the `drivers` folder, as the archive comes with two JARs.

Ensure JDBC connection properties match the SQL Server setup, especially when trying to reuse the Azure provided SQL JDBC URL
which is invalid for SQL Server.  This may lead to the node failing to start with the message:
*Caused by: org.hibernate.HibernateException: Access to DialectResolutionInfo cannot be null when ‘hibernate.dialect’ not set*.



#### Oracle

Node configuration for Oracle:


```groovy
dataSourceProperties = {
    dataSourceClassName = "oracle.jdbc.pool.OracleDataSource"
    dataSource.url = "jdbc:oracle:thin:@<host>:<port>:<sid>"
    dataSource.user = my_user
    dataSource.password = "my_password"
}
database = {
    transactionIsolationLevel = READ_COMMITTED
    schema = my_user
    runMigration = true
}
```



Replace the placeholders *<host>*, *<port>* and *<sid>* with appropriate values, for a basic Oracle installation the default *<sid>* value is *xe*.
If the user was created with *administrative* permissions the schema name `database.schema` will be the same as the user name (*my_user*).

Do not change the default isolation for this database (*READ_COMMITTED*) as the Corda platform has been validated for functional correctness and performance using this level.
The `runMigration` value must be set to *true* when the database user has *administrative* permissions and set to *false* when using *restricted* permissions.

Copy the Oracle JDBC driver *ojdbc6.jar* for 11g RC2 or *ojdbc8.jar* for Oracle 12c to the node directory `drivers`.



#### PostgreSQL

Node configuration for PostgreSQL:


```none
dataSourceProperties = {
    dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
    dataSource.url = "jdbc:postgresql://<host>:<port>/<database>"
    dataSource.user = my_user
    dataSource.password = "my_password"
}
database = {
    transactionIsolationLevel = READ_COMMITTED
    schema = my_schema
    runMigration = true
}
```



Replace the placeholders *<host>*, *<port>* and *<database>* with appropriate values.
The `database.schema` is the database schema name assigned to the user.
The value of `database.schema` is automatically wrapped in double quotes to preserve case-sensitivity
(e.g. *AliceCorp* becomes *AliceCorp*, without quotes PostgresSQL would treat the value as *alicecorp*),
this behaviour differs from Corda Open Source where the value is not wrapped in double quotes.

Do not change the default isolation for this database (*READ_COMMITTED*) as the Corda platform has been validated for functional correctness and performance using this level.
The `runMigration` value should be set to *true* when using *administrative* permissions only, otherwise set the value to *false*.

Copy the PostgreSQL JDBC Driver *42.2.8* version *JDBC 4.2* to the node directory `drivers`.



### 3. Start the node to auto-create schema objects

The node will create all database schema objects upon startup, as `runMigration` is set to `true`.
Additionally, the node will create any tables for CorDapps containing Liquibase database migration scripts.



## Database schema update

As the Corda node is configured to automatically run migrations on startup,
no additional database update steps are required when upgrading Corda.
See the [Corda node upgrade notes](cm-upgrading-node.md#node-upgrade-notes-update-database-ref) for more information.



## Database schema setup when deploying a new CorDapp

The procedure for Cordapp deployment is the same as for production systems
apart from a simplified database update step.
A CorDapp, which stores data in a custom table, should contain an embedded Liquibase database migration script.
[Liquibase](http://www.liquibase.org) is used by Corda for the database schema management.

To allow a Corda node to auto-update the database based on the content from a database migration script,
ensure that:


* the node can connect to the  database with **administrative permissions** or runs with the default embedded H2 database.
* the node configuration `node.conf` file contains the *runMigration* option set to *true*:
```groovy
database = {
    runMigration = true
    # other properties
}
```





Those requirements should already be set during [the initial Corda node configuration](#db-setup-developer-step-3-ref).

You can optionally check if a CorDapp which is expected to store data in custom tables, is correctly built.
To check the presence of script files inside *migration* directory,
verify the content of the CorDapp JAR file with Java `jar` command, e.g. for Linux:


>
```bash
jar -tf <cordapp.jar> | grep -E 'migration.*\.(xml|yml|sql)'
```
>

{{< note >}}
It is possible that a CorDapp is shipped without a database migration script when it should contain one.
Liquibase database migration scripts for CorDapps are not used when a node runs with the default embeeded H2 database.

{{< /note >}}



## Database schema update when upgrading a CorDapp

When an upgraded CorDapp contains a requires a database schema changes, the
database is automatically updated during a node restart, see:
[database schema update for a new CorDapp](#node-database-developer-database-schema-setup-when-deploying-a-new-cordapp-ref).



## Database schema cleanup

When developing/testing CorDapps you may need cleanup the database between test runs
(e.g. when running using the Gradle plugin `Cordform` `deployNodes`).


### SQL Azure and SQL Server

To remove node tables run the following SQL script against a user database:


```sql
DROP TABLE my_schema.DATABASECHANGELOG;
DROP TABLE my_schema.DATABASECHANGELOGLOCK;
DROP TABLE my_schema.NODE_ATTACHMENTS_SIGNERS;
DROP TABLE my_schema.NODE_ATTACHMENTS_CONTRACTS;
DROP TABLE my_schema.NODE_ATTACHMENTS;
DROP TABLE my_schema.NODE_CHECKPOINTS;
DROP TABLE my_schema.NODE_TRANSACTIONS;
DROP TABLE my_schema.NODE_MESSAGE_IDS;
DROP TABLE my_schema.VAULT_STATES;
DROP TABLE my_schema.NODE_OUR_KEY_PAIRS;
DROP TABLE my_schema.NODE_SCHEDULED_STATES;
DROP TABLE my_schema.VAULT_FUNGIBLE_STATES_PARTS;
DROP TABLE my_schema.VAULT_LINEAR_STATES_PARTS;
DROP TABLE my_schema.VAULT_FUNGIBLE_STATES;
DROP TABLE my_schema.VAULT_LINEAR_STATES;
DROP TABLE my_schema.VAULT_TRANSACTION_NOTES;
DROP TABLE my_schema.NODE_LINK_NODEINFO_PARTY;
DROP TABLE my_schema.NODE_INFO_PARTY_CERT;
DROP TABLE my_schema.NODE_INFO_HOSTS;
DROP TABLE my_schema.NODE_INFOS;
DROP TABLE my_schema.CP_STATES;
DROP TABLE my_schema.NODE_CONTRACT_UPGRADES;
DROP TABLE my_schema.NODE_IDENTITIES;
DROP TABLE my_schema.NODE_NAMED_IDENTITIES;
DROP TABLE my_schema.NODE_NETWORK_PARAMETERS;
DROP TABLE my_schema.NODE_PROPERTIES;
DROP TABLE my_schema.CONTRACT_CASH_STATES;
DROP TABLE my_schema.NODE_MUTUAL_EXCLUSION;
DROP TABLE my_schema.PK_HASH_TO_EXT_ID_MAP;
DROP TABLE my_schema.STATE_PARTY;
DROP VIEW my_schema.V_PKEY_HASH_EX_ID_MAP;
DROP SEQUENCE my_schema.HIBERNATE_SEQUENCE;
```



Additional tables for a Notary node:


```sql
DROP TABLE IF EXISTS my_schema.NODE_NOTARY_REQUEST_LOG;
DROP TABLE IF EXISTS my_schema.NODE_NOTARY_COMMITTED_STATES;
DROP TABLE IF EXISTS my_schema.NODE_NOTARY_COMMITTED_TXS;
DROP TABLE IF EXISTS my_schema.NODE_BFT_COMMITTED_STATES;
DROP TABLE IF EXISTS my_schema.NODE_BFT_COMMITTED_TXS;
DROP TABLE IF EXISTS my_schema.NODE_RAFT_COMMITTED_STATES;
DROP TABLE IF EXISTS my_schema.NODE_RAFT_COMMITTED_TXS;
```



Also delete CorDapp specific tables.

If you need to remove the schema and users, run the following script as a database administrator on a user database:


```sql
DROP SCHEMA my_schema;
DROP USER my_user;
DROP USER IF EXISTS my_admin_user;
```



To remove users’ logins, run the following script as a database administrator on the master database
(skip the second statement if you haven’t created a *my_admin_login* login):


```sql
DROP LOGIN my_login;
DROP LOGIN my_admin_login;
```




### Oracle

To remove node tables run the following SQL script:


```sql
DROP TABLE my_user.DATABASECHANGELOG CASCADE CONSTRAINTS;
DROP TABLE my_user.DATABASECHANGELOGLOCK CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_ATTACHMENTS_SIGNERS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_ATTACHMENTS_CONTRACTS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_ATTACHMENTS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_CHECKPOINTS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_TRANSACTIONS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_MESSAGE_IDS CASCADE CONSTRAINTS;
DROP TABLE my_user.VAULT_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_OUR_KEY_PAIRS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_SCHEDULED_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.VAULT_FUNGIBLE_STATES_PARTS CASCADE CONSTRAINTS;
DROP TABLE my_user.VAULT_LINEAR_STATES_PARTS CASCADE CONSTRAINTS;
DROP TABLE my_user.VAULT_FUNGIBLE_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.VAULT_LINEAR_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.VAULT_TRANSACTION_NOTES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_LINK_NODEINFO_PARTY CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_INFO_PARTY_CERT CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_INFO_HOSTS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_INFOS CASCADE CONSTRAINTS;
DROP TABLE my_user.CP_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_CONTRACT_UPGRADES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_IDENTITIES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_NAMED_IDENTITIES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_NETWORK_PARAMETERS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_PROPERTIES CASCADE CONSTRAINTS;
DROP TABLE my_user.CONTRACT_CASH_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_MUTUAL_EXCLUSION CASCADE CONSTRAINTS;
DROP TABLE my_user.PK_HASH_TO_EXT_ID_MAP;
DROP TABLE my_user.STATE_PARTY;
DROP VIEW my_user.V_PKEY_HASH_EX_ID_MAP;
DROP SEQUENCE my_user.HIBERNATE_SEQUENCE;
```



Additional tables for a Notary node:


```sql
DROP TABLE my_user.NODE_NOTARY_REQUEST_LOG CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_NOTARY_COMMITTED_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_NOTARY_COMMITTED_TXS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_BFT_COMMITTED_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_BFT_COMMITTED_TXS CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_RAFT_COMMITTED_STATES CASCADE CONSTRAINTS;
DROP TABLE my_user.NODE_RAFT_COMMITTED_TXS CASCADE CONSTRAINTS;
```



Also delete CorDapps specific tables.


### PostgreSQL

To remove node and CorDapp specific tables run the following SQL script:


```sql
DROP SCHEMA IF EXISTS "my_schema" CASCADE;
DROP OWNED BY "my_user";
```
