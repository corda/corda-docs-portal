---
aliases:
- /releases/3.0/tutorial-cordapp.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-tutorial-cordapp
    parent: corda-enterprise-3-0-other-docs
    weight: 1020
tags:
- tutorial
- cordapp
title: The example CorDapp
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}




# The example CorDapp


The example CorDapp allows nodes to agree IOUs with each other, as long as they obey the following contract rules:


* The IOU’s value is strictly positive
* A node is not trying to issue an IOU to itself

We will deploy and run the CorDapp on four test nodes:


* **Notary**, which hosts a validating notary service
* **PartyA**
* **PartyB**
* **PartyC**

Because data is only propagated on a need-to-know basis, any IOUs agreed between PartyA and PartyB become “shared
facts” between PartyA and PartyB only. PartyC won’t be aware of these IOUs.


## Downloading the example CorDapp

Start by downloading the example CorDapp from GitHub:


* Set up your machine by following the [quickstart guide](getting-set-up.md)
* Clone the example CorDapp from the [cordapp-example repository](https://github.com/corda/cordapp-example) using
the following command: `git clone https://github.com/corda/cordapp-example`
* Change directories to the freshly cloned repo: `cd cordapp-example`
* Checkout the branch for Corda Enterprise 3.0 by running `git checkout release-enterprise-V3`


## Opening the example CorDapp in IntelliJ

Let’s open the example CorDapp in IntelliJ IDEA:


* Open IntelliJ
* A splash screen will appear. Click `open`, navigate to the folder where you cloned the `cordapp-example`, and
click `OK`
* Once the project is open, click `File`, then `Project Structure`. Under `Project SDK:`, set the project SDK by
clicking `New...`, clicking `JDK`, and navigating to `C:\Program Files\Java\jdk1.8.0_XXX` (where `XXX` is the
latest minor version number). Click `OK`
* Again under `File` then `Project Structure`, select `Modules`. Click `+`, then `Import Module`, then select
the `cordapp-example` folder and click `Open`. Choose to `Import module from external model`, select
`Gradle`, click `Next` then `Finish` (leaving the defaults) and `OK`
* Gradle will now download all the project dependencies and perform some indexing. This usually takes a minute or so


### Project structure

The example CorDapp has the following structure:

```none
.
├── config
│   ├── dev
│   │   └── log4j2.xml
│   └── test
│       └── log4j2.xml
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── java-source
│   └── ...
├── kotlin-source
│   ├── build.gradle
│   └── src
│       ├── main
│       │   ├── kotlin
│       │   │   └── com
│       │   │       └── example
│       │   │           ├── api
│       │   │           │   └── ExampleApi.kt
│       │   │           ├── client
│       │   │           │   └── ExampleClientRPC.kt
│       │   │           ├── contract
│       │   │           │   └── IOUContract.kt
│       │   │           ├── flow
│       │   │           │   └── ExampleFlow.kt
│       │   │           ├── model
│       │   │           │   └── IOU.kt
│       │   │           ├── plugin
│       │   │           │   └── ExamplePlugin.kt
│       │   │           ├── schema
│       │   │           │   └── IOUSchema.kt
│       │   │           └── state
│       │   │               └── IOUState.kt
│       │   └── resources
│       │       ├── META-INF
│       │       │   └── services
│       │       │       └── net.corda.webserver.services.WebServerPluginRegistry
│       │       ├── certificates
│       │       │   ├── readme.txt
│       │       │   ├── sslkeystore.jks
│       │       │   └── truststore.jks
│       │       ├── exampleWeb
│       │       │   ├── index.html
│       │       │   └── js
│       │       │       └── angular-module.js
│       │       └── nodeConfiguration
│       │           ├── partya.service
│       │           ├── partya-webserver.service
│       │           └── ...
│       ├── test
│       │   └── kotlin
│       │       └── com
│       │           └── example
│       │               ├── NodeDriver.kt
│       │               ├── contract
│       │               │   └── IOUContractTests.kt
│       │               └── flow
│       │                   └── IOUFlowTests.kt
│       └── integrationTest
│           └── kotlin
│               └── com
│                   └── example
│                       └── DriverBasedTests.kt
├── lib
│   ├── README.txt
│   └── quasar.jar
├── .gitignore
├── LICENCE
├── README.md
├── TRADEMARK
├── build.gradle
├── gradle.properties
├── gradlew
├── gradlew.bat
└── settings.gradle
```

The key files and directories are as follows:


* The **root directory** contains some gradle files, a README and a LICENSE
* **config** contains log4j configs
* **gradle** contains the gradle wrapper, which allows the use of Gradle without installing it yourself and worrying
about which version is required
* **lib** contains the Quasar jar which rewrites our CorDapp’s flows to be checkpointable
* **kotlin-source** contains the source code for the example CorDapp written in Kotlin
    * **kotlin-source/src/main/kotlin** contains the source code for the example CorDapp
    * **kotlin-source/src/main/resources** contains the certificate store, some static web content to be served by the
nodes and the WebServerPluginRegistry file
    * **kotlin-source/src/test/kotlin** contains unit tests for the contracts and flows, and the driver to run the nodes
via IntelliJ


* **java-source** contains the same source code, but written in Java. CorDapps can be developed in any language
targeting the JVM


## Running the example CorDapp

There are two ways to run the example CorDapp:


* Via the terminal
* Via IntelliJ

Both approaches will create a set of test nodes, install the CorDapp on these nodes, and then run the nodes. You can
read more about how we generate nodes [here](generating-a-node.md).


### Running the example CorDapp from the terminal


#### Building the example CorDapp


* Open a terminal window in the `cordapp-example` directory
* Make sure you are on the Corda Enterprise 3.0 branch `git checkout release-enterprise-V3`
* Build the test nodes with our CorDapp using the following command:
    * Unix/Mac OSX: `./gradlew deployNodes`
    * Windows: `gradlew.bat deployNodes`

This will automatically build four nodes with our CorDapp already installed

{{< note >}}
CorDapps can be written in any language targeting the JVM. In our case, we’ve provided the example source in
both Kotlin (`/kotlin-source/src`) and Java (`/java-source/src`). Since both sets of source files are
functionally identical, we will refer to the Kotlin version throughout the documentation.

{{< /note >}}

* After the build finishes, you will see the generated nodes in the `kotlin-source/build/nodes` folder
    * There will be a folder for each generated node, plus a `runnodes` shell script (or batch file on Windows) to run
all the nodes simultaneously
    * Each node in the `nodes` folder has the following structure:

```none
. nodeName
├── additional-node-infos  // NodeInfos for the other nodes on the bootstrapped network.
├── certificates           // The node's certificate (Signed by the Doorman).
├── corda.jar              // The Corda node runtime.
├── cordapps               // The node's CorDapps.
├── drivers                // Javaagents.
├── logs                   // The node's log files.
├── network-parameters     // The network parameters for the network this node is part of.
├── node.conf              // The node configuration file.
├── nodeInfo-B98HRS2Y...   // This node's NodeInfo file.
├── drivers                // The node configuration file.
├── persistence.vm.db      // Used by H2.
└── persistence.trace.db   // Used by H2.
```






#### Running the example CorDapp

Start the nodes by running the following command from the root of the `cordapp-example` folder:


* Unix/Mac OSX: `kotlin-source/build/nodes/runnodes`
* Windows: `call kotlin-source\build\nodes\runnodes.bat`


{{< warning >}}
On Unix/Mac OSX, do not click/change focus until all seven additional terminal windows have opened, or some
nodes may fail to start.

{{< /warning >}}


For each node, the `runnodes` script creates a node tab/window:

```none
______               __
```

/ ____/     _________/ /___ _   _______ __   _ _______ _______  ______  _____   ______ _____ _______ _______
/ /     __  / ___/ __  / __ 
{{< warning >}}`{{< /warning >}}

/   
{{< warning >}}|______ | \  |    |    |______ |_____/ |_____] |_____/   |   |______ |______
/ /___  /_/ / /  / /_/ / /_/ /    |______ |  \_|{{< /warning >}}

    |    
{{< warning >}}|______ |    _ |       |    _ __|__{{< /warning >}}

 ______| 
{{< warning >}}|{{< /warning >}}

______


____/     /_/   __,_/__,_/     ____________________________________________________________________________

💡  Administrator users can be granted access to do everything by granting them the ALL permission


* All rights reserved.                                                                                                             *
* This software is proprietary to and embodies the confidential technology of R3 LLC (“R3”).                                       *
* Possession, use, duplication or dissemination of the software is authorized only pursuant to a valid written license from R3.    *
* IF YOU DO NOT HAVE A VALID WRITTEN LICENSE WITH R3, DO NOT USE THIS SOFTWARE.                                                    *

Logs can be found in                    : /Users/username/Desktop/cordapp-example/kotlin-source/build/nodes/Notary/logs
⚠️   ATTENTION: This node is running in developer mode! 👩‍💻   This is not safe for production deployment.
Advertised P2P messaging addresses      : localhost:10006
RPC connection address                  : localhost:10004
RPC admin connection address            : localhost:10038
Loaded 3 CorDapp(s)                     : com.r3.corda.corda-finance version 3.0-RC08 by R3, com.example.cordapp-example version 0.1 by Unknown, corda-core version 3.0-RC08 by Corda Enterprise Edition
Node for “Notary” started up and registered in 50.92 sec

Welcome to the Corda interactive shell.
Useful commands include ‘help’ to see what is available, and ‘bye’ to shut down the node.

Fri Jun 29 11:14:13 BST 2018>>>


For every node except the notary, the script also creates a webserver terminal tab/window:

```none
Logs can be found in /Users/username/Desktop/cordapp-example/kotlin-source/build/nodes/PartyA/logs/web
Starting as webserver: localhost:10009
Webserver started up in 42.02 sec
```

It usually takes around 60 seconds for the nodes to finish starting up. To ensure that all the nodes are running, you
can query the ‘status’ end-point located at `http://localhost:[port]/api/status` (e.g.
`http://localhost:10009/api/status` for `PartyA`).


