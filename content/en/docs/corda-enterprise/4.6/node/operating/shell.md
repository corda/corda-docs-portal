---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating-interacting
tags:
- shell
title: Node shell
weight: 1
---




# Node shell

The Corda shell is an embedded or standalone command line that allows an administrator to control and monitor a node. It is based on the [CRaSH](http://www.crashub.org/) shell and supports many of the same features. These features include:

* Invoking any of the node’s RPC methods.
* Viewing a dashboard of threads, heap usage, VM properties.
* Uploading and downloading attachments.
* Issuing SQL queries to the underlying database.
* Viewing JMX metrics and monitoring exports.
* UNIX style pipes for both text and objects, an `egrep` command and a command for working with columnar data.
* Shutting the node down.


## Permissions

When accessing the shell (embedded, standalone, via SSH) RPC permissions are required. This is because the shell actually communicates with the node using RPC calls.

There are several operations that are read-only in nature and granting them should have no impact on the ledger state of the node.

These permissions are:

```bash
permissions=[
    "InvokeRpc.nodeInfo",
    "InvokeRpc.networkMapSnapshot",
    "InvokeRpc.currentNodeTime",
    "InvokeRpc.wellKnownPartyFromX500Name",
    "InvokeRpc.vaultQuery",
    "InvokeRpc.vaultQueryBy",
    "InvokeRpc.stateMachinesSnapshot",
    "InvokeRpc.nodeDiagnosticInfo",
    "InvokeRpc.notaryIdentities",
    "InvokeRpc.attachmentExists",
    "InvokeRpc.partyFromKey",
    "InvokeRpc.notaryPartyFromX500Name",
    "InvokeRpc.partiesFromName",
    "InvokeRpc.registeredFlows"
]
```

There are also operations that allow starting/killing the flows or even stopping the node as a whole:

* Watching flows (`flow watch`) requires `InvokeRpc.stateMachinesFeed`.
* Starting flows requires `InvokeRpc.registeredFlows` and `InvokeRpc.wellKnownPartyFromX500Name`, as well as a permission for the flow being started.
* Killing flows (`flow kill`) requires `InvokeRpc.killFlow`. This currently allows the user to kill *any* flow, so please be careful when granting it!

Description of RPC operations can be found in the [RPC operations](../../api-rpc.md) documentation.

{{< note >}}
`InvokeRpc.startTrackedFlowDynamic` permission gives permission to run all existing flows.
{{< /note >}}


## The shell via the local terminal

{{< note >}}
Local terminal shell works only in dev mode!
{{< /note >}}

The shell will display in the node’s terminal window. It connects to the node as `shell` user with password `shell` (which is only available in dev mode). It may be disabled by passing the `--no-local-shell` flag when running the node.


## The shell via SSH

The shell is also accessible via SSH.

{{< warning >}}
The SSH port should not be exposed publicly. Limit exposure of the SSH port as much as possible.
{{< /warning >}}


### Enabling SSH access

By default, the SSH server is *disabled*. To enable it, a port must be configured in the node’s `node.conf` file:

```bash
sshd {
    port = 2222
}
```


### Authentication

Users log in to shell via SSH using the same credentials as they would use for RPC. No RPC permissions are required to allow the connection and log in.

The host key is loaded from the `<node root directory>/sshkey/hostkey.pem` file. If this file does not exist, it is
generated automatically. In dev mode, the seed may be specified to give the same results on the same computer in order to avoid host-checking errors.

Only RSA key is currently supported as a host key. If `hostkey.pem` is not RSA, it will be replaced by the newly generated RSA key.


### Connecting to the shell

#### Linux and MacOS

Run the following command from the terminal:

```bash
ssh -p [portNumber] [host] -l [user]
```

Where:

* `[portNumber]` is the port number specified in the `node.conf` file.
* `[host]` is the node’s host (for example, `localhost` if running the node locally).
* `[user]` is the RPC username.

The RPC password will be requested after a connection is established.

{{< note >}}
In dev mode, restarting a node frequently may cause the host key to be regenerated. SSH usually saves
trusted hosts and will refuse to connect in case of a change. This check can be disabled using the
`-o StrictHostKeyChecking=no` flag. This option should never be used in a production environment!

{{< /note >}}

#### Windows

Windows does not provide a built-in SSH tool. An alternative such as [PuTTY](https://www.putty.org/) should be used.


## The standalone shell

The standalone shell is a standalone application interacting with a Corda node via RPC calls. RPC node permissions are necessary for authentication and authorisation. Certain operations, such as starting flows, require access to the CorDapp `.jar` files.


### Starting the standalone shell

Run the following command from the terminal:

```bash
corda-shell [-hvV] [--logging-level=<loggingLevel>] [--password=<password>]
            [--truststore-file=<trustStoreFile>]
            [--truststore-password=<trustStorePassword>]
            [--truststore-type=<trustStoreType>] [--user=<user>] [-a=<host>]
            [-c=<cordappDirectory>] [-f=<configFile>] [-o=<commandsDirectory>]
            [-p=<port>] [COMMAND]
```

Where:

* `--config-file=<configFile>`, `--f` The path to the shell configuration file, used instead of providing the rest of the command line options.
* `--cordapp-directory=<cordappDirectory>`, `-c` The path to the directory containing CorDapp jars, CorDapps are required when starting flows.
* `--commands-directory=<commandsDirectory>`, `-o` The path to the directory containing additional CRaSH shell commands.
* `--host`, `-a`: The host address of the Corda node.
* `--port`, `-p`: The RPC port of the Corda node.
* `--user=<user>`: The RPC user name.
* `--password=<password>` The RPC user password. If not provided it will be prompted for on startup.
* `--truststore-password=<trustStorePassword>`: The password to unlock the TrustStore file.
* `--truststore-file=<trustStoreFile>`: The path to the TrustStore file.
* `--truststore-type=<trustStoreType>`: The type of the TrustStore (for example, JKS).
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.

Additionally, the `install-shell-extensions` subcommand can be used to install the `corda-shell` alias and auto completion for bash and zsh. See [Shell extensions for CLI Applications](cli-application-shell-extensions.md) for more info.

The format of `config-file`:

```bash
node {
    addresses {
        rpc {
            host : "localhost"
            port : 10006
        }
    }
}
shell {
        workDir : /path/to/dir
}
extensions {
    cordapps {
        path : /path/to/cordapps/dir
    }
}
ssl {
    keystore {
        path: "/path/to/keystore"
        type: "JKS"
        password: password
    }
    trustore {
        path: "/path/to/trusttore"
        type: "JKS"
        password: password
    }
}
user : demo
password : demo
```

{{< note >}}
SSH server is not supported inside the standalone shell.

{{< /note >}}

## Shell Safe Mode

This is a new mode added in the Enterprise 4.3 release to prevent the CRaSH shell embedded commands (for example, `java`, `system`) from being executed by a user with insufficient privilege. This is part of a general security-tightening initiative.

When a shell is running in unsafe mode, the shell behaviour will be the same as before and will include CRaSH built-in commands. By default the internal shell will run in safe mode but will still be have the ability to execute RPC client calls as before based on existing RPC permissions. No Corda functionality is affected by this change; only the ability to access to the CRaSH shell embedded commands.

When running an SSH shell, it will run in safe mode for any user that does not explicitly have permission ‘ALL’ as one the items in their RPC permission list, see [Working with the CordaRPCClient API](../../../../corda-os/4.7/tutorial-clientrpc-api.md) for more information about the RPC Client API. These shell changes arealso applied to the Stand Alone shell which will now run in safe mode (Enterprise 4.3 onwards). It may be possible that, in the future, the CRaSH shell embedded commands may become deprecated. Where possible, please do not write any new code that depends on them as they are technically not part of Corda functionality.

### Getting help

You can type `help` in the shell to list the available commands, and `man` to get interactive help on many commands. You can also pass the `--help` or `-h` flags to a command to get info about what switches it supports.

Commands may have subcommands, in the same style as `git`. In that case, running the command by itself will list the supported subcommands.


## Node shell commands

You can use the shell to:

* Issue RPCs.
* Upload and download attachments.
* Extract information about attachments from the node.
* Output information about the flows running on the node.
* Work with flows.
* Check if a transaction is recorded on the node.
* Extract healthcheck information about a running node.
* View and change `run` command output format.
* Shut down the node.

### Issue RPCs

The shell interacts with the node by issuing RPCs (remote procedure calls). You make an RPC from the shell by typing `run`, followed by the name of the desired RPC method.

You can find a list of the available RPC methods
[here](https://docs.corda.net/api/kotlin/corda/net.corda.core.messaging/-corda-r-p-c-ops/index.html).

Some RPCs return a stream of events that will be shown on screen until you press Ctrl-C.

#### Example command

Query the vault for `CashState` states with the following command:

`run vaultQuery contractStateType: net.corda.finance.contracts.asset.Cash$State`

This breaks down as follows:

* `run` is the shell command for making an RPC call.
* `vaultQuery` is an RPC call that queries the vault for vault states.
* `net.corda.finance.contracts.asset.Cash$State` is the fully-qualified name of the state type we are querying for.

{{< note >}}
For further guidance on the parameters used in shell commands, see the [Parameters Syntax section](#parameter-syntax) below.
{{< /note >}}

#### Example command output

An example of the output for `run vaultQuery contractStateType: net.corda.finance.contracts.asset.Cash$State` is shown below:

```
- state:
    data: !<net.corda.finance.contracts.asset.Cash$State>
      amount: "200.00 USD issued by O=BankOfCorda, L=London, C=GB[01]"
      owner: "GfHq2tTVk9z4eXgyNkbxxXPps9MWrSaKeKs3jyh3QJeg7DdewnP468emNA9K"
    contract: "net.corda.finance.contracts.asset.Cash"
    notary: "O=Notary Service, L=Zurich, C=CH"
    encumbrance: null
    constraint: !<net.corda.core.contracts.SignatureAttachmentConstraint>
      key: "aSq9DsNNvGhYxYyqA9wd2eduEAZ5AXWgJTbTEw3G5d2maAq8vtLE4kZHgCs5jcB1N31cx1hpsLeqG2ngSysVHqcXhbNts6SkRWDaV7xNcr6MtcbufGUchxredBb6"
  ref:
    txhash: "2524B8C9D1D0A7695175465358AAB17809E65A3DC23D6C1393F4167C105D2815"
    index: 0
- state:
    data: !<net.corda.finance.contracts.asset.Cash$State>
      amount: "300.00 GBP issued by O=BankOfCorda, L=London, C=GB[01]"
      owner: "GfHq2tTVk9z4eXgyUUZVN63pZ88HnfX7CKBDUaRAzDhehzB5CbRPhFuJtaXX"
    contract: "net.corda.finance.contracts.asset.Cash"
    notary: "O=Notary Service, L=Zurich, C=CH"
    encumbrance: null
    constraint: !<net.corda.core.contracts.SignatureAttachmentConstraint>
      key: "aSq9DsNNvGhYxYyqA9wd2eduEAZ5AXWgJTbTEw3G5d2maAq8vtLE4kZHgCs5jcB1N31cx1hpsLeqG2ngSysVHqcXhbNts6SkRWDaV7xNcr6MtcbufGUchxredBb6"
  ref:
    txhash: "C438CE336B62D0D8BF731D96566D93DBEACFADF18864C030A1D871C8B15F6978"
    index: 0
statesMetadata:
- ref:
    txhash: "2524B8C9D1D0A7695175465358AAB17809E65A3DC23D6C1393F4167C105D2815"
    index: 0
  contractStateClassName: "net.corda.finance.contracts.asset.Cash$State"
  recordedTime: "2020-11-11T14:39:47.609Z"
  consumedTime: null
  status: "UNCONSUMED"
  notary: "O=Notary Service, L=Zurich, C=CH"
  lockId: null
  lockUpdateTime: "2020-11-11T14:39:47.642Z"
  relevancyStatus: "RELEVANT"
  constraintInfo:
    constraint:
      key: "aSq9DsNNvGhYxYyqA9wd2eduEAZ5AXWgJTbTEw3G5d2maAq8vtLE4kZHgCs5jcB1N31cx1hpsLeqG2ngSysVHqcXhbNts6SkRWDaV7xNcr6MtcbufGUchxredBb6"
- ref:
    txhash: "C438CE336B62D0D8BF731D96566D93DBEACFADF18864C030A1D871C8B15F6978"
    index: 0
  contractStateClassName: "net.corda.finance.contracts.asset.Cash$State"
  recordedTime: "2020-11-11T14:41:35.103Z"
  consumedTime: null
  status: "UNCONSUMED"
  notary: "O=Notary Service, L=Zurich, C=CH"
  lockId: null
  lockUpdateTime: "2020-11-11T14:41:35.117Z"
  relevancyStatus: "RELEVANT"
  constraintInfo:
    constraint:
      key: "aSq9DsNNvGhYxYyqA9wd2eduEAZ5AXWgJTbTEw3G5d2maAq8vtLE4kZHgCs5jcB1N31cx1hpsLeqG2ngSysVHqcXhbNts6SkRWDaV7xNcr6MtcbufGUchxredBb6"
totalStatesAvailable: -1
stateTypes: "UNCONSUMED"
otherResults: []
```


### Upload and download attachments

The shell can be used to upload and download attachments from the node. To learn how, see the [Working with attachments](../../../../corda-os/4.7/tutorial-attachments.md#uploading-an-attachment) tutorial.


### Extract attachment information

Use the `attachments` shell command to extract information about attachments from the node. This commands allows you to examine installed and uploaded attachments as well as those that were received over the network.

#### Command

`attachments trustInfo`

#### Output

The output will contain the following information:

* If an attachment is installed locally.
  * `True` if the attachment is installed in the CorDapps directory or uploaded via RPC.
  * `False` in all other scenarios, including attachments received from a peer node or uploaded via any means other than RPC.
* If an attachment is trusted.
* Which other attachment, if any, provided trust to an attachment.

Below is an example of the commands's output:

```
Name                                          Attachment ID                                                        Installed             Trusted                Trust Root
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
net.corda.dummy-cordapp-contracts-states      654CDFD0F195269B1C839DD9D539592B4DE7DD09BF29A3762EF600F94AE45E18     true                  true                   net.corda.dummy-cordapp-contracts-states
Corda Finance Demo                            71154836EBE54C0A60C6C5D9513EE015DB722EED57034B34428C72459CF133D7     true                  true                   Corda Finance Demo
Received from: O=PartyA, L=London, C=GB       CDDDD9A5C97DBF839445FFD79F604078D9D9766D178F698780EA4F9EA7A02D5F     false                 true                   net.corda.dummy-cordapp-contracts-states
```

{{< note >}}
The `Name` column will be empty if the attachment has been stored without a name. `Trust Root` will also display an attachment hash if there is no name to display.
{{< /note >}}

The output above shows that two CorDapps have been installed locally and are therefore trusted. The third record is an attachment received from another node, hence the `Name` field containing `Received from: O=PartyA, L=London, C=GB`. The CorDapp is also trusted as another CorDapp has been signed by a common key; the `Trust Root` field is filled in to highlight this.


### Output information about the flows running on the node

Use the `checkpoints` command to output information about the flows running on a node. This is useful for diagnosing the causes of stuck flows. Using the generated output, corrective actions can be taken to resolve the issues flows are facing.

#### Command

`checkpoints dump`

#### Output

The command will create a zip and generate a JSON file for each flow. Each file follows the naming format `<flow name>-<flow id>.json` - for example, `CashIssueAndPaymentFlow-90613d6f-be78-41bd-98e1-33a756c28808.json`.

The `.zip` file is placed into the `logs` directory of the node and is named `checkpoints_dump-<date and time>.zip` - for example, `checkpoints_dump-20190812-153847`.

You can find the following useful fields in the output:

* `flowId`: The id of the flow.
* `topLevelFlowClass`: The name of the original flow that was invoked (by RPC or a service).
* `topLevelFlowLogic`: Detailed view of the top level flow.
* `flowCallStackSummary`: A summarised list of the current stack of subflows along with any progress tracker information.
* `suspendedOn`: The command that the flow is suspended on (for example, `SuspendAndReceive`) which includes the `suspendedTimestamp`.
* `flowCallStack`: A detailed view of the current stack of subflows.

#### Example output

```json
{
  "flowId" : "90613d6f-be78-41bd-98e1-33a756c28808",
  "topLevelFlowClass" : "net.corda.finance.flows.CashIssueAndPaymentFlow",
  "topLevelFlowLogic" : {
    "amount" : "10.00 USD",
    "issueRef" : "MTIzNA==",
    "recipient" : "O=BigCorporation, L=New York, C=US",
    "anonymous" : true,
    "notary" : "O=Notary, L=London, C=GB"
  },
  "flowCallStackSummary" : [
    {
      "flowClass" : "net.corda.finance.flows.CashIssueAndPaymentFlow",
      "progressStep" : "Paying recipient"
    },
    {
      "flowClass" : "net.corda.finance.flows.CashPaymentFlow",
      "progressStep" : "Generating anonymous identities"
    },
    {
      "flowClass" : "net.corda.confidential.SwapIdentitiesFlow",
      "progressStep" : "Awaiting counterparty's anonymous identity"
    }
  ],
  "suspendedOn" : {
    "sendAndReceive" : [
      {
        "session" : {
          "peer" : "O=BigCorporation, L=New York, C=US",
          "ourSessionId" : -5024519991106064492
        },
        "sentPayloadType" : "net.corda.confidential.SwapIdentitiesFlow$IdentityWithSignature",
        "sentPayload" : {
          "identity" : {
            "class" : "net.corda.core.identity.PartyAndCertificate",
            "deserialized" : "O=BankOfCorda, L=London, C=GB"
          },
          "signature" : "M5DN180OeE4M8jJ3mFohjgeqNYOWXzR6a2PIclJaWyit2uLnmJcZatySoSC12b6e4rQYKIICNFUXRzJnoQTQCg=="
        }
      }
    ],
    "suspendedTimestamp" : "2019-08-12T15:38:39Z",
    "secondsSpentWaiting" : 7
  },
  "flowCallStack" : [
    {
      "flowClass" : "net.corda.finance.flows.CashIssueAndPaymentFlow",
      "progressStep" : "Paying recipient",
      "flowLogic" : {
        "amount" : "10.00 USD",
        "issueRef" : "MTIzNA==",
        "recipient" : "O=BigCorporation, L=New York, C=US",
        "anonymous" : true,
        "notary" : "O=Notary, L=London, C=GB"
      }
    },
    {
      "flowClass" : "net.corda.finance.flows.CashPaymentFlow",
      "progressStep" : "Generating anonymous identities",
      "flowLogic" : {
        "amount" : "10.00 USD",
        "recipient" : "O=BigCorporation, L=New York, C=US",
        "anonymous" : true,
        "issuerConstraint" : [ ],
        "notary" : "O=Notary, L=London, C=GB"
      }
    },
    {
      "flowClass" : "net.corda.confidential.SwapIdentitiesFlow",
      "progressStep" : "Awaiting counterparty's anonymous identity",
      "flowLogic" : {
        "otherSideSession" : {
          "peer" : "O=BigCorporation, L=New York, C=US",
          "ourSessionId" : -5024519991106064492
        },
        "otherParty" : null
      }
    }
  ],
  "origin" : {
    "rpc" : "bankUser"
  },
  "ourIdentity" : "O=BankOfCorda, L=London, C=GB",
  "activeSessions" : [ ],
  "errored" : null
}
```

### Work with flows

Use the different flow commands available to make changes on the ledger. You can `start`, `kill`, `watch`, or `list` flows. You can also perform several commands that help to manage flows that have encountered an error. These are: `retry`, `pause`, `pauseAll`, `retryAllPaused`, `pauseAllHospitalized`, and `retryAllPausedHospitalized`.  You may also find it useful to query flow data.


#### Query flow data

The shell can be used to query flow data. For more information on the types of data that can be queried and instructions for doing so, see the documentation on [Querying flow data](querying-flow-data.html#querying-flow-data-via-the-node-shell).


#### Start a flow

Use this command to start a flow. The `flow start` command takes the name of a flow class, or *any unambiguous substring* thereof, as well as the data to be passed to the flow constructor.

If there are several matches for a given substring, the possible matches will be printed out. If a flow has multiple constructors then the names and types of the arguments will be used to try and automatically determine which one to use. If the match against available constructors is unclear, the reasons each available constructor failed to match will be printed out. In the case of an ambiguous match, the first applicable constructor will be used.

{{< note >}}
`start` is an alias for `flow start`.
{{< /note >}}

##### Example command

Start the `CashIssueFlow` flow:

`flow start CashIssueFlow amount: $1000, issuerBankPartyRef: 1234, notary: "O=Controller, L=London, C=GB"`

This breaks down as follows:

* `flow start` is the shell command for starting a flow.
* `CashIssueFlow` is the name of a flow.
* Each `name: value` pair after that is a flow constructor argument.


If you are unsure of the parameters a specific flow takes, enter `flow start` with the flow name. The missing constructor will be returned. See the example with `CashIssueFlow` below:

```
$>>>flow start CashIssueFlow
No matching constructor found:
- [amount: Amount<Currency>, issuerBankPartyRef: OpaqueBytes, notary: Party]: missing parameter amount
- [request: CashIssueFlow.IssueRequest]: missing parameter request
- [amount: Amount<Currency>, issuerBankPartyRef: OpaqueBytes, notary: Party, progressTracker: ProgressTracker]: missing parameter amount
```

##### Example output

The above command for `CashIssueFlow` invokes the following `CashIssueFlow` constructor:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
class CashIssueFlow(val amount: Amount<Currency>,
                    val issuerBankPartyRef: OpaqueBytes,
                    val recipient: Party,
                    val notary: Party) : AbstractCashFlow(progressTracker)
```
{{% /tab %}}

{{< /tabs >}}



#### Kill a flow

Use this command to kill a single flow, as identified by its UUID.

##### Example command

Kill a flow with a given UUID as follows:

`flow kill f6e08ab5-7a79-4225-a62d-1da910ce269e`

* `flow kill` is the shell command for killing the flow.
* `f6e08ab5-7a79-4225-a62d-1da910ce269e` is an example flow UUID.


##### Example output

This command only works for running flows. The following will be returned if you attempt to kill a flow (identified by its UUID) that is not running:

`Failed to kill flow [f6e08ab5-7a79-4225-a62d-1da910ce269e]`

When a flow is successfully killed, the following output (with the corresponding flow UUID) will be returned:

`Killed flow [f6e08ab5-7a79-4225-a62d-1da910ce269e]`


#### Watch flows

Use this command to display all flows currently running on the node with result (or error) information. When this command is run, the shell waits for flows and logs them as they are run.

##### Command

`flow watch`

#### Example Output

The output will show results listed with flow `Id`, `Flow name`, `Initiator`, and `Status`.

```
Id                                Flow name                                                          Initiator                        Status                                                             
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
27fc3a53-5fc3-4c30-a872-a2f282291 Cash Payment Receiver                                              O=BankOfCorda, L=London, C=GB    No return value                                                    
Waiting for completion or Ctrl-C ...
```

#### List flows

Use this command to list all flows available on the node. You can start all flows listed.

##### Command

`flow list`

#### Example output

This will return an output similar to the output shown below:

```
net.corda.core.flows.ContractUpgradeFlow$Authorise
net.corda.core.flows.ContractUpgradeFlow$Deauthorise
net.corda.core.flows.ContractUpgradeFlow$Initiate
net.corda.finance.flows.CashExitFlow
net.corda.finance.flows.CashIssueAndPaymentFlow
net.corda.finance.flows.CashIssueFlow
net.corda.finance.flows.CashPaymentFlow
net.corda.finance.internal.CashConfigDataFlow
```


#### Retry a flow

Use this command to retry a specific flow that is running on the node, identified by its UUID.

##### Example command

`flow retry f6e08ab5-7a79-4225-a62d-1da910ce269e`

##### Example output

`Retrying flow [f6e08ab5-7a79-4225-a62d-1da910ce269e] succeeded`


#### Pause a flow

Use this command to pause a specific flow that is running on the node, identified by its UUID.

##### Example command

`flow pause dbf76170-a3bf-4704-85a1-274b1b442430`

##### Example output

If the flow is paused successfully, you will see an output similar to the output below:

`Paused flow [dbf76170-a3bf-4704-85a1-274b1b442430]`

If the flow is not paused successfully, you will receive an error message.


#### Pause all flows

Use this command to pause all flows that are running on the node.

##### Command

`flow pauseAll`

##### Output

If all flows are paused successfully, you will see the following output:

`Pausing all flows succeeded.`

If this action is not successful, you will receive an error message.


#### Retry all paused flows

Use this command to retry all paused flows on the node.

##### Command

`flow retryAllPaused`

##### Output

If all flows are retried successfully, you will see the following output:

`Retrying all paused flows succeeded.`

If this action is not successful, you will receive an error message.


#### Pause all hospitalized flows

Use this command to pause all [hospitalized flows](../node-flow-hospital.md).

##### Command

`flow pauseAllHospitalized`

##### Output

If all hospitalized flows are paused successfully, you will see the following output:

`Pausing all Hospitalized flows succeeded.`

If this action is not successful, you will receive an error message.


#### Retry all paused, hospitalized flows

Use this command to retry all paused flows that were hospitalized before they were paused.

##### Command

`flow retryAllPausedHospitalized`

##### Output

If all flows are retried successfully, you will see the following output:

`Retrying all paused hospitalized flows succeeded.`

If not, you will receive an error message.




### Check if a transaction is recorded on the node

Use the `hashLookup` command to check if a transaction matching a specified Id hash value is recorded on the node. If you do not have the needed transaction Id at hand, run `vaultQuery` to find the Id.

#### Example command

The `hashLookup` command is constructed as shown below, with a hexadecimal SHA-256 hash value representing the hashed transaction Id.

`hashLookup F69A7626ACC27042FEEAE187E6BFF4CE666E6F318DC2B32BE9FAF87DF687930C`

#### Example output

If the transaction **is not** recorded on the node, the following will be returned:

`No matching transaction found`

If the transaction **is** recorded on the node, this will be confirmed as below:

`Found a matching transaction with Id: F69A7626ACC27042FEEAE187E6BFF4CE666E6F318DC2B32BE9FAF87DF687930C`


### Extract healthcheck information

Use the `healthcheck` shell command to extract healthcheck information about the running node. This produces the Corda node's JVM runtime information in a JSON format.

#### Command

`healthcheck runtimeInfo`

#### Example output

The output will be similar to the output shown below:

{{< codesample file="/content/en/docs/corda-enterprise/codesamples/healthcheck-runtimeInfo.txt" >}}


### View and update the `run` command output format

You can view and choose the format in which the output of `run` commands will be shown. Valid formats are `json`, `yaml`. The default format is `yaml`.


#### Commands

To see the format currently used run:

`output-format get`


To update the format run:

* `output-format set json` to set the output format to JSON.

* `output-format set yaml` to set the output format to YAML.

{{<warning>}}
This setting only affects the output of `run ...` commands - for example, `run nodeInfo`.

The format of any other shell output is not affected - the result of a flow invocation is simply printed on the console by calling its own `Any#toString` method.
{{</warning>}}


### Shut down the node

You can shut the node down via shell:

* `run gracefulShutdown` will put the node into draining mode, and shut down when there are no flows running.
* `run shutdown` will shut the node down immediately.




### Parameter syntax

Parameters are passed to RPC or flow commands using a syntax called [Yaml](http://www.yaml.org/spec/1.2/spec.html) (yet another markup language), a simple JSON-like language. The key features of Yaml are:


* Parameters are separated by commas.
* Each parameter is specified as a `key: value` pair.
    * There **MUST** be a space after the colon, otherwise you’ll get a syntax error.
* Strings do not need to be surrounded by quotes unless they contain commas, colons, or embedded quotes.
* Class names must be fully-qualified (for example `java.lang.String`).
* Nested classes are referenced using `$`. For example, the `net.corda.finance.contracts.asset.Cash.State`
class is referenced as `net.corda.finance.contracts.asset.Cash$State` (note the `$`).

{{< note >}}
If your CorDapp is written in Java, named arguments won’t work unless you compiled the node using the
`-parameters` argument to `javac`. See the documentation on [Creating nodes locally](../deploy/generating-a-node.md) to learn how to specify it via Gradle.
{{< /note >}}


#### Creating an instance of a class

Class instances are created using curly-bracket syntax. For example, if we have a `Campaign` class with the following constructor:

`data class Campaign(val name: String, val target: Int)`

Then we could create an instance of this class to pass as a parameter as follows:

`newCampaign: { name: Roger, target: 1000 }`

Where `newCampaign` is a parameter of type `Campaign`.


#### Mappings from strings to types

In addition to the types already supported by Jackson, several parameter types can automatically be mapped from strings.
We cover the most common types here.


##### Amount

A parameter of type `Amount<Currency>` can be written as either:


* A dollar ($), pound (£) or euro (€) symbol followed by the amount as a decimal.
* The amount as a decimal followed by the ISO currency code (for example, “100.12 CHF”).


##### SecureHash

A parameter of type `SecureHash` can be written as a hexadecimal string: `F69A7626ACC27042FEEAE187E6BFF4CE666E6F318DC2B32BE9FAF87DF687930C`


##### OpaqueBytes

A parameter of type `OpaqueBytes` can be provided as a UTF-8 string.


##### PublicKey and CompositeKey

A parameter of type `PublicKey` can be written as a Base58 string of its encoded format: `GfHq2tTVk9z4eXgyQXzegw6wNsZfHcDhfw8oTt6fCHySFGp3g7XHPAyc2o6D`.
`net.corda.core.utilities.EncodingUtils.toBase58String` will convert a `PublicKey` to this string format.


##### Party

A parameter of type `Party` can be written in several ways:

* By using the full name: `"O=Monogram Bank,L=Sao Paulo,C=GB"`.
* By specifying the organisation name only: `"Monogram Bank"`.
* By specifying any other non-ambiguous part of the name: `"Sao Paulo"` (if only one network node is located in Sao
Paulo).
* By specifying the public key (see above).


##### NodeInfo

A parameter of type `NodeInfo` can be written in terms of one of its identities (see `Party` above).


##### AnonymousParty

A parameter of type `AnonymousParty` can be written in terms of its `PublicKey` (see above).


##### NetworkHostAndPort

A parameter of type `NetworkHostAndPort` can be written as a “host:port” string: `"localhost:1010"`.


##### Instant and Date

A parameter of `Instant` and `Date` can be written as an ISO-8601 string: `"2017-12-22T00:00:00Z"`.



## Extending the shell

{{< note >}}
This functionality is now only available when running the shell in unsafe mode (see the "Safe Shell" section above). This is because of possible security vulnerabilities caused by the CRaSH shell embedded commands. When shell commands are executed via SSH, a remote user has the ability to effect the node internal state (including running scripts, garbage collection, and even shutting down the node). Prior to Enterprise 4.3 this was possible regardless of the user’s permissions. A user must now have ‘ALL’ as one of their RPC Permissions to be able to use the embedded commands via the unsafe shell. You are advised, where possible to design out dependencies on the CRaSH shell embedded commands (non-Corda commands) and, as a minimum, not to introduce any new dependencies on the unsafe shell environment.
{{< /note >}}

The shell can be extended using commands written in either Java or [Groovy](http://groovy-lang.org/) (a Java-compatible scripting language).
These commands have full access to the node’s internal APIs and thus can be used to achieve almost anything.

A full tutorial on how to write such commands is out of scope for this documentation. To learn more, please refer to the [CRaSH](http://www.crashub.org/) documentation. New commands are placed in the `shell-commands` subdirectory in the node directory. Edits to existing commands will be used automatically, but currently commands added after the node has started won’t be automatically detected. Commands must have names all in lower-case with either a `.java` or `.groovy` extension.


{{< warning >}}
Commands written in Groovy ignore Java security checks, so have unrestricted access to node and JVM internals regardless of any sandboxing that may be in place. Don’t allow untrusted users to edit files in the `shell-commands` directory!

{{< /warning >}}



## Limitations

The shell will be enhanced over time. The currently known limitations include:

* Flows cannot be run unless they override the progress tracker.
* If a command requires an argument of an abstract type, the command cannot be run because the concrete subclass to use cannot be specified using the YAML syntax.
* There is no command completion for flows or RPCs.
* Command history is not preserved across restarts.
* The `jdbc` command requires you to explicitly log into the database first.
* Commands placed in the `shell-commands` directory are only noticed after the node is restarted.
* The `jul` command advertises access to logs, but it doesn’t work with the logging framework used in Corda.
