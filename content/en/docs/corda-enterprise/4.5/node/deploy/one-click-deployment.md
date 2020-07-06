---
date: '2020-06-12T12:00:00Z'
menu:
  corda-enterprise-4-5:
    identifier: one-click-corda-deployment
    name: "One-click Corda deployment"
    parent: corda-enterprise-4-5-corda-nodes
tags:
- env
- dev

title: One-click Corda deployment
weight: 65
---


# One-click Corda deployment

This document describes how Corda nodes and networks can be deployed in one click in an Azure environment.

There are three options that can be found on the Azure Marketplace:

* **CENM Deployment**: A CENM instance is deployed onto a newly-created Azure Kubernetes Service cluster.
* **Nodes Onto An Existing Network**: Corda Enterprise Nodes are deployed onto a newly-created Azure Kubernetes Service cluster that connects to an existing Corda network.
* **Corda One Click**: A CEMN instance is deployed onto a newly-created Azure Kubernetes Service cluster and then nodes running a custom CorDapp are deployed.

{{< note >}}The nodes deployed using these templates are not production-ready. In particular, they use H2 as their database, which is not a supported configuration, as per the [Platform Support Matrix](../../platform-support-matrix.md#node-databases). In addition, they are not configured to use hardware security modules or Corda Enterprise Firewall instances, and are not deployed in high-availability mode. {{< /note >}}

{{< note >}}Corda Enterprise may be used for evaluation purposes for 90 days pursuant to the [Software Evaluation License Agreement](https://www.r3.com/corda-enterprise-evaluation-license). Any use beyond this (for example in production deployments) requires a commercial licence. Please contact <sales@r3.com> for more information. {{< /note >}}

## Prerequisites

To deploy the node and its CorDapps on Azure, you need the following.

1. An Azure account
2. A Resource Group

   This will be the location your cluster and deployment coordinators are deployed to.

   Due to a service restriction on the Azure side, this resource group must be located in East US.
3. A Service Principal with contributor rights for your resource group.

   In particular, you will need a **Service Principal Client Id**, a **Service Principal Tenant**, and a **Service Principal Client Secret**. Contact your subscription owner for more detail.

## Generating CorDapp images with Gradle

1. Add the following lines to your CorDapp `build.gradle` file.

   ```gradle
   task buildDockerFile(type: net.corda.plugins.DockerImage) {
      baseImage "<DESIRED CORDA BASE IMAGE>"
      cordaJars project.files(project(":workflows").jar, project(":contracts").jar, jar)
      dockerImageTag "<docker registry name>/<image name>:<version>"
      trustRootStoreFile project.file("network-root-truststore.jks")
   }
   ```

   Where
   * `baseImage`: the Docker base image of the version of Corda you are using
   * `cordaJars`: the `.jar` files to be included in this image
   * `dockerImageTag`: the tag that will be used for the image; this is optional
   * `TrustRootStoreFile`: the trust root store file; this is optional and
   only needed if you are connecting your node to an external CENM network

2. Run the command `gradlew buildDockerFile` and the plugin will build your image locally for you.

3. Upload the Docker image to your private repo on Azure. The repo should be in the same resource group that will be used for deployment.

   ```bash
   docker push <azure registry>/<image name>:<version>
   ```

## Deploying CENM from Azure

1. Open your Azure CENM Deployment Template in Deploy Mode.

2. Select appropriate **Subscription** and **Resource Group**.

3. Enter a value for **Cluster Name**.

4. Enter values for **Service Principal Client Id**, **Service Principal Tenant**, and **Service Principal Client Secret**.

5. Enter a value for **Deloyment Name**.

6. Enter values for **Artifactory Username** and **Artifactory Password**.

7. Set **ACCEPT_LICENSE** to `YES`.

8. Select the terms and conditions checkbox.

9. Click **Purchase** and wait while the cluster and containers deploy. This can take around 20 minutes.

10. Return to the resource group. The resouce group should now contain a cluster (Kubernetes service) with the cluster name you set and a delpoyment (container instances) with the deployment name you set.

11. Click the the container group with the name deployment name. In this example it is `cenm`.

    {{< figure src="../../resources/resource-group.png" width="1168px" >}}

12. In the left-hand column, click **Containers**

    {{< figure src="../../resources/containers.png" width="350px" >}}

13. Here you should see a single container called **cenm-deployer**. Click **cenm-deployer** and then click **Logs**. From here you can monitor the deployment of your CENM instance.

Once the deployer has finished deploying CENM, it will display the `Network_Map` URL and the `Doorman` URL. These can be added to a `node.conf` for a Corda Node to allow you to start using your CENM instance.

## Deploying a Corda Node onto an existing CENM Network

To deploy a Corda Node into an existing CENM network, you will need a copy of the root trust store for that network. For more details, see [How to join your network](../../../../cenm/1.2/deployment-kubernetes.md#how-to-join-your-network).

1. Copy the trust root store into your CorDapp project root.
2. Add the `trustRootStoreFile` parameter to the `buildDockerFile` task, as described in [Generating CorDapp images with Gradle](#generating-cordapp-images-with-gradle).
3. Generate the image and push it to your private Azure repository.
4. Open the “Node to External Network” template in a deploy mode and fill out the required fields.

   a. For Network Map and Doorman URLs, use the URLs found in the logs of the CENM deployment.

   b.  The trust root password used by test environments is `trust-store-password`.
5. Once finished, you can find the `node-deployer` job inside of the container group with the deployment name.

## Deploying CENM and Corda Nodes at the same time

1. Open your Azure One Click Deployment Template in Deploy Mode.

1. Select the appropriate **Subscription** and **Resource Group**.

1. Enter a value for **Cluster Name**.

1. Enter values for **Service Principal Client Id**, **Service Principal Tenant**, and **Service Principal Client Secret**.

1. Enter the address for the **Cordapp Image**.

1. Enter a value for **Deloyment Name**.

1. Enter an email address in the **EMAIL** field.

1. Set **ACCEPT_LICENSE** to `YES`.

1. Select the terms and conditions checkbox.

1. Click **Purchase** and wait while the cluster and containers deploy. This can take around 20 minutes.

1. Return to the resource group. The resouce group should now contain a cluster (Kubernetes service) with the cluster name you set and a deployment (container instances) with the deployment name you set.

1. Click the the container group with the name deployment name.

1. In the left hand column click **Containers**

1. Here you should see two containers, `cenm-deployer` and `node-deployer`

`node-deployer` will wait for `cenm-deployer` to complete its deployment before deploying the Corda Nodes.

## Interacting with the deployed nodes

Once `node-deployer` has completed, it will display the RPC address and port and the command to connect to it over SSH.

The RPC password for these test environments is always `test`.
