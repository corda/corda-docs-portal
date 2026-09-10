---
date: '2021-08-11'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-upgrading-menu
tags:
- node
- operations
- upgrade
- cordapps
aliases: /docs/4.14/enterprise/node/operating/node-operations-upgrade-cordapps.html
title: Upgrading deployed CorDapps
weight: 50
---

# Upgrading deployed CorDapps

For developer information on upgrading CorDapps, see [release new CorDapp versions]({{< relref "cordapps/upgrading-cordapps.md" >}}).

{{< warning >}}

To be compatible with Corda Enterprise, CorDapps need to bundle database migration scripts. See [Database management scripts]({{< relref "cordapps/database-management.md" >}}) for more information.

{{< /warning >}}

## Check for backwards-compatible changes

Before you upgrade a CorDapp on a node, you need to determine if any backwards-compatible
changes have been made, such as  database changes or changes in the protocol.

If any backwards-incompatible changes have been made (see [what constitutes a non-backwards compatible flow change?]({{< relref "cordapps/upgrading-cordapps.md#non-backwards-compatible-flow-changes" >}})
for more information), you need to follow the upgrade method detailed below. Otherwise, the CorDapp JAR can just
be replaced with the new version.


## Contract and state upgrades

There are two types of contract and state upgrade that you can perform.


- **Implicit:** Allow multiple implementations of the contract ahead of time, using constraints. See
[Contract constraints]({{< relref "cordapps/api-contract-constraints.md" >}}) to learn more.
- **Explicit:** Create a special *contract upgrade transaction* and require all participants of a state to sign it using the
contract upgrade flows.

This topic covers the *explicit* type of upgrade, as implicit contract upgrades are handled by the CorDapp.

In an explicit upgrade, contracts and states can be changed in arbitrary ways only if all of the state’s participants
agree to the proposed upgrade. The following combinations of upgrades are possible:


* A contract is upgraded while the state definition remains the same.
* A state is upgraded while the contract stays the same.
* The state and the contract are updated simultaneously.


## Performing the upgrade

If a contract or state requires an explicit upgrade, update all states to the new contract at a time all the participants agree on.
by all participants. The updated CorDapp JAR needs to be distributed to all relevant parties in advance of the changeover
time.

To perform the upgrade:

1. Drain the node to avoid the definition of states or contracts changing whilst a flow is in progress. See [Draining the node]({{< relref "cordapps/upgrading-cordapps.md#draining-the-node" >}}) for more information. There are two ways you can drain the node:
   - **By RPC:** Use the `setFlowsDrainingModeEnabled` method with the parameter `true`.
   - **Via the shell:** Run the following command: `run setFlowsDrainingModeEnabled enabled: true`.
2. Check that all the flows have completed:
   - **By RPC:** Use the `stateMachinesSnapshot` method and checking that there are no results
   - **Via the shell:** Run the following command: `run stateMachinesSnapshot`
      {{< note >}}The `stateMachinesSnapshot` method ties the flow ID with the `flowName` class. The result shows you all the flows running in your node. You can use the `flow watch` method instead. It omits all the details returned by `stateMachinesSnapshot` that you do not need.{{< /note >}}
3. Once all flows have completed, stop the node.
4. Replace the existing JAR with the new version.
5. Make any required database changes to any custom vault tables for the upgraded CorDapp by following the database upgrade steps in [Installing CorDapps on a node]({{< relref "node/operating/node-operations-cordapp-deployment.md" >}}). Database changes required for a CorDapp upgrade follow the same steps as those to set up a database for a new CorDapp.
6. Restart the node.
7. If you drained the node prior to upgrading, switch off flow draining mode. This allows the node to continue to receive requests. There are two ways you can switch off flow draining mode:
   - **By RPC:** Use the `setFlowsDrainingModeEnabled` method with the parameter `false`.
   - **Via the shell:** Run the following command: `run setFlowsDrainingModeEnabled enabled: false`
8. Run the contract upgrade authorization flow `ContractUpgradeFlow$Initiate` for each state that needs to be updated.
You can do this manually via RPC. However, if there are more than a couple of states, you should provide a script that queries the vault and runs this flow for all states.
  Only one participant for each state need run `ContractUpgradeFlow$Initiate`. The flow automatically upgrades the state for all participants.
