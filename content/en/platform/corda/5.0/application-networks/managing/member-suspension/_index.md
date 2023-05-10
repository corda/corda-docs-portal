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


It is possible to temporarily suspend a member of a group. Once a member has been suspended, flow communication between it and other members of the group is blocked. A suspended member performing a member lookup can only see see updates from the MGM and not from other members. It is not possible to suspend the MGM. This section describes how to perform the following:
* [Querying for Members]({{< relref "#querying-for-members">}})
* [Suspending a Member]({{< relref "#suspending-a-member">}})
* [Activating a Member]({{< relref "#activating-a-member">}})

The commands shown in this section, use the following variables:
* `MGM_HOLDING_ID` — the short hash of the MGM's Holding Identity.
* `X500_NAME` — the X.500 name of the member being suspended or re-activated.
* `REST_API_URL` — the URL of the REST worker. This may vary depending on where you have deployed your cluster and how you have forwarded the ports. For example, `https://localhost:8888/api/v1`.
* `REST_API_USER` — your username for invoking the REST API. 
* `REST_API_PASSWORD` — your password for invoking the REST API.
* `AUTH_INFO` — the authetication information if using PowerShell. You can set this as follows:
   ```
   $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("admin:admin" -f $username,$password)))
   ```

## Querying for Members

You can use the [Member Lookup REST endpoint](../../reference/rest-api/C5_OpenAPI.html#tag/Member-Lookup-API) to query for all members with a particular status by specifying the MGM. By default, the endpoint returns only ACTIVE members. You can also query for multiple statuses together. For example, to query for all members with the status SUSPENDED:

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

The GET method of the `/api/v1/members/{holdingidentityshorthash}` endpoint returns a list of members, specifying the `memberContext` and `mgmContext` of each. You can extract the serial number of a member from the `corda.serial` field inside the `mgmContext`. This serial number is required when [suspending]({{< relref "#suspending-a-member">}}) or [activating]({{< relref "#activating-a-member">}}) a member.

## Suspending a Member

You can use GET method of the [MGM REST endpoint](../../reference/rest-api/C5_OpenAPI.html#tag/Member-Lookup-API) to 

## Activating a Member