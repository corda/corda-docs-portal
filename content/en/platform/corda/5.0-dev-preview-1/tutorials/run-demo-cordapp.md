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

* Ensure you have all the [third-party software prerequisites](../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/prerequisites.md).
* Follow the <a href="../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/overview.html#step-by-step-installation-guide">Step-by-step installation guide</a>.
* Read about:
    * Setting up a [local network](../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/setup-network.md).
    * The [Corda CLI](../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/overview.md).
    * The [CorDapp Builder](../../../../../en/platform/corda/5.0-dev-preview-1/packaging/cordapp-builder.md).
    * The [Corda Node CLI](../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/cli-curl/cli-curl.md).
    * The [CorDapp CPK and CPB Gradle plugins](../../../../../en/platform/corda/5.0-dev-preview-1/packaging/gradle-plugin/overview.md).

If you're new to Corda, check out the [CorDapp documentation](../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/overview.md) for key concepts.

## Clone the sample CorDapps repo

{{< note >}}
You can write a CorDapp in any language targeting the JVM. Source files for this CorDapp are provided in Kotlin and Java. Instructions in this tutorial are provided for the Kotlin CorDapp.

You can see both Kotlin and Java versions of the CorDapp in their respective repositories:

* [Solar System CorDapp - Kotlin](https://github.com/corda/samples-kotlin-corda5/tree/main/Tutorial/solarsystem)
* [Solar System CorDapp - Java](https://github.com/corda/samples-java-corda5/tree/main/Tutorial/solarsystem)
{{< /note >}}

1. Decide where you want to store the sample CorDapp.
2. Open that directory in the command line.
3. Run the following command to clone the Kotlin sample CorDapps repository:

   ```console
   git clone https://github.com/corda/samples-kotlin-corda5.git
   ```

   The sample project appears in your chosen directory.

## Open the sample CorDapp in IntelliJ IDEA

Open the sample CorDapp in IntelliJ IDEA to explore the CorDapp's structure.

1. Open IntelliJ.
2. Choose **Open** from the top menu.
3. Navigate to the `solarsystem` directory and click **OK**.

   The project containing the sample CorDapp opens.

## Deploy the CorDapp using Corda CLI

1. Navigate to the root directory of the project from the command line.

2. Configure the network:
   ```console
   corda-cli network config docker-compose solar-system
   ```

3. Run a Gradle command ([or run a Gradle task in IntelliJ](https://www.jetbrains.com/help/idea/work-with-gradle-tasks.html#gradle_tasks)) to build the CorDapp and generate the `.cpb` file:

   ```console
   ./gradlew build
   ```

   This command builds the CorDapp package (`.cpk`) files. Most CorDapps have two files: a `contracts` file and a `workflows` file. The command also builds the CorDapp package bundle (`.cpb`).

4. Compile your `.cpk` files into a single `.cpb` file using the CorDapp Builder CLI:

   ```console
   cordapp-builder create --cpk contracts/build/libs/corda5-solar-system-contracts-demo-contracts-1.0-SNAPSHOT-cordapp.cpk --cpk workflows/build/libs/corda5-solar-system-contracts-demo-workflows-1.0-SNAPSHOT-cordapp.cpk -o corda5-solar-system-1.0-SNAPSHOT-package.cpb
   ```

5. Deploy the network using `corda-cli` and `docker-compose`:
   ```console
   corda-cli network deploy -n solar-system -f solar-system.yaml | docker-compose -f - up -d
   ```
   {{< note >}}
   The `-f` flag lets you specify the location of the network definition file. Since the network and network definition `.yaml` have the same name in this example, you can omit it. It is included here as a best practice example.

   See the [Corda CLI commands documentation](../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/commands.html#subcommands) for more information on commands and their flags.
   {{< /note >}}

   {{< note >}}
   The safest way to view the network contents is to pipe them to Docker.

   While this is *not* the recommended approach, you can also output the contents to a file if you want to see what is happening. Use this command to do so: `corda-cli network deploy -n solar-system -f solar-system.yaml > solar-system-compose.yaml`.
   {{< /note >}}

6. Wait for the network to be ready with:
`corda-cli network wait -n solar-system`

7. Check the network's status using [Corda CLI](../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/overview.md):
   ```console
   corda-cli network status -n solar-system
   ```

     You can see the status of the nodes. The nodes are up and running when their status is `Ready`.

   {{< note >}}
   Take note of the `HTTP RPC port` for each node. You will use these later when you [test the CorDapp using Swagger UI](#test-the-sample-cordapp-using-swagger-ui) or [Corda Node CLI](#test-the-sample-cordapp-using-corda-node-cli).
   {{< /note >}}

8. Install the CorDapp on the network using Corda CLI.

   In Corda 4, this process was much more involved. Now you can install the application on the network with a single command:
   ```console
   corda-cli package install -n solar-system corda5-solar-system-1.0-SNAPSHOT-package.cpb
   ```

   In this command, you must specify the network and the `.cpb` file. Depending on the Gradle setup, the `.cpb` will be in one of the build folders and the name may be different.

   Your CorDapp is now up and running.

9. Double-check that everything is working properly:

    1. Open Docker Desktop.

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

3. Check which flows are on your CorDapp:
   1. Go to the **FlowStarterRPCOps** heading.
   2. Run the GET request for registered flows: `GET /flowstarter/registeredFlows`
   3. Select **Execute** to run the flow. This flow does not take in any parameters.

      This returns the `LaunchProbeFlow`.

4. Start the `LaunchProbeFlow` by sending a POST request: `POST /flowstarter/startFlow`. Pass the following parameters:

   ```console
   {
     "rpcStartFlowRequest": {
       "clientId": "launchpad-2",
       "flowName": "net.corda.solarsystem.flows.LaunchProbeFlow",
       "parameters": {
         "parametersInJson": "{\"message\": \"Hello Mars\", \"target\": \"C=GB, L=FOURTH, O=MARS, OU=PLANET\", \"planetaryOnly\":\"true\"}"
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

   ```console
   {
     "rpcStartFlowRequest": {
       "clientId": "launchpad-1",
       "flowName": "net.corda.solarsystem.flows.LaunchProbeFlow",
       "parameters": {
         "parametersInJson": "{\"message\": \"Hello Pluto\", \"target\": \"C=US, L=NINTH, O=PLUTO, OU=DWARF_PLANET\", \"planetaryOnly\":\"true\"}"
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

   ```console
   corda-node-cli endpoint add -n earth --basic-auth -u earthling -P password https://localhost:<port>/api/v1/
   ```

2. You are prompted with a message asking if you trust the node. Enter `y` for yes.

3. Set the node you added to the Corda Node CLI as the default node. This means that the flows you run will be sent to that node.

   ```console
   corda-node-cli endpoint set -e earth
   ```

4. List the flows to see what is available. These flows are all authenticated, so you must include the node's username and password in this command:
   ```console
   corda-node-cli flow list -u earthling -P password
   ```
   This returns the flows available in the CorDapp. This CorDapp only has one flow: `net.corda.solarsystem.flows.LaunchProbeFlow`

5. Launch the flow to test its functionality. Pass in the parameters in the same JSON format. Unlike in Swagger UI, you do not need to include the `clientId`. However, you do need to add the username and password again.
   ```console
   corda-node-cli flow start -n LaunchProbeFlow -A message="hello" -A target="C=US, L=NINTH, O=MARS, OU=PLANET" -A planetaryOnly=true -u earthling -P password
   ```

   The flow returns the `clientId` and the `flowId`.

6. Use the `flowId` from step 5 to check the status of the flow.
   ```console
   corda-node-cli flow status -s <flow ID> -u earthling -P password
   ```

   This returns the same output as checking the flow status on Swagger UI. You see:

   * Flow status
   * Signatures of both parties
   * ID of the state

If you have any questions about the Corda Node CLI commands, run the `--help` command for more information.

## Set up and test the UI

The Solar System CorDapp comes with a built-in UI. See the <a href="https://github.com/corda/samples-kotlin-corda5/tree/main/Tutorial/solarsystem/Web-UI">`Web-UI`</a> folder of the sample folder to study the code.

### Before you start

Before you can build the Solar System CorDapp UI, you must:

* [Deploy your CorDapp to a local Corda 5 network](#deploy-the-cordapp-using-corda-cli)
* Download the [Node.js](https://nodejs.org/en/download/) asynchronous event-driven JavaScript runtime for your platform. Choose the latest version that is marked as "recommended for most users".
* Ensure that port `3000` is not being used by any other applications.

{{< note >}}
The UI proxy is hard-coded to run on port `3000`. A proxy is used because the current implementation of the web server does not populate any of the CORS headers. The proxy ensures that when the Open API is used by externally-hosted websites, no errors occur on the client side.
{{< /note >}}

### Set up the UI

Follow these steps to start up the UI:

1. Navigate to the `Web-UI` folder of the project.

2. Run this command to set up the React project:

   ```console
   npm install
   ```

   Your `node_modules` and `package-lock.json` are set up.

   {{< note >}}
   You only need to run this command the first time you build the UI.
   {{< /note >}}

3. Run this command to start up the UI:

   ```console
   npm start
   ```

   A message indicating that the UI has been compiled is displayed. You can now open it in your browser.

4. Visit [http://localhost:3000/](http://localhost:3000/) to test the UI.

{{<
  figure
	 src="solar-system-home.png"
	 zoom="solar-system-home.png"
   width=100%
	 figcaption="Solar System CorDapp UI"
	 alt="Solar system CorDapp UI"
>}}

{{<
  figure
	 src="solar-system-earth.png"
	 zoom="solar-system-earth.png"
   width=100%
	 figcaption="Solar System CorDapp UI - Earth"
	 alt="Solar system CorDapp UI - Earth"
>}}

### Test the CorDapp using the UI

Now that you have the UI up and running, test out the same functionalities you tried with [Swagger](#test-the-sample-cordapp-using-swagger-ui) and [Node CLI](#test-the-sample-cordapp-using-corda-node-cli).

1. Click one of the celestial bodies shown to send a probe from that location. Choose from:
    * **Earth**
    * **Mars**
    * **Pluto**

   The homepage of the location you selected is displayed.

   {{< note >}}
   You can open each celestial body in a different browser tab to quickly navigate between them.
   {{< /note >}}

2. Wait for the **Member Information** box to load all info. Your node is connected and your location is ready to send a probe when you can see the **X500 Name**, **Status**, **Platform Version**, and **Serial** values.

3. Send a probe:
    1. Click **SEND PROBE** in the menu.
    2. Enter the message you wish to send to the other celestial body.
    3. Select the checkbox if you want to include the Planetary Only smart contract logic.
    4. Click the **SEND PROBE** button.

       You see your flow status as it progresses from RUNNING to COMPLETE. The probe is sent.

4. **Optional:** Click **CHECK FLOW OUTCOME** to see what happened with your flow.

5. **Optional:** Click **VIEW MESSAGES** to see all messages received in your location.

6. **Optional:** Continue to send probes back and forth.

## Next steps

Now that you've run the Solar System demo CorDapp, [build your own CorDapp](../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-intro.md).
