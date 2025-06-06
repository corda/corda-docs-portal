---
aliases:
- /head/running-a-node.html
- /HEAD/running-a-node.html
- /running-a-node.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-12:
    identifier: corda-community-4-12-running-a-node
    parent: corda-community-4-12-corda-nodes-index
    weight: 1140
tags:
- running
- node
title: Running nodes locally
---


# Running nodes locally

This page contains information on three methods for locally running nodes:

* Nodes can be run manually from a local machine.
* The [Dockerform]({{< relref "generating-a-node-dockerform.md" >}}) or [Cordform]({{< relref "generating-a-node-cordform.md" >}}) gradle plugins can also be used to run nodes locally.
* Running nodes remotely is also possible - find instructions on how to do this [here]({{< relref "running-a-node-remotely.md" >}}).

{{< note >}}
You should already have generated your node(s) with their CorDapps installed by following the instructions in
[Creating nodes locally]({{< relref "generating-a-node.md" >}}). For node operations using Docker, visit the [Docker deployments]({{< relref "node-docker-deployments.md" >}}) page.
{{< /note >}}

There are several ways to run a Corda node locally for testing purposes:

## Starting a Corda node from the command prompt

You can run a node by opening a terminal/command prompt window in the node’s directory and running the following command:

```shell
java -jar corda.jar
```

By default, the node will look for a configuration file called `node.conf` and a CorDapps folder called `cordapps`
in the current working directory. You can override the configuration file and workspace paths on the command line:

```shell
java -jar ./corda.jar --config-file=test.conf --base-directory=/opt/corda/nodes/test`).
````

If you need to initialise or migrate the node's database schema objects, you need to run the `run-migration-scripts` sub-command.
You may get an error message stating:

```shell
Incompatible database schema version detected, please run schema migration scripts
```
If this is the case, you will need to run the migration scripts.
One way of doing so is with
```shell
java -jar corda.jar run-migration-scripts --core-schemas --app-schemas`.
 ```

See [Node command-line options]({{< relref "node-commandline.md" >}}) for more options and further details.

## Setting JVM arguments

There are several ways to set JVM arguments for the node process (particularly the garbage collector and the memory settings).
They are listed here in order of increasing priority - if the same flag is set in a way mentioned later in the list below, it will override
anything set earlier.


* **Default arguments in capsule**:
  The capsuled Corda node has default flags set to `-Xmx512m -XX:+UseG1GC` - this gives the node a relatively
  low 512 MB of heap space, and turns on the G1 garbage collector, ensuring low pause times for garbage collection.

When `devMode` is explicitly set to `false`, the default node memory size will be enlarged to 4G: `-Xmx4G -XX:+UseG1GC`.


* **Node configuration**:
  The node configuration file can specify custom default JVM arguments by adding a section like the one below:

```none
custom = {
   jvmArgs: [ "-Xmx1G", "-XX:+UseG1GC" ]
}
```

{{< note >}}
This action completely replaces any capsuled Corda node default flags, not just the flags set here. So if you use this
to set, for example, the memory, you also need to set the garbage collector, or it will revert to whatever default value your JVM is using.
{{< /note >}}

* **Capsule specific system property**:
  You can use a special system property that Capsule understands, to set JVM arguments only for the Corda
  process, not the launcher that actually starts it:

```kotlin
java -Dcapsule.jvm.args="-Xmx1G" -jar corda.jar
```

Setting a property like this will override any value for this property, but not interfere with any other JVM arguments that are configured
in any way mentioned above. In this example, it resets the maximum heap memory to `-Xmx1G` but it does not touch the garbage collector settings.
This is particularly useful for either setting large memory allowances that you don’t want to give to the launcher, or for setting values that
can only be set on one process at a time - for example, a debug port.


* **Command line flag**:
  You can set JVM arguments in the command prompt that apply to the launcher process and the node process as in the example
  above. This overrides any value for the same flag set any other way, but leaves any other JVM arguments alone.


* **OutOfMemoryError handling**:
  In addition to the JVM arguments listed above, the capsuled Corda node has two flags that cause the node to stop
  on out-of-memory error and generate the corresponding diagnostic files:

```kotlin
-XX:+HeapDumpOnOutOfMemoryError -XX:+CrashOnOutOfMemoryError
```

With `CrashOnOutOfMemoryError` the node which is running out of memory is expected to stop immediately (fail-fast) to preserve ledger
consistency and avoid flaws in operations.

Unlike for arguments related to memory and GC, to completely replace the default out-of-memory error arguments, you must explicitly add
at least one out-of-memory error related argument into the `custom.jvmArgs` section. For example, the following configuration turns off
`HeapDumpOnOutOfMemoryError` and does not invoke the `CrashOnOutOfMemoryError` option:

```none
custom = {
   jvmArgs: [ "-Xmx1G", "-XX:+UseG1GC", "-XX:-HeapDumpOnOutOfMemoryError" ]
}
```

## Command-line options

You can optionally start a node using the following command-line options:


* `--base-directory`, `-b`: The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the configuration file. Defaults to `node.conf`.
* `--dev-mode`, `-d`: Runs the node in development mode. Unsafe in production. Defaults to `true` on MacOS and desktop versions of Windows, otherwise defaults to `false`.
* `--no-local-shell`, `-n`: Do not start the embedded shell locally.
* `--on-unknown-config-keys <[FAIL,INFO]>`: How to behave on unknown node configuration. Defaults to `FAIL`.
* `--sshd`: Enables SSH server for node administration.
* `--sshd-port`: Sets the port for the SSH server. If not supplied and SSH server is enabled, the port defaults to `2222`.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: `ERROR`, `WARN`, `INFO` (default), `DEBUG`, `TRACE`.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.


### Sub-commands

`clear-network-cache`: Clears the local copy of the network map - it will be restored from the server or the file system on node start-up.

`initial-registration`: Starts an initial node registration with the compatibility zone to obtain a certificate from the Identity Manager Service (formerly Doorman).

Parameters:


* `--network-root-truststore`, `-t` **required**: Network root trust store obtained from the network operator.
* `--network-root-truststore-password`, `-p`: Network root trust store password obtained from the network operator.

`generate-node-info`: Performs the node start-up tasks necessary to generate the `node.info` file, saves it to disk, then exits.

`generate-rpc-ssl-settings`: Generates the SSL keystore and truststore for a secure RPC connection.

`install-shell-extensions`: Installs a `corda` alias and auto-completion for `bash` and `zsh`. For more information, see [Shell extensions for CLI Applications]({{< relref "cli-application-shell-extensions.md" >}}).

`validate-configuration`: Validates the actual configuration without starting the node.


## Enabling remote debugging

To enable remote debugging of the node, run the node with the following JVM arguments:

`java -Dcapsule.jvm.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005" -jar corda.jar`

