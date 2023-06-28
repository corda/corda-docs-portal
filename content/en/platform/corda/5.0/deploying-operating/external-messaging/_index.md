---
date: '2023-06-28'
title: "Configuring External Messaging"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-cluster-external-messaging
    parent: corda5-cluster
    weight: 10000
section_menu: corda5
---

# Configuring External Messaging

CorDapp flows can send simple messages via Kafka to external systems. This section de

## Route Configuration

The <a href="../config/fields/externalMessaging.html">`externalMessaging` configuration section</a> specifies how Corda creates the required messaging routes when [creating a new virtual node]({{< relref "../../application-networks/creating/members/cpi.md">}}). 
To update these values using Bash with Curl or PowerShell:

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