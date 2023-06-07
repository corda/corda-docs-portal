---
date: '2023-04-07'
version: 'Corda 5.0'
title: "Configuring Manual Approval Rules"
menu:
  corda5:
    identifier: corda5-manual-approval-rules
    parent: corda5-networks-reg-requests
    weight: 1000
section_menu: corda5
---
# Configuring Manual Approval Rules
As described in [Registration Approval]({{< relref "./_index.md#manual-approval" >}}), membership groups can require that member registration requests are manually approved (or declined). This section describes how to manage manual registration rules using the Corda REST API.
## Adding a Group Approval Rule

To add a group approval rule, use the [mgm/{holdingidentityshorthash}/approval/rules POST method](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__approval_rules) of the REST API.

For example, to specify that all requests with changes to keys in the Corda namespace must be manually approved:

```bash
RULE_PARAMS='{"ruleParams":{"ruleRegex": "corda.*", "ruleLabel": "Review all changes to keys in the Corda namespace"}}'
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d "$RULE_PARAMS" $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules
```

## Viewing Current Group Approval Rules

To retrieve all applied group approval rules, use the [mgm/{holdingidentityshorthash}/approval/rules GET method](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__approval_rules).

```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules
```

This method returns the rules in the following format:
```JSON
  {
    "ruleId": "string",
    "ruleLabel": "string",
    "ruleRegex": "string"
  }
```

## Deleting a Group Approval Rule

To delete an applied group approval rule, pass the ID of the rule to the [mgm/{holdingidentityshorthash}/approval/rules/{ruleid} DELETE method](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/delete_mgm__holdingidentityshorthash__approval_rules__ruleid_). You can retrieve the ID of a rule from the response of creating the rule, or from the response of the GET method described in [Viewing Current Group Approval Rules]({{< relref "#viewing-current-group-approval-rules" >}}).

```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X DELETE $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/<RULE_ID>
```
