---
date: '2023-06-12'
title: "Retrieving Virtual Nodes"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-cluster-nodes-retrieving
    parent: corda5-cluster-nodes
    weight: 1000
section_menu: corda5
---

# Retrieving Virtual Nodes

## Retrieving All Virtual Nodes

To retrieve a list of all virtual nodes in the cluster, use the GET method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Virtual-Node-API/operation/get_virtualnode">`/api/v1/virtualnode` endpoint </a>:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/api/v1/virtualnode
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Uri $REST_API_URL/api/v1/virtualnode
```shell
{{% /tab %}}
{{< /tabs >}}

This endpoint returns the list of all virtual nodes in the cluster as an array of `VirtualNodeInfo` objects in the following format:
```json
{
  "virtualNodes": [
    {
      "cpiIdentifier": {
        "cpiName": "string",
        "cpiVersion": "string",
        "signerSummaryHash": "string"
      },
      "cryptoDdlConnectionId": "string",
      "cryptoDmlConnectionId": "string",
      "flowOperationalStatus": "INACTIVE",
      "flowP2pOperationalStatus": "INACTIVE",
      "flowStartOperationalStatus": "INACTIVE",
      "holdingIdentity": {
        "fullHash": "string",
        "groupId": "string",
        "shortHash": "string",
        "x500Name": "string"
      },
      "hsmConnectionId": "string",
      "operationInProgress": "string",
      "uniquenessDdlConnectionId": "string",
      "uniquenessDmlConnectionId": "string",
      "vaultDbOperationalStatus": "INACTIVE",
      "vaultDdlConnectionId": "string",
      "vaultDmlConnectionId": "string"
    }
  ]
}
```

## Retrieving the Virtual Node of a Member

To retrieve information about the virtual node of a specific member in the cluster, use the GET method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Virtual-Node-API/operation/get_virtualnode__holdingidentityshorthash_">`/api/v1/virtualnode/<holdingidentityshorthash>` endpoint </a>:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/api/v1/virtualnode/<holdingidentityshorthash>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Uri $REST_API_URL/api/v1/virtulnode/<holdingidentityshorthash>
```
{{% /tab %}}
{{< /tabs >}}

This endpoint returns a `VirtualNodeInfo` object for the specified member in the following format:
```json
{
  "cpiIdentifier": {
    "cpiName": "string",
    "cpiVersion": "string",
    "signerSummaryHash": "string"
  },
  "cryptoDdlConnectionId": "string",
  "cryptoDmlConnectionId": "string",
  "flowOperationalStatus": "INACTIVE",
  "flowP2pOperationalStatus": "INACTIVE",
  "flowStartOperationalStatus": "INACTIVE",
  "holdingIdentity": {
    "fullHash": "string",
    "groupId": "string",
    "shortHash": "string",
    "x500Name": "string"
  },
  "hsmConnectionId": "string",
  "operationInProgress": "string",
  "uniquenessDdlConnectionId": "string",
  "uniquenessDmlConnectionId": "string",
  "vaultDbOperationalStatus": "INACTIVE",
  "vaultDdlConnectionId": "string",
  "vaultDmlConnectionId": "string"
}
```