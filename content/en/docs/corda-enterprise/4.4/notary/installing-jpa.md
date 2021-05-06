---
aliases:
- /releases/4.4/notary/installing-jpa.html
- /docs/corda-enterprise/head/notary/installing-jpa.html
- /docs/corda-enterprise/notary/installing-jpa.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    identifier: corda-enterprise-4-4-corda-nodes-notary-config
    name: "Configuring a notary"
    parent: corda-enterprise-4-4-corda-nodes
tags:
- installing
- jpa
title: Configuring a JPA notary backend
weight: 100
---

# Configuring a JPA notary backend

Prior to using the JPA notary, the database must be prepared. This can be performed using the
[Corda Database Management Tool](../node/operating/node-database.md#database-management-tool-ref). If preferred, the required tables can be manually
created. See below for example database scripts. Note that in these examples, a database named “corda” is created to
house the tables - this is purely for example purposes. The database name could be any string supported by your
database vendor - ensure that the configuration matches the database name.


## Supported databases for highly available mode

The JPA notary uses the Java Persistence API (JPA) interface to connect to the notary state database. For performance
and ease of operation, the recommended database is CockroachDB 19.1.2. The full set of supported configurations is
listed in the [Platform support matrix](../platform-support-matrix.md).

{{< note >}}
Please note that CockroachDB is not supported by the Corda Database Management Tool. It is recommended that
the SQL script provided below be used as the basis for setting up a CockroachDB database. This means it will not
be possible to setup a CockroachDB database schema using the Corda Database Management Tool, neither will it be
possible to upgrade an existing schema to a newer version using the tool.

{{< /note >}}

### Using the Corda Database Management Tool

If using the Corda Database Management Tool to perform initial schema setup, take note of the following:



* Always specify the command as the first parameter. This would be either `dry-run` or `execute-migration`
* Specify the mode as being JPA_NOTARY by using the command-line parameter `--mode=JPA_NOTARY`
* Ensure that the configuration file used is correct, as detailed in the section below.


Use the `dry-run` command to generate SQL scripts which could be inspected prior to being run. Alternatively, use the
`execute-migration` command to prepare the database, including table creation. Note that users and databases are not
created. Thus, the database must already exist.

{{< note >}}
Creating the schema manually and then switching to using the Corda Database Management Tool is not supported. We
recommend that one method of creating the schema be selected from the start and that this method should then be used for
the lifetime of the notary.

{{< /note >}}

#### DBM Tool configuration file format

The configuration file used as an input to the Database Management Tool should closely resemble that of the notary itself.
Only some minor changes may be needed. Take note of the following:



* The `dataSourceClassName` property must be provided.
* The `dataSource.url` property must be provided and should be identical to that used by the notary itself.
* The username and password needed for access to the database must be stored as `dataSource.user` and `dataSource.password` respectively.
* Any unused configuration parameters will be ignored.


Below is an example configuration file for the Database Management Tool:

{{< tabs name="tabs-1" >}}
dbm.conf

{{% tab name="kotlin" %}}
```kotlin
notary {
    validating = false
    jpa {
        dataSourceProperties {
            dataSource.url = "jdbc:oracle:thin:@(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST={host 1 IP address})(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST={host 2 IP address})(PORT=1521))(CONNECT_DATA=(SERVICE_NAME={service name})))"
            dataSource.user = {username}
            dataSource.password = {password}
            dataSourceClassName = "oracle.jdbc.pool.OracleDataSource"
        }
    }
}
```
{{% /tab %}}




[dbm.conf](../resources/dbm.conf) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

If the Corda Database Management Tool’s `dry-run` mode is used, the `databasechangelog` and `databasechangeloglock` tables must already exist
and the database user would need read and write permissions. If the tool’s `execute-migration` mode is used, the database user would require
schema modification rights. For more information, see [Corda Database Management Tool](../node/operating/node-database.md#database-management-tool-ref).


### Database users

We recommend creating one database user with schema modification rights so as to be able to create the schema objects
necessary for the operation of the notary. However, this user should not be used for the operation of the notary for
security reasons. We recommend the creation of a user with more limited permissions for the operation of the notary. This
would be set in the configuration of the notary in the `dataSourceProperties` section.


## Database Tables


### Notary Committed States

The collection of spent states, used to detect double spend attempts.


{{< table >}}

|Column|Description|
|------------------------------------|------------------------------------------------------------------------|
|state_ref|The ID of the spent state (indexed).|
|consuming_transaction_id|The ID of the transaction spending this state.|

{{< /table >}}


### Notary Committed Transactions

The collection of notarised transactions, used to re-notarise transactions that don’t get recorded into
the collection of spent states because they only reference states or are time window issue transactions that
don’t spend any states.


{{< table >}}

|Column|Description|
|------------------------------------|------------------------------------------------------------------------|
|transaction_id|The ID of a notarised transaction (indexed).|

{{< /table >}}


### Notary Request Log

The request log, used to record the request signatures of the requesting parties.


{{< table >}}

|Column|Description|
|------------------------------------|------------------------------------------------------------------------|
|id|The ID of the request (indexed).|
|consuming_transaction_id|The ID of the transaction consuming the input states.|
|requesting_party_name|The X500 name of the party requesting the notarisation.|
|request_timestamp|The timestamp when the notary worker started processing the request.|
|request_signature|The request signature of the requesting party.|
|worker_node_x500_name|The X500 name of the notary worker processing the request.|

{{< /table >}}


## Configuring the notary backend - CockroachDB

The JPA notary service is tested against CockroachDB 19.1.2. CockroachDB’s
[documentation page](https://www.cockroachlabs.com/docs/v19.1/) explains the installation
in detail.

Some information specific to the configuration of the JPA notary to interact with CockroachDB is covered below.


### Database setup

To create the database, a user with administrative permissions is required. CockroachDB automatically creates a root user during setup.
This root user is the only user with administrative permissions, and so is the only user able to create databases. Only CockroachDB
Enterprise supports the creation of administrative users besides root. The CockroachDB root user can only authenticate with
certificates and is unable to authenticate via passwords.

Open a terminal window on one of the machines on which CockroachDB is installed. Connect to the SQL interface of the database with the
following command. Note the command is an example and assumes that Cockroach has been installed to `/opt/roach`. Make sure to specify


the correct path for your certificates.


```bash
sudo cockroach sql --certs-dir=/opt/roach/certs
```

Once connected to CockroachDB, create the database and tables required. Note that the database name can be changed from “corda”,
but the table names must be left as-is. If the database name is changed, make sure to change the JDBC URL in the configuration file to
match.

```sql
create database if not exists corda;

create table corda.notary_committed_states (
  state_ref varchar(73) not null,
  consuming_transaction_id varchar(64) not null,
  constraint id1 primary key (state_ref)
  );

create table corda.notary_committed_transactions (
  transaction_id varchar(64) not null,
  constraint id2 primary key (transaction_id)
  );

create table corda.notary_request_log (
  id varchar(76) not null,
  consuming_transaction_id varchar(64),
  requesting_party_name varchar(255),
  request_timestamp timestamp not null,
  request_signature bytea not null,
  worker_node_x500_name varchar(255),
  constraint id3 primary key (id)
  );
```


### Database user setup

Once the database and tables have been created, create a user with restricted rights that the notary worker will use to log
in to the database. This user will only be able to insert and read data. It will not be able to delete or update data, nor
will it be able to modify any schemas. Ensure that the database name is correct if it was changed in the previous step. The
username can be changed if desired - ensure that the configuration file is updated to match.

```sql
create user if not exists corda;

grant select on database corda to corda;
grant insert on database corda to corda;

grant select on table corda.* to corda;
grant insert on table corda.* to corda;
```


### Generating a client certificate

It is recommended that the CockroachDB installation be configured to use SSL for secure connections. This will
require certificates to be generated for the database user that Corda uses to connect to CockroachDB. When
generating the certificates, make sure that PKCS8 certificates are also generated. An example `bash` command
is given below.

```sh
sudo cockroach cert create-client corda --certs-dir=/opt/roach/certs --ca-key=/opt/roach/my-safe-directory/ca.key --also-generate-pkcs8-key
```

Once generated, ensure that the certificates are accessible by the user that is being used to run the Corda
process.
Additionally, the same user has to have access to the key in PKCS8 format used to create above certificate.


### JDBC driver

The PostgresSQL driver should be used when attempting to connect the JPA notary to CockroachDB. The JPA notary
service has been tested with driver version 42.2.7. This JAR file should be placed in the `drivers` folder.


### Connection string

The properties specifying the location of the client certificates must be passed in via the JDBC connection
string. It will not be possible to pass them in as configuration properties. See below for an example connection
string.


```javascript
dataSource.url="jdbc:postgresql://{list of CockroachDB node IP addresses}:26257/corda?sslmode=require&sslrootcert=certificates/ca.crt&sslcert=certificates/client.corda.crt&sslkey=certificates/client.corda.key.pk8"
```

Refer to the section [Configuring the notary worker nodes](installing-the-notary-service.md) for more details on configuring the JPA notary.


## Configuring notary backend - Oracle RAC 12cR2

The JPA notary service is tested against Oracle RAC, with Oracle database version 12cR2.
Oracle’s [documentation page](https://docs.oracle.com/database/121/RACAD/toc.htm) explains the installation
in detail.

Some information specific to the configuration of the JPA notary to interact with Oracle RAC is covered below.


### Database setup

It is recommended that a pluggable database be created to house the notary data. This can be done by opening a
terminal window on the Oracle machine and running the following command in order to start sqlplus, the Oracle
SQL command line tool.

```bash
sudo su - oracle
sqlplus / as sysdba
```

With sqlplus running, create a pluggable database using the following command. The database name, administrative
user name and password can all be changed as needed.

```sql
CREATE PLUGGABLE DATABASE corda_pdb ADMIN USER corda_adm IDENTIFIED BY Password1;
ALTER PLUGGABLE DATABASE corda_pdb OPEN;
```

Once the database is created, connect to it with the following command:

```sql
ALTER SESSION SET CONTAINER = corda_pdb;
```

While still connected to the newly created pluggable database, run the following command in order to determine
the service name. The service name forms part of the JDBC URL for the database and is necessary for either the
Corda Database Management Tool or the notary worker to connect to the database. Note that the service name can
be specified manually during the creation of the pluggable database.

```sql
SELECT SERVICE_NAME FROM gv$session WHERE sid IN (SELECT sid FROM V$MYSTAT);
```

Now the necessary tables can be created. Note that this step can be performed using the Corda Database Management
Tool if desired. If not, the following script can be used. Note that this script must be run on the pluggable
database created above.

```sql
create table notary_committed_states (
  state_ref varchar(73) not null,
  consuming_transaction_id varchar(64) not null,
  constraint id1 primary key (state_ref)
  );

create table notary_committed_transactions (
  transaction_id varchar(64) not null,
  constraint id2 primary key (transaction_id)
  );

create table notary_request_log (
  id varchar(76) not null,
  consuming_transaction_id varchar(64),
  requesting_party_name varchar(255),
  request_timestamp timestamp not null,
  request_signature RAW(1024) not null,
  worker_node_x500_name varchar(255),
  constraint id3 primary key (id)
  );
```


### Database user setup

Once the database and tables have been created, create a user with restricted rights that the notary worker will use to
log in to the database. This user will be a local user with access rights only to the pluggable database created above.
Ensure that the container for the sqlplus session is still the Corda pluggable database as created above - this will make
sure that the user created belongs to the pluggable database. The username can be changed if desired - ensure that the
configuration file is updated to match.

This user will only be able to insert and read data. It will not be able to delete or update data, nor will it be able to modify any schemas. Ensure that
the database name is correct if it was changed in the previous step.

```sql
ALTER SESSION SET CONTAINER = corda_pdb;
CREATE USER corda_pdb_user IDENTIFIED BY Password1 CONTAINER=CURRENT;

GRANT CREATE SESSION to corda_pdb_user CONTAINER=CURRENT;

GRANT SELECT, INSERT ON corda_adm.notary_committed_states TO corda_pdb_user;
GRANT SELECT, INSERT ON corda_adm.notary_committed_transactions TO corda_pdb_user;
GRANT SELECT, INSERT ON corda_adm.notary_request_log TO corda_pdb_user;
```


### JDBC driver

The `ojdbc8` driver should be used when connecting to Oracle RAC database 12cR2. This JAR file
should be placed in the `drivers` folder.


### Connection string

Below is an example connection string for use with an Oracle RAC database. Note that more than 2 host IP addresses
may be specified if desired. It is important to use the correct service name.


```javascript
dataSource.url="jdbc:oracle:thin:@(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST={host 1 IP address})(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST={host 2 IP address})(PORT=1521))(CONNECT_DATA=(SERVICE_NAME={service name})))"
```
