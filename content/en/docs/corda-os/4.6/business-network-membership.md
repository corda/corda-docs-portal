---
date: '2020-09-25T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-business-network-management
    parent: corda-os-4-6-corda-networks-index
    weight: 1200
tags:
- BNO
- notary
title: Managing Business Network membership
---

# Business Network management

This Corda platform extension allows you to create and manage business networks - as a node operator, this means you can define and create a logical network based on a set of common CorDapps as well as a shared business context.

Corda nodes outside of your business network are not aware of its members. The network can be split into subgroups or membership lists which allows for further privacy (members of a group only know about those in their group).

In a business network, there is at least one *authorised member*. This member has sufficient permissions to execute management operations over the network and its members.

{{< warning >}}
In this version, it is possible for an authorised member - such as the Business Network Operator - to remove permissions from itself, potentially leaving the network in a state where no member can perform management operations.  In such a case, permissions can be granted back by other members who are authorised to do so. If there are none left, there is no way of recovering.
{{< /warning >}}

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

### Members, authorised members and Business Network Operators

In a Business Network, you can assign different roles to members of the network. In this documentation, and throughout your network in general, you may encounter the following type of members:

* Business Network Operator - has all administrative permissions in Business Network.
* Authorised member - has at least the required administrative permissions to perform a certain task.
* Member - may not have administrative permissions but is still a member of the group.

## Installation

This is an extension of Corda OS 4.6. If you have this version of Corda, and want to set up and run a Business Network, you can make use of the extension flows.

## Create a business network

From either the node shell or from an RPC client, run `CreateBusinessNetworkFlow`. This will self-issue a membership with an exhaustive permissions set that allows the calling node to manage future operations for the newly created network.

**Flow arguments:**

- ```networkId``` Custom ID to be given to the new Business Network. If not specified, a randomly selected one will be used.
- ```businessIdentity``` Optional custom business identity to be given to membership.
- ```groupId``` Custom ID to be given to the initial Business Network group. If not specified, randomly selected one will be used.
- ```groupName``` Optional name to be given to the Business Network group.
- ```notary``` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used.

*Example*:
```kotlin
val myIdentity: BNIdentity = createBusinessNetworkIdentity() // mock method that creates an instance of a class implementing [BNIdentity]
val businessNetworkId = UniqueIdentifier()
val groupId = UniqueIdentifier()
val notary = serviceHub.networkMapCache.notaryIdentities.first()

subFlow(CreateBusinessNetworkFlow(businessNetworkId, myIdentity, groupId, "Group 1", notary))
```

## On-board a new member

Joining a business network is a 2 step process. First the prospective member must send a request. Then the request is approved and the member is added.

### Step 1 - prospective member sends a membership request

1. The Corda node wishing to join must run the ```RequestMembershipFlow``` either from the node shell or any other RPC client.
2. As a result of a successful run, a membership is created with a *PENDING* status and all authorised members will be notified of any future operations involving it.
3. The prospective member awaits action to activate their membership by an authorised member of the network.


Until activated by an authorised party, such as a Business Network Operator (BNO), the newly generated membership can neither be used nor grant the requesting node any permissions in the business network.

**RequestMembershipFlow arguments**:

- ```authorisedParty``` Identity of authorised member from whom membership activation is requested
- ```networkId``` ID of the Business Network that potential new member wants to join
- ```businessIdentity``` Optional custom business identity to be given to membership
- ```notary``` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used

*Example*:

```kotlin
val myIdentity: BNIdentity = createBusinessNetworkIdentity() // create an instance of a class implementing [BNIdentity]
val networkId: UniqueIdentifier = ... // user provided network unique identifier
val bno: Party = ... // get the [Party] object of the Corda node acting as a BNO for the business network represented by [networkId]
val notary = serviceHub.networkMapCache.notaryIdentities.first())

subFlow(RequestMembershipFlow(bno, networkId, myIdentity, notary))
```

### Step 2 - an authorised network member activates the new membership

To finalise the on-boarding process:

1. As an authorised member, such as BNO, run the ```ActivateMembershipFlow``` to update the targeted membership status from *PENDING* to *ACTIVE*.
2. Signatures are collected from **all** authorised parties in the network.
3. Follow-up with a group assignment by running the ```ModifyGroupFlow```.

