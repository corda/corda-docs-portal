---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating-db
tags:
- node
- database
- tables
title: Database tables
weight: 50
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


### Node info

These are tables that store the node info of other network participants.
They are just a local cache that is kept in sync with the network map server.
By calling `rpc.clearNetworkMapCache()` all these tables will be cleared and recreated from the network map server.

Read more here: network-map

{{< figure alt="node info tables" zoom="/en/images/node_info_tables.png" >}}

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
Read more in api-identity and node-services


{{< table >}}

|NODE_IDENTITIES|Maps a public key hash to an identity.|
|------------------------------|------------------------------------------------------------------------------------------|
|PK_HASH|The public key hash.|
|IDENTITY_VALUE|The certificate chain.|

{{< /table >}}


{{< table >}}

|NODE_NAMED_IDENTITIES|Maps the X500 name of a participant to a public key hash.|
|------------------------------|------------------------------------------------------------------------------------------|
|NAME|The x500 name.|
|PK_HASH|The public key hash.|

{{< /table >}}


{{< table >}}

|NODE_IDENTITIES_NO_CERT|Maps a public key hash to the X500 name of a participant.|
|------------------------------|------------------------------------------------------------------------------------------|
|PK_HASH|The public key hash.|
|NAME|The x500 name.|

{{< /table >}}


{{< table >}}

|NODE_HASH_TO_KEY|Maps a public key hash to a public key.|
|------------------------------|------------------------------------------------------------------------------------------|
|PK_HASH|The public key hash.|
|PUBLIC_KEY|The public key.|

{{< /table >}}


### Network parameters

Read more here: network-map.
Each downloaded network parameters file will create an entry in this table.
The historical network parameters are used when validating transactions, which makes this table logically part of the `Ledger`.
It is an append only table and the size will be fairly small.


{{< table >}}

|NODE_NETWORK_PARAMETERS|Stores the downloaded network parameters.|
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
Read more in key-concepts-ledger


### Attachments

Read more in tutorial-attachments and node-services

{{< figure alt="attachments tables" zoom="/en/images/attachments_tables.png" >}}

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

|NODE_ATTACHMENTS_CONTRACTS|Many-to-one contracts per attachment. Empty for non-contract attachments.|
|------------------------------|--------------------------------------------------------------------------------------------|
|ATT_ID|Foreign key|
|CONTRACT_CLASS_NAME|The fully qualified contract class name. E.g.: `net.corda.finance.contracts.asset.Cash`|

{{< /table >}}


{{< table >}}

|NODE_ATTACHMENTS_SIGNERS|Many-to-one JAR signers of an attachment. Empty if not signed.|
|------------------------------|------------------------------------------------------------------------------------------|
|ATT_ID|Foreign key|
|SIGNER|Hex encoded public key of the JAR signer.|

{{< /table >}}


### Transactions

These are all the transactions that the node has created or has ever downloaded as part of transaction resolution. This table can grow very large.
It is an append-only table, and the data will never change.
Read more in node-services - `DBTransactionStorage`
This is the key ledger table used as a source of truth. In the future the content will be encrypted to preserve confidentiality.


{{< table >}}

|NODE_TRANSACTIONS|Corda transactions in a binary format|
|------------------------------|---------------------------------------------------------------------------------------------|
|TX_ID|The hash of the transaction. Primary key.|
|TRANSACTION_VALUE|The binary representation of the transaction.|
|STATE_MACHINE_RUN_ID|The flow id associated with this transaction.|
|STATUS|`VERIFIED` or `UNVERIFIED`|
|TIMESTAMP|The insert or status update time of this transaction, as measured by the local node, in UTC.|

{{< /table >}}







### Contract upgrades

Read more in contract-upgrade


{{< table >}}

|NODE_CONTRACT_UPGRADES|Represents an authorisation to upgrade a state_ref to a contract.|
|------------------------------|------------------------------------------------------------------------------------------|
|STATE_REF|The authorised state.|
|CONTRACT_CLASS_NAME|The contract.|

{{< /table >}}

This table should be empty when no states are authorised for upgrade or after authorised states have been upgraded.


### Scheduling

Read more in event-scheduling


