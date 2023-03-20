---
date: '2023-03-15'
title: "Configuring Pre-Authentication Rules"
menu:
  corda-5-beta:
    identifier: corda-5-beta-config-pre-auth-rules
    parent: corda-5-beta-reg-requests-pre-auth
    weight: 4000
section_menu: corda-5-beta
---

As described in [Registration Approval]({{< relref "../../registration-approval.md" >}}), you can specify that certain changes to the member’s context must be manually approved (or declined), even if a pre-auth token was submitted. This section describes how to manage pre-auth registration rules using the Corda REST API.

## Adding a Pre-Auth Approval Rule

To add an approval rule for registrations containing a valid pre-auth token, use the [mgm/{holdingidentityshorthash}/approval/rules/preauth POST method](../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__approval_rules_preauth) of the REST API.

For example, to specify that all requests that contain a valid pre-auth token, with changes to the endpoint information in the member context must be manually approved:

```bash
RULE_PARAMS='{"ruleParams":{"ruleRegex": "^corda.endpoints.*$", "ruleLabel": "Any change to P2P endpoints requires manual review."}}'
curl --insecure -u <username>:<password> -d $RULE_PARAMS <REST-API-URL>/mgm/<MGM-HOLDING-ID>/approval/rules/preauth
```

## Viewing Current Pre-Auth Approval Rules

To retrieve all created pre-auth approval rules, use the [mgm/{holdingidentityshorthash}/approval/rules/preauth GET method](../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__approval_rules_preauth).

```bash
curl --insecure -u <username>:<password> <REST-API-URL>/mgm/<MGM-HOLDING-ID>/approval/rules/preauth
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

To delete a pre-auth approval rule, pass the ID of the rule to the [mgm/{holdingidentityshorthash}/approval/rules/preauth/{ruleid} DELETE method](../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/delete_mgm__holdingidentityshorthash__approval_rules_preauth__ruleid_). You can retrieve the ID of a rule from the response of creating the rule, or from the response of the GET method described in [Viewing Current Pre-Auth Approval Rules]({{< relref "#viewing-current-pre-auth-approval-rules" >}}).

```bash
curl --insecure -u <username>:<password> -X DELETE <REST-API-URL>/mgm/<MGM-HOLDING-ID>/approval/rules/<RULE-ID>
```
