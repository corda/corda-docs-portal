---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: "corda-enterprise-4-6-release-notes"
    name: "Release notes"
tags:
- release
- notes
- enterprise
title: Corda Enterprise release notes
weight: 1

---


# Corda Enterprise release notes

## Corda Enterprise 4.6 release overview

This release introduces a number of new features, major functional and operational improvements, and fixes for a range of known issues in the following major areas:

**Flow management features and improvements**

The new flow management features and improvements introduced in Corda Enterprise 4.6 include:

* Ability to [query flow data](#ability-to-query-flow-data-via-rpc-and-via-the-node-shell) via RPC and via the node shell.

  This helps node operators manage the set of flows currently in execution on their node, by giving operators the ability to a) identify one or more flows that did not complete as expected and b) retrieve status information relating to one or more flows.

* Ability to [pause and retry flows](#ability-to-pause-and-resume-flows) via RPC and the Shell.

  This release introduces a new set of RPC calls and node shell commands that allow node operators to set flow checkpoints to a “paused” state, effectively marking problematic flows as "do not restart" and preventing them from being retried automatically when the node is restarted. Node operators can retry all paused flows, or retry all paused flows that were previously hospitalised.

* Ability to use a unique ID to [prevent duplicate flow starts](#ability-to-prevent-duplicate-flow-starts-and-retrieve-the-status-of-started-flows).

  This can be done using an RPC client and is an additional way to start flows by passing in a unique identifier when starting a flow. This allows you to:
    * Check that a flow started correctly (for example, if there was a disconnect event).
    * Prevent duplicate flow starts - if you try and start a flow twice with the same unique identifier, it will only fire once.
    * Recover the progress tracker for in-flight flows.
    * Recover the result of finished flows.

Watch this short video overview of flow querying, flow pausing, and flow retrying via RPC:

{{< youtube E-8oceG5zI4 >}}

Watch this short video demo of flow querying, flow pausing, and flow retrying via RPC:

{{< youtube bhybmX9TICQ >}}

Watch this short video overview of the ability to prevent duplicate flow starts via a unique ID:

{{< youtube nn0sP5HDiG0 >}}

**Operational improvements**

* We have rationalised the way in which [database schema management](#database-schema-harmonisation) is performed across Corda open source and Corda Enterprise. This includes improvements to the [Database Management Tool](#database-management-tool-improvements).
* We now release [Docker images](#deployment-docker-images-for-corda-enterprise-firewall-and-all-corda-enterprise-setup-tools) for Corda Enterprise Firewall and all Corda Enterprise setup tools.
* This release introduces a set of improvements to make the flow state machine more resilient.
* We have added support for [storing node TLS keys in HSM](#support-for-storing-node-tls-keys-in-hsm-without-firewall) even without running the Corda Firewall. A new optional `tlsCryptoServiceConfig` section was introduced inside `enterpriseConfiguration` in `node.conf`.
* We have introduced Node Maintenance Mode, which enables you to [schedule maintenance windows](#node-maintenance-mode) for your nodes via the `maintenanceMode` configuration field within the `enterpriseConfiguration` [node configuration file](node/setup/corda-configuration-fields.html#enterpriseconfiguration) section.
* We have added the ability to perform message ID cleanup less aggressively. Corda Enterprise now performs a [less aggressive and safer cleanup](#ability-to-perform-message-id-cleanup-less-aggressively) of the table that contains identifiers of previously processed messages.

**Developer experience features and improvements**

We are focused on improving the overall developer experience to ensure Corda maintains its status as an easy-to-use platform for developers. In this release we have a number of improvements that will help developers build more resilient applications.

* [Automatic detection of unrestorable checkpoints](#automatic-detection-of-unrestorable-checkpoints). During development, flows are now automatically serialized then deserialized whenever they reach a checkpoint. This enables automatic detection of flow code that creates checkpoints that cannot be deserialized.
* Register [custom pluggable serializers](#ability-to-register-custom-pluggable-serializers-for-cordapp-checkpoints) for CorDapp checkpoints. Custom serializers can now be used when serializing types as part of a flow framework checkpoint. Most classes will not need a custom serializer. This exists for classes that throw exceptions during checkpoint serialization. Implement the new `CheckpointCustomSerializer` interface to create a custom checkpoint serializer.

Plus a lot more - please read these release notes carefully to understand what’s new in this release and how the new features and enhancements can help you.

Corda Enterprise 4.6 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. See the Corda Enterprise [platform support matrix](platform-support-matrix.md) for more information.

Corda Enterprise 4.6 extends the [Corda Enterprise 4.5 release](../4.5/release-notes-enterprise.md) and is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.5, 4.4, 4.3, 4.2, 4.1, 4.0, and 3.x. See the [Corda (open source) release notes](../../corda-os/4.6/release-notes.md) for more information.

{{< note >}}
Just as prior releases have brought with them commitments to wire and API stability, Corda 4.6 comes with those same guarantees.

States and apps valid in Corda 3.0 and above are usable in Corda 4.6.
{{< /note >}}

## New features and enhancements

### Ability to access new, remote RPC interfaces via Multi RPC Client

A new RPC Client, called the Multi RPC Client, has been added in Corda Enterprise 4.6.

Node operators can now use the Multi RPC client to interact with a Corda Enterprise node via any of the following custom, remote RPC interfaces:

* `net.corda.client.rpc.proxy.AuditDataRPCOps`: enables you to audit the log of RPC activity.
* `net.corda.client.rpc.proxy.FlowRPCOps`: enables you to retry a previously hospitalised flow.
* `net.corda.client.rpc.proxy.NodeFlowStatusRpcOps`: enables external applications to query and view the status of the flows which are currently under monitoring by the Flow Hospital.
* `net.corda.client.rpc.proxy.NodeHealthCheckRpcOps`: enables you to get a report about the health of the Corda Enterprise node.
* `net.corda.client.rpc.proxy.notary.NotaryQueryRpcOps`: enables you to perform a spend audit for a particular state reference.

All of these interfaces are located in the `:client:extensions-rpc` module. Corda Enterprise customers can extend these interfaces to add custom, user-defined functionality to help manage their Corda Enterprise nodes.

{{< note >}}
`COMPLETED`, `FAILED`, and `KILLED` flows can only be queried when started by the `startFlowWithClientId` or `startFlowDynamicWithClientId` APIs using [a unique client-provided ID](#ability-to-prevent-duplicate-flow-starts-and-retrieve-the-status-of-started-flows).
{{< /note >}}

For more information, see the [Interacting with a node](node/operating/clientrpc.md) documentation section or see [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.6/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html) in the API documentation.

### Ability to query flow data via RPC and via the node shell

Corda Enterprise 4.6 introduces the ability to query flow checkpoint data. This helps node operators manage the set of flows currently in execution on their node, by giving operators the ability to a) identify one or more flows that did not complete as expected and b) retrieve status information relating to one or more flows.

Node operators can use one of the following methods to query flow status:

* They can use the new `net.corda.client.rpc.proxy.NodeFlowStatusRpcOps` interface to interact with their node and query flow status via RPC.
* They can query the node manually via the node shell, using the new `flowstatus` command.

Querying the node using either method enables node operators to:

* Return a list of all flows that have not completed as expected (suspended flows)
* Return all suspended flows that meet particular search criteria such as the following:
	* The flow is or is not compatible with the current Corda runtime environment.
	* The flow relates to a particular CorDapp.
	* The flow includes a particular flow class.
	* The flow was executed within a specific time window.
	* The flow is in a particular state.
	* The flow did not proceed beyond a specific progress step.
	* The flow remained stuck at a checkpoint for a particular length of time.
* Retrieve status information for one or more suspended flows.

See the [Querying flow data](node/operating/querying-flow-data.md) documentation section for more information.

### Ability to pause and resume flows

We have added a new set of RPC calls and node shell commands that allow node operators to set flow checkpoints to a “paused” state, effectively marking problematic flows as "do not restart" and preventing them from being retried automatically when the node is restarted.

Paused checkpoints will not be loaded in memory on node restart. This helps node operators to manage memory usage - if too many checkpoints are loaded at the same time, the node might crash and it might be impossible to perform a successful restart.

Node operators can retry all paused flows, or retry all paused flows that were previously hospitalised. Hospitalised flows can be retried via RPC, thus eliminating the need to restart the node to trigger retries.

For more information, see [Pause and resume flows](flow-pause-and-resume.md).

#### Ability to prevent duplicate flow starts and retrieve the status of started flows

Corda’s RPC client now allows each flow to be started with a unique client-provided ID. Flows started in this manner have the following benefits:

* If a flow is invoked multiple times with the same client ID, they will be considered duplicates. All subsequent invocations after the first will simply return the result of the first invocation.
* A running flow can be reattached using the client ID. This allows its flow handle to be recovered.
* The result of a completed flow can still be viewed after the flow has completed, using the client ID.

This enables you to:

* Reconnect reliably to previously started flows.
* Reclaim a flow's result or exception at any time in the future.

For more information, see [Starting a flow with a client-provided unique ID](flow-start-with-client-id.md).

#### Database schema harmonisation

As part of this release, we have rationalised the way in which database schema management is performed across Corda open source and Corda Enterprise.

* We have moved all schema management options from node configuration files to start-up sub-commands (in order to reduce misconfigurations and make changing options a less onerous process).
  * We have removed the ability to create/upgrade the database schema as part of running a node, by introducing a schema creation/migration sub-command that needs to be run as part of a node installation/upgrade.
  * We have harmonised the configuration, set-up, and behaviour of databases between Corda and Corda Enterprise.
  * We have removed automatic schema migration for updating from Corda versions prior to 4.0.
* Added support in Corda open source for packaging custom CorDapp schemas into Liquibase migrations through introducing Liquibase schema migration/description scripts for CorDapps.

{{< warning >}}
Schema migration/creation has been decoupled from the normal node run mode and needs to be done using a separate
sub-command. **All configuration keys relating to schema migration have been removed and will cause errors if used in Corda 4.6.**
{{< /warning >}}

Some of the more significant changes are listed below.

**Schema management for CorDapps**

Corda 4.6 now supports CorDapp schema migration via Liquibase in the same way as Corda Enterprise, where:

* Each CorDapp needs to provide a migration resource with Liquibase scripts to create/migrate any required schemas.
* Old Corda open source CorDapps that do not have migration scripts need to be migrated in the same way as described in the [Enterprise migration](cordapps/database-management.md#adding-scripts-retrospectively-to-an-existing-cordapp) documentation.
* A node can manage app schemas automatically using Hibernate with H2 in dev mode. This must be enabled with the `--allow-hibernate-to-manage-app-schema` command-line flag.

**Schema creation**

In Corda 4.6, a Corda node can no longer modify/create schema on the fly in normal run mode. Instead, you should apply schema setup or changes deliberately using a new sub-command called `run-migration-scripts`. This subcommand will create/modify the schema and then exit.

**A split into core and app schema**

Corda nodes have a set of core schema that is required for the node itself to work. In addition, CorDapps can define additional mapped schemas to store their custom states in the vault.

Up to Corda 4.6, the node/schema migration would use the combination of both and run all the required schema creation/migration using hardcoded lists and heuristics to figure out which is which (as, for example, core and app schema have different requirements whether they can be run while checkpoints are present in the database).

This has now changed - the `run-migration-scripts` sub-command takes two new parameters: `--core-schemas` and `--app-schemas`. At least one of these parameters must be present and will run the migration scripts for the respective requested schema set.

{{< note >}}
Core schemas cannot be migrated while there are checkpoints.

App schemas can be forced to migrate with checkpoints present using the `--update-app-schema-with-checkpoints` flag.
{{< /note >}}

**Tests**

Automated tests (as in `MockNetwork`, `NodeBasedTest` and Node Driver tests) are able to set up the required schema
automatically.

* Mock Network. The `MockNode` overrides a field in `AbstractNode` that allows the node to run schema migration on the fly (which is **not** available via the command-line). It takes extra constructor parameters to control whether Liquibase will be run and whether Hibernate can be used to create the app schema. Both default to `true` for compatibility with existing tests.
* Node Driver. In-process nodes use a similar mechanism to Mock Nodes. Out-of-process nodes using a persistent database need the database to be set up before they start (as does a real node). Therefore, `DriverDSL` will run a schema migration step before running the node in this case. Out-of-process nodes using an in-memory database are a particularly tricky case, as there is no persistent database that could be set up before the node starts. Therefore, the node itself can check for H2 in-memory JDBC URLs and will run any required migration if that is detected.
* Node-based Tests use the same in-process node as does NodeDriver.

**Bootstrapping**

The Network Bootstrapper runs core schema migrations as part of the bootstrapping process.

Cordformation has an extra parameter that can be added to the node section in the `build.gradle`, as follows:

```
runSchemaMigration = true
```

This will run the full schema migration as the last step of the cordformation setup, leaving the nodes ready to run.

**Configuration changes**

The following fields have been removed from the database section in the node configuration file. These need to be removed from the node configuration as the node will throw an
exception on startup if it finds any of them:

* `transactionIsolationLevel`: this is now hard-coded in the node.
* `initialiseSchema`: as above - schema initialisation cannot be run as part of node startup.
* `initialiseAppSchema`: as above.
* `runMigration`: this is deprecated. Schema migration can only be run via the [Database Management Tool](#database-management-tool-improvements) or the new `run-migration-script` sub-command.

In addition, it is now possible to run a CorDapp without a schema migration resource in `devMode` - Corda Enterprise 4.6 accepts the same `--allow-hibernate-to-manage-app-schemas` command-line flag as Corda open source 4.6, and has relaxed the check for the presence of app schemas when running in `devMode`.

{{< note >}}
Please check the schema management documentation to see what adjustments are needed to your CorDapp packaging process.
{{< /note >}}

**Schema migration from Corda versions prior to V4.0**

Corda 4.6 drops the support for retro-fitting the database changelog when migrating from Corda versions older than 4.0. Thus it is required to migrate to a previous 4.x version before
migrating to Corda 4.6 - for example, 3.3 to 4.5, and then 4.5 to 4.6.

### Database Management Tool improvements

We have improved the [Database Management Tool](database-management-tool.md) in order to facilitate database migrations from Corda to Corda Enterprise.

The changes are briefly described below.

* A new `sync-app-schemas` command has been added. It updates the migration changelog for all available CorDapps.
* The `dry-run` command has two new parameters: `--core-schemas` (the tool outputs DB-specific DDL to apply the core node schema migrations) and `--app-schemas` (the tool outputs DB-specific DDL to apply the migrations for custom CorDapp schemas).
* The `execute-migration command` has three new parameters: `--core-schemas` (the tool will attempt to run the node Liquibase core schema migrations), `--app-schemas` (the tool will attempt to run Liquibase migrations for custom CorDapp schemas), and `--db-admin-config <path/to/adminconfigfile>` (this parameter specifies the location on disk of a config file holding elevated access credentials for the DB - the tool will use the credentials listed in the config file to connect to the node database and apply the changes).
* Obfuscated passwords are now allowed. To enable the tool to de-obfuscate the obfuscated fields, the following command-line options are provided for setting the passphrase and seed if necessary: `--config-obfuscation-passphrase` and `--config-obfuscation-seed`.
* Base directory, which defaults to the current working directory if not set.
* Location of output file when `dry-run` is used. The output file will now be created relative to the current working directory rather than the base directory.

For more information, see [Database Management Tool](database-management-tool.md).

#### Ability to register custom pluggable serializers for CorDapp checkpoints

CorDapp developers now have the ability to create a custom serializer for a given type, which is then used when serializing the type in question as part of a flow framework checkpoint.

Note that this is an advanced feature, designed specifically for certain types that throw exceptions during checkpoint serialization. The vast majority of classes will not need a custom serializer.

Custom checkpoint serializers are created by implementing the new `CheckpointCustomSerializer` interface.

For more information, see [Pluggable serializers for CorDapp checkpoints](cordapp-custom-serializers-checkpoints.md).

### Automatic detection of unrestorable checkpoints

Flows are now automatically serialized then deserialized whenever they reach a checkpoint. This allows better detection of flow code that creates checkpoints that cannot be deserialized, and enables developers and network operators to detect unrestorable checkpoints when developing CorDapps and thus reduces the risk of writing flows that cannot be retried gracefully.

This feature addresses the following common problems faced by developers:

* Creating objects or leveraging data structures that cannot be serialized/deserialized correctly by Kryo (the checkpoint serialization library Corda uses).
* Writing flows that are not idempotent or do not deduplicate behaviour (such as calls to an external system).

The feature provides a way for flows to reload from checkpoints, even if no errors occur. As a result, developers can be more confident that their flows would work correctly, without needing a way to inject recoverable errors throughout the flows.

{{< note >}}
This feature should not be used in production. It is disabled by default in the [node configuration file](node/setup/corda-configuration-fields.md) - `reloadCheckpointAfterSuspend = false`.
{{< /note >}}

For more information, see [Automatic detection of unrestorable checkpoints](checkpoint-tooling.md#automatic-detection-of-unrestorable-checkpoints).

### Host to Container SSH port mapping for Dockerform

When creating a Docker container, you can now map the SSH port on the host to the same port on the container. For more information, see [Optional configuration](node/deploy/generating-a-node.md#optional-configuration) in [Creating nodes locally](node/deploy/generating-a-node.md).

### Metering client for the Metering Collection Tool

You can now collect metering data from Corda Enterprise Nodes without having to build a custom client or accessing the Shell. For more information, see [Metering client for the Metering Collection Tool](metering-rpc.md).

### Hotloading of notaries list

The notaries list can now be hotloaded. Updates to the `notaries` network parameter do not require the node to be shut down and restarted.

For more information, see [Hotloading](network/network-map.md#hotloading) in [Network map](network/network-map.md).

### Support for storing node TLS keys in HSM without Firewall

The node now supports storing its TLS keys in HSM even without running the Corda Enterprise Firewall. To this end, a new optional `tlsCryptoServiceConfig` section has been added to the `enterpriseConfiguration` configuration section in the [node configuration file](node/setup/corda-configuration-fields.md).

To migrate from file-based node's TLS keystore to HSM, you need to add `tlsCryptoServiceConfig` section into `node.conf` and renew TLS certificate and keys, as described in the [Renewing TLS certificates](ha-utilities.md#renewing-tls-certificates) section in [HA Utilities](ha-utilities.md).

For more information, see [Storing node TLS keys in HSM](node/setup/tls-keys-in-hsm.md).

### LedgerGraph available as a stand-alone CorDapp

LedgerGraph enables other CorDapps, such as the set of [Collaborative Recover CorDapps](node/collaborative-recovery/introduction-cr.md), to have near real-time access to data concerning all of a node’s transactions and their relationships.

LedgerGraph has been in use in some solutions already, but is now available as a CorDapp in its own right. Therefore, as an operator, you can now use LedgerGraph as a standalone application on your node in order to expose in-memory transaction statistics related to the Corda ledger via flows and JMX/RPC.

The metrics exposed by LedgerGraph include:

* Size in bytes and depth of each transaction chain.
* Number of attachments referenced by each transaction chain.
* Whether all the outputs of a transaction chain have been consumed.

### Collaborative Recovery upgraded to V1.1

As LedgerGraph is now available as a stand alone CorDapp, the Collaborative Recovery CorDapps have been upgraded to reflect this change. In order [to use Collaborative Recovery V1.1](node/collaborative-recovery/introduction-cr.md) you must have a corresponding LedgerGraph CorDapp installed. If you use Confidential Identities with Collaborative Recovery, in V1.1 you must configure LedgerGraph to handle this. In V1.0, Confidential Identities configuration needed to be added to the **LedgerSync** CorDapp.

### Improved CockroachDB performance

A new configuration flag has been introduced, enabling native SQL for CockroachDB with multi-row insert statements.

For more information, see [Node configuration reference](node/setup/corda-configuration-fields.md).

### Migrating Notary data to CockroachDB

Notary data stored in a Percona database can now be migrated to Cockroach DB.

For more information, see [Importing Percona notary data to CockroachDB](notary/upgrading-a-notary.md).

### Notary identity configuration

When registering a notary, the new field `notary.serviceLegalName` must be defined. This allows single-node notaries to be upgraded to HA notaries.

For more information, see [Notary service overview](notary/ha-notary-service-overview.md).

### Standalone JPA notary optimisation

We have added a new configuration flag - `notary.jpa.generateNativeSQL`. Setting this option to `notary.jpa.generateNativeSQL = true` enables the generation of native SQL for Cockroach DB with multi-row `insert` statements. This results in better notary performance in some cases through a reduction of the number of `insert` SQL queries and the service latency.

### Node Maintenance Mode

We have added a way for Corda Enterprise node operators to schedule maintenance windows for their nodes. During a maintenance window, the node can be configured to:

* Clear the RPC audit table.
* Clean up the message ID table.

Maintenance windows can be scheduled through a node’s [configuration file](node/setup/corda-configuration-file.md) using the new, optional `maintenanceMode` configuration field within the `enterpriseConfiguration` top-level [configuration section](node/setup/corda-configuration-fields.md#enterpriseconfiguration).

A descriptive log entry is emitted whenever a node triggers or completes a maintenance window.

For more information, see [Node Maintenance Mode](node/operating/maintenance-mode.md).

### Ability to perform message ID cleanup less aggressively

Corda Enterprise now performs a less aggressive and safer cleanup of the table that contains identifiers of previously processed messages.

You can also adjust some parameters that control the frequency of this cleanup mechanism. To do so, use the `processedMessageCleanup` field in the `enterpriseConfiguration` section of the [node configuration file](node/setup/corda-configuration-fields.html#enterpriseconfiguration).

### Configuration option for the attachments class loader cache size

The attachments class loader cache size is now configurable through the new `EnterpriseConfiguration` configuration field `attachmentClassLoaderCacheSize` in the [node configuration file](node/setup/corda-configuration-fields.md#enterpriseconfiguration). This cache caches the class loaders used to store the transaction attachments.

The default value is `256` attachments per cache.

{{< warning >}}
The default value must **not** be changed unless explicitly advised by R3 support.
{{< /warning >}}

### Deployment: Docker images for Corda Enterprise Firewall and all Corda Enterprise setup tools

We now release Docker images for the Corda Enterprise Firewall [https://hub.docker.com/r/corda/enterprise-firewall](https://hub.docker.com/r/corda/enterprise-firewall), as well as for the required tools for Corda Enterprise setup [https://hub.docker.com/r/corda/enterprise-setup](https://hub.docker.com/r/corda/enterprise-setup).

Our Docker Hub organisation (https://hub.docker.com/u/corda) now contains all the Docker images required for a full production deployment of Corda Enterprise.

### Other changes and improvements

* To avoid a third-party dependency issue, we have reverted the supported H2 Database Engine version to **1.4.197** in Corda Enterprise versions 4.4.3, 4.5.1, and 4.6.
* To reduce the risk of vulnerabilities, we have upgraded the Apache Zookeeper version used by the Corda Enterprise [Firewall component](node/corda-firewall-component.md#prerequisites-4) from 3.5.4-Beta to 3.61. See [Apache ZooKeeper setup](operations/deployment/corda-firewall-configuration-file.md#apache-zookeeper-setup) for more information.
* We have upgraded `commons-beanutils` to version 1.9.4 for improved security.
* As of Corda Enterprise 4.6, support for [DemoBench](demobench.md) is deprecated.
* We have released a new minor version of [Accounts SDK](https://github.com/corda/accounts/blob/master/docs.md) - version 1.0.2. This version includes database improvements that make it compatible with Corda Enterprise 4.6. If you are planning to use the Accounts SDK with Corda Enterprise 4.6, you must use Accounts SDK V 1.0.2.
* We have released a new minor version of [Tokens SDK](cordapps/token-sdk-introduction.md) - version 1.2.1. This version includes database improvements that make it compatible with Corda Enterprise 4.6. If you are planning to use the Tokens SDK with Corda Enterprise 4.6, you must use Tokens SDK V 1.2.1.
* When starting a new driver using the driver DSL, the notary node will start by default as a thread in the same JVM process that runs the driver regardless of the `startNodesInProcess` driver properties (and not as a new process if the `startNodesInProcess` is `false`). This setting can be overridden. Please note that if the test interacts with the notary and expects the notary to run as a new process, you must set `startInProcess` to `false`.
* In Corda Enterprise 4.6, if a CorDapp's `minimumPlatformVersion` is higher than the platform version of the node, the CorDapp is not loaded and the node fails to start. This is a change in behaviour compared to Corda Enterprise 4.5 where under these conditions the node would start up and log that the CorDapp could not be loaded. See [Versioning](cordapps/versioning.md) for more information.

## Platform version change

The platform version of Corda 4.6 has been bumped up from 7 to 8.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## Important upgrade and migration notes

{{< warning >}}

The operational improvements around [database schema harmonisation](#database-schema-harmonisation) we have made in Corda 4.6 require a number of manual steps when upgrading to Corda 4.6 and Corda Enterprise 4.6 from a previous version or from Corda open source to Corda Enterprise. These changes are described in detail in the following pages:
* [Upgrading CorDapps to newer Platform Versions](app-upgrade-notes.md).
* [Upgrading CorDapps to Corda Enterprise 4.6](app-upgrade-notes-enterprise.md)
* [Upgrading nodes to a new Corda version](node-upgrade-notes.md).

A brief checklist of required steps follows below for each upgrade path.

**Upgrading an existing node from Corda 4.5 (or earlier 4.x version) to version 4.6**

1. Remove any entries of `transactionIsolationLevel`, `initialiseSchema`, `initialiseAppSchema`, and `runMigration` from the database section of your [node configuration file](node/setup/corda-configuration-file.md).
2. Update any missing core schema changes by running the node in `run-migration-scripts` mode: `java -jar corda.jar run-migration-scripts --core-schemas`.
3. Add Liquibase resources to CorDapps. In Corda 4.6, CorDapps that introduce custom schema need Liquibase migration scripts allowing them to create the schema upfront. For existing CorDapps that do not have migration scripts in their resources, they can be added as an external migration `.jar` file, as documented in [Database management scripts](cordapps/database-management.md#adding-scripts-retrospectively-to-an-existing-cordapp).
4. Update the changelog for existing schemas. After upgrading the Corda `.jar` file and adding Liquibase scripts to the CorDapp(s), any custom schemas from the apps are present
in the database, but the changelog entries in the Liquibase changelog table are missing (as they have been created by Liquibase). This will cause issues when starting the node, and also when running `run-migration-scripts` as tables that already exist cannot be recreated. By running the new sub-command `sync-app-schemas`, changelog entries are created for all existing mapped schemas from CorDapps: `java -jar corda.jar sync-app-schemas`.

**IMPORTANT** Do **not** install any new CorDapp, or a version adding schema entities, before running the `sync-app-schemas` sub-command. Any mapped schema found in the CorDapps will be added to the changelog **without** trying to create the matching database entities.

**IMPORTANT** If you are upgrading a node to Corda 4.6 while any CorDapp with mapped schemas is being installed, you **must synchronise the schemas** (and thus run `sync-app-schemas`) **before** the node can start again and/or before any app schema updates can be run. Therefore, you must **not** install or update a CorDapp with new or modified schemas while upgrading
the node, or after upgrading but before synchronising the app schemas.

**Upgrading from Corda 3.x or Corda Enterprise 3.x**

Corda 4.6 drops the support for retro-fitting the database changelog when migrating from Corda versions older than 4.0. Thus it is required to migrate to a previous 4.x version before
migrating to Corda 4.6 - for example, 3.3 to 4.5, and then 4.5 to 4.6.

**Important note about running the initial node registration command**

In Corda Enterprise 4.6, database migrations are run on initial node registration **by default**.

To prevent this, use the `--skip-schema-creation` flag alongside the `--initial-registration` command.

The `initial-registration` command is described in [Node command-line options](node/node-commandline.md#sub-commands) and [Joining a compatibility zone](network/joining-a-compatibility-zone.md#joining-an-existing-compatibility-zone).

{{< /warning >}}


## Fixed issues

* We have fixed an issue where the FutureX provider threw a `javax.security.auth.login.LoginException` when trying to establish a connection with the HSM.
* We have fixed an issue where a Corda node in dev mode did not start up without the Network Map Service running.
* We have fixed an issue with failing `flows continue despite errors – net.corda.node.flows.FlowRetryTest` tests.
* We have fixed an issue where an unexpected error with unique constraints in the `node_metering_data_pkey` occurred following an upgrade from Corda Enterprise 4.5.1 with the Database Management Tool.
* We have fixed an issue where the RPC `startFlow` could not reattach to existing client id flows when flow draining mode was enabled.
* We have fixed an issue where the Health Survey Tool could not verify the connection to the node's Artemis broker.
* We have fixed an issue where the `FlowSessionCloseTest.flow` could not access a closed session unless it was a duplicate close that was handled gracefully.
* We have fixed an issue where the `RetryFlowMockTest` failed due to restart not setting `senderUUID` and the early end session message not hanging the receiving flow.
* We have fixed an issue where Corda did not write the error message for a start-up error into the log file.
* We have fixed an issue where the expected `error_code="5"` error was missing in logs run with custom CorDapps without the Liquibase schema.
* We have fixed an issue where a flow could fail with a null error and stack trace if the counterparty was busy.
* We have fixed an issue with inconsistent behaviour between killed client ID flows and flows with other statuses.
* We have fixed an issue where restarting the Corda node without the `--pause-all-flows` flag would cause the node to remain in flow draining mode, pausing flow processing until the mode was manually disabled.
* We have fixed an issue where it was not possible to register multiple notaries configured to use TLS keys in one HSM.
* We have fixed an issue where the HA Utilities did not log information about the used `tlsCryptoServiceConfig` configuration.
* We have fixed an issue where months and years were not supported values in `rpcAuditDataRetentionPeriod`.
* We have fixed an issue where a node failed to shut down when the `senderRetentionPeriodInDays` was set to a negative integer.
* We have fixed an issue where CorDapps that were working on Corda 4.3 were not registered when Corda was upgraded to version 4.5.
* We have fixed an issue where the `tlsCryptoServiceConfig.cryptoServiceConf` file path was resolved incorrectly, leading to an error when registering the node.
* The Corda Health Survey Tool now displays a warning message when network information is resolved and an HTTP redirect occurs.
* We have fixed an issue where an error occurred on node shutdown with the message: `The configuration values provided for message cleanup are invalid`.
* We have fixed an issue where the Corda Health Survey Tool was hanging after performing all checks when Artemis was shut down during the Health Survey Tool test.
* There is now an informative error message if HSM is unavailable.
* CRaSH Flow query now displays `Data` and `Time` information correctly.
* We fixed an issue where the optional `file:prefix` was stripped from the classpath element passed to the `ClassGraph()` filter function, resulting in the filter function not recognising the element.
* We fixed an issue were flows would start executing when the `StateMachineManager.start` database transaction had not started yet.
* We have reverted to Jackson 2.9.7 to resolve an issue where R3 Tools could not work properly with the upgraded version.
* We have fixed an issue where `Paths.get("")` returns `null` instead of the current working directory.
* We have fixed an issue where the sample web app for IRS demo could not be run due to the following error: `no main manifest attribute, in web-4.6-RC05-thin.jar`.
* A warning now appears after sleep task execution because the next maintenance event was not triggered due to a long execution of the current event.
* A previously unhandled exception when the password for an RPC user was wrong is now handled correctly.
* A previously unhandled exception with problems accessing DB is now treated as a `HikariPool.PoolInitializationException`.
* We have fixed an issue where the Classloader failed to find the class when a CorDapp class was used.
* The path for network parameters is now configurable and the network parameters file is stored in the location specified by the node configuration.

## Known issues
* The HA Utilities tool and the Health Survey Tool do not process configuration `include` commands correctly if the configuration is located in the tool's root directory.
* It is currently not possible to build the Kotlin CorDapp template against Corda Enterprise 4.6.
* There are inconsistencies in code stubs and actual code between the Kotlin and Java CorDapp templates.
* The Database Management Tool and Corda Enterprise do not run with the same configuration in the Command-line Interface options and configuration files.
* The node does not connect to the HSM on the second registration attempt if the first attempt was not successful due to HSM inaccessibility.
* Using the local network bootstrapper takes longer than in previous versions of Corda.
* The "new" operation on the `FlowRPCOps` RPC interface takes a `StateMachineID` as an argument, leading to repetitive invocations of the form.
* An SSL connection cannot be established between two nodes when one of the nodes does not have access to the Identity Manager Service and, as a result, to CRL distribution points.
* A node cannot be run with the `--dev-mode` option unless `devModeOptions.allowCompatibilityZone=true` is added to the node configuration.
* Corda throws an exception instead of producing a clear error message when a log cannot be created.
* In HA Utilities, the `notary-registration` option does not write CSR details to the log file.
* In the Attachment Demo, the `runSender` task uses `myLegalName` instead of `serviceLegalName` for notarisation.
* Some samples cannot be run on Windows due to an issue with long file names.
* The Database Management Tool does not work with Corda Enterprise 4.6 when `dataSourceProperties` is in a separate file.
* Business Network roles are not displayed when `MembershipState` is queried via the Shell Command-line Interface. It is also not possible to change the participant roles via the Shell Command-line Interface.
* Filtering flows by `FlowStart` using the constants `Instant.MAX` and `Instant.MIN` returns an exception.
* The SSH Client returns inconsistent exit codes after `gracefulShutdown` is run, indicating that an error has occurred.
* The Docker node does not generate configuration and certificates against Testnet.
* The node rejects the incoming P2P connection from a node with a revoked certificate, with warnings and errors, but does not block any attempts to re-establish it. This leads to a quick accumulation of warnings and errors in the node log files.
* The error text is repeated in the console when trying to register a node with forbidden characters in the Organisation (`O`) name.
* The ``<install-shell-extensions>`` sub-command of Corda node creates log files in the home folder, while all other sub-commands create log files the `logs` subfolder.
* If a notary registration fails when using HA Utilities, a dummy notary keystore file is created. If users are unaware that this keystore file has been created, it causes issues when they attempt to register the notary again.
