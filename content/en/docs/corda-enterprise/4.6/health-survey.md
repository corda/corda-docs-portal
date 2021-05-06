---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- health
- survey
title: Health Survey Tool
weight: 120
---

# Health Survey Tool

The Health Survey Tool is a command line utility that can be used to collect information about a node,
which can be used by the R3 support team as an aid to diagnose support issues. It works by scanning a provided
node base directory and archiving some of the important files. Furthermore, it does a deployment status check by connecting to the node and probing
it and the firewall (if deployed externally) for information on configuration, service status, connection map and more.


## Running

To run the health survey tool, use the following command:

```kotlin
java -jar corda-tools-health-survey-4.6.jar --base-directory DIRECTORY [--node-configuration DIRECTORY]
```

Usage:

* `-h`, `--help`:                        Display help
* `-c`, `--node-configuration` <file>:   Path to the Corda node configuration file, optional
* `-d`, `--base-directory` <dir>:        Path to the Corda node base directory
* `-l`, `--local`:                       Verify local node configuration only without checking bridge/firewall, by default verifies all
* `-e`, `--exclude-logs`:                Exclude node’s log files from ZIP report, by default logs are included in ZIP report
* `-t`, `--text-format`:                 Create report as a single .txt file without node’s log files, default is ZIP format
* `-i`, `--timeout` <arg>:               Override default timeout for sending health request messages
* `-v`, `--config-validate`:             Validate configuration files
* `-b`, `--bridge-configuration` <file>: Path to bridge configuration when used in conjunction with *config-validate*
* `-f`, `--float-configuration` <file>:  Path to float configuration when used in conjunction with *config-validate*
* `--bridge-crl-url` <url>:        Alternative CRL URL to be used by the bridge for CRL validation test


RPC Access:

* `--rpc-user` <arg>:              Set the user name for RPC commands
* `--rpc-password` <arg>:          Set the password for RPC user


Connectivity tests:

* `-p`, `--ping` <legal-name>:           Ping remote node’s P2P port using nodes’s legal name
* `-n`, `--notary`:                      Ping all notaries listed on node’s network map
* `--ping-notary` <legal-name>:    Ping named notary using notary’s legal name


High Availability test:

* `--toggle-bridge`:              Switch which bridge is active


Running the tool with no arguments assumes that the base-directory argument is the current working directory.


## Access to node using RPC

The RPC communication test, ping test and notary checks all require permission to run RPC commands on the node.

By default, the Health Survey tool uses the first user with ‘ALL’ permission recorded in the *users*
section of the `security` block or of the `rpcUsers` array in the node configuration file:

```kotlin
security {
    authService {
        dataSource {
            type = INMEMORY
            users = [
                {
                    password = <{ ... }>
                    permissions = [
                        ALL
                    ]
                    username=user
                }
            ]
        }
    }
}
```

If no account has ‘ALL’ access then a specific user name can be used by setting the `–rpc-user` command line option.
This account must have the following permissions:

**For RPC Validation Test:**

* InvokeRpc.nodeInfo

**Ping node check:**

* InvokeRpc.nodeInfoFromParty
* InvokeRpc.wellKnownPartyFromX500Name


For notary checks:

* InvokeRpc.networkMapSnapshot
* InvokeRpc.notaryIdentities
* InvokeRpc.nodeInfoFromParty
* InvokeRpc.wellKnownPartyFromX500Name

{{< note >}}
The Corda Health Survey currently does not support testing RPC communication if users are stored in an external database.
{{< /note >}}

## Output

The tool generates the archive of the collected files in the same directory it is ran in. The names are in the format: `report-date-time.zip`

{{< figure alt="health survey photo" zoom="resources/health-survey-photo.png" >}}

## Deployment health check

The Corda Health Survey is designed to perform connectivity and configuration checks on a Corda Enterprise Node. The tool supports the following deployment configurations:

* Node with internal Artemis broker
* Node with external Artemis broker
* Node with combined Bridge/Float
* Node with separate Bridge/Float
* Node with configured HTTP/SOCKS Proxy
* Bridge with configured HTTP/SOCKS Proxy


