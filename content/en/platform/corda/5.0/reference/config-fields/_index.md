---
title: "Configuration Fields"
project: corda
version: 'Corda 5.0'
date: 2023-04-24
menu:
  corda5:
    parent: corda5-references
    identifier: corda5-config-fields
    weight: 1000
section_menu: corda5
---

This section lists the fields of each Corda configuration section:
{{< childpages >}}
Set the fields in a section by sending the configuration fields as JSON to the [config endpoint](../../rest-api/C5_OpenAPI.html#tag/Configuration-API/operation/put_config) of the REST API.

For example, if the REST API is exposed on `localhost`, to set fields in the [messaging]({{< relref "./messaging.md" >}}) section using Bash with Curl or PowerShell:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"section":"corda.messaging", "version":"1", "config":"{"maxAllowedMessageSize":972800,"publisher":{"closeTimeout":600,"transactional":true},"subscription":{"commitRetries":3,"pollTimeout":500,"processorRetries":3,"processorTimeout":15000,"subscribeRetries":3,"threadStopTimeout":10000}}", "schemaVersion": {"major": 1, "minor": 0}}' "https://localhost:8888/api/v1/config"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method Put -Uri "https://localhost:8888/api/v1/config" -Body (ConvertTo-Json -Depth 4 @{
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