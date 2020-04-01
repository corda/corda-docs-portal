---
aliases:
- /releases/release-1.0/database-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-database-set-up
    parent: cenm-1-0-operations
    weight: 180
tags:
- database
- set
title: ENM Databases
---


# ENM Databases

There are currently two types of Enterprise Network Manager database:


* **Identity Manager** - Used by the Identity Manager service. Contains information relating to certificate signingrequests of nodes wanting to join the network as well as information regarding revocation of
nodes from the network.
* **Network Map** - Used by the Network Map service. Contains information relating to the current participants on thenetwork, the current network parameters and any pending parameter updates.

Due to the way the migrations are defined, the services *must* use separate DB schemas (either in the same DB instance
or in completely separate instances). Attempting to run an Identity Manager and Network Map service that share the same
DB schema will result in errors.


## Supported Databases

The Enterprise Network Manager supports the following databases “out of the box”, that is without providing an external
JDBC driver jar



* Microsoft SQL Server (deployed locally or through Azure)
* H2 (an in-memory database meant primarily for testing)


Support for additional databases can be added by providing a suitable JDBC driver JAR file and indicating it’s location
in your service’s configuration. Currently, the following databases have been tested


* Postgresql


{{< warning >}}
H2 as a database is not considered to be suitable for production.

{{< /warning >}}



## Setup

Since the ENM services ([Identity Manager Service](identity-manager.md) and [Network Map Service](network-map.md)) benefit from the Liquibase database changes
tracking library, upon every deployment the current schema state can be validated and the migrations can be performed if
necessary. This behaviour can be switched on via the appropriate configuration option for the service. See the
“Database Setup” section of the docs for the relevant service.

Currently, Identity Manager deployment supports (apart from the H2 database) both the SQL Server and Azure databases.


{{< important >}}
Support for Oracle is planned for a future release.


{{< /important >}}


## Tables

Note that `<SCHEMA_NAME>` below is a placeholder value representing the actual name for the appropriate schema.


### Identity Manager

The following is the list of tables created by the Identity Manager service:

```sql
<SCHEMA_NAME>.DATABASECHANGELOG
<SCHEMA_NAME>.DATABASECHANGELOGLOCK
<SCHEMA_NAME>.certificate_data
<SCHEMA_NAME>.certificate_revocation_list
<SCHEMA_NAME>.certificate_revocation_request
<SCHEMA_NAME>.certificate_revocation_request_AUD
<SCHEMA_NAME>.certificate_signing_request
<SCHEMA_NAME>.certificate_signing_request_AUD
<SCHEMA_NAME>.private_network_global
<SCHEMA_NAME>.REVINFO
<SCHEMA_NAME>.migration
```


### Network Map

The following is the list of tables created by the Network Map service:

```sql
<SCHEMA_NAME>.DATABASECHANGELOG
<SCHEMA_NAME>.DATABASECHANGELOGLOCK
<SCHEMA_NAME>.certificate_chain
<SCHEMA_NAME>.network_map
<SCHEMA_NAME>.network_map_AUD
<SCHEMA_NAME>.network_parameters
<SCHEMA_NAME>.network_parameters_update
<SCHEMA_NAME>.node_info
<SCHEMA_NAME>.private_network
<SCHEMA_NAME>.REVINFO
<SCHEMA_NAME>.node_info_staging
<SCHEMA_NAME>.migration
```


## Required Permissions

The Enterprise Network Manager does not distinguish database configurations between the deployment and runtime phases of
each individual service. As such, there is a single user expected to be configured on the database for the entire
Enterprise Network Manager lifecycle. It is assumed that the configured user has its own (i.e. sole access) schema.

{{< note >}}
This assumption will be changed in the Future.

{{< /note >}}
The following is the list of permissions required to be configured for the ENM user:


* **SQL Server and Azure**: 
```sql
GRANT ALTER, DELETE, INSERT, REFERENCES, SELECT, UPDATE ON SCHEMA::SCHEMA_NAME TO USER_NAME;
GRANT CREATE TABLE TO USER_NAME;
```




## Clearing The DB

Clearing the DB will depend upon the exact database that you are running on, however the general scripts for clearing
the Identity Manager and Network Map DB are below:


### Identity Manager

```sql
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOGLOCK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_revocation_list;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_revocation_request;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_revocation_request_AUD;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_signing_request_AUD;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_data;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_signing_request;
DROP TABLE IF EXISTS <SCHEMA_NAME>.private_network_global;
DROP TABLE IF EXISTS <SCHEMA_NAME>.migration;
DROP TABLE IF EXISTS <SCHEMA_NAME>.REVINFO;
DROP SEQUENCE IF EXISTS <SCHEMA_NAME>.hibernate_sequence;
```


### Network Map

```sql
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOG;
DROP TABLE IF EXISTS <SCHEMA_NAME>.DATABASECHANGELOGLOCK;
DROP TABLE IF EXISTS <SCHEMA_NAME>.certificate_chain;
DROP TABLE IF EXISTS <SCHEMA_NAME>.network_map;
DROP TABLE IF EXISTS <SCHEMA_NAME>.network_map_AUD;
DROP TABLE IF EXISTS <SCHEMA_NAME>.network_parameters;
DROP TABLE IF EXISTS <SCHEMA_NAME>.network_parameters_update;
DROP TABLE IF EXISTS <SCHEMA_NAME>.node_info;
DROP TABLE IF EXISTS <SCHEMA_NAME>.private_network;
DROP TABLE IF EXISTS <SCHEMA_NAME>.migration;
DROP TABLE IF EXISTS <SCHEMA_NAME>.node_info_staging;
DROP TABLE IF EXISTS <SCHEMA_NAME>.REVINFO;
DROP SEQUENCE IF EXISTS <SCHEMA_NAME>.hibernate_sequence;
```

