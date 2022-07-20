---
date: '2020-09-10'
title: "API changes from Corda 4"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-confidential-identities-corda4
    weight: 400
    parent: corda-5-dev-preview-1-confidential-identities
section_menu: corda-5-dev-preview

---

Changes to the way confidential identities are handled have prompted updates to some elements of the Identity Service API. The core concepts have not changed—it is still a directory of parties, with their names and public keys.

In the identity service API:
-   Confidential identities are associated with an X.500 name, rather than a party. If a method previously associated a confidential identity with a party, it now associates the confidential identity with an X.500 name.
-   The `partiesFromName` method has been removed. You can achieve similar RPC functionality with the [member lookup service](../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/extending-rpc.md).
-   The prefix “wellKnown” has been removed. All parties are considered well-known unless they use a confidential identity. In this case,  they are referred to as “anonymous”.
-   The identity utilities service methods `IdentityUtils.kt` has moved to `application-internal/src/main/kotlin/net/corda/internal/application/identity/IdentityInternalUtils.kt`
-   These methods have been removed:
    - `verifyAndRegisterIdentity`
    - `assertOwnership`
    - `getAllIdentities`
    - `certificateFromKey`
    - `requireWellKnownPartyFromAnonymous`
    - `partiesFromName`

In the persistent identity service:
-   The persistent identity service database structure only includes two tables:
   -   Key hash to name.
   -   Key hash to key.
-   The `partyFromAnonymous` method has been simplified to support key rotation, as there is now only one method for keeping confidential identities.
-   The notary lookup method has been removed. Register notaries with `member-info` files.

Additionally, the `unknownAnonymousPartyException` and `InMemoryIdentityService` have been removed.
