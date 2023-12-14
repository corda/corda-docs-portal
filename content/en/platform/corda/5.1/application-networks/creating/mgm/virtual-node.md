---
date: '2023-04-07'
version: 'Corda 5.1'
title: "Create a Virtual Node for the MGM"
menu:
  corda51:
    parent: corda51-networks-mgm
    identifier: corda51-networks-mgm-virtual-node
    weight: 2000
    name: "Create a Virtual Node"
section_menu: corda51
---

# Create a Virtual Node for the MGM

You can create a virtual node using the POST method of the [/api/v5_1/virtualnode endpoint](../../../reference/rest-api/openapi.html#tag/Virtual-Node-API/operation/post_virtualnode). The following sections describe how to use this method:
* [Create a Virtual Node on Linux or macOS](#create-a-virtual-node-on-linux-or-macos)
* [Create a Virtual Node on Windows](#create-a-virtual-node-on-windows)

## Create a Virtual Node on Linux or macOS

To create a virtual node for the {{< tooltip >}}MGM{{< /tooltip >}} on Linux or macOS, run the following commands in Bash to send the request using Curl, changing the {{< tooltip >}}X.500{{< /tooltip >}} name and using the checksum retrieved when you [uploaded the MGM CPI]({{< relref"./cpi.md#upload-the-cpi" >}}):

```shell
export CPI_CHECKSUM=<CPI-checksum>
export X500_NAME="C=GB, L=London, O=MGM"
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d '{ "request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "'$X500_NAME'"}}' $REST_API_URL/virtualnode
```

You can use the `requestId` from the response to check that the virtual node was created successfully. Run the following, replacing `<request-ID>` with the ID received:

```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/virtualnode/status/<request-ID>
```

Once the operation is complete, this request returns a JSON object with `status` set to `SUCCEEDED`. You may have to call the `/virtualnode/status` endpoint multiple times until you receive the `SUCCEEDED` status. Once complete, to save the ID of the virtual node for future use, run the following command, replacing `<resource-ID>` with the ID returned in the received response:

```shell
export MGM_HOLDING_ID = <resource-ID>
```

## Create a Virtual Node on Windows

To create a virtual node for the MGM on Windows, run the following commands in PowerShell, changing the X.500 name. The command uses the checksum of the CPI from the response saved when you [uploaded the MGM CPI]({{< relref"./cpi.md#upload-the-cpi" >}}).

```shell
$X500_NAME = "C=GB, L=London, O=Alice"
$VIRTUAL_NODE_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/virtualnode" -Method Post -Body (ConvertTo-Json @{
    request = @{
       cpiFileChecksum = $CPI_STATUS_RESPONSE.cpiFileChecksum
       x500Name = $X500_NAME
    }
})
```

You can use the `requestId` from the response to check that the virtual node was created successfully by running the following:

```shell
$VIRTUAL_NODE_RESPONSE_STATUS = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/virtualnode/status/$($VIRTUAL_NODE_RESPONSE.requestId)" -Method Get
```

Once the operation is complete, this request returns a JSON object with `status` set to `SUCCEEDED`. You may have to call the `/virtualnode/status` endpoint multiple times until you receive the `SUCCEEDED` status. Once complete, to save the ID of the virtual node for future use, run the following command:

```shell
$HOLDING_ID = $VIRTUAL_NODE_RESPONSE_STATUS.resourceId
```