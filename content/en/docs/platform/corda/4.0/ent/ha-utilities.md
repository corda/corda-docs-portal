---
aliases:
- /releases/4.0/ha-utilities.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-ha-utilities
    parent: corda-enterprise-4-0-tools-index-enterprise
    weight: 1020
tags:
- ha
- utilities
title: HA Utilities
---


# HA Utilities

Setting up multiple nodes behind shared Corda Firewall require preparation of various keystores and config files, which can be time consuming and error prone.
The HA Utilities aims to provide tools to streamline the node provision and deployment process.

The tool is distributed as part of Corda Enterprise 4.0 in the form of runnable JAR “corda-tools-ha-utilities-4.0.jar”.

To run simply pass in the file or URL as the first parameter:

```kotlin
java -jar corda-tools-ha-utilities-4.0.jar <sub-command> <command line options>
```


Use the `--help` flag for a full list of command line options.


## Sub-commands

`node-registration`: Corda registration tool for registering 1 or more node with the Corda Network, using provided node configuration.
`import-ssl-key`: Key copying tool for creating bridge SSL keystore or add new node SSL identity to existing bridge SSL keystore.
`generate-internal-artemis-ssl-keystores`: Generate self-signed root and SSL certificates for internal communication between the services and external Artemis broker.
`generate-internal-tunnel-ssl-keystores`: Generate self-signed root and SSL certificates for internal communication between Bridge and Float.
`configure-artemis`: Generates required configuration files for the external Artemis broker.
`install-shell-extensions`: Install alias and autocompletion for bash and zsh. See [Shell extensions for CLI Applications](cli-application-shell-extensions.md) for more info.


### Node Registration Tool

The registration tool can be used to register multiple Corda nodes with the network operator, it is useful when managing multiple identities and setting up multiple Corda nodes sharing Corda firewall infrastructures.
For convenience the tool is also downloading network parameters.


#### Command-line options

```shell
ha-utilities node-registration [-hvV] [--logging-level=<loggingLevel>] [-b=FOLDER] -p=PASSWORD -t=FILE -f=FILE... [-f=FILE...]...
```


* `-v`, `--verbose`, `--log-to-console`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO
* `-b`, `--base-directory=FOLDER`: The node working directory where all the files are kept.
* `-f`, `--config-files=FILE...`: The path to the config file
* `-t`, `--network-root-truststore=FILE`: Network root trust store obtained from network operator.
* `-p`, `--network-root-truststore-password=PASSWORD`: Network root trust store password obtained from network operator.
* `-h`, `--help`: Show this help message and exit.
* `-V`, `--version`: Print version information and exit.


### SSL key copier

When using shared external bridge, the bridge will need to have access to nodes’ SSL key in order to establish connections to counterparties on behalf of the nodes.
The SSL key copier sub command can be used to provision the SSL keystore and add additional keys when adding more nodes to the shared infrastructure.


#### Command-line options

```shell
ha-utilities import-ssl-key [-hvV] [--logging-level=<loggingLevel>] [-b=FOLDER] [-k=FILES] -p=PASSWORDS --node-keystore-passwords=PASSWORDS... [--node-keystore-passwords=PASSWORDS...]... --node-keystores=FILES... [--node-keystores=FILES...]...
```


* `-v`, `--verbose`, `--log-to-console`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO
* `--node-keystores=FILES...`: The path to the node SSL keystore(s)
* `--node-keystore-passwords=PASSWORDS...`: The password(s) of the node SSL keystore(s)
* `-b`, `--base-directory=FOLDER`: The working directory where all the files are kept.
* `-k`, `--bridge-keystore=FILES`: The path to the bridge SSL keystore.
* `-p`, `--bridge-keystore-password=PASSWORDS`: The password of the bridge SSL keystore.
* `-h`, `--help`: Show this help message and exit.
* `-V`, `--version` :Print version information and exit.


### Self signed internal Artemis SSL keystore

TLS is used to ensure communications between HA components and standalone Artemis are secured. This tool can be used to generate the required keystores if TLS cert signing infrastructure is not available within your organisation.
Please note that for Artemis to work correctly, the password for the store and the password for the private key will need to be set to the same value.


#### Command-line options

```shell
ha-utilities generate-internal-artemis-ssl-keystores [-hvV] [--logging-level=<loggingLevel>] [-b=<baseDirectory>] [-c=<country>] [-l=<locality>] [-o=<organization>] [-p=<keyStorePassword>] [-t=<trustStorePassword>]
```


