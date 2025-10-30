---
description: "Learn the most important key concepts for Corda 5 Cluster Administrators."
title: "Architecture for Cluster Administrators"
date: 2023-07-24
menu:
  corda51:
    identifier: corda51-key-concepts-cluster-admin
    parent: corda51-key-concepts
    weight: 3000
---

# Architecture for Cluster Administrators

This section describes Corda 5 from the perspective of a [Corda cluster Administrator]({{< relref "../../../../../about-the-docs/_index.md#cluster-administrator" >}}). If you are new to Corda, refer to [Corda Fundamentals]({{< relref "../fundamentals/_index.md" >}}) to familiarize yourself with the key concepts. If you are familiar with Corda 4, remember that while {{< version >}} is an evolution of Corda, it is quite different from an infrastructure and administration point of view.

Corda 5 is a distributed application made of multiple stateless workers, as described in the [Workers]({{< relref "workers/_index.md" >}}) section. The following sections examine the core technologies that underpin Corda:

* [Persistence](#persistence)
* [Key Management](#key-management)
* [Kafka](#kafka)
* [Load Balancers](#load-balancers)
* [Java/JVM](#javajvm)
* [Observability](#observability)

## Persistence

Corda uses relational databases for its persistence layer. Corda uses a number of databases which can be co-hosted on the same database server or even share a single database instance but segregated by schemas. All are logically separated, with Corda managing the connection details for each of the logical databases.

Broadly speaking, there are two groups of databases:

* [Cluster-wide databases]({{< relref "#cluster-databases" >}}) — contain data that is necessary for the running of the Corda cluster.
* [Virtual node databases]({{< relref "#virtual-node-databases" >}}) — contain data that is specific to a particular {{< tooltip >}}virtual node{{< /tooltip >}}.

The following diagram provides a high-level overview of the Corda databases:

{{<
  figure
	 src="architecture-db.png"
   width="40%"
	 figcaption="Database Architecture"
>}}

### Cluster Databases

* `Config` — contains data that is used to support the general operation of the cluster, such as data about {{< tooltip >}}CorDapps{{< /tooltip >}}, worker configuration, and virtual node metadata.
* `{{< tooltip >}}RBAC{{< /tooltip >}}` (Role Based Access Control) — contains the data used for User Access Control. Currently, this is used for authorization of the REST API.
* `Crypto` — contains (encrypted) cryptographic key material that is used for cluster-wide operations. <!--For more information, see [Key Management](#key-management).-->

### Virtual Node Databases

Corda requires one of each of the following types per virtual node:

* `Vault` — contains the virtual node ledger data as well as data defined in CorDapp custom schemas.
* `Crypto` — contains the virtual node (encrypted) cryptographic key material such as {{< tooltip >}}ledger keys{{< /tooltip >}}.
* `Uniqueness` (optional) — maintains a record of unspent and spent {{< tooltip >}}states{{< /tooltip >}} generated as part of {{< tooltip >}}UTXO{{< /tooltip >}} ledger transactions. This is only relevant for {{< tooltip >}}notary{{< /tooltip >}} nodes.

### Database Management

All cluster-level databases must be initialized before Corda is operational. See the [Corda Deployment section]({{< relref "../../deploying-operating/deployment/deploying/_index.md#database" >}}) for information about how databases are bootstrapped.
Once the databases are created, Corda must be aware of where the dependent databases are. This happens in two places:

* `Config` database — the connection details for the config database are passed into all instances of the {{< tooltip >}}database worker{{< /tooltip >}} when it is started. A read-only connection to this database must also be passed into the {{< tooltip >}}crypto worker{{< /tooltip >}} to enable it to read crypto database configuration.
* All other databases — connection details for all other databases are stored in a table inside the `Config` database.

This design enables Corda to connect to a dynamic set of databases, specifically the virtual node databases, which are created and managed by Corda itself.
Virtual node databases are automatically created when a new virtual node is created. A future version may include functionality that allows a Cluster Administrator to create and manage virtual node databases outside of Corda.

Because database connection details, including credentials, are stored inside the `config` database, we suggest passwords, and other sensitive configuration values, are treated as “secrets”. For more information, see [Configuration Secrets]({{< relref "../../deploying-operating/config/secrets.md">}}).

## Key Management

Corda requires the following types of keys:

* P2P
* P2P Session initiation
* MGM
* Notary
* Ledger
* CorDapp publisher code signing

{{< note >}}
It is not currently possible to revoke or rotate keys.
{{< /note >}}

For a list of the keys and certificates used by Corda, see the [Reference]({{< relref "../../reference/certificates.md" >}}) section.

### Key Wrapping

All keys are stored in the Crypto databases (cluster and virtual nodes) and they are all encrypted at rest with “wrapping keys”:

{{<
  figure
	 src="wrapping-keys.png"
   width="75%"
	 figcaption="Wrapping Keys"
>}}

The diagram illustrates that key wrapping is hierarchical. The master wrapping key protects other wrapping keys, such as the virtual node related keys, which in turn protect the private keys used by Corda. It must never be possible for someone with a copy of the Corda database, or a virtual node database, to decrypt the keys stored in the database using other information stored in the database. Therefore, the master wrapping key, or the information required to generate this key, must be stored and managed outside Corda. This can be achieved in one of the following ways:

* Pass a passphrase and salt, to generate the master key, into the crypto worker processes. For more information, see [Default Secrets Service]({{< relref "../../deploying-operating/deployment/deploying/_index.md#default-secrets-service" >}}).
* {{< enterprise-icon noMargin="true" >}} Store and manage the master in an external key management system that Corda retrieves when required. For more information, see [External Secrets Service]({{< relref "../../deploying-operating/deployment/deploying/_index.md#external-secrets-service" >}}).

## Kafka

Corda uses Apache Kafka internally as a message bus and also to emit events from {{< tooltip >}}flow{{< /tooltip >}} code. For more information see:

* [Configuring Kafka]({{< relref "../../deploying-operating/deployment/deploying/_index.md#kafka-bootstrap-servers" >}})
* [External Messaging Administration]({{< relref "../../deploying-operating/external-messaging/_index.md" >}}) {{< enterprise-icon >}}

## Load Balancers

A standard HTTP load balancer can be used to balance the load between all REST API workers.
For information about configuring your load balancer, see the [Deploying]({{< relref "../../deploying-operating/deployment/deploying/_index.md#expose-the-rest-api" >}}) section.

## Java/JVM

All Corda components are hosted in a JAVA 17 compatible JVM. Azul Zulu 17 is currently the only supported and tested JVM, and is distributed with the Corda container images.

## Observability

### Logging

All components in a Corda cluster produce logs at level INFO by default. These are sent to stdout/stderr and can easily be integrated with a log collector or aggregator of choice. All application-level logging is handled by Log4J which means the log level and target can be changed through customizing the Log4J config.

For more information about retrieving logs from {{< tooltip >}}Kubernetes{{< /tooltip >}}, see [Metrics]({{< relref "../../deploying-operating/observability/logs.md" >}}).

### Metrics

Corda workers expose metrics to provide a better insight into the system as a whole. These metrics are exposed as [Prometheus](https://prometheus.io/)-compatible HTTP endpoints that can be consumed by a collector and visualization tool of choice. For more information, see [Metrics]({{< relref "../../deploying-operating/observability/metrics/_index.md" >}}).