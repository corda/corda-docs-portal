---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-operations-guide-deployment-configuration-host-prereq
    parent: corda-enterprise-4-6-operations-guide-deployment-configuration
tags:
- host
- prereq
title: Host prerequisites and database requirements
weight: 2
---


# Host prerequisites and database requirements


## Operating Systems Supported in Production


{{< table >}}

|Platform|CPU Architecture|Versions|
|---------------------------------------|-----------------------|--------------|
|Red Hat Enterprise Linux|x86-64|7.x, 6.x|
|Suse Linux Enterprise Server|x86-64|12.x, 11.x|
|Ubuntu Linux|x86-64|16.10, 16.04|
|Oracle Linux|x86-64|7.x, 6.x|

{{< /table >}}


## Operating Systems Supported in Development


{{< table >}}

|Platform|CPU Architecture|Versions|
|---------------------------------------|-----------------------|--------------|
|Microsoft Windows|x86-64|10, 8.x|
|Microsoft Windows Server|x86-64|2016, 2012 R2, 2012|
|Apple macOS|x86-64|10.9 and above|

{{< /table >}}


## Corda Vault


{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|---------------------------|-----------------|-----------------|------------------|
|Microsoft|x86-64|Azure SQL, SQL Server 2017|Microsoft JDBC Driver 6.2|
|Oracle|x86-64|11gR2|Oracle JDBC 6|
|Oracle|x86-64|12cR2|Oracle JDBC 8|
|PostgreSQL|x86-64|9.6|PostgreSQL JDBC Driver 42.1.4|

{{< /table >}}


## Sizing

The recommended minimum vault database size is 2GB. As with the Corda node, the use case determines the sizing needs for the database. When testing in your development environment, pay attention to the size of objects created in the `NODE_CHECKPOINT_BLOBS` and `NODE_TRANSACTIONS` tables, to inform the sizing requirements of your use case. Some guidance on this is provided in: [Sizing and Performance: Database server configuration](../../performance-testing/performance-results.md#database-server-configuration). In a production implementation, a separate high availability database instance should be deployed for each Corda node. However, it’s possible to create a separate schema for each node within a single database instance subject to performance, availability, and security constraints (the schema to be used is defined in the node configuration file).

Corda Enterprise uses Liquibase to generate the requisite database schemas for both the Corda node the CorDapps the node has installed. The `run-migration-script` sub-command controls whether these database schemas are generated automatically. In many production scenarios, you may require more control over the creation and running of those scripts. In these cases, simply do not run the `run-migration-script` sub-command. The [Corda Enterprise Database Management Tool](../../cordapps/database-management.html#creating-script-for-initial-table-creation-using-corda-database-management-tool) can assist a database administrator by creating scripts for initial table creation.


## Corda Node, Bridge and Float

Prerequisite and sizing information for the Corda Node, Bridge and Float components.


### VM Sizing Guidelines

{{< note >}}
R3 recommend a max Java heap memory size of 4 GB be allocated to a Corda Node running in a production environment.

{{< /note >}}
Minimum specification for a testing environment with components on separate VMs:


* Corda Node 2 CPU Core, 4 GB Memory
* Corda Bridge 2 CPU Core, 2 GB Memory
* Corda Float 2 CPU Core, 2 GB Memory

Recommended production specification for components on separate VMs:


* Corda Node 4 CPU Core, 8 GB Memory
* Corda Bridge 2 CPU Core, 2 GB Memory
* Corda Float 2 CPU Core, 2 GB Memory

Recommended production specification for multiple nodes


* Corda Node(s) 8 CPU Core, 16 GB Memory, assuming two nodes, scale linearly for more
* Corda Bridge(s) 4 CPU Core, 4 GB Memory
* Corda Float(s) 2 CPU Core, 4 GB Memory


### Additional Details

JDBC Connectivity from the Corda node to the Corda vault is required to create Corda system tables on startup as well as storing application tables/logic. Corda stores information about several aspects of the Corda node and network in tables in the vault.

During deployment the following system (not user) tables will be created in the vault database:


* DATABASECHANGELOG
* DATABASECHANGELOGLOCK
* NODE_ATTACHMENTS
* NODE_ATTACHMENTS_CONTRACTS
* NODE_ATTACHMENTS_SIGNERS
* NODE_CHECKPOINTS
* NODE_CHECKPOINT_BLOBS
* NODE_FLOW_RESULTS
* NODE_FLOW_EXCEPTIONS
* NODE_FLOW_METADATA
* NODE_CONTRACT_UPGRADES
* NODE_IDENTITIES
* NODE_INFOS
* NODE_INFO_HOSTS
* NODE_INFO_PARTY_CERT
* NODE_LINK_NODEINFO_PARTY
* NODE_MESSAGE_IDS
* NODE_NAMED_IDENTITIES
* NODE_NETWORK_PARAMETERS
* NODE_OUR_KEY_PAIRS
* NODE_PROPERTIES
* NODE_SCHEDULED_STATES
* NODE_TRANSACTIONS
* PK_HASH_TO_EXT_ID_MAP
* STATE_PARTY
* VAULT_FUNGIBLE_STATES
* VAULT_FUNGIBLE_STATES_PARTS
* VAULT_LINEAR_STATES
* VAULT_LINEAR_STATES_PARTS
* VAULT_STATES
* VAULT_TRANSACTION_NOTES
* V_PKEY_HASH_EX_ID_MAP

Detailed information on the Corda Vault can be found [here](../../node/operating/node-database.md).

JDBC Connectivity to the Corda Vault is handled in the Corda Enterprise `node.conf` file in `/opt/corda`. Here are examples for each supported RDBMS.
