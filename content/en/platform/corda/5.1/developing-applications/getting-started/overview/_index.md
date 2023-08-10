---
date: '2023-08-10'
title: "CSDE Overview"
version: 'Corda 5.1'
menu:
  corda51:
    parent: corda51-develop-get-started
    identifier: corda51-csde-overview
    weight: 2050
section_menu: corda51
---
# CSDE Overview

This section provides an overview of the content of CSDE. Other sections show you how to use it in the process of writing a {{< tooltip >}}CorDapp{{< /tooltip >}}.

## Project Structure

On the left, you can see the folder structure created, ready for CorDapps development.
 {{< figure src="project-structure.png" figcaption="CSDE folder structure" alt="CSDE folders in IntelliJ" >}}

For Kotlin, write your {{< tooltip >}}flow{{< /tooltip >}} code in `workflows/src/main/kotlin/<your package path>` and your contract and {{< tooltip >}}states{{< /tooltip >}} code in `/contracts/src/main/kotlin/<your package path>`.

For Java, use `workflows/src/main/java/<your package path>` and your contract and states code in `/contracts/src/main/java/<your package path>`.

For test code, use the corresponding test folder.
## Gradle Helpers for the Combined Worker

On the right, you can see the Gradle tasks that we have included to help you work with a local deployment of Corda using the combined worker:
{{< figure src="gradle-helpers.png" figcaption="CSDE gradle helpers" alt="CSDE gradle tasks in IntelliJ" width=100% length=100% >}}
The **combined worker** is a Corda cluster that runs all of the workers in one JVM process.

The helpers are split into three folders:
* [csde-corda](#csde-corda)
* [csde-cordapp](#csde-cordapp)
* [csde-queries](#csde-queries)

### csde-corda

These tasks help with the lifecycle of your local Corda cluster.

| <div style="width:220px">Helper   </div> | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `startCorda`                             | 1. Downloads a copy of the combined worker JAR, if required. <br> 2. Starts an instance of a Postgres Docker container. You will need Docker Engine or Docker Desktop running.<br> 3. Starts the combined worker. The Combined Worker will continue to run in a 'Run' Console until it is shut down. <br> Note, Corda takes about one minute to start up. It is best to poll the cluster with one of the `csde-query` helpers until it responds to confirm if the cluster is live and ready to interact. |
| `stopCorda`                              | 1. Stops the Postgres database. <br> 2. Stops the combined worker.        |

### csde-cordapp

| <div style="width:220px">Helper</div> | Description                                                                                                                                                                             |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `1-createGroupPolicy`                 | Creates the {{< tooltip >}}group policy{{< /tooltip >}} which is required to set up the {{< tooltip >}}application network{{< /tooltip >}}.                                                                                                           |
| `2-createKeyStore`                    | Creates the signing keys for publishing the {{< tooltip >}}CPIs{{< /tooltip >}}.                                                                                                                                       |
| `3-buildCPIs`                         | Builds your CorDapp and wraps it in a signed CPI.                                                                                                                                       |
| `4-deployCPIs`                        | Deploys the CPI to your local Corda cluster. If the CPI has already been deployed to the nodes on the cluster, this task performs a forced upload and replaces the old CPI with the new one. |
| `5-vNodeSetup`                        | Sets up the virtual nodes specified in `config/static-network-config.json` on you local Corda cluster with the uploaded CPI.                                                            |

Each of these tasks has a dependency on the previous. So, if you run 3, it also runs 1 and 2.

{{< note >}}
You only need to run `5-vNodeSetup` the first time you upload your CPI to the corda cluster. On subsequent builds, you can just run `4-deployCPIs`. (`5-vNodeSetup` has no effect if the virtual nodes have already been set up. It will not try to recreate them.)
{{< /note >}}

### csde-queries

These are standard queries that are useful to run against your Corda cluster.

| <div style="width:220px">Helper</div> | Description                                                                                                               |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `listVNodes`                          | Queries the Corda cluster and returns the list of vnodes. This includes the `ShortHash` that you  need for running flows. |
| `listCPIs`                          | Queries the Corda cluster and returns the list of CPIs uploaded. |

## Debug Configuration
In the toolbar, you can select the `DebugCorDapp` run configuration to debug the running Corda from IntelliJ.

{{< figure src="debugging.png" figcaption="CSDE DebugCorDapp" alt="Menu in IntelliJ to debug Corda" >}}
