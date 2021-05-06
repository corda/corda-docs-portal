---
aliases:
- /head/hello-world-running.html
- /HEAD/hello-world-running.html
- /hello-world-running.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-hello-world-running
    parent: corda-os-4-6-hello-world-introduction
    weight: 1040
tags:
- running
title: Running your CorDapp
---




# Running your CorDapp

Now that you've written a CorDapp, it’s time to test it by running it on some real Corda nodes.


## Deploying your CorDapp

Let’s take a look at the nodes you're going to deploy. Open the project’s `build.gradle` file and scroll down to the
`task deployNodes` section. This section defines three nodes. There are two standard nodes (`PartyA` and
`PartyB`), plus a special network map/notary node that is running the network map service and advertises a validating notary
service.

```none
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {

    nodeDefaults {
        projectCordapp {
            deploy = false
        }
        cordapp project(':contracts')
        cordapp project(':workflows')
        runSchemaMigration = true
    }
    node {
        name "O=Notary,L=London,C=GB"
        notary = [validating : false]
        p2pPort 10002
        rpcSettings {
            address("localhost:10003")
            adminAddress("localhost:10043")
        }
    }
    node {
        name "O=PartyA,L=London,C=GB"
        p2pPort 10005
        rpcSettings {
            address("localhost:10006")
            adminAddress("localhost:10046")
        }
        rpcUsers = [[ user: "user1", "password": "test", "permissions": ["ALL"]]]
    }
    node {
        name "O=PartyB,L=New York,C=US"
        p2pPort 10008
        rpcSettings {
            address("localhost:10009")
            adminAddress("localhost:10049")
        }
        rpcUsers = [[ user: "user1", "password": "test", "permissions": ["ALL"]]]
    }
}
```

You can run this `deployNodes` task using Gradle. For each node definition, Gradle will:


* Package the project’s source files into a CorDapp jar.
* Create a new node in `build/nodes` with your CorDapp already installed.

To do this, run the command that corresponds to your operating system from the root of your project:

* Mac OSX: `./gradlew clean deployNodes`
* Windows: `gradlew clean deployNodes`


## Running the nodes

Running `deployNodes` will build the nodes under `build/nodes`. If you navigate to one of these folders, you'll see
the three node folders. Each node folder has the following structure:


```bash
.
|____additional-node-infos
|____certificates
|____corda.jar                  // The runnable node.
|____cordapps
|____djvm
|____drivers
|____logs
|____network-parameters
|____node.conf                // The node's configuration file.
|____nodeInfo
|____persistence.mv.db
|____persistence.trace.db
```


Start the nodes by running the following commands from the root of the project:

* Mac OSX: `build/nodes/runnodes`
* Windows: `build/nodes/runnodes.bat`


This will start a terminal window for each node. Give each node a moment to start - you’ll know it’s ready when its terminal windows displays
the message “Welcome to the Corda interactive shell.”.


{{< figure alt="running node" zoom="/en/images/running_node.png" >}}


## Interacting with the nodes

Now that our nodes are running, let’s order one of them to create an IOU by kicking off our `IOUFlow`. In a larger
app, you’d generally provide a web API sitting on top of our node. Here, for simplicity, you’ll be interacting with the
node via its built-in CRaSH shell.

Go to the terminal window displaying the CRaSH shell of `PartyA`. Typing `help` will display a list of the available
commands.

{{< note >}}
Local terminal shell is available only in a development mode. In a production environment SSH server can be enabled.
More about SSH and how to connect can be found on the [Node shell](shell.md) page.
{{< /note >}}

You want to create an IOU of 99 with `PartyB`. To start the `IOUFlow`, type the following syntax:

```bash
start IOUFlow iouValue: 99, otherParty: "O=PartyB,L=New York,C=US"
```

This single command will cause `PartyA` and `PartyB` to automatically agree an IOU. This is one of the great advantages of
the flow framework - it allows you to reduce complex negotiation and update processes into a single function call.

If the flow worked, it should have recorded a new IOU in the vaults of both `PartyA` and `PartyB`. Let’s check.

You can check the contents of each node’s vault by running:

```bash
run vaultQuery contractStateType: com.template.states.IOUState
```

The vaults of `PartyA` and `PartyB` should both display the following output:

```bash
states:
- state:
    data: !<com.template.states.IOUState>
      value: "99"
      lender: "O=PartyA, L=London, C=GB"
      borrower: "O=PartyB, L=New York, C=US"
    contract: "com.template.contracts.TemplateContract"
    notary: "O=Notary, L=London, C=GB"
    encumbrance: null
    constraint: !<net.corda.core.contracts.SignatureAttachmentConstraint>
      key: "aSq9DsNNvGhYxYyqA9wd2eduEAZ5AXWgJTbTEw3G5d2maAq8vtLE4kZHgCs5jcB1N31cx1hpsLeqG2ngSysVHqcXhbNts6SkRWDaV7xNcr6MtcbufGUchxredBb6"
  ref:
    txhash: "D189448F05D39C32AAAAE7A40A35F4C96529680A41542576D136AEE0D6A80926"
    index: 0
statesMetadata:
- ref:
    txhash: "D189448F05D39C32AAAAE7A40A35F4C96529680A41542576D136AEE0D6A80926"
    index: 0
  contractStateClassName: "com.template.states.IOUState"
  recordedTime: "2020-10-19T11:09:58.183Z"
  consumedTime: null
  status: "UNCONSUMED"
  notary: "O=Notary, L=London, C=GB"
  lockId: null
  lockUpdateTime: null
  relevancyStatus: "RELEVANT"
  constraintInfo:
    constraint:
      key: "aSq9DsNNvGhYxYyqA9wd2eduEAZ5AXWgJTbTEw3G5d2maAq8vtLE4kZHgCs5jcB1N31cx1hpsLeqG2ngSysVHqcXhbNts6SkRWDaV7xNcr6MtcbufGUchxredBb6"
totalStatesAvailable: -1
stateTypes: "UNCONSUMED"
otherResults: []
```

This is the transaction issuing our `IOUState` onto a ledger.

However, if you run the same command on the other node (the notary), you will see the following:

```bash
{
  "states" : [ ],
  "statesMetadata" : [ ],
  "totalStatesAvailable" : -1,
  "stateTypes" : "UNCONSUMED",
  "otherResults" : [ ]
}
```

This is the result of Corda’s privacy model. Because the notary was not involved in the transaction and had no need to see the data, the
transaction was not distributed to them.


## Conclusion

You have written a simple CorDapp that allows IOUs to be issued onto the ledger. This CorDapp is made up of two key
parts:


* The `IOUState`, which represents IOUs on the blockchain.
* The `IOUFlow`, which orchestrates the process of agreeing the creation of an IOU on-ledger.

After completing this tutorial, your CorDapp should look like this:


* Java: [https://github.com/corda/corda-tut1-solution-java](https://github.com/corda/corda-tut1-solution-java)
* Kotlin: [https://github.com/corda/corda-tut1-solution-kotlin](https://github.com/corda/corda-tut1-solution-kotlin)


## Next steps

There are a number of improvements you could make to this CorDapp:

* You could add unit tests, using the contract-test and flow-test frameworks.
* You could change `IOUState.value` from an integer to a proper amount of a given currency.
* You could add an API, to make it easier to interact with the CorDapp.

But for now, the biggest priority is to add an `IOUContract` imposing constraints on the evolution of each
`IOUState` over time - see [Applying contract constraints](tut-two-party-introduction.md).
