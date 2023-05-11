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

It is possible to temporarily suspend a member of a group. Once a member has been suspended, Corda blocks flow communication between it and other members of the group. A suspended member performing a member lookup can only see updates from the MGM and not from other members. It is not possible to suspend the MGM. This section describes how to perform the following:
* [Query for Members]({{< relref "#query-for-members">}})
* [Suspend a Member]({{< relref "#suspend-a-member">}})
* [Activate a Member]({{< relref "#activate-a-member">}})

The commands shown in this section, use the following variables:
* `MGM_HOLDING_ID` — the short hash of the MGM's holding identity.
* `X500_NAME` — the X.500 name of the member being suspended or re-activated.
* `REST_API_URL` — the URL of the REST worker. This may vary depending on where you have deployed your cluster and how you have forwarded the ports. For example, `https://localhost:8888/api/v1`.
* `REST_API_USER` — your username for invoking the REST API. 
* `REST_API_PASSWORD` — your password for invoking the REST API.
* `AUTH_INFO` — the authentication information if using PowerShell. You can set this as follows:
   ```
   $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("admin:admin" -f $username,$password)))
   ```

## Query for Members

You can use the [Member Lookup REST endpoint](../../reference/rest-api/C5_OpenAPI.html#tag/Member-Lookup-API) to query for all members with a particular status by specifying the MGM and the status. By default, the endpoint returns only ACTIVE members. You can also query for multiple statuses together. For example, to query for all members with the status SUSPENDED:

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

The GET method of the `/api/v1/members/{holdingidentityshorthash}` endpoint returns a list of members, specifying the `memberContext` and `mgmContext` of each. You can extract the serial number of a member from the `corda.serial` field inside the `mgmContext`. This serial number should be used when [suspending]({{< relref "#suspending-a-member">}}) or [activating]({{< relref "#activating-a-member">}}) a member.

## Suspend a Member

You can use the <a href="../../reference/rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__suspend">POST method of the `/api/v1/members/{holdingidentityshorthash}/suspend` endpoint</a> to suspend a member of a group:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -u $REST_API_USER:$REST_API_PASSWORD -X 'POST' "$API_URL/mgm/$MGM_HOLDING_ID/suspend" -H 'Content-Type: application/json' \
 -d '{"x500Name": '\"$MEMBER_X500_NAME\"', "serialNumber": "<serial-number>"}'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)}`
  -Method Post -Uri $API_URL/mgm/$MGM_HOLDING_ID/suspend -Body (ConvertTo-Json -Depth 1 @{
  x500Name = $MEMBER_X500_NAME; serialNumber = <serial-number>})
```
{{% /tab %}}
{{< /tabs >}}

`<serial-number>` is the current serial number of the member, as retrieved by the [Member Lookup endpoint]({{< relref "#query-for-members">}}). The `<serial-number>` is optional. If it is not specified, the latest serial number is used. However, we recommend always specifying the serial number in the request to avoid suspending a member based on outdated information. If the serial number does not match, the method returns a `409 CONFLICT`. This can happen if another process has updated the member information, before the suspension operation. If this occurs, you can query the Member Lookup endpoint again and decide whether to proceed with the operation.

## Activate a Member

You can use the <a href="../../reference/rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__activate">POST method of the `/api/v1/members/{holdingidentityshorthash}/activate` endpoint</a> to re-activate a suspended member of a group:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -u $REST_API_USER:$REST_API_PASSWORD -X 'POST' "$API_URL/mgm/$MGM_HOLDING_ID/activate" -H 'Content-Type: application/json' \
 -d '{"x500Name": '\"$MEMBER_X500_NAME\"', "serialNumber": "<serial-number>"}'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)}`
  -Method Post -Uri $API_URL/mgm/$MGM_HOLDING_ID/activate -Body (ConvertTo-Json -Depth 1 @{
  x500Name = $MEMBER_X500_NAME; serialNumber = <serial-number>})
```
{{% /tab %}}
{{< /tabs >}}

`<serial-number>` is the current serial number of the member, as retrived by the [Member REST endpoint]({{< relref "#query-for-members">}}). The `<serial-number>` is optional. If it is not specified, the latest serial number is used. However, we recommend always specifying the serial number in the request to avoid suspending a member based on outdated information. If the serial number does not match, the method returns a `409 CONFLICT`.

 Once a member has been re-activated, flow communication between it and other members can resume.