---
description: "Learn how the Network Operator can configure the MGM to require that member registration requests are manually approved (or declined)."
date: '2023-04-07'
title: "Configuring Manual Approval Rules"
menu:
  corda52:
    identifier: corda52-manual-approval-rules
    parent: corda52-networks-reg-requests
    weight: 1000
---
# Configuring Manual Approval Rules

As described in [Registration Approval]({{< relref "./_index.md#manual-approval" >}}), {{< tooltip >}}membership groups{{< /tooltip >}} can require that {{< tooltip >}}member{{< /tooltip >}} registration requests are manually approved (or declined). This section describes how to manage manual registration rules using the Corda REST API.

{{< note >}}
When you apply manual approval, the member registration status is set as `PENDING_MANUAL_APPROVAL`. This is the final outcome of registering the member through rules.
{{< /note >}}

## Adding a Group Approval Rule

To add a group approval rule, use the [mgm/{holdingidentityshorthash}/approval/rules POST method](../../../reference/rest-api/openapi.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__approval_rules) of the REST API.

For example, to specify that all requests with changes to keys in the Corda namespace must be manually approved:
{{< tabs >}}
{{% tab name="Bash"%}}
```bash
RULE_PARAMS='{"ruleParams":{"ruleRegex": "corda.*", "ruleLabel": "Review all changes to keys in the Corda namespace"}}'
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d "$RULE_PARAMS" $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules" -Body (ConvertTo-Json -Depth 4 @{
    ruleLabel = "Review all changes to keys in the Corda namespace",
    ruleRegex = "corda.*"
    }
})
```
{{% /tab %}}
{{< /tabs >}}

## Viewing Current Group Approval Rules

To retrieve all applied group approval rules, use the [mgm/{holdingidentityshorthash}/approval/rules GET method](../../../reference/rest-api/openapi.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__approval_rules).

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules
```
{{% /tab %}}
{{% tab name="PowerShell"%}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules"
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

## Deleting a Group Approval Rule

To delete an applied group approval rule, pass the ID of the rule to the [mgm/{holdingidentityshorthash}/approval/rules/{ruleid} DELETE method](../../../reference/rest-api/openapi.html#tag/MGM-API/operation/delete_mgm__holdingidentityshorthash__approval_rules__ruleid_). You can retrieve the ID of a rule from the response of creating the rule, or from the response of the GET method described in [Viewing Current Group Approval Rules]({{< relref "#viewing-current-group-approval-rules" >}}).

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
