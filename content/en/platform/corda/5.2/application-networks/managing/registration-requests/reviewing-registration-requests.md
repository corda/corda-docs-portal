---
description: "Learn how the Network Operator reviews and manually approves or declines registration requests."
date: '2023-04-07'
title: "Reviewing Registration Requests"
menu:
  corda52:
    identifier: corda52-approval-review
    parent: corda52-networks-reg-requests
    weight: 3000
---
# Reviewing Registration Requests

This section describes how to review and manually approve or decline registration requests. This process applies to registration requests that meet the criteria for manual approval specified by a [standard rule for the group]({{< relref "./configuring-manual-approval-rules.md" >}}) or by a [pre-auth rule]({{< relref "pre-auth/configuring-pre-auth-rules.md" >}}).

## Viewing Requests Pending Manual Approval

To view all registration requests for a {{< tooltip >}}membership group{{< /tooltip >}}, use the [GET method of the
mgm/{holdingidentityshorthash}/approval/registrations endpoint](../../../reference/rest-api/openapi.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__registrations).

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations"
```
{{% /tab %}}
{{< /tabs >}}

This method returns the requests in the following format:
```JSON
{
  "memberInfoSubmitted": {
    "data": 
  },
  "reason": "string",
  "registrationId": "string",
  "registrationSent": "2023-06-24T10:15:30Z",
  "registrationStatus": "PENDING_MANUAL_APPROVAL",
  "registrationUpdated": "2023-06-24T10:15:30Z"
}
```

Requests that are pending manual approval have the status `PENDING_MANUAL_APPROVAL`.

To view requests from a specific {{< tooltip >}}member{{< /tooltip >}} (for example, `C=GB, L=London, O=Alice`):

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations?requestsubjectx500name=C%3DGB%2C%20L%3DLondon%2C%20O%3DAlice'
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations?requestsubjectx500name=C%3DGB%2C%20L%3DLondon%2C%20O%3DAlice"
```
{{% /tab %}}
{{< /tabs >}}

To include historic requests, set the `viewhistoric` parameter to `true`:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations?requestsubjectx500name=C%3DGB%2C%20L%3DLondon%2C%20O%3DAlice&viewhistoric=true'
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations?requestsubjectx500name=C%3DGB%2C%20L%3DLondon%2C%20O%3DAlice&viewhistoric=true"
```
{{% /tab %}}
{{< /tabs >}}

## Approving a Request

To approve a rquest, pass the ID of the request to the [POST method of the
mgm/{holdingidentityshorthash}/approve/{requestid} endpoint](../../../reference/rest-api/openapi.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__approve__requestid_). You can retrieve the ID of a request from the response of the GET endpoint described in [Viewing Requests Pending Manual Approval]({{< relref "#viewing-requests-pending-manual-approval" >}}).

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/mgm/$MGM_HOLDING_ID/approve/<REQUEST-ID>
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approve/<REQUEST-ID>"
```
{{% /tab %}}
{{< /tabs >}}

 {{< note >}}
You can only approve requests that are in the `PENDING_MANUAL_APPROVAL` status.
{{< /note >}}

## Declining a Request

To decline a request, pass the ID of the request and a reason to the [POST method of the
mgm/{holdingidentityshorthash}/decline/{requestid} endpoint](../../../reference/rest-api/openapi.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__decline__requestid_). You can retrieve the ID of a request from the response of the GET endpoint described in [Viewing Requests Pending Manual Approval]({{< relref "#viewing-requests-pending-manual-approval" >}}).

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d <REASON> $REST_API_URL/mgm/$MGM_HOLDING_ID/decline/<REQUEST-ID>
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/decline/<REQUEST-ID>" -Body "<REASON>"
```
{{% /tab %}}
{{< /tabs >}}

 {{< note >}}
You can only decline requests that have the status `PENDING_MANUAL_APPROVAL`.
{{< /note >}}
