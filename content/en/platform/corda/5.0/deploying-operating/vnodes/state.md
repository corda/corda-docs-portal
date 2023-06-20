---
date: '2023-06-12'
title: "Setting the State of Virtual Nodes"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-cluster-nodes-state
    parent: corda5-cluster-nodes
    weight: 2000
section_menu: corda5
---

# Setting the State of Virtual Nodes

A virtual node can have one of the following states: 

* `ACTIVE` — normal operational mode.
* `MAINTENANCE` — maintenance mode. This mode disables all operational statuses:
    * `flowOperationalStatus` — a virtual node’s ability to start new flows.
    * `flowP2pOperationalStatus` — a virtual node’s ability to communicate with peers.
    * `flowStartOperationalStatus` — a virtual node’s ability to run flows, to have checkpoints, and to continue in-progress flows.
    * `vaultDbOperationalStatus` — a virtual node’s ability to perform persistence operations on the virtual node’s vault.
    
    A virtual node in maintenance mode does not allow the starting or running of flows. Any activity for existing flows cause the flow to be killed and marked with a flow status of `KILLED`. Counterparty flows fail with an error message indicating that a peer is in maintenance. This state allows virtual node operators to have a static vault with which they can take backups before performing potentially destructive operations such as a virtual node upgrade for migrations. Changing a virtual node's state back to active requires that the virtual node has executed all migrations in the currently associated CPI. This prevents a virtual node from becoming operational while migrations are in progress during a virtual node upgrade.

You can put an operational virtual node into maintenance mode, or return a node from maintenance to active mode, using the PUT method of the <a href ="../../reference/rest-api/C5_OpenAPI.html#tag/Virtual-Node-API/operation/put_virtualnode__virtualnodeshortid__state__newstate_">`api/v1/virtualnode/<virtualnodeshortid>/state/<newstate>` endpoint </a>:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/api/v1/virtualnode/<virtualnodeshortid>/state/<newstate>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $REST_API_USER:$REST_API_PASSWORD)} -Method PUT -Uri $REST_API_URL/api/v1virtualnode/<virtualnodeshortid>/state/<newstate>
```
{{% /tab %}}
{{< /tabs >}}