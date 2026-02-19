---
aliases:
- /head/node-operations-upgrade-cordapps.html
- /HEAD/node-operations-upgrade-cordapps.html
- /node-operations-upgrade-cordapps.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4.14:
    identifier: corda-community-4.14-node-operations-upgrade-cordapps
    parent: corda-community-4.14-corda-nodes-index
    weight: 1100
tags:
- node
- operations
- upgrade
- cordapps
title: Upgrading CorDapps on a node
---


# Upgrading CorDapps on a node

In order to upgrade a CorDapp on a node to a new version, it needs to be determined whether any backwards compatible
changes have been made. These could range from database changes, to changes in the protocol.

For developer information on upgrading CorDapps, see [Release new CorDapp versions]({{< relref "upgrading-cordapps.md" >}}).

CorDapps must ship with database migration scripts or clear documentation about how to update the database to be compatible with the new version.


## Flow upgrades

If any backwards-incompatible changes have been made (see [What constitutes a non-backwards compatible flow change?]({{< relref "upgrading-cordapps.md" >}})
for more information), the upgrade method detailed below will need to be followed. Otherwise the CorDapp JAR can just
be replaced with the new version.


## Contract and state upgrades

There are two types of contract and state upgrade that you can perform:


- **Implicit:** Allow multiple implementations of the contract ahead of time, using constraints. See
[API: Contract constraints]({{< relref "api-contract-constraints.md" >}}) to learn more.
- **Explicit:** Create a special *contract upgrade transaction* and getting all participants of a state to sign it using the
contract upgrade flows.

This topic covers the *explicit* type of upgrade, as implicit contract upgrades are handled by the CorDapp.

In an explicit upgrade, contracts and states can be changed in arbitrary ways, only if all of the state’s participants
agree to the proposed upgrade. The following combinations of upgrades are possible:


* A contract is upgraded while the state definition remains the same.
* A state is upgraded while the contract stays the same.
* The state and the contract are updated simultaneously.


## Performing the upgrade

If a contract or state requires an explicit upgrade, update all states to the new contract at a time all the participants agree on.
by all participants. The updated CorDapp JAR needs to be distributed to all relevant parties in advance of the changeover
time.

To perform the upgrade:


1. Drain the node to avoid the definition of states or contracts changing whilst a flow is in progress. See [Flow drains]({{< relref "upgrading-cordapps.md#flow-drains" >}}) for more information. There are two ways you can drain the node:
   - **By RPC:** Use the `setFlowsDrainingModeEnabled` method with the parameter `true`.
   - **Via the shell:** Run the following command: `run setFlowsDrainingModeEnabled enabled: true`.
2. Check that all the flows have completed:
   - **By RPC:** Use the `stateMachinesSnapshot` method and checking that there are no results
   - **Via the shell:** Run the following command: `run stateMachinesSnapshot`
      {{< note >}}The `stateMachinesSnapshot` method ties the flow ID with the `flowName` class. The result shows you all the flows running in your node. You can use the `flow watch` method instead. It omits all the details returned by `stateMachinesSnapshot` that you do not need.{{< /note >}}
3. Once all flows have completed, stop the node.
4. Replace the existing JAR with the new version.
5. Make any required database changes to any custom vault tables for the upgraded CorDapp by following the database upgrade steps in [Release new CorDapp versions]({{< relref "upgrading-cordapps.md" >}}). Database changes required for a CorDapp upgrade follow the same steps as those to set up a database for a new CorDapp.
6. Restart the node.
7. If you drained the node prior to upgrading, switch off flow draining mode. This allows the node to continue to receive requests. There are two ways you can switch off flow draining mode:
   - **By RPC:** Use the `setFlowsDrainingModeEnabled` method with the parameter `false`.
   - **Via the shell:** Run the following command: `run setFlowsDrainingModeEnabled enabled: false`
7. Run the contract upgrade authorisation flow (`ContractUpgradeFlow$Initiate`) for each state that requires updating on every node.
   - You can do this manually via RPC but for anything more than a couple of states it is assumed that a script will be
provided by the CorDapp developer to query the vault and run this for all states.
   - The contract upgrade initiate flow only needs to be run on one of the participants for each state. The flow will
automatically upgrade the state on all participants.
