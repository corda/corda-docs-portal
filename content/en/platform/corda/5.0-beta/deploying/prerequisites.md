---
date: '2022-23-11'
title: "Prerequisites for Cluster Deployments"
menu:
  corda-5-beta:
    parent: corda-5-beta-deploy
    identifier: corda-5-beta-cluster-prereqs
    weight: 1000
section_menu: corda-5-beta
---

This section lists the software prerequisites for multi-worker cluster deployments.
The prerequisites for both the target environment and the environment from which you are deploying are listed.
For information about the prerequisites for local deployment with the [CorDapp Standard Development Environment (CSDE)](../cordapp-standard-development-environment/csde.html), see [Prerequisites for the CSDE](..developing/getting-started/prerequisites.html).

## Local Environment

| Software | Version        |
|----------|----------------|
| [Corda CLI](..developing/getting-started/installing-corda-cli.html)  |   |  
| kubectl  | 1.23           |
| Helm     | 3.9.4 or newer |
| Docker   |                |

Corda deployments have been tested with Windows 11 and macOS Monterey version 12.6.1.

## Target Environment

### Container Orchestration

| Software                                | Version |
|-----------------------------------------|---------|
| Kubernetes                              | 1.23    |
| Amazon Elastic Kubernetes Service (EKS) | 1.23    |
| Red Hat OpenShift Container Platform    | 4.10    |

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
