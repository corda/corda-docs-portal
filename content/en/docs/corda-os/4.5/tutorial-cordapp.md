---
aliases:
- /head/tutorial-cordapp.html
- /HEAD/tutorial-cordapp.html
- /tutorial-cordapp.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-5:
    identifier: corda-os-4-5-tutorial-cordapp
    parent: corda-os-4-5-building-a-cordapp-index
    weight: 1030
tags:
- tutorial
- cordapp
title: Running a sample CorDapp
---





# Running a sample CorDapp

To help you get up and running on Corda, a number of sample CorDapps for both Java and Kotlin are available from the [Corda page on GitHub](https://github.com/corda) &mdash;
 see the [Java samples repository](https://github.com/corda/samples-java) and the [Kotlin samples repository](https://github.com/corda/samples-kotlin). This topic describes how to deploy and run a sample CorDapp.

{{< note >}}
If you'd like to deploy and run a sample CorDapp as you work through this topic, ensure that you’ve [set up your development environment](getting-set-up.md) before proceeding.
{{< /note >}}

## Scenario

The local Corda network includes one notary, and three nodes, each representing a party in the network. A Corda node is an individual instance of Corda representing one party in a network. For more information on nodes, see the [node documentation](key-concepts-node.md).

The sample CorDapp allows nodes to agree IOUs with each other, as long as they obey the following contract rules:

* The IOU’s value is strictly positive
* A node is not trying to issue an IOU to itself

This section describes how to deploy and run the sample CorDapp on the following four test nodes:

* **Notary**, which runs a notary service
* **PartyA**
* **PartyB**
* **PartyC**

Because data is only propagated on a need-to-know basis, any IOUs agreed between PartyA and PartyB become “shared facts” between PartyA and PartyB only. PartyC won’t be aware of these IOUs.

## Downloading a sample CorDapp

{{< note >}}
CorDapps can be written in any language targeting the JVM. However, source files for the sample CorDapps are provided in both Kotlin and Java. Since both sets of source files are functionally identical, the instructions in this topic will refer to the Java version.
{{< /note >}}

To download the sample CorDapp, open a command prompt or terminal in the directory where you want to download the sample CorDapp, and run the following command to clone the  samples repository:

{{< tabs name="tabs-1" >}}
{{% tab name="java" %}}
```java
git clone https://github.com/corda/samples-java
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
git clone https://github.com/corda/samples-kotlin
```
{{% /tab %}}

{{< /tabs >}}

The `samples-java` and `samples-kotlin` repositories each contain a number of sample CorDapps. For details of all the sample CorDapps and their features and usage, see the Readme file located within the `samples-java` or `samples-kotlin` folder.

The sample CorDapp that we are going to run and deploy is the **Basic** CorDapp &mdash; the source files for this CorDapp are located in the `Basic\cordapp-example` sub-folder.


## Opening the sample CorDapp in IntelliJ IDEA

To open the sample CorDapp in the IntelliJ IDEA:

1. Open IntelliJ. From the splash screen, click **Open**, navigate to the `Basic\cordapp-example` sub-folder, and click **OK**. The sample CorDapp opens.
3. Specify which JDK you are using. To do this:
    * Click **File** >  **Project Structure**.
    * Under **Project Settings**, click the **Project** option (if not displayed by default).
    * In the **Project SDK** section, click **New…** > **JDK**, then select the home directory of your JDK and click **OK**.
4. Specify the following additional settings:
    * Select **Modules**, then click the **+** button located just above the `cordapp-example` folder and select **Import Module**.
    * On the **Select File or Directory to Import** window, navigate to `samples-java\Basic\cordapp-example` and click **OK**.
    * On the **Import Module** window, select the **Import module from external model** option, then select **Gradle** from the list of options and click **Next**.
    * Select the **Use auto-import** checkbox and click **Finish**, then click **OK**.

    Gradle will now download all the project dependencies and perform some indexing. This usually takes a minute or so.


### Project structure

The `cordapp-example` folder is structured as follows:


```none
.

├── clients
│   ├── build.gradle
│   └── src
│       └── main
│           ├── java
│           │   └── com
│           │       └── example
│           │           └── server
│           │               ├── CONSTANTS.java
│           │               ├── MainController.java
│           │               ├── NodeRPCConnection.java
│           │               └── Server.java
│           │  
│           └── resources
│               ├── application.properties
│               └── public
│                   ├── index.html
│                   └── js
│                       └── angular-module.js
├── config
│   ├── dev
│      └── log4j2.xml
│  
│  
├── contracts-java
│   ├── build.gradle
│   └── src
│       └── main
│           └── java
│               └── com
│                   └── example
│                       ├── contract
│                       │   └── IOUContract.java
│                       ├── schema
│                       │   ├── IOUSchema.java
│                       │   └── IOUSchemaV1.java
│                       └── state
│                           └── IOUState.java
├── contracts-kotlin
│   ├── build.gradle
│   └── src
│       └── main
│           └── kotlin
│               └── com
│                   └── example
│                       ├── contract
│                       │   └── IOUContract
│                       ├── schema
│                       │   └── IOUSchema.kt
│                       └── state
│                           └── IOUState
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
│ 
├── lib
│   ├── README.txt
│   └── quasar.jar
│ 
├── workflows-java
│   ├── build.gradle
│   └── src
│       ├── integrationTest
│       │   └── java
│       │       └── com
│       │           └── example
│       │               └── DriverBasedTests.java
│       ├── main
│       │   └── java
│       │       └── com
│       │           └── example
│       │               └── flow
│       │                   └── ExampleFlow.java
│       └── test
│           └── java
│               └── com
│                   └── example
│                       ├── NodeDriver.java
│                       ├── contract
│                       │   └── IOUContractTests.java
│                       └── flow
│                           └── IOUFlowTests.java
├──  workflows-kotlin
│    ├── build.gradle
│    └── src
│        ├── integrationTest
│        │   └── kotlin
│        │       └── com
│        │           └── example
│        │               └── DriverBasedTests.kt
│        ├── main
│        │   └── kotlin
│        │       └── com
│        │           └── example
│        │               └── flow
│        │                   └── ExampleFlow.kt
│        └── test
│            └── kotlin
│                └── com
│                    └── example
│                        ├── NodeDriver.kt
│                        ├── contract
│                        │   └── IOUContractTests.kt
│                        └── flow
│                            └── IOUFlowTests.kt
├── build.gradle
├── gradle.properties
├── gradlew
├── gradlew.bat
├── LICENCE
├── README.md
├── repositories.gradle
├── settings.gradle
└── TRADEMARK

```

The key files and directories are as follows:

* The **root directory** contains some gradle files, a README, a LICENSE and a TRADEMARK statement
* **clients** contains the source code for Spring Boot integration
* **config** contains the log4j2 configuration
* **contracts-java** and **workflows-java** contain the source code for the sample CorDapp written in Java
* **contracts-kotlin** and **workflows-kotlin** contain the same source code, but written in Kotlin. CorDapps can be developed in either Java and Kotlin
* **gradle** contains the gradle wrapper, which allows the use of Gradle without installing it yourself and worrying about which version is required
* **lib** contains the Quasar jar, which rewrites our CorDapp’s flows to be checkpointable


## Starting the sample CorDapp

Starting the sample CorDapp is a two step-process:
* First, you must deploy the sample CorDapp to a set of test nodes running locally, as described in the section that follows.
* Once you have deployed the CorDapp to the nodes, you must then start the nodes to launch the CorDapp.

### Deploying the CorDapp locally

The first step is to deploy the CorDapp to nodes running locally. To do this:

1. Open a terminal window in the `cordapp-example` directory.
2. Run the `deployNodes` Gradle task to build four nodes with the CorDapp installed on them:
      * Unix/Mac OSX: `./gradlew deployNodes`
      * Windows: `gradlew.bat deployNodes`
3. After the build finishes, navigate to the `workflows-java/build/nodes` or `workflows-kotlin/build/nodes` folder - you should see the following output:
      * A folder for each generated node
      * A `runnodes` shell script for running all the nodes simultaneously on osX
      * A `runnodes.bat` batch file for running all the nodes simultaneously on Windows

      Each node in the `nodes` folder is structured as follows:

```none
. nodeName
├── additional-node-infos  //
├── certificates
├── corda.jar              // The Corda node runtime
├── cordapps               // The node's CorDapps
│   ├── config
│   ├── corda-example-contracts-0.1.jar
│   └── corda-example-workflows-0.1.jar
├── djvm
├── drivers
├── logs
├── network-parameters
├── node.conf              // The node's configuration file
├── nodeInfo-<HASH>        // The hash will be different each time you generate a node
├── persistence.mv.db      // The node's database
└── persistence.trace.db   // The node's database
```



{{< note >}}
`deployNodes` is a utility task that can be used in a development environment to create an entirely new set of nodes for testing a CorDapp. In a production environment, you would instead create a single node as described in [Creating nodes locally](generating-a-node.md) and build your CorDapp JARs as described
in [Building and installing a CorDapp](cordapp-build-systems.md).
{{< /note >}}

### Launching the sample CorDapp

Start the nodes by running the relevant command below from the root of the `cordapp-example` folder:

To run the Java sample CorDapp, run the command that corresponds to your operating system:

* Unix/Mac OSX: `workflows-java/build/nodes/runnodes`
* Windows: `call workflows-java\build\nodes\runnodes.bat`

To run the Kotlin sample CorDapp, run the command that corresponds to your operating system:

* Unix/Mac OSX: `workflows-kotlin/build/nodes/runnodes`
* Windows: `call workflows-kotlin\build\nodes\runnodes.bat`

Start a Spring Boot server for each node by opening a terminal/command prompt for each node and entering the following command, replacing X with A, B and C:


* Unix/Mac OSX: `./gradlew runPartyXServer`
* Windows: `gradlew.bat runPartyXServer`

Look for the `Started Server in X seconds` message &mdash; don’t rely on the % indicator.


{{< warning >}}
On Unix/Mac OSX, do not click/change focus until all seven additional terminal windows have opened, or some nodes may fail to start. You can run `workflows-java/build/nodes/runnodes --headless` to prevent each server from opening in a new terminal window. To interact with the nodes, you will need to use ssh, see [Node shell](shell.md).
{{< /warning >}}


For each node, the `runnodes` script creates a node tab/window:

```none
   ______               __
  / ____/     _________/ /___ _
 / /     __  / ___/ __  / __ `/         Top tip: never say "oops", instead
/ /___  /_/ / /  / /_/ / /_/ /          always say "Ah, Interesting!"
\____/     /_/   \__,_/\__,_/

--- Corda Open Source corda-4.4 (4157c25) -----------------------------------------------


Logs can be found in                    : /Users/joeldudley/Desktop/cordapp-example/workflows-java/build/nodes/PartyA/logs
Database connection url is              : jdbc:h2:tcp://localhost:59472/node
Incoming connection address             : localhost:10005
Listening on port                       : 10005
Loaded CorDapps                         : corda-finance-corda-4.4, cordapp-example-0.1, corda-core-corda-4.4
Node for "PartyA" started up and registered in 38.59 sec


Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Fri Mar 02 17:34:02 GMT 2018>>>
```

It usually takes around 60 seconds for the nodes to finish starting up. Each node will display “Welcome to the Corda interactive shell” along with a prompt when ready.

You can read more about how to generate nodes [here](generating-a-node.md).

## Interacting with the sample CorDapp

You can interact with the sample CorDapp in various ways:

* Via HTTP
* Via the interactive shell (terminal only)
* Via the h2 web console

### Via HTTP

The Spring Boot servers run locally on the following ports:


* PartyA: `localhost:50005`
* PartyB: `localhost:50006`
* PartyC: `localhost:50007`

These ports are defined in `clients/build.gradle`.

Each Spring Boot server exposes the following endpoints:


* `/api/example/me`
* `/api/example/peers`
* `/api/example/ious`
* `/api/example/create-iou` with parameters `iouValue` and `partyName` which is CN name of a node

There is also a web front-end served from the home web page e.g. `localhost:50005`.


{{< warning >}}
The content is only available for demonstration purposes and does not implement
anti-XSS, anti-XSRF or other security techniques. Do not use this code in production.

{{< /warning >}}



#### Creating an IOU via the endpoint

An IOU can be created by sending a PUT request to the `/api/example/create-iou` endpoint directly, or by using the
the web form served from the home directory.

To create an IOU between PartyA and PartyB, run the following command from the command line:

```bash
curl -i -X POST 'http://localhost:50005/api/example/create-iou?iouValue=12&partyName=O=PartyB,L=New%20York,C=US' -H 'Content-Type: application/x-www-form-urlencoded'
```

Note that both PartyA’s port number (`50005`) and PartyB are referenced in the PUT request path. This command
instructs PartyA to agree an IOU with PartyB. Once the process is complete, both nodes will have a signed, notarised
copy of the IOU. PartyC will not.


#### Submitting an IOU via the web front-end

To create an IOU between PartyA and PartyB, navigate to the home directory for the node, click the “create IOU” button at the top-left
of the page, and enter the IOU details into the web-form. The IOU must have a positive value. For example:

```none
Counterparty: Select from list
Value (Int):   5
```

And click submit. Upon clicking submit, the modal dialogue will close, and the nodes will agree the IOU.


#### Checking the output

Assuming all went well, you can view the newly-created IOU by accessing the vault of PartyA or PartyB:

*Via the HTTP API:*


* PartyA’s vault: Navigate to [http://localhost:50005/api/example/ious](http://localhost:50005/api/example/ious)
* PartyB’s vault: Navigate to [http://localhost:50006/api/example/ious](http://localhost:50006/api/example/ious)

*Via home page:*


* PartyA: Navigate to [http://localhost:50005](http://localhost:50005) and hit the “refresh” button
* PartyB: Navigate to [http://localhost:50006](http://localhost:50006) and hit the “refresh” button

The vault and web front-end of PartyC (at `localhost:50007`) will not display any IOUs. This is because PartyC was
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
```


#### Creating an IOU via the interactive shell

We can create a new IOU using the `ExampleFlow$Initiator` flow. For example, from the interactive shell of PartyA,
you can agree an IOU of 50 with PartyB by running
`flow start ExampleFlow$Initiator iouValue: 50, otherParty: "O=PartyB,L=New York,C=US"`.

This will print out the following progress steps:

```none
✅   Generating transaction based on new IOU.
✅   Verifying contract constraints.
✅   Signing transaction with our private key.
✅   Gathering the counterparty's signature.
    ✅   Collecting signatures from counterparties.
    ✅   Verifying collected signatures.
✅   Obtaining notary signature and recording transaction.
    ✅   Requesting signature by notary service
            Requesting signature by Notary service
            Validating response from Notary service
    ✅   Broadcasting transaction to participants
✅   Done
```


#### Checking the output

We can also issue RPC operations to the node via the interactive shell. Type `run` to see the full list of available
operations.

You can see the newly-created IOU by running `run vaultQuery contractStateType: com.example.state.IOUState`.

As before, the interactive shell of PartyC will not display any IOUs.


### Via the h2 web console

You can connect directly to your node’s database to see its stored states, transactions and attachments. To do so,
please follow the instructions in [Node database](node-database.md).


## Running nodes across machines

The nodes can be configured to communicate as a network even when distributed across several machines:


* Deploy the nodes as usual:
    * Unix/Mac OSX: `./gradlew deployNodes`
    * Windows: `gradlew.bat deployNodes`


* Navigate to the build folder (`workflows-java/build/nodes`)
* For each node, open its `node.conf` file and change `localhost` in its `p2pAddress` to the IP address of the machine
where the node will be run (e.g. `p2pAddress="10.18.0.166:10007"`)
* These changes require new node-info files to be distributed amongst the nodes. Use the network bootstrapper tool
(see [Network Bootstrapper](../network-bootstrapper.md)) to update the files and have them distributed locally:`java -jar network-bootstrapper.jar workflows-java/build/nodes`
* Move the node folders to their individual machines (for example, using a USB key). It is important that none of the
nodes - including the notary - end up on more than one machine. Each computer should also have a copy of `runnodes`
and `runnodes.bat`. For example, you may end up with the following layout:
    * Machine 1: `Notary`, `PartyA`, `runnodes`, `runnodes.bat`
    * Machine 2: `PartyB`, `PartyC`, `runnodes`, `runnodes.bat`


* After starting each node, the nodes will be able to see one another and agree IOUs among themselves


{{< warning >}}
The bootstrapper must be run **after** the `node.conf` files have been modified, but **before** the nodes
are distributed across machines. Otherwise, the nodes will not be able to communicate.
{{< /warning >}}


{{< note >}}
If you are using H2 and wish to use the same `h2port` value for two or more nodes, you must only assign them that
value after the nodes have been moved to their individual machines. The initial bootstrapping process requires access to
the nodes’ databases and if two nodes share the same H2 port, the process will fail.
{{< /note >}}

## Testing the CorDapp

Corda provides several frameworks for writing unit and integration tests for CorDapps.


### Contract tests

You can run the CorDapp’s contract tests by running the `Run Contract Tests - Java` run configuration.


### Flow tests

You can run the CorDapp’s flow tests by running the `Run Flow Tests - Java` run configuration.


### Integration tests

You can run the CorDapp’s integration tests by running the `Run Integration Tests - Java` run configuration.



### Running tests in IntelliJ

See [Running tests in IntelliJ](testing.md#tutorial-cordapp-alternative-test-runners).


## Debugging the CorDapp

See [Debugging a CorDapp](debugging-a-cordapp.md).
