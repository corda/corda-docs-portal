---
date: '2023-05-16'
version: 'Corda 5.0 Beta 4'
title: "Dynamic Configuration"
menu:
  corda5:
    identifier: corda5-cluster-dynamic
    parent: corda5-cluster-config
    weight: 1000
section_menu: corda5
---

# Dynamic Configuration


## Setting Configuration Fields Dynamically

You can set the fields in a configuration section by sending the values as JSON to the <a href="../../reference/rest-api/C5_OpenAPI.html#tag/Configuration-API/operation/put_config">`config` endpoint</a> of the REST API. The PUT method of `/api/v1/config` requires the following parameters:
* `section` — the configuration section that the JSON updates. See the [Configuration Fields page]({{< relref "./fields/_index.md" >}}) for a list of the configuration sections.
* `version` — the version of the configuration. Corda versions configurations to avoid two concurrent updates clashing with each other. You can [retrieve]({{< relref "#retrieving-current-configuration-values">}}) the current version, with the current configuration structure, using the GET method of the `/api/v1/config` endpoint.
* `config` — the configuration fields and values specified as JSON. For more information about these fields, see [Configuration Fields]({{< relref "./fields/_index.md">}}).
* `schemaVersion` — the configuration schema version. Set this to `{"major": 1, "minor": 0}` for this version of Corda.

For example, to set fields in the [messaging]({{< relref "./fields/messaging.md" >}}) section using Bash with Curl or PowerShell:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"section":"corda.messaging", "version":"1", "config":"{"maxAllowedMessageSize":972800,"publisher":{"closeTimeout":600,"transactional":true},"subscription":{"commitRetries":3,"pollTimeout":500,"processorRetries":3,"processorTimeout":15000,"subscribeRetries":3,"threadStopTimeout":10000}}", "schemaVersion": {"major": 1, "minor": 0}}' "$REST_API_URL/config"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f ${REST_API_USER}:${REST_API_PASSWORD})} -Method Put -Uri "$REST_API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
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

## Retrieving Current Configuration Values

You can retrieve the current values of the fields in a particular configuration section by using the GET method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Configuration-API/operation/get_config__section_">`/api/v1/config` endpoint</a>.

For example, to retrieve the fields in the [messaging]({{< relref "./fields/messaging.md" >}}) section using Bash with Curl or PowerShell:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/config/corda.messaging
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f ${REST_API_USER}:${REST_API_PASSWORD})} -Uri "$REST_API_URL/config/corda.messaging"
   ```
   {{% /tab %}}
   {{< /tabs >}}

The GET method of the `/api/v1/config` endpoint returns the current values of the specified configuration section in JSON.