{{< note >}}
Highly available Corda Bridge/Float deployments are supported.

The Corda Health Survey is designed to help operators with initial setup of a Node; it is not intended as an ongoing monitoring tool.
{{< /note >}}

## Report format

After each run, the Corda Health Survey collects and packages up into a .zip file information that R3 Support can use to help a customer with a support request, including:

* An obfuscated version of the config files (i.e., without passwords, etc.)
* Node logs from the last 3 days (if the user is happy to share)
* The version of Corda, Java virtual machine and operating system, networking information with DNS lookups to various endpoints (database, network map, doorman, external addresses)
* A copy of the network parameters file
* A list of installed CorDapps (including file sizes and checksums)
* A list of the files in the drivers directory
* A copy of the Node information file and a list of the ones in the additional-node-infos directory, etc.

Instead of zipping the reports, operators can print them to a text file using the command line option `-t`.


## Using Health Survey Tool in HA Environments

In deployments with separate Bridge/Float configuration the ECHO test will receive a response from the Corda node plus one echo
from each bridge plus a single echo from the active float.
Hence in an HA environment with two bridges and two floats the ECHO test will receive four responses.

## Ping Remote Nodes

The ping, notary and ping-notary commands will attempt to resolve the legal name against the node’s network map to obtain the remote
node’s IP address and port. The Health Survey tool will then establish an AMQP connection via the active bridge and/or SOCKS proxy
to the remote port. This test is to verify that the local and remote firewall rules allow AMQP connections across the network.

If no bridge is installed then the Health Survey will attempt to connect directly to the remote address.

{{< note >}}
The option `–ping-notary` should only be used to test a notary cluster. To test a single notary you can use `–ping`.
{{< /note >}}

## Toggle Active Bridge

The `toggle-bridge` command can be used in HA environments to temporarily shut down the active bridge to allow passive bridge
to become the master.

This command can be used to verify that the firewall settings for both bridges have been configured correctly.

## Running CRL checks via the Bridge

If a node running behind the Corda Firewall has been configured to delegate CRL checks to the Bridge, the Health Survey is able to test the functionality and verify that the connectivity path to the CRL endpoint is clear.

This check runs only if the `revocationConfig` property in the Float configuration file is set to `EXTERNAL_SOURCE`. By default, the check tries to reach the Corda Network node TLS CRL endpoint. Users are allowed to verify alternative endpoints by using the `--bridge-crl-url` command-line argument.


## Disabling the Corda Health Survey in production

The tool relies on dedicated Artemis queues to relay configuration and runtime information from the Corda Firewall components. This functionality is enabled by default.
After verifying a production deployment, operators are advised to disable the health checking functionality (in order to use the standard Artemis setup for Corda Enterprise) by adding the following entry in the Node configuration file:

```
enterpriseConfiguration { healthCheck = false }
```

And the following entry in the Bridge configuration file:

```
healthCheck = false
```


## Starting Health Survey as a Corda flow

The Health Survey tool can be started as a Corda flow by installing the Health Survey CorDapp and starting the flow on the console.

```
start HealthSurveyFlow parameters:[]
```

The flow can also be invoked over RPC using the `CordaRPCOps.startFlow()` API with the following stub code.

```none
package net.corda.healthsurvey.flows

import net.corda.core.flows.FlowLogic
import net.corda.core.messaging.CordaRPCOps
import net.corda.core.messaging.startFlow

/**
 * This is a dummy implementation so that the client can compile.
 */
class HealthSurveyFlow(private val parameters: Array<String>) : FlowLogic<Pair<String, ByteArray>>() {
    override fun call(): Pair<String, ByteArray> {
        return Pair("", ByteArray(0))
    }
}

/**
 * Runs the Health Survey tool and returns the report file as a byte stream
 */
fun CordaRPCOps.runHealthSurvey(parameters: Array<String>): Pair<String, ByteArray> {
    return this.startFlow(::HealthSurveyFlow, parameters).returnValue.get()
}
```

