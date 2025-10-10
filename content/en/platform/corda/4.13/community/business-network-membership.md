---
date: '2020-09-25T12:00:00Z'
menu:
  corda-community-4-13:
    identifier: corda-community-4-13-business-network-management
    parent: corda-community-4-13-corda-networks-index
    weight: 1200
tags:
- BNO
- notary
title: Managing business network membership
---

# Managing business networks

The Business Network Membership Management extension for Corda allows you to create and manage *business networks*. As a node operator, this means you can define and create a logical network based on a set of common CorDapps as well as a shared business context. Corda nodes outside of your business network are not aware of its members. The network can be split into subgroups or membership lists which allows for further privacy (members of a group only know about those in their group).

With the Business Network Membership Management extension, you can use a set of flows to:

- Start a business network
- Add members to a business network
- Assign members to subgroups of a business network
- Update information about a member, such as their business network identity
- Modify members' roles in a business network
- Suspend or revoke memberships from a business network

{{< note >}}
The code samples in this documentation show you how to run management operations using the provided primitives from the context of a tool or CorDapp. It is also possible to do these operations from an RPC client or node shell by simply invoking the supplied administrative flows using data resulting from executing vault queries.
{{< /note >}}

## Available versions

The Business Network Membership Management extension has two available versions which are functionally identical:

- **1.3:** This release is:
  - Only compatible with Corda 4.12 and above
  - Only compatible with JDK 17

- **1.1.2:** This release is:
  - Only compatible with Corda 4.11 and below
  - Only compatible with JDK 8

## Recent change history

### v1.3

In v1.3, no new functionality was added: only support for Corda 4.12 and for JDK 17.

### v1.1.2

In v1.1.2, Apache Log4j dependency has been upgraded to version 2.17.1. This is to prevent exposure to security issues raised with earlier versions of Log4j 2.

In this version, you can:

* Create batch membership requests to speed up onboarding and activation processes.
* Access control group reporting.
* Query group membership.
* Log and report actions to membership attestations.
* Request membership attribute changes.

## Installing the Business Network Membership Management extension

To download and install the Business Network Membership Management extension:

