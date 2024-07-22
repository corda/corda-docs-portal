---
description: "Learn how Cluster Administrators configure a Corda Enterprise cluster for CorDapps that implement external messaging."
date: '2023-06-28'
title: "External Messaging Administration"
menu:
  corda53:
    identifier: corda53-cluster-external-messaging
    parent: corda53-cluster
    weight: 10000
---

# External Messaging Administration {{< enterprise-icon >}}

{{< tooltip >}}CorDapp{{< /tooltip >}} flows can send simple messages via {{< tooltip >}}Kafka{{< /tooltip >}} to external systems. For more information, see [External Messaging CorDapps]({{< relref "../../developing-applications/external-messaging.md" >}}). This section describes the cluster administration tasks required for CorDapps that implement external messaging. It contains the following:

* [Configuring External Messaging Routes](#configuring-external-messaging-routes)
* [Creating Kafka Topics](#creating-kafka-topics)

## Configuring External Messaging Routes

The <a href="./config/fields/externalmessaging.html">`externalMessaging` configuration section</a> specifies how Corda creates the required messaging routes when [creating a new virtual node]({{< relref "../../application-networks/creating/members/cpi.md">}}).
You can update these using the <a href="../reference/rest-api/openapi.html#tag/Configuration/operation/put_config">`config` endpoint</a> of the REST API. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"section":"corda.externalMessaging", "version":"1", "config":"{"routeDefaults": {"active": false,"inactiveResponseType": "IGNORE","receiveTopicPattern": "ext.$HOLDING_ID.$CHANNEL_NAME.receive"}", "schemaVersion": {"major": 1, "minor": 0}}' "$REST_API_URL/config"
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f ${REST_API_USER}:${REST_API_PASSWORD})} -Method Put -Uri "$REST_API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
section = "corda.messaging"
version = 1
{
    "config": "{
        "routeDefaults": {
            "active": false,
            "inactiveResponseType": "IGNORE",
            "receiveTopicPattern": "ext.$HOLDING_ID.$CHANNEL_NAME.receive"
        }",
    "schemaVersion": {
        "major": 1,
        "minor": 0
    },
    "section": "corda.messaging",
    "version": 1
})
```
{{% /tab %}}
{{< /tabs >}}

## Creating Kafka Topics

Corda does not create Kafka topics used for external messaging. You must manually create a Kafka topic for each active and current route created for a {{< tooltip >}}virtual node{{< /tooltip >}}. To determine the required topics and create these topics, do the following:

1. Retrieve the configuration of the virtual node. For more information, see [Retrieving Virtual Nodes]({{< relref "../vnodes/retrieving.md" >}}).
   If a CorDapp that implements external messaging is uploaded to a virtual node, the routes configuration is included in the response. For example:
   ```json
   {
     "virtualNodes": [
       {
         ...
         "externalMessagingRouteConfiguration": {
           "currentRoutes": {
             "cpiIdentifier": {
               "name": "upgrade-testing-cordapp_ea6732c2-183a-4158-a9f0-7fe1084e8ee9",
               "version": "v1",
               "signerSummaryHash": "SHA-256:E53DA5C67A637D42335808FA1534005281BAE7E49CCE8833213E58E0FDCA8B35"
             },
             "routes": [
               {
                 "channelName": "external_app_v1",
                 "externalReceiveTopicName": "ext.B5C16DBC7BB5.external_app_v1.receive",
                 "active": true,
                 "inactiveResponseType": "ERROR"
               }
             ]
           },
           "previousVersionRoutes": []
         }
       }
     ]
   }
   ```
   The `externalMessagingRouteConfiguration` field contains the configuration for the routes that were generated for each channel. The `currentRoutes` field specifies the current configuration while the `previousVersionRoutes` field contains historical configuration. The `previousVersionRoutes` field shows how the configuration has evolved over time, which can be useful when troubleshooting issues.

2. Manually create a Kafka topic for each route returned in `externalMessagingRouteConfiguration.currentRoutes.routes`. In the example above, create a topic named `ext.B5C16DBC7BB5.external_app_v1.receive`. For more information, see the [Manual Bootstrapping]({{< relref "../deployment/deploying/manual-bootstrapping.md">}}) section.

3. Listen to the Kafka topic for messages using the `kafka-console-consumer` command. Log in to the pod or container that is running Kafka and execute the following:
   ```shell
   kafka-console-consumer --topic <topic-nam> --from-beginning --bootstrap-server localhost:9092
   ```
   To test that everything is working correctly, start the {{< tooltip >}}flow{{< /tooltip >}} that sends external messages. For more information, see the <a href="../reference/rest-api/openapi.html#tag/Flow-Management/operation/post_flow__holdingidentityshorthash_">REST API documentation of the `flow` endpoint</a>.
