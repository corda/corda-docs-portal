---
aliases:
- /releases/release-1.1/config-database.html
- /config-database.html
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
Upgrade the CENM upgrade for any schema level changes


* **initialiseSchema**: 
Automatically creates the tables required by the CENM component


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
(Optional) Additional database properties





