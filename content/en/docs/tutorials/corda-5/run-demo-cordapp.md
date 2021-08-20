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

Get started with the Corda 5 developer preview by running a sample CorDapp. Learn how to deploy and test a CorDapp before you modify the CorDapp template to write your own.

This sample CorDapp allows you to launch probes between celestial bodies to send short messages. In this scenario, the solar system represents your local network. The celestial bodies are the nodes on your network. To learn more about nodes, see the [node documentation]().

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

Before you can run the sample CorDapp, set up the following tools:

* Corda CLI
* CorDapp Builder
* Node CLI
* Docker

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
2. Build the app with this command:
  `gradlew build`
3. Build the CorDapp with the `cordapp-builder` CLI util:
  `cordapp-builder create --cpk contracts\build\libs\corda5-solar-system-contracts-cordapp.cpk --cpk workflows\build\libs\corda5-solar-system-workflows-cordapp.cpk -o corda5-hello-solarsystem.cpb`
4. Build the network deployment Dockerfile using Corda CLI:
  `corda-cli network deploy -n solar-system -f solar-system.yaml > solar-system-compose`
5. Deploy the network using `docker-compose`:
  `docker-compose -f solar-system-compose up -d`
6. Once the CorDapp is deployed, check the status with Corda CLI:
  `corda-cli network status -n solar-system`

  {{< note >}}
  Take note of the mapped web ports. You will use these later when you [test the CorDapp using Swagger UI](#test-using-swagger-ui).
  {{< /note >}}
7. Install the application on the network using Corda CLI:
  `corda-cli package install -n solar-system cordaSolarSystem.cpb`

## Test the CorDapp

When you are ready to test the CorDapp, you have two options for doing so. You can use [Swagger UI](https://swagger.io/tools/swagger-ui/) to visualize and interact with the API. Alternatively, perhaps if you have additional security requirements, you can test the CorDapp using Corda's Node CLI.

### Test using Swagger UI

1. Using the ports you noted when deploying the CorDapp, visit each node's Swagger UI:

`https://localhost:<port>/api/v1/swagger`

2. Click on the button in the top right corner to log in. Use the following usernames and passwords for each node:

{{< table >}}
| Planet | Username    | Password   |
|:------ |:----------- |:---------- |
| Earth  | `earthling` | `password` |
| Mars   | `martian`   | `password` |
| Pluto  | `plutonian` | `password` |
{{< /table >}}

3. Start the `LaunchProbeFlow` using the Start Flow API. Pass parameters such as the following:

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

4. Check the status of the flow using the ___ API.

### Test using Node CLI
