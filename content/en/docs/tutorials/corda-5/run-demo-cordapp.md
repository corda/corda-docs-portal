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

1. Decide where you want to store the sample CorDapp.
2. Open that directory in the command line.
3. Run the following command to clone the repository:
