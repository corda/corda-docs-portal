---
date: '2022-09-19'
title: "Third-Party Prerequisites for the CSDE"
menu:
  corda-5-alpha:
    parent: corda-5-alpha-start
    identifier: corda-5-alpha-prereqs
    weight: 1000
section_menu: corda-5-alpha
---
This section lists the third-party prerequisites for local deployment with the [CorDapp Standard Development Environment (CSDE)](../cordapp-standard-development-environment/csde.html) and [Simulator](../fast-feedback-with-the-simulator/fast-feedback-with-the-simulator.html).
For information about the prerequisites for multi-worker cluster deployments, see [Third-Party Prerequisites for Cluster Deployments](../../deploying/prerequisites.html).

## Software Prerequisites

Corda 5 Alpha has been tested with the following:

| Software      | Version |
| ----------- | ----------- |
| Operating systems      | <li>Mac OS (intel and ARM)</li><li>Windows 10/11</li><li>Linux</li>     |
| Java   | Azul Zulu JDK 11 (Other versions should work but have not been extensively tested.)  |
| Intellij    | ~v2021.X.Y community edition   |
| git | ~v2.24.1    |
| Docker | Docker Engine ~v20.X.Y or Docker Desktop ~v3.5.X    |

## Additional Configuration for Mac

The current version of the [Corda combined worker](../cordapp-standard-development-environment/csde.html#gradle-helpers-for-the-combined-worker) runs on port 7000.
Some Mac operating systems use port 7000 for the system Control Center.
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
