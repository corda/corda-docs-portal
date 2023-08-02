---
title: "Workers"
date: 2023-07-24
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cluster-admin-workers
    parent: corda5-key-concepts-cluster-admin
    weight: 2000
section_menu: corda5
---

# Workers 

Corda 5 introduces a distributed architecture for the Corda runtime that is based on worker processes. There are different types of worker processors which each have their own operational responsibility and, because each worker is stateless, it is possible to scale horizontally.

{{< 
  figure
	 src="workers.png"
   width="75%"
	 figcaption="Corda Workers"
>}}

Currently, Corda uses the following types of workers:

* {{< tooltip >}}Crypto workers{{< /tooltip >}} — the only worker type that can load sensitive cryptographic material such as private keys.
* {{< tooltip >}}Database workers{{< /tooltip >}} — responsible for all persistence operations (read, write, update) for the cluster or on behalf of the virtual nodes.
* Flow workers — execute the {{< tooltip >}}CorDapp{{< /tooltip >}} code represented by {{< tooltip >}}flows{{< /tooltip >}}.
* Member workers — provide all membership capabilities, such as joining an application network and discovering other members in the network.
* P2P Gateway — responsible for establishing TLS connections with the gateways from other clusters and sending or receiving messages via HTTPS; this is typically internet facing.
* P2P Link Managers — responsible for delivering messages between two virtual nodes in a secure and reliable way. 
* REST workers — expose the Corda REST API used for administration and flow execution.

Workers are typically referred to in the plural form because they are designed to be deployed with multiple replicas (for example, [Kubernetes replica sets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)) to achieve high availability. 
Each worker instance is stateless, and work in the cluster is distributed to all available workers of a particular type. The number of replica workers needed is a function of the desired throughput and availability.
Workers are made available as [docker images]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#download-and-push-container-images-to-a-registry" >}}), one for each type and we recommend they are deployed to Kubernetes via a [Helm chart]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#download-the-corda-helm-chart" >}}).
