---
date: '2020-07-15T12:00:00Z'
menu:
  get-started:
    identifier: get-started-corda-4
    name: Getting started with Corda 4
title: Getting started with Corda 4
weight: 400
---

# Getting started with Corda 4

The best way to get started with Corda is to:
1. Decide whether you need to use:
   * **Corda Enterprise** - the enterprise version of Corda, for which you require a commercial contract with R3. Corda Enterprise is accessed via R3's customer hub. If you are an existing Corda Enterprise customer, you can find all downloads on [R3 Customer Hub](https://customerhub.r3.com/s/).

     If you are new to Corda and would like to experience Corda Enterprise, you can [register for a trial now](https://www.corda.net/get-corda/).
   * **Corda Community Edition** - the open source version of Corda, which you can build on now. To use Corda Community Edition, you can access the latest version in one of three ways:
     * Clone the [Github repository](https://github.com/corda/corda), then follow the tutorials to set up your nodes and developer environment.
     * Download the latest Corda Community Edition `.tar` [file](https://download.corda.net/corda-community-edition/4.10/community-4.10.tar) that contains the required Corda `.jars`. 
     * Use the Docker image and accompanying guide from the [Docker Hub](https://hub.docker.com/repository/docker/corda/community).

2. Familiarize yourself with the [Corda key concepts](./corda-key-concepts.md). 
3. Run a [sample CorDapp](../../en/platform/corda/4.10/community/tutorial-cordapp.md) to see Corda in action.
4. [Build your own CorDapp](../../en/tutorials/corda/4.10/community/build-basic-cordapp/basic-cordapp-intro.md) from scratch.

You can then take your Corda integration to the next level by deep-diving into specific topics in our [Corda Community Edition](../../en/platform/corda/4.10/community.html) documentation, or [Corda Enterprise](../../en/platform/corda/4.10/enterprise.html) documentation. You can also view the [API reference material](../../en/api-ref.html), browse [featured apps](../../en/apps.html), or browse [tools and add-ons](../../en/tools.html).

{{< note >}}
<b>Read Corda white papers</b>
* The [introductory white paper](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/) describes Corda’s mission and philosophy. It’s suitable for a business audience.
* The [technical white paper](https://www.r3.com/white-papers/corda-technical-whitepaper/) describes the architecture and protocol.
{{< /note >}}

## Getting started with Corda Enterprise Network Manager (CENM) 1.5

Before you deploy [CENM](../../en/platform/corda/1.5/cenm.html), read about [Corda networks](../../en/platform/corda/1.5/cenm/corda-networks.md) and the [components of CENM](../../en/platform/corda/1.5/cenm/enm-components.md). For instructions on deploying:
* CENM with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts](../../en/platform/corda/1.5/cenm/deployment-kubernetes.md).
* CENM with Amazon Web Services (AWS), see [CENM Deployment on AWS](../../en/platform/corda/1.5/cenm/aws-deployment-guide.md).
* CENM services as a test environment, see the [CENM test environment quick start guide](../../en/platform/corda/1.5/cenm/quick-start.md).
