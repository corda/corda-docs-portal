---
description: "Learn about communication within a Corda 5 cluster and from outside a Corda 5 cluster."
title: "Cluster Communications"
date: 2023-07-24
version: 'Corda 5.2'
menu:
  corda52:
    identifier: corda52-cluster-admin-communications
    parent: corda52-key-concepts-cluster-admin
    weight: 4000
section_menu: corda52
---

# Cluster Communications

Communication between workers, within a cluster, is mostly achieved through the internal message bus, integrated with {{< tooltip >}}Kafka{{< /tooltip >}}. However, communication originating from outside a cluster usually uses the HTTP protocol.

## REST

Interaction with the Corda cluster for administration or {{< tooltip >}}flow{{< /tooltip >}} management uses a [REST API]({{< relref "../../../reference/rest-api/_index.md" >}}) over standard secure HTTP (HTTPS).
These HTTP REST endpoints are exposed by the {{< tooltip >}}REST workers{{< /tooltip >}} in the cluster.
Like other {{< tooltip >}}worker{{< /tooltip >}} types, REST workers are stateless, so requests can be divided across all REST workers using a standard HTTP load balancer, which must be exposed to the application and/or user that interacts with the cluster.

HTTP requests are authenticated using basic authentication, and authorization is based on Corda’s [RBAC capabilities]({{< relref "../../../deploying-operating/config-users/_index.md" >}}).

## P2P

Communication between different Corda clusters to support distributed workflows, that is peer-to-peer (P2P) communication, also uses standard secure HTTP (HTTPS).
The components of the peer-to-peer communications layer are responsible for delivering messages between virtual nodes in a secure and reliable way.
If the two virtual nodes communicating reside in the same cluster, the messages can be routed back without exiting the cluster at all.
If the two virtual nodes communicating reside in separate clusters, the {{< tooltip >}}P2P link manager{{< /tooltip >}} processor is responsible for establishing end-to-end authenticated sessions with the link managers on the other cluster in order to transfer the messages in a secure way.
The link manager is also responsible for ensuring the message is delivered reliably in the case of any transient issues in the network path between the two clusters.
Any messages destined for a separate cluster are forwarded by the link manager to the P2P gateway, which forwards them to the P2P gateway of the other cluster via HTTPS.
A gateway can connect to another gateway in a separate cluster via mutual {{< tooltip >}}TLS{{< /tooltip >}}, depending on the policy of the application network.
