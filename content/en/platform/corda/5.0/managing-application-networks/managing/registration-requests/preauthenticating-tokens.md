---
date: '2023-04-07'
title: "Managing Pre-Authentication Tokens"
menu:
  corda-5:
    identifier: corda-5-pre-auth-tokens
    parent: corda-5-pre-auth
    weight: 1000
section_menu: corda-5
---



## Creating a Token

To create a pre-auth token for a member, use the [mgm/{holdingidentityshorthash}/preauthtoken POST method](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/post_mgm__holdingidentityshorthash__preauthtoken) of the REST API.

For example, for the member `O=Alice, L=London, C=GB`:

```bash
curl -u $REST_API_USER:$REST_API_PASSWORD -X POST -d '{"ownerX500Name": "O=Alice, L=London, C=GB"}' $REST_API_URL/mgm/$MGM_HOLDING_ID/preauthtoken
```

This token is tied to the specified X.500 name and only a registering member with the same X.500 name can consume that token.

You can also pass the following optional properties when creating a token:
* time-to-live — specifies a duration after which the token will no longer be valid. 
This duration is submitted in the ISO-8601 duration format (PnDTnHnMn.nS). 
For example, PT15M (15 minutes), P4D (4 days), P1DT2H2M (1 day, 2 hours, and 2 minutes). 
The specified duration is added to the current time when the request to create the token is submitted to calculate the time after which the token is no longer valid. 
If no time-to-live value is submitted, the token only expires after it is consumed or revoked. 
* remark —  a user-defined string stored along with the token to provide additional information about the token creation.

## Viewing Tokens

To retrieve all valid pre-auth tokens, use the [mgm/{holdingidentityshorthash}/preauthtoken GET method](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/get_mgm__holdingidentityshorthash__preauthtoken). A valid token is one that has not been consumed, revoked, or expired.

```bash
curl -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/preauthtoken
```

This method returns the rules in the following format:
```JSON
  {
    "creationRemark": "string",
    "id": "string",
    "ownerX500Name": "string",
    "removalRemark": "string",
    "status": "REVOKED",
    "ttl": "2022-06-24T10:15:30Z"
  }
```

You can also pass the following optional properties to filter or expand the search results:
* ownerX500Name — the X.500 name of the member who the token was issued for. 
This is passed as a URL query parameter with the full URL encoded X.500 name.
* preauthtokenid — the ID of a specific token to look up.
* viewinactive — set this to `true` to include consumed, revoked, or expired tokens.
If this is set to false, only tokens that are active and ready to use are returned.

These optional parameters can be used in any combination. The following is an example of all parameters used together:
```bash
TOKEN_ID=<token-ID>
OWNER_X500=<URL-encoded-X.500-name>
curl -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/mgm/$MGM_HOLDING_ID/reauthtoken?viewInactive=true&preAuthTokenId='$TOKEN_ID'&ownerX500Name='$OWNER_X500
```

## Revoking Tokens

To revoke a pre-auth token, pass the ID of the token to the [mgm/{holdingidentityshorthash}/preauthtoken/revoke/{preauthtokenid} PUT method](../../../rest-api/C5_OpenAPI.html#tag/MGM-API/operation/put_mgm__holdingidentityshorthash__preauthtoken_revoke__preauthtokenid_). You can retrieve the ID of a token from the response of creating the token, or from the response of the GET method described in [Viewing Tokens]({{< relref "#viewing-tokens" >}}). This prevents the token from being used. Any registrations submitted with a revoked token are automatically declined.

```bash
curl -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/mgm/$MGM_HOLDING_ID/preauthtoken/revoke/<TOKEN-ID>
```

Optionally, you can submit a remark with the action to revoke the token. This will be stored with the token and visible when viewing tokens for future reference. To include a remark, include a body in the request. For example:

```bash
TOKEN_ID=<token-ID>
curl -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"remarks":"Additional authentication required."}' $REST_API_URL/mgm/$MGM_HOLDING_ID/preauthtoken/revoke/$TOKEN_ID
```