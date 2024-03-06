---
date: '2023-06-21'
title: "Overview"
description: Learn about the contents of the CorDapp template.
menu:
  corda52:
    parent: corda52-develop-get-started
    identifier: corda52-runtime-plugin-overview
    weight: 2050

---
# CorDapp Template Overview

This section provides an overview of the content of the CorDapp template. It contains the following:

* [Project Structure](#project-structure)
* [Gradle Helpers for the Combined Worker](#gradle-helpers-for-the-combined-worker)
* [Debug Configuration](#debug-configuration)

## Project Structure

On the left, you can see the folder structure created, ready for CorDapps development.
 {{< figure src="project-structure.png" figcaption="CorDapp template folder structure" alt="CorDapp template folders in IntelliJ" >}}

For Kotlin, write your {{< tooltip >}}flow{{< /tooltip >}} code in `workflows/src/main/kotlin/<your package path>` and your contract and {{< tooltip >}}states{{< /tooltip >}} code in `/contracts/src/main/kotlin/<your package path>`.

For Java, use `workflows/src/main/java/<your package path>` for your flows and `/contracts/src/main/java/<your package path>` for your contract and states code.

For test code, use the corresponding test folder.

## Gradle Helpers for the Combined Worker

On the right, you can see the Gradle tasks that help you work with a local deployment of Corda using the combined worker. The **combined worker** is a Corda cluster that runs all of the workers in one JVM process for development purposes.
{{< figure src="gradle-helpers.png" figcaption="Corda Runtime gradle helpers" alt="Corda Runtime gradle tasks in IntelliJ" width=100% length=100% >}}

The Gradle helpers are grouped into five folders:

* [corda-runtime-plugin-local-environment](#corda-runtime-plugin-local-environment)
* [corda-runtime-plugin-cordapp](#corda-runtime-plugin-cordapp)
* [corda-runtime-plugin-network](#corda-runtime-plugin-network)
* [corda-runtime-plugin-queries](#corda-runtime-plugin-queries)
* [corda-runtime-plugin-supporting](#corda-runtime-plugin-supporting)

<style>
table th:first-of-type {
    width: 25%;
}
table th:nth-of-type(2) {
    width: 75%;
}
</style>

### corda-runtime-plugin-local-environment

The `corda-runtime-plugin-local-environment` tasks help with the lifecycle of your local Corda cluster:

| Helper                       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `startCorda`                 | Starts an instance of the Corda cluster using Docker Compose, with the combined worker container on the network with the necessary prerequisites (Kafka and Postgres). This requires Docker Engine or Docker Desktop running.<br> The Docker Compose process will continue to run in a 'Run' console, providing output from all of the containers, until it is shut down. <br> Note, Corda takes about one minute to start up. You should poll the cluster with one of the `corda-runtime-plugin-queries` helpers until it responds to confirm if the cluster is live and ready to interact. |
| `stopCorda`                  | Stops the Corda cluster using Docker Compose and deletes all containers and networks used by the cluster.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `stopCordaAndCleanWorkspace` | 1. Stops the Corda cluster using Docker Compose and deletes all containers and networks used by the cluster (same as the `stopCorda` task). <br> 2. Recursively deletes workspace directory, to reset any pending state.                                                                                                                                                                                                                                                                                                                                                                     |

### corda-runtime-plugin-cordapp

The `corda-runtime-plugin-cordapp` tasks help to create and deploy CPIs:

| Helper              | Description                                                                                                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `createGroupPolicy` | Creates the {{< tooltip >}}group policy{{< /tooltip >}} which is required to set up the {{< tooltip >}}application network{{< /tooltip >}}.                                                  |
| `createKeyStore`    | Creates the signing keys for publishing the {{< tooltip >}}CPIs{{< /tooltip >}}.                                                                                                             |
| `buildCPIs`         | Builds your CorDapp and wraps it in a signed CPI.                                                                                                                                            |
| `deployCPIs`        | Deploys the CPI to your local Corda cluster. If the CPI has already been deployed to the nodes on the cluster, this task performs a forced upload and replaces the old CPI with the new one. |

Some tasks have a dependency on the others. So, for example, if you run `deployCPIs`, it also runs `createGroupPolicy`, `createKeyStore` and `buildCPIs`.

### corda-runtime-plugin-network

The `corda-runtime-plugin-network` tasks set up your virtual nodes:

| Helper        | Description                                                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `vNodesSetup` | Sets up the virtual nodes specified in `config/static-network-config.json` on you local Corda cluster with the uploaded CPI. |

Some tasks have a dependency on the others. So, for example, if you run `vNodesSetup`, it also runs `deployCPIs`.

{{< note >}}
You only need to run `vNodesSetup` the first time you upload your CPI to the Corda cluster. On subsequent builds, you can just run `deployCPIs`. (`vNodeSetup` has no effect if the virtual nodes have already been set up. It will not try to recreate them.)
{{< /note >}}

### corda-runtime-plugin-queries

The `corda-runtime-plugin-queries` tasks are standard queries that are useful to run against your Corda cluster:

| Helper       | Description                                                                                                                      |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `listVNodes` | Queries the Corda cluster and returns the list of virtual nodes. This includes the `ShortHash` that you  need for running flows. |
| `listCPIs`   | Queries the Corda cluster and returns the list of CPIs uploaded.                                                                 |

### corda-runtime-plugin-supporting

The `corda-runtime-plugin-supporting` tasks are  are supporting Gradle tasks, used internally by other tasks:

| Helper                   | Description                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `getNotaryServerCPB`     | Downloads the Notary Server CPB.                                                            |
| `projInit`               | Creates the workspace directory.                                                            |
| `updateProcessorTimeout` | Updates the processor timeout in the `corda.messaging` config section of the Corda cluster. |

## Debug Configuration

In the toolbar, you can select the `DebugCorDapp` run configuration to debug the running Corda instance from IntelliJ.

{{< figure src="debugging.png" figcaption="CorDapp template DebugCorDapp" width="40%" alt="Menu in IntelliJ to debug Corda" >}}
