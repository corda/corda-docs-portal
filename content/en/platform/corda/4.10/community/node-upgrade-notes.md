---
aliases:
- /head/node-upgrade-notes.html
- /HEAD/node-upgrade-notes.html
- /node-upgrade-notes.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-node-upgrade-notes
    parent: corda-community-4-10-upgrading
    weight: 30
tags:
- node
- upgrade
- notes
title: Upgrading your node to Corda Community Edition 4.10
---


# Upgrading your node to Corda Community Edition 4.10

Corda releases strive to be backwards compatible, so upgrading a node is fairly straightforward and should not require changes to
applications. It consists of the following steps:

1. [Drain the node](#step-1-drain-the-node)
2. [Make a backup of your node directories and/or database](#step-2-make-a-backup-of-your-node-directories-andor-database)
3. [Download Corda Community Edition](#step-3-download-corda-community-edition)
4. [Upgrade the node to Corda 4.0 or later](#step-4-upgrade-the-node-to-corda-40-or-later)
5. [Replace the corda.jar file with the new version](#step-5-replace-cordajar-with-the-new-version)
6. [Update the configuration](#step-6-update-the-configuration)
7. [Start the node with the run-migration-scripts subcommand](#step-7-start-the-node-with-run-migration-scripts-subcommand)
8. [Start the node in the normal way](#step-8-start-the-node-in-the-normal-way)
9. [Undrain the node](#step-9-undrain-the-node)

The protocol is designed to tolerate node outages, so during the upgrade process peers on the network will wait for your node to come back.

## Step 1: Drain the node

Before a node or application on it can be upgraded, the node must be put in [Draining mode](key-concepts-node.html#draining-mode). This brings the currently running
[Flows](key-concepts-flows.md) to a smooth halt such that existing work is finished and new work is queuing up rather than being processed.

Draining flows is a key task for node administrators to perform. It exists to simplify applications by ensuring apps don’t have to be
able to migrate workflows from any arbitrary point to other arbitrary points, a task that would rapidly become infeasible as workflow
and protocol complexity increases.

To drain the node, run the `gracefulShutdown` command. This will wait for the node to drain and then shut down the node when the drain
is complete.

{{< warning >}}
The length of time a node takes to drain depends on both how your applications are designed, and whether any apps are currently
talking to network peers that are offline or slow to respond. It is thus hard to give guidance on how long a drain should take, but in
an environment with well written apps and in which your counterparties are online, drains may need only a few seconds.

{{< /warning >}}

## Step 2: Make a backup of your node directories and/or database

It’s always a good idea to make a backup of your data before upgrading any server. This will make it easy to roll back if there’s a problem.
You can simply make a copy of the node’s data directory to enable this. If you use an external non-H2 database please consult your database
user guide to learn how to make backups.

We provide some [backup recommendations](node-administration.html#backup-recommendations) if you’d like more detail.

## Step 3: Download Corda Community Edition

Download the required version of Corda Community Edition from [software.r3.com](https://software.r3.com).

## Step 4: Upgrade the node to Corda 4.0 or later

Ensure your node is running Corda 4.0 or later.

## Step 5: Replace `corda.jar` with the new version

Download the latest version of Corda from [Maven](https://download.corda.net/maven/corda-releases/net/corda/corda-node/4.10.3/corda-node-4.10.3.jar).
Make sure it’s available on your path, and that you’ve read the [Release notes](release-notes.md), in particular to discover what version of Java this
node requires.

{{< important >}}
Corda 4 requires Java 8u171 or any higher Java 8 patch level. Java 9+ is not currently supported.

{{< /important >}}

## Step 6: Update the configuration

This step is only required when updating from versions less than or equal to 4.5.

Remove any `transactionIsolationLevel`, `initialiseSchema`, or `initialiseAppSchema` entries from the database section of your configuration.

## Step 7: Start the node with `run-migration-scripts` subcommand

Start the node with the `run-migration-scripts` sub-command with `--core-schemas` and `--app-schemas`.

```bash
java -jar corda.jar run-migration-scripts --core-schemas --app-schemas
```

The node will perform any automatic data migrations required, which may take some
time. If the migration process is interrupted it can be continued simply by starting the node again, without harm. The node will stop automatically when migration is complete.

{{< important >}}
This step may incur a delay whilst any needed database migrations are applied
{{</ important >}}

## Step 8: Start the node in the normal way

Start the node in the normal way.

## Step 9: Undrain the node

Finally, undrain the node to re-enable processing of new inbound flows.

You may now do any checks that you wish to perform, read the logs, and so on. When you are ready, use this command at the shell:

`run setFlowsDrainingModeEnabled enabled: false`

Your upgrade is complete.
