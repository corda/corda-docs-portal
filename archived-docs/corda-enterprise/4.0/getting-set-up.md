---
aliases:
- /releases/4.0/getting-set-up.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-getting-set-up
    parent: corda-enterprise-4-0-building-a-cordapp-index
    weight: 1020
tags:
- getting
- set
title: Getting set up for CorDapp development
---


# Getting set up for CorDapp development


## Software requirements

Corda uses industry-standard tools:


* **Java 8 JVM** - we require at least version 8u171, but do not currently support Java 9 or higher.
We have tested with Oracle JDK, Amazon Corretto, and Red Hat’s OpenJDK builds. Please note that OpenJDK builds
usually exclude JavaFX, which our GUI tools require.
* **IntelliJ IDEA** - supported versions **2017.x** and **2018.x** (with Kotlin plugin version 1.2.71)
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


### Download a sample project


* Open a command prompt
* Clone the CorDapp example repo by running `git clone https://github.com/corda/cordapp-example`
* Move into the `cordapp-example` folder by running `cd cordapp-example`
* Checkout the corresponding branch for Corda Enterprise 3.1 by running `git checkout release-enterprise-V3` in the current directory


### Resolve Corda Enterprise binaries

The Corda Enterprise binaries are not available in a publicly accessible Maven repository. Instead, the Corda Enterprise
binaries will be made available to your organisation as a compressed tarball (`corda-3.1-developer-pack.tar.gz`).
This tarball contains all of the Corda dependencies as they would appear in your local Maven repository located at
`C:\Documents and Settings\{your-username}\.m2`.

