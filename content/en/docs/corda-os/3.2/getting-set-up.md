---
aliases:
- /releases/release-V3.2/getting-set-up.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- getting
- set
title: Getting set up
---


# Getting set up


## Software requirements

Corda uses industry-standard tools:


* **Oracle JDK 8 JVM** - minimum supported version **8u171**
* **IntelliJ IDEA** - supported versions **2017.x** and **2018.x** (with Kotlin plugin version 1.2.51)
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
[Kotlin Koans](https://kotlinlang.org/docs/tutorials/koans.html).
* IntelliJ IDEA is recommended due to the strength of its Kotlin integration.

Following these software recommendations will minimize the number of errors you encounter, and make it easier for
others to provide support. However, if you do use other tools, we’d be interested to hear about any issues that arise.


## Set-up instructions

The instructions below will allow you to set up a Corda development environment and run a basic CorDapp. If you have
any issues, please consult the [Troubleshooting](troubleshooting.md) page, or reach out on [Slack](https://slack.corda.net/) or
[Stack Overflow](https://stackoverflow.com/questions/tagged/corda)

The set-up instructions are available for the following platforms:


* [Windows](#windows-label) (or [in video form](https://vimeo.com/217462250))
* [Mac](#mac-label) (or [in video form](https://vimeo.com/217462230))



## Windows


{{< warning >}}
If you are using a Mac machine, please follow the [Mac](#mac-label) instructions instead.

{{< /warning >}}



### Java


* Visit [http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* Scroll down to “Java SE Development Kit 8uXXX” (where “XXX” is the latest minor version number)
* Toggle “Accept License Agreement”
* Click the download link for jdk-8uXXX-windows-x64.exe (where “XXX” is the latest minor version number)
* Download and run the executable to install Java (use the default settings)
* Open a new command prompt and run `java -version` to test that Java is installed correctly


### Git


* Visit [https://git-scm.com/download/win](https://git-scm.com/download/win)
* Click the “64-bit Git for Windows Setup” download link.
* Download and run the executable to install Git (use the default settings)
* Open a new command prompt and type `git --version` to test that git is installed correctly


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?code=IIC)
* Download and run the executable to install IntelliJ Community Edition (use the default settings)
* Ensure the Kotlin plugin in Intellij is updated to version
{{< warning >}}|kotlin_version|{{< /warning >}}




### Download a sample project


* Open a command prompt
* Clone the CorDapp example repo by running `git clone https://github.com/corda/cordapp-example`
* Move into the cordapp-example folder by running `cd cordapp-example`


### Run from the command prompt


* From the cordapp-example folder, deploy the nodes by running `gradlew deployNodes`
* Start the nodes by running `call kotlin-source/build/nodes/runnodes.bat`
* Wait until all the terminal windows display either “Webserver started up in XX.X sec” or “Node for “NodeC” started up and registered in XX.XX sec”
* Test the CorDapp is running correctly by visiting the front end at [http://localhost:10007/web/example/](http://localhost:10007/web/example/)


### Run from IntelliJ


* Open IntelliJ Community Edition
* On the splash screen, click “Open” (do NOT click “Import Project”) and select the cordapp-example folder


{{< warning >}}
If you click “Import Project” instead of “Open”, the project’s run configurations will be erased!

{{< /warning >}}



* Once the project is open, click “File > Project Structure”. Under “Project SDK:”, set the project SDK by clicking “New…”, clicking “JDK”, and navigating to C:\Program Files\Java\jdk1.8.0_XXX (where “XXX” is the latest minor version number). Click “OK”.
* Click “View > Tool Windows > Event Log”, and click “Import Gradle project”, then “OK”. Wait, and click “OK” again when the “Gradle Project Data To Import” window appears
* Wait for indexing to finish (a progress bar will display at the bottom-right of the IntelliJ window until indexing is complete)
* At the top-right of the screen, to the left of the green “play” arrow, you should see a dropdown. In that dropdown, select “Run Example Cordapp - Kotlin” and click the green “play” arrow.
* Wait until the run windows displays the message “Webserver started up in XX.X sec”
* Test the CorDapp is running correctly by visiting the front end at [http://localhost:10007/web/example/](http://localhost:10007/web/example/)



## Mac


{{< warning >}}
If you are using a Windows machine, please follow the [Windows](#windows-label) instructions instead.

{{< /warning >}}



### Java


* Open “System Preferences > Java”
* In the Java Control Panel, if an update is available, click “Update Now”
* In the “Software Update” window, click “Install Update”. If required, enter your password and click “Install Helper” when prompted
* Wait for a pop-up window indicating that you have successfully installed the update, and click “Close”
* Open a new terminal and type `java -version` to test that Java is installed correctly


### IntelliJ


* Visit [https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC](https://www.jetbrains.com/idea/download/download-thanks.html?platform=mac&code=IIC)
* Download and run the executable to install IntelliJ Community Edition (use the default settings)
* Ensure the Kotlin plugin in Intellij is updated to version
{{< warning >}}|kotlin_version|{{< /warning >}}




### Download a sample project


* Open a terminal
* Clone the CorDapp example repo by running `git clone https://github.com/corda/cordapp-example`
* Move into the cordapp-example folder by running `cd cordapp-example`


### Run from the terminal


* From the cordapp-example folder, deploy the nodes by running `./gradlew deployNodes`
* Start the nodes by running `kotlin-source/build/nodes/runnodes`. Do not click while 8 additional terminal windows start up.
* Wait until all the terminal windows display either “Webserver started up in XX.X sec” or “Node for “NodeC” started up and registered in XX.XX sec”
* Test the CorDapp is running correctly by visiting the front end at [http://localhost:10007/web/example/](http://localhost:10007/web/example/)


### Run from IntelliJ


* Open IntelliJ Community Edition
* On the splash screen, click “Open” (do NOT click “Import Project”) and select the cordapp-example folder
* Once the project is open, click “File > Project Structure”. Under “Project SDK:”, set the project SDK by clicking “New…”, clicking “JDK”, and navigating to /Library/Java/JavaVirtualMachines/jdk1.8.0_XXX (where “XXX” is the latest minor version number). Click “OK”.
* Click “View > Tool Windows > Event Log”, and click “Import Gradle project”, then “OK”. Wait, and click “OK” again when the “Gradle Project Data To Import” window appears
* Wait for indexing to finish (a progress bar will display at the bottom-right of the IntelliJ window until indexing is complete)
* At the top-right of the screen, to the left of the green “play” arrow, you should see a dropdown. In that dropdown, select “Run Example Cordapp - Kotlin” and click the green “play” arrow.
* Wait until the run windows displays the message “Webserver started up in XX.X sec”
* Test the CorDapp is running correctly by visiting the front end at [http://localhost:10007/web/example/](http://localhost:10007/web/example/)


## Corda source code

The Corda platform source code is available here:


[https://github.com/corda/corda.git](https://github.com/corda/corda.git)


A CorDapp template that you can use as the basis for your own CorDapps is available in both Java and Kotlin versions:


[https://github.com/corda/cordapp-template-java.git](https://github.com/corda/cordapp-template-java.git)

[https://github.com/corda/cordapp-template-kotlin.git](https://github.com/corda/cordapp-template-kotlin.git)


And a list of simple sample CorDapps for you to explore basic concepts is available here:


[https://www.corda.net/samples/](https://www.corda.net/samples/)


You can clone these repos to your local machine by running the command `git clone [repo URL]`.


## Next steps

The best way to check that everything is working fine is by taking a deeper look at the
[example CorDapp](tutorial-cordapp.md).

Next, you should read through [Corda Key Concepts](key-concepts.md) to understand how Corda works.

By then, you’ll be ready to start writing your own CorDapps. Learn how to do this in the
[Hello, World tutorial](hello-world-introduction.md). You may want to refer to the API docs, the
[flow cookbook](flow-cookbook.md) and the [samples](https://www.corda.net/samples/) along the way.

If you encounter any issues, please see the [Troubleshooting](troubleshooting.md) page, or get in touch with us on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) or via [slack](https://slack.corda.net/).

