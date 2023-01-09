---
aliases:
- /head/node-database.html
- /HEAD/node-database.html
- /node-database.html
- /releases/release-V4.4/node-database.html
- /docs/corda-os/head/node-database.html
- /docs/corda-os/node-database.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-4:
    identifier: corda-os-4-4-node-database
    parent: corda-os-4-4-corda-nodes-index
    weight: 1070
tags:
- node
- database
title: Node database
---


# Node database



## Configuring the node database


### H2

By default, nodes store their data in an H2 database. See [Database access when running H2](node-database-access-h2.md).

### PostgreSQL

Nodes can also be configured to use PostgreSQL 9.6, using PostgreSQL JDBC Driver 42.2.8. However, this is an experimental community contribution.
The Corda continuous integration pipeline does not run unit tests or integration tests of this databases.

Here is an example node configuration for PostgreSQL:

```groovy
dataSourceProperties = {
    dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
    dataSource.url = "jdbc:postgresql://[HOST]:[PORT]/[DATABASE]"
    dataSource.user = [USER]
    dataSource.password = [PASSWORD]
}
database = {
    transactionIsolationLevel = READ_COMMITTED
}
```

Note that:


* Database schema name can be set in JDBC URL string e.g. *currentSchema=my_schema*
* Database schema name must either match the `dataSource.user` value to end up
on the standard schema search path according to the
[PostgreSQL documentation](https://www.postgresql.org/docs/9.3/static/ddl-schemas.html#DDL-SCHEMAS-PATH), or
the schema search path must be set explicitly for the user.
* If your PostgresSQL database is hosting multiple schema instances (using the JDBC URL currentSchema=my_schema)
for different Corda nodes, you will need to create a *hibernate_sequence* sequence object manually for each subsequent schema added after the first instance.
Corda doesn’t provision Hibernate with a schema namespace setting and a sequence object may be not created.
Run the DDL statement and replace *my_schema* with your schema namespace:

```groovy
CREATE SEQUENCE my_schema.hibernate_sequence INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 8 CACHE 1 NO CYCLE;
```


* The PostgreSQL JDBC database driver must be placed in the `drivers` directory in the node.

## Node database tables

By default, the node database has the following tables:


{{< table >}}

|Table name|Columns|
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|DATABASECHANGELOG|ID, AUTHOR, FILENAME, DATEEXECUTED, ORDEREXECUTED, EXECTYPE, MD5SUM, DESCRIPTION, COMMENTS, TAG, LIQUIBASE, CONTEXTS, LABELS, DEPLOYMENT_ID|
|DATABASECHANGELOGLOCK|ID, LOCKED, LOCKGRANTED, LOCKEDBY|
|NODE_ATTACHMENTS|ATT_ID, CONTENT, FILENAME, INSERTION_DATE, UPLOADER, VERSION|
|NODE_ATTACHMENTS_CONTRACTS|ATT_ID, CONTRACT_CLASS_NAME|
|NODE_ATTACHMENTS_SIGNERS|ATT_ID, SIGNER|
|NODE_CHECKPOINTS|CHECKPOINT_ID, CHECKPOINT_VALUE|
|NODE_CONTRACT_UPGRADES|STATE_REF, CONTRACT_CLASS_NAME|
|NODE_HASH_TO_KEY|PK_HASH, PUBLIC_KEY|
|NODE_IDENTITIES|PK_HASH, IDENTITY_VALUE|
|NODE_IDENTITIES_NO_CERT|PK_HASH, NAME|
|NODE_INFOS|NODE_INFO_ID, NODE_INFO_HASH, PLATFORM_VERSION, SERIAL|
|NODE_INFO_HOSTS|HOST_NAME, PORT, NODE_INFO_ID, HOSTS_ID|
|NODE_INFO_PARTY_CERT|PARTY_NAME, ISMAIN, OWNING_KEY_HASH, PARTY_CERT_BINARY|
|NODE_LINK_NODEINFO_PARTY|NODE_INFO_ID, PARTY_NAME|
|NODE_MESSAGE_IDS|MESSAGE_ID, INSERTION_TIME, SENDER, SEQUENCE_NUMBER|
|NODE_NAMED_IDENTITIES|NAME, PK_HASH|
|NODE_NETWORK_PARAMETERS|HASH, EPOCH, PARAMETERS_BYTES, SIGNATURE_BYTES, CERT, PARENT_CERT_PATH|
|NODE_OUR_KEY_PAIRS|PUBLIC_KEY_HASH, PRIVATE_KEY, PUBLIC_KEY|
|NODE_PROPERTIES|PROPERTY_KEY, PROPERTY_VALUE|
|NODE_SCHEDULED_STATES|OUTPUT_INDEX, TRANSACTION_ID, SCHEDULED_AT|
|NODE_TRANSACTIONS|TX_ID, TRANSACTION_VALUE, STATE_MACHINE_RUN_ID, STATUS|
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

For more details see: [Database tables](node-database-tables.md).


## Database connection pool

Corda uses [Hikari Pool](https://github.com/brettwooldridge/HikariCP) for creating the connection pool.
To configure the connection pool any custom properties can be set in the *dataSourceProperties* section.

For example:

```groovy
dataSourceProperties = {
    dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
    ...
    maximumPoolSize = 10
    connectionTimeout = 50000
}
```
