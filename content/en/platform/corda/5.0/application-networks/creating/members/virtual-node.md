---
date: '2023-04-13'
title: "Create a Virtual Node"
menu:
  corda5:
    identifier: corda5-networks-members-node
    parent: corda5-networks-members
    weight: 2000
section_menu: corda5
---

You can create a virtual node using the POST method of the [/api/v1/virtualnode endpoint](../../../reference/rest-api/C5_OpenAPI.html#tag/Virtual-Node-API/operation/post_virtualnode). The following sections describe how to use this method:
* [Create a Virtual Node on Linux or macOS](#create-a-virtual-node-on-linux-or-macos)
* [Create a Virtual Node on Windows](#create-a-virtual-node-on-linux-or-windows)

## Create a Virtual Node on Linux or macOS

To create a virtual node for a member on Linux or macOS, run the following commands in Bash to send the request using Curl, changing the X.500 name and using the checksum retrieved when you [uploaded the member CPI]({{< relref"./cpi.md#upload-the-cpi" >}}):

```shell
export CPI_CHECKSUM=<CPI-checksum>
export X500_NAME="C=GB, L=London, O=Alice"
curl -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "'$X500_NAME'"}}' $API_URL/virtualnode
```

If successful, this request returns the details of the new virtual node as JSON. To save the ID of the virtual node for future use, run the following command, replacing `<holding-identity-ID>` with the ID returned in `holdingIdentity.shortHash` in the received response. For example, `58B6030FABDD`.

```shell
export MGM_HOLDING_ID=<holding-identity-ID>
```

## Create a Virtual Node on Windows

To create a virtual node for a member on Windows, run the following commands in PowerShell, changing the X.500 name. The command uses the checksum of the CPI from the repsonse saved when you [uploaded the member CPI]({{< relref"./cpi.md#upload-the-cpi" >}}):

```shell
$X500_NAME = "C=GB, L=London, O=Alice"
$VIRTUAL_NODE_RESPONSE = Invoke-RestMethod -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/virtualnode" -Method Post -Body (ConvertTo-Json @{
    request = @{
       cpiFileChecksum = $CPI_STATUS_RESPONSE.cpiFileChecksum
       x500Name = $X500_NAME
    }
})

$HOLDING_ID = $VIRTUAL_NODE_RESPONSE.holdingIdentity.shortHash
```