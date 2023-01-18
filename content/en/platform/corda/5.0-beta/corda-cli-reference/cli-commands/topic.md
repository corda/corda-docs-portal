---
date: '2022-12-20'
menu:
  corda-5-beta:
    identifier: corda-5-beta-cordacli-topic
    weight: 5000
    parent: corda-5-cli-reference
section_menu: corda-5-beta
title: "topic"
---

This section lists the Corda CLI `topic` arguments. You can use these commands to manually create or delete topics in Kafka, as described in the [Manual Bootstrapping Tutorial](../../deploying/deployment-tutorials/manual.mdhtml).

| <div style="width:160px">Argument</div> | Description                                                                                                                                           |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| -b, \-\-bootstrap-server                | The address of the bootstrap server.                                                                                                                  |
| -k, \-\-kafka-config                    | The path to the Kafka configuration file.                                                                                                             |
| -n, \-\-name-prefix                     | The name prefix for topics.                                                                                                                           |
| -r                                      | The number of replicas.                                                                                                                               |
| -p                                      | The number of partitions.                                                                                                                             |
| connect                                | Connects to the specified server; see [Topic Creation by Direct Connection](../../deploying/deployment-tutorials/manual.html#topic-creation-by-direct-connection) |
| -f                                      | The name of the script file genrated; see [Topic Creation by Scripting](../../deploying/deployment-tutorials/manual.html#topic-creation-by-scripting).             |
| -c                                      | The number of topics to create in parallel; see [Topic Creation by Scripting](../../deploying/deployment-tutorials/manual.html#topic-creation-by-scripting).       |
| create                                  | Creates Kafka topics; see [create](#create).                                                                                                          |
| delete                                  | Deletes Kafka topics; see [delete](#delete).                                                                                                          |

## create

{{< tabs name="create-topics">}}
{{% tab name="Linux" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{% tab name="macOS" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <REPLICAS> -p <PARTITIONS> connect
   ```
{{% /tab %}}
{{% tab name="Windows" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{< /tabs >}}

## delete

{{< tabs name="delete-topics">}}
{{% tab name="Linux" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> delete connect
```
{{% /tab %}}
{{% tab name="macOS" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> delete connect
   ```
{{% /tab %}}
{{% tab name="Windows" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> delete connect
```
{{% /tab %}}
{{< /tabs >}}