---
description: "Learn how to upgrade the CPI of a virtual node using the REST API."
date: '2023-06-12'
title: "Upgrading a CPI"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-cluster-nodes-upgrade
    parent: corda51-cluster-nodes
    weight: 3000
section_menu: corda51
---

# Upgrading a CPI

You can upgrade a virtual node's {{< tooltip >}}CPI{{< /tooltip >}} using the PUT method of the <a href ="../../reference/rest-api/openapi.html#tag/Virtual-Node-API/operation/put_virtualnode__virtualnodeshortid__cpi__targetcpifilechecksum_">`api/v1/virtualnode/<virtualnodeshortid>/cpi/<targetcpifilechecksum>` endpoint </a>.

{{< note >}}
The target CPI should have the same name, signer summary hash, and MGM group ID as the existing CPI. You can check the values of the existing CPI by [retrieving the virtual node]({{< relref"./retrieving.md">}}).
{{< /note >}}

To upgrade a CPI, do the following:

1. [Set the state of the virtual node to MAINTENANCE]({{< relref "./state.md">}}).
2. Ensure no flows are running (that is, all flows have either “COMPLETED”, “FAILED” or “KILLED” status). You can check the list of running flows using <a href ="../../reference/rest-api/openapi.html#tag/Flow-Management-API/operation/get_flow__holdingidentityshorthash_">`GET /api/v5_1/flow/<holdingidentityshorthash>` </a>.
3. Send the checksum of the CPI to upgrade to using the PUT method of the <a href ="../../reference/rest-api/openapi.html#tag/Virtual-Node-API/operation/put_virtualnode__virtualnodeshortid__cpi__targetcpifilechecksum_">`api/v1/virtualnode/<virtualnodeshortid>/cpi/<targetcpifilechecksum>` endpoint</a>:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/api/v5_1/virtualnode/<virtualnodeshortid>/cpi/<targetcpifilechecksum>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method PUT -Uri    $REST_API_URL/api/v5_1virtualnode/<virtualnodeshortid>//cpi/<targetcpifilechecksum>
   ```
   {{% /tab %}}
   {{< /tabs >}}

   Upgrading a CPI triggers the member to [re-register]({{< relref "../../application-networks/creating/members/reregister.md" >}}) with the MGM. This ensures the MGM has the latest information about the CPIs that virtual nodes are running.

4. [Set the state of the virtual node to ACTIVE]({{< relref "./state.md">}}).

{{< note >}}
If necessary, you can set the optional `forceupgrade` query parameter to `true` to force an upgrade. An upgrade should only be forced if a previous upgrade attempt failed.
{{< /note >}}
