---
date: '2023-03-15'
title: "Manual Registration Approval"
menu:
  corda-5-beta:
    identifier: corda-5-beta-manual-registration
    parent: corda-5-beta-operate
    weight: 1000
section_menu: corda-5-beta
---

Membership groups can be configured to specify that the MGM operator must manually approve (or decline) member registration requests. 
The approval process can specify that requests satisfying specific criteria require manual approval, while others are approved automatically. 
The manual approval process presents the request to the MGM operator, enabling the operator to review the request before approving or declining it using the REST API. 
This process applies to both registration and re-registration requests. 
The approval process can be configured at any point in time, and only affects future registration requests - previously approved members are not required to re-register.

Registration requests are evaluated according to regular expression-based rules defined by the MGM operator. 
The proposed [MemberInfo]({{< relref "../developing/api/api-membership.md#memberinfo" >}}) is compared with the previous (if any) `MemberInfo` to calculate the difference in their member contexts. 
This difference will be 100% in case of a first-time registration, since there will be no previous `MemberInfo` for that member known to the MGM. 
If any of the keys present in this `MemberInfo` difference match the regular expressions set by the MGM operator, the request requires manual approval. 
If there are no matches, the request is auto-approved.

To learn how to manage manual approval rules, see [Configuring Manual Approval]({{< relref "./operating-tutorials/manual-approval.md" >}}).