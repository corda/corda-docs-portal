---
title: "Technology Stack"
date: 2023-07-24
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cluster-admin-tech-stack
    parent: corda5-key-concepts-cluster-admin
    weight: 1000
section_menu: corda5
---

# Technology Stack

This section examines the core technologies that underpin Corda. Corda 5 is a distributed application made of multiple stateles workers, as described in the [following section]({{< relref "#workers" >}}). This section contains the following:
* [Persistence](#persistence)
* [Key Management](#key-management)
* [Kafka](#kafka)
* [Load Balancers](#load-balancers)
* [Java/JVM](#javajvm)

## Persistence

Corda uses relational databases for its persistence layer. Currently, Corda supports PostgreSQL Version 14.4 only, but support for other types of databases may be added in future releases. Corda uses a number of databases which can be co-hosted on the same database host or even share a single database instance but seggregated by schema. All are logically separated with Corda managing connection details for each of the logical databases.

Broadly speaking, there are two groups of databases:
* [Cluster-wide databases]({{< relref "#cluster-databases" >}}) — contain data that is necessary for the running of the Corda cluster.
* [Virtual node databases]({{< relref "#virtual-node-databases" >}}) — contain data that is specific to a particular virtual node only.

{{< 
  figure
	 src="architecture-db.png"
   width="50%"
	 figcaption="Database Architecture"
>}}

### Cluster Databases

* `Config` — contains data that is used to support the general operation of the cluster such as data about CorDapps, worker configuration, virtual node metadata.
* `RBAC` (Role Based Access Control) — contains the data used for User Access Control. Currently, this is used for authorisation of the REST API.
* `Crypto` — contains (encrypted) cryptographic key material that is used for cluster-wide operations. <!--For more information, see [Key Management](#key-management).-->

### Virtual Node Databases 

Corda creates one of each of the following types per virtual node:
* `Vault` — contains the virtual node ledger data as well as data defined in CorDapp custom schemas.
* `Crypto` — contains the virtual node (encrypted) cryptographic key material such as ledger keys.
* `Uniqueness` (optional) — maintains a record of unspent and spent states generated as part of UTXO ledger transactions. This is only relevant for notary nodes.

### Database Management

All cluster-level databases must be initialized before Corda is operational. See the [Corda Deployment section]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#database" >}}) for information about how databases are bootstrapped.
Once the databases are created, Corda must be aware of where the dependent databases are. This happens in two places:
* `Config` database — the connection details for the config database are passed into all instances of the database worker when it is started. A read-only connection to this database must also be passed into the crypto worker to enable it to read crypto database configuration.
* All other databases — connection details for all other database are stored in a table inside the `Config` database. 

This design enables Corda to connect to a dynamic set of databases, specifically the virtual node databases, which are created and managed by Corda itself.
Virtual node databases are automatically created when a new virtual node is created. A future version may include functionality that allows a Cluster Administrator to create and manage virtual node databases outside of Corda.

Because database connection details, including credentials, are stored inside the `config` database, we suggest passwords, and other sensitive configuration values, are treated as “secrets”. For more information, see [Configuration Secrets]({{< relref "../../../deploying-operating/config/secrets.md">}}).

## Key Management

Corda required the following types of keys:
* P2P TLS
* P2P Session initiation
* MGM ECDH
* Notary
* Ledger
* CorDapp publisher code signing

All of the above keys are stored in the Crypto datbases (cluster and virtual nodes) and they are all encrypted at rest with “Wrapping keys”. <!--more info to follow-->

{{< note >}}
It is not currently possible to revoke or rotate keys.
{{< /note >}}

## Kafka
Apache Kafka version 3.2.0 is supported by Corda. It is used internally in the Corda Cluster as as message bus and can also be used to emit events from flow code. For more information see:
* [Configuring Kafka]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#kafka" >}})
* [External Messaging Administration]({{< relref "../../../deploying-operating/external-messaging/_index.md" >}})

## Load Balancers
A standard HTTP load balancer can be used to balance load between all REST API workers.
For information about configuring your load balancer, see the [Deploying]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#expose-the-rest-api" >}}) section.

## Java/JVM

All Corda components are hosted in a JAVA 17 compatible JVM. Azul Zulu 17 is currently the only supported, and tested, JVM, and is distributed with the Corda container images.