---
date: '2020-04-07T12:00:00Z'
menu:
  versions:
    weight: -650
  corda-community-4-9:
    weight: 1
    name: Corda Community Edition 4.9
project: corda
section_menu: corda-community-4-9
title: Corda Community Edition 4.9
version: 'Community 4.9'
---

# Corda Community Edition

Corda Community Edition is a free to use, open source version of Corda, with added optional support. By choosing to develop using this edition of Corda, you can access affordable technical support to help you take your project to market with confidence.

{{< vimeo 205410473 >}}

## What's new in Corda Community Edition

Along with the free-to-use Corda platform, Corda Community Edition comes with an affordable support package from R3, the makers of Corda. Check the [Community Edition support services](http://r3.com/support) to see which flexible package suits you best.

## Set up Corda Community Edition in three steps

To start using Corda Community Edition if you have never used Corda before:

1. Install the required software:
    * Java 8 JDK
    * IntelliJ IDEA
    * Git
    * Gradle

For help finding these, use the [setup guide](community/getting-set-up.md).

2. Clone the CorDapp samples repository. CorDapps are applications that run on a Corda network. Run the appropriate command:

* Java: `git clone http://github.com/corda/samples-java`
* Kotlin: `git clone http://github.com/corda/samples-kotlin`

3. Follow the [tutorials](community/tutorial-cordapp.md) to set up a Corda network and start coding your CorDapps.

## Upgrade to Corda Community Edition from Corda Open Source

If you are already using an open source version of Corda (Corda 4.1–Corda 4.8) and want to upgrade to Corda Community Edition, you can choose to:

* Download the `.tar` [file](https://download.corda.net/corda-community-edition/4.9/community-4.9.tar).
* Use the Docker image available on [Docker Hub](https://hub.docker.com/repository/docker/corda/community).

Follow the upgrade guides to make sure your [node](community/node-upgrade-notes.md) and [CorDapps](community/upgrading-cordapps.md) are upgraded correctly.
