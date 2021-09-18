---
aliases:
- /releases/release-V4.0/getting-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-getting-set-up
    parent: corda-os-4-0-building-a-cordapp-index
    weight: 1020
tags:
- getting
- set
title: Getting set up for CorDapp development
---


# Getting set up for CorDapp development


## Software requirements

Corda uses industry-standard tools:


* **Oracle JDK 8 JVM** - minimum supported version **8u171**
* **IntelliJ IDEA** - supported versions **2017.x** and **2018.x** (with Kotlin plugin version 1.2.71)
* **Git**

We also use Gradle and Kotlin, but you do not need to install them. A standalone Gradle wrapper is provided, and it
will download the correct version of Kotlin.

Please note:


* Corda runs in a JVM. JVM implementations other than Oracle JDK 8 are not actively supported. However, if you do
choose to use OpenJDK, you will also need to install OpenJFX
* Applications on Corda (CorDapps) can be written in any language targeting the JVM. However, Corda itself and most of
the samples are written in Kotlin. Kotlin is an
[official Android language](https://developer.android.com/kotlin/index.html), and you can read more about why
Kotlin is a strong successor to Java
[here](https://medium.com/@octskyward/why-kotlin-is-my-next-programming-language-c25c001e26e3). If you’re
unfamiliar with Kotlin, there is an official
[getting started guide](https://kotlinlang.org/docs/tutorials/), and a series of
[Kotlin Koans](https://kotlinlang.org/docs/tutorials/koans.html)
* IntelliJ IDEA is recommended due to the strength of its Kotlin integration

Following these software recommendations will minimize the number of errors you encounter, and make it easier for
others to provide support. However, if you do use other tools, we’d be interested to hear about any issues that arise.


## Set-up instructions

The instructions below will allow you to set up your development environment for running Corda and writing CorDapps. If
you have any issues, please reach out on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via
[our Slack channels](http://cordaledger.slack.com/).

The set-up instructions are available for the following platforms:


* [Windows](#windows-label) (or [in video form](https://vimeo.com/217462250))
* [Mac](#mac-label) (or [in video form](https://vimeo.com/217462230))
* [Debian/Ubuntu](#deb-ubuntu-label)
* [Fedora](#fedora-label)



## Windows


{{< warning >}}
If you are using a Mac, Debian/Ubuntu or Fedora machine, please follow the [Mac](#mac-label), [Debian/Ubuntu](#deb-ubuntu-label) or [Fedora](#fedora-label) instructions instead.

{{< /warning >}}



### Java


* Visit [http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* Scroll down to “Java SE Development Kit 8uXXX” (where “XXX” is the latest minor version number)
* Toggle “Accept License Agreement”
* Click the download link for jdk-8uXXX-windows-x64.exe (where “XXX” is the latest minor version number)
* Download and run the executable to install Java (use the default settings)
* Add Java to the PATH environment variable by following the instructions at [https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path](https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path)
* Open a new command prompt and run `java -version` to test that Java is installed correctly


### Git


* Visit [https://git-scm.com/download/win](https://git-scm.com/download/win)
* Click the “64-bit Git for Windows Setup” download link.
* Download and run the executable to install Git (use the default settings)
* Open a new command prompt and type `git --version` to test that git is installed correctly


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?code=IIC)
* Download and run the executable to install IntelliJ Community Edition (use the default settings)
* Ensure the Kotlin plugin in Intellij is updated to version 1.2.71



## Mac


{{< warning >}}
If you are using a Windows, Debian/Ubuntu or Fedora machine, please follow the [Windows](#windows-label), [Debian/Ubuntu](#deb-ubuntu-label) or [Fedora](#fedora-label) instructions instead.

{{< /warning >}}



### Java


* Visit [http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* Scroll down to “Java SE Development Kit 8uXXX” (where “XXX” is the latest minor version number)
* Toggle “Accept License Agreement”
* Click the download link for jdk-8uXXX-macosx-x64.dmg (where “XXX” is the latest minor version number)
* Download and run the executable to install Java (use the default settings)
* Open a new terminal window and run `java -version` to test that Java is installed correctly


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC)
* Download and run the executable to install IntelliJ Community Edition (use the default settings)
* Ensure the Kotlin plugin in Intellij is updated to version 1.2.71



## Debian/Ubuntu


{{< warning >}}
If you are using a Mac, Windows or Fedora machine, please follow the [Mac](#mac-label), [Windows](#windows-label) or [Fedora](#fedora-label) instructions instead.

{{< /warning >}}


These instructions were tested on Ubuntu Desktop 18.04 LTS.


### Java


* Open a new terminal and add the Oracle PPA to your repositories by typing `sudo add-apt-repository ppa:webupd8team/java`. Press ENTER when prompted.
* Update your packages list with the command `sudo apt update`
* Install the Oracle JDK 8 by typing `sudo apt install oracle-java8-installer`. Press Y when prompted and agree to the licence terms.
* Verify that the JDK was installed correctly by running `java -version`


### Git


* From the terminal, Git can be installed using apt with the command `sudo apt install git`
* Verify that git was installed correctly by typing `git --version`


### IntelliJ

Jetbrains offers a pre-built snap package that allows for easy, one-step installation of IntelliJ onto Ubuntu.


* To download the snap, navigate to [https://snapcraft.io/intellij-idea-community](https://snapcraft.io/intellij-idea-community)
* Click `Install`, then `View in Desktop Store`. Choose `Ubuntu Software` in the Launch Application window.
* Ensure the Kotlin plugin in Intellij is updated to version 1.2.71



## Fedora


{{< warning >}}
If you are using a Mac, Windows or Debian/Ubuntu machine, please follow the [Mac](#mac-label), [Windows](#windows-label) or [Debian/Ubuntu](#deb-ubuntu-label) instructions instead.

{{< /warning >}}


These instructions were tested on Fedora 28.


### Java


* Download the RPM installation file of Oracle JDK from [https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).
* Install the package with `rpm -ivh jdk-<version>-linux-<architecture>.rpm` or use the default software manager.
* Choose java version by using the following command `alternatives --config java`
* Verify that the JDK was installed correctly by running `java -version`


### Git


* From the terminal, Git can be installed using dnf with the command `sudo dnf install git`
* Verify that git was installed correctly by typing `git --version`


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?platform=linux&code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?platform=linux&code=IIC)
* Unpack the `tar.gz` file using the following command `tar xfz ideaIC-<version>.tar.gz -C /opt`
* Run IntelliJ with `/opt/ideaIC-<version>/bin/idea.sh`
* Ensure the Kotlin plugin in IntelliJ is updated to version 1.2.71


## Next steps

First, run the [example CorDapp](tutorial-cordapp.md).

Next, read through the [Corda Key Concepts](key-concepts.md) to understand how Corda works.

By then, you’ll be ready to start writing your own CorDapps. Learn how to do this in the
[Hello, World tutorial](hello-world-introduction.md). You may want to refer to the
[API documentation](corda-api.md), the [flow cookbook](flow-cookbook.md) and the
[samples](https://www.corda.net/samples/) along the way.

If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via
[our Slack channels](http://cordaledger.slack.com/).
