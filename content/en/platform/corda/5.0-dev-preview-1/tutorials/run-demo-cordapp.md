---
date: 2021-08-20
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-tutorials
    name: Running a sample CorDapp
    weight: 100
    identifier: run-demo-cordapp
title: Running a sample CorDapp
---

Get started with the Corda 5 Developer Preview by running a sample CorDapp. Learn how to deploy and test a CorDapp before you modify the CorDapp template to write your own.

This sample CorDapp lets you launch probes between celestial bodies to send short messages. In this scenario, the solar system represents your local network. The celestial bodies are the nodes on your network. To learn more about nodes, see the [node documentation](../../../../../en/platform/corda/5.0-dev-preview-1/nodes/nodes-homepage.md).

The Solar System CorDapp has an optional smart contract implemented. You can use it to determine if all celestial bodies can receive probes, or if only planets can receive them.

The sample CorDapp contains these nodes:

* Earth
* Mars
* Pluto

The CorDapp has a single flow that you use to send messages between planets: `LaunchProbeFlow`.

The flow takes in three parameters:
{{< table >}}
| Parameter       | Definition                                                                                        | Type        |
|:--------------- |:------------------------------------------------------------------------------------------------- |:----------- |
| `message`       | A message to send with the probe.                                                                 | `String`    |
| `target`        | The X500 name of the probe's target.                                                              | `String` |
| `planetaryOnly` | Determines whether the probe is only able to travel to planets, or if it can visit any celestial body. | `Boolean`   |
{{< /table >}}

## Before you start

Before you run the sample CorDapp:

* Follow the <a href="../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/overview.html#step-by-step-installation-guide">Step-by-step installation guide</a>.
* Read about setting up a [local network](../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/setup-network.md).
* Read about [Corda CLI](../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/overview.md).
* Read about [CorDapp Builder](../../../../../en/platform/corda/5.0-dev-preview-1/packaging/cordapp-builder.md).
* Read about [Corda Node CLI](../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/cli-curl/cli-curl.md).

If you're new to Corda, check out the [CorDapp documentation](../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/overview.md) for key concepts.

## Download the sample CorDapp

{{< note >}}
You can write a CorDapp in any language targeting the JVM. Source files for this CorDapp are provided in Kotlin.
{{< /note >}}

1. Decide where you want to store the sample CorDapp.
2. Open that directory in the command line.
3. Run the following command to clone the repository:

```
git clone https://github.com/corda/corda5-solarsystem-contracts-demo.git
```

The sample project appears in your chosen directory.

## Open the sample CorDapp in IntelliJ IDEA

Open the sample CorDapp in IntelliJ IDEA to explore the CorDapp's structure.

1. Open IntelliJ.
2. Choose **Open** from the top menu.
3. Navigate to the `Corda5-SolarSystem` directory and click **OK**.

The project containing the sample CorDapp opens.

## Deploy the CorDapp using Corda CLI

1. Navigate to the root directory of the project from the command line.

2. Configure the network:

`corda-cli network config docker-compose solar-system`

3. Run a Gradle command to build the CorDapp and generate the `.cpb` file:

  `./gradlew build`

