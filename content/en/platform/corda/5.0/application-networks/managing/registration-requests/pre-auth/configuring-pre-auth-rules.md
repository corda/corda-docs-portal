---
date: '2023-04-07'
version: 'Corda 5.0 Beta 4'
title: "Configuring Pre-Authentication Rules"
menu:
  corda5:
    identifier: corda5-pre-auth-rules
    parent: corda5-networks-pre-auth
    weight: 2000
section_menu: corda5
---
# Configuring Pre-Authentication Rules

As described in [Registration Approval]({{< relref "../_index.md#pre-authentication" >}}), you can specify that certain changes to the member’s context must be manually approved (or declined), even if a pre-auth token was submitted. This section describes how to manage pre-auth registration rules using the Corda REST API.

## Adding a Pre-Auth Approval Rule

To add an approval rule for registrations containing a valid pre-auth token, use the [mgm/{holdingidentityshorthash}/approval/rules/preauth POST method](../../../../reference/rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__approval_rules_preauth) of the REST API.

For example, to specify that all requests that contain a valid pre-auth token, with changes to the endpoint information in the member context must be manually approved:

```bash
RULE_PARAMS='{"ruleParams":{"ruleRegex": "^corda.endpoints.*$", "ruleLabel": "Any change to P2P endpoints requires manual review."}}'
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d $RULE_PARAMS $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/preauth
```

## Viewing Current Pre-Auth Approval Rules

To retrieve all created pre-auth approval rules, use the [mgm/{holdingidentityshorthash}/approval/rules/preauth GET method](../../../../reference/rest-api/C5_OpenAPI.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__approval_rules_preauth).

```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/preauth
```

This method returns the rules in the following format:
```JSON
  {
    "ruleId": "string",
    "ruleLabel": "string",
    "ruleRegex": "string"
  }
```

## Deleting a Pre-Auth Approval Rule

To delete a pre-auth approval rule, pass the ID of the rule to the [mgm/{holdingidentityshorthash}/approval/rules/preauth/{ruleid} DELETE method](../../../../reference/rest-api/C5_OpenAPI.html#tag/MGM-API/operation/delete_mgm__holdingidentityshorthash__approval_rules_preauth__ruleid_). You can retrieve the ID of a rule from the response of creating the rule, or from the response of the GET method described in [Viewing Current Pre-Auth Approval Rules]({{< relref "#viewing-current-pre-auth-approval-rules" >}}).

```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X DELETE $REST_API_URL/mgm/$MGM_HOLDING_ID/approval/rules/<RULE_ID>
```
