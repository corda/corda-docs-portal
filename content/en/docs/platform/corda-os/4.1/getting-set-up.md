---
aliases:
- /releases/release-V4.1/getting-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-1:
    identifier: corda-os-4-1-getting-set-up
    parent: corda-os-4-1-building-a-cordapp-index
    weight: 1020
tags:
- getting
- set
title: Getting set up for CorDapp development
---


# Getting set up for CorDapp development

There are four pieces of required software for CorDapp development: the Java 8 JDK, IntelliJ IDEA, Git, and Gradle 4.10.


* Install the Java 8 JDK, version 8u171. We have tested using the following Java builds:



* [Oracle JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* [Amazon Corretto](https://aws.amazon.com/corretto/)
* [Red Hat’s OpenJDK](https://developers.redhat.com/products/openjdk/overview/)
* [Zulu’s OpenJDK](https://www.azul.com/)

Please note: OpenJDK builds often exclude JavaFX, which is required by the Corda GUI tools. Corda supports only Java 8.

If you are using Windows: Add Java to the PATH environment variable by following the instructions in the [Oracle documentation](https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path).



* Install [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/). Corda supports IntelliJ IDEA versions **2017.x**, **2018.x**, and **2019.x**; and Kotlin plugin version 1.2.71.


To install IntelliJ IDEA in a Ubuntu environment, navigate to the [Jetbrains IntelliJ snap package](https://snapcraft.io/intellij-idea-community).



* Install [git](https://git-scm.com/).
* Install [Gradle version 4.10](https://gradle.org/install/). If you are using a supported Corda sample, the included `gradlew` script should install Gradle automatically.


Please note: Corda requires Gradle version 4.10, and does not support any other version of Gradle.



## Next steps

First, run the [example CorDapp](tutorial-cordapp.md).

Next, read through the [Corda Key Concepts](key-concepts.md) to understand how Corda works.

By then, you’ll be ready to start writing your own CorDapps. You may want to refer to the
[API documentation](corda-api.md), the [flow cookbook](flow-cookbook.md) and the
[samples](https://www.corda.net/samples/) along the way.

If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via [our Slack channels](http://cordaledger.slack.com/).
