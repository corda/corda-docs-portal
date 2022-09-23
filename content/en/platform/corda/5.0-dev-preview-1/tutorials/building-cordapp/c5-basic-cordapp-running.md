---
date: '2021-09-22'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-running
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1055
tags:
- tutorial
- cordapp
title: Run your CorDapp
---


## Learning objectives

After you have completed this tutorial, you will know how to deploy, launch, interact with, and use the Swagger API interface to test the CorDapp that you built when following the previous tutorials.

The local Corda network needed for this CorDapp includes one notary and two nodes, each representing a party in the network - Mars Express and Peter. A Corda node is an individual instance of Corda representing one party in a network.

Deploy and run the Mission Mars CorDapp on the following test nodes:

* Notary, which runs a notary service
* PartyA
* PartyB

## Before you start

Before you run your Mission Mars CorDapp, you may want to compare your files to the ones from R3's [missionmars](https://github.com/corda/samples-kotlin-corda5/tree/main/Tutorial/missionmars) solution repository. This should give you a more holistic view of the CorDapp and help to resolve any issues you might have encountered when writing it.

## Deploy your CorDapp to a local Corda 5 network

1. Compile the CorDapp's code into the Corda package files (`.cpk`s) by running the `./gradlew clean build` command from the root of your project. See the [Gradle plugin page](../../../../../../en/platform/corda/5.0-dev-preview-1/packaging/gradle-plugin/overview.md) for more information about using this plugin.

2. Assemble your `.cpk` files into a single Corda package bundle (`.cpb`) file using the CorDapp Builder CLI:

   ```console
   cordapp-builder create --cpk contracts/build/libs/corda5-missionmars-contracts-1.0-SNAPSHOT-cordapp.cpk --cpk workflows/build/libs/corda5-missionmars-workflows-1.0-SNAPSHOT-cordapp.cpk -o missionMars.cpb
   ```

3. Configure the `missionmars-network`:

   ```
   corda-cli network config docker-compose missionmars-network
   ```

4. In the root of your project, create a network definition `mission-mars.yaml` file.

   The network definition `.yaml` file is a template for the network you want to deploy. This template allows you to configure how the nodes will be set up.

5. Add the following parameters to the newly-created `mission-mars.yaml` file:

   ```yaml
   nodes:
     PartyA:
       debug: true
       x500: "C=GB, L=London, O=Mars Express, OU=LLC"
       users:
         user1:
           password: test
         angelenos:
           password: password
           permissions: [ "ALL" ]

     PartyB:
       x500: "C=US, L=New York, O=Peter, OU=INC"
       users:
         user1:
           password: test
         londoner:
           password: password
           permissions: [ "ALL" ]

     PartyC:
       x500: "C=US, L=San Diego, O=Friend, OU=LLC"
       users:
         user1:
           password: test
         newyorker:
           password: password
           permissions: [ "ALL" ]

     notary:
       notary: true
   ```

