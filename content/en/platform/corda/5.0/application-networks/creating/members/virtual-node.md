---
date: '2023-04-13'
title: "Create a Virtual Node"
menu:
  corda-5:
    identifier: corda-5-networks-members-node
    parent: corda-5-networks-members
    weight: 2000
section_menu: corda-5
---

To create a virtual node for a member, run the following commands, changing the X.500 name:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export CPI_CHECKSUM=<CPI-checksum>
export X500_NAME="C=GB, L=London, O=Alice"
curl -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "'$X500_NAME'"}}' $API_URL/virtualnode
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$X500_NAME = "C=GB, L=London, O=Alice"
$VIRTUAL_NODE_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/virtualnode" -Method Post -Body (ConvertTo-Json @{
    request = @{
       cpiFileChecksum = $CPI_STATUS_RESPONSE.cpiFileChecksum
       x500Name = $X500_NAME
    }
})

$HOLDING_ID = $VIRTUAL_NODE_RESPONSE.holdingIdentity.shortHash
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, run the following, replacing `<holding identity ID>` with the ID returned in `holdingIdentity.shortHash` (for example, `58B6030FABDD`).
```bash
export HOLDING_ID=<holding-identity-ID>
```