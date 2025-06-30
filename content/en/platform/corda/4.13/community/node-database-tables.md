---
aliases:
- /head/node-database-tables.html
- /HEAD/node-database-tables.html
- /node-database-tables.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-13:
    identifier: corda-community-4-13-node-database-tables
    parent: corda-community-4-13-corda-nodes-index
    weight: 1090
tags:
- node
- database
- tables
title: Database tables
---


# Database tables

A Corda node database contains tables corresponding to the various services that the node provides.
It also contains custom tables defined by the CorDapps that are installed on the node.
Currently all these tables share the same database schema, but in a future release they will be isolated from each other.

{{< note >}}
Unless specified otherwise the node tables are for internal use and can change between versions.

{{< /note >}}
Some tables, especially the ones where the `Ledger` is maintained are append-only and the data will never change.


{{< warning >}}
Manually adding, removing or updating any data should only be done with great care. Corda is a distributed ledger and modifying
data could lead to unexpected behaviour and inconsistent views of the ledger.

{{< /warning >}}



## Network map


### Node infos

These are tables that store the NodeInfo of other network participants.
They are just a local cache that is kept in sync with the network map server.
By calling `rpc.clearNetworkMapCache()` all these tables will be cleared and recreated from the network map server. For more information, see [The network map]({{< relref "network-map.md" >}}).

{{< figure alt="node info tables" width=80% zoom="/en/images/node_info_tables.png" >}}

{{< table >}}

|NODE_INFOS|Stores `NodeInfo` objects. The principal table.|
|------------------------------|------------------------------------------------------------------------------------------|
|NODE_INFO_ID|Primary key|
|NODE_INFO_HASH|Hash of the binary nodeInfo file|
|PLATFORM_VERSION|Declared version of the participant node.|
|SERIAL|Version of the NodeInfo|

{{< /table >}}


{{< table >}}

|NODE_INFO_HOSTS|Many-to-one addresses to node|
|------------------------------|------------------------------------------------------------------------------------------|
|HOSTS_ID|Primary key|
|HOST_NAME|Host name of the participant’s node|
|PORT|Port|
|NODE_INFO_ID|FK to NODE_INFOS|

{{< /table >}}


{{< table >}}

|NODE_INFO_PARTY_CERT|Legal identity for a network participant|
|------------------------------|------------------------------------------------------------------------------------------|
|PARTY_NAME|The X500 name|
|OWNING_KEY_HASH|The public key|
|ISMAIN|If this is a main identity|
|PARTY_CERT_BINARY|The certificate chain|

{{< /table >}}


{{< table >}}

|NODE_LINK_NODEINFO_PARTY|Many-to-Many link between the hosts and the legal identities|
|------------------------------|------------------------------------------------------------------------------------------|
|NODE_INFO_ID|FK to Node_info|
|PARTY_NAME|FK to NODE_INFO_PARTY_CERT|

{{< /table >}}


### Node identities

The following four tables are used by the `IdentityService` and are created from the NodeInfos.
They are append only tables used for persistent caching.
They will also be cleared on `rpc.clearNetworkMapCache()`.
For more information, see [API: Identity]({{< relref "api-identity.md" >}}) and [Node services]({{< relref "node-services.md" >}}).


{{< table >}}

|NODE_IDENTITIES|Maps public key hash to identity|
|------------------------------|------------------------------------------------------------------------------------------|
|PK_HASH|The public key hash.|
|IDENTITY_VALUE|The certificate chain.|

{{< /table >}}


{{< table >}}

|NODE_NAMED_IDENTITIES|Maps X500 name of participant to public key hash |
|------------------------------|------------------------------------------------------------------------------------------|
|NAME|The x500 name.|
|PK_HASH|The public key hash.|

{{< /table >}}


{{< table >}}

|NODE_IDENTITIES_NO_CERT|Maps public key hash to X500 name of participant |
|------------------------------|------------------------------------------------------------------------------------------|
|PK_HASH|The public key hash.|
|NAME|The x500 name.|

{{< /table >}}


{{< table >}}

|NODE_HASH_TO_KEY|Maps public key hash to public key |
|------------------------------|------------------------------------------------------------------------------------------|
|PK_HASH|The public key hash.|
|PUBLIC_KEY|The public key.|

{{< /table >}}


### Network parameters

