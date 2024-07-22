---
description: "Learn how to connect a virtual node to a database not managed by Corda."
date: '2023-01-16'
version: 'Corda 5.3'
title: "Bringing Your Own Database"
menu:
  corda53:
    parent: corda53-cluster-nodes
    identifier: corda53-cluster-byod
    weight: 900
section_menu: corda53
---

# Bringing Your Own Database

The default Corda deployment and migration functionality for [virtual nodes databases]({{< relref "../../key-concepts/cluster-admin/_index.md#virtual-node-databases" >}}) may not be suitable for environments with a controlled set of database permissions. Changes to database schemas may be a separate process run under the control of a Database Administrator. The bring-your-own-database (BYOD) feature enables Cluster Administrators to manage the creation and any subsequent updates of a PostgreSQL database, rather than using a database managed by Corda.

{{< toc >}}

## Creating Your Own Virtual Node Databases

The following REST API endpoints are available to generate the SQL to update the schemas required for a virtual node:

* [api/v5_3/virtualnode/create/db/crypto](../../reference/rest-api/openapi.html#tag/Virtual-Node/operation/get_virtualnode_create_db_crypto) — returns the SQL required to create the `crypto` database.
* [api_v5_3/virtualnode/create/db/uniqueness](../../reference/rest-api/openapi.html#tag/Virtual-Node/operation/get_virtualnode_create_db_uniqueness) — returns the SQL required to create the `uniqueness` database.
* [api/v5_3/virtualnode/create/db/vault/<cpichecksum>](../../reference/rest-api/openapi.html#tag/Virtual-Node/operation/get_virtualnode_create_db_vault__cpichecksum_) — returns the SQL required to create the `vault` database for a particular {{< tooltip >}}CPI{{< /tooltip >}} specified by its checksum.

For example, to create the required databases for a virtual node:

1. Create the necessary schemas and users. You must specify the `search_path` for the schema for all users. The DML user for each database requires SELECT, UPDATE, INSERT, and DELETE permissions. The DDL user is optional but, if used, it requires full permissions to enable it to deploy schema.

2. Retrieve the SQL for the `crypto` database:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X $REST_API_URL/api/v5_3/virtualnode/create/db/crypto
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method -Uri    $REST_API_URL/virtualnode/create/db/crypto
   ```
   {{% /tab %}}
   {{< /tabs >}}
3. Retrieve the SQL for the `uniqueness` database:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X $REST_API_URL/api/v5_3/virtualnode/create/db/uniqueness
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method -Uri    $REST_API_URL/virtualnode/create/db/uniqueness
   ```
   {{% /tab %}}
   {{< /tabs >}}
4. Retrieve the SQL for the `vault` database:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X $REST_API_URL/api/v5_3/virtualnode/create/db/vault/<CPI_CHECKSUM>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method -Uri    $REST_API_URL/virtualnode/create/db/vault/<CPI_CHECKSUM>
   ```
   {{% /tab %}}
   {{< /tabs >}}
5. Execute the SQL for the three databases.

## Connecting a Virtual Node to Your Own Database

To update an existing virtual node to connect to your own database, use the PUT method of the [/api/v5_3/virtualnode/<virtualnodeshortid>/db endpoint](../../reference/rest-api/openapi.html#tag/Virtual-Node/operation/put_virtualnode__virtualnodeshortid__db). This method requires the short hash ID of the virtual node as a path parameter and the connection strings as parameters in the request body. For example:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"cryptoDdlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"cryptoddlconnection_fd545924ff37\",\"pass\":\"WXZS48pRyFQu0GNJNseRMeIL8ZczwfPAHnDJRZdQ11M6fJxjjdhbcKEYSwSiHHqT\"}}","cryptoDmlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"cryptodmlconnection_fd545924ff37\",\"pass\":\"d6LIdsVpTwoHaetemyeGWXb0TjRHXOCR6yrxeCCWzWTGiqiDxR5zPuYMBaFdbj6A\"}}","uniquenessDdlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"uniquenessddlconnection_fd545924ff37\",\"pass\":\"nVzjzsjfmQpSubHi7K7Rt2Cjlt40wb85zPQQI1KxprmCUswqUJhHH0ovdTy6wYWi\"}}","uniquenessDmlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"uniquenessdmlconnection_fd545924ff37\",\"pass\":\"HjgqzcVTohZIapZrgsNz6dlW6U4yHUn6LjCsfG5nwHbuso5hsvAuWBB8DievZX7R\"}}","vaultDdlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"vaultddlconnection_fd545924ff37\",\"pass\":\"UwFGEWX9KFfLf9Gai63bUAgcMMh0OzUP9wTRGYEhptkBcfzqScK6tqnz6wSAxN7K\"}}","vaultDmlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"vaultdmlconnection_fd545924ff37\",\"pass\":\"PJRFQInjedKZcgf1o0YYq7Dv7vhbsdFL5U7FuCID3S7ZYjPNJ7GITbyTgIofeQwL\"}}"}' $REST_API_URL/virtualnode/<virtualnodeshortid>/db
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/virtualnode/<virtualnodeshortid>/db" -Method Post -Body (ConvertTo-Json @{
    request = @{
      "cryptoDdlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"cryptoddlconnection_fd545924ff37\",\"pass\":\"WXZS48pRyFQu0GNJNseRMeIL8ZczwfPAHnDJRZdQ11M6fJxjjdhbcKEYSwSiHHqT\"}}"
      "cryptoDmlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"cryptodmlconnection_fd545924ff37\",\"pass\":\"d6LIdsVpTwoHaetemyeGWXb0TjRHXOCR6yrxeCCWzWTGiqiDxR5zPuYMBaFdbj6A\"}}"
      "uniquenessDdlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"uniquenessddlconnection_fd545924ff37\",\"pass\":\"nVzjzsjfmQpSubHi7K7Rt2Cjlt40wb85zPQQI1KxprmCUswqUJhHH0ovdTy6wYWi\"}}"
      "uniquenessDmlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"uniquenessdmlconnection_fd545924ff37\",\"pass\":\"HjgqzcVTohZIapZrgsNz6dlW6U4yHUn6LjCsfG5nwHbuso5hsvAuWBB8DievZX7R\"}}"
      "vaultDdlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"vaultddlconnection_fd545924ff37\",\"pass\":\"UwFGEWX9KFfLf9Gai63bUAgcMMh0OzUP9wTRGYEhptkBcfzqScK6tqnz6wSAxN7K\"}}"
      "vaultDmlConnection":"{\"database\":{\"jdbc\":{\"url\":\"jdbc:postgresql://localhost:5432/yourdatabase\"},\"user\":\"vaultdmlconnection_fd545924ff37\",\"pass\":\"PJRFQInjedKZcgf1o0YYq7Dv7vhbsdFL5U7FuCID3S7ZYjPNJ7GITbyTgIofeQwL\"}}"
   }
})
```
{{% /tab %}}
{{< /tabs >}}
