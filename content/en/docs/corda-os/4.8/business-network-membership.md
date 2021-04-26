---
date: '2020-09-25T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-business-network-management
    parent: corda-os-4-8-corda-networks-index
    weight: 1200
tags:
- BNO
- notary
title: Managing Business Network membership
---

# Business Network membership management

This Corda platform extension allows you to create and manage business networks - as a node operator, this means you can define and create a logical network based on a set of common CorDapps as well as a shared business context.

Corda nodes outside of your business network are not aware of its members. The network can be split into subgroups or membership lists which allows for further privacy (members of a group only know about those in their group).

In a business network, there is at least one *authorised member*. This member has sufficient permissions to execute management operations over the network and its members.

## In version 1.1

In this version, you can:

* Create batch membership requests to speed up onboarding and activation processes.
* Access control group reporting.
* Query group membership.
* Log and report actions to membership attestations.
* Request membership attribute changes.

## Creating and managing a business network

With this extension, you can use a set of flows to:

* Start a business network.
* Add members.
* Assign members to membership lists or groups.
* Update information about a member - such as their Business Network identity.
* Modify a member's roles in the network.
* Suspend or revoke membership.

{{< note >}}
The code samples in this documentation show you how to run management operations using the provided primitives from the context of a tool or Cordapp. It is also possible to do these operations from an RPC client or node shell by simply invoking the supplied administrative flows using data resulted from executing vault queries.
{{< /note >}}

### Members, authorised members, and Business Network Operators

In a Business Network, you can assign different roles to members of the network. In this documentation, and throughout your network in general, you may encounter the following type of members:

* **Business Network Operator** - has all administrative permissions in the Business Network.
* **Authorised member** - has at least the required administrative permissions to perform a certain task.
* **Member** - may not have administrative permissions but is still a member of the group.

## Installation

This is an extension for Corda 4.8. If you have this version of Corda, you can access the required `.jar` files here:

* BNE contracts: [https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-contracts/1.1/business-networks-contracts-1.1.jar](https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-contracts/1.1/business-networks-contracts-1.1.jar).
* BNE workflows: [https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-workflows/1.1/business-networks-workflows-1.1.jar](https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-workflows/1.1/business-networks-workflows-1.1.jar).
* Sample CorDapp contracts: [https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-demo-contracts/1.1/business-networks-demo-contracts-1.1.jar](https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-demo-contracts/1.1/business-networks-demo-contracts-1.1.jar).
* Sample CorDapp workflows: [https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-demo-workflows/1.1/business-networks-demo-workflows-1.1.jar](https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-releases/net/corda/bn/business-networks-demo-workflows/1.1/business-networks-demo-workflows-1.1.jar).

To install the extension:

1. Add the `business-networks-contracts` dependency in your **contracts** (and states) CorDapp module:

```
dependencies {
    //...
    cordapp("net.corda.bn:business-networks-contracts:$corda_bn_extension_version")
    //...
}
```
2. Add the `business-networks-workflows` dependency in your **workflows** CorDapp module:

```
dependencies {
    //...
	cordapp("net.corda.bn:business-networks-workflows:$corda_bn_extension_version")
    //...
}
```

