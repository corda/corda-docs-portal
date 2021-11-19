---
aliases:
- /releases/4.4/node-database-intro.html
- /docs/corda-enterprise/head/node-database-intro.html
- /docs/corda-enterprise/node-database-intro.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-corda-nodes-operating-db
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

The documentation contains the required [database user permission and schema creation](../../../../../en/platform/corda/4.4/enterprise/node/operating/node-database-admin.md) steps
for production systems for a new Corda installation or [database upgrade](../../../../../en/platform/corda/4.4/enterprise/node/operating/cm-upgrading-node.html#node-upgrade-notes-update-database-ref) for upgrading Corda nodes.
Database schema updates may be also required when [deploying CorDapps on a node](../../../../../en/platform/corda/4.4/enterprise/node/operating/node-operations-cordapp-deployment.md)
or [upgrading CorDapps](../../../../../en/platform/corda/4.4/enterprise/node/operating/node-operations-upgrade-cordapps.md).

For development/testing purposes, the [simplified database schema setup for development](../../../../../en/platform/corda/4.4/enterprise/node/operating/node-database-developer.md) documentation covers database setup with simplified user permissions. Documentation on [understanding the node database](../../../../../en/platform/corda/4.4/enterprise/node/operating/node-database.md) explains the differences between both setups.

Corda Enterpise is released with the [Database Management Tool](../../../../../en/platform/corda/4.4/enterprise/node/operating/node-database.html#database-management-tool-ref).
The tool is distributed as a standalone JAR file named `tools-database-manager-${corda_version}.jar`.
It is intended to be used by Corda Enterprise node administrators during database schema creation.

It can be also used by CorDapp developers as a helper to create Liquibase database migration scripts.
Any CorDapp deployed onto a Corda Enteprise node, which stores data in a custom table,
requires embedded DDL scripts written in a cross database manner database-management.