4. Run the `gradle cpk` [task in IntelliJ](https://www.jetbrains.com/help/idea/work-with-gradle-tasks.html#gradle_tasks) to build the CorDapp package (`.cpk`) files of your CorDapp. Most CorDapps will have two files: a `contracts` file and a `workflows` file.

5. Run the `gradle cpb` task in IntelliJ to build the CorDapp package bundle (`.cpb`).

6. Deploy the network using `corda-cli` and `docker-compose`:
  `corda-cli network deploy -n solar-system | docker-compose -f - up`


7. Check the CorDapp's status using [Corda CLI](../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/overview.md):
  `corda-cli network status -n solar-system`

  You'll be able to see the status of the node. The nodes are up and running when their status is `Ready`.

  {{< note >}}
  Take note of the `HTTP RPC port` for each node. You will use these later when you [test the CorDapp using Swagger UI](#test-the-sample-cordapp-using-swagger-ui) or [Corda Node CLI](#test-the-sample-cordapp-using-corda-node-cli).
  {{< /note >}}
8. Install the application on the network using Corda CLI.

In Corda 4, this process was much more involved. Now you can install the application on the network with a single command:

  `corda-cli package install -n solar-system cordaSolarSystem.cpb`

  In this command, you must specify the network and the `.cpb` file.

  After running this command, your CorDapp is up and running.

9. Double-check that everything is working properly:
    1. Open Docker.
    2. Go to **Containers/Apps**.
    3. Select the project.

A drop down opens, displaying each node, its status, and its port.

{{< note >}}
If you need to remove the network, use this command: `corda-cli network terminate -fn <network name>`.
{{< /note >}}

## Test the CorDapp

The Corda 5 Developer Preview provides two options for testing your CorDapp. You can use [Swagger UI](https://swagger.io/tools/swagger-ui/) to visualize and interact with the API. Alternatively, you can test the CorDapp using Corda's Node CLI.

### Test the sample CorDapp using Swagger UI

In Corda 4, you needed to build your own Spring application to test a CorDapp with Swagger UI. The Corda 5 Developer Preview comes with built-in HTTP-RPC. This lets you get Swagger UI up and running quickly, so you can test and interact with your APIs visually.

1. Visit each node's Swagger UI URL. You'll need the ports you noted when [deploying the CorDapp](#deploy-the-cordapp-using-corda-cli):

`https://localhost:<port>/api/v1/swagger`

2. Log in. Use these usernames and passwords for each node:

{{< table >}}
| Planet | Username    | Password   |
|:------ |:----------- |:---------- |
| Earth  | `earthling` | `password` |
| Mars   | `martian`   | `password` |
| Pluto  | `plutonian` | `password` |
{{< /table >}}

These usernames and passwords are specified in the `solar-system.yaml` file.

3. Check which flows are on your CorDapp.
  1. Go to the **FlowStarterRPCOps** heading.
  2. Run the GET request for registered flows: `GET /flowstarter/registeredFlows`
  3. Select **Execute** to run the flow. This flow does not take in any parameters.

  This returns the `LaunchProbeFlow`.

4. Start the `LaunchProbeFlow` by sending a POST request: `POST /flowstarter/startFlow`. Pass the following parameters:

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

In Corda 4, this process was more complicated because you needed a Java or Kotlin application to run the RPCClient. In the Corda 5 Developer Preview, you can run the RPCClient easily with JavaScript.

The `parametersInJson` field includes all parameters that the flow takes in. You must create a JSON string with another JSON inside it, then escape all the characters that matter. To escape the characters, insert `\` before each `"` for each parameter and its value.

The X500 name of the receiving node must be included in the `target` field. The X500 names of all nodes can be found in the `solar-system.yaml` file.

The flow returns a `200` response, including the `flowId` (a `uuid`) and the `clientId`.

5. Take the `flowId` from the previous step to check the flow's status. Under the **FlowStarterRPCOps** heading, run the GET request for flow outcomes (`GET /flowstarter/flowoutcome/{flowid}`). Enter the `flowId` from the response in step 4.

The flow returns a `200` response, which includes these items in the response body:

* Flow status
* Signatures of both parties
* ID of the state

6. Test the contract code. This time, try to send a probe to Pluto with `planetaryOnly` set to `true`.

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
Make sure you assign the `clientId` to a launchpad that isn't already running a flow.
{{< /note >}}

The flow returns a `200` response, including the `flowId` (a `uuid`) and the `clientId`.

7. Take the `flowId` from step 6 and run the GET request for flow outcomes again: `GET /flowstarter/flowoutcome/{flowid}`.

The flow returns a `200` response—but this time the flow has failed because Pluto is not a planet. The `message` says: `Contract verification failed: Failed requirement: Planetary Probes must only visit planets` and includes the contract name and transaction ID.

### Test the sample CorDapp using Corda Node CLI

You can also use Corda Node CLI to test your CorDapp. This tool lets you perform the same tests as Swagger UI, but you do not need a web browser to run it.

1. Add a node to Corda Node CLI so you can use the endpoint to run flows. Use the HTTP RPC port you noted when [deploying the CorDapp](#deploy-the-cordapp-using-corda-cli):

```
corda-node-cli endpoint add -n earth --basic-auth -u earthling -P password https://localhost:<port>/api/v1/
```

2. You are prompted with a message asking if you trust the node. Enter `y` for yes.

3. Set the node you added to the Corda Node CLI as the default node. This means that the flows you run will be sent to that node.

```
corda-node-cli endpoint set -e earth
```

4. List the flows to see what is available. These flows are all authenticated, so you must include the node's username and password in this command:
```
corda-node-cli.cmd flow list -u earthling -P password
```
This returns the flows available in the CorDapp. This CorDapp only has one flow: `net.corda.solarsystem.flows.LaunchProbeFlow`

5. Launch the flow to test its functionality. Pass in the parameters in the same JSON format. Unlike in Swagger UI, you do not need to include the `clientId`. However, you do need to add the username and password again.
```
corda-node-cli flow start -n LaunchProbeFlow -A message="hello" -A target="C=US, L=NINTH, O=PLUTO, OU=DWARF_PLANET" -A planetaryOnly=true -u earthling -P password
```

The flow returns the `clientId` and the `flowId`.

6. Use the `flowId` from step 5 to check the status of the flow.
```
corda-node-cli.cmd flow status -s <flow ID> -u earthling -P password
```

This returns the same output as checking the flow status on Swagger UI. You see:

* Flow status
* Signatures of both parties
* ID of the state

If you have any questions about the Corda Node CLI commands, run the `--help` command for more information.


## Next steps

Now that you've run the Solar System demo CorDapp, try [building your own CorDapp](../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-intro.md).
