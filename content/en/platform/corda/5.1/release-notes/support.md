---
title: "Platform Support"
date: 2023-08-17
version: 'Corda 5.0'
menu:
  corda51:
    parent: corda51-release-notes
    identifier: corda51-release-notes-support
    weight: 900
section_menu: corda51
---

<style>
table th:first-of-type {
    width: 60%;
}
table th:nth-of-type(2) {
    width: 40%;
}

</style>

# {{< version >}} Platform Support

This page lists the versions of [third-party software](#third-party-support) that {{< version >}} supports. It also outlines the [end of life strategy](#end-of-life-strategy).

## Third-Party Support

This section lists the supported versions of the following:
* [Databases]({{< relref "#databases">}})
* [Container Orchestration]({{< relref "#container-orchestration">}})
* [Messaging]({{< relref "#messaging">}})
* [Security Vault]({{< relref "#security-vault">}})

### Databases

| Database                  | Version |
| ------------------------- | ------- |
| PostgreSQL                | 14.4    |
| Amazon RDS for PostgreSQL | 14.4    |
| Amazon Aurora PostgreSQL  | 14.4    |
| Microsoft Azure for PostgreSQL  | 14.4    |

### Container Orchestration

| Software                                                                          | Version |
| --------------------------------------------------------------------------------- | ------- |
| Kubernetes                                                                        | 1.25    |
| Amazon Elastic Kubernetes Service (EKS)                                           | 1.25    |
| Azure Kubernetes Service (AKS)                                                    | 1.25    |
| RedHat OpenShift Container Platform (OCP) {{< enterprise-icon noMargin="True" >}} | 4.12.12 |

### Messaging

| Software                                        | Version |
| ----------------------------------------------- | ------- |
| Kafka                                           | 3.2.0   |
| Amazon Managed Streaming for Apache Kafka (MSK) | 3.2.0   |
| Confluent Cloud                                 | 3.2.0   |

### Security Vault {{< enterprise-icon >}}

| Software        | Version |
| --------------- | ------- |
| HashiCorp Vault | 1.13.1  |


## End of Life Strategy
Use the following table to track the end of life schedule for each version of Corda. Each version of Corda has R3 support available for a fixed period. 
After this period has ended, these versions are no longer supported by R3, and any associated documentation is archived. You should always aim to upgrade to the latest version of Corda whenever possible.

Definitions:

* **End of maintenance**: This release will no longer receive functional patches after the date shown.
* **End of security**: This release will no longer be eligible for security patches after the date shown.
* **End of support**: Support (including documentation) provided by R3 is no longer available after this date.

{{< note >}}
All dates refer to the end of the month indicated.
{{< /note >}}

{{< snippet "end-of-life-corda5.md" >}}