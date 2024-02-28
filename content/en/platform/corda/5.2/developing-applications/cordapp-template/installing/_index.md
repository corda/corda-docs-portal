---
date: '2023-06-21'
title: "Installing"
description: Learn how to install the CorDapp template.
menu:
  corda52:
    parent: corda52-develop-get-started
    identifier: corda52-runtime-plugin-installing
    weight: 2000

---

# Installing the CorDapp Template

This section describes how to install the CorDapp template. It contains the following:

* [Downloading](#downloading)
* [Configuring](#configuring)

{{< note >}}
The images in this section show the `cordapp-template-kotlin` repository in IntelliJ. If you are working with the `cordapp-template-java` repository, it looks very similar but the flow code is in a `java` folder and the flow code is saved in more source files. For more information, see [Java Flow Code]({{< relref "../first-flow/code-java.md" >}}).
{{< /note >}}

## Downloading

1. To obtain the {{< version >}} CorDapp template, clone the [cordapp-template-kotlin repository](https://github.com/corda/cordapp-template-kotlin) or [cordapp-template-java repository](https://github.com/corda/cordapp-template-java):

   {{< tabs name="clone">}}
   {{% tab name="Kotlin"%}}
   ```sh
   git clone https://github.com/corda/cordapp-template-kotlin.git <local-folder>
   ```
   {{% /tab %}}

   {{% tab name="Java" %}}
   ```sh
   git clone https://github.com/corda/cordapp-template-java.git <local-folder>
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Checkout the {{< version-num >}} branch:

   ```sh
   git checkout release-V5.2
   ```

3. Initialize the Git repository and change the remote so you do not inadvertently push your work back to the R3 repository:

   ```sh
   git init
   git remote add origin <remote-url>
   ```

   where `<remote-url>` is the URL of the remote repository that you have created.

4. Open the project in IntelliJ and let the import process complete.
   When complete, the project structure looks as follows:

   {{< figure src="CSDE-full-screen.png" figcaption="CSDE project" alt="CSDE project in IntelliJ" >}}

## Configuring

The CorDapp template includes [Gradle tasks]({{< relref "../overview/_index.md#gradle-helpers-for-the-combined-worker" >}}) to manage a local deployment of Corda. This section describes how to configure Gradle for your installation and contains the following:

* [Corda Version](#corda-version)
* [Java Version](#java-version)

### Corda Version

The `gradle.properties` file specifies the Corda version that the Gradle tasks use. Update the version by setting `cordaNotaryPluginsVersion` and `combinedWorkerJarVersion` to the Corda Version. For example, for Corda 5.2:

```shell
cordaNotaryPluginsVersion=5.2.0.0
combinedWorkerJarVersion=5.2.0.0
```

### Java Version

 The Corda runtime Gradle tasks require Java Azul Zulu 17. To configure IntelliJ to use the correct Java version for Gradle:

1. Set **Gradle JVM** to **Project SDK 17**, via **File > Settings > Build, Execution, Deployment > Build Tools > Gradle**.

   {{< figure src="gradle-configuration.png" figcaption="Gradle Java version" alt="JVM version in IntelliJ for CSDE project" >}}

2. Update the Java version in the `build.gradle` file:

   {{< figure src="configure-csde-build-gradle-block.png" figcaption="Configure the CSDE plugin via the build.gradle file" alt="CSDE build gradle block in IntelliJ for CSDE project" >}}

If using IntelliJ IDEA version 2023.1.4 or greater, you should instead set the environmental variable `JAVA_HOME` to point to your installation of Java Azul Zulu 17.
