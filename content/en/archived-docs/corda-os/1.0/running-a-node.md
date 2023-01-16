---
aliases:
- /releases/release-V1.0/running-a-node.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-1-0:
    identifier: corda-os-1-0-running-a-node
    parent: corda-os-1-0-corda-nodes-index
    weight: 1020
tags:
- running
- node
title: Running a node
---


# Running a node


## Starting your node

After following the steps in [Deploying a node](deploying-a-node.md), you should have deployed your node(s) with any chosen CorDapps
already installed. You run each node by navigating to `<node_dir>` in a terminal window and running:

```shell
java -jar corda.jar
```


{{< warning >}}
If your working directory is not `<node_dir>` your plugins and configuration will not be used.

{{< /warning >}}


The configuration file and workspace paths can be overridden on the command line. For example:

`./corda.jar --config-file=test.conf --base-directory=/opt/r3corda/nodes/test`.

Otherwise the workspace folder for the node is the current working path.


## Debugging your node

To enable remote debugging of the node, run the following from the terminal window:

`java -Dcapsule.jvm.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005" -jar corda.jar`

This command line will start the debugger on port 5005 and pause the process awaiting debugger attachment.