### Running the example CorDapp from IntelliJ


* Select the `Run Example CorDapp - Kotlin` run configuration from the drop-down menu at the top right-hand side of
the IDE
* Click the green arrow to start the nodes:![run config drop down](/en/images/run-config-drop-down.png "run config drop down")

* To stop the nodes, press the red square button at the top right-hand side of the IDE, next to the run configurations


## Interacting with the example CorDapp


### Via HTTP

The nodes’ webservers run locally on the following ports:


* PartyA: `localhost:10009`
* PartyB: `localhost:10012`
* PartyC: `localhost:10015`

These ports are defined in each node’s node.conf file under `kotlin-source/build/nodes/NodeX/node.conf`.

Each node webserver exposes the following endpoints:


* `/api/example/me`
* `/api/example/peers`
* `/api/example/ious`
* `/api/example/create-iou` with parameters `iouValue` and `partyName` which is CN name of a node

There is also a web front-end served from `/web/example`.


{{< warning >}}
The content in `web/example` is only available for demonstration purposes and does not implement
anti-XSS, anti-XSRF or other security techniques. Do not use this code in production.

{{< /warning >}}



#### Creating an IOU via the endpoint

An IOU can be created by sending a PUT request to the `api/example/create-iou` endpoint directly, or by using the
the web form served from `/web/example`.

