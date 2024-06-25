---
aliases:
- /docs/corda-enterprise/head/cordapps/getting-set-up.html
- /docs/corda-enterprise/cordapps/getting-set-up.html
date: '2021-07-15'
menu:
  corda-enterprise-4-12:
    parent: corda-enterprise-4-12-cordapps
tags:
- getting
- set
title: Getting set up for CorDapp development
weight: 10

---

# Get set up for CorDapp development

Before you start developing CorDapps, you need to download four pieces of software: the Java 17 JDK, IntelliJ IDEA, Git, and Gradle.

## Install the Java 17 JDK

Install the Java 17 JDK. 

Corda 4.12 has been tested against the following Java builds:

  * [Oracle JDK 17.0.9](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
  * [Zulu’s OpenJDK 17.46.19 (17.0.9+8)](https://www.azul.com/downloads/?version=java-17-lts&show-old-builds=true#zulu)

{{< note >}}
  OpenJDK builds often exclude JavaFX, which is required by the Corda GUI tools.
  {{< /note >}}

If you are using Windows, you must also add Java to the PATH environment variable by following the instructions in the [Oracle documentation](https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path).

## Install IntelliJ IDEA

IntelliJ IDEA is an integrated development environment (IDE) that offers strong support for Kotlin and Java development.

Install the [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/). Corda supports IntelliJ IDEA versions **2017.x**, **2018.x**, **2019.x**, **2020.x**, and **2024.x**, and Kotlin plugin version 1.9.20.


To install IntelliJ IDEA in a Ubuntu environment, go to the [Jetbrains IntelliJ snap package](https://snapcraft.io/intellij-idea-community).

## Install Git

We use Git to host our sample CorDapp and provide version control.

To install Git, go to [Git](https://git-scm.com/) and install the version for your operating system.

## Install Gradle

Gradle is a build automation tool for multi-language software development. It controls the development process in the tasks of compilation and packaging to testing, deployment, and publishing.

* If you [run the sample CorDapp]({{< relref "tutorial-cordapp.md" >}}), the included `gradlew` script installs Gradle automatically when you open the sample CorDapp in IntelliJ.
* If you plan to start developing your own CorDapp straight away, install Gradle manually. Go to [Gradle](https://gradle.org/releases/), then locate and install Gradle **version 7.6.4**. 

You now have everything you need to develop CorDapps. If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via [our Slack channels](http://slack.corda.net/).

## Run a sample CorDapp *(optional)*

R3 recommends [running a sample CorDapp]({{< relref "tutorial-cordapp.md" >}}) to see Corda in action before you start developing.

## Resources

* [Sample CorDapps, templates, and community projects](https://www.corda.net/samples/).
* [Corda API documentation](../../../../../../en/api-ref.html).
* [Flow cookbook]({{< relref "flow-cookbook.md" >}}).
* CorDapp [Java](https://github.com/corda/samples-java) and [Kotlin](https://github.com/corda/samples-kotlin) sample repositories - contain multiple sample CorDapps, from those to get you started, to those which demonstrate specific features and advanced usage.
* CorDapp [Java](https://github.com/corda/cordapp-template-java) and [Kotlin](https://github.com/corda/cordapp-template-kotlin) templates - a stubbed-out CorDapp that you can use to bootstrap your own CorDapps.

For more developer resources, open-source projects, and CorDapp templates, check out R3's [Developer Portal](https://developer.r3.com/corda/).
