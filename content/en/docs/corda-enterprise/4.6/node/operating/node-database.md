---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-corda-nodes-operating-db
    name: "Understanding the node database"
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- node
- database
title: Understanding the node database
weight: 1
---


# Understanding the node database

The Corda platform, and the installed CorDapps store their data in a relational database (see [State Persistence]({{% ref "../../cordapps/state-persistence.md" %}})).

Corda Enterprise supports a range of commercial 3rd party databases: Azure SQL, SQL Server, Oracle, and PostgreSQL.
This document provides an overview of required database permissions, related ways to create database schema objects,
and explains how a Corda node verifies the correct database schema version.



## Database user permissions

A Corda node connects to a database using a single database user, and stores data within a single database schema (a schema namespace).
A database schema can not be shared between two different nodes (except for hot-cold-deployment).
Depending on how the schema objects are created, a Corda node can connect to the database with a different set of database permissions:



* **restricted permissions** This grants the database user access to DML execution only (to manipulate data itself e.g. select/delete rows),
and a database administrator needs to create database schema objects before running the Corda node.
This permission set is recommended for a Corda node in a production environment (including hot-cold-deployment).
* **administrative permissions** This grants the database user full access to a Corda node, such that it can execute both DDL statements
(to define data structures/schema content e.g. tables) and DML queries (to manipulate data itself e.g. select/delete rows).
This permission set is more permissive and should be used with caution in production environments.
A Corda node with full control of the database schema can create or upgrade schema objects automatically upon node startup.
This eases the operational maintenance for development and testing.


Database setup for production systems (with **restricted permissions**) is described in [Database schema setup](node-database-admin.md),
and the recommended setup for development/testing environments are described in [Simplified database schema setup for development](node-database-developer.md).


## Database schema objects management

