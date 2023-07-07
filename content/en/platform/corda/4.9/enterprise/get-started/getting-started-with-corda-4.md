---
title: Getting started
date: '2023-01-27'

menu:
  corda-enterprise-4-9:
    identifier: get-started-landing-4-9
    name: "Getting started"
tags:
- started
- enterprise

weight: -1
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

2. Familiarize yourself with the [Corda key concepts]({{< relref "../../enterprise/about-corda/corda-key-concepts.md" >}}). 
3. Run a [sample CorDapp]({{< relref "../cordapps/tutorial-cordapp.md" >}}) to see Corda in action. 
4. [Build your own CorDapp]({{< relref "../cordapps/cordapp-build-systems.md" >}}) from scratch.

You can then take your Corda integration to the next level by deep-diving into specific topics in our [Corda Enterprise]({{< relref "../../enterprise/_index.md" >}}) documentation. You can also view the [API reference material](../../../../../api-ref.html), browse [featured apps]({{< relref "../apps/apps-index.md" >}}), or browse [tools and add-ons]({{< relref "../../../../../tools/_index.md" >}}).

{{< note >}}
<b>Read Corda white papers</b>
* The [introductory white paper](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/) describes Corda’s mission and philosophy. It’s suitable for a business audience.
* The [technical white paper](https://www.r3.com/white-papers/corda-technical-whitepaper/) describes the architecture and protocol.
{{< /note >}}

## Getting started with Corda Enterprise Network Manager (CENM) 1.5

Before you deploy [CENM]({{< relref "../../../../corda/1.5/cenm/_index.md" >}}), read about [Corda networks]({{< relref "../../../../corda/1.5/cenm/corda-networks.md" >}}) and the [components of CENM]({{< relref "../../../../corda/1.5/cenm/enm-components.md" >}}). For instructions on deploying:
* CENM with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts]({{< relref "../../../..//corda/1.5/cenm/deployment-kubernetes.md" >}}).
* CENM with Amazon Web Services (AWS), see [CENM Deployment on AWS]({{< relref "../../../../corda/1.5/cenm/aws-deployment-guide.md" >}}).
* CENM services as a test environment, see the [CENM test environment quick start guide]({{< relref "../../../../corda/1.5/cenm/quick-start.md" >}}).

