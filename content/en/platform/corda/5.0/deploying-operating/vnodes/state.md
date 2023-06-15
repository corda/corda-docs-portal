---
date: '2023-06-12'
title: "Setting the State of Virtual Nodes"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cluster-nodes-state
    parent: corda5-cluster-nodes
    weight: 2000
section_menu: corda5
---

# Setting the State of Virtual Nodes

A virtual node can be in one of the following states: 

* `ACTIVE` — normal operational mode.
* `MAINTENANCE` — maintenance mode. This mode disables all operational statuses:
    * `flowOperationalStatus` — a virtual node’s ability to start new flows.
    * `flowP2pOperationalStatus` — a virtual node’s ability to communicate with peers.
    * `flowStartOperationalStatus` — a virtual node’s ability to run flows, to have checkpoints, and to continue in-progress flows.
    * `vaultDbOperationalStatus` — a virtual node’s ability to perform persistence operations on the virtual node’s vault.

You can put an operational virtual node into maintenance mode, or return a node from maintenance to active mode, using the PUT method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Virtual-Node-API/operation/put_virtualnode__virtualnodeshortid__state__newstate_">`api/v1/virtualnode/<virtualnodeshortid>/state/<newstate>` endpoint </a>:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/api/v1/virtualnode/<virtualnodeshortid>/state/<newstate>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method PUT -Uri $REST_API_URL/api/v1virtualnode/<virtualnodeshortid>/state/<newstate>
```shell
{{% /tab %}}
{{< /tabs >}}