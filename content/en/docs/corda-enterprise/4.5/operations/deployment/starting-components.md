---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    identifier: corda-enterprise-4-5-operations-guide-deployment-node-starting
    parent: corda-enterprise-4-5-operations-guide-deployment-node
tags:
- starting
- components
title: Starting a Corda node
weight: 6
---


# Starting a Corda node

The components to be started in a deployment are:


* Float
* Node
* Bridge

{{< note >}}
The `corda-firewall.jar` is used by both Bridge and Float. The JAR file  assumes the input is `bridge.conf` however this may be overridden with the `--config-file` parameter so you can designate whatever config file name you wish to use.

{{< /note >}}

## Starting the Float

To start the Float run the following command from the Float VM:

`/usr/bin/java -Xmx1024m -jar /opt/corda/corda-firewall-4.5.jar --config-file float.conf`

You should see the following output:

```shell
FloatSupervisorService: active = false
FloatSupervisorService: active = true
```


## Starting the Corda Node

To start the Node run the following command from the Node VM:

`/usr/bin/java -Xmx2048m -jar /opt/corda/corda-4.5.jar --config-file node.conf`

{{< note >}}
If your node configuration file is obfuscated and you want to deobfuscate it when running the node, you need to pass the obfuscation seed and passphrase to the node in the node run command.

To do so using the [Configuration Obfuscator](../../tools-config-obfuscation.md) command-line tool, use the `--config-obfuscation-seed` and `--config-obfuscation-passphrase` flags, respectively, in your node run command.

The following example shows how to pass a seed and a passphrase explicitly to a node component using the Configuration Obfuscator command-line tool:

```bash
$ /usr/bin/java -Xmx2048m -jar /opt/corda/corda-4.5.jar --config-file node.conf --config-obfuscation-seed my-seed --config-obfuscation-passphrase my-passphrase

```

To pass the seed and passphrase to a node using environment variables, follow the example below:

```bash
$ export CONFIG_OBFUSCATION_SEED=my-seed; export CONFIG_OBFUSCATION_PASSPHRASE=my-passphrase; /usr/bin/java -Xmx2048m -jar /opt/corda/corda-4.5.jar --config-file node.conf
```
{{< /note >}}


## Starting the Bridge

To start the Bridge run the following command from the Bridge VM:

`/usr/bin/java -Xmx1024m -jar /opt/corda/corda-firewall-4.5.jar`

You should see the following output in the Bridge:

```shell
BridgeSupervisorService: active = false
BridgeSupervisorService: active = true
```


You should see the following output in the Float log:

```shell
Now listening for incoming connections on VM-Of-Float-Public-IP:Port
```


