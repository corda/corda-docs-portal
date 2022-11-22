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

The CorDapp Standard Development Environment (CSDE) makes the process of prototyping CorDapps on Developer Preview 2 more straight-forward.
The CSDE is obtained by cloning our `CSDE-cordapp-template-kotlin` or `CSDE-cordapp-template-java` repository to your local machine. The CSDE provides:
* a prepared CorDapp project that you can use as a starting point to develop your own prototypes.
* a base Gradle configuration that brings in the dependencies you need to write and test a Corda 5 CorDapp.
* a set of Gradle helper tasks which speed up and simplify the development and deployment process; these are effectively wrappers over the [Corda CLI](../../developing/corda-cli/overview.html).
* debug configuration for debugging a local Corda cluster.
* the `MyFirstFlow` code which forms the basis of the Getting Started documentation.
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

2. Change to the new directory and checkout the Developer Preview 2 branch:

   ```sh
   git checkout release/corda-5-developer-preview-2
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

For Kotlin, write your flow code in `src/main/kotlin/<your package path>` and your flow tests in `src/test/kotlin/<your package path>`.
For Java, use `src/main/java/<your package path>` and `src/test/java/<your package path>` respectively.

### Gradle Helpers for the Combined Worker

On the right, you can see the Gradle tasks that we have included to help you work with a local deployment of Corda using the combined worker:
{{< figure src="gradle-helpers.png" figcaption="CSDE gradle helpers" alt="CSDE gradle tasks in IntelliJ" >}}
The **combined worker** is a Corda cluster that runs all of the workers in one JVM process.

#### `startCorda`

The `startCorda` task does the following:

1. Downloads and locally stores a copy of the combined worker JAR, if required
2. Starts an instance of a Postgres Docker container; you will need Docker Engine or Docker Desktop running
3. Starts the combined worker

#### `stopCorda`

The `stopCorda` task does the following:

* Stops the Postgres database
* Stops the combined worker

#### `deployCorDapp`

The `deployCorDapp` task does the following to compile and deploy the CorDapp to the combined worker:

1. Compiles the [CPB](../../introduction/key-concepts.html#corda-package-bundles-cpbs) and [CPI](../../introduction/key-concepts.html#corda-package-installer-cpi) using the [buildCPI](#buildCPI-task) task
2. Uploads the CPI to the combined worker
3. Generates the [virtual nodes](../../introduction/key-concepts.html#virtual-nodes) with the CPI

#### `buildCPI`

The `buildCPI` task compiles your CorDapp into a CPI file.

#### `listVNodes`

The `listVNodes` task displays a list of the virtual nodes on the local Corda cluster.

### Debug Configuration
In the toolbar, you can select the `DebugCorDapp` run configuration to debug the running Corda from IntelliJ.

{{< figure src="debugging.png" figcaption="CSDE DebugCorDapp" alt="Menu in IntelliJ to debug Corda" >}}
