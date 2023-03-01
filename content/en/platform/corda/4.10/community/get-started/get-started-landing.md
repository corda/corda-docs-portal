---
title: Getting started
date: '2023-01-27'

menu:
  corda-community-4-10:
    identifier: get-started-landing-4-10-community
    name: "Getting started"
tags:
- started
- community

weight: -1
---

## Setting up Corda Community Edition

To start using Corda Community Edition if you have never used Corda before:

1. Install the required software:
   * Java 8 JDK
   * IntelliJ IDEA
   * Git
   * Gradle

   For help finding these, use the [setup guide]({{< relref "../../community/getting-set-up.md" >}}).

2. Clone the CorDapp samples repository. CorDapps are applications that run on a Corda network. Run the appropriate command:

  * Java: `git clone http://github.com/corda/samples-java`
  * Kotlin: `git clone http://github.com/corda/samples-kotlin`

3. Follow the [tutorials](community/tutorial-cordapp.md) to set up a Corda network and start coding your CorDapps.

## Upgrading to Corda Community Edition from Corda Open Source

If you are already using an open source version of Corda (Corda 4.1–Corda 4.9) and want to upgrade to Corda Community Edition, you can choose to:

* Download the `.tar` [file](https://download.corda.net/corda-community-edition/4.10/community-4.10.tar).
* Download the `.zip` [file](https://download.corda.net/corda-community-edition/4.10/community-4.10.zip)
* Use the Docker image available on [Docker Hub](https://hub.docker.com/repository/docker/corda/community).

Follow the upgrade guides to make sure your [node](../../community/node-upgrade-notes.md) and [CorDapps](../../community/upgrading-cordapps.md) are upgraded correctly.

## Next steps

1. Familiarize yourself with the [Corda key concepts](../about-corda/corda-key-concepts.md). 
2. Run a [sample CorDapp](../../community/tutorial-cordapp.md) to see Corda in action.
4. [Build your own CorDapp](../../community/building-a-cordapp-index.md) from scratch. /

You can then take your Corda integration to the next level by deep-diving into specific topics in our [Corda Community Edition](../../community.html) documentation. You can also view the [API reference material](../../../../../../en/api-ref.html), browse [featured apps](../apps/apps-index.md), or browse [tools and add-ons](../../../../../../en/tools.html).

{{< note >}}
<b>Read Corda white papers</b>
* The [introductory white paper](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/) describes Corda’s mission and philosophy. It’s suitable for a business audience.
* The [technical white paper](https://www.r3.com/white-papers/corda-technical-whitepaper/) describes the architecture and protocol.
{{< /note >}}
