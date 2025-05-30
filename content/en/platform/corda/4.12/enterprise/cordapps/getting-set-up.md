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

Install the Java 17 JDK. Corda requires at least version 17.0.9, but does not currently support Java 18 or higher.

Corda has been tested against the following Java builds:

  * [Oracle JDK](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
  * [Zulu’s OpenJDK](https://www.azul.com)

{{< note >}}
  OpenJDK builds often exclude JavaFX, which is required by the Corda GUI tools. Corda supports only Java 17.
  {{< /note >}}

If you are using Windows, you must also add Java to the PATH environment variable by following the instructions in the [Oracle documentation](https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path).

## Install IntelliJ IDEA

IntelliJ IDEA is an integrated development environment (IDE) that offers strong support for Kotlin and Java development.

Install the [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/). Corda supports IntelliJ IDEA versions **2023.x** and **2024.x**, and Kotlin plugin version 1.9.20.


To install IntelliJ IDEA in a Ubuntu environment, go to the [Jetbrains IntelliJ snap package](https://snapcraft.io/intellij-idea-community).

## Install Git

We use Git to host our sample CorDapp and provide version control.

To install Git, go to [Git](https://git-scm.com/) and install the version for your operating system.

## Install Gradle

Gradle is a build automation tool for multi-language software development. It controls the development process in the tasks of compilation and packaging to testing, deployment, and publishing.

* If you [run the sample CorDapp]({{< relref "tutorial-cordapp.md" >}}), the included `gradlew` script installs Gradle automatically when you open the sample CorDapp in IntelliJ.
* If you plan to start developing your own CorDapp straight away, install Gradle manually. Go to [Gradle](https://gradle.org/releases/), then locate and install Gradle **version 7.6.4**. Corda requires Gradle version 7.6.x, and does not support Gradle 8.x.

You now have everything you need to develop CorDapps. If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via [our Slack channels](http://slack.corda.net/).

## Run a sample CorDapp *(optional)*

R3 recommends [running a sample CorDapp]({{< relref "tutorial-cordapp.md" >}}) to see Corda in action before you start developing.

## Resources

* [Sample CorDapps, templates, and community projects](https://www.corda.net/samples/)
* [Corda API documentation]({{< relref "../../../../../../en/api-ref/_index.md" >}})
* [Flow cookbook]({{< relref "flow-cookbook.md" >}})
* CorDapp [Java](https://github.com/corda/samples-java/tree/release/4.12) and [Kotlin](https://github.com/corda/samples-kotlin/tree/release/4.12) sample repositories - contain multiple sample CorDapps, from those to get you started, to those which demonstrate specific features and advanced usage
* CorDapp [Java](https://github.com/corda/cordapp-template-java/tree/release/4.12) and [Kotlin](https://github.com/corda/cordapp-template-kotlin/tree/release/4.12) templates - a stubbed-out CorDapp that you can use to bootstrap your own CorDapps

For more developer resources, open-source projects, and CorDapp templates, check out R3's [Developer Platform](https://developer.r3.com/) portal.
