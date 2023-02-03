---
aliases:
- /docs/corda-enterprise/head/cordapps/getting-set-up.html
- /docs/corda-enterprise/cordapps/getting-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-cordapps
tags:
- getting
- set
title: Getting set up for CorDapp development
weight: 2

---

# Getting set up for CorDapp development

There are four pieces of required software for CorDapp development: the Java 8 JDK, IntelliJ IDEA, Git, and Gradle.

## Installing the Java 8 JDK

Install the Java 8 JDK. Corda requires at least version 8u171, but do not currently support Java 9 or higher for this version of Corda.

Corda has been tested against the following Java builds:

  * [Oracle JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
  * [Amazon Corretto](https://aws.amazon.com/corretto/)
  * [Red Hat’s OpenJDK](https://developers.redhat.com/products/openjdk/overview/)
  * [Zulu’s OpenJDK](https://www.azul.com/)

{{< note >}}
  OpenJDK builds often exclude JavaFX, which is required by the Corda GUI tools. Corda supports only Java 8.
  {{< /note >}}

If you are using Windows, you must also add Java to the PATH environment variable by following the instructions in the [Oracle documentation](https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path).

## Installing the IntelliJ IDEA

IntelliJ is an IDE that offers strong support for Kotlin and Java development.

Install the [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/). Corda supports IntelliJ IDEA versions **2017.x**, **2018.x**, **2019.x**, and **2020.x**; and Kotlin plugin version 1.2.71.


To install IntelliJ IDEA in a Ubuntu environment, navigate to the [Jetbrains IntelliJ snap package](https://snapcraft.io/intellij-idea-community).

## Installing Git

We use Git to host our sample CorDapp and provide version control.

To install Git, navigate to [Git](https://git-scm.com/) and install your preferred version, depending on your OS.

## Installing Gradle

If you intend to proceed directly to run a sample CorDapp, as described in [Running a sample CorDapp](tutorial-cordapp.md), the included `gradlew` script should install Gradle automatically when you open the sample CorDapp in IntelliJ.

If you'd prefer to install Gradle manually, navigate to [Gradle](https://gradle.org/releases/) then locate and install Gradle **version 5.6.4**. Corda requires a Gradle version between 5.1 and 5.6.4, and does not support Gradle 6.x.

 ## Run a sample CorDapp *(optional)*

We recommend [running a sample CorDapp](tutorial-cordapp.md) to see Corda in action before you start developing.

## Resources

* [Sample CorDapps, templates, and community projects](https://www.corda.net/samples/).
* [Corda API documentation](../../../../../../en/api-ref.html).
* [Flow cookbook](flow-cookbook.md).
* CorDapp [Java](https://github.com/corda/samples-java) and [Kotlin](https://github.com/corda/samples-kotlin) sample repositories - contain multiple sample CorDapps, from those to get you started, to those which demonstrate specific features and advanced usage.
* CorDapp [Java](https://github.com/corda/cordapp-template-java) and [Kotlin](https://github.com/corda/cordapp-template-kotlin) templates - a stubbed-out CorDapp that you can use to bootstrap your own CorDapps.

For more developer resources, open-source projects, and CorDapp templates, check out R3's [Developer Portal](https://developer.r3.com/corda/).