---
description: "Learn how the Network Operator can update the current group parameters using the REST API. New group parameters are then signed by the MGM and distributed within the network."
date: '2023-10-05'
title: "Updating Group Parameters"
menu:
  corda52:
    identifier: corda52-networks-update-group-params
    parent: corda52-networks-manage
    weight: 4000
---
# Updating Group Parameters

The {{< tooltip >}}MGM{{< /tooltip >}} can update the current group parameters using the REST {{< tooltip >}}API{{< /tooltip >}}. Updates to the current group parameters can only include changes to the minimum platform version and custom properties. To update the group parameters, the MGM must submit an updated version of the group parameters to the REST endpoint, which overwrites any previous properties submitted using the endpoint.

To view the current group parameters use the <a href="../../reference/rest-api/openapi.html#tag/Member-Lookup-API/operation/get_members__holdingidentityshorthash__group_parameters"> GET method of the `/api/v5_2/members/{holdingidentityshorthash}/group-parameters` endpoint</a>:

{{< tabs >}}
{{% tab name="Bash"%}}

```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/members/$HOLDING_ID/group-parameters
```

{{% /tab %}}
{{% tab name="PowerShell" %}}

```shell
 Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/membership/$HOLDING_ID/group-parameters" | ConvertTo-Json -Depth 4
```
{{% /tab %}}
{{< /tabs >}}

To submit a group parameters update, use the <a href="../../reference/rest-api/openapi.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__group_parameters"> POST method of the `/api/v5_2/mgm/{holdingidentityshorthash}/group-parameters` endpoint</a>, as shown below. Keys of custom properties must have the prefix `ext.`. For the minimum platform version, use the key `corda.minimum.platform.version`. For example:

{{< tabs >}}
{{% tab name="Bash"%}}

```shell
export GROUP_PARAMS_UPDATE='{"newGroupParameters":{"corda.minimum.platform.version": "50000", "ext.group.key.0": "value0", "ext.group.key.1": "value1"}}'
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d "GROUP_PARAMS_UPDATE" $REST_API_URL/mgm/$HOLDING_ID/group-parameters
```

{{% /tab %}}
{{% tab name="PowerShell" %}}

```shell
GROUP_PARAMS_UPDATE = @{
  'corda.minimum.platform.version' = "50000"
  'ext.group.key.0' = "value0"
  'ext.group.key.1' = "value1"
}
$GROUP_PARAMS_UPDATE_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/mgm/$HOLDING_ID/group-parameters" -Body (ConvertTo-Json -Depth 4 @{
    newGroupParameters = $GROUP_PARAMS_UPDATE
})
$GROUP_PARAMS_UPDATE_RESPONSE.parameters
```
{{% /tab %}}
{{< /tabs >}}

These submitted parameters are combined with notary information from Corda to construct the new group parameters, which are then signed by the MGM and distributed within the network.

{{< note >}}
Custom properties have a character limit of 128 for keys and 800 for values. A maximum of 100 key-value pairs can be defined in a registration context.
{{< /note >}}
