---
date: '2021-08-11'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-upgrading-menu
tags:
- node
- operations
- upgrade
- cordapps
aliases: /docs/4.9/enterprise/node/operating/node-operations-upgrade-cordapps.html
title: Upgrading deployed CorDapps
weight: 50
---

# Upgrading deployed CorDapps

For developer information on upgrading CorDapps, see [release new CorDapp versions]({{< relref "../../../../../en/platform/corda/4.9/enterprise/cordapps/upgrading-cordapps.md" >}}).

{{< warning >}}

To be compatible with Corda Enterprise, CorDapps need to bundle database migration scripts. See [database management scripts]({{< relref "../../../../../en/platform/corda/4.9/enterprise/cordapps/database-management.md" >}}) for more information.

{{< /warning >}}

## Check for backwards-compatible changes

Before you upgrade a CorDapp on a node, you need to determine if any backwards-compatible
changes have been made, such as  database changes or changes in the protocol.

If any backwards-incompatible changes have been made (see [what constitutes a non-backwards compatible flow change?](../../../../../en/platform/corda/4.9/enterprise/cordapps/upgrading-cordapps.html#what-constitutes-a-non-backwards-compatible-flow-change)
for more information), you need to follow the upgrade method detailed below. Otherwise, the CorDapp JAR can just
be replaced with the new version.


## Contract and state upgrades

There are two types of contract and state upgrade that you can perform.


1. *Implicit* upgrades allow multiple implementations of the contract ahead of time, using constraints. See
[Contract Constraints](cordapps/api-contract-constraints.md) to learn more.
2. *Explicit* upgrades create a special *contract upgrade transaction* and require all participants of a state to sign it using the
contract upgrade flows.

This guide covers the *explicit* type of upgrade, as implicit contract upgrades are handled by the CorDapp.

In an explicit upgrade, contracts and states can be changed in arbitrary ways if all of the state’s participants
agree to the proposed upgrade. The following combinations of upgrades are possible:


* A contract is upgraded while the state definition remains the same.
* A state is upgraded while the contract stays the same.
* The state and the contract are updated simultaneously.


## Perform the upgrade

If a contract or state requires an explicit upgrade, update all states to the new contract at a time all the participants agree on.
by all participants. The updated CorDapp JAR needs to be distributed to all relevant parties in advance of the changeover
time.

To perform the upgrade:


1. Drain the node to avoid the definition of states or contracts changing whilst a flow is in progress. See [flow drains](../../../../../en/platform/corda/4.9/enterprise/cordapps/upgrading-cordapps.html#flow-drains) for more information. There are two ways you can drain the node:
    * By RPC using the `setFlowsDrainingModeEnabled` method with the parameter `true`.
    * Via the shell by issuing the command `run setFlowsDrainingModeEnabled enabled: true`.

2. Check all flows have completed. There are two ways you can check this:
    * By RPC using the `stateMachinesSnapshot` method and checking that there are no results.
    * Via the shell by issuing the command `run stateMachinesSnapshot`.

    {{< note >}}

    The `stateMachinesSnapshot` method ties the flow ID with the `flowName` class. The result shows you all the flows running in your node.
    You can use the `flow watch` method instead. It omits all the details returned by `stateMachinesSnapshot` that you don't need.

    {{< /note >}}

3. Stop the node when all flows are complete.

4. Replace the existing JAR with the new version.

5. Make required database changes to any custom vault tables for the upgraded CorDapp by following the database upgrade steps in [deploying CorDapps on a node]({{< relref "../../../../../en/platform/corda/4.9/enterprise/node/operating/node-operations-cordapp-deployment.md" >}}). Database changes required for a CorDapp upgrade follow the same steps as those to set up a database for a new CorDapp.

6. Restart the node.

7. If you drained the node prior to upgrading, switch off flow draining mode. This allows the node to continue to receive requests. There are two ways you can switch off flow draining mode:
    * By RPC using the `setFlowsDrainingModeEnabled` method with the parameter `false`.
    * Via the shell by issuing the command `run setFlowsDrainingModeEnabled enabled: false`.

8. Run the contract upgrade authorization flow `ContractUpgradeFlow$Initiate` for each state that needs to be updated.
You can do this manually via RPC. However, if there are more than a couple of states, you should provide a script that queries the vault and runs this flow for all states.
  Only one participant for each state need run `ContractUpgradeFlow$Initiate`. The flow automatically upgrades the state for all participants.
