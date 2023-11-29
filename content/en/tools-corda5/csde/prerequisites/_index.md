---
date: '2023-11-01'
title: "Prerequisites for the CSDE"
menu:
  corda5-tools:
    parent: corda5-develop-get-started
    identifier: corda5-prereqs
    weight: 1000
section_menu: corda5-tools
---
# Prerequisites for the CSDE
This section lists the third-party software prerequisites for local deployment with the [CorDapp Standard Development Environment (CSDE)]({{< relref "../installing/_index.md" >}}).

{{< note >}}
You cannot start Corda via the CSDE `startCorda` task if any existing local programs are using ports 5432, 5005, or 8888. Reserve these ports. For more information, see [Required CSDE Ports]({{< relref "#required-csde-ports" >}}).
{{< /note >}}

## Software Prerequisites

The {{< version >}} CSDE has been tested with the following:

| Software                                 | Version                                                                             |
| ---------------------------------------- | ----------------------------------------------------------------------------------- |
| Operating systems                        | <li>Mac OS (intel and ARM)</li><li>Windows 10/11</li><li>Linux</li>                 |
| Java                                     | Azul Zulu JDK 11 (Other versions should work but have not been extensively tested.) |
| Intellij                                 | ~v2021.X.Y community edition                                                        |
| git                                      | ~v2.24.1                                                                            |
| Docker                                   | Docker Engine ~v20.X.Y or Docker Desktop ~v3.5.X                                    |
| {{< tooltip >}}Corda CLI{{< /tooltip >}} |                                                                                     |

## Required CSDE Ports

The current version of the [Corda combined worker]({{< relref "../installing/_index.md#gradle-helpers-for-the-combined-worker" >}}) runs on ports 5005, 5432, and 8888. Reserve these ports to avoid errors. For example, some Mac operating systems use port 5005 for the system Control Center. The following section describes how to make the port available.

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

