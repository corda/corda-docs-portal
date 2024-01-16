---
description: "Learn how to connect a virtual node to a database not managed by Corda."
date: '2023-01-16'
version: 'Corda 5.2'
title: "Bringing Your Own Database"
menu:
  corda52:
    parent: corda52-cluster-nodes
    identifier: corda52-cluster-byod
    weight: 900
section_menu: corda52
---

# Bringing Your Own Database {{< enterprise-icon >}}

The default Corda deployment and migration functionality for [virtual nodes databases]({{< relref "../../key-concepts/cluster-admin/_index.md#virtual-node-databases" >}}) may not be suitable for environments with a controlled set of database permissions. Changes to database schemas may be a separate process run under the control of a Database Administrator. The bring-your-own-database (BYOD) feature of Corda Enterprise enables Cluster Administrators to manage the creation and any subsequent updates of a PostgreSQL database, rather than using a database managed by Corda.

{{< toc >}}

## Creating Your Own Virtual Node Databases

The following {{< tooltip >}}REST API{{< /tooltip >}} endpoints are available to generate the SQL required to create or update the schemas required for a virtual node:

* [api/v5_2/virtualnode/create/db/crypto](../../reference/rest-api/openapi.html#tag/Virtual-Node-API/operation/get_virtualnode_create_db_crypto) — returns the SQL required to create the `crypto` database.
* [api_v5_2/virtualnode/create/db/uniqueness](../../reference/rest-api/openapi.html#tag/Virtual-Node-API/operation/get_virtualnode_create_db_uniqueness) — returns the SQL required to create the `uniqueness` database.
* [api/v5_2/virtualnode/create/db/vault/{cpichecksum}](../../reference/rest-api/openapi.html#tag/Virtual-Node-API/operation/get_virtualnode_create_db_vault__cpichecksum_) — returns the SQL required to create the `vault` database for a particular {{< tooltip >}}CPI{{< /tooltip >}} specified by its checksum.

For example, to create the required databases for a virtual node:

1. Retrieve the required SQL for the `crypto` database:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X $REST_API_URL/api/v5_2/virtualnode/create/db/crypto
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method -Uri    $REST_API_URL/virtualnode/create/db/crypto
   ```
   {{% /tab %}}
   {{< /tabs >}}
2. Retrieve the required SQL for the `uniqueness` database:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X $REST_API_URL/api/v5_2/virtualnode/create/db/uniqueness
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method -Uri    $REST_API_URL/virtualnode/create/db/uniqueness
   ```
   {{% /tab %}}
   {{< /tabs >}}
3. Retrieve the required SQL for the `vault` database:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X $REST_API_URL/api/v5_2/virtualnode/create/db/vault/<CPI_CHECKSUM>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method -Uri    $REST_API_URL/virtualnode/create/db/vault/<CPI_CHECKSUM>
   ```
   {{% /tab %}}
   {{< /tabs >}}
4. Execute the SQL for the three databases.

## Connecting a Virtual Node to Your Own Database

To update a virtual node to connect to your own database use the PUT method of the [/api/v5_2/virtualnode_virtualnodeshortid_db endpoint](../../../reference/rest-api/openapi.html#tag/Virtual-Node-API/operation/put_virtualnode__virtualnodeshortid__db). This method requires the short hash ID of the virtual node as a path parameter and the connection strings as parameters in the request body. For example:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"cryptoDdlConnection": "'$...'", ...}}' $REST_API_URL/virtualnode/<virtualnodeshortid>/db
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$X500_NAME = "C=GB, L=London, O=Alice"
$VIRTUAL_NODE_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/virtualnode/<virtualnodeshortid>/db" -Method Post -Body (ConvertTo-Json @{
    request = @{
       cryptoDdlConnection = 
       .....
    }
})
```
{{% /tab %}}
{{< /tabs >}}