3. Add both dependencies in your **Cordform** - `deployNodes` - [task](generating-a-node.md#tasks-using-the-cordform-plug-in).

You have installed the Business Network membership extension.

## Create a business network

From either the node shell or from an RPC client, run `CreateBusinessNetworkFlow`. This will self-issue a membership with an exhaustive permissions set that allows the calling node to manage future operations for the newly created network.

**Flow arguments:**

- `networkId`: Custom ID to be given to the new Business Network. If not specified, a randomly selected one will be used.
- `businessIdentity`: Optional custom business identity to be given to the membership.
- `groupId`: Custom ID to be given to the initial Business Network group. If not specified, randomly selected one will be used.
- `groupName`: Optional name to be given to the Business Network group.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:
```kotlin
val myIdentity: BNIdentity = createBusinessNetworkIdentity() // mock method that creates an instance of a class implementing [BNIdentity]
val businessNetworkId = UniqueIdentifier()
val groupId = UniqueIdentifier()
val notary = serviceHub.networkMapCache.notaryIdentities.first()

subFlow(CreateBusinessNetworkFlow(businessNetworkId, myIdentity, groupId, "Group 1", notary))
```

## Onboarding a new member to your network

You can onboard a new member to your network:

* With prior request from the prospective member.
* Without prior request from the prospective member.

You can also onboard and activate memberships in batches using [Composite flows](#onboard-and-activate-members-with-composite-flows).

### Onboard a new member with prior request

You can make joining a business network a two-step process, in which prospective members must first send a request to join the network. The request can then be approved by the relevant parties, and the member is added.

#### Step 1 - prospective member sends a membership request

1. The Corda node wishing to join must run the `RequestMembershipFlow` either from the node shell or any other RPC client.
2. As a result of a successful run, a membership is created with a `PENDING` status and all authorised members will be notified of any future operations involving it.
3. The prospective member awaits action to activate their membership by an authorised member of the network.

Until activated by an authorised party, such as a Business Network Operator (BNO), the newly generated membership can neither be used nor grant the requesting node any permissions in the business network.

**RequestMembershipFlow arguments**:

- `authorisedParty`: Identity of authorised member from whom membership activation is requested.
- `networkId`: ID of the Business Network that potential new member wants to join.
- `businessIdentity`: Optional custom business identity to be given to the membership.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val myIdentity: BNIdentity = createBusinessNetworkIdentity() // create an instance of a class implementing [BNIdentity]
val networkId: UniqueIdentifier = ... // user provided network unique identifier
val bno: Party = ... // get the [Party] object of the Corda node acting as a BNO for the business network represented by [networkId]
val notary = serviceHub.networkMapCache.notaryIdentities.first())

subFlow(RequestMembershipFlow(bno, networkId, myIdentity, notary))
```

#### Step 2 - an authorised network member activates the new membership

To finalise the on-boarding process:

1. As an authorised member, such as BNO, run the `ActivateMembershipFlow` to update the targeted membership status from `PENDING` to `ACTIVE`.
2. Signatures are collected from **all** authorised parties in the network.
3. Follow up with a group assignment by running the `ModifyGroupFlow`.

**ActivateMembershipFlow arguments**:

- `membershipId`: ID of the membership to be activated.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

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

### Onboard a new member without prior request

As an authorised member of the network, you can onboard a new member without needing a prior membership request. The joining party is immediately added to the network with an `ACTIVE` status. You can then add the member directly to the relevant groups.

1. Run `OnboardMembershipFlow` to directly issue a new membership with `ACTIVE` status.
2. Run `ModifyGroupFlow` to assign the new member to the correct groups.

**OnboardMembershipFlow arguments**:

- `networkId`: ID of the Business Network that member is onboarded to.
- `onboardedParty`: Identity of an onboarded member.
- `businessIdentity`: Custom business identity to be given to the onboarded membership.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

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

### Onboard and activate members with composite flows

To save time and effort, you can use composite flows to perform batch membership onboarding and activation. You can call multiple primitive Business Network management flows (flows under the `net.corda.bn.flows` package) contained within a single flow from the `net.corda.bn.flows.composite` package.

There are two composite flows:

* `BatchOnboardMembershipFlow`: Onboards a set of new memberships and adds them to the specified groups.
* `BatchActivateMembershipFlow`: Activates a set of pending membership requests and adds them to the specified groups.

**BatchOnboardMembershipFlow arguments**:

* `networkId`: ID of the Business Network where members are onboarded.
* `onboardedParties`: Set of parties to be onboarded and group where to be added after onboarding.
* `defaultGroupId`: ID of the group where members are added if the specific group ID is not provided in their `OnboardingInfo`.
* `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

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

**BatchActivateMembershipFlow arguments**:

* `memberships`: Set of memberships' `ActivationInfo`s.
* `defaultGroupId`: ID of the group where members are added if the specific group ID is not provided in their `ActivationInfo`.
* `notary`: Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used.

*Example*:

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

## Amend a membership

There are attributes of a member's information that can be updated, not including network operations such as membership suspension or revocation. To perform these amendments, you must be an authorised network party.

The attributes which can be amended are:

* Business network identity.
* Membership list or group.
* Roles.

### Update a members business identity attribute

To update a member's business identity attribute:

1. Run the `ModifyBusinessIdentityFlow`.
2. All network members with sufficient permissions approve the proposed change.

**ModifyBusinessIdentityFlow arguments**:

- `membershipId`: ID of the membership to modify business identity.
- `businessIdentity`: Optional custom business identity to be given to the membership.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val bnService = serviceHub.cordaService(BNService::class.java)
val networkId: UniqueIdentifier = ... // id of the network containing the member whose business identity is being updated
val partyToBeUpdated = ... // get the [Party] object of the member being updated
val membership = bnService.getMembership(networkId, partyToBeUpdated)
val updatedIdentity: BNIdentity = updateBusinessIdentity(membership.state.data.identity) // mock method that updates the business identity in some meaningful way
val notary = serviceHub.networkMapCache.notaryIdentities.first())

