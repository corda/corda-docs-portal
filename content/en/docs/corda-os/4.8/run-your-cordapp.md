---
aliases:
- /head/hello-world-running.html
- /HEAD/hello-world-running.html
- /hello-world-running.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-hello-world-running
    parent: corda-os-4-8-hello-world-introduction
    weight: 1040
tags:
- running
title: Run your CorDapp
---

# Run your CorDapp

Now that you've written a CorDapp, it’s time to test it by running it on some real Corda nodes.


## Build your nodes

Let’s take a look at the nodes you're going to deploy.

1. Open the project’s root directory `build.gradle` file in IntelliJ and scroll down to the `task deployNodes` section.


      This section defines three nodes. There are two standard nodes (`PartyA` and `PartyB`), plus a special network map/notary node that is running the network map service and advertises a validating notary service.

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

2. Click the right-hand side **Gradle** tab and open the **cordformation** folder. Double-click **deployNodes**.

   For each node definition, Gradle will:

   * Package the project’s source files into a CorDapp `.jar`.
   * Create a new node in `build/nodes` with your CorDapp already installed.

## Run the nodes

Running `deployNodes` builds the nodes under `build/nodes`. If you navigate to one of these folders, you'll see
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

1. In the IntelliJ terminal window, navigate to `build/nodes` from the root directory.

2. Start the nodes by running the following command:

   * Mac OSX: `runnodes`
   * Windows: `runnodes.bat`

This starts a terminal window for each node. Give each node a moment to start - you’ll know it’s ready when its terminal windows displays
the message “Welcome to the Corda interactive shell.”.


{{< figure alt="running node" zoom="/en/images/running_node.png" >}}


## Start the IOU flow

Once your nodes are running, order one of them to create an IOU by triggering the `IOUFlow`. In a larger
app, you’d generally provide a web API sitting on top of your node. Here, for simplicity, you’ll be interacting with the
node via its built-in CRaSH shell.

1. Go to the terminal window displaying the CRaSH shell of `PartyA`.

2. Type `help` to display a list of the available commands.

   {{< note >}}
   The local terminal shell is only available in development mode. In a production environment, you can enable an SSH server.
   You can find more about SSH on the [Node shell](shell.md) page.
   {{< /note >}}

3. Create an IOU of 99 with `PartyB`. To start the `IOUFlow`, type the following syntax:

   ```bash
   start IOUFlow iouValue: 99, otherParty: "O=PartyB,L=New York,C=US"
   ```

   This single command will cause `PartyA` and `PartyB` to automatically agree an IOU. This is one of the great advantages of
   the flow framework - it allows you to reduce complex negotiation and update processes into a single function call.

   Starting this flow will return the following:
   ```bash
   ✅   Starting
          Requesting signature by Notary Service
              Requesting signature by Notary Service
              Validating response from Notary Service
      ✅   Broadcasting transaction to participants
    ➡️   Done
    Flow completed with result: null
    ```

    If the flow worked, there should be a record of a new IOU in the vaults of both `PartyA` and `PartyB`..

4. Check the contents of each node’s vault by running:

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

      This is the transaction issuing your `IOUState` onto a ledger.

5. If you run the same command on the other node (the notary), you will see the following:

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

You could make several improvements to this CorDapp. You could:

* Add unit tests, using the contract-test and flow-test frameworks.
* Change `IOUState.value` from an integer to a proper amount of a given currency.
* Add an API, to make it easier to interact with the CorDapp.

The biggest priority for your next step is to add an `IOUContract` imposing constraints on the evolution of each
`IOUState` over time - see [Applying contract constraints](tut-two-party-introduction.md).
