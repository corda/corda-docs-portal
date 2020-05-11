---
aliases:
- /releases/release-1.2/config-database.html
- /docs/cenm/head/config-database.html
- /docs/cenm/config-database.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- config
- database
title: CENM Database Configuration
---


# CENM Database Configuration

Both the Network Map and Identity Manager Components require a persistent layer to be available. This is described in
their respective configs with the following configuration state.


* **database**:

* **runMigration**:
Create or upgrade the database schema (database objects like tables, indices)
to the current version of the service. If set to false then the service will validate
if the database schema is up to date.


* **initialiseSchema**:
*(Deprecated)* Automatically creates the tables required by the CENM component,
the property was used for H2 database only, its ignored since CENM 1.2 and its replaced by `runMigration`


* **jdbcDriver**:
Path to the jar file containing the specific JDBC driver


* **driverClassName**:
See the specific JDBC driver documentation


* **url**:
Location of the Database on the network


* **user**:
Database user


* **password**:
Database user password


* **additionalProperties**:
*(Optional)* Additional database properties
