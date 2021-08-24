---
date: 2021-08-20
section_menu: tutorials
menu:
  tutorials:
    corda-5:
      name: Corda 5 tutorials
      weight: 100
      identifier: run-demo-cordapp
title: Run a sample CorDapp
---

Get started with the Corda 5 Developer Preview by running a sample CorDapp. Learn how to deploy and test a CorDapp before you modify the CorDapp template to write your own.

This sample CorDapp allows you to launch probes between celestial bodies to send short messages. In this scenario, the solar system represents your local network. The celestial bodies are the nodes on your network. To learn more about nodes, see the [node documentation]().

The solar system CorDapp has an optional smart contract implemented that lets you control if all celestial bodies can receive probes or if only planets can receive them.

The sample CorDapp contains the following nodes:

* Earth
* Mars
* Pluto

The CorDapp has a single flow that you use to send messages between planets: `LaunchProbeFlow`

The flow takes in three parameters:
{{< table >}}
| Parameter       | Definition                                                                                        | Type        |
|:--------------- |:------------------------------------------------------------------------------------------------- |:----------- |
| `message`       | A message to send with the probe.                                                                 | `String`    |
| `target`        | The X500 name of the probe's target.                                                              | `String` |
| `planetaryOnly` | Determines whether the probe is able to travel to only planets or other celestial bodies as well. | `Boolean`   |
{{< /table >}}

## Before you start

Before you can run the sample CorDapp, set up the following:

* A local network
* Corda CLI
* CorDapp Builder
* Node CLI
* Docker

<!-- Add links to documentation for these tools once it is in place. -->

If you're new to Corda, check out the [CorDapp documentation]() for some background knowledge.

## Download the sample CorDapp

{{< note >}}
You can write a CorDapp in any language targeting the JVM. Source files for this CorDapp are provided in Kotlin.
{{< /note >}}

<!--- Update this section after Nina provides details on access. --->

1. Decide where you want to store the sample CorDapp.
2. Open that directory in the command line.
3. Run the following command to clone the repository:

```
git clone git@github.com:corda/Corda5-SolarSystem.git
```

The sample project will appear in your chosen directory.

## Open the sample CorDapp in IntelliJ IDEA

Open the sample CorDapp in IntelliJ IDEA to explore the CorDapp's structure.

1. Open IntelliJ.
2. Choose **Open** from the top menu.
3. Navigate to the `Corda5-SolarSystem` directory and click **OK**.

The project containing the sample CorDapp opens.

## Deploy the CorDapp using Corda CLI

1. Navigate to the root directory of the project from the command line.

2. Deploy your network by building the network deployment Dockerfile using Corda CLI:
  `corda-cli network deploy -n solar-system -f solar-system.yaml > solar-system-compose`

    The `-n` here is the name of the network. The `-f` is the network definition file.

    After running this command, you can see a new `docker-compose.yaml` file in your project. This contains all of the details for your network, which is now ready to go.

2. Run a Gradle command to build the CorDapp and generate the `.cpk` files:

  `gradlew build`

3. Use the `cordapp-builder` CLI utility to bundle the `.cpk` files into an easy-to-use `.cpb` file:

  `cordapp-builder create --cpk contracts\build\libs\corda5-solar-system-contracts-cordapp.cpk --cpk workflows\build\libs\corda5-solar-system-workflows-cordapp.cpk -o corda5-hello-solarsystem.cpb`

  In this command, you specify the `.cpk` files of your CorDapp. Most CorDapps will have two files: a contracts file and a workflows file.

  You also specify the output file. Here the output file is `corda5-hello-solarsystem.cpb`.

  If the command is successful, there is no output.

  If you have an error in your command, the segment with the error is returned in red.

4. Deploy the network using `docker-compose`:
  `docker-compose -f docker-compose.yaml up`

  Here you are specifying the name of the `docker-compose` file generated in step 2.

