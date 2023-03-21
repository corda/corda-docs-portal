---
date: '2023-03-15'
title: "Registration Approval"
menu:
  corda-5-beta:
    identifier: corda-5-beta-registration
    parent: corda-5-beta-operate
    weight: 2000
section_menu: corda-5-beta
---

A network operator can configure a membership group to require that the operator must manually approve (or decline) member registration requests. 
The configuration specifies that requests satisfying specific criteria require [manual approval]({{< relref "#manual-approval" >}}), while others are approved automatically. 
The network operator can also [pre-authenticate specific members]({{< relref "#pre-authentication" >}}), allowing them to bypass the standard approval rules defined for the group.
The operator can further configure pre-authentication to specify that certain changes to the member's context must be manually reviewed.

## Manual Approval

The manual registration approval process presents the request to the operator, enabling the operator to [review the request]({{relref <"./operating-tutorials/registration-requests/reviewing-registration-requests.md" >}}) before approving or declining it using the REST API. 
This process applies to both registration and re-registration requests. 
The approval process can be configured at any point in time, and only affects future registration requests: previously approved members are not required to re-register.

Registration requests are evaluated according to regular expression-based rules defined by the MGM operator. 
The proposed [MemberInfo]({{< relref "../developing/api/api-membership.md#memberinfo" >}}) is compared with the previous (if any) `MemberInfo` to calculate the difference in their member contexts. 
This difference will be 100% in case of a first-time registration, since there will be no previous `MemberInfo` for that member known to the MGM. 
If any of the keys present in this `MemberInfo` difference match the regular expressions set by the MGM operator, the request requires manual approval. 
If there are no matches, the request is auto-approved.

Corda has a set of REST APIs available for managing approval rules. To learn more, see [Configuring Manual Approval Rules]({{< relref "./operating-tutorials/registration-requests/configuring-manual-approval-rules.md" >}}).

## Pre-Authentication

The network operator can pre-authenticate registrations for specific members. This allows a registering member to bypass approval rules defined for the group. Authentication is done outside of Corda using any criteria the operator chooses. Once the network operator has completed their authentication process, they can generate a one-time-use pre-authentication token, also known as a pre-auth token, specific to the authenticated member.

Corda has a set of REST APIs available for managing these pre-auth tokens. Through these APIs, tokens can be created, revoked, and viewed. When viewing a token, it is possible to see the token ID, the X.500 name of the member the token is assigned to, optionally a time and date when the token expires, the token status, and additional information provided by the MGM when creating or revoking the token. For more information, see [Managing Pre-Authentication Tokens]({{< relref "./operating-tutorials/registration-requests/preauthenticating-tokens.md" >}}).

A registration with a pre-auth token can fail for the following reasons:
* The token is not a valid UUID.
* The token was not issued for the X.500 name of the registering member.
* The registration was submitted after the token's time-to-live has expired.
* The token was revoked by the MGM.
* The token was successfully consumed previously.

If any of these conditions are met, the registration is declined.

Although pre-auth tokens allow registrations to bypass the standard set of registration rules configured, the network operator can specify that certain changes to the member's context must be reviewed, even if a pre-auth token was submitted. This is possible through a set of REST APIs very similar to those used to definine group registration approval rules. For more information, see [Configuring Pre-Authentication Rules]({{< relref "./operating-tutorials/registration-requests/configuring-pre-auth-rules.md" >}}).