---
date: '2022-11-11'
title: "Third-Party Prerequisites for Cluster Deployments"
menu:
  corda-5-alpha:
    parent: corda-5-alpha-deploy
    identifier: corda-5-alpha-cluster-prereqs
    weight: 1000
section_menu: corda-5-alpha
---

This section lists the third-party software prerequisites for multi-worker cluster deployments. <!--For information about the prerequisites for local deployment with the [CorDapp Standard Development Environment (CSDE)](../cordapp-standard-development-environment/csde.html), see [Third-Party Prerequisites for the CSDE](../getting-started/prerequisites.html).-->

### Container Orchestration

| Software                                | Version           |
|-----------------------------------------|-------------------|
| Kubernetes                              | 1.23              |
| Amazon Elastic Kubernetes Service (EKS) | 1.23              |
| Helm                                    | 3.9.4 or newer    |

### Messaging

| Software                                        | Version |
|-------------------------------------------------|---------|
| Kafka                                           | 3.2.0   |
| Amazon Managed Streaming for Apache Kafka (MSK) | 3.2.0   |
| Confluent Cloud                                 |         |

### Database

| Software                  | Version |
|---------------------------|---------|
| PostgreSQL                | 14.4    |
| Amazon RDS for PostgreSQL | 14.4    |
| Amazon Aurora PostgreSQL  | 14.4    |

<!--## Minimum Resource Requirements

Corda 5 cluster deployments have the following minimum requirements:

| Software   | Requirements |
|------------|--------------|
| Kubernetes |              |
| Kafka      |              |
| PostgreSQL |              |
-->
