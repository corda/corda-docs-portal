---
date: '2023-03-08'
title: "Configuration Fields"
menu:
  corda-5-beta:
    identifier: corda-5-beta-config-fields
    parent: corda-5-beta-operate
    weight: 4000
section_menu: corda-5-beta
---
This section lists the fields of each Corda configuration section. Set the fields in a section by sending the configuration fields as JSON to the [config endpoint](../../rest-api/C5_OpenAPI.html#tag/Configuration-API/operation/put_config) of the REST API.

For example, to set fields in the [messaging](messaging.md) section:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u <username>:<password> -X PUT -d '{"section":"corda.messaging", "version":"1", "config":"{"maxAllowedMessageSize":972800,"publisher":{"closeTimeout":600,"transactional":true},"subscription":{"commitRetries":3,"pollTimeout":500,"processorRetries":3,"processorTimeout":15000,"subscribeRetries":3,"threadStopTimeout":10000}}", "schemaVersion": {"major": 1, "minor": 0}}' "https://localhost:8888/api/v1/config"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f <username>:<password>)} -Method Put -Uri "https://localhost:8888/api/v1/config" -Body (ConvertTo-Json -Depth 4 @{
    section = "corda.messaging"
    version = 1
    {
     "config": "{
        "maxAllowedMessageSize":972800,
        "publisher":{
           "closeTimeout":600,
           "transactional":true
        },
        "subscription":{
           "commitRetries":3,
           "pollTimeout":500,
           "processorRetries":3,
           "processorTimeout":15000,
           "subscribeRetries":3,
           "threadStopTimeout":10000
        }
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

{{< note >}}
The `db` configuration section is passed when starting Corda and cannot be updated dynamically through the REST endpoint.
{{< /note >}}
