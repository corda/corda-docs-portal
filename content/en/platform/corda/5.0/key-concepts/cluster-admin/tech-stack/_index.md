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

This section examines the core technologies that underpin Corda. Corda 5 is a distributed application made of multiple stateless workers, as described in the [following section]({{< relref "../workers" >}}). This section contains the following:
* [Persistence](#persistence)
* [Key Management](#key-management)
* [Kafka](#kafka)
* [Load Balancers](#load-balancers)
* [Java/JVM](#javajvm)

## Persistence

Corda uses relational databases for its persistence layer. Currently, Corda only supports PostgreSQL Version 14.4, but support for other types of databases may be added in future releases. Corda uses a number of databases which can be co-hosted on the same database host or even share a single database instance but segregated by schema. All are logically separated, with Corda managing the connection details for each of the logical databases.

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

* `Config` — contains data that is used to support the general operation of the cluster, such as data about {{< tooltip >}}CorDapps{{< /tooltip >}}, worker configuration, and virtual node metadata.
* `RBAC` (Role Based Access Control) — contains the data used for User Access Control. Currently, this is used for authorization of the REST API.
* `Crypto` — contains (encrypted) cryptographic key material that is used for cluster-wide operations. <!--For more information, see [Key Management](#key-management).-->

### Virtual Node Databases 

Corda creates one of each of the following types per virtual node:
* `Vault` — contains the virtual node ledger data as well as data defined in CorDapp custom schemas.
* `Crypto` — contains the virtual node (encrypted) cryptographic key material such as ledger keys.
* `Uniqueness` (optional) — maintains a record of unspent and spent states generated as part of UTXO ledger transactions. This is only relevant for notary nodes.

### Database Management

All cluster-level databases must be initialized before Corda is operational. See the [Corda Deployment section]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#database" >}}) for information about how databases are bootstrapped.
Once the databases are created, Corda must be aware of where the dependent databases are. This happens in two places:
* `Config` database — the connection details for the config database are passed into all instances of the {{< tooltip >}}database worker{{< /tooltip >}} when it is started. A read-only connection to this database must also be passed into the crypto worker to enable it to read crypto database configuration.
* All other databases — connection details for all other databases are stored in a table inside the `Config` database. 

This design enables Corda to connect to a dynamic set of databases, specifically the virtual node databases, which are created and managed by Corda itself.
Virtual node databases are automatically created when a new virtual node is created. A future version may include functionality that allows a Cluster Administrator to create and manage virtual node databases outside of Corda.

Because database connection details, including credentials, are stored inside the `config` database, we suggest passwords, and other sensitive configuration values, are treated as “secrets”. For more information, see [Configuration Secrets]({{< relref "../../../deploying-operating/config/secrets.md">}}).

## Key Management

Corda requires the following types of keys:
* P2P TLS
* P2P Session initiation
* MGM {{< tooltip >}}ECDH{{< /tooltip >}}
* Notary
* Ledger
* CorDapp publisher code signing

All of these keys are stored in the Crypto databases (cluster and virtual nodes) and they are all encrypted at rest with “wrapping keys”. 

{{< 
  figure
	 src="wrapping-keys.png"
   width="75%"
	 figcaption="Wrapping Keys"
>}}

The diagram illustrates that key wrapping is hierarchical. The master wrapping key protects other wrapping keys, such as the virtual node related keys, which in turn protect the private keys used by Corda. It must never be possible for someone with a copy of the Corda database, or a virtual node database, to decrypt the keys stored in the database using other information stored in the database. Threfore, the master wrapping key, or the information required to generate this key, must be stored and managed outside Corda. This can be achieved in one of the following ways:
* Pass a passphrase and salt, to generate the master key, into the crypto worker processes. For more information, see [Default Secrets Service]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#default-secrets-service" >}}).
* {{< enterprise-icon noMargin="true" >}} Store and manage the master in an external key management system that Corda retrieves when required. For more information, see [External Secrets Service]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#external-secrets-service" >}}).

{{< note >}}
It is not currently possible to revoke or rotate keys.
{{< /note >}}

## Kafka
Apache Kafka version 3.2.0 is supported by Corda. It is used internally in the Corda Cluster as a message bus and can also be used to emit events from {{< tooltip >}}flow{{< /tooltip >}} code. For more information see:
* [Configuring Kafka]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#kafka" >}})
* [External Messaging Administration]({{< relref "../../../deploying-operating/external-messaging/_index.md" >}}) {{< enterprise-icon >}}

## Load Balancers
A standard HTTP load balancer can be used to balance the load between all REST API workers.
For information about configuring your load balancer, see the [Deploying]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#expose-the-rest-api" >}}) section.

## Java/JVM

All Corda components are hosted in a JAVA 17 compatible JVM. Azul Zulu 17 is currently the only supported and tested JVM, and is distributed with the Corda container images.