* `-v`, `--verbose`, `--log-to-console`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO
* `-p`, `--keyStorePassword=<keyStorePassword>`: Password for all generated keystores. Default: changeit
* `-t`, `--trustStorePassword=<trustStorePassword>`: Password for the trust store. Default: changeit
* `-o`, `--organization=<organization>`: X500Name’s organization attribute. Default: Corda
* `-l`, `--locality=<locality>`: X500Name’s locality attribute. Default: London
* `-c`, `--country=<country>`: X500Name’s country attribute. Default: GB
* `-b`, `--base-directory=<baseDirectory>`: The node working directory where all the files are kept.
* `-h`, `--help`: Show this help message and exit.
* `-V`, `--version`: Print version information and exit.


### Self signed internal Tunnel SSL keystore

TLS is used for communications between Bridge and Float components. This tool can be used to generate the required keystores if TLS cert signing infrastructure is not available within your organisation.


#### Command-line options

```shell
ha-utilities generate-internal-tunnel-ssl-keystores [-hvV] [--logging-level=<loggingLevel>] [-b=<baseDirectory>] [-c=<country>] [-l=<locality>] [-o=<organization>] [-p=<keyStorePassword>] [-e=<entryPassword>] [-t=<trustStorePassword>]
```


* `-v`, `--verbose`, `--log-to-console`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO
* `-p`, `--keyStorePassword=<keyStorePassword>`: Password for all generated keystores. Default: changeit
* `-e`, `--entryPassword=<entryPassword>`: Password for all the keystores private keys. Default: changeit
* `-t`, `--trustStorePassword=<trustStorePassword>`: Password for the trust store. Default: changeit
* `-o`, `--organization=<organization>`: X500Name’s organization attribute. Default: Corda
* `-l`, `--locality=<locality>`: X500Name’s locality attribute. Default: London
* `-c`, `--country=<country>`: X500Name’s country attribute. Default: GB
* `-b`, `--base-directory=<baseDirectory>`: The node working directory where all the files are kept.
* `-h`, `--help`: Show this help message and exit.
* `-V`, `--version`: Print version information and exit.


### Artemis configuration

Configuring an external Artemis broker to be used by Corda nodes and firewall components can be a little daunting. This tool will generate the necessary configuration files and install (if needed) a new Artemis instance.
Please note that the generated configuration files will be copied to a destination supplied as an argument to the command, replacing existing ones.
The keystore and truststore information will be downloaded by the clients when Artemis is configured in HA mode. Therefore, the tool will configure broker.xml with paths relative to the Artemis instance (for acceptors) and client’s working directory (for connectors).
For example, using the option –keystore ./artemiscerts/keystore.jks will require the keystore to be installed in $ARTEMIS_DIR/etc/artemiscerts and $NODE_OR_BRIDGE_DIR/artemiscerts.


#### Command-line options

```shell
ha-utilities configure-artemis [-hvV] [--logging-level=<loggingLevel>] [--install] [--distribution=<dist>] --path=<workingDir>  --user=<userX500Name> --acceptor-address=<acceptorHostAndPort> --keystore=<keyStore> --keystore-password=<keyStorePass> --truststore=<trustStore> --truststore-password=<trustStorePass> [--ha=<mode>] [--connectors=<connectors>[;<connectors>...]]
```


* `-v`, `--verbose`, `--log-to-console`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO
* `--install`: Install an Artemis instance at the specified path.
* `--distribution`: The path to the Artemis distribution used to install an instance.
* `--path`: The path where the generated configuration files will be installed. Used as the new instance location when using the –install option.
* `--user`: The X500 name of connecting users (clients). CN must be “artemis”. Other fields must match those passed in to `generate-internal-artemis-ssl-keystores`. This parameter is whitespace-sensitive. Example value: “CN=artemis, O=Corda, L=London, C=GB”
* `--acceptor-address`: The broker instance acceptor network address for incoming connections.
* `--keystore`: The SSL keystore path.
* `--keystore-password`: The SSL keystore password.
* `--truststore`: The SSL truststore path.
* `--truststore-password`: The SSL truststore password.
* `--ha`: The broker’s working mode. If specified, the broker will be configured to work in HA mode. Valid values: NON_HA, MASTER, SLAVE
* `--connectors`: A list of network hosts and ports representing the Artemis connectors used for the Artemis HA cluster. The first entry in the list will be used by the instance configured with this tool. The connector entries are separated by commas (e.g. localhost:10000,localhost:10001,localhost:10002)
* `-h`, `--help`: Show this help message and exit.
* `-V`, `--version`: Print version information and exit.

