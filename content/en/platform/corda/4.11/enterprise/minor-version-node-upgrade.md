---
date: '2021-12-21'
menu:
  corda-enterprise-4-11:
    identifier: "corda-enterprise-4-11-node-minor-version-upgrade"
    parent: corda-enterprise-4-11-upgrading-menu
tags:
- upgrading
- node
- upgrade
- notes
title: Upgrading a node to a minor version of Corda Enterprise Edition 4.11
weight: 11
---

# Upgrading a node to a minor version of Corda Enterprise Edition 4.11

Follow these steps to upgrade a node from Corda Enterprise Edition 4.11 to Corda Enterprise Edition 4.11.x.

Most of the Corda 4 public, non-experimental APIs are stable. See the [full list of stable APIs]({{< relref "../../../../api-ref/api-ref-corda-4.md" >}}). If you are working with a stable API, you don't need to update your CorDapps. To upgrade:

1. [Drain the node]({{< relref "#step-1-drain-the-node" >}}).
2. [Replace the corda.jar file with the new version]({{< relref "#step-2-replace-cordajar-with-the-new-version" >}}).
3. [Start the node]({{< relref "#step-3-start-the-node" >}}).
4. [Undrain the node]({{< relref "#step-4-undrain-the-node" >}}).

{{< note >}}
The protocol tolerates node outages. Peers on the network wait for your node to become available after upgrading.
{{< /note >}}

## Step 1: Drain the node

Node operators must drain nodes (or CorDapps on nodes) before they can upgrade them. Draining brings all [flows]({{< relref "cordapps/api-flows.md" >}}) that are currently running to a smooth halt. The node finishes any work already in progress, and queues any new work. This process frees CorDapps from the requirement to migrate workflows from an arbitrary point to another arbitrary point—a task that would rapidly become unfeasible as workflow and protocol complexity increases.

To drain a node, run `gracefulShutdown`. This waits for all running flows to be completed and then shuts the node down.

{{< warning >}}
The length of time a node takes to drain varies. It depends on how your CorDapps are designed and whether any CorDapps are
communicating with network peers that are offline or slow to respond. If
the CorDapps are well-written and the required counterparties are online, drains may only take a few seconds.

For a smooth node draining process, avoid long-running flows.
{{< /warning >}}

## Step 2: Replace `corda.jar` with the new version

Replace the `corda.jar` with the latest version from Corda.

Download the latest version of Corda from the [Customer Hub](https://customerhub.r3.com).
Make sure it’s available on your path, and that you’ve read the [Corda release notes]({{< relref "release-notes-enterprise.md" >}}). Pay particular attention to which version of Java the node requires.

{{< important >}}
Corda 4 requires Java 8u171 or any higher Java 8 patch level. Java 9+ is not currently supported.
{{< /important >}}

## Step 3: Start the node

Start the node in the normal way.

The node performs any required automatic data migrations, which may take some
time. If the migration process is interrupted, restart the node to continue. The node stops automatically when migration is complete.

## Step 4: Undrain the node

Run this command in the shell:

`run setFlowsDrainingModeEnabled enabled: false`

Your upgrade is complete.

## Notes

{{< warning >}}
You must align the multi-RPC client version with the node version. Both must be running the same version of Corda Enterprise. See [Querying flow data]({{< relref "node/operating/querying-flow-data.md" >}}) for more information.
{{< /warning >}}