To build CorDapps on development machines the Corda Enterprise binaries will need to be discoverable by Gradle. The
[build.gradle](https://github.com/corda/cordapp-example/blob/release-enterprise-V3/build.gradle) file on the
`cordapp-example` `release-enterprise-V3` branch includes instructions on how to allow Gradle to discover
dependencies.


* Open `cordapp-example\build.gradle`
* Do any of the following to allow Gradle to resolve Corda Enterprise binaries, for more information read the commented code in `build.gradle`:
* Add Corda Enterprise binaries and dependencies to your local maven repository path (e.g., `C:\Documents and Settings\{your-username}\.m2`).
* Upload Corda Enterprise binaries and dependencies to your company’s private Maven repository and register the repository with Gradle.
* Add Corda Enterprise binaries to a local directory and register a local Maven repository pointing to this directory with Gradle.



{{< note >}}
Upon receiving the binaries, the quickest way to get started developing your CorDapps is **option a**. This can
be done by firstly unpacking the `corda-3.1-developer-pack.tar.gz` compressed tarball. Then, copy the unpacked
`respository` folder to your local Maven repository located at `C:\Documents and Settings\{your-username}\.m2`.

{{< /note >}}

### Run from the command prompt


* Move into the `cordapp-example` folder by running `cd cordapp-example`
* From the `cordapp-example` folder, deploy the nodes by running `gradlew deployNodes`
* Start the nodes by running `call kotlin-source/build/nodes/runnodes.bat`
* Wait until all the terminal windows display either `Webserver started up in XX.X sec` or `Node for "NodeC" started up and registered in XX.XX sec`
* Confirm that the CorDapp is running correctly by visiting the front end at [http://localhost:10009/web/example/](http://localhost:10009/web/example/)


### Run from IntelliJ


* Open IntelliJ Community Edition
* On the splash screen, click `Open` (do **not** click `Import Project`) and select the `cordapp-example` folder


{{< warning >}}
If you click `Import Project` instead of `Open`, the project’s run configurations will be erased!

{{< /warning >}}



* Once the project is open, click `File`, then `Project Structure`. Under `Project SDK:`, set the project SDK by
clicking `New...`, clicking `JDK`, and navigating to `C:\\Program Files\\Java\\jdk1.8.0_XXX` (where `XXX` is
the latest minor version number). Click `OK`
* Again under `File` then `Project Structure`, select `Modules`. Click `+`, then `Import Module`, then select
the `cordapp-example` folder and click `Open`. Choose to `Import module from external model`, select
`Gradle`, click `Next` then `Finish` (leaving the defaults) and `OK`
* Wait for the indexing to finish (a progress bar will display at the bottom-right of the IntelliJ window until indexing
is complete)
* At the top-right of the screen, to the left of the green `play` arrow, you should see a dropdown. In that
dropdown, select `Run Example Cordapp - Kotlin` and click the green `play` arrow.
* Wait until the run windows displays the message `Webserver started up in XX.X sec`
* Confirm that the CorDapp is running correctly by visiting the front end at 
{{< warning >}}`{{< /warning >}}

[http://localhost:10009/web/example/](http://localhost:10009/web/example/)



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
* Open a new terminal window and run `java -version` to test that Java is installed correctly. The version should be
“8u171” or higher.


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC)
* Download and run the executable to install IntelliJ Community Edition (use the default settings)
* Ensure the Kotlin plugin in Intellij is updated to version 1.2.71


### Download a sample project


* Open a terminal
* Clone the CorDapp example repo by running `git clone https://github.com/corda/cordapp-example`
* Move into the `cordapp-example` folder by running `cd cordapp-example`
* Checkout the corresponding branch for Corda Enterprise 3.1 by running `git checkout release-enterprise-V3` in the current directory



### Resolve Corda Enterprise binaries

The Corda Enterprise binaries are not available in a publicly accessible Maven repository. Instead, the Corda Enterprise
binaries will be made available to your organisation as a compressed tarball (`corda-3.1-developer-pack.tar.gz`).
This tarball contains all of the Corda dependencies as they would appear in your local Maven repository located at
`~/.m2/repository`.

To build CorDapps on development machines the Corda Enterprise binaries will need to be discoverable by Gradle. The
[build.gradle](https://github.com/corda/cordapp-example/blob/release-enterprise-V3/build.gradle) file on the
`cordapp-example` `release-enterprise-V3` branch includes instructions on how to allow Gradle to discover
dependencies.


* Open `cordapp-example/build.gradle`
* Do any of the following to allow Gradle to resolve Corda Enterprise binaries, for more information read the commented code in `build.gradle`:
* Add Corda Enterprise binaries and dependencies to your local maven repository path e.g., `~/.m2/repository`
* Upload Corda Enterprise binaries and dependencies to your company’s private Maven repository and register the repository with Gradle.
* Add Corda Enterprise binaries to a local directory and register a local Maven repository pointing to this directory with Gradle.



{{< note >}}
Upon receiving the binaries, the quickest way to get started developing your CorDapps is **option a**. This can

{{< /note >}}
be done by firstly unpacking the `corda-3.1-developer-pack.tar.gz` compressed tarball:



`tar -xvzf corda-3.1-developer-pack.tar.gz`


Then, copy the unpacked `respository` folder to your local Maven repository:


`rsync -av repository ~/.m2/`


The extracted folder can now be deleted:


`rm -rf repository`




### Run from the terminal


* Move into the `cordapp-example` folder by running `cd cordapp-example`
* From the `cordapp-example` folder, deploy the nodes by running `./gradlew deployNodes`
* Start the nodes by running `kotlin-source/build/nodes/runnodes`. Do not click while 7 additional terminal windows start up.
* Wait until all the terminal windows display either `Webserver started up in XX.X sec` or `Node for "NodeC" started up and registered in XX.XX sec`
* Confirm that the CorDapp is running correctly by visiting the front end at [http://localhost:10009/web/example/](http://localhost:10009/web/example/)


### Run from IntelliJ


* Open IntelliJ Community Edition
* On the splash screen, click `Open` (do **not** click `Import Project`) and select the `cordapp-example` folder


{{< warning >}}
If you click `Import Project` instead of `Open`, the project’s run configurations will be erased!

{{< /warning >}}



* Once the project is open, click `File`, then `Project Structure`. Under `Project SDK:`, set the project SDK by
clicking `New...`, clicking `JDK`, and navigating to your JDK installation (e.g., `/Library/Java/JavaVirtualMachines/jdk1.8.0_XXX.jdk`, where `XXX` is
the latest minor version number). Click `OK`
* Again under `File` then `Project Structure`, select `Modules`. Click `+`, then `Import Module`, then select
the `cordapp-example` folder and click `Open`. Choose to `Import module from external model`, select
`Gradle`, click `Next` then `Finish` (leaving the defaults) and `OK`
* Wait for the indexing to finish (a progress bar will display at the bottom-right of the IntelliJ window until indexing
is complete)
* At the top-right of the screen, to the left of the green `play` arrow, you should see a dropdown. In that
dropdown, select `Run Example Cordapp - Kotlin` and click the green `play` arrow.
* Wait until the run windows displays the message `Webserver started up in XX.X sec`
* Confirm that the CorDapp is running correctly by visiting the front end at [http://localhost:10009/web/example/](http://localhost:10009/web/example/)


## CorDapp Templates and samples

A CorDapp template that you can use as the basis for your own CorDapps is available in both Java and Kotlin versions:


[https://github.com/corda/cordapp-template-java.git](https://github.com/corda/cordapp-template-java.git)

[https://github.com/corda/cordapp-template-kotlin.git](https://github.com/corda/cordapp-template-kotlin.git)


And a list of simple sample CorDapps for you to explore basic concepts is available here:


[https://www.corda.net/samples/](https://www.corda.net/samples/)


You can clone these repos to your local machine by running the command `git clone [repo URL]`.



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

The best way to check that everything is working fine is by taking a deeper look at the
[example CorDapp](tutorial-cordapp.md).

Next, you should read through [Corda Key Concepts](key-concepts.md) to understand how Corda works.

By then, you’ll be ready to start writing your own CorDapps. Learn how to do this in the
[Hello, World tutorial](hello-world-introduction.md). You may want to refer to the
[API documentation](corda-api.md), the [flow cookbook](flow-cookbook.md) and the
[samples](https://www.corda.net/samples/) along the way.

If you encounter any issues, please ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via
[our Slack channels](https://slack.corda.net/).

