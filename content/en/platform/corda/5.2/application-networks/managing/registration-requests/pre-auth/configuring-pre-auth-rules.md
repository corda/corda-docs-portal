---
description: ""
date: '2023-04-07'
title: "Configuring Pre-Authentication Rules"
menu:
  corda52:
    identifier: corda52-pre-auth-rules
    parent: corda52-networks-pre-auth
    weight: 2000
---
# Configuring Pre-Authentication Rules

As described in [Registration Approval]({{< relref "../_index.md#pre-authentication" >}}), you can specify that certain changes to the member’s context must be manually approved (or declined), even if a pre-auth {{< tooltip >}}token{{< /tooltip >}} was submitted. This section describes how to manage pre-auth registration rules using the Corda REST API.

{{< note >}}
When you apply pre-auth rules, the member registration status is set as `PENDING_MANUAL_APPROVAL`. This is the final outcome of registering the member through rules.
{{< /note >}}

## Adding a Pre-Auth Approval Rule

To add an approval rule for registrations containing a valid pre-auth token, use the [mgm/{holdingidentityshorthash}/approval/rules/preauth POST method](../../../../reference/rest-api/openapi.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__approval_rules_preauth) of the REST API.

For example, to specify that all requests that contain a valid pre-auth token, with changes to the endpoint information in the {{< tooltip >}}member{{< /tooltip >}}  context must be manually approved:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
RULE_PARAMS='{"ruleParams":{"ruleRegex": "^corda.endpoints.*$", "ruleLabel": "Any change to P2P endpoints requires manual review."}}'
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d $RULE_PARAMS $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/preauth
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/preauth" -Body (ConvertTo-Json  @{
    ruleRegex = "^corda.endpoints.*$",
    ruleLabel = "Any change to P2P endpoints requires manual review."
    }
})
```
{{% /tab %}}
{{< /tabs >}}

## Viewing Current Pre-Auth Approval Rules

To retrieve all created pre-auth approval rules, use the [mgm/{holdingidentityshorthash}/approval/rules/preauth GET method](../../../../reference/rest-api/openapi.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__approval_rules_preauth).

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/preauth
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/preauth"
```
{{% /tab %}}
{{< /tabs >}}

This method returns the rules in the following format:
```JSON
{
  "ruleId": "string",
  "ruleLabel": "string",
  "ruleRegex": "string"
}
```

## Deleting a Pre-Auth Approval Rule

To delete a pre-auth approval rule, pass the ID of the rule to the [mgm/{holdingidentityshorthash}/approval/rules/preauth/{ruleid} DELETE method](../../../../reference/rest-api/openapi.html#tag/MGM-API/operation/delete_mgm__holdingidentityshorthash__approval_rules_preauth__ruleid_). You can retrieve the ID of a rule from the response of creating the rule, or from the response of the GET method described in [Viewing Current Pre-Auth Approval Rules]({{< relref "#viewing-current-pre-auth-approval-rules" >}}).

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X DELETE $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/<RULE_ID>
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Delete -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/<RULE_ID>"
```
{{% /tab %}}
{{< /tabs >}}