5. Once the CorDapp is deployed with the Docker network, check the status with Corda CLI:
  `corda-cli network status -n solar-system`

  You'll be able to see the status of the node. The nodes are up and running when their status is `Ready`.

  {{< note >}}
  Take note of the `HTTP RPC port` for each node. You will use these later when you [test the CorDapp using Swagger UI](#test-using-swagger-ui) or [Corda Node CLI](#test-using-corda-node-cli).
  {{< /note >}}
7. Install the application on the network using Corda CLI. In Corda 4, this process was much more involved. Now you can install the application on the network with a single command:

  `corda-cli package install -n solar-system cordaSolarSystem.cpb`

  In this command, you must specify the network and the `.cpb` file.

  After running this command, your CorDapp is up and running.

8. If you want to double check that everything is working properly, open up Docker and go to **Containers/Apps**. Select the project and a drop down opens, displaying each node, its status, and its port.

## Test the CorDapp

The Corda 5 Developer Preview provides two options for testing your CorDapp. You can use [Swagger UI](https://swagger.io/tools/swagger-ui/) to visualize and interact with the API. Alternatively, you can test the CorDapp using Corda's Node CLI.

### Test using Swagger UI

In Corda 4, testing your own CorDapp with Swagger UI added a significant amount of work to your project as you'd have to build your own Spring application to use this tool. However, the Corda 5 Developer Preview comes with built-in HTTP-RPC. This allows you to quickly get Swagger UI up and running, which helps you to test and interact with your APIs visually. Follow these steps to start testing:

1. Using the ports you noted when deploying the CorDapp, visit each node's Swagger UI URL:

`https://localhost:<port>/api/v1/swagger`

2. Click on the button in the top right corner to log in. Use the following usernames and passwords for each node:

{{< table >}}
| Planet | Username    | Password   |
|:------ |:----------- |:---------- |
| Earth  | `earthling` | `password` |
| Mars   | `martian`   | `password` |
| Pluto  | `plutonian` | `password` |
{{< /table >}}

These usernames and passwords are specified in the `solar-system.yaml` file.

3. It's a good idea to check which flows are on your CorDapp before running any. Go to the **FlowStarterRPCOps** heading and run the GET request for registered flows (`GET /flowstarter/registeredFlows`). This flow takes in no parameters, simply click **Execute** to run it. This returns the `LaunchProbeFlow`.

4. Also under the **FlowStarterRPCOps** heading, start the `LaunchProbeFlow` by sending a POST request (`POST /flowstarter/startFlow`). Pass the following parameters:

```
{
  "rpcStartFlowRequest": {
    "clientId": "launchpad-2",
    flowName": "net.corda.solarsystem.flows.LaunchProbeFlow",
    "parameters": {
      "parametersInJson": "{\"message\": \"Hello Mars\", \"target\": \"C=GB, L=FIFTH, O=MARS, OU=PLANET\", \"planetaryOnly\":\"true\"}"
    }
  }
}
```

In Corda 4, this process was more complicated as you needed a Java or Kotlin application to run the RPCClient. The Corda 5 Developer Preview simplifies the process as you can run the RPCClient easily with Javascript.

The `parametersInJson` field includes all parameters that the flow takes in. You must create a JSON string with another JSON inside it, then escape all the characters that matter. For each parameter and its value, insert `\` before the each `"`.

The X500 name of each node can be found in the `solar-system.yaml` file.

The flow returns a `200` response, including the `flowId` (a `uuid`) and the `clientId`.

4. Take the `flowId` from the previous step to check the flow's status. Again under the **FlowStarterRPCOps** heading, run the GET request for flow outcomes (`GET /flowstarter/flowoutcome/{flowid}`). Enter the `flowId` from the response in step 4.

The flow returns a `200` response and includes these items in the response body:

* flow status
* Signatures of both parties
* ID of the state

5. Now let's test the contract code. This time, try to send a probe to Pluto with `planetaryOnly` set to `true`.

```
{
  "rpcStartFlowRequest": {
    "clientId": "launchpad-1",
    flowName": "net.corda.solarsystem.flows.LaunchProbeFlow",
    "parameters": {
      "parametersInJson": "{\"message\": \"Hello Pluto\", \"target\": \"C=GB, L=FIFTH, O=PLUTO, OU=DWARF_PLANET\", \"planetaryOnly\":\"true\"}"
    }
  }
}
```

{{< note >}}
Remember the `clientId` must be assigned to a launchpad that isn't already running a flow.
{{< /note >}}

The flow returns a `200` response, including the `flowId` (a `uuid`) and the `clientId`.

6. Take the `flowId` from step 5 and run the GET request for flow outcomes again (`GET /flowstarter/flowoutcome/{flowid}`).

The flow returns a `200` response but this time the flow has failed because Pluto is not a planet. The `message` indicates `Contract verification failed: Failed requirement: Planetary Probes must only visit planets` and includes the contract name and transaction ID.

### Test using Corda Node CLI

You can also use Corda Node CLI to test your CorDapp. This tool allows you to perform the same tests as Swagger UI, but you do not need a web browser to run it.

1. Add a node to Corda Node CLI so you can use the endpoint to run flows. Use the HTTP RPC port you noted earlier:

```
corda-node-cli endpoint add -n earth --basic-auth -u earthling -P password https://localhost:<port>/api/v1/
```

2. You are prompted with a message asking if you trust the node. Enter `y` for yes.

3. Set the node from step 1 as the default node. This means that the flows you run will be sent to that node.

```
corda-node-cli endpoint set -e earth
```

4. List the flows to see what is available. These flows are all authenticated, so you must include the node's username and password in this command:
```
corda-node-cli.cmd flow list -u earthling -P password
```
This will return the flows available in the CorDapp. As you already know, this CorDapp only has one flow: `net.corda.solarsystem.flows.LaunchProbeFlow`

5. Launch the flow to test its functionality. Pass in the parameters in the same JSON format. Unlike in Swagger UI, you do not need to include the `clientId`. However, you do need to add the username and password once again.
```
corda-node-cli flow start -n LaunchProbeFlow -A message="hello" -A target="C=US, L=NINTH, O=PLUTO, OU=DWARF_PLANET" -A planetaryOnly=true -u earthling -P password
```

The flow returns the `clientId` and the `flowId`.

6. Use the `flowId` from step 5 to check the status of the flow.
```
corda-node-cli.cmd flow status -s <flow ID> -u earthling -P password
```

This returns the same output as checking the flow status on Swagger UI. You see:

* flow status
* Signatures of both parties
* ID of the state

If you have any questions about the Corda Node CLI commands, run the `--help` command for more information.
