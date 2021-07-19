---
aliases:
- /releases/4.2/getting-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-getting-set-up
    parent: corda-enterprise-4-2-building-a-cordapp-index
    weight: 1020
tags:
- getting
- set
title: Getting set up for CorDapp development
---


# Getting set up for CorDapp development


## Software requirements

Corda uses industry-standard tools:


* **Java 8 JVM** - we require at least version 8u171, but do not currently support Java 9 or higher.We have tested with the following builds:
    * [Oracle JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
    * [Amazon Corretto](https://aws.amazon.com/corretto/)
    * [Red Hat’s OpenJDK](https://developers.redhat.com/products/openjdk/overview/)
    * [Zulu’s OpenJDK](https://www.azul.com/)

Please note that OpenJDK builds usually exclude JavaFX, which our GUI tools require.
* **IntelliJ IDEA** - supported versions **2017.x**, **2018.x** and **2019.x** (with Kotlin plugin version 1.2.71)
* **Gradle** - we use 4.10 and the `gradlew` script in the project / samples directories will download it for you.

Please note:


* Applications on Corda (CorDapps) can be written in any language targeting the JVM. However, Corda itself and most of
the samples are written in Kotlin. Kotlin is an
[official Android language](https://developer.android.com/kotlin/index.html), and you can read more about why
Kotlin is a strong successor to Java
[here](https://medium.com/@octskyward/why-kotlin-is-my-next-programming-language-c25c001e26e3). If you’re
unfamiliar with Kotlin, there is an official
[getting started guide](https://kotlinlang.org/docs/tutorials/), and a series of
[Kotlin Koans](https://kotlinlang.org/docs/tutorials/koans.html)
* IntelliJ IDEA is recommended due to the strength of its Kotlin integration.
* If an HA Bridge/Float deployment is required then a `Zookeeper 3.5.4-Beta` cluster will be required.
Refer to [Hot-cold deployment](hot-cold-deployment.md) and Bridge configuration
for more deployment information.

Following these software recommendations will minimize the number of errors you encounter, and make it easier for
others to provide support. However, if you do use other tools, we’d be interested to hear about any issues that arise.


## Set-up instructions

The instructions below will allow you to set up your development environment for running Corda and writing CorDapps. If
you have any issues, please reach out on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via
[our Slack channels](https://slack.corda.net/).

The set-up instructions are available for the following platforms:


* [Windows](#windows-label) (or [in video form](https://vimeo.com/217462250))
* [Mac](#mac-label) (or [in video form](https://vimeo.com/217462230))
* [Next steps](#deb-ubuntu-label)
* [Fedora](#fedora-label)

{{< note >}}
These setup instructions will guide you on how to install the Oracle JDK.

{{< /note >}}


## Windows


{{< warning >}}
If you are using a Mac, Debian/Ubuntu or Fedora machine, please follow the [Mac](#mac-label), [Next steps](#deb-ubuntu-label) or [Fedora](#fedora-label) instructions instead.

{{< /warning >}}



### Java


* Visit [http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* Click the download link for jdk-8uXXX-windows-x64.exe (where “XXX” is the latest minor version number)
* Download and run the executable to install Java (use the default settings)
* Add Java to the PATH environment variable by following the instructions in the [Oracle documentation](https://docs.oracle.com/javase/7/docs/webnotes/install/windows/jdk-installation-windows.html#path)
* Open a new command prompt and run `java -version` to test that Java is installed correctly


### Git


* Visit [https://git-scm.com/download/win](https://git-scm.com/download/win)
* Click the “64-bit Git for Windows Setup” download link.
* Download and run the executable to install Git (use the default settings)
* Open a new command prompt and type `git --version` to test that git is installed correctly


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?code=IIC)
* Download and run the executable to install IntelliJ Community Edition (use the default settings)
* Ensure the Kotlin plugin in Intellij is updated to version 1.2.71 (new installs will contains this version)



## Mac


{{< warning >}}
If you are using a Windows, Debian/Ubuntu or Fedora machine, please follow the [Windows](#windows-label), [Next steps](#deb-ubuntu-label) or [Fedora](#fedora-label) instructions instead.

{{< /warning >}}



### Java


* Visit [http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* Click the download link for jdk-8uXXX-macosx-x64.dmg (where “XXX” is the latest minor version number)
* Download and run the executable to install Java (use the default settings)
* Open a new terminal window and run `java -version` to test that Java is installed correctly


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC)
* Download and run the executable to install IntelliJ Community Edition (use the default settings)
* Ensure the Kotlin plugin in IntelliJ is updated to version 1.2.71 (new installs will contains this version)


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
* Ensure the Kotlin plugin in Intellij is updated to version 1.2.71 (new installs will contains this version)



## Fedora


{{< warning >}}
If you are using a Mac, Windows or Debian/Ubuntu machine, please follow the [Mac](#mac-label), [Windows](#windows-label) or [Next steps](#deb-ubuntu-label) instructions instead.

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
* Ensure the Kotlin plugin in IntelliJ is updated to version 1.2.71 (new installs will contains this version)


## Resolve Corda Enterprise binaries

The Corda Enterprise binaries are not available in a publicly accessible Maven repository. Instead, the Corda Enterprise
binaries will be made available to your organisation as a compressed tarball (corda-4.2-developer-pack.tar.gz).
This tarball contains all of the Corda dependencies as they would appear in your local Maven repository located at
`C:\Documents and Settings\{your-username}\.m2`.

To build CorDapps on development machines the Corda Enterprise binaries will need to be discoverable by Gradle. The
[build.gradle](https://github.com/corda/samples/tree/release-V4-enterprise/cordapp-example/build.gradle) file in the Corda
samples repository (`release-V4-enterprise` branch) includes instructions on how to allow Gradle to discover dependencies.


* Open `samples\cordapp-example\build.gradle`
* Do any of the following to allow Gradle to resolve Corda Enterprise binaries, for more information read the commented code in `build.gradle`:
* Add Corda Enterprise binaries and dependencies to your local maven repository path (e.g., `C:\Documents and Settings\{your-username}\.m2`).
* Upload Corda Enterprise binaries and dependencies to your company’s private Maven repository and register the repository with Gradle.
* Add Corda Enterprise binaries to a local directory and register a local Maven repository pointing to this directory with Gradle.



{{< note >}}
Upon receiving the binaries, the quickest way to get started developing your CorDapps is **option a**. This can

{{< /note >}}
`respository` folder to your local Maven repository located at `C:\Documents and Settings\{your-username}\.m2`.
## Download and run a sample project

Follow the instructions in [https://docs.corda.net/tutorial-cordapp.html](https://docs.corda.net/tutorial-cordapp.html).


{{< warning >}}
Ensure you checkout the corresponding branch for for Corda Enterprise 4.2 by running `git checkout release-V4-enterprise` in the samples directory

{{< /warning >}}



## CorDapp Templates and samples

A CorDapp template that you can use as the basis for your own CorDapps is available in both Java and Kotlin versions:


[https://github.com/corda/cordapp-template-java.git](https://github.com/corda/cordapp-template-java.git)

[https://github.com/corda/cordapp-template-kotlin.git](https://github.com/corda/cordapp-template-kotlin.git)


A comprehensive list of samples, including CorDapps written by R3 and community CorDapps and projects, are available here:


[https://www.corda.net/samples/](https://www.corda.net/samples/)


You can clone these repos to your local machine by running the command `git clone [repo URL]`.



## Next steps

The best way to check that everything is working fine is by taking a deeper look at the
[example CorDapp](tutorial-cordapp.md).

Next, you should read through [Corda Key Concepts](key-concepts.md) to understand how Corda works.

By then, you’ll be ready to start writing your own CorDapps. Learn how to do this in the
[Hello, World tutorial](hello-world-introduction.md). You may want to refer to the
[API documentation](corda-api.md), the [flow cookbook](flow-cookbook.md) and the
[samples](https://www.corda.net/samples/) along the way.

If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via
[our Slack channels](https://slack.corda.net/).