For more information, see [The network map: Network parameters]({{< relref "network-map.md#network-parameters" >}}).
Each downloaded network parameters file will create an entry in this table.
The historical network parameters are used when validating transactions, which makes this table logically part of the `Ledger`.
It is an append-only table and the size will be fairly small.


{{< table >}}

|NODE_NETWORK_PARAMETERS|Stores downloaded network parameters |
|------------------------------|------------------------------------------------------------------------------------------|
|HASH|The hash of the downloaded file. Used as a primary key.|
|EPOCH|The version of the parameters|
|PARAMETERS_BYTES|The serialized bytes|
|SIGNATURE_BYTES|The signature|
|CERT|First signer certificate in the certificate chain.|
|PARENT_CERT_PATH|Parent certificate path of signer.|

{{< /table >}}


## Ledger

The ledger data is formed of transactions and attachments.
In future versions this data will be encrypted using SGX.
For more information, see [Ledger]({{< relref "key-concepts-ledger.md" >}}).


### Attachments

For more information, see [Working with attachments]({{< relref "../enterprise/get-started/tutorials/supplementary-tutorials/tutorial-attachments.md" >}}) and [Node services]({{< relref "node-services.md" >}}).

{{< figure alt="attachments tables" width=80% zoom="/en/images/attachments_tables.png" >}}

{{< table >}}

|NODE_ATTACHMENTS|Stores attachments|
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
|ATT_ID|The hash of the content of the file.|
|CONTENT|The binary content|
|FILENAME|Not used at the moment.|
|INSERTION_DATE|Date.|
|UPLOADER|One of: `p2p`, `app`, `rpc`, `unknown`. Currently used for for determining if this attachment is safe to execute during transaction verification.|
|VERSION|The version of the JAR file.|

{{< /table >}}


{{< table >}}

|NODE_ATTACHMENTS_CONTRACTS|Many-to-one contracts per attachment; empty for non-contract attachments |
|------------------------------|--------------------------------------------------------------------------------------------|
|ATT_ID|Foreign key|
|CONTRACT_CLASS_NAME|The fully qualified contract class name; for example, `net.corda.finance.contracts.asset.Cash`|

{{< /table >}}


{{< table >}}

|NODE_ATTACHMENTS_SIGNERS|Many-to-one JAR signers of an attachment; empty if not signed |
|------------------------------|------------------------------------------------------------------------------------------|
|ATT_ID|Foreign key|
|SIGNER|Hex encoded public key of the JAR signer.|

{{< /table >}}


### Transactions

These are all the transactions that the node has created or has ever downloaded as part of transaction resolution. This table can grow very large.
It is an append-only table, and the data will never change.
For more information, see [Node services: DBTransactionStorage]({{< relref "node-services.md#dbtransactionstorage" >}}). This is the key ledger table used as a source of truth. In future, the content will be encrypted to preserve confidentiality.


{{< table >}}

|NODE_TRANSACTIONS|Corda transactions in a binary format|
|------------------------------|------------------------------------------------------------------------------------------|
|TX_ID|The hash of the transaction. Primary key.|
|TRANSACTION_VALUE|The binary representation of the transaction.|
|STATE_MACHINE_RUN_ID|The flow ID associated with this transaction.|
|STATUS|`VERIFIED` or `UNVERIFIED`|

{{< /table >}}







### Contract upgrades



{{< table >}}

|NODE_CONTRACT_UPGRADES|Represents an authorisation to upgrade a state_ref to a contract |
|------------------------------|------------------------------------------------------------------------------------------|
|STATE_REF|The authorised state.|
|CONTRACT_CLASS_NAME|The contract.|

{{< /table >}}

This table should be empty when no states are authorised for upgrade or after authorised states have been upgraded.


### Scheduling


{{< table >}}

|NODE_SCHEDULED_STATES|Contains scheduled states|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|SCHEDULED_AT|Timestamp when this state will execute.|

{{< /table >}}

This table should be empty when no events are scheduled.


### Storage of private keys


{{< table >}}

|NODE_OUR_KEY_PAIRS|Stores anonymous identities|
|------------------------------|------------------------------------------------------------------------------------------|
|PUBLIC_KEY_HASH|Primary key|
|PRIVATE_KEY|Binary private key|
|PUBLIC_KEY|Binary public key|

{{< /table >}}


{{< table >}}

