---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-operating
tags:
- node
- commandline
title: Node command-line options
weight: 140
---


# Node command-line options

The node can optionally be started with the following command-line options:


* `--base-directory`, `-b`: The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. The path can be absolute or relative to the base directory. Defaults to `node.conf`.
* `--dev-mode`, `-d`: Runs the node in development mode. Unsafe in production. Defaults to true on MacOS and desktop versions of Windows. False otherwise.
* `--no-local-shell`, `-n`: Do not start the embedded shell locally.
* `--on-unknown-config-keys <[FAIL,INFO]>`: How to behave on unknown node configuration. Defaults to FAIL.
* `--sshd`: Enables SSH server for node administration.
* `--sshd-port`: Sets the port for the SSH server. If not supplied and SSH server is enabled, the port defaults to 2222.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.

{{< warning >}}
Ensure that the `[COMMAND]` precedes all options. Failing this, the provided arguments will not be in scope for the command and default arguments will be used instead as a result. For example, if `-f custom_config.conf` precedes the `[COMMAND]`, Corda will look for the default `node.conf` instead of the specified `custom_config.conf`.
{{< /warning >}}

## Sub-commands

`clear-network-cache`: Clears local copy of network map, on node startup it will be restored from server or file system.

`initial-registration`: Starts initial node registration with the compatibility zone to obtain a certificate from the Doorman.

Parameters:


* `--network-root-truststore`, `-t` **required**: Network root trust store obtained from network operator.
* `--network-root-truststore-password`, `-p`: Network root trust store password obtained from network operator.

`generate-node-info`: Performs the node start-up tasks necessary to generate the nodeInfo file, saves it to disk, then exits.

`generate-rpc-ssl-settings`: Generates the SSL keystore and truststore for a secure RPC connection.

`install-shell-extensions`: Install `corda` alias and auto completion for bash and zsh. See cli-application-shell-extensions for more info.

`validate-configuration`: Validates the actual configuration without starting the node.



## Enabling remote debugging

To enable remote debugging of the node, run the node with the following JVM arguments:

`java -Dcapsule.jvm.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005" -jar corda.jar`

This will allow you to attach a debugger to your node on port 5005.
