---
aliases:
- /shell.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-shell
    parent: cenm-1-3-tools-and-utilities
    weight: 290
tags:
- shell
title: Embedded Shell
---


# Embedded Shell


The embedded shell allows an administrator to control and monitor the suite of CENM services being run (Network Map,
Identity Manager and Signing service). It is based on the [CRaSH](http://www.crashub.org/) shell and provides certain functions such as viewing
the current state of the network (via the Network Map shell), viewing the CSRs awaiting approval (via the Identity
Manager shell) or executing signing tasks (via the Signing Service shell).



## Shell Configuration

The optional `shell` configuration block can be added to the given CENM service configuration file to enable the
embedded shell. There are two modes that the shell can run in:


### SSH Mode

The most versatile method to access the shell is via SSH. This can be configured by specifying the port, user and
password within the `shell` configuration block:

```guess
...
shell {
    sshdPort = <PORT>
    user = <USERNAME>
    password = <PASSWORD>
}
...
```


### Local Mode

The service can be configured to boot straight into the local shell upon start-up by setting the `shell.localShell`
optional configuration parameter to be true:

```guess
...
shell {
    localShell = true
}
...
```


## SSH Authentication

The host key is loaded from the `<BASE_DIRECTORY>/sshkey/hostkey.pem` file, where <BASE_DIRECTORY> corresponds to the
directory that the service is being run from. This can be overloaded with the `shell.sshHostKeyDirectory` config
parameter option. If this file does not exist, it is generated automatically.


## Connecting to the shell via SSH

For Linux/Mac OS user, the following commands can be run from the terminal:

```bash
ssh -p [portNumber] [host] -l [user]
```

Where:


* `[portNumber]` is the port number specified by the `shell.sshdPort` configuration parameter
* `[host]` is the service’s host (e.g. `localhost` if running the service locally)
* `[user]` is the username specified by the `shell.user` configuration parameter

The password will be requested after a connection is established.

{{< note >}}
Restarting the service frequently may cause the host key to be regenerated. SSH usually saves
trusted hosts and will refuse to connect in case of a change. This check can be disabled using the
`-o StrictHostKeyChecking=no` flag. This option should never be used in production environment!

{{< /note >}}

## Supported Commands

The top level list of available commands can be seen by executing `help` from the shell. There are currently two types
of commands:


* `view` - Commands relating to viewing properties and states relating to the current service.
* `run` - Commands that interact with the service and change the state in some manner.

The list of available commands in each subsection can be viewed by executing either `view` or `run` from the shell.
A shell command can by run by executing the type of the command followed by the command name
(`[view|run] <COMMAND_NAME>`). For example, to view all notaries within the Network Map Service:

```bash
view notaries
```

More information, including an command-line example, for each command can be acquired by using the built-in `man`
functionality (`man <COMMAND_NAME>`). For example, to find out more about the view all notaries command listed above:

```bash
man notaries
```


### Network Map Service

The current supported commands that can be run from the shell are:

```kotlin
    @Description(description = "View the network parameters currently in use",
                 example = "view networkParameters")
    @ViewCommand
    fun networkParameters(): NetworkParameters?

    @Description(description = "View the current pending network parameter update (if exists)",
                 example = "view networkParametersUpdate")
    @ViewCommand
    fun networkParametersUpdate(): Map<String, Any>?

    @Description(description = "View basic information about the currently notaries on the network",
                 example = "view notaries")
    @ViewCommand
    fun notaries(): List<NotaryInfo>

    @Description(description = "View all nodes currently within the public network",
                 example = "view publicNetworkParticipants")
    @ViewCommand
    fun publicNetworkParticipants(): List<CordaX500Name>

    @Description(description = "View all node infos currently within the public network",
                 example = "view publicNetworkNodeInfos")
    @ViewCommand
    fun publicNetworkNodeInfos(): NodeInfosAndPlatformVersions?

    @Description(description = "View all node infos with a publish request in staging",
                 example = "view nodeInfosInStaging")
    @ViewCommand
    fun nodeInfosInStaging(): List<NodeInfo>

    @Description(description = "View all node infos with a quarantined publish request",
                 example = "view quarantinedNodeInfos")
    @ViewCommand
    fun quarantinedNodeInfos(): List<QuarantinedNodeInfo>

    @Description(description = "Remove a node info from the quarantine table",
                 example = "run purgeQuarantinedNodeInfo nodeInfoHash: FA84768F995E50BB61219A139B970560C9231035BC4F5D073AF4E38A4DDC3D58")
    @RunCommand
    fun purgeQuarantinedNodeInfo(nodeInfoHash: String)

    @Description(description = "Remove a node from the staging table and into the network map",
            example = "run purgeStagedNodeInfo nodeInfoHash: FA84768F995E50BB61219A139B970560C9231035BC4F5D073AF4E38A4DDC3D58")
    @RunCommand
    fun purgeStagedNodeInfo(nodeInfoHash: String)

    @Description(description = "Remove all nodes from the staging table and into the network map",
            example = "run purgeAllStagedNodeInfos")
    @RunCommand
    fun purgeAllStagedNodeInfos()

    @Description(description = "Test connections to the configured CENM services",
                 example = "run clientHealthCheck")
    @RunCommand
    fun clientHealthCheck()

    @Description(description = "View nodes that have or haven't accepted a given parameters update " +
                "($DEFAULT_PAGE_SIZE entry per page, 0-indexed pagination)",
            example = "view nodesAcceptedParametersUpdate accepted: true, " +
                    "parametersHash: 0E3A4A700868D1E480A7C31E85621FE5E627A6A361EBE92B3F7A0048A90DE076 " +
                    "pageNumber: 0")
    @ViewCommand
    fun nodesAcceptedParametersUpdate(accepted: Boolean,
                                      parametersHash: String,
                                      pageNumber: Int): List<NodeHashAndInfo>

    @Description(description = "Register network parameters for update, networkParametersFile is the only required parameter " +
            "since it can used on its own when whitelisting a notary with its' X500 name. Bear in mind only HA notaries can " +
            "be whitelisted with X500 name.",
            example = "run networkParametersRegistration networkParametersFile: params.conf networkTrustStore: truststore.jks " +
                    "trustStorePassword: trustpass rootAlias: cordarootca")
    @RunCommand
    fun networkParametersRegistration(
            networkParametersFile: Path,
            networkTrustStore: Path?,
            trustStorePassword: String?,
            rootAlias: String?
    )

    @Description(description = "Initiate flag day", example = "run flagDay")
    @RunCommand
    fun flagDay()

    @Description(description = "Cancel pending network parameters update", example = "run cancelUpdate")
    @RunCommand
    fun cancelUpdate()


```

### Identity Manager Service

The current supported commands that can be run from the shell are:

```kotlin
    @Description(description = "View all approved CSRs currently waiting to be signed",
            example = "view approvedCSRs")
    @ViewCommand
    fun approvedCSRs(): List<CordaX500Name>

    @Description(description = "View all CSRs currently waiting to be approved",
            example = "view awaitingApprovalCSRs")
    @ViewCommand
    fun awaitingApprovalCSRs(): List<CordaX500Name>

    @ViewCommand
    @Description(description = "View all available approval plugins",
            example = "view approvalPlugins")
    fun approvalPlugins(): List<String>

    @ViewCommand
    @Description(description = "View all approved CRRs currently waiting to be signed",
            example = "view approvedCRRs")
    fun approvedCRRs(): List<CordaX500Name>?

    @Description(description = "View all CRRs currently waiting to be approved",
            example = "view awaitingApprovalCRRs")
    @ViewCommand
    fun awaitingApprovalCRRs(): List<CordaX500Name>?

    @RunCommand
    @Description(description = "Run specified workflow plugin",
            example = "run approvalPluginManager")
    fun approvalPluginManager(): List<String>

    @RunCommand
    @Description(description = "Run specified workflow plugin",
            example = "run approvalPluginManager pluginAlias: \"my-plugin-alias\"")
    fun approvalPluginManager(pluginAlias: String)

```

### Signing Service

The current supported commands that can be run from the shell are:

```kotlin
    @Description(description = "View all configured signing processes",
                 example = "view signers")
    @ViewCommand
    fun signers()

    @Description(description = "Run a given manual signing process",
                 example = "run signer name: \"Example Signer Name\"")
    @RunCommand
    fun signer(name: String)

    @Description(description = "Test connections to the configured CENM services",
                 example = "run clientHealthCheck")
    @RunCommand
    fun clientHealthCheck()

```