|PK_HASH_TO_EXT_ID_MAP|Maps public keys to external ID; mainly used by CorDapps that need to simulate accounts |
|------------------------------|--------------------------------------------------------------------------------------------|
|EXTERNAL_ID|External ID|
|PUBLIC_KEY_HASH|Public key hash|

{{< /table >}}

These tables should be append-only.


### Node state machine

For more information, see [Node services]({{< relref "node-services.md" >}}).

{{< table >}}

|NODE_CHECKPOINTS|Stores high-level information about checkpoints|
|------------------------------|------------------------------------------------------------------------------------------|
|FLOW_ID|Primary key|
|STATUS|The status of the flow|
|COMPATIBLE|Whether the checkpoint is compatible with the current CorDapps/Corda version|
|PROGRESS_STEP|The progress step that the flow reached|
|FLOW_IO_REQUEST|The request type the flow suspended on|
|TIMESTAMP|The timestamp|

{{< /table >}}

{{< table >}}

|NODE_CHECKPOINT_BLOBS|Stores serialized flow checkpoint blobs|
|------------------------------|------------------------------------------------------------------------------------------|
|FLOW_ID|Primary key|
|CHECKPOINT_VALUE|Serialized information about the flow|
|FLOW_STATE|Serialized application stack|
|TIMESTAMP|The timestamp|

{{< /table >}}

{{< table >}}

|NODE_FLOW_RESULTS|Stores results of flows|
|------------------------------|------------------------------------------------------------------------------------------|
|FLOW_ID|Primary key|
|RESULT_VALUE|Serialized result of the flow|
|TIMESTAMP|The timestamp|

{{< /table >}}

{{< table >}}

|NODE_FLOW_EXCEPTIONS|Stores exceptions thrown by flows|
|------------------------------|------------------------------------------------------------------------------------------|
|FLOW_ID|Primary key|
|TYPE|The class name of the exception|
|EXCEPTION_MESSAGE|The message of the exception|
|STACK_TRACE|The stack trace of the exception|
|EXCEPTION_VALUE|Serialized exception thrown by the flow|
|TIMESTAMP|The timestamp|

{{< /table >}}

{{< table >}}

|NODE_FLOW_METADATA|Stores exceptions thrown by flows|
|------------------------------|------------------------------------------------------------------------------------------|
|FLOW_ID|Primary key|
|INVOCATION_ID|The invocation ID of the flow|
|FLOW_NAME|The class name of the flow|
|FLOW_IDENTIFIER|The identifier of the flow|
|STARTED_TYPE|How the flow was started|
|FLOW_PARAMETERS|The parameters the flow was started with|
|CORDAPP_NAME|The name of the CorDapp that contains the flow|
|PLATFORM_VERSION|The platform version at the start time of the flow|
|STARTED_BY|The RPC user that started the flow|
|INVOCATION_TIME|The time the flow was originally invoked by RPC|
|START_TIME|The time the flow started inside the state machine|
|FINISH_TIME|The finish time of the flow|

{{< /table >}}

These tables will see the most intense read-write activity, especially `NODE_CHECKPOINTS` and `NODE_CHECKPOINT_BLOBS`. Depending on the installed flows and the traffic on the node the I/O operations on this
table will be the main bottleneck of the node performance.
There will be an entry for every running flow.
Draining the node means waiting for this table to become emtpy. Read more in: [Upgrading CorDapps on a node]({{< relref "node-operations-upgrade-cordapps.md" >}}).


{{< table >}}

|NODE_MESSAGE_IDS|Used for de-duplication of messages received by peers.|
|------------------------------|------------------------------------------------------------------------------------------|
|MESSAGE_ID|Message ID|
|INSERTION_TIME|Insertion time|
|SENDER|P2p sender|
|SEQUENCE_NUMBER|Sequence number|

{{< /table >}}


### Key value store


{{< table >}}

|NODE_PROPERTIES|General key value store. Currently only used for the flow draining mode.|
|------------------------------|------------------------------------------------------------------------------------------|
|PROPERTY_KEY|The key|
|PROPERTY_VALUE|The value|

{{< /table >}}


## Vault tables

Read more about the vault here [Vault]({{< relref "key-concepts-vault.md" >}}).

Note that the vault tables are guaranteed to remain backwards compatible and are safe to be used directly by third party applications.