To create an IOU between PartyA and PartyB, run the following command from the command line:

```bash
curl -X PUT 'http://localhost:10009/api/example/create-iou?iouValue=1&partyName=O=PartyB,L=New%20York,C=US'
```

Note that both PartyA’s port number (`10009`) and PartyB are referenced in the PUT request path. This command
instructs PartyA to agree an IOU with PartyB. Once the process is complete, both nodes will have a signed, notarised
copy of the IOU. PartyC will not.


#### Submitting an IOU via the web front-end

To create an IOU between PartyA and PartyB, navigate to `/web/example`, click the “create IOU” button at the top-left
of the page, and enter the IOU details into the web-form. The IOU must have a positive value. For example:

```none
Counterparty: Select from list
Value (Int):   5
```

And click submit. Upon clicking submit, the modal dialogue will close, and the nodes will agree the IOU.


#### Checking the output

Assuming all went well, you can view the newly-created IOU by accessing the vault of PartyA or PartyB:

*Via the HTTP API:*


* PartyA’s vault: Navigate to [http://localhost:10009/api/example/ious](http://localhost:10009/api/example/ious)
* PartyB’s vault: Navigate to [http://localhost:10012/api/example/ious](http://localhost:10012/api/example/ious)

*Via web/example:*


* PartyA: Navigate to [http://localhost:10009/web/example](http://localhost:10009/web/example)
* PartyA: Navigate to [http://localhost:10012/web/example](http://localhost:10012/web/example)

The vault and web front-end of PartyC (at `localhost:10015`) will not display any IOUs. This is because PartyC was
not involved in this transaction.


### Via the interactive shell (terminal only)

Nodes started via the terminal will display an interactive shell:

```none
Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Fri Jul 07 16:36:29 BST 2017>>>
```

Type `flow list` in the shell to see a list of the flows that your node can run. In our case, this will return the
following list:

```none
com.example.flow.ExampleFlow$Initiator
net.corda.core.flows.ContractUpgradeFlow$Authorise
net.corda.core.flows.ContractUpgradeFlow$Deauthorise
net.corda.core.flows.ContractUpgradeFlow$Initiate
net.corda.finance.flows.CashConfigDataFlow
net.corda.finance.flows.CashExitFlow
net.corda.finance.flows.CashIssueAndPaymentFlow
net.corda.finance.flows.CashIssueFlow
net.corda.finance.flows.CashPaymentFlow
```


#### Creating an IOU via the interactive shell

We can create a new IOU using the `ExampleFlow$Initiator` flow. For example, from the interactive shell of PartyA,
you can agree an IOU of 50 with PartyB by running
`flow start ExampleFlow$Initiator iouValue: 50, otherParty: "O=PartyB,L=New York,C=US"`.

This will print out the following progress steps:

```none
 ❎   Generating transaction based on new IOU.
 ❎   Verifying contract constraints.
 ✅   Signing transaction with our private key.
 ✅   Gathering the counterparty's signature.
     ✅   Collecting signatures from counterparties.
     ✅   Verifying collected signatures.
 ✅   Obtaining notary signature and recording transaction.
     ❎   Requesting signature by notary service
         ❎   Requesting signature by Notary service
         ❎   Validating response from Notary service
     ✅   Broadcasting transaction to participants
 ✅   Done
Flow completed with result: SignedTransaction(id=7D046CF233FFE0F68338E29273CD0C898FAF0D68ABBC51BFC97463E3425BD253)
```


#### Checking the output

We can also issue RPC operations to the node via the interactive shell. Type `run` to see the full list of available
operations.

You can see the newly-created IOU by running `run vaultQuery contractStateType: com.example.state.IOUState`.

As before, the interactive shell of PartyC will not display any IOUs.


### Via the h2 web console

You can connect directly to your node’s database to see its stored states, transactions and attachments. To do so,
please follow the instructions in [Node database](node-database.md).


### Using the example RPC client

`/src/main/kotlin-source/com/example/client/ExampleClientRPC.kt` defines a simple RPC client that connects to a node,
logs any existing IOUs and listens for any future IOUs. If you haven’t created
any IOUs when you first connect to one of the nodes, the client will simply log any future IOUs that are agreed.


#### Running the client via IntelliJ

Run the ‘Run Example RPC Client’ run configuration. By default, this run configuration is configured to connect to
PartyA. You can edit the run configuration to connect on a different port.


#### Running the client via the command line

Run the following gradle task:

`./gradlew runExampleClientRPCKotlin`

This will connect the RPC client to PartyA and log their past and future IOU activity.

You can close the application using `ctrl+C`.

For more information on the client RPC interface and how to build an RPC client application, see:


* [Client RPC documentation](clientrpc.md)
* [Client RPC tutorial](tutorial-clientrpc-api.md)


## Running nodes across machines

The nodes can be split across different machines and configured to communicate across the network.

After deploying the nodes, navigate to the build folder (`kotlin-source/build/nodes`) and for each node that needs to
be moved to another machine open its config file and change the Artemis messaging address to the IP address of the machine
where the node will run (e.g. `p2pAddress="10.18.0.166:10007"`).

These changes require new node-info files to be distributed amongst the nodes. Use the network bootstrapper tool
(see [Network Bootstrapper](network-bootstrapper.md) for more information on this and how to built it) to update the files and have
them distributed locally.

`java -jar network-bootstrapper.jar kotlin-source/build/nodes`

Once that’s done move the node folders to their designated machines (e.g. using a USB key). It is important that none of the
nodes - including the notary - end up on more than one machine. Each computer should also have a copy of `runnodes`
and `runnodes.bat`.

For example, you may end up with the following layout:


* Machine 1: `Notary`, `PartyA`, `runnodes`, `runnodes.bat`
* Machine 2: `PartyB`, `PartyC`, `runnodes`, `runnodes.bat`

After starting each node, the nodes will be able to see one another and agree IOUs among themselves.

{{< note >}}
If you are using H2 and wish to use the same `h2port` value for all the nodes, then only assign them that
value after the nodes have been moved to their machines. The initial bootstrapping process requires access to the nodes’
databases and if they share the same H2 port then the process will fail.

{{< /note >}}

## Testing and debugging


### Testing a CorDapp

Corda provides several frameworks for writing unit and integration tests for CorDapps.


#### Contract tests

You can run the CorDapp’s contract tests by running the `Run Contract Tests - Kotlin` run configuration.


#### Flow tests

You can run the CorDapp’s flow tests by running the `Run Flow Tests - Kotlin` run configuration.


#### Integration tests

You can run the CorDapp’s integration tests by running the `Run Integration Tests - Kotlin` run configuration.


### Debugging Corda nodes

Debugging is done via IntelliJ as follows:


* Start the nodes using the “Run Example CorDapp” run configuration in IntelliJ
* IntelliJ will build and run the CorDapp. The remote debug ports for each node will be automatically generated and
printed to the terminal. For example:

```none
[INFO ] 15:27:59.533 [main] Node.logStartupInfo - Working Directory: /Users/joeldudley/cordapp-example/build/20170707142746/PartyA
[INFO ] 15:27:59.533 [main] Node.logStartupInfo - Debug port: dt_socket:5007
```


* Edit the “Debug CorDapp” run configuration with the port of the node you wish to connect to
* Run the “Debug CorDapp” run configuration
* Set your breakpoints and interact with the node you’ve connected to. When the node hits a breakpoint, execution will
pause
* The node webserver runs in a separate process, and is not attached to by the debugger



