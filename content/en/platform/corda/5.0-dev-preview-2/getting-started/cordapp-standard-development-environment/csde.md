---
date: '2022-09-19'
title: "Cordapp Standard Development Environment (CSDE)"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-csde
    weight: 2000
section_menu: corda-5-dev-preview
---
To make the process of prototyping CorDapps on Developer Preview 2 more straight-forward, we have developed the CorDapp Standard Development Environment (CSDE).
The CSDE is obtained by cloning our `CSDE-Cordapp-Template-Kotlin` repository to your local machine. The CSDE provides:
* A prepared CorDapp project that you can use as a starting point to develop your own prototypes.
* A base Gradle configuration that brings in the dependencies you need to write and test a Corda 5 CorDapp.
* A set of Gradle helper tasks which speed up and simplify the development and deployment process. These are effectively wrappers over the [Corda CLI](../../developing/corda-cli/overview.html).
* Debug configuration for debugging a local Corda cluster.
* The `MyFirstFlow` code which forms the basis of the Getting Started documentation.
* The ability to configure the members of the local Corda network.
{{< note >}}
The CSDE is experimental. The decision whether or not we release it as part of Corda 5.0, will in part be based on your feedback.  
{{< /note >}}

## Downloading the CSDE template

1. To obtain the CSDE template, clone the [`CSDE-Cordapp-Template-Kotlin` repository](https://github.com/corda/CSDE-cordapp-template-kotlin):

  ```sh
  # git clone https://github.com/corda/CSDE-cordapp-template-kotlin.git <name of the folder to put it in>
  ```

2. Change to the new directory and checkout *<insert final tag>*:

  ```sh
  # git checkout xxx
  ```

  You should initialise the git repo and change the remote so you do not inadvertently push your work back to our R3 repo.

3. Open the project in IntelliJ and let the import process complete.
  When complete, the project structure looks as follows:
{{< figure src="CDSE-full-screen.png" figcaption="CSDE project" alt="CSDE project in IntelliJ" >}}

## CSDE overview

This section provides an overview of the content of CSDE. Other sections show you how to use it in the process of writing a CorDapp.

### Project Structure
On the left, you can see the folder structure created, ready for CorDapps development.
{{< figure src="project-structure.png" figcaption="CSDE folder structure" alt="CSDE folders in IntelliJ" >}}

You will write your flow code in `src/main/kotlin/<your package path>` and your flow tests in `src/main/kotlin/<your package path>`.
(For Java, it will be `src/main/java/<your package path>` and `src/test/java/<your package path>` respectively.)

### Gradle helpers for the Combined Worker
On the right, you can see the Gradle tasks that we have included to help you work with a local deployment of Corda using the combined worker:
{{< figure src="gradle-helpers.png" figcaption="CSDE gradle helpers" alt="CSDE gradle tasks in IntelliJ" >}}
The **combined worker** is a Corda cluster that runs all of the workers in one JVM process.

#### `startCorda`

The `startCorda` task does the following:

1. Downloads and locally stores a copy of the Combined Worker JAR, if required.
2. Starts an instance of a Postgres Docker container. You will need Docker Engine or Docker Desktop running.
3. Starts the combined worker.

#### `stopCorda`

The `stopCorda` task does the following:

* Stops the Postgres database.
* Stops the combined worker.

#### `deployCorDapp`

The `deployCorDapp` task does the following to compile and deploy the CorDapp to the combined worker:

1. Compiles the [CPB](../../../introduction/key-concepts.html#corda-package-bundles-cpbs) and [CPI](../../../introduction/key-concepts.html#corda-package-installer-cpi).
2. Uploads the CPI to the combined worker.
3. Generates the [virtual nodes](../../../introduction/key-concepts.html#virtual-nodes) with the CPI.

### Debug Configuration
In the toolbar, you can select the `DebugCorDapp` run configuration, which allows you to debug the running Corda from IntelliJ.
{{< figure src="debugging.png" figcaption="CSDE DebugCorDapp" alt="Menu in IntelliJ to debug Corda" >}}
