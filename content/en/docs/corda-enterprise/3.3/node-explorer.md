---
aliases:
- /releases/3.3/node-explorer.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    parent: corda-enterprise-3-3-node
tags:
- node
- explorer
title: Node Explorer
---


# Node Explorer

The node explorer provides views into a node’s vault and transaction data using Corda’s RPC framework.
            Node Explorer assumes that “corda-finance-3.3.jar” CorDapp is deployed on the node.
            The user can execute cash transaction commands to issue and move cash to other parties on the network or exit cash (eg. remove from the ledger)

The tool is distributed in the form of runnable JAR file: “corda-tools-explorer-3.3.jar”.


## Running the UI

```kotlin
> java -jar corda-tools-explorer-3.3.jar
```

## Interface



Login
User can login to any Corda node using the explorer. Alternatively, `gradlew explorer:runDemoNodes` can be used to start up demo nodes for testing.
                            Corda node address, username and password are required for login, the address is defaulted to `localhost:0` if left blank.
                            Username and password can be configured via the `rpcUsers` field in node’s configuration file.

![login](resources/explorer/login.png "login")

Dashboard
The dashboard shows the top level state of node and vault.
                            Currently, it shows your cash balance and the numbers of transaction executed.
                            The dashboard is intended to house widgets from different CordApps and provide useful information to system admin at a glance.

![dashboard](resources/explorer/dashboard.png "dashboard")

Cash
The cash view shows all currencies you currently own in a tree table format, it is grouped by issuer -> currency.
                            Individual cash transactions can be viewed by clicking on the table row. The user can also use the search field to narrow down the scope.

![vault](resources/explorer/vault.png "vault")

New Transactions
This is where you can create new cash transactions.
                            The user can choose from three transaction types (issue, pay and exit) and any party visible on the network.

General nodes can only execute pay commands to any other party on the network.

![newTransactionCash](resources/explorer/newTransactionCash.png "newTransactionCash")

Issuer Nodes
Issuer nodes can execute issue (to itself or to any other party), pay and exit transactions.
                            The result of the transaction will be visible in the transaction screen when executed.

![newTransactionIssuer](resources/explorer/newTransactionIssuer.png "newTransactionIssuer")

Transactions
The transaction view contains all transactions handled by the node in a table view. It shows basic information on the table e.g. Transaction ID,
                            command type, USD equivalence value etc. User can expand the row by double clicking to view the inputs,
                            outputs and the signatures details for that transaction.

![transactionView](resources/explorer/transactionView.png "transactionView")

Network
The network view shows the network information on the world map. Currently only the user’s node is rendered on the map.
                            This will be extended to other peers in a future release.
                            The map provides an intuitive way of visualizing the Corda network and the participants.

![network](resources/explorer/network.png "network")

Settings
User can configure the client preference in this view.


{{< note >}}
Although the reporting currency is configurable, FX conversion won’t be applied to the values as we don’t have an FX service yet.

{{< /note >}}
![settings](resources/explorer/settings.png "settings")
