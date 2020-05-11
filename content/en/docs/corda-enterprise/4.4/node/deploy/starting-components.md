---
aliases:
- /releases/4.4/node/deploy/starting-components.html
- /docs/corda-enterprise/head/node/deploy/starting-components.html
- /docs/corda-enterprise/node/deploy/starting-components.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-corda-nodes-deploying
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

`/usr/bin/java -Xmx1024m -jar /opt/corda/corda-firewall-4.1.jar --config-file float.conf`

You should see the following output:

```shell
FloatSupervisorService: active = false
FloatSupervisorService: active = true
```


## Starting the Corda Node

To start the Node run the following command from the Node VM:

`/usr/bin/java -Xmx2048m -jar /opt/corda/corda-4.1.jar --config-file node.conf`


## Starting the Bridge

To start the Bridge run the following command from the Bridge VM:

`/usr/bin/java -Xmx1024m -jar /opt/corda/corda-firewall-4.1.jar`

You should see the following output in the Bridge:

```shell
BridgeSupervisorService: active = false
BridgeSupervisorService: active = true
```


You should see the following output in the Float log:

```shell
Now listening for incoming connections on VM-Of-Float-Public-IP:Port
```
