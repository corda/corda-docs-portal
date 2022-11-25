---
date: '2022-09-19'
title: "Prerequisites for the CSDE"
menu:
  corda-5-beta:
    parent: corda-5-beta-start
    identifier: corda-5-beta-prereqs
    weight: 1000
section_menu: corda-5-beta
---

This section lists the third-party software prerequisites for local deployment with the [CorDapp Standard Development Environment (CSDE)](../cordapp-standard-development-environment/csde.html)
For information about the prerequisites for multi-worker cluster deployments, see [Prerequisites for Cluster Deployments](../../deploying/prerequisites.html).

## Software Prerequisites

The Corda 5 Beta CSDE has been tested with the following:

| Software      | Version |
| ----------- | ----------- |
| Operating systems      | <li>Mac OS (intel and ARM)</li><li>Windows 10/11</li><li>Linux</li>     |
| Java   | Azul Zulu JDK 11 (Other versions should work but have not been extensively tested.)  |
| Intellij    | ~v2021.X.Y community edition   |
| git | ~v2.24.1    |
| Docker | Docker Engine ~v20.X.Y or Docker Desktop ~v3.5.X    |
<!--| Gradle |  7.0+   |-->

<!--## Hardware prerequisites

Most of the computers that we use to develop, build, and test Corda 5 have:

| Hardware      | Description |
| ----------- | ----------- |
| CPU      | Gen 9 Intel (6 cores / 12 threads)      |
| RAM   | 32GiB         |
| Hard disk   | At least 30GiB.        |

These are not minimum specifications.
This what is known to work with the code as of Developer Preview 2.-->

## Required CSDE ports

The current version of the [Corda combined worker](../cordapp-standard-development-environment/csde.html#gradle-helpers-for-the-combined-worker) runs on ports 7000, 5432, and 8888. Reserve these ports to avoid errors. For example, some Mac operating systems use port 7000 for the system Control Center. The following section describes how to make the port available.

### Disabling Airplay Receiver on Mac

You can check if your Mac is using port 7000 for Control Center by running `lsof -i :7000` from your terminal. If you see the following results, you must disable Airplay Receiver:

```shell
COMMAND     PID             USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
ControlCe 18519 <your user name>  32u  IPv4 0x775d695bdd932d5d      0t0  TCP *:afs3-fileserver (LISTEN)
ControlCe 18519 <your user name>  33u  IPv6 0x775d6960b58a6055      0t0  TCP *:afs3-fileserver (LISTEN)
```
To disable Airplay Receiver:
1. Select **Sharing** in **Preferences**.
2. Clear the **AirPlay Receiver** check box.
   {{< figure src="switch-off-airplay.png" width="50%" figcaption="AirPlay Receiver in Preferences" alt="Disabling AirPlay Receiver to unblock port 7000" >}}

We hope to fix this clash in a future release.
