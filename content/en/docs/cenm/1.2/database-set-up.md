---
aliases:
- /releases/release-1.2/database-set-up.html
- /docs/cenm/head/database-set-up.html
- /docs/cenm/database-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-database-set-up
    parent: cenm-1-2-operations
    weight: 180
tags:
- database
- set
title: CENM Databases
---


# CENM Databases

There are currently two types of Corda Enterprise Network Manager database:

1. **Identity Manager**
- Used by the Identity Manager service. Contains information relating to certificate signing requests of nodes wanting
to join the network as well as information regarding revocation of nodes from the network.

2. **Network Map**
- Used by the Network Map service. Contains information relating to the current participants on the network, the current
network parameters and any pending parameter updates.

Due to the way the migrations are defined, the services *must* use separate DB schemas (either in the same DB instance
or in completely separate instances). Attempting to run an Identity Manager and Network Map service that share the same
DB schema will result in errors.


## Supported Databases

Corda Enterprise Network Manager currently supports the following databases:


* Microsoft SQL Server (deployed locally or through Azure)
* PostgreSQL
* Oracle DB

The appropriate JDBC driver JAR file must be provided and its location should be specified in the service configuration.

H2 is also supported “out of the box”, without providing an external JDBC driver jar.


{{< warning >}}
H2 as a database is not considered to be suitable for production.

{{< /warning >}}


{{< note >}}
CENM uses H2 version 1.4.197, which does not support some SQL commands (e.g. *SELECT … FOR UPDATE*).
Hence, the sql command *SELECT_FOR_UPDATE_MVCC=FALSE* is patched to the H2 connection url string to circumvent
any potential errors stemming from the former.

{{< /note >}}

## Database Schema Setup

This document provides instructions describing how to create database schemas (user permissions, the CENM service
tables, and other database objects), and how to configure CENM services to connect to a database with *restricted
permissions* for production use.

Note that in contrast to Corda nodes, CENM schema creation/migration is done by the CENM services rather
than a separate tool. The expectation is that the services are configured to connect as a privileged
user when doing this creation/migration, and a more restricted user for production use. This is covered
in more depth further down.

Setting up a CENM service (Identity Manager / Network Map) to connect to a database requires:


