+++
date = "2020-01-08T09:59:25Z"
title = "CENM Database Configuration"
aliases = [ "/releases/release-1.0/config-database.html",]
tags = [ "config", "database",]

[menu.cenm-1-0]
parent = "cenm-1-0-config"
+++


# CENM Database Configuration

Both the Network Map and Identity Manager Components require a persistent layer to be available. This is described in their respsective configs with the following configuration state.



database


runMigration
Upgrade the CENM upgrade for any schema level changes


initialiseSchema
Automatically creates the tables required by the CENM component


jdbcDriver
path to the jar file containing the specific JDBC driver


driverClassName
see the specifc JDBC driver documentation


url
Location of the Database on the network


user
Database user


password
Database users password


