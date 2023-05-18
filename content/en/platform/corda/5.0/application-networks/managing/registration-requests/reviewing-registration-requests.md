---
date: '2023-03-15'
version: 'Corda 5.0'
title: "Reviewing Registration Requests"
menu:
  corda5:
    identifier: corda5-approval-review
    parent: corda5-networks-reg-requests
    weight: 3000
section_menu: corda5
---

This section describes how to review and manually approve or decline registration requests. This process applies to registration requests that meet the criteria for manual approval specified by a [standard rule for the group]({{< relref "./configuring-manual-approval-rules.md" >}}) or by a [pre-auth rule]({{< relref "pre-auth/configuring-pre-auth-rules.md" >}}). 

## Viewing Requests Pending Manual Approval

To view all registration requests, use the [GET method of the
mgm/{holdingidentityshorthash}/approval/registrations endpoint](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__registrations).

```bash
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations
```

This method returns the rules in the following format:
```JSON
  {
    "memberInfoSubmitted": {
      "data": 
    },
    "reason": "string",
    "registrationId": "string",
    "registrationSent": "2022-06-24T10:15:30Z",
    "registrationStatus": "SENT_TO_MGM",
    "registrationUpdated": "2022-06-24T10:15:30Z"
  }
```

Requests that are pending manual approval have the status `PENDING_MANUAL_APPROVAL`.

To view requests from a specific member (for example, `C=GB, L=London, O=Alice`) and include historic requests:

```bash
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/registrations?requestsubjectx500name=C%3DGB%2C%20L%3DLondon%2C%20O%3DAlice&viewhistoric=true'
```

## Approving a Request

To approve a rquest, pass the ID of the request to the [POST method of the
mgm/{holdingidentityshorthash}/approve/{requestid} endpoint](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__approve__requestid_). You can retrieve the ID of a request from the response of the GET endpoint described in [Viewing Requests Pending Manual Approval]({{< relref "#viewing-requests-pending-manual-approval" >}}). 

```bash
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/mgm/$MGM_HOLDING_ID/approve/<REQUEST_-_ID>
```
 {{< note >}}
You can only approve requests that are in the `PENDING_MANUAL_APPROVAL` status.
{{< /note >}}

## Declining a Request

To decline a request, pass the ID of the request and a reason to the [POST method of the
mgm/{holdingidentityshorthash}/decline/{requestid} endpoint](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__decline__requestid_). You can retrieve the ID of a request from the response of the GET endpoint described in [Viewing Requests Pending Manual Approval]({{< relref "#viewing-requests-pending-manual-approval" >}}). 

```bash
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -d <REASON> $REST_API_URL/mgm/$MGM_HOLDING_ID/decline/<REQUEST_-_ID>
```
 {{< note >}}
You can only decline requests that have the status `PENDING_MANUAL_APPROVAL`.
{{< /note >}}