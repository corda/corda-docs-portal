---
aliases:
- /head/getting-set-up.html
- /HEAD/getting-set-up.html
- /getting-set-up.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-12:
    identifier: corda-community-4-12-getting-set-up
    parent: corda-community-4-12-building-a-cordapp-index
    weight: 1020
tags:
- getting
- set
title: Getting set up for CorDapp development
---


# Getting set up for CorDapp development

There are four pieces of required software for CorDapp development:
* Java 17 JDK
* IntelliJ IDEA
* Git
* Gradle

{{< note >}} Visit the [platform support matrix]({{< relref "release-platform-support-matrix.md" >}}) to check the latest third-party application versions supported by Corda. {{< /note >}}

## Installing the Java 17 JDK

Install the Java 17 JDK. 

Corda 4.12 has been tested against the following Java builds:

  * [Oracle JDK 17.0.9](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
  * [Zulu’s OpenJDK 17.46.19 (17.0.9+8)](https://www.azul.com/downloads/?version=java-17-lts&show-old-builds=true#zulu)

{{< note >}}
OpenJDK builds often exclude JavaFX, which is required by the Corda GUI tools.
{{< /note >}}

If you are using Windows, you must also add Java to the PATH environment variable by following the instructions in the [Oracle documentation](https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path).

## Installing the IntelliJ IDEA

IntelliJ is an IDE that offers strong support for Kotlin and Java development.

Install the [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/). Corda supports IntelliJ IDEA versions **2023.x** and **2024.x**, and Kotlin plugin version 1.9.20.


To install IntelliJ IDEA in a Ubuntu environment, navigate to the [Jetbrains IntelliJ snap package](https://snapcraft.io/intellij-idea-community).

## Installing Git

We use Git to host our sample CorDapp and provide version control.

To install Git, navigate to [Git](https://git-scm.com/) and install your preferred version, depending on your OS.

## Installing Gradle

If you intend to proceed directly to run a sample CorDapp, as described in [Running a sample CorDapp]({{< relref "tutorial-cordapp.md" >}}), the included `gradlew` script should install Gradle automatically when you open the sample CorDapp in IntelliJ.

If you'd prefer to install Gradle manually, navigate to [Gradle](https://gradle.org/releases/) then locate and install Gradle **version 7.6.4**. 

## Next steps

First, run the [sample CorDapp]({{< relref "tutorial-cordapp.md" >}}).

Next, read through the [Corda Key Concepts]({{< relref "about-corda/corda-key-concepts.md" >}}) to understand how Corda works.

By then, you’ll be ready to start writing your own CorDapps. You may want to refer to the
API documentation, the [flow cookbook]({{< relref "flow-cookbook.md" >}}) and the
[samples](https://www.corda.net/samples/) along the way.

If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via [our Slack channels](http://cordaledger.slack.com).
