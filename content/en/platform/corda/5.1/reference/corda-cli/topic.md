---
date: '2023-08-10'
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-cordacli-topic
    weight: 5000
    parent: corda51-cli-reference
section_menu: corda51
title: "topic"
---
# topic
This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `topic` arguments. You can use these commands to manually create or delete topics in {{< tooltip >}}Kafka{{< /tooltip >}}, as described in the [Manual Bootstrapping]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md" >}}) section.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument | Description                                                                                                                                                       |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -b, \-\-bootstrap-server                | The address of the bootstrap server.                                                                                                                              |
| -k, \-\-kafka-config                    | The path to the Kafka configuration file.                                                                                                                         |
| -n, \-\-name-prefix                     | The name prefix for topics.                                                                                                                                       |
| -r                                      | The number of replicas.                                                                                                                                           |
| -p                                      | The number of partitions.                                                                                                                                         |
| connect                                 | Connects to the specified server; see [Topic Creation by Direct Connection]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#topic-creation-by-direct-connection" >}}) |
| -f                                      | The name of the script file genrated; see [Topic Creation by Scripting]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#topic-creation-by-scripting" >}}).            |
| -c                                      | The number of topics to create in parallel; see [Topic Creation by Scripting]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#topic-creation-by-scripting" >}}).      |
| create                                  | Creates Kafka topics; see [create](#create).                                                                                                                      |
| delete                                  | Deletes Kafka topics; see [delete](#delete).                                                                                                                      |

## create

{{< tabs name="create-topics">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{< /tabs >}}

## delete

{{< tabs name="delete-topics">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k client.properties delete connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k client.properties delete connect
```
{{% /tab %}}
{{< /tabs >}}
