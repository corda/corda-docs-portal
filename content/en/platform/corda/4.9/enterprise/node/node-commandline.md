---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-corda-nodes-operating
tags:
- node
- commandline
title: Node command-line options
weight: 140
---


# Node command-line options

The node can optionally be started with the following command-line options:


* `--base-directory`, `-b`: the node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: the path to the config file. The path can be absolute or relative to the base directory. Defaults to `node.conf`.
* `--dev-mode`, `-d`: runs the node in development mode. Unsafe in production. Defaults to true on MacOS and desktop versions of Windows. False otherwise.
* `--no-local-shell`, `-n`: do not start the embedded shell locally.
* `--on-unknown-config-keys <[FAIL,INFO]>`: how to behave on unknown node configuration. Defaults to FAIL.
* `--sshd`: enables SSH server for node administration.
* `--sshd-port`: sets the port for the SSH server. If not supplied and SSH server is enabled, the port defaults to 2222.
* `--verbose`, `--log-to-console`, `-v`: if set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: show this help message and exit.
* `--version`, `-V`: print version information and exit.
* `--allow-hibernate-to-manage-app-schema`: enable this option to make the node manage app schemas automatically using Hibernate
with H2 in dev mode.

{{< warning >}}
Ensure that the `[COMMAND]` precedes all options. Failing this, the provided arguments will not be in scope for the command and default arguments will be used instead as a result. For example, if `-f custom_config.conf` precedes the `[COMMAND]`, Corda will look for the default `node.conf` instead of the specified `custom_config.conf`.
{{< /warning >}}

## Sub-commands

`clear-network-cache`: Clears the local copy of the network map. On node startup it will be restored from the server or the file system.

`initial-registration`: Starts the initial node registration with the compatibility zone to obtain a certificate from the Identity Manager Service.

{{< warning >}}
**Important note about running the initial node registration command**

From Corda Enterprise Edition 4.6, database schemas are no longer initialised/migrated automatically by running any command at the first run of the node - typically at the initial node registration. This is now done explicitly by running `run-migration-scripts`, so no other commands during the first node run would initialise/migrate the database schema.

The exception to that is the `initial-registration` command, which embeds `run-migration-scripts` and therefore runs the database migration scripts by default.

So if you are using deployment automation you may need to adjust your scripts accordingly and exclude the database initialisation/migration task from the initial node registration command. To do so, use the `--skip-schema-creation` flag alongside the `initial-registration` command.
{{< /warning >}}

Parameters:

* `--network-root-truststore`, `-t` **required**: Network root trust store obtained from network operator.
* `--network-root-truststore-password`, `-p`: Network root trust store password obtained from network operator.
* `--skip-schema-creation`: Skips the default database migration step.

{{< note >}}
Node `initial-registration` now includes the creation of `identity-private-key` keystore alias. For more information, see [node folder structure]({{< relref "setup/node-structure.md" >}}). Previously, only `cordaclientca` and `cordaclienttls` aliases were created during `initial-registration`, while `identity-private-key` was generated on demand on the first node run. Hence, in Corda 4.9 the content of `nodekeystore.jks` is never altered during a regular node run (except for `devMode = true`, where the certificates directory can be filled with pre-configured keystores).
{{< /note >}}

`run-migration-scripts`: From version 4.6, a Corda node can no longer modify/create schema on the fly in normal run mode - schema setup or changes must be
applied deliberately using this sub-command. It runs the database migration script for the requested schema set defined in the following parameters. Once it creates or modifies the schema(s), the sub-command will exit.

Parameters:

* `--core-schemas`: Use to run the core database migration script for the node database. Core schemas cannot be migrated while there are checkpoints.
* `--app-schemas`: Use to run the app database migration script for CorDapps. To force an app schema to migrate with checkpoints present, use the `--update-app-schema-with-checkpoints` flag alongside the `run-migration-scripts` sub-command.

`generate-node-info`: Performs the node start-up tasks necessary to generate the nodeInfo file, saves it to disk, then exits.

`generate-rpc-ssl-settings`: Generates the SSL keystore and truststore for a secure RPC connection.

`install-shell-extensions`: Install `corda` alias and auto completion for bash and zsh. See [Shell extensions for CLI Applications
]({{< relref "operating/cli-application-shell-extensions.md" >}}) for more info.

`validate-configuration`: Validates the actual configuration without starting the node.

## Enabling remote debugging

To enable remote debugging of the node, run the node with the following JVM arguments:

`java -Dcapsule.jvm.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005" -jar corda.jar`

This will allow you to attach a debugger to your node on port 5005.
