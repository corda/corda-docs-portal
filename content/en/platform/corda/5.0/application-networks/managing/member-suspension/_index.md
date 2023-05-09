---
date: '2023-05-09'
title: "Member Suspension"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-networks-member-suspension
    parent: corda5-networks-manage
    weight: 1000
section_menu: corda5
---

It is possible to temporarily suspend a member of a group. Once a member has been suspended, flow communication between it and other members of the group is blocked. A suspended member performing a member lookup can not see updates for other members, apart from the MGM. It is not possible to suspend the MGM. This section describes how to perform the following:
* 

The commands shown in this section, use the following variables:
* `REST_API_URL` — the URL of the REST worker. This may vary depending on where you have deployed your cluster and how you have forwarded the ports. For example, `https://localhost:8888/api/v1`.
* `REST_API_USER` — your username for invoking the REST API. 
* `REST_API_PASSWORD` — your password for invoking the REST API.
* `AUTH_INFO` — the authetication information if using PowerShell. You can set this as follows:
   `$AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("admin:admin" -f $username,$password)))`
* `MGM_HOLDING_ID` — the short hash of the MGM's Holding Identity.
* `X500_NAME` — the X500 name of the member being suspended or re-activated.

## Querying for Members

You can use the `Member Lookup` REST endpoint to query for all members with a partciular status. By default, the endpoint returns only ACTIVE members. You can also query for multiple statuses together. For example, to query for all members with the status SUSPENDED:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -u $REST_API_USER:$REST_API_PASSWORD "$REST_API_URL/members/$MGM_HOLDING_ID?statuses=SUSPENDED"
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)}`
   -Method Get -Uri $API_URL/members/$MGM_HOLDING_ID`?statuses=SUSPENDED
```
{{% /tab %}}
{{< /tabs >}}