---
aliases:
- /releases/4.0/node-upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-node-upgrade-notes
    weight: 40
tags:
- node
- upgrade
- notes
title: Upgrading your node to Corda 4
---


# Upgrading your node to Corda 4

Corda releases strive to be backwards compatible, so upgrading a node is fairly straightforward and should not require changes to
applications. It consists of the following steps:


* Drain the node.
* Make a backup of your node directories and/or database.
* Update database
* Replace the `corda.jar` file with the new version.
* Start up the node. This step may incur a delay whilst any needed database migrations are applied.
* Undrain it to re-enable processing of new inbound flows.

The protocol is designed to tolerate node outages, so during the upgrade process peers on the network will wait for your node to come back.


## Step 1. Drain the node

Before a node or application on it can be upgraded, the node must be put in [Draining mode](key-concepts-node.md#draining-mode). This brings the currently running
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



## Step 2. Make a backup of your node directories and/or database

It’s always a good idea to make a backup of your data before upgrading any server. This will make it easy to roll back if there’s a problem.
You can simply make a copy of the node’s data directory to enable this. If you use an external non-H2 database please consult your database
user guide to learn how to make backups.

Please see [Backup recommendations](node-administration.md#backup-recommendations) for a detailed explanation of Corda backup and recovery guarantees.


## Step 3. Update database

Upgrading to Corda 4 from Corda 3.x requires both schema and data updates.

If using the development **H2** database, there is no need to perform any explicit upgrade steps if schema changes are additive (e.g. new tables, columns, indexes).
Simply restart the node with the upgraded `corda.jar` and the H2 database will be updated automatically.
However, if schema changes are non-additive (e.g. modification or removal of tables, columns) the user is responsible for manually adjusting
the H2 schema to reflect these changes (and perform any data copying as required).


### Schema update

If using an Enterprise grade **commercial** database you have two options:


* Use the Corda Database management tool to generate and execute SQL upgrade scripts.Generate the scripts by running the following command:

java -jar corda-tools-database-manager-4.0.jar –base-directory /path/to/node –dry-run


The generated scripts should then be applied by your database administrator using their tooling of choice or by executing the following command:


java -jar corda-tools-database-manager-4.0.jar –base-directory /path/to/node –execute-migration


Restart the node with the upgraded `corda.jar`.

{{< note >}}
This is the recommended best practice in strictly controlled UAT, staging and production environments.

{{< /note >}}

{{< warning >}}
Ensure you use the same version of the Database management tool as the Corda Node it wil be used against.

{{< /warning >}}




* Configure the node to automatically execute all database SQL scripts upon startup.
This requires setting the following flag in the node’s associated `node.conf` configuration file:

```none
database.runMigration = true
```

{{< note >}}
This is only recommended for rapid prototyping and test environments.{{< /note >}}



{{< warning >}}
It is always recommended to take backups of your database before executing any upgrade steps.

{{< /warning >}}


See [Backup Recommendations](node-administration.md#backup-recommendations) for further information.

Please refer to [Database schema setup](node-operations-database-schema-setup.md) for detailed instructions.


### Data update

This release requires some data migration to populate new entities.


* DDL script execution and automatic data update by a database administrator using the Corda Database management tool.Follow the steps described [here](node-operations-database-schema-setup.md#db-setup-database-management-ddl-execution-ref).
This upgrade procedure is a mix of running the DDL script for schema update and running Database management tool for non-schema alteration changes.
All steps of this procedure except the first one needed to be run:*Extract DDL script using :ref:`Database management tool <migration-tool>`*
*Apply DDL scripts on a database*
*Apply remaining data upgrades on a database.*Note the last step is important because Corda 4 contains new columns/tables which needed to be populated based on your existing data,
and these migration can’t be expressed in DDL script.Specifically, the `vault_states` table adds the following:>

    * `relevancy_status` column
    * referenced `state_party` table (and new fields)


and uses some custom migration code (executed as a custom change set by Liquibase) to achieve this. In order to determine if a state is relevant
for a node, the migration code needs to know the nodes name, which it obtains from `myLegalName` (set in the Database management tool configuration file).
The migration code also requires access to the node’s CorDapps in order to understand which custom `MappedSchema` objects to process.>

    * If you are not reusing a node base directory, copy any CorDapps from a node being upgraded to *cordapps* subdirectory accessed by the tool.





## Step 4. Replace `corda.jar` with the new version

Download the latest version of Corda from [our Artifactory site](https://software.r3.com/artifactory/webapp/#/artifacts/browse/simple/General/corda/net/corda/corda-node).
Make sure it’s available on your path, and that you’ve read the [Release notes for Corda 4](release-notes.md), in particular to discover what version of Java this
node requires.


{{< important >}}
Corda 4 requires Java 8u171 or any higher Java 8 patchlevel. Java 9+ is not currently supported.


{{< /important >}}


## Step 5. Start up the node

Start the node in the usual manner you have selected. The node will perform any automatic data migrations required, which may take some
time. If the migration process is interrupted it can be continued simply by starting the node again, without harm.


## Step 6. Undrain the node

You may now do any checks that you wish to perform, read the logs, and so on. When you are ready, use this command at the shell:

`run setFlowsDrainingModeEnabled enabled: false`

Your upgrade is complete.


{{< warning >}}
if upgrading from Corda Enterprise 3.x, please ensure your node has been upgraded to the latest point release of that
distribution. See [Upgrade a Corda 3.X Enterprise Node](https://docs.corda.net/docs/corda-enterprise/3.3/node-operations-upgrading.html#upgrading-a-corda-enterprise-node)
for information on upgrading Corda 3.x versions.

{{< /warning >}}
