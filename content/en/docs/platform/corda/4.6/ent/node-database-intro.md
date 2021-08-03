---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating-db
tags:
- node
- database
- intro
title: Database management
weight: 10
---


# Database management

The Corda platform, and the installed CorDapps store their data in a relational database.

Corda Enterprise supports a range of commercial 3rd party databases: Azure SQL, SQL Server, Oracle and PostgreSQL.

The documentation contains the required [database user permission and schema creation](node/operating/node-database-admin.md) steps
for production systems for a new Corda installation or [database upgrade](node-upgrade-notes.md#step-3-update-the-database-manual) for upgrading Corda nodes.
Database schema updates may be also required when [deploying CorDapps on a node](node/operating/node-operations-cordapp-deployment.md)
or [upgrading CorDapps](node-operations-upgrade-cordapps.md).

For development/testing purposes, the [simplified database schema setup for development](node/operating/node-database-developer.md) documentation covers database setup with simplified user permissions. Documentation on [understanding the node database](node/operating/node-database.md) explains the differences between both setups.

Corda Enterprise is released with the [Database Management Tool](node/operating/node-database.md#database-management-tool-ref).
The tool is distributed as a standalone JAR file named `tools-database-manager-${corda_version}.jar`.
It is intended to be used by Corda Enterprise node administrators during database schema creation.

It can be also used by CorDapp developers as a helper to create Liquibase database migration scripts.
Any CorDapp deployed onto a Corda Enterprise node, which stores data in a custom table,
requires embedded DDL scripts written in a cross database manner database-management.
