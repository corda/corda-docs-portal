---
description: "Learn how the Network Operator can use the MGM admin API to decline an in-progress registration request that may be stuck or displaying some other unexpected behavior."
date: '2023-10-05'
title: "Declining In-Progress Registrations"
menu:
  corda52:
    identifier: corda52-networks-decline-registration
    parent: corda52-networks-manage
    weight: 3000
---
# Declining In-Progress Registrations

As the Network Operator, you can use the MGM admin API to decline an in-progress registration request that may be stuck or displaying some other unexpected behavior.

{{< note >}}
Only use this endpoint under exceptional circumstances.
{{< /note >}}

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
REQUEST_ID=<REQUEST ID>
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/mgmadmin/$MGM_HOLDING_ID/force-decline/$REQUEST_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REQUEST_ID = <REQUEST ID>
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/mgmadmin/$MGM_HOLDING_ID/force-decline/$REQUEST_ID" -Method POST
```
{{% /tab %}}
{{< /tabs >}}