1. Download the required JAR files (either v1.3 or v1.1.2) from the following URLs:

   - For v1.3, if you are using Corda 4.12 or above with JDK 17:
      - [BNE contracts](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-contracts/1.3/business-networks-contracts-1.3.jar)
      - [BNE workflows](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-workflows/1.3/business-networks-workflows-1.3.jar)
      - [Sample CorDapp contracts](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-demo-contracts/1.3/business-networks-demo-contracts-1.3.jar)
      - [Sample CorDapp workflows](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-demo-workflows/1.3/business-networks-demo-workflows-1.3.jar)

   - For v1.1.2, if you are using Corda 4.11 or lower with JDK 8:
      - [BNE contracts](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-contracts/1.1.2/business-networks-contracts-1.1.2.jar)
      - [BNE workflows](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-workflows/1.1.2/business-networks-workflows-1.1.2.jar)
      - [Sample CorDapp contracts](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-demo-contracts/1.1.2/business-networks-demo-contracts-1.1.2.jar)
      - [Sample CorDapp workflows](https://download.corda.net/maven/corda-releases/net/corda/bn/business-networks-demo-workflows/1.1.2/business-networks-demo-workflows-1.1.2.jar)
   

2. Add the `business-networks-contracts` dependency to your **contracts** (and states) CorDapp module:

   ```
   dependencies {
       //...
       cordapp("net.corda.bn:business-networks-contracts:$corda_bn_extension_version")
       //...
   }
   ```
   
3. Add the `business-networks-workflows` dependency to your **workflows** CorDapp module:

   ```
   dependencies {
       //...
      cordapp("net.corda.bn:business-networks-workflows:$corda_bn_extension_version")
       //...
   }
   ```

4. Add both dependencies in your **Cordform** `deployNodes` task; see [Use the cordformation Gradle plugin to create a set of local nodes automatically]({{< relref "generating-a-node.md#use-the-cordformation-gradle-plugin-to-create-a-set-of-local-nodes-automatically" >}}).

You have now installed the Business Network membership extension.

## Business network member types

In a business network, you can assign different roles to members of the network. In this documentation, and throughout your network in general, you may encounter the following type of members:

* **Business network operator:** Has all administrative permissions in the business network.
* **Authorised member:** In a business network, there is at least one *authorised member*. This member has sufficient permissions to execute management operations over the network and its members. Has at least the required administrative permissions to perform a certain task.
* **Member:** May not have administrative permissions but is still a member of the group.

## Creating business networks

To create a new business network:

- From either the node shell or from an RPC client, run `CreateBusinessNetworkFlow` with the following arguments:

   - `networkId`: Custom ID to be given to the new business network. If not specified, a randomly selected one will be used.
   - `businessIdentity`: Optional custom business identity to be given to the membership.
   - `groupId`: Custom ID to be given to the initial business network group. If not specified, randomly selected one will be used.
   - `groupName`: Optional name to be given to the business network group.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val myIdentity: BNIdentity = createBusinessNetworkIdentity() // mock method that creates an instance of a class implementing [BNIdentity]
   val businessNetworkId = UniqueIdentifier()
   val groupId = UniqueIdentifier()
   val notary = serviceHub.networkMapCache.notaryIdentities.first()

   subFlow(CreateBusinessNetworkFlow(businessNetworkId, myIdentity, groupId, "Group 1", notary))
   ```
This will self-issue a membership with an exhaustive permissions set that allows the calling node to manage future operations for the newly created network.

## Managing business network groups

A business network can be split into subgroups or membership lists which allows for further privacy. Members of a group only know about those in their group.

This section describes how an authorised member of a business network can:

- [Create business network groups](#creating-business-network-groups)
- [Modify business network groups](#modifying-business-network-groups)
- [Delete business network groups](#deleting-business-network-groups)

### Creating business network groups

To create a new business network group:

1. Run `CreateGroupFlow` with the following arguments:

   - `networkId`: ID of the business network that the target business network group will relate to.
   - `groupId`: Custom ID to be given to the issued business network group. If not specified, a randomly generated ID will be used.
   - `groupName`: Optional name to be given to the issued business network group.
   - `additionalParticipants`: Set of participants to be added to issued business network group alongside initiator's identity.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val myNetworkId: UniqueIdentifier = ... // id of the network for which groups are created
   val myGroupId = UniqueIdentifier()
   val groupName = "Group 1"
   val notary = serviceHub.networkMapCache.notaryIdentities.first())

   subFlow(CreateGroupFlow(myNetworkId, myGroupId, groupName, emptySet(), notary))
   ```

2. All network members with sufficient permissions approve the proposed change.


### Modifying business network groups

{{< note >}}
When modifying a group, you must ensure that any member who is removed from the group is still part of at least one business network group; otherwise, they will no longer be discoverable.
{{< /note >}}

Use `ModifyGroupFlow` to update the name of a group and/or its list of members. 

To modify a group:

1. Run `ModifyGroupFlow` with the following arguments: 

   - `groupId`: ID of group to be modified.
   - `name`: New name of the modified group. At least one of the *name* or *participants* arguments must be provided.
   - `participants`: New participants of the modified group.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val bnService = serviceHub.cordaService(BNService::class.java)
   val bnGroupId: UniqueIdentifier = ... // get the identifier of the group being updated
   val bnGroupName = bnService.getBusinessNetworkGroup(bnGroupId).state.data.name
   val participantsList = bnService.getBusinessNetworkGroup(bnGroupId).state.data.participants
   val newParticipantsList = removeMember(someMember, participantsList) // mock method that removes a member from the group
   val notary = serviceHub.networkMapCache.notaryIdentities.first())

   subFlow(ModifyGroupFlow(bnGroupId, bnGroupName, newParticipantsList, notary))
   ```

2. All network members with sufficient permissions approve the proposed change.


### Deleting business network groups

To delete a business network group:

1. Run `DeleteGroupFlow` with the following arguments:

   - `groupId`: ID of group to be deleted.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

2. All network members with sufficient permissions must then approve the proposed change.

## Onboarding new members to business networks

You can onboard new members to your business network using any one of the following methods:

- [With prior request from the prospective member](#onboarding-new-members-with-prior-request)
- [Without prior request from the prospective member](#onboarding-new-members-without-prior-request)
- [Both onboard and activate memberships in batches using composite flows](#onboarding-and-activating-members-using-composite-flows)

### Onboarding new members with prior request

Onboarding new members with a prior request is a two-part process:

- **[Part 1:](#part-1-prospective-member-sends-membership-request)** The prospective member first sends a request to join the business network. 
- **[Part 2:](#part-2-authorised-network-member-activates-new-membership)** The request is then approved by the relevant parties and the member is added.

#### Part 1: Prospective member sends membership request

1. The Corda node wishing to join must run the `RequestMembershipFlow` either from the node shell or any other RPC client, using the following arguments:

   - `authorisedParty`: Identity of authorised member from whom membership activation is requested.
   - `networkId`: ID of the Business Network that potential new member wants to join.
   - `businessIdentity`: Optional custom business identity to be given to the membership.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val myIdentity: BNIdentity = createBusinessNetworkIdentity() // create an instance of a class implementing [BNIdentity]
   val networkId: UniqueIdentifier = ... // user provided network unique identifier
   val bno: Party = ... // get the [Party] object of the Corda node acting as a BNO for the business network represented by [networkId]
   val notary = serviceHub.networkMapCache.notaryIdentities.first())

   subFlow(RequestMembershipFlow(bno, networkId, myIdentity, notary))
   ```

