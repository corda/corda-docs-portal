---
description: "Review the tools required by Cluster Administrators."
date: '2023-05-10'
title: "Cluster Administrator Tooling"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-cluster-tooling
    parent: corda51-cluster
    weight: 2000
section_menu: corda51
---
<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}

</style>
# Cluster Administrator Tooling

This section outlines the tools needed by a Cluster Administrator to deploy and operate Corda.
There are additional tools which may be required depending on the installation approach taken.

| Tool                                            | Description                                                                                                                                                                                                                                                                                                |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| {{< tooltip >}}Kubernetes{{< /tooltip >}} CLI | Corda 5 is deployed to Kubernetes and to interact with the cluster, the Cluster Administrator requires the Kubernetes client kubectl. The [Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/#kubectl) contains details on how to install kubectl. You should use a version of the CLI that is within one minor version of the Kubernetes cluster that you are using, for example, if your cluster is v1.23, your CLI should be v1.22, v1.23, or v1.24.       |
| {{< tooltip >}}Helm{{< /tooltip >}} CLI       | Corda 5 is deployed as a Helm chart. To perform the installation, the Cluster Administrator requires the Helm CLI. The [Helm documentation](https://helm.sh/docs/intro/install/) contains details on how to install Helm. The Helm version should be v3.9.4 or newer.                                 |
| {{< tooltip >}}Corda CLI{{< /tooltip >}}      | The Cluster Administrator requires the Corda CLI if they intend to [manually bootstrap]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md" >}}) Kafka and PostgreSQL. See the documentation on [installing the Corda CLI]({{< relref "../tooling/installing-corda-cli.md" >}}). |
| curl           | Examples in this documentation for Linux and macOS use the curl CLI to interact with HTTP endpoints. See the [curl documentation](https://everything.curl.dev/get) for details on how to install curl. Alternatives may be used if desired. On Windows, PowerShell contains native support for HTTP calls.         |
| jq             | Examples in this documentation for Linux and macOS use the jq CLI to parse content out of JSON responses received from the Corda REST API. See the [jq documentation](https://stedolan.github.io/jq/download/) for details on how to install jq. Alternatives may be used if desired. On Windows, PowerShell contains native support for parsing JSON.                       |
| PostgreSQL Client   | The Cluster Administrator, or their database administrator, requires a PostgreSQL client if they intend to [manually bootstrap]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md" >}}) PostgreSQL. Examples in this documentation use the psql CLI. See the [Postgres documentation](https://www.postgresql.org/download/) for details on how to download Postgres. Alternatives may be used if desired.      |
| {{< tooltip >}}Kafka{{< /tooltip >}} Client        | The Cluster Administrator, or their Kafka administrator, may require a Kafka client if they intend to [manually bootstrap]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md" >}}) Kafka. Examples in this documentation use the scripts packaged with Kafka. See the [Kafka documentation](https://kafka.apache.org/downloads) for details on how to download Kafka. Alternatives may be used if desired. |
