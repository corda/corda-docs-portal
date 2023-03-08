---
aliases:
- /head/tutorial-cordapp.html
- /HEAD/tutorial-cordapp.html
- /tutorial-cordapp.html
- /releases/release-V4.4/tutorial-cordapp.html
- /docs/corda-os/head/tutorial-cordapp.html
- /docs/corda-os/tutorial-cordapp.html
date: '2021-07-15'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-cordapps
tags:
- tutorial
- cordapp
- deploy
- quickstart
title: Run a sample CorDapp
weight: 20

---
# Run a sample CorDapp

Get started with Corda by running a sample CorDapp. Learn how to download, deploy, launch, interact with, and test a CorDapp before you try [building your own](../get-started/tutorials/build-basic-cordapp/basic-cordapp-intro.md), modifying a [Java](https://github.com/corda/cordapp-template-java) or [Kotlin](https://github.com/corda/cordapp-template-kotlin) template or using a [community CorDapp](https://www.corda.net/samples/).

The local Corda network in the sample includes one notary and two nodes, each representing a party in the network. A Corda node is an individual instance of Corda representing one party in a network. For more information on nodes, see the [node documentation](../../../../../../en/platform/corda/4.9/enterprise/node/component-topology.md).

The sample CorDapp allows nodes to reach loan agreements with each other, as long as they obey the following contract rules:

* The loan agreement’s value is strictly positive.
* A node is not trying to issue a loan agreement to itself.

You will deploy and run the sample CorDapp on the following test nodes:


* **Notary**, which runs a notary service
* **PartyA**
* **PartyB**


## Before you start

* Learn [what a CorDapp is](../../../../../../en/platform/corda/4.9/enterprise/cordapps/cordapp-overview.md).
* Set up your [development environment](../../../../../../en/platform/corda/4.9/enterprise/cordapps/getting-set-up.md).


## Step 1: Download the sample CorDapp

{{< note >}}
CorDapps can be written in any language targeting the JVM. However, source files for the sample CorDapps are provided in both Kotlin and Java. Since both sets of source files are functionally identical, the instructions in this topic will refer to the Java version.
{{< /note >}}

1. Choose a directory to store the sample CorDapp.
2. Open the command line from that directory.
3. Run the following command to clone the sample repository:

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

The sample project folders will appear in your chosen directory.
{{< note >}}

The `samples-java` and `samples-kotlin` repositories each contain a number of sample CorDapps. For details of all the sample CorDapps and their features and usage, see the README file in the `samples-java` or `samples-kotlin` folder. The sample CorDapp that you are going to run and deploy is the **Basic** CorDapp in the `Basic\cordapp-example` sub-folder.


You can see the project structure in Appendix A.
{{< /note >}}


## Step 2: Open the sample CorDapp in IntelliJ IDEA

1. Open IntelliJ.
2. Choose **Open** from the top menu.
3. Navigate to the `Basic\cordapp-example` sub-folder and click **OK**.

The project containing the sample CorDapp opens.



### Step 3: Deploy the CorDapp locally

1. Open the command line from the `cordapp-example` directory.
2. Run the `deployNodes` Gradle task:
      * Unix/Mac OSX: `./gradlew deployNodes`
      * Windows: `gradlew.bat deployNodes`

   This builds three nodes with the CorDapp installed on them.

3. When the build finishes, go to the `workflows-java/build/nodes` or `workflows-kotlin/build/nodes` folder.

You will see the following output:
      * A folder for each generated node
      * A `runnodes` shell script for running all the nodes simultaneously on OSX
      * A `runnodes.bat` batch file for running all the nodes simultaneously on Windows

    See **Appendix B** for the node structure.


{{< note >}}
`deployNodes` is a utility task that can be used in a development environment to create a new set of nodes for testing a CorDapp. In a production environment, you would create a single node as described in [Creating nodes locally](../node/deploy/generating-a-node.md) instead, and build your CorDapp JARs as described
in [Building and installing a CorDapp](cordapp-build-systems.md).
{{< /note >}}


### Step 4: Launch the sample CorDapp

To start the nodes and the sample CorDapp:

1. Run the command that corresponds to your operating system:

* Unix/Mac OSX: `./build/nodes/runnodes`
* Windows: `.\build\nodes\runnodes.bat`

2. Start a Spring Boot server for Party A. Run the command:

* Unix/Mac OSX: `./gradlew runPartyAServer`
* Windows: `gradlew.bat runPartyAServer`

Look for the `Started Server in X seconds` message &mdash; don’t rely on the % indicator.

3. Repeat the command to start the server for Party B:

* Unix/Mac OSX: `./gradlew runPartyBServer`
* Windows: `gradlew.bat runPartyBServer`


{{< warning >}}
On Unix/Mac OSX, do not click/change focus until all seven additional terminal windows have opened, or some nodes may fail to start. You can run `workflows-java/build/nodes/runnodes --headless` to prevent each server from opening in a new terminal window. To interact with the nodes, you will need to use ssh, see [Node shell](../../../../../../en/platform/corda/4.9/enterprise/node/operating/shell.md).
{{< /warning >}}


The `runnodes` script creates a node tab/window for each node. It usually takes about 60 seconds for all the nodes to start. Each node displays “Welcome to the Corda interactive shell” along with a prompt.

```none
   ______               __
  / ____/     _________/ /___ _
 / /     __  / ___/ __  / __ `/         Top tip: never say "oops", instead
/ /___  /_/ / /  / /_/ / /_/ /          always say "Ah, Interesting!"
\____/     /_/   \__,_/\__,_/

--- Corda Community Edition corda-4.9 (4157c25) -----------------------------------------------


Logs can be found in                    : /Users/cordauser/Desktop/cordapp-example/workflows-java/build/nodes/PartyA/logs
Database connection url is              : jdbc:h2:tcp://localhost:59472/node
Incoming connection address             : localhost:10005
Listening on port                       : 10005
Loaded CorDapps                         : corda-finance-corda-4.9, cordapp-example-0.1, corda-core-corda-4.9
Node for "PartyA" started up and registered in 38.59 sec


Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Fri Mar 02 17:34:02 GMT 2018>>>
```


## Step 5: Interact with the sample CorDapp

You can interact with the sample CorDapp:

* Via HTTP
* Via the interactive shell (terminal only)
* Via the h2 web console

### Via HTTP

The Spring Boot servers run locally on the following ports:

* PartyA: `localhost:50005`
* PartyB: `localhost:50006`

These ports are defined in `clients/build.gradle`.

Each Spring Boot server exposes the following endpoints:

* `/me`
* `/peers`
* `/ious`
* `/create-iou` with parameters `iouValue` and `partyName` which is CN name of a node

There is also a web front-end served from the home web page (for example, `localhost:50005`).


{{< warning >}}
The content is only available for demonstration purposes and does not implement
anti-XSS, anti-XSRF or other security techniques. Do not use this code in production.

{{< /warning >}}


#### Create an IOU via the endpoint


You can create an IOU by sending a `PUT` request to the `/create-iou` endpoint directly, or by using the web form served from the home directory.

To create an IOU between PartyA and PartyB, run the following command:

```bash
curl -i -X POST 'http://localhost:50005/create-iou?iouValue=12&partyName=O=PartyB,L=New%20York,C=US' -H 'Content-Type: application/x-www-form-urlencoded'
```

Note that both PartyA’s port number (`50005`) and PartyB are referenced in the PUT request path. This command
instructs PartyA to agree an IOU with PartyB. Once the process is complete, both nodes will have a signed, notarised
copy of the IOU.


### Via the interactive shell (command line only)

Nodes started via the command line will display an interactive shell:

```none
Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Mon May 10 16:36:29 BST 2021>>>
```

Type `flow list` in the shell to see a list of the flows that your node can run. In our case, this will return the
following list:

```none
net.corda.samples.example.flows.ExampleFlow$Initiator
net.corda.core.flows.ContractUpgradeFlow$Authorise
net.corda.core.flows.ContractUpgradeFlow$Deauthorise
net.corda.core.flows.ContractUpgradeFlow$Initiate
```


#### Create an IOU via the interactive shell

You can create a new IOU using the `ExampleFlow$Initiator` flow. For example, from the interactive shell of Party A,
you can agree an IOU of 50 with Party B by running
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


#### Check the output

You can also issue RPC operations to the node via the interactive shell. Type `run` to see the full list of available
operations.

You can see the newly-created IOU by running `run vaultQuery contractStateType: net.corda.samples.example.states.IOUState`.

### Via the h2 web console


You can connect directly to your node’s database to see its stored states, transactions and attachments. Follow the instructions in [Node database](../../../../../../en/platform/corda/4.9/enterprise/node/operating/node-database.md).


## Step 6: Test the CorDapp

Corda provides several frameworks for writing unit and integration tests for CorDapps. To access test flows in IntelliJ, select an option from the ‘Run Configurations’ dropdown next to the **hammer icon**.  For a general guide, see [Running tests in IntelliJ](../testing.html#running-tests-in-intellij).

### Integration tests


First, run an integration test to calibrate your environment.
1. Go to `Workflows` > `src` > `IntegrationTest` > `DriverBasedTest`.
2. Select the **green arrow** next to the test code. This will open the Run Terminal.

### Contract tests

You can run the CorDapp’s contract tests by running the `Run Contract Tests - Java` run configuration.

1. Go to `Workflow` > `src` > `test` > `ContractTests`.
2. Select the arrow next to the test code. Choose the arrow at the top to run all the tests at once, or select the arrow next to a particular section to test it individually.

### Flow tests

You can run the CorDapp’s flow tests by running the `Run Flow Tests - Java` run configuration.

1. Go to `Workflow` > `src` > `test` > `FlowTests`.
2. Select the **arrow** next to the test code. Choose the arrow at the top to run all the tests at once, or select the arrow next to a particular section to test it individually.

### Debug a test

If your test fails, run a Gradle test instead of a unit test.

1. Open the **Gradle** tab on the right-hand side of your IntelliJ window.
2. Open **Build Tool Settings** (wrench icon) and select **Gradle Settings**.
3. Set Gradle as the default in your **Build and Run** settings and click **Apply**.
4. Go to **Run Configurations** (next to the hammer icon) and select **Edit Configurations**.
5. Delete the unit test driver and click **Apply**.
6. Return to your test code. You will see the **Gradle icon** (an elephant).
7. Select the **Gradle icon** to run your test.


## Related Content

* [Debugging a CorDapp](../../../../../../en/platform/corda/4.9/enterprise/cordapps/debugging-a-cordapp.md)
* [Writing a CorDapp](../../../../../../en/platform/corda/4.9/enterprise/cordapps/writing-a-cordapp.md)
* [Build a CorDapp](../../../../../../en/platform/corda/4.9/enterprise/cordapps/cordapp-build-systems.md)


## Appendix A: Project structure

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

* The **root directory** contains some gradle files, a `README`, a `LICENSE`, and a `TRADEMARK` statement.
* **clients** contains the source code for Spring Boot integration.
* **config** contains the Log4j 2 configuration.
* **contracts-java** and **workflows-java** contain the source code for the sample CorDapp written in Java.
* **contracts-kotlin** and **workflows-kotlin** contain the same source code, but written in Kotlin. CorDapps can be developed in either Java and Kotlin
* **gradle** contains the Gradle Wrapper, which allows the use of Gradle without installing it yourself and worrying about which version is required.
* **lib** contains the Quasar jar, which rewrites your CorDapp’s flows to be checkpointable.

## Appendix B: Node structure

Each node in the `nodes` folder is structured as follows:

```
=======

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

## Appendix B: Node structure

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
