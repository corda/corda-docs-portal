---
aliases:
- /head/tutorial-cordapp.html
- /HEAD/tutorial-cordapp.html
- /tutorial-cordapp.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-tutorial-cordapp
    parent: corda-community-4-10-building-a-cordapp-index
    weight: 1030
tags:
- tutorial
- cordapp
title: Run a sample CorDapp
---



# Run a sample CorDapp

Get started with Corda by running a sample CorDapp. Learn how to download, deploy, launch, interact with, and test a CorDapp before you try modifying a [CorDapp template](../../../../tutorials/corda/4.10/community/template-tutorial/writing-a-cordapp-using-a-template.md), [building your own](../../../../tutorials/corda/4.10/community/build-basic-cordapp/basic-cordapp-intro.md), or using a [community CorDapp](https://www.corda.net/samples/).

The local Corda network in the sample includes one notary and two nodes, each representing a party in the network. A Corda node is an individual instance of Corda representing one party in a network. For more information on nodes, see the [node documentation](key-concepts-node.md).

The sample CorDapp allows nodes to reach loan agreements with each other, as long as they obey the following contract rules:

* The loan agreement’s value is strictly positive.
* A node is not trying to issue a loan agreement to itself.

You will deploy and run the sample CorDapp on the following test nodes:

* **Notary**, which runs a notary service
* **PartyA**
* **PartyB**


## Before you start

* Learn [what a CorDapp is](cordapp-overview.md).
* Set up your [development environment](getting-set-up.md).


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



## Step 3: Deploy the CorDapp locally

1. Open the command line from the `cordapp-example` directory.
2. Run the `deployNodes` Gradle task:
      * Unix/Mac OSX: `./gradlew deployNodes`
      * Windows: `gradlew.bat deployNodes`

   This builds three nodes with the CorDapp installed on them.

3. When the build finishes, go to the `build/nodes` folder.

   You will see the following output:

      * A folder for each generated node
      * A `runnodes` shell script for running all the nodes simultaneously on OSX
      * A `runnodes.bat` batch file for running all the nodes simultaneously on Windows

See **Appendix B** for the node structure.


{{< note >}}
`deployNodes` is a utility task that can be used in a development environment to create a new set of nodes for testing a CorDapp. In a production environment, you would create a single node as described in [Creating nodes locally](generating-a-node.md) instead, and build your CorDapp JARs as described
in [Building and installing a CorDapp](cordapp-build-systems.md).
{{< /note >}}


## Step 4: Launch the sample CorDapp

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
On Unix/Mac OSX, do not click/change focus until all seven additional terminal windows have opened, or some nodes may fail to start. You can run `build/nodes/runnodes --headless` to prevent each server from opening in a new terminal window. To interact with the nodes, you will need to use ssh, see [Node shell](shell.md).
{{< /warning >}}


The `runnodes` script creates a node tab/window for each node. It usually takes about 60 seconds for all the nodes to start. Each node displays “Welcome to the Corda interactive shell” along with a prompt. Whilst the `runnodes` script terminates, the two commands to start Party A and B do not and should be run in separate terminal windows.

4. **Optional:** If not all the nodes start successfully the first time, close the terminals and run the script again.

```none
   ______               __
  / ____/     _________/ /___ _
 / /     __  / ___/ __  / __ `/         I won $3M on the lottery so I donated a quarter
/ /___  /_/ / /  / /_/ / /_/ /          of it to charity. Now I have $2,999,999.75.
\____/     /_/   \__,_/\__,_/

--- Corda Community Edition 4.10 (fa98aa7) -------------------------------------------------------------


Logs can be found in                    : /Users/cordauser/src/samples-kotlin/Basic/cordapp-example/build/nodes/PartyA/logs
⚠️   ATTENTION: This node is running in development mode! 👩‍💻   This is not safe for production deployment.
Advertised P2P messaging addresses      : localhost:10005
RPC connection address                  : localhost:10006
RPC admin connection address            : localhost:10046
Loaded 2 CorDapp(s)                     : Contract CorDapp: Example-Cordapp Contracts version 1 by vendor Corda Open Source with licence Apache License, Version 2.0, Workflow CorDapp: Example-Cordapp Flows version 1 by vendor Corda Open Source with licence Apache License, Version 2.0
Node for "PartyA" started up and registered in 8.07 sec


Welcome to the Corda interactive shell.
You can see the available commands by typing 'help'.

Tue Jan 24 16:30:32 GMT 2023>>> Running P2PMessaging loop
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

You can create an IOU by sending a `POST` request to the `/create-iou` endpoint directly, or by using the
the web form served from the home directory.

To create an IOU between PartyA and PartyB, run the following command:

```bash
curl -i -X POST 'http://localhost:50005/create-iou?iouValue=12&partyName=O=PartyB,L=New%20York,C=US' -H 'Content-Type: application/x-www-form-urlencoded'
```

Note that both PartyA’s port number (`50005`) and PartyB are referenced in the POST request path. This command
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

You can connect directly to your node’s database to see its stored states, transactions, and attachments. Follow the instructions in [Node database](../../4.8/enterprise/node/operating/node-database.md).

## Step 6: Test the CorDapp

Corda provides several frameworks for writing unit and integration tests for CorDapps. To access test flows in IntelliJ, select an option from the ‘Run Configurations’ dropdown next to the **hammer icon**.  For a general guide, see [Running tests in IntelliJ](testing.html#tutorial-cordapp-alternative-test-runners).

### Integration tests


First, run an integration test to calibrate your environment.
1. Go to:
   * Kotlin: `workflows > src > integrationTest > kotlin > net.corda.samples.example > DriverBasedTest`
   * Java: `workflows > src > integrationTest > java > net.corda.samples.example > DriverBasedTest`

2. Select the **green arrow** next to the test code. This will open the `Run Terminal`.

### Contract tests

You can run the CorDapp’s contract tests by running the `Run Contract Tests - Java` run configuration.

1. Go to:
   * Kotlin: `contracts > src > test > kotlin > net.corda.samples.example.contracts > ContractTests`
   * Java: `contracts > src > test > java > net.corda.samples.example.contracts > ContractTests`

2. Select the arrow next to the test code. Choose the arrow at the top to run all the tests at once, or select the arrow next to a particular section to test it individually.

### Flow tests

You can run the CorDapp’s flow tests by running the `Run Flow Tests - Java` run configuration.

1. Go to:
   * Kotlin: `workflows > src > test > kotlin > net.corda.samples.example > FlowTests.kt`
   * Java: `workflows > src > test> java > net.corda.samples.example > FlowTests`

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

* [Debugging a CorDapp](debugging-a-cordapp.md)
* [Writing a CorDapp](writing-a-cordapp.md)
* [Build a CorDapp](cordapp-build-systems.md)


## Appendix A: Projects' structure

The `cordapp-example` Java folder is structured as follows:


```none
.

├── clients
│   ├── build.gradle
│   └── src
│       └── main
│           ├── java
│           │   └── net
│           │       └── corda
│           │             └── samples
│           │                   └── example
│           │                         ├── webserver
│           │                         │      ├── Controller.java
│           │                         │      ├── NodeRPCConnection.java
│           │                         │      └── Starter.java
│           │                         │
│           │                         └── Client.java
│           │                     
│           └── resources
│                    └── static
│                           ├── index.html
│                           └── app.js
│                       
├── config
│     ├── dev
│     │     └── log4j2.xml
│     └── test
│            └── log4j2.xml
│  
│  
├── contracts
│   ├── build.gradle
│   └── src
│       ├── main
│       │    └── java
│       │        └── net
│       │              └── corda
│       │                     └── samples
│       │                          └── example
│       │                                ├── contract
│       │                                │     └── IOUContract.java
│       │                                ├── schema
│       │                                │     ├── IOUSchema.java
│       │                                │     └── IOUSchemaV1.java
│       │                                └── states
│       │                                      └── IOUState.java
│       └── test
│            └── java
│                 └── net
│                      └── corda
│                            └── samples
│                                  └── example
│                                        └── contracts
│                                              ├── ContractTests.java
│                                              └── StateTests.java
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
│ 
├── lib
│   ├── README.txt
│   └── quasar.jar
│ 
├── workflows
│   ├── build.gradle
│   └── src
│        ├── integrationTest
│        │   └── java
│        │        └── net
│        │             └── corda
│        │                  └── samples
│        │                         └── example
│        │                                └── DriverBasedTests.java
│        ├── main
│        │   ├── java
│        │   │    └── net
│        │   │        └── corda
│        │   │              └── samples
│        │   │                     └── example
│        │   │                           └── flows
│        │   │                                 └── ExampleFlow.java
│        │   └── resources
│        │            └── migration
│        │                     ├── iou.changelog-master.xml
│        │                     └── iou.changelog-v1.xml
│        │
│        └── test
│            └── java
│                └── net
│                     └── corda
│                           └── samples
│                                 └── example
│                                        └── FlowTests.java
│
├── LICENCE
├── README.md
├── TRADEMARK
├── build.gradle
├── gradle.properties
├── gradlew
├── gradlew.bat
├── repositories.gradle
└── settings.gradle

```

The `cordapp-example` Kotlin folder is structured as follows:


```none
.

├── clients
│   ├── build.gradle
│   └── src
│       └── main
│           ├── kotlin
│           │   └── net
│           │       └── corda
│           │             └── samples
│           │                   └── example
│           │                         ├── webserver
│           │                         │      ├── Controller.kt
│           │                         │      ├── NodeRPCConnection.kt
│           │                         │      └── Server.kt
│           │                         │
│           │                         └── Client.kt
│           │                     
│           └── resources
│                    └── static
│                           ├── index.html
│                           └── app.js
├── config
│   ├── dev
│   │   └── log4j2.xml
│   └──test
│        └── log4j2.xml
│  
│
├── contracts
│   ├── build.gradle
│   └── src
│       ├── main
│       │    └── kotlin
│       │        └── net
│       │            └── corda
│       │                 └── samples
│       │                       └── example
│       │                             ├── contract
│       │                             │     └── IOUContract.kt
│       │                             ├── schema
│       │                             │     └── IOUSchema.kt
│       │                             └── states
│       │                                   └── IOUState.kt                                                    
│       └── test
│            └── kotlin
│                 └── net
│                      └── corda
│                            └── samples
│                                  └── example
│                                        └── contracts
│                                              ├── ContractTests.kt
│                                              └── StateTests.kt
│           
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
│ 
│
├──  workflows
│    ├── build.gradle
│    └── src
│        ├── integrationTest
│        │   └── kotlin
│        │       └── net
│        │            └── corda
│        │                 └── samples
│        │                         └── example
│        │                                └── DriverBasedTests.kt
│        ├── main
│        │   ├── kotlin
│        │   │    └── net
│        │   │        └── corda
│        │   │              └── samples
│        │   │                     └── example
│        │   │                           └── flows
│        │   │                                 └── ExampleFlow.kt
│        │   └── resources
│        │            └── migration
│        │                     ├── iou.changelog-master.xml
│        │                     └── iou.changelog-v1.xml
│        │
│        └── test
│            └── kotlin
│                └── net
│                     └── corda
│                           └── samples
│                                 └── example
│                                        └── FlowTests.kt
├── LICENCE
├── README.md
├── TRADEMARK
├── build.gradle
├── constans.properties
├── gradle.properties
├── gradlew
├── gradlew.bat
├── repositories.gradle
└── settings.gradle


```

The key files and directories are as follows:

* The **root directory** contains some gradle files, a `README`, a `LICENSE`, and a `TRADEMARK` statement.
* **clients** contains the source code for Spring Boot integration.
* **config** contains the Log4j 2 configuration.
* **contracts** and **workflows** contain the source code for the sample CorDapp. CorDapps can be developed in either Java or Kotlin.
* **gradle** contains the Gradle Wrapper, which allows the use of Gradle without installing it yourself and worrying about which version is required.
* **lib** contains the Quasar jar, which rewrites your CorDapp’s flows to be checkpointable.

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