This will allow you to attach a debugger to your node on port 5005.


## Starting a node with JMX monitoring enabled

To enable export of JMX metrics over HTTP via [Jolokia](https://jolokia.org/), run the following command in the command prompt:

`java -Dcapsule.jvm.args="-javaagent:drivers/jolokia-jvm-1.3.7-agent.jar=port=7005" -jar corda.jar`

This command will start the node with JMX metrics accessible via HTTP on port 7005.

See [Monitoring via Jolokia]({{< relref "node-administration.md#monitoring-jolokia" >}}) for further details.

## Starting all nodes at once on a local machine from the command prompt

### Cordform

The [Cordform]({{< relref "generating-a-node-cordform.md" >}}) gradle plugin (as used by the `deployNodes` gradle task) generates a `runnodes` script. Executing this allows you to quickly start up all nodes. Only use `runnodes` for testing purposes.


Start the nodes with `runnodes` by running the following command from the root of the project:


* Linux/macOS: `build/nodes/runnodes`
* Windows: `call build\nodes\runnodes.bat`


{{< warning >}}
On macOS, do not click/change focus until all the node terminal windows have opened, or some processes may
fail to start.

{{< /warning >}}


If you receive an `OutOfMemoryError` exception when interacting with the nodes, you need to increase the amount of
Java heap memory available to them, which you can do when running them individually. See
[Starting a Corda node from the command line](#starting-a-corda-node-from-the-command-prompt).

### Dockerform

If you created your nodes using [Dockerform]({{< relref "generating-a-node-dockerform.md" >}}), a `docker-compose.yml` file has been created. You can use `docker-compose` to bring up a cluster of Corda nodes. See `prepareDockerNodes` in the [generating nodes locally]({{< relref "generating-a-node.md" >}}) for more information on this.
In order to start up the nodes in a new, internal network, go to the `build/nodes` directory and run the `docker-compose up` command. After the nodes are started, you can use the `docker ps` command to see how the ports are mapped.

{{< warning >}}
You need both `Docker` and `docker-compose` installed and enabled to use this method. Docker CE
(Community Edition) is sufficient. Please refer to [Docker CE documentation](https://www.docker.com/community-edition)
and [Docker Compose documentation](https://docs.docker.com/compose/install/) for installation instructions for all
major operating systems.
{{< /warning >}}

{{< note >}}
Before running any Corda Docker images, you must accept the license agreement and indicate that you have done this by setting the environment variable `ACCEPT_LICENSE` to `YES` or `Y` on your machine. If you do not do this, none of the Docker containers will start.

As an alternative, you can specify this parameter when running the `docker-compose up` command, for example:
`ACCEPT_LICENSE=Y docker-compose up`
{{< /note >}}

## Database migrations

Depending on the versions of Corda and of the CorDapps used, database migration scripts might need to run before a node is able to start.
For more information, see [Database management]({{< relref "node-database-access-h2.md" >}}).

From Corda 4.6, if you need to initialise or migrate the node's database schema objects, you need to run the `run-migration-scripts` sub-command. See [Node command-line options]({{< relref "node-commandline.md" >}}) for details.


## Stability of the Corda node

There are a number of critical resources that a Corda node needs to operate in order to ensure the transactional consistency of the ledger.
These critical resources include:

* Connection to a database.
* Connection to Artemis Broker for P2P communication.
* Connection to Artemis Broker for RPC communication.

Should any of those critical resources becomes unavailable, the Corda node will get into an unstable state and, as a safety precaution, it will
shut itself down, reporting the cause as an error message to its log file.

{{< note >}}
On some operating systems, if the machine switches to "sleep" mode while a Corda node is running, the message broker embedded in Node Artemis reports
the loss of a heartbeat event, which in turn causes a loss of connectivity to Artemis. In such circumstances, the Corda node will exit and will report a broker
connectivity problem in the log.

{{< /note >}}
Once all the critical resources the node relies on are available again, it is safe for the node operator to restart the node for normal operation.
