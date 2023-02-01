---
date: '2022-09-19'
title: "CorDapp Standard Development Environment (CSDE)"
menu:
  corda-5-beta:
    parent: corda-5-beta-start
    identifier: corda-5-beta-csde
    weight: 2000
section_menu: corda-5-beta
---
{{< note >}}
The CSDE is experimental. The decision whether or not we release it as part of Corda 5.0 will, in part, be based on your [feedback](https://community.r3.com/c/corda-5-developer-preview/41).
{{< /note >}}

The CorDapp Standard Development Environment (CSDE) makes the process of prototyping CorDapps on Beta 1.1 more straight-forward.
The CSDE is obtained by cloning our `CSDE-cordapp-template-kotlin` or `CSDE-cordapp-template-java` repository to your local machine. The CSDE provides:
* a prepared CorDapp project that you can use as a starting point to develop your own prototypes.
* a base Gradle configuration that brings in the dependencies you need to write and test a Corda 5 CorDapp.
* a set of Gradle helper tasks which speed up and simplify the development and deployment process; these are effectively wrappers over the [Corda CLI](../installing-corda-cli.html).
* debug configuration for debugging a local Corda cluster.
* the `MyFirstFlow` code which forms the basis of the Getting Started documentation.
* the `utxoexample` Chat Cordapp, which provides a basic, working utxo Ledger Cordapp.
* the ability to configure the members of the local Corda network.

{{< note >}}
The images in this section show the `CSDE-cordapp-template-kotlin` repository in IntelliJ. If you are working with the `CSDE-cordapp-template-java` repository, it looks very similar but the flow code and flow tests are in a `java` folder and the flow code is saved in more source files. For more information, see [Java Flow Code](../first-flow/code-java.html).
{{< /note >}}

## Downloading the CSDE

1. To obtain the CSDE template, clone the [CSDE-cordapp-template-kotlin repository](https://github.com/corda/CSDE-cordapp-template-kotlin) or [CSDE-cordapp-template-java repository](https://github.com/corda/CSDE-cordapp-template-java):

   {{< tabs name="clone-csde">}}
   {{% tab name="Kotlin"%}}
   ```sh
   git clone https://github.com/corda/CSDE-cordapp-template-kotlin.git <local-folder>
   ```
   {{% /tab %}}

   {{% tab name="Java" %}}
   ```sh
   git clone https://github.com/corda/CSDE-cordapp-template-java.git <local-folder>
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Change to the new directory and checkout the Beta 1 branch:

   ```sh
   git checkout release/corda-5-beta-1
   ```

3. Initialise the git repo and change the remote so you do not inadvertently push your work back to our R3 repo.

3. Open the project in IntelliJ and let the import process complete.
  When complete, the project structure looks as follows:

  {{< figure src="CDSE-full-screen-kotlin.png" figcaption="CSDE project" alt="CSDE project in IntelliJ" >}}


## Configuring the CSDE

The CSDE includes [Gradle tasks](#gradle-helpers-for-the-combined-worker) to manage a local deployment of Corda. These Gradle tasks require Java Azul Zulu 11. To configure IntelliJ to use the correct Java version for Gradle, set **Gradle JVM** to `Project SDK 11`, as follows:

{{< figure src="gradle-configuration.png" figcaption="Gradle Java version" alt="JVM version in IntelliJ for CSDE project" >}}

## CSDE Overview

This section provides an overview of the content of CSDE. Other sections show you how to use it in the process of writing a CorDapp.

### Project Structure

On the left, you can see the folder structure created, ready for CorDapps development.
{{< figure src="project-structure.png" figcaption="CSDE folder structure" alt="CSDE folders in IntelliJ" >}}

For Kotlin, write your flow code in `workflows/src/main/kotlin/<your package path>` and your contract and states code in `/contracts/src/main/kotlin<your package path>`.

For Java, use `workflows/src/main/java/<your package path>` and your contract and states code in `/contracts/src/main/kotlin<your package path>`.

For test code, use the corresponding test folder.

{{< note >}}
The Simulator has not yet been updated for `UTXOLedgerService` and so the flow tests you can run are currently limited. There is also currently no unit testing framework for contract code.
As an approximation, the Kotlin template contains `ContractTestFlow`, which, when run as a normal flow from swagger, tests the `utxoexample` contract.
{{< /note >}}



### Gradle Helpers for the Combined Worker

On the right, you can see the Gradle tasks that we have included to help you work with a local deployment of Corda using the combined worker:
{{< figure src="gradle-helpers.png" figcaption="CSDE gradle helpers" alt="CSDE gradle tasks in IntelliJ" >}}
The **combined worker** is a Corda cluster that runs all of the workers in one JVM process.


The helpers are split into three folders:
* [csde-corda](#csde-corda)
* [csde-cordapp](#csde-cordapp)
* [csde-queries](#csde-queries)
#### csde-corda

These tasks help with the lifecycle of your local Corda cluster.

`startCorda` which:
1. Downloads and locally stores a copy of the combined worker JAR, if required
2. Starts an instance of a Postgres Docker container; you will need Docker Engine or Docker Desktop running
3. Starts the combined worker

Note, corda takes around a minute to start up, however at present the gradle tasks shows as complete before the start up has finished. It is best to poll the cluster with one of the csde-query helpers until it responds, this will tell you the cluster is live and ready to interact.

`stopCorda` which:

#### `startCorda`
1. Stops the Postgres database
2. Stops the combined worker

#### csde-cordapp

These tasks help with the compilation and deployment of your Cordapp.

`1-createGroupPolicy` creates the Group policy which is required to set up the Application Network.

`2-createKeyStore` creates the signing keys for publishing the CPIs.

`3-buildCPIs` builds your Cordapp and wraps it in a signed CPI.

`4-deployCPIs` deploys the CPI to your local corda cluster.

`5-createAndRegisterVNodes` sets up the Virtual Nodes specified in `config/dev-net.json` on you local corda with the uploaded CPI

Each of these tasks has a dependency on the previous, so if you run 3, it will also run 1 and 2.

`quickDeployCordapp` is just an alias for `5-createAndRegisterVNodes`, you should click this to do your first deployment of your Cordapp to a newly started cluster.

{{< note >}}
You only need to run `quickDeployCordapp` the first time you upload your CPI to the corda cluster. On subsequent builds you can just click `4-deployCPIs`. This will reduce your turnaround time for deploying your code from 1-2 mins to around 20-30 seconds.
{{< /note >}}

#### csde-queries

These are standard queries which you will find useful to run against your Corda cluster.

`listVNodes` queries the Corda CLuster and returns the list of VNodes, this includes the ShortHash which you will need for running flows.

`listCPIs` queries the Corda CLuster and returns the list of CPIs uploaded.



### Debug Configuration
In the toolbar, you can select the `DebugCorDapp` run configuration to debug the running Corda from IntelliJ.

{{< figure src="debugging.png" figcaption="CSDE DebugCorDapp" alt="Menu in IntelliJ to debug Corda" >}}
