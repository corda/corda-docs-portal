---
aliases:
- /head/building-corda.html
- /HEAD/building-corda.html
- /building-corda.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-building-corda
    parent: corda-os-4-6-contributing-index
    weight: 1030
tags:
- building
- corda
title: Building Corda
---


# Building Corda

These instructions are for downloading and building the Corda code locally. If you only wish to develop CorDapps for
use on Corda, you don’t need to do this, follow the instructions at [Getting set up for CorDapp development](getting-set-up.md) and use the precompiled binaries.


## Windows


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
* Download and run the executable to install Git (use the default installation values) and make a note of the installation directory.
* Open a new command prompt and type `git --version` to test that Git is installed correctly


### Building Corda


* Open a command prompt
* Run `git clone https://github.com/corda/corda.git`
* Run `gradlew build`


## Debian/Ubuntu Linux

These instructions were tested on Ubuntu Server 18.04 LTS. This distribution includes `git` and `python` so only the following steps are required:


### Java


* Run `sudo add-apt-repository ppa:webupd8team/java` from the terminal. Press ENTER when prompted.
* Run `sudo apt-get update`
* Then run `sudo apt-get install oracle-java8-installer`. Press Y when prompted and agree to the licence terms.
* Run `java --version` to verify that java is installed correctly


### Building Corda


* Open the terminal
* Run `git clone https://github.com/corda/corda.git`
* Run `./gradlew build`