{{< table >}}

|VAULT_STATES|Principal vault table.|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|CONSUMED_TIMESTAMP|When the state was consumed.|
|CONTRACT_STATE_CLASS_NAME|Contract class|
|LOCK_ID|The soft lock ID|
|LOCK_TIMESTAMP|The soft lock timestamp|
|NOTARY_NAME|The notary|
|RECORDED_TIMESTAMP|Recorded timestamp|
|STATE_STATUS|`CONSUMED` or `UNCONSUMED`|
|RELEVANCY_STATUS|`RELEVANT` or `NOT_RELEVANT`|
|CONSTRAINT_TYPE|The contract constraint.|
|CONSTRAINT_DATA|The hash or the composite key depending on the `CONSTRAINT_TYPE`|
|CONSUMING_TX_ID| When a state is consumed by a transaction, the ID of the consuming transaction is added to this column.|

{{< /table >}}

The `VAULT_STATES` table contains an entry for every relevant state.
This table records the status of states and allows CorDapps to soft lock states it intends to consume.
Depending on the installed CorDapps this table can grow. For example when fungible states are used.

In case this table grows too large, the DBA can choose to archive old consumed states.
The actual content of the states can be retrieved from the `NODE_TRANSACTIONS` table by deserializing the binary representation.


{{< table >}}

|VAULT_TRANSACTION_NOTES|Allows additional notes per transaction|
|------------------------------|------------------------------------------------------------------------------------------|
|SEQ_NO|Primary key|
|TRANSACTION_ID|The transaction|
|NOTE|The note|

{{< /table >}}


{{< table >}}

|STATE_PARTY|Maps participants to states|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|PUBLIC_KEY_HASH|The public key of the participant|
|X500_NAME|The name of the participant or null if unknown.|

{{< /table >}}


{{< table >}}

|V_PKEY_HASH_EX_ID_MAP| View used to map states to external IDs |
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|PUBLIC_KEY_HASH|The public key of the participant.|
|EXTERNAL_ID|The external ID.|

{{< /table >}}


### Fungible states

{{< figure alt="vault fungible states" width=80% zoom="/en/images/vault_fungible_states.png" >}}

{{< table >}}

|VAULT_FUNGIBLE_STATES|Properties specific to fungible states|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|ISSUER_NAME|Issuer|
|ISSUER_REF|Reference number used by the issuer|
|OWNER_NAME|X500 name of the owner, or null if unknown|
|QUANTITY|The amount.|

{{< /table >}}


{{< table >}}

|VAULT_FUNGIBLE_STATES_PARTS|Many-to-one participants to a fungible state|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|PARTICIPANTS|X500 name of participant.|

{{< /table >}}


### Linear states

{{< figure alt="vault linear states" width=80% zoom="/en/images/vault_linear_states.png" >}}

{{< table >}}

|VAULT_LINEAR_STATES|Properties specific to linear states|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|EXTERNAL_ID|The external ID of this linear state.|
|UUID|The internal ID of this linear state.|

{{< /table >}}


{{< table >}}

|VAULT_LINEAR_STATES_PARTS|Many-to-one participants to a linear state|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction ID|
|PARTICIPANTS|X500 name of participant.|

{{< /table >}}


## Liquibase database migration

These are [Liquibase](https://www.liquibase.org) proprietary tables used by Corda internally to manage schema change and evolution.


{{< table >}}

|DATABASECHANGELOG|Read more: [DATABASECHANGELOG](https://www.liquibase.org/documentation/databasechangelog_table.html)|
|------------------------------|------------------------------------------------------------------------------------------------------|
|ID||
|AUTHOR||
|FILENAME||
|DATEEXECUTED||
|ORDEREXECUTED||
|EXECTYPE||
|MD5SUM||
|DESCRIPTION||
|COMMENTS||
|TAG||
|LIQUIBASE||
|CONTEXTS||
|LABELS||
|DEPLOYMENT_ID||

{{< /table >}}


{{< table >}}

|DATABASECHANGELOGLOCK|Read more: [DATABASECHANGELOGLOCK](https://www.liquibase.org/documentation/databasechangeloglock_table.html)|
|------------------------------|--------------------------------------------------------------------------------------------------------------|
|ID||
|LOCKED||
|LOCKGRANTED||
|LOCKEDBY||

{{< /table >}}
