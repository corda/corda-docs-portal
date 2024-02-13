---
description: "Learn how to "
title: "Rotating Wrapping Keys"
date: '2024-02-12'
menu:
  corda52:
    identifier: corda52-cluster-wrapping-rotation
    parent: corda52-cluster-wrapping-keys
    weight: 2000
---

# Rotating Wrapping Keys

R3 recommend changing the wrapping keys frequently to limit the probability of a compromised key being in use.
Corda supports the following key rotation:

{{< toc >}}

## Rotating Master Wrapping Key

Because the master key is not managed by Corda, you must first change the key in the source system. Corda must then re-encrypt all of the keys that were wrapped with the old master key.
To rotate the master wrapping key, do the following:

1. Add the new key to the source environment. For more information, see [Configuring the Master Wrapping Key]({{ relref "./master.md" >}}).
2. Add the new key to the `corda.crypto` configuration section, setting it as the default key. The [Setting Configuration Fields Dynamically]({{< relref "../config/dynamic.md#setting-configuration-fields-dynamically" >}}) section describes how to update configuration values. For example, to specify *:

  {{< tabs >}}
  {{% tab name="Bash"%}}
  ```shell
  curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"section":"corda.crypto", "version":"1", "config":"{"maxAllowedMessageSize":972800,"publisher":{"closeTimeout":600,"transactional":true},"subscription":{"commitRetries":3,"pollTimeout":500,"processorRetries":3,"processorTimeout":15000,"subscribeRetries":3,"threadStopTimeout":10000}}", "schemaVersion": {"major": 1, "minor": 0}}' "$REST_API_URL/config"
  ```
  {{% /tab %}}
  {{% tab name="PowerShell" %}}
  ```shell
  Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f ${REST_API_USER}:${REST_API_PASSWORD})} -Method Put -Uri "$REST_API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
  {
    "config": "{
      "hsm":{
        "defaultWrappingKey": "master2"
        "wrappingKeys":[{
          "alias": ,
          "passphrase": , 
          "salt": 
        },
        {
          "alias": ,
          "passphrase": , 
          "salt": 
        }]
      }
    }",
    "schemaVersion": {
      "major": 1,
      "minor": 0
    },
    "section": "corda.crypto",
    "version": 1
  })
  ```
  {{% /tab %}}
  {{< /tabs >}}
3. Rotate the key using the POST method of the [/api/v5_2/wrappingkey/rotation/{tenantid} endpoint](../../../reference/rest-api/openapi.html#tag/Key-Rotation-API/operation/post_wrappingkey_rotation__tenantid_).

## Rotating Managed Wrapping Keys

