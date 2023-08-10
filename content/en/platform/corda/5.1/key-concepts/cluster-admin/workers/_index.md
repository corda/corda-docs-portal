---
title: "Workers"
date: 2023-07-24
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-cluster-admin-workers
    parent: corda51-key-concepts-cluster-admin
    weight: 2000
section_menu: corda51
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
* {{< tooltip >}}Flow workers{{< /tooltip >}} — execute the {{< tooltip >}}CorDapp{{< /tooltip >}} code represented by {{< tooltip >}}flows{{< /tooltip >}}.
* {{< tooltip >}}Membership workers{{< /tooltip >}} — provide all membership capabilities, such as joining an application network and discovering other {{< tooltip >}}members{{< /tooltip >}} in the network.
* {{< tooltip >}}Gateway workers{{< /tooltip >}} — responsible for establishing {{< tooltip >}}TLS{{< /tooltip >}} connections with the gateways from other clusters and sending or receiving messages via HTTPS; this is typically internet facing.
* {{< tooltip >}}P2P Link Manager workers{{< /tooltip >}} — responsible for delivering messages between two virtual nodes in a secure and reliable way. 
* {{< tooltip >}}REST workers{{< /tooltip >}} — expose the Corda REST API used for administration and flow execution.

Workers are typically referred to in the plural form because they are designed to be deployed with multiple replicas (for example, [Kubernetes replica sets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)) to achieve high availability. 
Each worker instance is stateless, and work in the cluster is distributed to all available workers of a particular type. The number of replica workers needed is a function of the desired throughput and availability.
Workers are made available as [docker images]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#download-and-push-container-images-to-a-registry" >}}), one for each type and we recommend they are deployed to {{< tooltip >}}Kubernetes{{< /tooltip >}} via a [Helm chart]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#download-the-corda-helm-chart" >}}).