subFlow(ModifyBusinessIdentityFlow(membership.state.data.linearId, updatedIdentity, notary))
```

### Update a members business network roles

You can also update a member's business identity attributes by modifying their roles. Depending on your proposed changes, the updated member may become an **authorised member**. In this case, your enhancement must be preceded by an execution of the [`ModifyGroupsFlow`](#modify-a-group) to add the member to all membership lists that it will have administrative powers over.

To update a member's roles and permissions in the business network:

1. Run the `ModifyRolesFlow`.
2. All network members with sufficient permissions approve the proposed change.

**ModifyRolesFlow arguments**:

- `membershipId`: ID of the membership to assign roles.
- `roles`: Set of roles to be assigned to the membership.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

There are two additional flows that can be used to quickly assign roles to a membership: `AssignBNORoleFlow` and `AssignMemberRoleFlow`. They both share the same arguments:

- `membershipId`: ID of the membership to assign the role.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val roles = setOf(BNORole()) // assign all administrative permissions to member
val bnService = serviceHub.cordaService(BNService::class.java)
val networkId: UniqueIdentifier = ... // id of the network containing the member whose roles are updated
val partyToBeUpdated = ... // get the [Party] object of the member being updated
val membershipId = bnService.getMembership(networkId, partyToBeUpdated).state.data.linearId
val notary = serviceHub.networkMapCache.notaryIdentities.first())

subFlow(ModifyRolesFlow(membershipId, roles, notary))
```

## Manage groups

To manage the membership lists or groups, one of the authorised members of the network can use `CreateGroupFlow`, `DeleteGroupFlow`, and `ModifyGroupFlow`.

{{< note >}}
When modifying a group, you must ensure that any member who is removed from the group is still part of at least one Business Network Group, otherwise they will no longer be discoverable.
{{< /note >}}

### Create a group

To create a new group:

1. Run `CreateGroupFlow`.
2. All network members with sufficient permissions approve the proposed change.

**CreateGroupFlow arguments**:

- `networkId`: ID of the Business Network that the target Business Network Group will relate to.
- `groupId`: Custom ID to be given to the issued Business Network Group. If not specified, a randomly generated ID will be used.
- `groupName`: Optional name to be given to the issued Business Network Group.
- `additionalParticipants`: Set of participants to be added to issued Business Network Group alongside initiator's identity.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

**Example**:

```kotlin
val myNetworkId: UniqueIdentifier = ... // id of the network for which groups are created
val myGroupId = UniqueIdentifier()
val groupName = "Group 1"
val notary = serviceHub.networkMapCache.notaryIdentities.first())

subFlow(CreateGroupFlow(myNetworkId, myGroupId, groupName, emptySet(), notary))
```

### Delete a group

To delete a group:

1. Run `DeleteGroupFlow`.
2. All network members with sufficient permissions approve the proposed change.

**DeleteGroupFlow arguments**:

- `groupId`: ID of group to be deleted.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

### Modify a group

The `ModifyGroupFlow` can update the name of a group and/or its list of members. At least one of the *name* or *participants* arguments
must be provided (see below).

To modify a group:

1. Run `ModifyGroupFlow`.
2. All network members with sufficient permissions approve the proposed change.

**ModifyGroupFlow arguments**:

