---
date: '2023-10-05'
title: "Decline In-Progress Registrations"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-networks-decline-registration
    parent: corda51-networks-manage
    weight: 3000
section_menu: corda51
---
# Decline In-Progress Registrations

As the Network Operator, you can use the MGM admin API to force decline an in-progress registration request that may be stuck or displaying
some other unexpected behaviour.

{{< note >}}
You should use this endpoint under exceptional circumstances.
{{< /note >}}

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
REQUEST_ID=<REQUEST ID>
curl --insecure -u admin:admin -X POST $API_URL/mgmadmin/$MGM_HOLDING_ID/force-decline/$REQUEST_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REQUEST_ID = <REQUEST ID>
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/mgmadmin/$MGM_HOLDING_ID/force-decline/$REQUEST_ID" -Method POST
```
{{% /tab %}}
{{< /tabs >}}
