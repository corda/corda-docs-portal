---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-deploying
tags:
- running
- node
title: Running nodes locally
weight: 5
---


# Running nodes locally


{{< note >}}
You should already have generated your node(s) with their CorDapps installed by following the instructions in
[Creating nodes locally](generating-a-node.md).
{{< /note >}}

There are several ways to run a Corda node locally for testing purposes.


## Starting a Corda node using DemoBench

See the instructions in [Demobench](../../demobench.md).

{{< warning >}}
**DemoBench** is deprecated in Corda 4.6 and Corda Enterprise 4.6.
{{< /warning >}}

## Starting a Corda node from the command prompt

You can run a node by opening a terminal / command prompt window in the node’s directory and running the following command:

```shell
java -jar corda.jar
```

By default, the node will look for a configuration file called `node.conf` and a CorDapps folder called `cordapps`
in the current working directory. You can override the configuration file and workspace paths on the command line (e.g.
`./corda.jar --config-file=test.conf --base-directory=/opt/corda/nodes/test`).

If you need to initialise or migrate the node's database schema objects, you need to run the `run-migration-scripts` sub-command. See [Node command-line options](../node-commandline.md/) for details.

{{< note >}}
If your node configuration file is obfuscated and you want to deobfuscate it when running the node, you need to pass the
obfuscation seed and passphrase to the node in the node run command.

To do so using the [Configuration Obfuscator](../../tools-config-obfuscator.md/) command-line tool, use the
`--config-obfuscation-seed` and `--config-obfuscation-passphrase` flags, respectively, in your node run command.

The following example shows how to pass a seed and a passphrase explicitly to a node component using the Configuration
Obfuscator command-line tool:

```bash
$ java -jar corda.jar --config-obfuscation-seed my-seed --config-obfuscation-passphrase my-passphrase

```

To pass the seed and passphrase to a node using environment variables, follow the example below:

```bash
$ export CONFIG_OBFUSCATION_SEED=my-seed; export CONFIG_OBFUSCATION_PASSPHRASE=my-passphrase; java -jar corda.jar
```
{{< /note >}}


### Setting JVM arguments

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




### Command-line options

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
* `--pause-all-flows`: Paused all flows when the node starts up. Starting a node with the `--pause-all-flows` command-line option automatically enables flow draining mode but does not modify the node's configuration file. See [Pause and resume flows](../../flow-pause-and-resume.md#starting-the-node-and-pausing-all-flows) for more information.
* `--allow-hibernate-to-manage-app-schema`: enable this option to make the node manage app schemas automatically using Hibernate
with H2 in dev mode.

#### Sub-commands

`clear-network-cache`: Clears the local copy of the network map - it will be restored from the server or the file system on node start-up.

`initial-registration`: Starts an initial node registration with the compatibility zone to obtain a certificate from the Identity Manager Service (formerly Doorman).

{{< warning >}}

**Important note about running the initial node registration command**

In Corda 4.6, database schemas are no longer initialised/migrated automatically by running any command at the first run of the node - typically at the initial node registration. This is now done explicitly by running `run-migration-scripts`, so no other commands during the first node run would initialise/migrate the database schema.

The exception to that is the `--initial-registration` command, which embeds `run-migration-scripts` and therefore runs the database migration scripts by default.

So if you are using deployment automation you may need to adjust your scripts accordingly and exclude the database initialisation/migration task from the initial node registration command. To do so, use the `--skip-schema-creation` flag alongside the `--initial-registration` command.


{{< /warning >}}

Parameters:

* `--network-root-truststore`, `-t` **required**: Network root trust store obtained from the network operator.
* `--network-root-truststore-password`, `-p`: Network root trust store password obtained from the network operator.
* `--skip-schema-creation`: Skips the default database migration step.

`run-migration-scripts`: from version 4.6, a Corda node can no longer modify/create schema on the fly in normal run mode - schema setup or changes must be
applied deliberately using this sub-command. It runs the database migration script for the requested schema set defined in the following parameters. Once it creates or modifies the schema(s), the sub-command will exit.

Parameters:

* `--core-schemas`: use to run the core database migration script for the node database. Core schemas cannot be migrated while there are checkpoints.
* `--app-schemas`: use to run the app database migration script for CorDapps. To force an app schema to migrate with checkpoints present, use the `--update-app-schema-with-checkpoints` flag alongside the `run-migration-scripts` sub-command.

`generate-node-info`: Performs the node start-up tasks necessary to generate the `node.info` file, saves it to disk, then exits.