- `groupId`: ID of group to be modified.
- `name`: New name of the modified group.
- `participants`: New participants of the modified group.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

**Example**:

```kotlin
val bnService = serviceHub.cordaService(BNService::class.java)
val bnGroupId: UniqueIdentifier = ... // get the identifier of the group being updated
val bnGroupName = bnService.getBusinessNetworkGroup(bnGroupId).state.data.name
val participantsList = bnService.getBusinessNetworkGroup(bnGroupId).state.data.participants
val newParticipantsList = removeMember(someMember, participantsList) // mock method that removes a member from the group
val notary = serviceHub.networkMapCache.notaryIdentities.first())

subFlow(ModifyGroupFlow(bnGroupId, bnGroupName, newParticipantsList, notary))
```

## Suspend or revoke a membership

You can temporarily suspend a member or completely remove them from the business network. Suspending a member will result in a membership status change to `SUSPENDED` and still allow said member to be in the business network. Revocation means that the membership is marked as historic/spent and and a new one will have to be requested and activated in order for the member to re-join the network.

When a membership is revoked, the member is also removed from all Business Network Groups.

To suspend a member of the network:

1. Run `SuspendMembershipFlow`.
2. All network members with sufficient permissions approve the proposed change.

To remove membership completely:

1. Run `RevokeMembershipFlow`.
2. All network members with sufficient permissions approve the proposed change.

Both `SuspendMembershipFlow` and `RevokeMembershipFlow` use the same arguments:

- `membershipId`: ID of the membership to be suspended/revoked.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

**Example**:

```kotlin
val notary = serviceHub.networkMapCache.notaryIdentities.first())
val memberToBeSuspended = ... // get the linear ID of the membership state associated with the Party which is being suspended from the network
val memberToBeRevoked = ... // get the linear ID of the membership state associated with the Party which is being removed from the network
// Revocation
subFlow(RevokeMembershipFlow(memberToBeRevoked, notary))

// Suspension
subFlow(SuspendMembershipFlow(memberToBeRevoked, notary))
```

## Request membership attribute changes

Using the `RequestMembershipAttributeChangeFlow` flow, a member can create requests in order to change its attributes (business identity and roles).
This flow will create a `ChangeRequestState` with `PENDING` status.

{{< note >}}
When you request new roles, the changes will overwrite your existing roles.
{{< /note >}}

As an authorised member you can:

* Decline the requested changes using `DeclineMembershipAttributeChangeFlow`. If you decline the request the existing `ChangeRequestState` will have `DECLINED` status.
* Accept using `ApproveMembershipAttributeChangeFlow`. If you accept the request the existing `ChangeRequestState` will have `ACCEPTED` status.
* Mark the request as consumed using `DeleteMembershipAttributeChangeRequestFlow`. This avoids stockpiling requests in the database.

**RequestMembershipAttributeChangeFlow arguments**:

- `authorisedParty`: Identity of authorised member from whom the change request approval/rejection is requested.
- `networkId`: ID of the Business Network that members are part of.
- `businessIdentity`: The proposed business identity change.
- `roles`: The proposed role change.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val authorisedParty: Party = ... // get the [Party] object of the authorised Corda node
val networkId = "MyBusinessNetwork"
val updatedIdentity: BNIdentity = ... // the new business identity you want to associate the member with, if you don't want to modify your existing business identity, then simply skip this step
val updatedRoles: Set<BNRole> = ... // the new roles you want to associate the member with, if you don't want to modify your existing roles, then simply skip this step
val notary = serviceHub.networkMapCache.notaryIdentities.first()

// Request creation
subFlow(RequestMembershipAttributeChangeFlow(authorisedParty, networkId, updatedIdentity, updatedRoles, notary))
```

**ApproveMembershipAttributeChangeFlow arguments**:

- `requestId`: The ID of the request which needs to be accepted.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val requestId = ... // get the linear ID of the change request state associated with the Party which is requesting for attribute changes
val notary = serviceHub.networkMapCache.notaryIdentities.first()

// Approves request
subFlow(ApproveMembershipAttributeChangeFlow(requestId, notary))
```

