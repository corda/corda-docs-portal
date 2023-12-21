---
description: "Learn how the Network Operator can suspend and re-activate members."
date: '2023-05-09'
title: "Suspending Members"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-networks-member-suspension
    parent: corda51-networks-manage
    weight: 2000
section_menu: corda51
---
# Suspending Members

It is possible to temporarily suspend a {{< tooltip >}}member{{< /tooltip >}} of a group. Once a member has been suspended, Corda blocks {{< tooltip >}}flow{{< /tooltip >}} communication between it and other members of the group. A suspended member performing a member lookup can only see updates from the {{< tooltip >}}MGM{{< /tooltip >}} and not from other members. It is not possible to suspend the MGM. This section describes how to perform the following:

* [Search for Members]({{< relref "#search-for-members">}})
* [Suspend a Member]({{< relref "#suspend-a-member">}})
* [Activate a Member]({{< relref "#activate-a-member">}})

The commands shown in this section, use the following variables:

* `MGM_HOLDING_ID` — the short hash of the MGM's {{< tooltip >}}holding identity{{< /tooltip >}}.
* `X500_NAME` — the {{< tooltip >}}X.500{{< /tooltip >}} name of the member being suspended or re-activated.
* `REST_API_URL` — the URL of the {{< tooltip >}}REST worker{{< /tooltip >}}. This may vary depending on where you have deployed your {{< tooltip >}}cluster{{< /tooltip >}} and how you have forwarded the ports. For example, `https://localhost:8888/api/v5_1`.
* `REST_API_USER` — your username for invoking the REST API.
* `REST_API_PASSWORD` — your password for invoking the REST API.
* `AUTH_INFO` — the authentication information if using PowerShell. You can set this as follows:
   ```
   $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("${REST_API_USER}:${REST_API_PASSWORD}" -f $username,$password)))
   ```

## Search for Members

You can use the [Member Lookup REST endpoint](../../reference/rest-api/openapi.html#tag/Member-Lookup-API) to query for all members with a particular status by specifying the MGM and the status. By default, the endpoint only returns members with the status ACTIVE. You can also query for multiple statuses together. For example, to query for all members with the status SUSPENDED:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD "$REST_API_URL/members/$MGM_HOLDING_ID?statuses=SUSPENDED"
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)}`
   -Method Get -Uri $REST_API_URL/members/$MGM_HOLDING_ID`?statuses=SUSPENDED
```
{{% /tab %}}
{{< /tabs >}}

The GET method of the `/api/v5_1/members/{holdingidentityshorthash}` endpoint returns a list of members, specifying the `memberContext` and `mgmContext` of each. You can extract the serial number of a member from the `corda.serial` field inside the `mgmContext`. This serial number should be used when [suspending]({{< relref "#suspending-a-member">}}) or [activating]({{< relref "#activating-a-member">}}) a member.

## Suspend a Member

You can use the <a href="../../reference/rest-api/openapi.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__suspend">POST method of the `/api/v5_1/members/{holdingidentityshorthash}/suspend` endpoint</a> to suspend a member of a group:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X 'POST' "$REST_API_URL/mgm/$MGM_HOLDING_ID/suspend" -H 'Content-Type: application/json' \
 -d '{"x500Name": '\"$MEMBER_X500_NAME\"', "serialNumber": "<serial-number>"}'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)}`
  -Method Post -Uri $REST_API_URL/mgm/$MGM_HOLDING_ID/suspend -Body (ConvertTo-Json -Depth 1 @{
  x500Name = $MEMBER_X500_NAME; serialNumber = <serial-number>})
```
{{% /tab %}}
{{< /tabs >}}

`<serial-number>` is the current serial number of the member, as retrieved by the [Member Lookup endpoint]({{< relref "#search-for-members">}}). 
If the serial number does not match, the method returns a `409 CONFLICT`. This can happen if another process has updated the member information, before the suspension operation. If this occurs, you can query the Member Lookup endpoint again and decide whether to proceed with the operation.

## Activate a Member

You can use the <a href="../../reference/rest-api/openapi.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__activate">POST method of the `/api/v5_1/members/{holdingidentityshorthash}/activate` endpoint</a> to re-activate a suspended member of a group:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X 'POST' "$REST_API_URL/mgm/$MGM_HOLDING_ID/activate" -H 'Content-Type: application/json' \
 -d '{"x500Name": '\"$MEMBER_X500_NAME\"', "serialNumber": "<serial-number>"}'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)}`
  -Method Post -Uri $REST_API_URL/mgm/$MGM_HOLDING_ID/activate -Body (ConvertTo-Json -Depth 1 @{
  x500Name = $MEMBER_X500_NAME; serialNumber = <serial-number>})
```
{{% /tab %}}
{{< /tabs >}}

`<serial-number>` is the current serial number of the member, as retrieved by the [Member REST endpoint]({{< relref "#search-for-members">}}). 
If the serial number does not match, the method returns a `409 CONFLICT`.

 Once a member has been re-activated, flow communication between it and other members can resume.
