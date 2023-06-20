---
title: "Corda 5.0 Platform Support"
date: 2023-05-23
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-platform-support
    parent: corda5-release-notes
    weight: 1000
section_menu: corda5
---

<style>
table th:first-of-type {
    width: 60%;
}
table th:nth-of-type(2) {
    width: 40%;
}

</style>

# Corda 5.0 Platform Support

This page lists the supported versions of the following:
* [Databases]({{< relref "#databases">}})
* [Container Orchestration]({{< relref "#container-orchestration">}})
* [Messaging]({{< relref "#messaging">}})
* [Security Vault]({{< relref "#security-vault">}})

## Databases

| Database                  | Version |
| ------------------------- | ------- |
| PostgreSQL                | 14.4    |
| Amazon RDS for PostgreSQL | 14.4    |
| Amazon Aurora PostgreSQL  | 14.4    |

## Container Orchestration

| Software                                                                          | Version |
| --------------------------------------------------------------------------------- | ------- |
| Kubernetes                                                                        | 1.25    |
| Amazon Elastic Kubernetes Service (EKS)                                           | 1.25    |
| Azure Kubernetes Service (AKS)                                                    | 1.25    |
| RedHat OpenShift Container Platform (OCP) {{< enterprise-icon noMargin="True" >}} | 4.12.12 |

## Messaging

| Software                                        | Version |
| ----------------------------------------------- | ------- |
| Kafka                                           | 3.2.0   |
| Amazon Managed Streaming for Apache Kafka (MSK) | 3.2.0   |
| Confluent Cloud                                 | 3.2.0   |

## Security Vault {{< enterprise-icon >}}

| Software        | Version |
| --------------- | ------- |
| HashiCorp Vault | 1.13.1  |