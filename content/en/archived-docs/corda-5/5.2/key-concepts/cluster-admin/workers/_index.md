---
description: "Learn about the Corda 5 worker processors and their own operational responsibilities."
title: "Workers"
date: 2023-07-24
menu:
  corda52:
    identifier: corda52-cluster-admin-workers
    parent: corda52-key-concepts-cluster-admin
    weight: 2000
---

# Workers

Corda 5 introduces a distributed architecture for the Corda runtime that is based on worker processes. There are different types of worker processors which each have their own operational responsibility and, because each worker is stateless, it is possible to scale horizontally.

{{< 
  figure
	 src="featured_workers.png"
   width="75%"
	 figcaption="Corda Workers"
>}}

Currently, Corda uses the following types of workers:

* Crypto workers — the only worker type that can load sensitive cryptographic material such as private keys.
* Database workers — responsible for database configuration and management.
* Persistence workers — responsible for flow and ledger persistence operations within the database sandbox.
* Uniqueness workers — provide fixed-function checking for spent input and reference states and time-window validation.
* Flow workers — execute the {{< tooltip >}}CorDapp{{< /tooltip >}} code represented by {{< tooltip >}}flows{{< /tooltip >}}.
* Flow mapper workers — maintain the mapping and context switching between flows and sessions.
* Verification workers — verify ledger transactions within the ledger sandbox.
* Membership workers — provide all membership capabilities, such as joining an application network and discovering other {{< tooltip >}}members{{< /tooltip >}} in the network.
* Gateway workers — responsible for establishing {{< tooltip >}}TLS{{< /tooltip >}} connections with the gateways from other clusters and sending or receiving messages via HTTPS; this is typically internet facing.
* P2P Link Manager workers — responsible for delivering messages between two virtual nodes in a secure and reliable way.
* REST workers — expose the Corda REST API used for administration and flow execution.
* Token selection workers — selects the set of states to use as input states in a UTXO transaction.

Workers are typically referred to in the plural form because they are designed to be deployed with multiple replicas (for example, [Kubernetes replica sets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)) to achieve high availability.
Each worker instance is stateless, and work in the cluster is distributed to all available workers of a particular type. The number of replica workers needed is a function of the desired throughput and availability.
Workers are made available as [container images]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#download-and-push-container-images-to-a-registry" >}}) and R3 recommend deploying them to {{< tooltip >}}Kubernetes{{< /tooltip >}} via a [Helm chart]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#download-the-corda-helm-chart" >}}).