**DeclineMembershipAttributeChangeFlow arguments**:

- `requestId`: The ID of the request which needs to be rejected.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val requestId = ... // get the linear ID of the change request state associated with the Party which is requesting for attribute changes
val notary = serviceHub.networkMapCache.notaryIdentities.first()

// Declines request
subFlow(DeclineMembershipAttributeChangeFlow(requestId, notary))
```

**DeleteMembershipAttributeChangeRequestFlow arguments**:

- `requestId`: The ID of the request which needs to be consumed.
- `notary`: Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val requestId = ... // get the linear ID of the change request state associated with the Party which is requesting for attribute changes
val notary = serviceHub.networkMapCache.notaryIdentities.first()

// Marks request as CONSUMED
subFlow(DeleteMembershipAttributeChangeRequestFlow(requestId, notary))
```

## Access control report

As the Business Network Operator (BNO), you can ask for the access control report by calling `BNOAccessControlReportFlow`. You will receive the following information in the form of an `AccessControlReport`.

The attributes of the report file are:

* `members`: A detailed list of the members within the network. It contains the following information:
    * `cordaIdentity`: The Corda identity of the member.
    * `businessIdentity`: The business identity of the member.
    * `membershipStatus`: The current status of the member's membership.
    * `groups`: A list of all the groups the member is part of.
    * `roles`: A list of the roles the member has.
* `groups`: A detailed list of the groups within the network. It contains the following information:
    * `name`: The name of the group.
    * `participants`: A list of the participants in the group.

 **BNOAccessControlReportFlow arguments**:

* `networkId`: ID of the Business Network, where the participants are present.
* `path`: The chosen path for the report file to be placed.
* `fileName`: The chosen file name of the report file.

`path` and `fileName` are optional arguments - if unspecified, they take the default values `user.dir` and `bno-access-control-report`, respectively.

*Example*:

```kotlin
val networkId = "MyBusinessNetwork"
val path = ... // the absolute path where the report file should be placed
val fileName = ... // the name of the report file

subFlow(BNOAccessControlReportFlow(networkId, path, fileName))
```

## Reissue states affected by the change to a member's Corda Identity

It may happen that a member in the network needs to reissue the certificate to which its Corda Identity binds. In that case, all membership and group states, which are impacted, should be reissued with the new Corda Identity. This can be done using the `UpdateCordaIdentityFlow`. Please note that this flow requires the legal identity (CordaX500Name) to be the same. Furthermore, the flow can only be run from a member with sufficient permissions (who can modify groups).

**If several members of the network have their certificates rotated, it is important to start the identity update process with the authorised members as they are required
to sign all other identity update transactions.**

**UpdateCordaIdentityFlow arguments**:

- `membershipId`: The `membershipId` ID of the membership whose Corda Identity has changed.
- `notary`: The Identity of the notary to be used for transactions notarisation. If not specified, the first one from the whitelist will be used.

*Example*:

```kotlin
val notary = serviceHub.networkMapCache.notaryIdentities.first())
val updatedMember = ... // get the linear ID of the membership state associated with the Party which was updated

subflow(UpdateCordaIdentityFlow(updatedMember, notary))
```

## Business Network management demo

This demo showcases integration of Business Networks solution inside a CorDapp designed for issuing and settling loans between banks. It brings up 4 nodes: a notary and 3 nodes representing banks. Each bank node must be active member of the same Business Network, have a Swift Business Identifier Code (BIC) as their business identity and loan issuance initiators must be granted permission to do so.

### Flows

RPC exposed flows can be divided into 2 groups:

* Standard Business Network management flows (covered in this documentation).
* CorDapp specific ones.

### CorDapp specific flows

- `AssignBICFlow` assigns **BIC** (Swift Business Identifier Code) as a business identity of a bank node.
    - Usage: `flow start AssignBICFlow membershipId: <UNIQUE_IDENTIFIER>, bic: <STRING>, notary: <OPTIONAL_NOTARY_IDENTITY>`.
- `AssignLoanIssuerRoleFlow` grants loan issuance permission to a calling party. This is self-granting.
    - Usage: `flow start AssignLoanIssuerRoleFlow networkId: <STRING>, notary: <OPTIONAL_NOTARY_IDENTITY>`.