6. Deploy your network locally and start Docker.

   ```console
   corda-cli network deploy -n missionmars-network -f mission-mars.yaml | docker-compose -f - up -d
   ```

   The `-f` flag allows you to specify the location of the network definition file. See the [Corda CLI commands documentation](../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/commands.html#subcommands) for more information on commands and their flags.

   This step will take some time to complete.

7. Wait for the nodes to run. You can monitor nodes starting by using the following command:

   ```console
   corda-cli network wait -n missionmars-network
    ```

   This command inspects the logs every few seconds until all the nodes are ready.

8. Deploy your CorDapp to all the nodes in the running network using this command:

   ```console
   corda-cli package install -n missionmars-network missionMars.cpb
   ```

   The `package install` command copies the `.cpb` file to the nodes' CorDapps directory and restarts the nodes' containers.

9. Monitor CorDapp deployment by using the following command:

   ```console
   corda-cli network wait -n missionmars-network
   ```

10. Verify the status of the network using the `corda-cli network status -n missionmars-network` command.

    The **Deployed apps** section appears in the command’s output.

**Optional:** To terminate the network, run:
```console
corda-cli network terminate -n missionmars-network -ry
```
{{< warning >}}
Adding the `-ry` flags resets the network and deletes the CorDapp, meaning that you will have to redeploy the CorDapp the next time you want to run it.
{{< /warning >}}
## Interact with your CorDapp

To interact with your CorDapp and to test flows, use the Swagger API interface which is a set of HTTP APIs that you can use out of the box.


### Log in to the Swagger API

1. Open a browser and go to `https://localhost:<port>/api/v1/swagger`. For this app, the ports are:
   * PartyA's node: `12112`
   * PartyB's node: `12116`

   The Swagger API interface is displayed.

   {{< note >}}

   If the default port numbers do not work, confirm if they are correct with what's in the output of the `corda-cli network status -n missionmars-network` command.

   {{< /note >}}

2. To be able to interact with your CorDapp, log in to the node you want to use. For this app, the logins are:

   * PartyA - Username: `angelenos`, Password: `password`
   * PartyB - Username: `londoner`, Password: `password`

   {{< note >}}

   You can find his information in the `mission-mars.yaml` file.

   {{< /note >}}

3. Verify if you have logged in successfully:

   a. Navigate to **FlowStarterRPCOps > GET /flowstarter/registeredflows**.

   b. Click **Try it out** and then **Execute**.

   A **200** success callback code appears and **Response body** lists all implemented flows.


### Test flows

1. Navigate to **FlowStarterRPCOps > POST /flowstarter/startflow**.

2. Click **Try it out**.

3. Delete the `.json` code from the **Request body** and replace it with the one that tests the `CreateAndIssueMarsVoucher` flow:

   ```json
   {
     "rpcStartFlowRequest": {
       "clientId": "launchpad-2",
       "flowName": "net.corda.missionMars.flows.CreateAndIssueMarsVoucherInitiator",
       "parameters": {
         "parametersInJson": "{\"voucherDesc\": \"Space Shuttle 323\", \"holder\": \"C=US, L=New York, O=Peter, OU=INC\"}"
       }
     }
   }
   ```

4. Click **Execute**.

   A **200** success callback code appears and **Response body** lists `uuid` and `clientId`.

   {{< note >}}

   This does not mean the transaction has passed through. It means that the flow has been executed successfully, but the success of the transaction is not guaranteed.

   {{< /note >}}

5. To see the result of the flow, copy `clientId` from the **Response body**.

6. Navigate to **FlowStarterRPCOps > GET /flowstarter/flowoutcomeforclientid/{clientid}**.

7. Click **Try it out**, paste in the copied `clientId`, and click **Execute**.

   A **200** success callback code appears and **Response body** shows the flow's status as **COMPLETED** as well as the details of the output state. You have now completed a full cycle of running a flow.

8. Copy and store the `linearId` from the output in the **Response body**.

   You will need to provide this ID as the `voucherID` when testing the `RedeemBoardingTicketWithVoucher` flow.

9. Repeat all of the above steps for all of your flows.

When running each flow, you must replace the `.json` code for each flow in step 3:

* For the `CreateBoardingTicket` flow, use:

  ```json
  {
    "rpcStartFlowRequest": {
      "clientId": "launchpad-3",
      "flowName": "net.corda.missionMars.flows.CreateBoardingTicketInitiator",
      "parameters": {
        "parametersInJson": "{\"ticketDescription\": \"Space Shuttle 323 - Seat 16B\", \"daysUntilLaunch\": \"10\"}"
      }
    }
  }
  ```

* For the `RedeemBoardingTicketWithVoucher` flow, use:

  {{< note >}}

  You must replace the `voucherID` with `linearId` that you copied and stored in step 8.

  {{< /note >}}

  ```json
  {
    "rpcStartFlowRequest": {
      "clientId": "launchpad-4",
      "flowName": "net.corda.missionMars.flows.RedeemBoardingTicketWithVoucherInitiator",
      "parameters": {
        "parametersInJson": "{\"voucherID\": \"356ec449-da69-4ced-93b5-91c72c55912a\", \"holder\": \"C=US, L=New York, O=Peter, OU=INC\"}"
      }
    }
  }
  ```

## Next steps

Follow the [Write integration tests](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-int-test.md) tutorial to finish this learning path.
