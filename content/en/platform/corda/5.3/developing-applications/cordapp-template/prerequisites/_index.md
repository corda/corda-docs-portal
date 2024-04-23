---
date: '2023-11-01'
title: "Prerequisites"
description: Discover the prerequisites for the CorDapp template.
menu:
  corda53:
    parent: corda53-develop-get-started
    identifier: corda53-runtime-plugin-prereqs
    weight: 1000

---
# Prerequisites for the CorDapp Template

This section lists the third-party software prerequisites for local deployment with the CorDapp template.

{{< note >}}
You cannot start Corda via the CorDapp template `startCorda` task if any existing local programs are using ports 5432, 9092, 5005, 7004, or 8888. Reserve these ports. For more information, see [Required runtime Gradle plugin Ports](#required-runtime-gradle-plugin-ports).
{{< /note >}}

## Software Prerequisites

The {{< version >}} CorDapp Template has been tested with the following:

| Software                                 | Version                                                             |
| ---------------------------------------- | ------------------------------------------------------------------- |
| Operating systems                        | <li>Mac OS (Intel and ARM)</li><li>Windows 10/11</li><li>Linux</li> |
| Java                                     | Azul Zulu JDK 17                                                    |
| Intellij                                 | ~v2021.x.y Community Edition                                        |
| git                                      | ~v2.24.1                                                            |
| Docker                                   | Docker Engine ~v20.x.y or Docker Desktop ~v3.5.x                    |
| {{< tooltip >}}Corda CLI{{< /tooltip >}} |                                                                     |

## Required CorDapp Template Ports

The current version of the [Corda combined worker]({{< relref "../overview/_index.md#gradle-helpers-for-the-combined-worker" >}}) runs on ports 5432, 9092, 5005, 7004, or 8888. Reserve these ports to avoid errors. For example, some Mac operating systems use port 5005 for the system Control Center. The following section describes how to make that port available.

### Disabling Airplay Receiver on Mac

You can check if your Mac is using port 5005 for Control Center by running `lsof -i :5005` from your terminal. If you see the following results, you must disable Airplay Receiver:

```shell
COMMAND     PID             USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
ControlCe 18519 <your user name>  32u  IPv4 0x775d695bdd932d5d      0t0  TCP *:afs3-fileserver (LISTEN)
ControlCe 18519 <your user name>  33u  IPv6 0x775d6960b58a6055      0t0  TCP *:afs3-fileserver (LISTEN)
```
To disable Airplay Receiver:

1. Select **Sharing** in **Preferences**.
2. Clear the **AirPlay Receiver** check box.
   {{< figure src="switch-off-airplay.png" width="50%" figcaption="AirPlay Receiver in Preferences" alt="Disabling AirPlay Receiver to unblock port 5005" >}}