2. As a result of a successful run, a membership is created with a `PENDING` status and all authorised members will be notified of any future operations involving it.
3. The prospective member awaits action to activate their membership by an authorised member of the network.

Until activated by an authorised party, such as a business network operator, the newly generated membership can neither be used nor grant the requesting node any permissions in the business network.

#### Part 2: Authorised network member activates new membership

To finalise the on-boarding process:

1. As an authorised member, such as a BNO, run the `ActivateMembershipFlow` to update the targeted membership status from `PENDING` to `ACTIVE`, using the following arguments:

   - `membershipId`: ID of the membership to be activated.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val bnService = serviceHub.cordaService(BNService::class.java)
   val networkId: UniqueIdentifier = ... // id of the business network for which membership activation is done
   val newMemberPartyObject = ... // get the [Party] object of the member whose membership is being activated
   val membershipId = bnService.getMembership(networkId, newMemberPartyObject)
   val groupName = ... // name of the group which the member will be assigned to
   val groupId = ... // identifier of the group which the member will be assigned to
   val notary = serviceHub.networkMapCache.notaryIdentities.first()

   subFlow(ActivateMembershipFlow(membershipId, notary)
   // add newly activated member to a membership list
   val newParticipantsList = bnService.getBusinessNetworkGroup(groupId).state.data.participants.map {
       bnService.getMembership(networkId, it)!!.state.data.linearId
   } + membershipId

   subFlow(ModifyGroupFlow(groupId, groupName, newParticipantsList, notary))
   ```

2. Signatures are collected from **all** authorised parties in the network.
3. Follow up with a group assignment by running the `ModifyGroupFlow`.

The process of onboarding a new member with their prior request is now complete.

### Onboarding new members without prior request

As an authorised member of the network, you can onboard a new member without needing a prior membership request. The joining party is immediately added to the network with an `ACTIVE` status. You can then add the member directly to the relevant groups.

1. Run `OnboardMembershipFlow` to directly issue a new membership with `ACTIVE` status, using the following arguments:

   - `networkId`: ID of the Business Network that member is onboarded to.
   - `onboardedParty`: Identity of an onboarded member.
   - `businessIdentity`: Custom business identity to be given to the onboarded membership.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val bnService = serviceHub.cordaService(BNService::class.java)
   val networkId = "MyBusinessNetwork"
   val onboardedParty = ... // get the [Party] object of the Corda node acting as an onboarded member
   val businessIdentity: BNIdentity = createBusinessNetworkIdentity() // create an instance of a class implementing [BNIdentity]
   val notary = serviceHub.networkMapCache.notaryIdentities.first()
   val groupId = ... // identifier of the group which the member will be assigned to
   val groupName = "Group 1"

   subFlow(OnboardMembershipFlow(networkId, onboardedParty, businessIdentity, notary))

   // add newly activated member to a membership list
   val membershipId = bnService.getMembership(networkId, onboardedParty)!!.state.data.linearId
   val newParticipantsList = bnService.getBusinessNetworkGroup(groupId).state.data.participants.map {
       BNService.getMembership(networkId, it)!!.state.data.linearId
   } + membershipId

   subFlow(ModifyGroupFlow(groupId, groupName, newParticipantsList, notary))
   ```

2. Run `ModifyGroupFlow` to assign the new member to the correct groups.

The process of onboarding a new member without their prior request is now complete.


### Onboarding and activating members using composite flows

To save time and effort, you can use composite flows to perform batch membership onboarding and activation. You can call multiple primitive Business Network management flows (flows under the `net.corda.bn.flows` package) contained within a single flow from the `net.corda.bn.flows.composite` package.

There are two composite flows:

- **[BatchOnboardMembershipFlow](#batchonboardmembershipflow):** Onboards a set of new memberships and adds them to the specified groups.
- **[BatchActivateMembershipFlow](#batchactivatemembershipflow):** Activates a set of pending membership requests and adds them to the specified groups.

#### BatchOnboardMembershipFlow

`BatchOnboardMembershipFlow` takes the following arguments:

- `networkId`: ID of the Business Network where members are onboarded.
- `onboardedParties`: Set of parties to be onboarded and group where to be added after onboarding.
- `defaultGroupId`: ID of the group where members are added if the specific group ID is not provided in their `OnboardingInfo`.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

For example:

```kotlin
val networkId = "MyBusinessNetwork"
val (party1, party2) = ... // get parties to be onboarded to the Business Network
val groupForParty1 = ... // get ID of the group where party1 will be added after onboarding
val businessIdentity1 = createBusinessNetworkIdentity() // mock method that creates an instance of a class implementing [BNIdentity]
val onboardedParties = setOf(
    OnboardingInfo(party = party1, businessIdentity = businessIdentity1, groupId = groupForParty1),
    OnboardingInfo(party = party2, businessIdentity = null, groupId = null)
)
val defaultGroupId = ... // get ID of the group where activated members will be added by default
val notary = serviceHub.networkMapCache.notaryIdentities.first()

subFlow(BatchOnboardMembershipFlow(networkId, onboardedParties, defaultGroupId, notary))
```

#### BatchActivateMembershipFlow

`BatchActivateMembershipFlow` takes the following arguments:

- `memberships`: Set of memberships' `ActivationInfo`s.
- `defaultGroupId`: ID of the group where members are added if the specific group ID is not provided in their `ActivationInfo`.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used.

For example:

```kotlin
val (membershipId1, membershipId2) = ... // fetch pending memberships using [BNService]
val groupForMember1 = ... // get ID of the group where member1 will be added after activation
val memberships = setOf(
    ActivationInfo(membershipId = membershipId1, groupId = groupForMember1),
    ActivationInfo(membershipId = membershipId2, groupId = null)
)
val defaultGroupId = ... // get ID of the group where activated members will be added by default
val notary = serviceHub.networkMapCache.notaryIdentities.first()

subFlow(BatchActivateMembershipFlow(memberships, defaultGroupId, notary))
```

## Updating memberships

If you are an authorised network party, you can change the following attributes of a business network member:

- [Business network identity](#updating-business-identity-attribute)
- [Roles](#updating-business-network-roles)

### Updating business identity attributes

To update a member's business identity attribute:

1. Run the `ModifyBusinessIdentityFlow` with the following arguments:

   - `membershipId`: ID of the membership to modify business identity.
   - `businessIdentity`: Optional custom business identity to be given to the membership.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val bnService = serviceHub.cordaService(BNService::class.java)
   val networkId: UniqueIdentifier = ... // id of the network containing the member whose business identity is being updated
   val partyToBeUpdated = ... // get the [Party] object of the member being updated
   val membership = bnService.getMembership(networkId, partyToBeUpdated)
   val updatedIdentity: BNIdentity = updateBusinessIdentity(membership.state.data.identity) // mock method that updates the business identity in some meaningful way
   val notary = serviceHub.networkMapCache.notaryIdentities.first())

   subFlow(ModifyBusinessIdentityFlow(membership.state.data.linearId, updatedIdentity, notary))
   ```

2. All network members with sufficient permissions then approve the proposed change.


### Updating business network roles

You can also update a member's business identity attributes by modifying their roles. Depending on your proposed changes, the updated member may become an authorised member. In this case, your enhancement must be preceded by an execution of the [ModifyGroupFlow](#modifying-business-network-groups) to add the member to all membership lists that it will have administrative powers over.

To update a member's roles and permissions in the business network:

1. Run the `ModifyRolesFlow` with the following arguments:

   - `membershipId`: ID of the membership to assign roles.
   - `roles`: Set of roles to be assigned to the membership.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val roles = setOf(BNORole()) // assign all administrative permissions to member
   val bnService = serviceHub.cordaService(BNService::class.java)
   val networkId: UniqueIdentifier = ... // id of the network containing the member whose roles are updated
   val partyToBeUpdated = ... // get the [Party] object of the member being updated
   val membershipId = bnService.getMembership(networkId, partyToBeUpdated).state.data.linearId
   val notary = serviceHub.networkMapCache.notaryIdentities.first())

   subFlow(ModifyRolesFlow(membershipId, roles, notary))
   ```
   
2. All network members with sufficient permissions approve the proposed change.

Note there are two additional flows that can be used to quickly assign roles to a membership: `AssignBNORoleFlow` and `AssignMemberRoleFlow`. They both share the same arguments:

- `membershipId`: ID of the membership to assign the role.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

## Suspending or revoking memberships

You can temporarily suspend a member or completely remove them from the business network. Suspending a member will result in a membership status change to `SUSPENDED` and still allow said member to be in the business network. Revocation means that the membership is marked as historic/spent and a new one will have to be requested and activated for the member to re-join the network.

To suspend a member of the network:

1. Run `SuspendMembershipFlow` with the following arguments:

   - `membershipId`: ID of the membership to be suspended.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.
   
   For example:
   
   ```kotlin
   val notary = serviceHub.networkMapCache.notaryIdentities.first())
   val memberToBeSuspended = ... // get the linear ID of the membership state associated with the Party which is being suspended from the network
   subFlow(SuspendMembershipFlow(memberToBeRevoked, notary))
   ```

2. All network members with sufficient permissions approve the proposed change.

To revoke membership completely:

1. Run `RevokeMembershipFlow` with the following arguments:

   - `membershipId`: ID of the membership to be revoked.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.
   
   For example:
   
   ```kotlin
   val notary = serviceHub.networkMapCache.notaryIdentities.first())
   val memberToBeRevoked = ... // get the linear ID of the membership state associated with the Party which is being removed from the network
   subFlow(RevokeMembershipFlow(memberToBeRevoked, notary))
   ```

2. All network members with sufficient permissions approve the proposed change.

When a membership is revoked, the member is also removed from all Business Network Groups.


## Managing membership attribute change requests

Members can use the `RequestMembershipAttributeChangeFlow` flow to create requests to change their attributes (business identity and roles).
This flow will create a `ChangeRequestState` flow with a `PENDING` status.

{{< note >}}
When you request new roles, the changes will overwrite your existing roles.
{{< /note >}}

[Once a membership attribute change request has been created](#creating-membership-attribute-change-requests), as an authorised member, you can either:

- [Approve the request](#approving-membership-attribute-change-requests) using `ApproveMembershipAttributeChangeFlow`. If you accept the request, the existing `ChangeRequestState` will have `ACCEPTED` status.
- [Decline the request](#declining-membership-attribute-change-requests) using `DeclineMembershipAttributeChangeFlow`. If you decline the request, the existing `ChangeRequestState` will have `DECLINED` status.
- [Delete the request](#deleting-membership-attribute-change-requests) by marking it as consumed using `DeleteMembershipAttributeChangeRequestFlow`. This avoids stockpiling requests in the database.


### Creating membership attribute change requests

To create a request to change membership attributes:

-  Run `RequestMembershipAttributeChangeFlow` with the following attributes:

   - `authorisedParty`: Identity of authorised member from whom the change request approval/rejection is requested.
   - `networkId`: ID of the Business Network that members are part of.
   - `businessIdentity`: The proposed business identity change.
   - `roles`: The proposed role change.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val authorisedParty: Party = ... // get the [Party] object of the authorised Corda node
   val networkId = "MyBusinessNetwork"
   val updatedIdentity: BNIdentity = ... // the new business identity you want to associate the member with, if you do not want to modify your existing business identity, then simply skip this step
   val updatedRoles: Set<BNRole> = ... // the new roles you want to associate the member with, if you do not want to modify your existing roles, then simply skip this step
   val notary = serviceHub.networkMapCache.notaryIdentities.first()

   // Request creation
   subFlow(RequestMembershipAttributeChangeFlow(authorisedParty, networkId, updatedIdentity, updatedRoles, notary))
   ```
   
### Approving membership attribute change requests

To approve a request to change membership attributes:

-  Run `ApproveMembershipAttributeChangeFlow` with the following attributes:

   - `requestId`: The ID of the request which needs to be accepted.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val requestId = ... // get the linear ID of the change request state associated with the Party which is requesting for attribute changes
   val notary = serviceHub.networkMapCache.notaryIdentities.first()

   // Approves request
   subFlow(ApproveMembershipAttributeChangeFlow(requestId, notary))
   ```
### Declining membership attribute change requests

To decline a request to change membership attributes:

-  Run `DeclineMembershipAttributeChangeFlow` with the following attributes:

   - `requestId`: The ID of the request which needs to be rejected.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

    For example:

   ```kotlin
   val requestId = ... // get the linear ID of the change request state associated with the Party which is requesting for attribute changes
   val notary = serviceHub.networkMapCache.notaryIdentities.first()

   // Declines request
   subFlow(DeclineMembershipAttributeChangeFlow(requestId, notary))
   ```

### Deleting membership attribute change requests

You can delete membership attribute change requests to remove them from the database.

To delete a membership attribute change request:
 
-  Run `DeleteMembershipAttributeChangeRequestFlow` with the following attributes:

   - `requestId`: The ID of the request which needs to be consumed.
   - `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

   For example:

   ```kotlin
   val requestId = ... // get the linear ID of the change request state associated with the Party which is requesting for attribute changes
   val notary = serviceHub.networkMapCache.notaryIdentities.first()

   // Marks request as CONSUMED
   subFlow(DeleteMembershipAttributeChangeRequestFlow(requestId, notary))
   ```

## Generating access control reports

As a business network operator (BNO), you can ask for the access control report by calling `BNOAccessControlReportFlow`. You will receive the following information in the form of an `AccessControlReport`.

The attributes of the report file are:

* `members`: A detailed list of the members within the network. It contains the following information:
    * `cordaIdentity`: The Corda identity of the member.
    * `businessIdentity`: The business identity of the member.
    * `membershipStatus`: The status of the member's membership.
    * `groups`: A list of all the groups the member is part of.
    * `roles`: A list of the roles the member has.
* `groups`: A detailed list of the groups within the network. It contains the following information:
    * `name`: The name of the group.
    * `participants`: A list of the participants in the group.

To generate an access control report:

- Run `BNOAccessControlReportFlow` with the following arguments:
   - `networkId`: ID of the Business Network, where the participants are present.
   - `path`: The chosen path for the report file to be placed. Optional; if unspecified, the default value `user.dir` is used.
   - `fileName`: The chosen file name of the report file. Optional; if unspecified, the default value `bno-access-control-report` is used.

   For example:

   ```kotlin
   val networkId = "MyBusinessNetwork"
   val path = ... // the absolute path where the report file should be placed
   val fileName = ... // the name of the report file

   subFlow(BNOAccessControlReportFlow(networkId, path, fileName))
   ```

## Reissuing states affected by the change to a member's Corda Identity

It may happen that a member in the network needs to reissue the certificate to which its Corda identity binds. In that case, all membership and group states, which are impacted, should be reissued with the new Corda identity. This can be done using the `UpdateCordaIdentityFlow`. Please note that this flow requires the legal identity (CordaX500Name) to be the same. Furthermore, the flow can only be run by a member with sufficient permissions (who can modify groups).

{{< important >}}
If several members of the network have their certificates rotated, it is important to start the identity update process with the authorised members as they are required
to sign all other identity update transactions.
{{</ important >}}

**UpdateCordaIdentityFlow arguments**:

- `membershipId`: The ID of the membership whose Corda identity has changed.
- `notary`: The Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val notary = serviceHub.networkMapCache.notaryIdentities.first())
val updatedMember = ... // get the linear ID of the membership state associated with the Party which was updated

subflow(UpdateCordaIdentityFlow(updatedMember, notary))
```

## Business network management demo

This [demo](https://github.com/corda/bn-extension) showcases the integration of business networks inside a CorDapp designed for issuing and settling loans between banks. It 
creates four nodes: a notary and three nodes representing banks. Each bank node must be an active member of the same business network, have a Swift Business Identifier Code (BIC) as their business identity, and loan issuance initiators must be granted permission to do so.

### Flow types

RPC-exposed flows can be divided into two groups:

- Standard business network management flows (described above)
- CorDapp-specific ones (described below)

### CorDapp-specific flows

- `AssignBICFlow` assigns **BIC** (Swift Business Identifier Code) as a business identity of a bank node.
    - Usage: `flow start AssignBICFlow membershipId: <UNIQUE_IDENTIFIER>, bic: <STRING>, notary: <OPTIONAL_NOTARY_IDENTITY>`.
- `AssignLoanIssuerRoleFlow` grants loan issuance permission to a calling party. This is self-granting.
    - Usage: `flow start AssignLoanIssuerRoleFlow networkId: <STRING>, notary: <OPTIONAL_NOTARY_IDENTITY>`.
- `IssueLoanFlow` issues new loan state on ledger between caller as lender and borrower specified as flow argument. It also
  performs verification of both parties to ensure they are active members of a business network with the ID specified as
  flow argument. Existence of BIC as business identity is checked and whether flow caller has permission to issue loan.
    - Usage: `flow start IssueLoanFlow networkId: <STRING>, borrower: <PARTY>, amount: <INT>`.
- `SettleLoanFlow` decreases loan's amount by amount specified as flow argument. If it fully settles the loan, associated
  state is consumed. It also verifies that both parties are active members of a Business Network loan belongs to and that
  they both have BIC as business identity.
    - Usage: `flow start SettleLoanFlow loanId: <UNIQUE_IDENTIFIER>, amountToSettle: <INT>`

### Deploying the demo

To deploy and run nodes from the command line in Unix:

1. Run `./gradlew business-networks-demo:deployNodes` to create a set of configs and installs under
   `business-networks-demo/build/nodes`.
2. Run `./business-networks-demo/build/nodes/runnodes` to open up four new terminal tabs/windows with four bank nodes

To deploy and run nodes from the command line in Windows:

1. Run `gradlew business-networks-demo:deployNodes` to create a set of configs and installs under
   `business-networks-demo/build/nodes`
2. Run `business-networks-demo\build\nodes\runnodes` to open up four new terminal tabs/windows with three bank nodes

Next steps are same for every OS (Windows/Mac/Linux).

### Creating a demo business network environment

1. Create a business network from *Bank A* node:

   `flow start CreateBusinessNetworkFlow`
   
2. Obtain network ID and initial group ID from *Bank A*:

   `run vaultQuery contractStateType: net.corda.core.contracts.ContractState` 
   
   `MembershipState` and `GroupState` are issued containing the relevant information.
3. Request membership from *Bank B* and *Bank C* nodes:

   `flow start RequestMembershipFlow authorisedParty: Bank A, networkId: <OBTAINED_NETWORK_ID>, businessIdentity: null, notary: null`
   
4. Obtain requested membership IDs for *Bank B* and *Bank C*; on *Bank A* node, run:

   `run vaultQuery contractStateType: net.corda.core.contracts.ContractState`
   
   Then look into `linearId` of the newly-issued `MembershipState`s.

5. Activate *Bank B* and *Bank C* membership requests from *Bank A* node; for each requested membership, run:

   `flow start ActivateMembershipFlow membershipId: <LINEAR_ID>, notary: null`
   
6. Add newly activated *Bank B* and *Bank C* members into initial group; on *Bank A* node, run:

   `flow start ModifyGroupFlow groupId: <OBTAINED_GROUP_ID>, name: null, participants: [<BANK_A_ID>, <BANK_B_ID>, <BANK_C_ID>], notary: null`

7. Assign BIC to each of the three bank nodes; from *Bank A* node run:

   `flow start AssignBICFlow membershipId: <LINEAR_ID>, bic: <STRING>, notary: null`
   
   Examples of a valid BIC are "BANKGB00", "CHASUS33XXX".
   
8. Assign the Loan Issuer role to *Bank A*; from *Bank A* node, run:

   `flow start AssignLoanIssuerRoleFlow networkId: <OBTAINED_NETWORK_ID>, notary: null`

### Issuing and settling a loan

To demonstrate the issuing and settling of a loan:

1. Issue loan from *Bank A* to *Bank B*; on *Bank A* node, run:

   `flow start IssueLoanFlow networkId: <OBTAINED_NETWORK_ID>, borrower: Bank B, amount: 10`

2. Obtain loan ID from *Bank B* node; run:

   `run vaultQuery contractStateType: net.corda.bn.demo.contracts.LoanState`.
   Then examine `linearId`.
3. Settle the loan; from *Bank B* node, run:

   `flow start SettleLoanFlow loanId: <OBTAINED_LOAN_ID>, amountToSettle: 5`
4. Check that the loan state amount decreased to `5` on both bank nodes.
5. Fully settle the loan; on *Bank B* node, run:

   `flow start SettleLoanFlow loanId: <OBTAINED_LOAN_ID>, amountToSettle: 5`
6. Check the loan state was consumed on both bank nodes.