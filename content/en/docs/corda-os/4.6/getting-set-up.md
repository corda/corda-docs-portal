---
aliases:
- /head/getting-set-up.html
- /HEAD/getting-set-up.html
- /getting-set-up.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-getting-set-up
    parent: corda-os-4-6-building-a-cordapp-index
    weight: 1020
tags:
- getting
- set
title: Getting set up for CorDapp development
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

## Next steps

First, run the [sample CorDapp](tutorial-cordapp.md).

Next, read through the [Corda Key Concepts](key-concepts.md) to understand how Corda works.

By then, you’ll be ready to start writing your own CorDapps. You may want to refer to the
API documentation, the [flow cookbook](flow-cookbook.md) and the
[samples](https://www.corda.net/samples/) along the way.

If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via [our Slack channels](http://slack.corda.net/).
