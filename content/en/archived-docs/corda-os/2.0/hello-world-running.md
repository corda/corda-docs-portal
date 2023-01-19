---
aliases:
- /releases/release-V2.0/hello-world-running.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-2-0:
    identifier: corda-os-2-0-hello-world-running
    parent: corda-os-2-0-hello-world-introduction
    weight: 1040
tags:
- running
title: Running our CorDapp
---




# Running our CorDapp

Now that we’ve written a CorDapp, it’s time to test it by running it on some real Corda nodes.


## Deploying our CorDapp

Let’s take a look at the nodes we’re going to deploy. Open the project’s `build.gradle` file and scroll down to the
`task deployNodes` section. This section defines three nodes. There are two standard nodes (`PartyA` and
`PartyB`), plus a special Controller node that is running the network map service and advertises a validating notary
service.

```bash
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    directory "./build/nodes"
    networkMap "O=Controller,L=London,C=GB"
    node {
        name "O=Controller,L=London,C=GB"
        advertisedServices = ["corda.notary.validating"]
        p2pPort 10002
        rpcPort 10003
        cordapps = ["net.corda:corda-finance:$corda_release_version"]
    }
    node {
        name "O=PartyA,L=London,C=GB"
        advertisedServices = []
        p2pPort 10005
        rpcPort 10006
        webPort 10007
        cordapps = ["net.corda:corda-finance:$corda_release_version"]
        rpcUsers = [[ user: "user1", "password": "test", "permissions": []]]
    }
    node {
        name "O=PartyB,L=New York,C=US"
        advertisedServices = []
        p2pPort 10008
        rpcPort 10009
        webPort 10010
        cordapps = ["net.corda:corda-finance:$corda_release_version"]
        rpcUsers = [[ user: "user1", "password": "test", "permissions": []]]
    }
}
```

We can run this `deployNodes` task using Gradle. For each node definition, Gradle will:


* Package the project’s source files into a CorDapp jar
* Create a new node in `build/nodes` with our CorDapp already installed

We can do that now by running the following commands from the root of the project:

```bash
// On Windows
gradlew clean deployNodes

// On Mac
./gradlew clean deployNodes
```


## Running the nodes

Running `deployNodes` will build the nodes under `build/nodes`. If we navigate to one of these folders, we’ll see
the three node folders. Each node folder has the following structure:


```bash
.
|____corda.jar                     // The runnable node
|____corda-webserver.jar           // The node's webserver
|____node.conf                     // The node's configuration file
|____plugins
  |____java/kotlin-source-0.1.jar  // Our IOU CorDapp
```



Let’s start the nodes by running the following commands from the root of the project:

```bash
// On Windows
build/nodes/runnodes.bat

// On Mac
build/nodes/runnodes
```

This will start a terminal window for each node, and an additional terminal window for each node’s webserver - eight
terminal windows in all. Give each node a moment to start - you’ll know it’s ready when its terminal windows displays
the message, “Welcome to the Corda interactive shell.”.


![running node](/en/images/running_node.png "running node")


## Interacting with the nodes

Now that our nodes are running, let’s order one of them to create an IOU by kicking off our `IOUFlow`. In a larger
app, we’d generally provide a web API sitting on top of our node. Here, for simplicity, we’ll be interacting with the
node via its built-in CRaSH shell.

Go to the terminal window displaying the CRaSH shell of PartyA. Typing `help` will display a list of the available
commands.

We want to create an IOU of 100 with PartyB. We start the `IOUFlow` by typing:

```python
start IOUFlow iouValue: 99, otherParty: "O=PartyB,L=New York,C=US"
```

This single command will cause PartyA and PartyB to automatically agree an IOU. This is one of the great advantages of
the flow framework - it allows you to reduce complex negotiation and update processes into a single function call.

If the flow worked, it should have recorded a new IOU in the vaults of both PartyA and PartyB. Let’s check.

We can check the contents of each node’s vault by running:

{{< tabs name="tabs-1" >}}
{{% tab name="java" %}}
```java
run vaultQuery contractStateType: com.template.state.IOUState
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
run vaultQuery contractStateType: com.template.IOUState
```
{{% /tab %}}

{{< /tabs >}}

The vaults of PartyA and PartyB should both display the following output:

```bash
states:
- state:
    data:
      value: 99
      lender: "C=GB,L=London,O=PartyA"
      borrower: "C=US,L=New York,O=PartyB"
      participants:
      - "C=GB,L=London,O=PartyA"
      - "C=US,L=New York,O=PartyB"
    contract: "com.template.contract.IOUContract"
    notary: "C=GB,L=London,O=Controller,CN=corda.notary.validating"
    encumbrance: null
    constraint:
      attachmentId: "F578320232CAB87BB1E919F3E5DB9D81B7346F9D7EA6D9155DC0F7BA8E472552"
  ref:
    txhash: "5CED068E790A347B0DD1C6BB5B2B463406807F95E080037208627565E6A2103B"
    index: 0
statesMetadata:
- ref:
    txhash: "5CED068E790A347B0DD1C6BB5B2B463406807F95E080037208627565E6A2103B"
    index: 0
  contractStateClassName: "com.template.state.IOUState"
  recordedTime: 1506415268.875000000
  consumedTime: null
  status: "UNCONSUMED"
  notary: "C=GB,L=London,O=Controller,CN=corda.notary.validating"
  lockId: null
  lockUpdateTime: 1506415269.548000000
totalStatesAvailable: -1
stateTypes: "UNCONSUMED"
otherResults: []
```

This is the transaction issuing our `IOUState` onto a ledger.


## Conclusion

We have written a simple CorDapp that allows IOUs to be issued onto the ledger. Our CorDapp is made up of two key
parts:


* The `IOUState`, representing IOUs on the ledger
* The `IOUFlow`, orchestrating the process of agreeing the creation of an IOU on-ledger


## Next steps

There are a number of improvements we could make to this CorDapp:


* We chould add unit tests, using the contract-test and flow-test frameworks
* We chould change `IOUState.value` from an integer to a proper amount of a given currency
* We could add an API, to make it easier to interact with the CorDapp

But for now, the biggest priority is to add an `IOUContract` imposing constraints on the evolution of each
`IOUState` over time. This will be the focus of our next tutorial.

