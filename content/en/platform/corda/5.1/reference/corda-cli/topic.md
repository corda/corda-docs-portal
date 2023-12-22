---
description: "List of topic commands for the Corda 5.1 CLI. You can use these commands to manually create topics in Kafka."
date: '2022-12-20'
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
This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `topic` sub-commands and arguments. You can use these commands to manually create topics in {{< tooltip >}}Kafka{{< /tooltip >}}, as described in the [Manual Bootstrapping]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#kafka" >}}) section.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument                 | Description                                               |
| ------------------------ | --------------------------------------------------------- |
| -b, \-\-bootstrap-server | The address of the bootstrap server.                      |
| -k, \-\-kafka-config     | The path to the Kafka configuration file.                 |
| -n, \-\-name-prefix      | The name prefix for topics.                               |
| create                   | Creates the required Kafka topics; see [create](#create). |

## create

The following table lists the `create` sub-commands and arguments:

| Argument           | Description                                                                                                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| -r, \-\-replicas   | The number of replicas.                                                                                                                                                              |
| -p, \-\-partitions | The number of partitions.                                                                                                                                                            |
| -t, \-\-tag        | One or more tags associated with topics and their respective number of partitions. For example:<br> `-t t01=partitions:3 -t t02=partitions:599999`         |
| -u, \-\-user       | One or more Corda workers and their respective Kafka users. For example:<br> `-u crypto=Charlie -u rest=Rob99999`<br> For more information, see [Create the Default Topics]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.mdd#creating-acl-entries" >}}). |
| connect            | Connects to the specified server to create the default topics; see [Create the Default Topics]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#create-the-default-topics" >}}). |
| preview            | Generates a preview of the required Kafka topic configuration in YAML; see [preview](#preview).                                                                                      |

## connect

The following table lists the `connect` arguments:

| Argument     | Description                                                                                                                                                                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| -f, \-\-file | The name of the configuration file to create the topics; see [Modify the Topic Configuration Before Creating]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#modify-the-topic-configuration-before-creating" >}}). |

{{< tabs name="create-topics">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{< /tabs >}}

## preview

{{< tabs name="">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> preview
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> preview
```
{{% /tab %}}
{{< /tabs >}}
