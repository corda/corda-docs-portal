---
aliases:
- /database-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-database-set-up
    parent: cenm-1-4-operations
    weight: 180
tags:
- database
- set
title: CENM Databases
---


# CENM Databases

There are currently four types of CENM database schemas:

*  The **Identity Manager** database schema is used by the [Identity Manager Service](identity-manager.md). It contains information relating to:
    * Certificate signing requests of nodes wanting to join the network.
    * Requests to revocation of nodes on the network.

*  The **Network Map** database schema is used by the [Network Map Service](network-map.md). It contains information relating to:
    * The current participants on the network.
    * The current network parameters.
    * Any pending network parameter updates.

*  The **Zone** database schema is used by the [Zone Service](zone-service.md). It contains information relating to:
    * External addresses of services on the network.
    * Configurations of other services on the network.

*  The **Auth** database schema is used by the [Auth Service](auth-service.md) to store RBAC data (users, permissions, groups).

The services **must** use separate database schemas (either in the same database instance or in completely separate instances) due to the way the migrations are defined. If you try and run an Identity Manager Service, a Network Map Service, a Zone Service, or an Auth Service that shares the same database schema, it will result in errors.


## Supported Databases

CENM currently supports the following databases:

* PostgreSQL 9.6 (JDBC 42.2.8)
* PostgreSQL 10.10 (JDBC 42.2.8)
* PostgreSQL 11.5 (JDBC 42.2.8)
* PostgreSQL 12.2 (JDBC 42.2.8)
* SQL Server 2017 (Microsoft JDBC Driver 6.4)
* Oracle 11gR2 (Oracle JDBC 6)
* Oracle 12cR2 (Oracle JDBC 8)

The appropriate JDBC driver `.jar` file must be provided and its location should be specified in the service configuration.

{{< warning >}}
H2 database should only be used for testing. The JDBC driver is shipped as part of the service `.jar` files and does not require an external JDBC driver. It is not supported for use in production.
{{< /warning >}}

{{< note >}}
CENM uses H2 version 1.4.197, which does not support some SQL commands (e.g. *SELECT … FOR UPDATE*).
Hence, the SQL command *SELECT_FOR_UPDATE_MVCC=FALSE* is patched to the H2 connection url string to circumvent
any potential errors stemming from the former version.

{{< /note >}}

## Database Schema Setup

This section describes the processes for:
* Creating database schemas such as:
    * User permissions
    * The CENM service tables
    * Other database objects
* Configuring CENM services to connect to a database with *restricted
permissions* for production use.

