---
date: '2023-04-07'
version: 'Corda 5.0'
title: "Create a Virtual Node"
menu:
  corda5:
    parent: corda5-networks-mgm
    identifier: corda5-networks-mgm-virtual-node
    weight: 2000
section_menu: corda5
---

# Create a Virtual Node

To create a virtual node for the MGM, run the following, using the checksum retrieved when you [uploaded the MGM CPI]({{< relref"./cpi.md#upload-the-cpi" >}}):

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export CPI_CHECKSUM=<CPI-checksum>
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -d '{ "request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "C=GB, L=London, O=MGM"}}' $REST_API_URL/virtualnode
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$VIRTUAL_NODE_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/virtualnode" -Method Post -Body (ConvertTo-Json @{
    request = @{
       cpiFileChecksum = $CPI_STATUS_RESPONSE.cpiFileChecksum
       x500Name = "C=GB, L=London, O=MGM"
    }
})

$MGM_HOLDING_ID = $VIRTUAL_NODE_RESPONSE.holdingIdentity.shortHash
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, run the following, replacing `<holding-identity-ID>` with the ID returned in `holdingIdentity.shortHash` (for example, `58B6030FABDD`).
```
export MGM_HOLDING_ID=<holding-identity-ID>
```