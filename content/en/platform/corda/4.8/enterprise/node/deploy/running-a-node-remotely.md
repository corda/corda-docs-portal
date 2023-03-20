---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-corda-nodes-deploying
tags:
- running
- node
title: Running nodes remotely
weight: 6
---

# Running nodes remotely

{{< note >}}
The remote node running method described in this page is designed for testing use. For production-grade deployments visit the [node deployments page]({{< relref "../../../../../../../en/platform/corda/4.8/enterprise/node-docker-deployments.md" >}}).
{{< /note >}}

By default, a [Cordform](generating-a-node-cordform.md) task will run all the generated nodes on the same host machine.
In order to run the nodes remotely, you can deploy them locally and then copy them to a remote server.
If after copying the nodes to the remote machine you encounter errors related to a `localhost` resolution, you should follow the additional steps below.

To create nodes locally and run on a remote machine, perform the following steps:

* Configure a Cordform task and deploy the nodes locally as described in [Creating nodes locally](generating-a-node.md) and [Cordform](generating-a-node-cordform.md) pages.
* Copy the generated directory structure to a remote machine, for example using Secure Copy.
* Optionally, add database configuration settings if they could not be configured in the first step and the local machine does not have access to the remote database.
  * In each top-level `[NODE NAME]_node.conf` configuration file, add the database settings and copy the JDBC driver JAR file (if required).
  * Edit the top-level `[NODE NAME]_node.conf` files only and not the files inside the node sub-directories (for example, `node.conf`).
* Optionally, bootstrap the network on the remote machine. This is an optional step when a remote machine does not accept `localhost` addresses, or if the generated nodes are configured to run on another host’s IP address. If needed, change the host addresses in the top-level configuration files `[NODE NAME]_node.conf` for entries `p2pAddress`, `rpcSettings.address`, and  `rpcSettings.adminAddress`. Run the network bootstrapper tool to regenerate the nodes network map: `java -jar corda-tools-network-bootstrapper-Master.jar --dir <nodes-root-dir>`. For more information, see [Network bootstrapper](network-bootstrapper.md).
* Run nodes on the remote machine using the `runnodes` command.

The steps described above enable you to create the same test deployment as a `deployNodes` Gradle task would create on a local machine.