{{< note >}}
In contrast to Corda nodes, CENM schema creation/migration is done by the CENM services rather
than a separate tool. The services are expected to be configured for you to connect as a privileged
user when doing this creation/migration, and as a more restricted user for production use.
This is covered in <mark>more depth</mark> under [Database Migration](#5-database-migration).
{{< /note >}}

To set up a database that the service will use, and to configure the service to connect to it after that, follow the steps below.


* [Create a database user with schema permissions](#1-create-a-database-user-with-schema-permissions)
* [Create the database tables](#2-database-schema-creation)
* [CENM service configuration changes](#3-cenm-service-configuration)
* [Database configuration](#4-database-configuration)


### 1. Create a database user with schema permissions

A database administrator must create a database user and a schema namespace with **restricted permissions**.
This grants the user access to Data Manipulation Language (DML) execution only (to manipulate data itself - for example, select/delete rows). This permission set is recommended for production environments.

{{< note >}}
This step refers to *schema* as a namespace with a set of permissions. The schema content (tables, indexes) is created in [the next step](#2-database-schema-creation).
{{< /note >}}

Variants of Data Definition Language (DDL) scripts are provided for each supported database vendor.
The example permissions scripts have no group roles and do not specify physical database settings (such as the maximum disk space quota allocated for the database user).
The scripts and service configuration snippets contain placeholder values, as follows:

* *my_login* for login
* *my_user* / *my_admin_user* for users
* *my_password* for password
* *my_schema* for the schema name

{{< note >}}
These values are for illustrative purposes only. Replace them with the actual values configured for your environment or environments.
{{< /note >}}

{{< warning >}}
Each CENM service needs to use a separate database user and schema where multiple services are hosted on the same database instance.
{{< /warning >}}

Create database users with schema permissions for:

* [Azure SQL](#azure-sql)
* [SQL Server](#sql-server)
* [Oracle](#oracle)
* [PostgreSQL](#postgresql)


#### Azure SQL

Create two database users where the first one has permissions to create schema objects
and the second one has restricted permissions for a CENM service instance.
The schema objects are created by a separate user rather than a default database administrator. This ensures the correct schema namespace is used.

1. Connect to the master database as an administrator - for example:

```sql
jdbc:sqlserver://<database_server>.database.windows.net:1433;databaseName=master;[…]
```

2. Run the following script to create both users and their logins:

```sql
CREATE LOGIN my_admin_login WITH PASSWORD = 'my_password';
CREATE USER my_admin_user FOR LOGIN my_admin_login;
CREATE LOGIN my_login WITH PASSWORD = 'my_password';
CREATE USER my_user FOR LOGIN my_login;
```

Passwords must contain characters from three of the following four sets: uppercase letters, lowercase letters, digits, and symbols. For example, *C3NMP4ssword* is a valid password. Passwords are delimited with single quotes. Use different passwords for *my_admin_user* and *my_user*.

3. Connect to a user database as database administrator (replace *master* with a user database in the connection string).

4. Run the following script to create a schema:

```sql
CREATE SCHEMA my_schema;
```

After creating the schema you may need to commit the change - for example, with the `GO`
command on Microsoft tools, or `commit;` on other tools.

5. Run the following script to assign user permissions:

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

Create two database users where the first user has administrative permissions to create schema objects, and the second user has restricted permissions for a CENM service instance.
The schema objects are created by a separate user rather than a default database administrator. This ensures that the correct schema namespace
is used.

1. Connect to a master database as an administrator - for example:

  ```sql
  jdbc:sqlserver://<host>:<port>;databaseName=master
  ```

2. Run the following script to create a database, a user, and a login:

  ```sql
  CREATE DATABASE my_database;
  CREATE LOGIN my_admin_login WITH PASSWORD = 'my_password', DEFAULT_DATABASE = my_database;
  CREATE USER my_admin_user FOR LOGIN my_admin_login;
  CREATE LOGIN my_login WITH PASSWORD = 'my_password', DEFAULT_DATABASE = my_database;
  CREATE USER my_user FOR LOGIN my_login;
  ```

Passwords must contain characters from three of the following four sets: uppercase letters, lowercase letters, digits, and symbols. For example, *C3NMP4ssword* is a valid password. Passwords are delimited with single quotes. Use different passwords for *my_admin_user* and *my_user*.

You can create schemas for several instances of CENM services within the same database (*my_database*). In that case, run the first DDL statement (`CREATE DATABASE my_database;`) only once.

3. Connect to a user database as the administrator (replace *master* with *my_database* in the connection string).

4. Run the following script to create a schema:

```sql
CREATE SCHEMA my_schema;
```

After creating the schema you may need to commit the change - for example, with the `GO`
command on Microsoft tools, or `commit;` on other tools.

5. Run the following script to assign user permissions:

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

As CENM databases require some VARCHAR2 or NVARCHAR2 column types to store more than 2000 characters, ensure that the database instance is configured to use extended data types. For example, for Oracle 12.1, see [MAX_STRING_SIZE](https://docs.oracle.com/database/121/REFRN/GUID-D424D23B-0933-425F-BC69-9C0E6724693C.htm#REFRN10321).

The recommended configuration for CENM with Oracle is a one-to-one relationship between schemas and user accounts, so the user has full control over that schema.

In order to restrict the permissions to the database:

1. Create two users where one user has administrative permissions (*my_admin_user* in the SQL script) and the other user just has read only permissions (*my_user* in the SQL script).

A database administrator can create schema objects (tables/sequences) via a user with administrative permissions. The CENM service instance accesses the schema created by the administrator via a user with restricted permissions, allowing them to only select/insert/delete data. For Oracle databases, these permissions (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) need to be granted explicitly for each table.

As the tablespace size in the sample script below is unlimited, adjust the value (for example, 100M, 1 GB) depending on the sizing requirements for your nodes. The script uses the default tablespace *users* with *unlimited* database space quota assigned to the user. Revise these settings depending on the sizing requirements for your nodes.

2. Run this script as a database administrator:

```sql
CREATE USER my_admin_user IDENTIFIED BY my_password DEFAULT TABLESPACE users QUOTA unlimited ON users;
GRANT CREATE SESSION TO my_admin_user;
GRANT CREATE TABLE TO my_admin_user;
GRANT CREATE VIEW TO my_admin_user;
GRANT CREATE SEQUENCE TO my_admin_user;
GRANT SELECT ON v_$parameter TO my_admin_user;
```

The assignment of permissions, required for the CENM service instance user to access database objects, is done after the database objects are created. These steps are described in [the next section](#oracle-1).

The last permission for the *v_$parameter* view is needed when a database is running in [Database Compatibility mode](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/upgrd/what-is-oracle-database-compatibility.html).

#### PostgreSQL

To create a CENM service instance user in PostgreSQL, connect to the database as an administrator and run the following script:

```sql
CREATE USER "my_user" WITH LOGIN PASSWORD 'my_password';
CREATE SCHEMA "my_schema";
GRANT USAGE ON SCHEMA "my_schema" TO "my_user";
GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON ALL tables IN SCHEMA "my_schema" TO "my_user";
ALTER DEFAULT privileges IN SCHEMA "my_schema" GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON tables TO "my_user";
GRANT USAGE, SELECT ON ALL sequences IN SCHEMA "my_schema" TO "my_user";
ALTER DEFAULT privileges IN SCHEMA "my_schema" GRANT USAGE, SELECT ON sequences TO "my_user";
ALTER ROLE "my_user" SET search_path = "my_schema";
```

If you provide a custom schema name (different from the user name), then the last statement in the script - setting the `search_path` - prevents querying the differing ([default schema search path](https://www.postgresql.org/docs/9.3/static/ddl-schemas.html#DDL-SCHEMAS-PATH)).

## 2. Database schema creation

The general steps for creating database schemas are listed below, followed by specific instructions for Oracle.

1. Deploy the CENM services first with database administrator credentials, specified in the `database.user` and `database.password` configuration files. If the schema exists and you have administrative permissions, the Liquibase migrations will run on start-up and automatically create the tables under the schema.

2. After you create the tables, substitute the database user and password settings in the service configuration file with the CENM service instance user credentials with restricted permissions.

{{< warning >}}
Ensure that `database.runMigration` is set to `false` for users with restricted permissions.
{{< /warning >}}

#### Oracle

For Oracle databases, you must also add permissions to use tables.

To do so, connect to the Oracle database as a database administrator and run the following DDL scripts:

**Identity Manager**

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

**Network Map Service**

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

**Zone Service**

```sql
CREATE USER my_user identified by my_password;
GRANT CREATE SESSION TO my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOG to my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOGLOCK to my_user;
GRANT SELECT ON my_admin_user.HIBERNATE_SEQUENCE TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.CONFIGURATION_DEPLOYMENT to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.CONFIGURATION_METADATA to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.DATABASECHANGELOG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.DATABASECHANGELOGLOCK to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.DATABASE_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.DATABASE_ADDITIONAL_PROPERTIES to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.IDENTITY_MANAGER_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.KEY_STORE to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.LOCAL_SIGNER to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.MIGRATION to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.NETWORK_MAP_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.NETWORK_PARAMETERS_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.NOTARY_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.PACKAGE_OWNERSHIP_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.PARAMETERS_UPDATE_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SHELL_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SIGNER_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SIGNER_CONFIG_HSM to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SIGNER_CONFIG_KEY to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SIGNER_CONFIG_LOCAL_KEYSTORE to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SIGNER_CONFIG_TASK to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SOCKET_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SSL_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.SUBZONE to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.TRUST_STORE to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.WHITELIST_CONTRACTS_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.WHITELIST_CONTRACTS_CORDAPPS to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.WHITELIST_CONTRACTS_EXCLUDE to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.WHITELIST_CONTRACT_ATTACH_IDS to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.WHITELIST_CONTRACT_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.WORKFLOW_CONFIG to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.WORKFLOW_CONFIG_CRL_FILES to my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.ZONE to my_user;
```

**Auth Service**

```sql
CREATE USER my_user identified by my_password;
GRANT CREATE SESSION TO my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOG to my_user;
GRANT SELECT ON my_admin_user.DATABASECHANGELOGLOCK to my_user;
GRANT SELECT ON my_admin_user.SEQ_AUDIT_EVENTS TO my_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.AUDIT_EVENTS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.AUDIT_EVENT_DATA;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.BASELINE_CHANGES;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.BASELINE_LOCK;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.DATABASECHANGELOG;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.DATABASECHANGELOGLOCK;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.GROUPS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.GROUP_DATA;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.OAUTH_REFRESH_TOKENS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.PERMISSIONS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.PERMISSION_ASSIGNMENTS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.ROLES;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.ROLE_ASSIGNMENTS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.USERS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.USERS_IN_GROUPS;
GRANT SELECT, INSERT, UPDATE, DELETE ON my_admin_user.USER_DATA;
```

## 3. CENM service configuration

The required updates to the file system of a CENM service instance are described below.

The CENM service configuration file - `identitymanager.conf` or `networkmap.conf`, respectively - must contain JDBC connection properties in the `database` entry, along with other database properties (passed to a CENM service JPA persistence provider or schema creation/upgrade flag). The `database` entry format is shown below:

```groovy
database = {
        jdbcDriver = <path to JDBC driver .jar file>
        driverClassName = <JDBC driver class name>
        url = <JDBC database URL>
        user = <Database user>
        password = <Database password>
        transactionIsolationLevel = <Transaction isolation level>
        schema = <Database schema name>
        runMigration = false
    }
```

`runMigration` is set to `false` because the restricted CENM service instance database user does not have permissions to alter a database schema. See [CENM Database Configuration](config-database.md) for a complete list of database-specific properties.



{{< note >}}
The CENM distribution does not include any JDBC drivers with the exception of the H2 driver.
It is the responsibility of the CENM service administrator or a developer to install the appropriate JDBC driver.
{{< /note >}}

Corda uses [Hikari Pool](https://github.com/brettwooldridge/HikariCP) for creating connection pools. To configure a connection pool, set custom properties in the `database` section - for example:

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
* [Oracle](#oracle-2)
* [PostgreSQL](#postgresql-1)

### Azure SQL

See below an example CENM services configuration file for Azure SQL - initial deployment with administrative permissions:

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

See below an example CENM service configuration file for Azure SQL *restrictive permissions* - CENM service instance database user with restrictive permissions:

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

Replace the placeholders *<database_server>* and *<my_database>* with appropriate values (*<my_database>* is a user database). The `database.schema` is the database schema name assigned to the user.

You can download the Microsoft SQL JDBC driver from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=55539) - extract the downloaded archive and copy the file `mssql-jdbc-6.2.2.jre8.jar` (the archive comes with two `.jar` files).
The [Database configuration section](#4-database-configuration) further below explains the correct location for the driver `.jar` file in the CENM service installation structure.

### SQL Server

See below an example CENM services configuration file for SQL Server - initial deployment with administrative permissions:

```groovy
database = {
    jdbcDriver = path/to/mssql-jdbc-x.x.x.jre8.jar
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    url = "jdbc:sqlserver://<host>:<port>;databaseName=my_database"
    user = my_admin_login
    password = "my_admin_password"
    schema = my_schema
    runMigration = true
}
```

See below an example CENM service configuration file for SQL Server - CENM service instance database user with restricted permissions:

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

Replace the placeholders *<host>* and *<port>* with appropriate values (the default SQL Server port is 1433). By default, the connection to the database is not SSL. To secure the JDBC connection, refer to [Securing JDBC Driver Applications](https://docs.microsoft.com/en-us/sql/connect/jdbc/securing-jdbc-driver-applications?view=sql-server-2017).

You can download the Microsoft JDBC 6.2 driver from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=55539) - extract the downloaded archive and copy the file `mssql-jdbc-6.2.2.jre8.jar` (the archive comes with two `.jar` files).
The [Database configuration section](#4-database-configuration) further below explains the correct location for the driver `.jar` file in the CENM service installation structure.

Ensure that the JDBC connection properties match the SQL Server setup, especially when trying to reuse Azure SQL JDBC URLs, which are invalid for SQL Server. This may lead to CENM failing to start with the following message:

`Caused by: org.hibernate.HibernateException: Access to DialectResolutionInfo cannot be null when ‘hibernate.dialect’ not set`

### Oracle

See below an example CENM service configuration file for Oracle database - initial deployment with administrative permissions:

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

See below an example CENM service configuration file for Oracle database - CENM service instance database user with restrictive permissions:

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

Replace the placeholders *<host>*, *<port>*, and *<sid>* with appropriate values. For a basic Oracle installation, the default *<sid>* value is `xe`.

Set the `database.schema` value to the username of the admin user (in the example above - *my_admin_user*). CENM does not guarantee prefixing all SQL queries with the schema namespace. The additional configuration entry `connectionInitSql` sets the current schema to the username of the admin user (in the example above - *my_admin_user*) on connection to the database.

The transaction isolation level is set by CENM to `READ_COMMITTED` - an attempt to set another isolation level in the configuration will result in an error. This is intentional behaviour, as `READ_UNCOMMITTED` results in inconsistent data reads, and `REPEATABLE_READ` and `SERIALIZABLE` are not compatible with Corda.

Use Oracle JDBC driver *ojdbc6.jar* for 11g RC2 or *ojdbc8.jar* for Oracle 12c. You can find links to the appropriate drivers on [Oracle's website](https://www.oracle.com/database/technologies/appdev/jdbc-downloads.html).
The database schema name can be set in a JDBC URL string - for example, `currentSchema=my_schema`.

### PostgreSQL

See below an example CENM service configuration for PostgreSQL:

```groovy
database = {
    jdbcDriver = path/to/postgresql-xx.x.x.jar
    driverClassName = "org.postgresql.Driver"
    url = "jdbc:postgresql://<host>:<port>/<database>"
    user = my_user
    password = "my_password"
    schema = my_schema
}
```

Replace the placeholders *<host>*, *<port>*, and *<database>* with appropriate values.
The `database.schema` is the database schema name assigned to you (the user).
The value of `database.schema` is automatically wrapped in double quotes to preserve case-sensitivity (without quotes, PostgresSQL would treat *AliceCorp* as the value *alicecorp*).

## 4. Database configuration

This section provides additional vendor-specific database configuration details.

### SQL Server

The database collation for SQL Server should be *case insensitive* - see [Server Configuration documentation](https://docs.microsoft.com/en-us/sql/sql-server/install/server-configuration-collation?view=sql-server-2014&viewFallbackFrom=sql-server-2017) for more information.

### Oracle

To allow `VARCHAR2` and `NVARCHAR2` column types to store more than 2000 characters, ensure the database instance is configured to use extended data types.

{{< note >}}
For Oracle 12.1, refer to [MAX_STRING_SIZE](https://docs.oracle.com/database/121/REFRN/GUID-D424D23B-0933-425F-BC69-9C0E6724693C.htm#REFRN10321).
{{< /note >}}

## 5. Tables

Note that `<SCHEMA_NAME>` below is a placeholder value representing the actual name for the appropriate schema.


### Identity Manager

The list of tables created by the Identity Manager Service follows below:

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

The list of tables created by the Network Map Service follows below:

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

### Zone Service

The list of tables created by the Zone Service follows below:

```sql
<SCHEMA_NAME>.CONFIGURATION_DEPLOYMENT
<SCHEMA_NAME>.CONFIGURATION_METADATA
<SCHEMA_NAME>.DATABASECHANGELOG
<SCHEMA_NAME>.DATABASECHANGELOGLOCK
<SCHEMA_NAME>.DATABASE_CONFIG
<SCHEMA_NAME>.DATABASE_ADDITIONAL_PROPERTIES
<SCHEMA_NAME>.IDENTITY_MANAGER_CONFIG
<SCHEMA_NAME>.KEY_STORE
<SCHEMA_NAME>.LOCAL_SIGNER
<SCHEMA_NAME>.MIGRATION
<SCHEMA_NAME>.NETWORK_MAP_CONFIG
<SCHEMA_NAME>.NETWORK_PARAMETERS_CONFIG
<SCHEMA_NAME>.NOTARY_CONFIG
<SCHEMA_NAME>.PACKAGE_OWNERSHIP_CONFIG
<SCHEMA_NAME>.PARAMETERS_UPDATE_CONFIG
<SCHEMA_NAME>.SHELL_CONFIG
<SCHEMA_NAME>.SIGNER_CONFIG
<SCHEMA_NAME>.SIGNER_CONFIG_HSM
<SCHEMA_NAME>.SIGNER_CONFIG_KEY
<SCHEMA_NAME>.SIGNER_CONFIG_LOCAL_KEYSTORE
<SCHEMA_NAME>.SIGNER_CONFIG_TASK
<SCHEMA_NAME>.SOCKET_CONFIG
<SCHEMA_NAME>.SSL_CONFIG
<SCHEMA_NAME>.SUBZONE
<SCHEMA_NAME>.TRUST_STORE
<SCHEMA_NAME>.WHITELIST_CONTRACTS_CONFIG
<SCHEMA_NAME>.WHITELIST_CONTRACTS_CORDAPPS
<SCHEMA_NAME>.WHITELIST_CONTRACTS_EXCLUDE
<SCHEMA_NAME>.WHITELIST_CONTRACT_ATTACH_IDS
<SCHEMA_NAME>.WHITELIST_CONTRACT_CONFIG
<SCHEMA_NAME>.WORKFLOW_CONFIG
<SCHEMA_NAME>.WORKFLOW_CONFIG_CRL_FILES
<SCHEMA_NAME>.ZONE
```

### Auth Service

The list of tables created by the Auth Service follows below:

```sql
<SCHEMA_NAME>.AUDIT_EVENTS
<SCHEMA_NAME>.AUDIT_EVENT_DATA
<SCHEMA_NAME>.BASELINE_CHANGES
<SCHEMA_NAME>.BASELINE_LOCK
<SCHEMA_NAME>.DATABASECHANGELOG
<SCHEMA_NAME>.DATABASECHANGELOGLOCK
<SCHEMA_NAME>.GROUPS
<SCHEMA_NAME>.GROUP_DATA
<SCHEMA_NAME>.OAUTH_REFRESH_TOKENS
<SCHEMA_NAME>.PERMISSIONS
<SCHEMA_NAME>.PERMISSION_ASSIGNMENTS
<SCHEMA_NAME>.ROLES
<SCHEMA_NAME>.ROLE_ASSIGNMENTS
<SCHEMA_NAME>.USERS
<SCHEMA_NAME>.USERS_IN_GROUPS
<SCHEMA_NAME>.USER_DATA
```

## Clearing the database

Clearing the database will depend on the exact database that you are running.

The general scripts for clearing the Identity Manager Service database and Network Map Service database are provided below.


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

#### Zone Service

```sql
DROP TABLE IF EXISTS <SCHEMA_NAME>.CONFIGURATION_DEPLOYMENT;
DROP TABLE IF EXISTS <SCHEMA_NAME>.CONFIGURATION_METADATA;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOGLOCK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASE_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASE_ADDITIONAL_PROPERTIES;
DROP TABLE IF EXISTS <SCHEMA_NAME>.IDENTITY_MANAGER_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.KEY_STORE;
DROP TABLE IF EXISTS <SCHEMA_NAME>.LOCAL_SIGNER;
DROP TABLE IF EXISTS <SCHEMA_NAME>.MIGRATION;
DROP TABLE IF EXISTS <SCHEMA_NAME>.NETWORK_MAP_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.NETWORK_PARAMETERS_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.NOTARY_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.PACKAGE_OWNERSHIP_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.PARAMETERS_UPDATE_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SHELL_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SIGNER_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SIGNER_CONFIG_HSM;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SIGNER_CONFIG_KEY;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SIGNER_CONFIG_LOCAL_KEYSTORE;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SIGNER_CONFIG_TASK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SOCKET_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SSL_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.SUBZONE;
DROP TABLE IF EXISTS <SCHEMA_NAME>.TRUST_STORE;
DROP TABLE IF EXISTS <SCHEMA_NAME>.WHITELIST_CONTRACTS_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.WHITELIST_CONTRACTS_CORDAPPS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.WHITELIST_CONTRACTS_EXCLUDE;
DROP TABLE IF EXISTS <SCHEMA_NAME>.WHITELIST_CONTRACT_ATTACH_IDS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.WHITELIST_CONTRACT_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.WORKFLOW_CONFIG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.WORKFLOW_CONFIG_CRL_FILES;
DROP TABLE IF EXISTS <SCHEMA_NAME>.ZONE;
DROP SEQUENCE IF EXISTS <SCHEMA_NAME>.hibernate_sequence;
```

#### Auth Service

```sql
DROP TABLE IF EXISTS <SCHEMA_NAME>.AUDIT_EVENTS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.AUDIT_EVENT_DATA;
DROP TABLE IF EXISTS <SCHEMA_NAME>.BASELINE_CHANGES;
DROP TABLE IF EXISTS <SCHEMA_NAME>.BASELINE_LOCK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOGLOCK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.GROUPS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.GROUP_DATA;
DROP TABLE IF EXISTS <SCHEMA_NAME>.OAUTH_REFRESH_TOKENS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.PERMISSIONS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.PERMISSION_ASSIGNMENTS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.ROLES;
DROP TABLE IF EXISTS <SCHEMA_NAME>.ROLE_ASSIGNMENTS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.USERS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.USERS_IN_GROUPS;
DROP TABLE IF EXISTS <SCHEMA_NAME>.USER_DATA;
DROP SEQUENCE IF EXISTS <SCHEMA_NAME>.SEQ_AUDIT_EVENTS;
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

#### Zone Service

```sql
DROP TABLE <ZONE_ADMIN_USER>.CONFIGURATION_DEPLOYMENT CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.CONFIGURATION_METADATA CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.DATABASECHANGELOG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.DATABASECHANGELOGLOCK CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.DATABASE_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.DATABASE_ADDITIONAL_PROPERTIES CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.IDENTITY_MANAGER_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.KEY_STORE CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.LOCAL_SIGNER CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.MIGRATION CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.NETWORK_MAP_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.NETWORK_PARAMETERS_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.NOTARY_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.PACKAGE_OWNERSHIP_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.PARAMETERS_UPDATE_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SHELL_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SIGNER_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SIGNER_CONFIG_HSM CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SIGNER_CONFIG_KEY CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SIGNER_CONFIG_LOCAL_KEYSTORE CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SIGNER_CONFIG_TASK CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SOCKET_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SSL_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.SUBZONE CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.TRUST_STORE CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.WHITELIST_CONTRACTS_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.WHITELIST_CONTRACTS_CORDAPPS CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.WHITELIST_CONTRACTS_EXCLUDE CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.WHITELIST_CONTRACT_ATTACH_IDS CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.WHITELIST_CONTRACT_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.WORKFLOW_CONFIG CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.WORKFLOW_CONFIG_CRL_FILES CASCADE CONSTRAINTS;
DROP TABLE <ZONE_ADMIN_USER>.ZONE CASCADE CONSTRAINTS;
DROP SEQUENCE <ZONE_ADMIN_USER>.hibernate_sequence;
```

#### Auth Service

```sql
DROP TABLE <AUTH_ADMIN_USER>.AUDIT_EVENTS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.AUDIT_EVENT_DATA CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.BASELINE_CHANGES CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.BASELINE_LOCK CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.DATABASECHANGELOG CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.DATABASECHANGELOGLOCK CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.GROUPS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.GROUP_DATA CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.OAUTH_REFRESH_TOKENS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.PERMISSIONS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.PERMISSION_ASSIGNMENTS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.ROLES CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.ROLE_ASSIGNMENTS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.USERS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.USERS_IN_GROUPS CASCADE CONSTRAINTS;
DROP TABLE <AUTH_ADMIN_USER>.USER_DATA CASCADE CONSTRAINTS;
DROP SEQUENCE <AUTH_ADMIN_USER>.SEQ_AUDIT_EVENTS;
```

### PostgreSQL

To remove service tables, run the following SQL script:

```sql
DROP SCHEMA IF EXISTS "my_schema" CASCADE;
```

## 5. Database Migration

When upgrading a CENM service, any required database schema changes are applied by the services rather than by a standalone tool. As a best practice, we recommend that the services are configured with a database user without permission to make schema modifications, when running normally (this is the setup described above).

The typical service migration process is described below. Please read the release notes for any version-specific processes, especially when upgrading between major versions.

To migrate as service:

1. Shut down the service.
2. Back up the service database.
3. Back up the service configuration.
4. Update the `.jar` file.
5. Edit the service configuration to:
  * Set the user to connect to the database as an account with schema migration permissions.
  * Set `runMigration = true` in the database configuration.
6. Start the service.
7. Wait for the service to start completely and ensure that it is healthy.
8. Shut down the service.
9. Restore the configuration backup from earlier. Alternatively, edit the
   configuration to connect to the database as a user *without*
   schema migration permissions, and to set `runMigration = false` in the
   database configuration.

### 5.1. Zone Service database migration in CENM 1.4

If you are upgrading to CENM 1.4 from CENM 1.3, you **must** set `runMigration = true` in the database configuration. This is required due to a change in the Zone Service database schema - a new column in the database tables `socket_config` and `signer_config` called `timeout` is used to record the new optional `timeout` parameter values used in `serviceLocations` configuration blocks (Signing Services) and `identityManager` and `revocation` configuration blocks (Network Map Service). This value can remain `null`,
in which case the default 10 seconds timeout will be used wherever applicable.

An example follows below:

```
database = {
  driverClassName = "org.h2.Driver"
  user = "testuser"
	password = "password"
	url = "jdbc:h2:file:/etc/corda/db;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
  runMigration = true
}
```
