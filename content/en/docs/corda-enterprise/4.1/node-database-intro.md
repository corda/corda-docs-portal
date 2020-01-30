---
title: "Database management"
date: 2020-01-08T09:59:25Z
---


# Database management
The Corda platform, and the installed CorDapps store their data in a relational database.

Corda Enterprise supports a range of commercial 3rd party databases: Azure SQL, SQL Server, Oracle and PostgreSQL.

The documentation contains the required database user permission and schema creation steps
            for production systems [Database schema setup]({{< relref "node-database-admin" >}}) for a new Corda installation
            or [Database upgrade]({{< relref "node-upgrade-notes#node-upgrade-notes-update-database-ref" >}}) for upgrading Corda nodes.
            Database schema updates may be also required when [Deploying CorDapps on a node]({{< relref "node-operations-cordapp-deployment" >}})
            or [Upgrading CorDapps on a node]({{< relref "node-operations-upgrade-cordapps" >}}).

For development/testing purposes [Simplified database schema setup for development]({{< relref "node-database-developer" >}}) covers database setup with simplified user permissions.
            [Node database]({{< relref "node-database" >}}) explains the differences between both setups.

Corda Enterpise is released with the [Database Management Tool]({{< relref "node-database#database-management-tool-ref" >}}).
            The tool is distributed as a standalone JAR file named `tools-database-manager-${corda_version}.jar`.
            It is intended to be used by Corda Enterprise node administrators during database schema creation.

It can be also used by CorDapp developers as a helper to create Liquibase database migration scripts.
            Any CorDapp deployed onto a Corda Enteprise node, which stores data in a custom tables,
            requires embedded DDL scripts written in a cross database manner [Database management scripts]({{< relref "database-management" >}}).