**ActivateMembershipFlow arguments**:

- ```membershipId``` ID of the membership to be activated
- ```notary``` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used

*Example*:

```kotlin
val bnService = serviceHub.cordaService(BNService::class.java)
val networkId: UniqueIdentifier = ... // id of the business network for which membership activation is done
val newMemberPartyObject = ... // get the [Party] object of the member whose membership is being activated
val membershipId = bnService.getMembership(networkId, newMemberPartyObject)
val groupName = ... // name of the group which the member will be assigned to
val groupId = ... // identifier of the group which the member will be assigned to
val notary = serviceHub.networkMapCache.notaryIdentities.first())

subFlow(ActivateMembershipFlow(membershipId, notary)
// add newly activated member to a membership list
val newParticipantsList = bnService.getBusinessNetworkGroup(groupId).state.data.participants.map {
    bnService.getMembership(networkId, it)!!.state.data.linearId
} + membershipId

subFlow(ModifyGroupFlow(groupId, groupName, newParticipantsList, notary))
```

## Amend a membership

There are attributes of a member's information that can be updated, not including network operations such as membership suspension or revocation. To perform these amendments, you must be an authorised network party.

The attributes which can be amended are:

* Business network identity.
* Membership list or group.
* Roles.

### Update a members business identity attribute

To update a member's business identity attribute:

1. Run the ```ModifyBusinessIdentityFlow```.
2. All network members with sufficient permissions approve the proposed change.

**ModifyBusinessIdentityFlow arguments**:

- ```membershipId``` ID of the membership to modify business identity
- ```businessIdentity``` Optional custom business identity to be given to membership
- ```notary``` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used

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

You can update a member's business identity attributes - by modifying their roles. Depending on your proposed changes, the updated member may become an **authorised member**. In this case, your enhancement must be preceded by an execution of the [`ModifyGroupsFlow`](#modify-a-group) to add the member to all membership lists that it will have administrative powers over.

To update a member's roles and permissions in the business network:

1. Run the `ModifyRolesFlow`.
2. All network members with sufficient permissions approve the proposed change.

**ModifyRolesFlow arguments**:

- `membershipId` ID of the membership to assign roles
- `roles` Set of roles to be assigned to membership
- `notary` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used

There are two additional flows that can be used to quickly assign roles to a membership: `AssignBNORoleFlow` and `AssignMemberRoleFlow`. They both share the same arguments:

- `membershipId` ID of the membership to assign the role.
- `notary` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used.
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

To manage the membership lists or groups, one of the authorised members of the network can use `CreateGroupFlow`, `DeleteGroupFlow` and `ModifyGroupFlow`.

{{< note >}}
When modifying a group, you must ensure that any member who is removed from the group is still part of at least one Business Network Group, otherwise they will no longer be discoverable.
{{< /note >}}
### Create a group

To create a new group:

1. Run `CreateGroupFlow`.
2. All network members with sufficient permissions approve the proposed change.

**CreateGroupFlow arguments**:

- `networkId` ID of the Business Network that the target Business Network Group will relate to.
- `groupId` Custom ID to be given to the issued Business Network Group. If not specified, a randomly generated ID will be used.
- `groupName` Optional name to be given to the issued Business Network Group.
- `additionalParticipants` Set of participants to be added to issued Business Network Group alongside initiator's identity.
- `notary` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used.

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

- `groupId` ID of group to be deleted
- `notary` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used

### Modify a group

The `ModifyGroupFlow` can update the name of a group and/or its list of members. At least one of the *name* or *participants* arguments
must be provided.

To modify a group:

1. Run `ModifyGroupFlow`.
2. All network members with sufficient permissions approve the proposed change.

**ModifyGroupFlow arguments**:

- `groupId` ID of group to be modified
- `name` New name of modified group
- `participants` New participants of modified group
- `notary` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used

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

- `membershipId` ID of the membership to be suspended/revoked
- `notary` Identity of the notary to be used for transactions notarisation. If not specified, first one from the whitelist will be used

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
