---
aliases:
- /config-database.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-5:
    identifier: cenm-1-5-config-database
    parent: cenm-1-5-configuration
    weight: 210
tags:
- config
- database
title: CENM Database Configuration
---


# CENM Database Configuration
A persistent layer must be available for the Identity Manager and Network Map Components to function. This is described in
their respective configs with the following configuration states.

* **database**:
Database configuration. 

* **runMigration**:
Create or upgrade the database schema (database objects like tables, indices) to the current version of the service. If it is set to false, and the database schema is up to date, the service will validate.

* **initialiseSchema**:
*(Deprecated)* Automatically creates the tables required by the CENM component.
{{< note>}} This property was used for H2 database only. It has been ignored since CENM 1.2 and has been replaced by `runMigration`. {{< /note>}}

* **jdbcDriver**:
Path to the JAR file containing the specific JDBC driver.

* **driverClassName**:
See the specific JDBC driver documentation [here](https://www.oracle.com/java/technologies/javase/javase-tech-database.html).

* **url**:
Location of the database on the network.

* **user**:
Database user.

* **password**:
Database user password.

* **additionalProperties**:
*(Optional)* Additional database properties.

* **lockResolutionStrategy**: When `lockResolutionStrategy` is set to `SingleInstance` and `runMigration` is set to `true`, the database lock applied by Liquibase is forcefully removed before the migration. This can solve problems where the application was shut down during migration, and the database remains locked.

  * *Allowed values*:
    * Not set (Default)
    * SingleInstance

{{<note>}}
If multiple CENM instances are connected to the same database, this configuration option can cause startup problems and/or database corruption.
{{</note>}}