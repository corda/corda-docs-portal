---
date: '2023-08-10'
title: "Installing the CSDE"
version: 'Corda 5.1'
menu:
  corda51:
    parent: corda51-develop-get-started
    identifier: corda51-csde-installing
    weight: 2000
section_menu: corda51
---
# Installing the CSDE
* [Downloading the CSDE](#downloading-the-csde)
* [Configuring the CSDE](#configuring-the-csde)

{{< note >}}
The images in this section show the `CSDE-cordapp-template-kotlin` repository in IntelliJ. If you are working with the `CSDE-cordapp-template-java` repository, it looks very similar but the flow code is in a `java` folder and the flow code is saved in more source files. For more information, see [Java Flow Code]({{< relref "../first-flow/code-java.md" >}}).
{{< /note >}}

## Downloading the CSDE

1. To obtain the CSDE template, clone the [CSDE-cordapp-template-kotlin repository](https://github.com/corda/CSDE-cordapp-template-kotlin/tree/release/corda-5-0) or [CSDE-cordapp-template-java repository](https://github.com/corda/CSDE-cordapp-template-java/tree/release/corda-5-0):

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

2. Change to the new folder and checkout the 5.0 branch:

   ```sh
   git checkout release/corda-5-0
   ```

3. Initialise the Git repository and change the remote so you do not inadvertently push your work back to the R3 repository:

   ```sh
   git init
   git remote add origin <remote-url>
   ```

   where `<remote-url>` is the URL of the remote repository that you have created.

3. Open the project in IntelliJ and let the import process complete.
   When complete, the project structure looks as follows:

   {{< figure src="CSDE-full-screen.png" figcaption="CSDE project" alt="CSDE project in IntelliJ" >}}


## Configuring the CSDE

The CSDE includes [Gradle tasks](#gradle-helpers-for-the-combined-worker) to manage a local deployment of Corda. These Gradle tasks require Java Azul Zulu 11. To configure IntelliJ to use the correct Java version for Gradle, set **Gradle JVM** to **Project SDK 11**, as follows:

{{< figure src="gradle-configuration.png" figcaption="Gradle Java version" alt="JVM version in IntelliJ for CSDE project" >}}

{{< figure src="configure-CSDE-build-gradle-block.png" figcaption="Configure the CSDE plugin via the build.gradle file" alt="CSDE build gradle block in IntelliJ for CSDE project" >}}

If using IntelliJ IDEA version 2023.1.4 or greater, then you should instead set the environmental variable `JAVA_HOME` to point to your installation of Java Azul Zulu 11.