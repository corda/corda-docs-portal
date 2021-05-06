---
aliases:
- /head/quickstart-index.html
- /HEAD/quickstart-index.html
- /quickstart-index.html
date: '2020-04-07T12:00:00Z'
menu: []
tags:
- quickstart
title: Getting started developing CorDapps
---


# Getting started developing CorDapps



Getting started with Corda will walk you through the process of setting up a development environment, deploying an example CorDapp, and building your own CorDapp based on the example.


* [Setting up a development environment](#setting-up-a-development-environment)
* [Deploying an example CorDapp](./quickstart-deploy.html)
* [Building your own CorDapp](./quickstart-build.html)


## Setting up a development environment


### Prerequisites


* **Java 8 JDK** - We require at least version 8u171, but do not currently support Java 9 or higher.
* **IntelliJ IDEA** - IntelliJ is an IDE that offers strong support for Kotlin and Java development. We support versions **2017.x**, **2018.x** and **2019.x** (with Kotlin plugin version 1.2.71).
* **Git** - We use Git to host our sample CorDapp and provide version control.


### Step One: Downloading a sample project


* Open a command prompt or terminal.
* Clone the CorDapp example repo by running: `git clone https://github.com/corda/samples`
* Move into the `cordapp-example` folder by running: `cd samples/cordapp-example`
* Checkout the corresponding branch by running: `git checkout release-V4` in the current directory.


### Step Two: Creating an IntelliJ project


* Open IntelliJ. From the splash screen, click **Open**, navigate to and select the `cordapp-example` folder, and click **Ok**. This creates an IntelliJ project to work from.
* Click **File** >  **Project Structure**. To set the project SDK click **New…** > **JDK**, and navigating to the installation directory of your JDK. Click **Apply**.
* Select **Modules** > **+** > **Import Module**. Select the `cordapp-example` folder and click **Open**. Select **Import module from external model** > **Gradle** > **Next** > tick the **Use auto-import** checkbox > **Finish** > **Ok**. Gradle will now download all the project dependencies and perform some indexing.

Your CorDapp development environment is now complete.


## Next steps

Now that you’ve successfully set up your CorDapp development environment, we’ll cover deploying an example CorDapp locally, before writing a CorDapp from scratch.