{{< table >}}

|NODE_SCHEDULED_STATES|Contains scheduled states|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction id|
|SCHEDULED_AT|Timestamp when this state will execute.|

{{< /table >}}

This table should be empty when no events are scheduled.


### Storage of private keys


{{< table >}}

|NODE_OUR_KEY_PAIRS|Stores the anonymous identities|
|------------------------------|------------------------------------------------------------------------------------------|
|PUBLIC_KEY_HASH|Primary key|
|PUBLIC_KEY|Binary public key|
|PRIVATE_KEY|Binary private key|
|PRIVATE_KEY_MATERIAL_WRAPPED|Binary (encrypted) private key|
|SCHEME_CODE_NAME|String code representing the key algorithm|

{{< /table >}}

The columns `PRIVATE_KEY_MATERIAL_WRAPPED` and `SCHEME_CODE_NAME` are populated, instead of the column `PRIVATE_KEY`,
if an HSM is configured for anonymous identities. For more details about this feature, read [Using an HSM with confidential identities](confidential-identities-hsm.md).


{{< table >}}

|PK_HASH_TO_EXT_ID_MAP|Maps public keys to external ids. Mainly used by CorDapps that need to simulate accounts.|
|------------------------------|--------------------------------------------------------------------------------------------|
|EXTERNAL_ID|External id|
|PUBLIC_KEY_HASH|Public key hash|

{{< /table >}}

These tables should be append only.


### Node state machine

Read more in node-services

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
|INVOCATION_ID|The invocation id of the flow|
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
Draining the node means waiting for this table to become emtpy. Read more in: [Upgrading CorDapps on a node](node-operations-upgrade-cordapps.md).


{{< table >}}

|NODE_MESSAGE_IDS|Used for de-duplication of messages received by peers.|
|------------------------------|------------------------------------------------------------------------------------------|
|MESSAGE_ID|Message id|
|INSERTION_TIME|Insertion time|
|SENDER|P2p sender|
|SEQUENCE_NUMBER|Sequence number|

{{< /table >}}

The *NodeJanitor* is a background process that will clean up old entries from this table.
The size should be fairly constant.


### Key value store


{{< table >}}

|NODE_PROPERTIES|General key value store. Currently only used for the flow draining mode.|
|------------------------------|------------------------------------------------------------------------------------------|
|PROPERTY_KEY|The key|
|PROPERTY_VALUE|The value|

{{< /table >}}


## Vault tables

Read more about the vault here key-concepts-vault.

Note that the vault tables are guaranteed to remain backwards compatible and are safe to be used directly by third party applications.


{{< table >}}

|VAULT_STATES|Principal vault table.|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction id|
|CONSUMED_TIMESTAMP|When the state was consumed.|
|CONTRACT_STATE_CLASS_NAME|Contract class|
|LOCK_ID|The soft lock id|
|LOCK_TIMESTAMP|The soft lock timestamp|
|NOTARY_NAME|The notary|
|RECORDED_TIMESTAMP|Recorded timestamp|
|STATE_STATUS|`CONSUMED` or `UNCONSUMED`|
|RELEVANCY_STATUS|`RELEVANT` or `NOT_RELEVANT`|
|CONSTRAINT_TYPE|The contract constraint.|
|CONSTRAINT_DATA|The hash or the composite key depending on the `CONSTRAINT_TYPE`|

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
|TRANSACTION_ID|Reference to a state - transaction id|
|PUBLIC_KEY_HASH|The pk of the participant|
|X500_NAME|The name of the participant or null if unknown.|

{{< /table >}}


{{< table >}}

|V_PKEY_HASH_EX_ID_MAP|This is a database view used to map states to external ids.|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction id|
|PUBLIC_KEY_HASH|The public key of the participant.|
|EXTERNAL_ID|The external id.|

{{< /table >}}


### Fungible states

{{< figure alt="vault fungible states" zoom="/en/images/vault_fungible_states.png" >}}

{{< table >}}

|VAULT_FUNGIBLE_STATES|Properties specific to fungible states|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction id|
|ISSUER_NAME|Issuer|
|ISSUER_REF|Reference number used by the issuer|
|OWNER_NAME|X500 name of the owner, or null if unknown|
|QUANTITY|The amount.|