* [Creating a database user with schema permissions](#1-creating-a-database-user-with-schema-permissions)
* [Database table creation](#2-database-schema-creation)
* [CENM service configuration changes](#3-cenm-service-configuration)
* [Database configuration](#4-database-configuration)



### 1. Creating a database user with schema permissions

A database administrator must create a database user and a schema namespace with **restricted permissions**.
This grants the user access to DML execution only (to manipulate data itself e.g. select/delete rows).
This permission set is recommended for production environments.

{{< note >}}
This step refers to *schema* as a namespace with a set of permissions,
the schema content (tables, indexes) is created in [the next step](#db-setup-step-2-ref).

{{< /note >}}
Variants of Data Definition Language (DDL) scripts are provided for each supported database vendor.
The example permissions scripts have no group roles and do not specify physical database settings (such as the max disk space quota for a user).
The scripts and service configuration snippets contain placeholder values; *my_login* for login, *my_user*/*my_admin_user* for users,
*my_password* for password, and *my_schema* for the schema name. These values are for illustrative purposes only,
please replace them with the actual values configured for your environment or environments.


{{< warning >}}
Each CENM service needs to use a separate database user and schema where multiple services are hosted on the same database instance.

{{< /warning >}}


Creating database users with schema permissions for:


* [Azure SQL](#azure-sql)
* [SQL Server](#sql-server)
* [Oracle](#oracle)
* [PostgreSQL](#postgresql)



#### Azure SQL

Two database users needed to be created; the first one with administrative permissions to create schema objects,
and the second with restrictive permissions for a CENM service instance.
The schema objects are created by a separate user rather than a default database administrator. This ensures the correct schema namespace
is used.

Connect to the master database as an administrator
(e.g. *jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=master;[…]*).
Run the following script to create both users and their logins:

```sql
CREATE LOGIN my_admin_login WITH PASSWORD = 'my_password';
CREATE USER my_admin_user FOR LOGIN my_admin_login;
CREATE LOGIN my_login WITH PASSWORD = 'my_password';
CREATE USER my_user FOR LOGIN my_login;
```

By default the password must contain characters from three of the following four sets: uppercase letters, lowercase letters, digits, and symbols,
e.g. *C3NMP4ssword* is a valid password. Passwords are delimited with single quotes.
Use different passwords for *my_admin_user* and *my_user*.

Connect to a user database as the administrator (replace *master* with a user database in the connection string).

Run the following script to create a schema and assign user permissions:

```sql
CREATE SCHEMA my_schema;
```

After creating the schema you may need to commit the change - for example, with the `GO`
command on Microsoft tools, or `commit;` on other tools.

Run the following script to assign user permissions:

```sql
CREATE USER my_admin_user FOR LOGIN my_admin_login WITH DEFAULT_SCHEMA = my_schema;
GRANT ALTER ON SCHEMA::my_schema TO my_admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE, VIEW DEFINITION, REFERENCES ON SCHEMA::my_schema TO my_admin_user;
GRANT CREATE TABLE TO my_admin_user;
GRANT CREATE VIEW TO my_admin_user;
CREATE USER my_user FOR LOGIN my_login WITH DEFAULT_SCHEMA = my_schema;
GRANT SELECT, INSERT, UPDATE, DELETE, VIEW DEFINITION, REFERENCES ON SCHEMA::my_schema TO my_user;
```



#### SQL Server

Two database users need to be created; the first with administrative permissions to create schema objects,
the second with restrictive permissions for a CENM service instance.
The schema objects are created by a separate user rather than a default database administrator. This ensures the correct schema namespace
is used.

Connect to a master database as an administrator (e.g. *jdbc:sqlserver://<host>:<port>;databaseName=master*).
Run the following script to create a database, a user and a login:

```sql
CREATE DATABASE my_database;
CREATE LOGIN my_admin_login WITH PASSWORD = 'my_password', DEFAULT_DATABASE = my_database;
CREATE USER my_admin_user FOR LOGIN my_admin_login;
CREATE LOGIN my_login WITH PASSWORD = 'my_password', DEFAULT_DATABASE = my_database;
CREATE USER my_user FOR LOGIN my_login;
```

By default the password must contain characters from three of the following four sets: uppercase letters, lowercase letters, digits, and symbols,
e.g. *C3NMP4ssword* is a valid password. Passwords are delimited with single quotes.
Use different passwords for *my_admin_user* and *my_user*.

You can create schemas for several instances of CENM services within the same database (*my_database*),
in which case run the first DDL statement (*CREATE DATABASE my_database;*) only once.

Connect to a user database as the administrator (replace *master* with *my_database* in the connection string).
Run the following script to create a schema and assign user permissions:

```sql
CREATE SCHEMA my_schema;
```

After creating the schema you may need to commit the change - for example, with the `GO`
command on Microsoft tools, or `commit;` on other tools.

Run the following script to assign user permissions:

```sql
CREATE USER my_admin_user FOR LOGIN my_admin_login WITH DEFAULT_SCHEMA = my_schema;
GRANT ALTER ON SCHEMA::my_schema TO my_admin_user;
GRANT SELECT, INSERT, UPDATE, DELETE, VIEW DEFINITION, REFERENCES ON SCHEMA::my_schema TO my_admin_user;
GRANT CREATE TABLE TO my_admin_user;
GRANT CREATE VIEW TO my_admin_user;
CREATE USER my_user FOR LOGIN my_login WITH DEFAULT_SCHEMA = my_schema;
GRANT SELECT, INSERT, UPDATE, DELETE, VIEW DEFINITION, REFERENCES ON SCHEMA::my_schema TO my_user;
```



#### Oracle

{{< note >}}
CENM has been tested with Oracle database versions 12cR2 and 11gR2

{{< /note >}}
CENM databases require some VARCHAR2 or NVARCHAR2 column types to store more than 2000 characters,
ensure the database instance is configured to use extended data types. For example, for Oracle 12.1 refer to
[MAX_STRING_SIZE](https://docs.oracle.com/database/121/REFRN/GUID-D424D23B-0933-425F-BC69-9C0E6724693C.htm#REFRN10321).

The recommended configuration for CENM with Oracle is a one to one relationship between schemas and user accounts,
so the user has full control over that schema. In order to restrict the permissions to the database, two users need to be created,
one with administrative permissions (*my_admin_user* in the SQL script) and the other with read only permissions (*my_user* in the SQL script).
A database administrator can create schema objects (tables/sequences) via a user with administrative permissions.
The CENM service instance accesses the schema created by the administrator via a user with restricted permissions, allowing them to select/insert/delete data only.
For Oracle databases, those permissions (*SELECT*, *INSERT*, *UPDATE*, *DELETE*) need to be granted explicitly for each table.

The tablespace size in the sample script below is unlimited, adjust the value (e.g. 100M, 1 GB)
depending on your nodes sizing requirements.
The script uses the default tablespace *users* with *unlimited* database space quota assigned to the user.
Revise these settings depending on your nodes sizing requirements.

Run this script as database administrator:

```sql
CREATE USER my_admin_user IDENTIFIED BY my_password DEFAULT TABLESPACE users QUOTA unlimited ON users;
GRANT CREATE SESSION TO my_admin_user;
GRANT CREATE TABLE TO my_admin_user;
GRANT CREATE VIEW TO my_admin_user;
GRANT CREATE SEQUENCE TO my_admin_user;
GRANT SELECT ON v_$parameter TO my_admin_user;
```

The permissions for the CENM service instance user to access database objects will be assigned in [the following step](#db-setup-step-2-oracle-extra-step-ref)
after the database objects are created.

The last permission for the *v_$parameter* view is needed when a database is running in
[Database Compatibility mode](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/upgrd/what-is-oracle-database-compatibility.html).



#### PostgreSQL

Connect to the database as an administrator and run the following script to create a CENM service instance user:

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



## 2. Database schema creation

The CENM services should first be deployed with database administrator credentials specified in the config files (`database.user`, `database.password`).
Given that the schema exists and the user has administrative permissions, the Liquibase migrations will run on
startup and automatically create the tables under the schema.

Once the tables have been created, the database user and password settings in the service config file should be
substituted for the CENM service instance user credentials with restricted permissions.


{{< warning >}}
Ensure that `database.runMigration` is set to false for users with restricted permissions.

{{< /warning >}}




### 2.1. Add permission to use tables

For some databases the specific permissions can be assigned only after the tables are created.
This step is required for Oracle databases only.


#### Oracle

Connect to the database as administrator and run the following DDL scripts:


##### Identity Manager


```sql
CREATE USER my_user identified by my_password;
GRANT CREATE SESSION TO my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOG to my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOGLOCK to my_user;
GRANT SELECT ON my_admin_user.HIBERNATE_SEQUENCE TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.certificate_revocation_list TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.certificate_revocation_request TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.certificate_data TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.certificate_signing_request TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.private_network_global TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.migration TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.REVINFO TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.workflow_csr TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.workflow_crr TO my_user;
```




##### Network Map

Run the script after running the Liquibase migrations, by setting the initial network parameters
using a configuration file with administrative database user credentials.


```sql
CREATE USER my_user identified by my_password;
GRANT CREATE SESSION TO my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOG TO my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOGLOCK TO my_user;
GRANT SELECT ON my_admin_user.HIBERNATE_SEQUENCE TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.certificate_chain TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.network_map TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.network_parameters TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.network_parameters_update TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.node_info TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.private_network TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.migration TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.node_info_staging TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.node_info_quarantine TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.REVINFO TO my_user;
```





## 3. CENM service configuration

The following updates are required to the filesystem of a CENM service instance:



* The CENM service config file `identitymanager.conf` or `networkmap.conf` needs to contain JDBC connection properties
in the `database` entry along with other database properties (passed to a CENM service JPA persistence provider or schema creation/upgrade flag).

```groovy
database = {
   ...
   jdbcDriver = path/to/jdbcDriver.jar
   driverClassName = <JDBC driver class name>
   url = <JDBC database URL>
   user = <Database user>
   password = <Database password
   transactionIsolationLevel = <Transaction isolation level>
   schema = <Database schema name>
   runMigration = false
}
```


{{< note >}}
The [CENM Database Configuration](config-database.md) doc page contains a complete list of database specific properties.{{< /note >}}

* The restricted CENM service instance database user has no permissions to alter a database schema, so `runMigration` is set to `false`.
* The CENM distribution does not include any JDBC drivers with the exception of the H2 driver.
It is the responsibility of the CENM service administrator or a developer to install the appropriate JDBC driver.
* Corda uses [Hikari Pool](https://github.com/brettwooldridge/HikariCP) for creating connection pools.
To configure a connection pool, the following custom properties can be set in the `database` section, e.g.:

```groovy
database = {
   ...
   additionalProperties = {
       maximumPoolSize = 10
       connectionTimeout = 50000
   }
}
```





Configuration templates for each database vendor are shown below:


* [Azure SQL](#azure-sql-1)
* [SQL Server](#sql-server-1)
* [Oracle](#oracle-1)
* [PostgreSQL](#postgresql-1)



### Azure SQL

Example CENM services configuration file for Azure SQL - initial deployment with administrative permissions:


```groovy
database = {
    jdbcDriver = path/to/mssql-jdbc-x.x.x.jre8.jar
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    url = "jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=<my_database>;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    user = my_admin_login
    password = "my_admin_password"
    schema = my_schema
    runMigration = true
}
```



Example CENM service configuration file for Azure SQL *restrictive permissions* - CENM service instance database user with restrictive permissions:


```groovy
database = {
    jdbcDriver = path/to/mssql-jdbc-x.x.x.jre8.jar
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    url = "jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=<my_database>;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    user = my_login
    password = "my_password"
    schema = my_schema
    runMigration = false
}
```



Replace placeholders *\<database_server\>* and *\<my_database\>* with appropriate values (*\<my_database\>* is a user database).
The `database.schema` is the database schema name assigned to the user.

The Microsoft SQL JDBC driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=55539),
extract the archive and copy the single file *mssql-jdbc-6.2.2.jre8.jar* (the archive comes with two JARs).
[Common Configuration Steps paragraph](#db-setup-step-3-ref) explains the correct location for the driver JAR in the CENM service installation structure.



### SQL Server

Example CENM services configuration file for SQL Server - initial deployment with administrative permissions:


```groovy
database = {
    jdbcDriver = path/to/mssql-jdbc-x.x.x.jre8.jar
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    url = "jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=<my_database>;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    user = my_admin_login
    password = "my_admin_password"
    schema = my_schema
    runMigration = true
}
```



Example CENM service configuration file for SQL Server - CENM service instance database user with restricted permissions:


```groovy
database = {
    jdbcDriver = path/to/mssql-jdbc-x.x.x.jre8.jar
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    url = "jdbc:sqlserver://<host>:<port>;databaseName=my_database"
    user = my_login
    password = "my_password"
    schema = my_schema
    runMigration = false
}
```



Replace placeholders *\<host\>* and *\<port\>* with appropriate values (the default SQL Server port is 1433).
By default the connection to the database is not SSL. To secure the JDBC connection, refer to
[Securing JDBC Driver Applications](https://docs.microsoft.com/en-us/sql/connect/jdbc/securing-jdbc-driver-applications?view=sql-server-2017).

The Microsoft JDBC 6.2 driver can be downloaded from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=55539),
extract the archive and copy the single file `mssql-jdbc-6.2.2.jre8.jar` (the archive comes with two JARs).
[Common Configuration Steps](#db-setup-step-3-ref) explains the correct location for the driver JAR in the CENM service installation structure.

Ensure JDBC connection properties match the SQL Server setup. Especially when trying to reuse Azure SQL JDBC URLs
which are invalid for SQL Server. This may lead to CENM failing to start with message:
*Caused by: org.hibernate.HibernateException: Access to DialectResolutionInfo cannot be null when ‘hibernate.dialect’ not set*.



### Oracle

Example CENM service configuration file for Oracle DB - initial deployment with administrative permissions:

```groovy
database = {
    jdbcDriver = path/to/ojdbcx.jar
    driverClassName = "oracle.jdbc.driver.OracleDriver"
    url = "jdbc:oracle:thin:@<host>:<port>:<sid>"
    user = my_admin_user
    password = "my_admin_password"
    schema = my_admin_user
}
```

Example CENM service configuration file for Oracle DB - CENM service instance database user with restrictive permissions:

```groovy
database = {
    jdbcDriver = path/to/ojdbcx.jar
    driverClassName = "oracle.jdbc.driver.OracleDriver"
    url = "jdbc:oracle:thin:@<host>:<port>:<sid>"
    user = my_user
    password = "my_password"
    runMigration = false
    schema = my_admin_user
    additionalProperties {
        connectionInitSql="alter session set current_schema=my_admin_user"
    }
}
```

Replace the placeholders *\<host\>*, *\<port\>* and *\<sid\>* with appropriate values. (For a basic Oracle installation, the default *<sid>* value is *xe*.)
If the user was created with *administrative* permissions, the schema name `database.schema` is equal to the user name (*my_user*).

When connecting with a database user with restricted permissions, all queries need to be prefixed with the other schema name.
Set the `database.schema` value to *my_admin_user*.
CENM doesn’t guarantee prefixing all SQL queries with the schema namespace.
The additional configuration entry `connectionInitSql` sets the current schema to the admin user (*my_user*) on connection to the database.

The transaction isolation level is set by CENM to *READ_COMMITTED*, and attempting to set another
isolation level in the configuration will result in an error. This is intentional behaviour, as
*READ_UNCOMMITTED* results in inconsistent data reads, *REPEATABLE_READ* and *SERIALIZABLE* are not compatible
with Corda.

Use Oracle JDBC driver *ojdbc6.jar* for 11g RC2 or *ojdbc8.jar* for Oracle 12c.
Database schema name can be set in JDBC URL string e.g. currentSchema=my_schema.



### PostgreSQL

Example CENM service configuration for PostgreSQL:


```none
database = {
    jdbcDriver = path/to/postgresql-xx.x.x.jar
    driverClassName = "org.postgresql.Driver"
    url = "jdbc:postgresql://<host>:<port>/<database>"
    user = my_user
    password = "my_password"
    schema = my_schema
}
```



Replace the placeholders *\<host\>*, *\<port\>*, and *\<database\>* with appropriate values.
The `database.schema` is the database schema name assigned to the user.
The value of `database.schema` is automatically wrapped in double quotes to preserve case-sensitivity
(without quotes, PostgresSQL would treat *AliceCorp* as the value *alicecorp*).



## 4. Database configuration

Additional vendor specific database configuration.


### SQL Server

The database collation should be *case insensitive*, refer to
[Server Configuration documentation](https://docs.microsoft.com/en-us/sql/sql-server/install/server-configuration-collation?view=sql-server-2014&viewFallbackFrom=sql-server-2017).


### Oracle

To allow *VARCHAR2* and *NVARCHAR2* column types to store more than 2000 characters, ensure the database instance is configured to use
extended data types. For example, for Oracle 12.1 refer to [MAX_STRING_SIZE](https://docs.oracle.com/database/121/REFRN/GUID-D424D23B-0933-425F-BC69-9C0E6724693C.htm#REFRN10321).


## 5. Tables

Note that `<SCHEMA_NAME>` below is a placeholder value representing the actual name for the appropriate schema.


### Identity Manager

The following is the list of tables created by the Identity Manager service:

```sql
<SCHEMA_NAME>.DATABASECHANGELOG
<SCHEMA_NAME>.DATABASECHANGELOGLOCK
<SCHEMA_NAME>.certificate_data
<SCHEMA_NAME>.certificate_revocation_list
<SCHEMA_NAME>.certificate_revocation_request
<SCHEMA_NAME>.certificate_signing_request
<SCHEMA_NAME>.private_network_global
<SCHEMA_NAME>.workflow_csr
<SCHEMA_NAME>.workflow_crr
<SCHEMA_NAME>.migration
<SCHEMA_NAME>.REVINFO
```


### Network Map

The following is the list of tables created by the Network Map service:

```sql
<SCHEMA_NAME>.DATABASECHANGELOG
<SCHEMA_NAME>.DATABASECHANGELOGLOCK
<SCHEMA_NAME>.certificate_chain
<SCHEMA_NAME>.network_map
<SCHEMA_NAME>.network_parameters
<SCHEMA_NAME>.network_parameters_update
<SCHEMA_NAME>.node_info
<SCHEMA_NAME>.private_network
<SCHEMA_NAME>.node_info_staging
<SCHEMA_NAME>.node_info_quarantine
<SCHEMA_NAME>.migration
<SCHEMA_NAME>.REVINFO
```


## Clearing The DB

Clearing the DB will depend upon the exact database that you are running on, however the general scripts for clearing
the Identity Manager and Network Map DB are below:


### SQL Azure & SQL Server


#### Identity Manager

```sql
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOGLOCK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_revocation_list;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_revocation_request;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_data;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_signing_request;
DROP TABLE IF EXISTS <SCHEMA_NAME>.private_network_global;
DROP TABLE IF EXISTS <SCHEMA_NAME>.workflow_csr;
DROP TABLE IF EXISTS <SCHEMA_NAME>.workflow_crr;
DROP TABLE IF EXISTS <SCHEMA_NAME>.migration;
DROP TABLE IF EXISTS <SCHEMA_NAME>.REVINFO;
DROP SEQUENCE IF EXISTS <SCHEMA_NAME>.hibernate_sequence;
```


#### Network Map

```sql
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOGLOCK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_chain;
DROP TABLE IF EXISTS <SCHEMA_NAME>.network_map;
DROP TABLE IF EXISTS <SCHEMA_NAME>.network_parameters;
DROP TABLE IF EXISTS <SCHEMA_NAME>.network_parameters_update;
DROP TABLE IF EXISTS <SCHEMA_NAME>.node_info;
DROP TABLE IF EXISTS <SCHEMA_NAME>.private_network;
DROP TABLE IF EXISTS <SCHEMA_NAME>.migration;
DROP TABLE IF EXISTS <SCHEMA_NAME>.node_info_staging;
DROP TABLE IF EXISTS <SCHEMA_NAME>.node_info_quarantine;
DROP TABLE IF EXISTS <SCHEMA_NAME>.REVINFO;
DROP SEQUENCE IF EXISTS <SCHEMA_NAME>.hibernate_sequence;
```


### Oracle


#### Identity Manager

```sql
DROP TABLE <IM_ADMIN_USER>.DATABASECHANGELOG CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.DATABASECHANGELOGLOCK CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.certificate_revocation_list CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.certificate_revocation_request CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.certificate_data CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.certificate_signing_request CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.private_network_global CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.workflow_csr;
DROP TABLE <IM_ADMIN_USER>.workflow_crr;
DROP TABLE <IM_ADMIN_USER>.migration CASCADE CONSTRAINTS;
DROP TABLE <IM_ADMIN_USER>.REVINFO;
DROP SEQUENCE <IM_ADMIN_USER>.hibernate_sequence;
```


#### Network Map

```sql
DROP TABLE <NM_ADMIN_USER>.DATABASECHANGELOG CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.DATABASECHANGELOGLOCK CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.certificate_chain CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.network_map CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.network_parameters CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.network_parameters_update CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.node_info CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.private_network CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.migration CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.node_info_staging CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.node_info_quarantine CASCADE CONSTRAINTS;
DROP TABLE <NM_ADMIN_USER>.REVINFO;
DROP SEQUENCE <NM_ADMIN_USER>.hibernate_sequence;
```


### PostgreSQL

To remove service tables run the following SQL script:


```sql
DROP SCHEMA IF EXISTS "my_schema" CASCADE;
```
