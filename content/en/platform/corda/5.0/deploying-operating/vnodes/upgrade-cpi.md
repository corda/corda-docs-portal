---
date: '2023-06-12'
title: "Upgrading a CPI"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-cluster-nodes-upgrade
    parent: corda5-cluster-nodes
    weight: 3000
section_menu: corda5
---

# Upgrading a CPI

To upgrade a virtual node's CPI, use the the PUT method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Virtual-Node-API/operation/put_virtualnode__virtualnodeshortid__cpi__targetcpifilechecksum_">`api/v1/virtualnode/<virtualnodeshortid>/cpi/<targetcpifilechecksum>` endpoint </a>:

{{< note >}}
The target CPI should have the same name, signer summary hash, and MGM group ID as the existing CPI. You can check the values of the existing CPI using 
the <a href ="./retrieving.md">`/api/v1/virtualnode` endpoint </a>:
{{< /note >}}

To upgrade a CPI, do the following:

1. [Set the state of the virtual node to MAINTENANCE]({{< relref "./state.md">}}). 
2. Ensure no flows are running (that is, all flows have either “COMPLETED”, “FAILED” or “KILLED” status). You can check the list of running flows using <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Flow-Management-API/operation/get_flow__holdingidentityshorthash_">`GET /api/v1/flow/<holdingidentityshorthash>` </a>
3. Send the checksum of the CPI to upgrade to using the PUT method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Virtual-Node-API/operation/put_virtualnode__virtualnodeshortid__cpi__targetcpifilechecksum_">`api/v1/virtualnode/<virtualnodeshortid>/cpi/<targetcpifilechecksum>` endpoint </a>:
{{< tabs >}}   
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/api/v1/virtualnode/<virtualnodeshortid>/cpi/<targetcpifilechecksum>
```
{{% /tab %}}   
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method PUT -Uri $REST_API_URL/api/v1virtualnode/<virtualnodeshortid>//cpi/<targetcpifilechecksum>
```
{{% /tab %}}   {{< /tabs >}}