---
aliases:
- /config-database.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- config
- database
title: CENM Database Configuration
---


# CENM Database Configuration
<!-- Sentence below: needs clarity - to be available needs to be rewritten to make it more meaningful.. -->
Both the Network Map and Identity Manager Components require a persistent layer to be available. This is described in
their respective configs with the following configuration state.


* **database**:

* **runMigration**:
Create or upgrade the database schema (database objects like tables, indices) to the current version of the service. If it is set to false, and the database schema is up to date, the service will validate.

* **initialiseSchema**:
*(Deprecated)* Automatically creates the tables required by the CENM component.
{{< note>}} This property was used for H2 database only. It has  been ignored since CENM 1.2 and has been replaced by `runMigration` {{< /note>}}


* **jdbcDriver**:
Path to the `.jar` file containing the specific JDBC driver


* **driverClassName**:
See the specific JDBC driver documentation
<!-- Is there a link to it? -->


* **url**:
Location of the Database on the network


* **user**:
Database user


* **password**:
Database user password


* **additionalProperties**:
*(Optional)* Additional database properties

* **lockResolutionStrategy**: When `lockResolutionStrategy` is set to `SingleInstance` and `runMigration` is set to `true`, the database lock applied by Liquibase is forcefully removed before the migration. This can solve problems where the application was shut down during migration, and the database remains locked.

  * *Allowed values*:
    * Not set (Default)
    * SingleInstance

{{<note>}}
If multiple CENM instances are connected to the same database, this configuration option can cause startup problems and/or database corruption.
{{</note>}}