Database DDL scripts defining database tables (and other schema objects) are embedded inside the Corda distribution (`corda.jar` file)
or within the CorDapp distributions (a JAR file). Therefore Corda, and custom CorDapps are shipped without separate DDL scripts for each database vendor.
Whenever a node operator or database administrator needs to obtain a DDL script to be run, they can use the Corda Database Management Tool.
The tool, among other functions, outputs the DDL script which is compatible with the Corda release
and the database which the tool was running against.
Depending on [database user permissions](#node-database-user-permissions-ref) a Corda node may be configured to create database tables
(and other schema objects) automatically upon startup (and subsequently update tables).


DDL scripts are defined in a cross database syntax and grouped in change sets.
When a Corda node starts, it compares the list of change sets recorded in the database with the list embedded inside the Corda node
and associated CorDapps. Depending on the outcome and the node configuration, it will stop and report any differences or will create/update
any missing database objects.
Internally, the Corda node and Corda Database Management Tool use [Liquibase library/tool](http://www.liquibase.org)
for versioning database schema changes.

Liquibase is a tool that implements an automated, version based database migration framework with support for a large number of databases.
It works by maintaining a list of applied changesets. A changeset can be something very simple like adding a new column to a table.
It stores each executed changeset with columns like id, author, timestamp, description, md5 hash, etc in a table called `DATABASECHANGELOG`.
This changelog table will be read every time a migration command is run to determine
what change-sets need to be executed. It represents the “version” of the database (the sum of the executed change-sets at any point).
Change-sets are scripts written in a supported format (xml, yml, sql), and should never be modified once they have been executed.
Any necessary correction should be applied in a new change-set.
Understanding [how Liquibase works](https://www.thoughts-on-java.org/database-migration-with-liquibase-getting-started)
is highly recommended for understanding how database migrations work in Corda.


### Default Corda node configuration

By default, a node will *not* attempt to execute database migration scripts at startup (even when a new version has been deployed),
but will check the database “version” and halt if the database is not in sync with the node, to avoid data corruption.
To bring the database to the correct state we provide a [Database Management Tool](#database-management-tool-ref).
This setup/procedure is recommended for production systems.

Running the migration at startup automatically can only be configured by using the `initial registration` sub-command when running the node. The standard way of running the schema initialisation / migration scripts is to run the `run-migration-script` sub-command - see [Node command-line options](../node-commandline.md).
We recommend enabling database schema auto-creation/upgrade for development or test purposes only.
It is safe to run at startup if you have implemented the usual best practices for database management
(e.g. running a backup before installing a new version).



### Database Management Tool

The database management tool is distributed as a standalone JAR file named `tools-database-manager-${corda_version}.jar`.
It is intended to be used by Corda Enterprise node administrators who want more control over database changes made in production
environments.

The following sections document the available subcommands suitable for a node operator or database administrator.

{{< note >}}
The database management tool is for production databases only. H2 databases cannot be upgraded using the Database Management tool.

{{< /note >}}

You can review all available commands and options in the [Database Management Tool documentation](../../database-management-tool).

## Node database tables

By default, the node database has the following tables:


{{< table >}}

|Table name|Columns|
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|DATABASECHANGELOG|ID, AUTHOR, FILENAME, DATEEXECUTED, ORDEREXECUTED, EXECTYPE, MD5SUM, DESCRIPTTION, COMMENTS, TAG, LIQUIBASE, CONTEXTS, LABELS, DEPLOYMENT_ID|
|DATABASECHANGELOGLOCK|ID, LOCKED, LOCKGRANTED, LOCKEDBY|
|NODE_ATTACHMENTS|ATT_ID, CONTENT, FILENAME, INSERTION_DATE, UPLOADER, VERSION|
|NODE_ATTACHMENTS_CONTRACTS|ATT_ID, CONTRACT_CLASS_NAME|
|NODE_ATTACHMENTS_SIGNERS|ATT_ID, SIGNER|
|NODE_CHECKPOINTS|FLOW_ID, STATUS, COMPATIBLE, PROGRESS_STEP, FLOW_IO_REQUEST, TIMESTAMP|
|NODE_CHECKPOINT_BLOBS|FLOW_ID, CHECKPOINT_VALUE, FLOW_STATE, TIMESTAMP|
|NODE_FLOW_RESULTS|FLOW_ID, RESULT_VALUE, TIMESTAMP|
|NODE_FLOW_EXCEPTIONS|FLOW_ID, TYPE, EXCEPTION_MESSAGE, STACK_TRACE, EXCEPTION_VALUE, TIMESTAMP|
|NODE_FLOW_METADATA|FLOW_ID, INVOCATION_ID, FLOW_NAME, FLOW_IDENTIFIER, STARTED_TYPE, FLOW_PARAMETERS, CORDAPP_NAME, PLATFORM_VERSION, STARTED_BY, INVOCATION_TIME, START_TIME, FINISH_TIME|
|NODE_CONTRACT_UPGRADES|STATE_REF, CONTRACT_CLASS_NAME|
|NODE_CORDAPP_METADATA|CORDAPP_HASH, NAME, VENDOR, VERSION|
|NODE_CORDAPP_SIGNERS|CORDAPP_HASH, CORDAPP_SIGNERS|
|NODE_HASH_TO_KEY|PK_HASH, PUBLIC_KEY|
|NODE_IDENTITIES|PK_HASH, IDENTITY_VALUE|
|NODE_IDENTITIES_NO_CERT|PK_HASH, NAME|
|NODE_INFOS|NODE_INFO_ID, NODE_INFO_HASH, PLATFORM_VERSION, SERIAL|
|NODE_INFO_HOSTS|HOST_NAME, PORT, NODE_INFO_ID, HOSTS_ID|
|NODE_INFO_PARTY_CERT|PARTY_NAME, ISMAIN, OWNING_KEY_HASH, PARTY_CERT_BINARY|
|NODE_LINK_NODEINFO_PARTY|NODE_INFO_ID, PARTY_NAME|
|NODE_MESSAGE_IDS|MESSAGE_ID, INSERTION_TIME, SENDER, SEQUENCE_NUMBER|
|NODE_METERING_COMMANDS|ID, COMMAND_HASH, COMMAND_CLASS|
|NODE_METERING_CORDAPPS|ID, STACK_HASH, CORDAPP_HASH, POSITION|
|NODE_METERING_DATA|TIMESTAMP, SIGNING_ID, TRANSACTION_TYPE, CORDAPP_STACK_ID, COMMAND_ID, VERSION, COUNT, IS_COLLECTED|
|NODE_MUTUAL_EXCLUSION|MUTUAL_EXCLUSION_ID, MACHINE_NAME, PID, MUTUAL_EXCLUSION_TIMESTAMP, VERSION|
|NODE_NAMED_IDENTITIES|NAME, PK_HASH|
|NODE_NETWORK_PARAMETERS|HASH, EPOCH, PARAMETERS_BYTES, SIGNATURE_BYTES, CERT, PARENT_CERT_PATH|
|NODE_OUR_KEY_PAIRS|PUBLIC_KEY_HASH, PRIVATE_KEY, PUBLIC_KEY|
|NODE_PROPERTIES|PROPERTY_KEY, PROPERTY_VALUE|
|NODE_SCHEDULED_STATES|OUTPUT_INDEX, TRANSACTION_ID, SCHEDULED_AT|
|NODE_TRANSACTIONS|TX_ID, TRANSACTION_VALUE, STATE_MACHINE_RUN_ID, STATUS, TIMESTAMP|
|PK_HASH_TO_EXT_ID_MAP|EXTERNAL_ID, PUBLIC_KEY_HASH|
|STATE_PARTY|OUTPUT_INDEX, TRANSACTION_ID, PUBLIC_KEY_HASH, X500_NAME|
|VAULT_FUNGIBLE_STATES|OUTPUT_INDEX, TRANSACTION_ID, ISSUER_NAME, ISSUER_REF, OWNER_NAME, QUANTITY|
|VAULT_FUNGIBLE_STATES_PARTS|OUTPUT_INDEX, TRANSACTION_ID, PARTICIPANTS|
|VAULT_LINEAR_STATES|OUTPUT_INDEX, TRANSACTION_ID, EXTERNAL_ID, UUID|
|VAULT_LINEAR_STATES_PARTS|OUTPUT_INDEX, TRANSACTION_ID, PARTICIPANTS|
|VAULT_STATES|OUTPUT_INDEX, TRANSACTION_ID, CONSUMED_TIMESTAMP, CONTRACT_STATE_CLASS_NAME, LOCK_ID, LOCK_TIMESTAMP, NOTARY_NAME, RECORDED_TIMESTAMP, STATE_STATUS, RELEVANCY_STATUS, CONSTRAINT_TYPE, CONSTRAINT_DATA|
|VAULT_TRANSACTION_NOTES|SEQ_NO, NOTE, TRANSACTION_ID|
|V_PKEY_HASH_EX_ID_MAP|PUBLIC_KEY_HASH, TRANSACTION_ID, OUTPUT_INDEX, EXTERNAL_ID|

{{< /table >}}

For more details, see [Database tables](node-database-tables.md).

The node database for a Simple Notary has additional tables:


{{< table >}}

|Table name|Columns|
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|NODE_NOTARY_COMMITTED_STATES|OUTPUT_INDEX, TRANSACTION_ID, CONSUMING_TRANSACTION_ID|
|NODE_NOTARY_COMMITTED_TXS|TRANSACTION_ID|
|NODE_NOTARY_REQUEST_LOG|ID, CONSUMING_TRANSACTION_ID, REQUESTING_PARTY_NAME, REQUEST_TIMESTAMP, REQUEST_SIGNATURE|

{{< /table >}}

The structure of the tables of JPA notaries are described at [Configuring a JPA notary backend](../../notary/installing-jpa.md#configuring-jpa-notary-backend).

The tables for other experimental notary implementations are not described here.


### Database Schema Migration Logging

Database migration logs for Corda internal tables follow a structured format
described in [Database Schema Migration Logging](../../node-database-migration-logging.md#database-schema-migration-logging).