{{< /table >}}


{{< table >}}

|VAULT_FUNGIBLE_STATES_PARTS|Many-to-one participants to a fungible state|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction id|
|PARTICIPANTS|X500 name of participant.|

{{< /table >}}


### Linear states

{{< figure alt="vault linear states" zoom="/en/images/vault_linear_states.png" >}}

{{< table >}}

|VAULT_LINEAR_STATES|Properties specific to linear states|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction id|
|EXTERNAL_ID|The external id of this linear state.|
|UUID|The internal id of this linear state.|

{{< /table >}}


{{< table >}}

|VAULT_LINEAR_STATES_PARTS|Many-to-one participants to a linear state|
|------------------------------|------------------------------------------------------------------------------------------|
|OUTPUT_INDEX|Reference to a state - index in transaction|
|TRANSACTION_ID|Reference to a state - transaction id|
|PARTICIPANTS|X500 name of participant.|

{{< /table >}}


## Hot cold setup


{{< table >}}

|NODE_MUTUAL_EXCLUSION|Lock for hot-cold deployments. Only 1 entry with the active machine.|
|------------------------------|------------------------------------------------------------------------------------------|
|MUTUAL_EXCLUSION_ID|Primary key|
|MACHINE_NAME|The machine holding the lock|
|PID|The process id|
|MUTUAL_EXCLUSION_TIMESTAMP|When the lock was taken.|
|VERSION|The version|

{{< /table >}}


## Metering


{{< table >}}

|NODE_METERING_DATA|Metering data recorded for signing events on this node|
|------------------------------|------------------------------------------------------------------------------------------|
|TIMESTAMP|The time in UTC, to the nearest hour, that the metering count was recorded|
|SIGNING_ID|An external identifier that signed a transaction, or UNMAPPED_IDENTITY|
|TRANSACTION_TYPE|Whether this was a normal transaction, a contract upgrade, a notary change, or an indication that signing events were discarded due to heavy memory use or restarting a node|
|CORDAPP_STACK_ID|An identifier linking to the NODE_METERING_CORDAPPS table|
|COMMAND_ID|An identifier linking to the NODE_METERING_COMMANDS table|
|COUNT|The total number of events in this window with the above characteristics|
|IS_COLLECTED|Whether these counts have been gathered by collection tooling|
|VERSION|The platform version at which this data was recorded|

{{< /table >}}


{{< table >}}

|NODE_METERING_CORDAPPS|A record of what CorDapps were involved in signing events|
|------------------------------|------------------------------------------------------------------------------------------|
|STACK_HASH|An identifier for the set of CorDapps involved in a signing event|
|CORDAPP_HASH|The JAR hash of one CorDapp involved in the signing event|
|POSITION|The position in the stack this CorDapp was present at|
|ID|A unique identifier for this row|

{{< /table >}}


{{< table >}}

|NODE_METERING_COMMANDS|A record of what commands were on a transaction that has been metered|
|------------------------------|------------------------------------------------------------------------------------------|
|COMMAND_HASH|An identifier for the set of commands on a transaction|
|COMMAND_CLASS|The class name of a command in the set|
|ID|A unique identifier for this row|

{{< /table >}}


{{< table >}}

|NODE_CORDAPP_METADATA|Metadata about CorDapps that have been installed on the node|
|------------------------------|------------------------------------------------------------------------------------------|
|CORDAPP_HASH|The JAR hash of the installed CorDapp|
|NAME|The name of the CorDapp|
|VENDOR|The vendor of the CorDapp|
|VERSION|The version of the CorDapp|

{{< /table >}}


{{< table >}}

|NODE_CORDAPP_SIGNERS|Signing keys for a particular CorDapp|
|------------------------------|------------------------------------------------------------------------------------------|
|CORDAPP_HASH|The JAR hash of the CorDapp|
|SIGNING_KEY_HASH|Hash of the public key used to sign this CorDapp|

{{< /table >}}


## Liquibase database migration

These are [Liquibase](https://www.liquibase.org) proprietary tables used by Corda internally and by CorDapps to manage schema change and evolution.


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
