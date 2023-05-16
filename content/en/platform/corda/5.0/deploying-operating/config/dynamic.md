---
date: '2023-05-12'
title: "Dynamic Configuration"
menu:
  corda5:
    identifier: corda5-cluster-dynamic
    parent: corda5-cluster-config
    weight: 1000
section_menu: corda5
---

You can set the fields in a section by sending the configuration fields as JSON to the <a href="../../reference/rest-api/C5_OpenAPI.html#tag/Configuration-API/operation/put_config">`config` endpoint</a> of the REST API. The PUT method of `/api/v1/config` requires the following parameters:
* `section` — the configuration section that the JSON updates. 
* `version` — the version of the configuration. Corda versions configurations to avoid two concurrent updates clashing with each other. You can retrieve the current version, along with the current configuration structure, using the GET method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Configuration-API/operation/get_config__section_">`/api/v1/config` endpoint</a>.
* `config` — the configuration fields and values specified as JSON. For more information about these fields, see [Configuration Fields]({{< relref "./fields/_index.md">}}).
* `schemaVersion` — the configuration schema version. Set this to `{"major": 1, "minor": 0}` for this version of Corda.

For example, if the REST API is exposed on `localhost`, to set fields in the [messaging]({{< relref "./fields/messaging.md" >}}) section using Bash with Curl or PowerShell:

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
