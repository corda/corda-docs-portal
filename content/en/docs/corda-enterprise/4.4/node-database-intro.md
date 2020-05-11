---
aliases:
- /releases/4.4/node-database-intro.html
- /docs/corda-enterprise/head/node-database-intro.html
- /docs/corda-enterprise/node-database-intro.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- node
- database
- intro
title: Database management
---


# Database management

The Corda platform, and the installed CorDapps store their data in a relational database.

Corda Enterprise supports a range of commercial 3rd party databases: Azure SQL, SQL Server, Oracle and PostgreSQL.

The documentation contains the required database user permission and schema creation steps
for production systems node-database-admin for a new Corda installation
or [Database upgrade](node/operating/cm-upgrading-node.md#node-upgrade-notes-update-database-ref) for upgrading Corda nodes.
Database schema updates may be also required when node-operations-cordapp-deployment
or node-operations-upgrade-cordapps.

For development/testing purposes node-database-developer covers database setup with simplified user permissions.
node-database explains the differences between both setups.

Corda Enterpise is released with the [Database Management Tool](node/operating/node-database.md#database-management-tool-ref).
The tool is distributed as a standalone JAR file named `tools-database-manager-${corda_version}.jar`.
It is intended to be used by Corda Enterprise node administrators during database schema creation.

It can be also used by CorDapp developers as a helper to create Liquibase database migration scripts.
Any CorDapp deployed onto a Corda Enteprise node, which stores data in a custom tables,
requires embedded DDL scripts written in a cross database manner database-management.
