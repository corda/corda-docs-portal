---
aliases:
- /releases/release-V4.3/running-a-node.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-3:
    identifier: corda-os-4-3-running-a-node
    parent: corda-os-4-3-corda-nodes-index
    weight: 1140
tags:
- running
- node
title: Running nodes locally
---


# Running nodes locally


{{< note >}}
You should already have generated your node(s) with their CorDapps installed by following the instructions in
[Creating nodes locally](generating-a-node.md).

{{< /note >}}
There are several ways to run a Corda node locally for testing purposes.


## Starting a Corda node using DemoBench

See the instructions in [DemoBench](demobench.md).



## Starting a Corda node from the command line

Run a node by opening a terminal window in the node’s folder and running:

```shell
java -jar corda.jar
```

By default, the node will look for a configuration file called `node.conf` and a CorDapps folder called `cordapps`
in the current working directory. You can override the configuration file and workspace paths on the command line (e.g.
`./corda.jar --config-file=test.conf --base-directory=/opt/corda/nodes/test`).

Optionally run the node’s webserver as well by opening a terminal window in the node’s folder and running:

```shell
java -jar corda-webserver.jar
```


{{< warning >}}
The node webserver is for testing purposes only and will be removed soon.

{{< /warning >}}




### Setting JVM arguments

There are several ways of setting JVM arguments for the node process (particularly the garbage collector and the memory settings).
They are listed here in order of increasing priority, i.e. if the same flag is set in a way later in this list, it will override
anything set earlier.


* **Default arguments in capsule**: 
The capsuled Corda node has default flags set to `-Xmx512m -XX:+UseG1GC` - this gives the node (a relatively
low) 512 MB of heap space and turns on the G1 garbage collector, ensuring low pause times for garbage collection.


* **Node configuration**: 
The node configuration file can specify custom default JVM arguments by adding a section like:

```none
custom = {
   jvmArgs: [ "-Xmx1G", "-XX:+UseG1GC" ]
}
```

Note that this will completely replace any defaults set by capsule above, not just the flags that are set here, so if you use this
to set e.g. the memory, you also need to set the garbage collector, or it will revert to whatever default your JVM is using.


* **Capsule specific system property**: 
You can use a special system property that Capsule understands to set JVM arguments only for the Corda
process, not the launcher that actually starts it:

```kotlin
java -Dcapsule.jvm.args="-Xmx:1G" corda.jar
```

Setting a property like this will override any value for this property, but not interfere with any other JVM arguments that are configured
in any way mentioned above. In this example, it would reset the maximum heap memory to `-Xmx1G` but not touch the garbage collector settings.
This is particarly useful for either setting large memory allowances that you don’t want to give to the launcher or for setting values that
can only be set on one process at a time, e.g. a debug port.


* **Command line flag**: 
You can set JVM args on the command line that apply to the launcher process and the node process as in the example
above. This will override any value for the same flag set any other way, but will leave any other JVM arguments alone.


* **OutOfMemoryError handling**: 
In addition to the JVM arguments listed above, the capsuled Corda node has two flags that cause the node to stop
on out-of-memory error and generate the corresponding diagnostic files:

```kotlin
-XX:+HeapDumpOnOutOfMemoryError -XX:+CrashOnOutOfMemoryError
```

With `CrashOnOutOfMemoryError` the node which is running out of memory is expected to stop immediately (fail-fast) to preserve ledger
consistency and avoid flaws in operations.

Unlike for arguments related to memory and GC, to completely replace the default out-of-memory error args, you must explicitly add
at least one out-of-memory error related argument into the `custom.jvmArgs` section. For example, the following config turns off
`HeapDumpOnOutOfMemoryError` and doesn’t invoke `CrashOnOutOfMemoryError` option:

```none
custom = {
   jvmArgs: [ "-Xmx1G", "-XX:+UseG1GC", "-XX:-HeapDumpOnOutOfMemoryError" ]
}
```




## Starting all nodes at once on a local machine from the command line



### Native

If you created your nodes using `deployNodes`, a `runnodes` shell script (or batch file on Windows) will have been
generated to allow you to quickly start up all nodes and their webservers. `runnodes` should only be used for testing
purposes.

Start the nodes with `runnodes` by running the following command from the root of the project:


* Linux/macOS: `build/nodes/runnodes`
* Windows: `call build\nodes\runnodes.bat`


{{< warning >}}
On macOS, do not click/change focus until all the node terminal windows have opened, or some processes may
fail to start.

{{< /warning >}}


If you receive an `OutOfMemoryError` exception when interacting with the nodes, you need to increase the amount of
Java heap memory available to them, which you can do when running them individually. See
[Starting a Corda node from the command line](#starting-an-individual-corda-node).


### docker-compose

If you created your nodes using `Dockerform`, the `docker-compose.yml` file and corresponding `Dockerfile` for
nodes has been created and configured appropriately. Navigate to `build/nodes` directory and run `docker-compose up`
command. This will startup nodes inside new, internal network.
After the nodes are started up, you can use `docker ps` command to see how the ports are mapped.


{{< warning >}}
You need both `Docker` and `docker-compose` installed and enabled to use this method. Docker CE
(Community Edition) is enough. Please refer to [Docker CE documentation](https://www.docker.com/community-edition)
and [Docker Compose documentation](https://docs.docker.com/compose/install/) for installation instructions for all
major operating systems.

{{< /warning >}}



## Starting all nodes at once on a remote machine from the command line

By default, `Cordform` expects the nodes it generates to be run on the same machine where they were generated.
In order to run the nodes remotely, the nodes can be deployed locally and then copied to a remote server.
If after copying the nodes to the remote machine you encounter errors related to `localhost` resolution, you will additionally need to follow the steps below.

To create nodes locally and run on a remote machine perform the following steps:


* Configure Cordform task and deploy the nodes locally as described in [Creating nodes locally](generating-a-node.md).
* Copy the generated directory structure to a remote machine using e.g. Secure Copy.
* Optionally, bootstrap the network on the remote machine.This is optional step when a remote machine doesn’t accept `localhost` addresses, or the generated nodes are configured to run on another host’s IP address.If required change host addresses in top level configuration files `[NODE NAME]_node.conf` for entries `p2pAddress` , `rpcSettings.address` and  `rpcSettings.adminAddress`.Run the network bootstrapper tool to regenerate the nodes network map (see for more explanation [Network Bootstrapper](network-bootstrapper.md)):`java -jar corda-tools-network-bootstrapper-Master.jar --dir <nodes-root-dir>`
* Run nodes on the remote machine using [runnodes command](#starting-all-nodes-at-once).

The above steps create a test deployment as `deployNodes` Gradle task would do on a local machine.


## Stability of the Corda Node

There are a number of critical resources necessary for Corda Node to operate to ensure transactional consistency of the ledger.
These critical resources include:


* Connection to a database;
* Connection to Artemis Broker for P2P communication;
* Connection to Artemis Broker for RPC communication.

Should any of those critical resources become not available, Corda Node will be getting into an unstable state and as a safety precaution it will
shut itself down reporting the cause as an error message to the Node’s log file.

{{< note >}}
On some operating systems when PC is going to sleep whilst Corda Node is running, imbedded into Node Artemis message broker reports
the loss of heartbeat event which in turn causes loss of connectivity to Artemis. In such circumstances Corda Node will exit reporting broker
connectivity problem in the log.

{{< /note >}}
Once critical resources node relies upon are available again, it is safe for Node operator to re-start the node for normal operation.