`generate-rpc-ssl-settings`: Generates the SSL keystore and truststore for a secure RPC connection.

`install-shell-extensions`: Installs a `corda` alias and auto completion for `bash` and `zsh`. For more information, see [Shell extensions for CLI Applications](../operating/cli-application-shell-extensions.md).

`validate-configuration`: Validates the actual configuration without starting the node.


### Enabling remote debugging

To enable remote debugging of the node, run the node with the following JVM arguments:

`java -Dcapsule.jvm.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005" -jar corda.jar`

This will allow you to attach a debugger to your node on port 5005.


## Starting a node with JMX monitoring enabled

To enable export of JMX metrics over HTTP via [Jolokia](https://jolokia.org/), run the following command in the command prompt:

`java -Dcapsule.jvm.args="-javaagent:drivers/jolokia-jvm-1.3.7-agent.jar=port=7005" -jar corda.jar`

This command will start the node with JMX metrics accessible via HTTP on port 7005.

See [Monitoring via Jolokia](../operating/node-administration.md#monitoring-jolokia) for further details.


## Starting all nodes at once on a local machine from the command prompt


### Native

If you created your nodes using `deployNodes`, a `runnodes` shell script (or batch file on Windows) will have been
generated to allow you to quickly start up all nodes and their webservers. You should only use `runnodes` for testing
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

If you created your nodes using [Dockerform](generating-a-node.md), the `docker-compose.yml` file has been created and configured appropriately. Navigate to `build/nodes` directory and run the `docker-compose up` command. This will start up nodes inside a new, internal network. After the nodes are started, you can use the `docker ps` command to see how the ports are mapped.

{{< warning >}}
You need both `Docker` and `docker-compose` installed and enabled to use this method. Docker CE
(Community Edition) is sufficient. Please refer to [Docker CE documentation](https://www.docker.com/community-edition)
and [Docker Compose documentation](https://docs.docker.com/compose/install/) for installation instructions for all
major operating systems.
{{< /warning >}}

{{< note >}}
Before running any Corda Enterprise Docker images, you must accept the license agreement and indicate that you have done this by setting the environment variable `ACCEPT_LICENSE` to `YES` or `Y` on your machine. If you do not do this, none of the Docker containers will start.

As an alternative, you can specify this parameter when running the `docker-compose up` command, for example:
`ACCEPT_LICENSE=Y docker-compose up`
{{< /note >}}

## Starting all nodes at once on a remote machine from the command line

By default, a [Cordform](generating-a-node.md) task will run all the generated nodes on the same host machine.
In order to run the nodes remotely, you can deploy them locally and then copy them to a remote server.
If after copying the nodes to the remote machine you encounter errors related to a `localhost` resolution, you should follow the additional steps below.

To create nodes locally and run on a remote machine, perform the following steps:

* Configure a Cordform task and deploy the nodes locally as described in [Creating nodes locally](generating-a-node.md).
* Copy the generated directory structure to a remote machine, for example using Secure Copy.
* Optionally, add database configuration settings if they could not be configured in the first step and the local machine does not have access to the remote database.
In each top-level `[NODE NAME]_node.conf` configuration file, add the database settings and copy the JDBC driver `.jar` file (if required).
Edit the top-level `[NODE NAME]_node.conf` files only and not the files inside the node sub-directories (for example, `node.conf`).
* Optionally, bootstrap the network on the remote machine. This is an optional step when a remote machine does not accept `localhost` addresses, or if the generated nodes are configured to run on another host’s IP address. If needed, change the host addresses in the top-level configuration files `[NODE NAME]_node.conf` for entries `p2pAddress`, `rpcSettings.address`, and  `rpcSettings.adminAddress`. Run the network bootstrapper tool to regenerate the nodes network map: `java -jar corda-tools-network-bootstrapper-Master.jar --dir <nodes-root-dir>`. For more information, see [Network bootstrapper](../../network-bootstrapper.md).
* Run nodes on the remote machine using [runnodes command](#starting-all-nodes-at-once).

The steps described above enable you to create the same test deployment as a `deployNodes` Gradle task would create on a local machine.


## Database migrations

Depending on the versions of Corda and of the CorDapps used, database migration scripts might need to run before a node is able to start.
For more information, see [Database management](../../node-database-intro.md).

If you need to initialise or migrate the node's database schema objects, you need to run the `run-migration-scripts` sub-command. See [Node command-line options](../node-commandline.md) for details.


## Stability of the Corda Node

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