- `IssueLoanFlow` issues new loan state on ledger between caller as lender and borrower specified as flow argument. It also
  performs verification of both parties to ensure they are active members of Business Network with ID specified as
  flow argument. Existence of BIC as business identity is checked and whether flow caller has permission to issue loan.
    - Usage: `flow start IssueLoanFlow networkId: <STRING>, borrower: <PARTY>, amount: <INT>`.
- `SettleLoanFlow` decreases loan's amount by amount specified as flow argument. If it fully settles the loan, associated
  state is consumed. It also verifies both parties are active members of a Business Network loan belongs to and that
  they both have BIC as business identity.
    - Usage: `flow start SettleLoanFlow loanId: <UNIQUE_IDENTIFIER>, amountToSettle: <INT>`

## Sample usage

To deploy and run nodes from the command line in Unix:

1. Run `./gradlew business-networks-demo:deployNodes` to create a set of configs and installs under
   `business-networks-demo/build/nodes`.

2. Run `./business-networks-demo/build/nodes/runnodes` to open up 4 new terminal tabs/windows with 3 bank nodes

To deploy and run nodes from the command line in Windows:

1. Run `gradlew business-networks-demo:deployNodes` to create a set of configs and installs under
   `business-networks-demo/build/nodes`
2. Run `business-networks-demo\build\nodes\runnodes` to open up 4 new terminal tabs/windows with 3 bank nodes

Next steps are same for every OS (Windows/Mac/Linux).

### Create a Business Network environment

1. Create a Business Network from *Bank A* node by running `flow start CreateBusinessNetworkFlow`.

2. Obtain network ID and initial group ID from *Bank A* by running:
   `run vaultQuery contractStateType: net.corda.core.contracts.ContractState` and looking into latest
   `MembershipState` and `GroupState` issued

3. Request membership from *Bank B* and *Bank C* nodes by running:
   `flow start RequestMembershipFlow authorisedParty: Bank A, networkId: <OBTAINED_NETWORK_ID>, businessIdentity: null, notary: null`

4. Obtain requested membership IDs for *Bank B* and *Bank C* by running:
   `run vaultQuery contractStateType: net.corda.core.contracts.ContractState` on *Bank A* node and looking
   into `linearId` of newly issued `MembershipState`s.

5. Activate *Bank B* and *Bank C* membership requests from *Bank A* node by running
   `flow start ActivateMembershipFlow membershipId: <LINEAR_ID>, notary: null` for each requested membership.

6. Add newly activated *Bank B* and *Bank C* members into initial group by running
   `flow start ModifyGroupFlow groupId: <OBTAINED_GROUP_ID>, name: null, participants: [<BANK_A_ID>, <BANK_B_ID>, <BANK_C_ID>], notary: null`
   on *Bank A* node.

7. Assign BIC to each of 3 bank nodes by running
   `flow start AssignBICFlow membershipId: <LINEAR_ID>, bic: <STRING>, notary: null` on *Bank A* node
   (examples of valid BIC - "BANKGB00", "CHASUS33XXX").

8. Assign Loan Issuer role to *Bank A* by running
   `flow start AssignLoanIssuerRoleFlow networkId: <OBTAINED_NETWORK_ID>, notary: null` on *Bank A* node

### Issue and settle a loan

1. Issue loan from *Bank A* to *Bank B* by running:
   `flow start IssueLoanFlow networkId: <OBTAINED_NETWORK_ID>, borrower: Bank B, amount: 10` on *Bank A* node.

2. Obtain loan ID from *Bank B* node by running:
   `run vaultQuery contractStateType: net.corda.bn.demo.contracts.LoanState` and looking into `linearId`.

3. Settle loan by running `flow start SettleLoanFlow loanId: <OBTAINED_LOAN_ID>, amountToSettle: 5` on *Bank B* node.

4. Check loan state amount decreased to `5` on both bank nodes.

5. Fully settle loan by running `flow start SettleLoanFlow loanId: <OBTAINED_LOAN_ID>, amountToSettle: 5` again on *Bank B* node.

6. Check loan state was consumed on both bank nodes.
