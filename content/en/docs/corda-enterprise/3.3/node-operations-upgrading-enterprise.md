---
aliases:
- /releases/3.3/node-operations-upgrading-enterprise.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-node-operations-upgrading-enterprise
    parent: corda-enterprise-3-3-corda-nodes-index
    weight: 1100
tags:
- node
- operations
- upgrading
- enterprise
title: Upgrading a Corda Enterprise Node
---


# Upgrading a Corda Enterprise Node

The following steps apply to upgrading a Corda Enterprise node following a minor release update (eg. from 3.0 -> 3.1 -> 3.2 -> 3.3)
and/or patchlevel release (eg. 3.2 -> 3.2.20181019 -> 3.2-20190215):


* before shutting down a node, enable [Flow draining](upgrading-cordapps.md#upgrading-cordapps-flow-drains) to ensure that all “in-flight” flows are correctly checkpointed.
    * By RPC using the `setFlowsDrainingModeEnabled` method with the parameter `true`
    * Via the shell by issuing the following command `run setFlowsDrainingModeEnabled enabled: true`


* Check that all the flows have completed.
    * By RPC using the `stateMachinesSnapshot` method and checking that there are no results
    * Via the shell by issuing the following command `run stateMachinesSnapshot`


* Once all flows have completed, stop the node.
* Back-up the node’s database (using vendor or standard SQL database backup tooling).
Detailed information on database management in Corda can be found [here](database-management.md).
* Back-up the entire root directory of the node, plus any external directories and files optionally specified in the configuration.
* Replace the existing corda JAR with the new one.
* Restart the node.
* If you drained the node prior to upgrading, switch off flow draining mode to allow the node to continue to receive requests.
    * By RPC using the `setFlowsDrainingModeEnabled` method with the parameter `false`
    * Via the shell by issuing the following command `run setFlowsDrainingModeEnabled enabled: false`



Please see [Backup recommendations](node-administration.md#backup-recommendations) for a detailed explanation of Corda backup and recovery guarantees.


## Database upgrades

If using the development **H2** database, there is no need to perform any explicit upgrade steps if schema changes are additive (e.g. new tables, columns, indexes).
Simply restart the node with the upgraded `corda.jar` and the H2 database will be updated automatically.
However, if schema changes are non-additive (e.g. modification or removal of tables, columns) the user is responsible for manually adjusting
the H2 schema to reflect these changes (and perform any data copying as required).

If using an Enterprise grade **commercial** database you have two options:


* Use the Corda [Database management tool](database-management.md#migration-tool) to generate and execute SQL upgrade scripts.Generate the scripts by running the following command:

```kotlin
java -jar corda-tools-database-manager-3.3.jar --base-directory /path/to/node --dry-run
```

The generated scripts should then be applied by your database administrator using their tooling of choice or by executing the following command:

```kotlin
java -jar corda-tools-database-manager-3.3.jar --base-directory /path/to/node --execute-migration
```

Restart the node with the upgraded `corda.jar`.{{< note >}}
This is the recommended best practice in strictly controlled UAT, staging and production environments.{{< /note >}}

* Configure the node to automatically execute all database SQL scripts upon startup.
This requires setting the following flag in the node’s associated `node.conf` configuration file:

```none
database.runMigration = true
```

{{< note >}}
This is only recommended for rapid prototyping and test environments.{{< /note >}}



{{< warning >}}
It is always recommended to take backups of your database before executing any upgrade steps.
See [Backup Recommendations](node-administration.md#backup-recommendations) for further information.

{{< /warning >}}



### Migrating existing data from a Corda Enterprise 3.2 database to a Corda Enterprise 3.3 supported database

There are no database changes in the node for these upgrade paths.


### Migrating existing data from a Corda Enterprise 3.0 or 3.1 database to a Corda Enterprise 3.2 supported database

Follow the general database upgrade instructions listed previously for the respective Corda Enterprise version.

