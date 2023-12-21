---
description: "Learn how to create a new Corda Package Installer (CPI) for a new version of a Corda-deployed CorDapp or an upgraded Corda cluster."
date: '2023-11-21'
title: "Creating CPIs"
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-networks-cpi
    parent: corda51-networks
    weight: 5000
section_menu: corda51
---
# Creating CPIs

To ensure a trusted and shared model of the business, Network Operators are responsible for creating {{< tooltip >}}CPIs{{< /tooltip >}}. This is usually performed as part of [onboarding the MGM]({{< relref "../creating/mgm/cpi.md">}}) or [onboarding members]({{< relref "../creating/members/cpi.md">}}) to the application network. However, it is also necessary to create a new CPI in the following circumstances:

* A CorDapp Developer [creates a new CPB]({{< relref "../../developing-applications/upgrading/_index.md">}}) for a new version of a Corda-deployed {{< tooltip >}}CorDapp{{< /tooltip >}}.
* A Cluster Administrator [upgrades the Corda platform version]({{< relref "../../deploying-operating/deployment/upgrading/_index.md" >}}).

In these cases, you must create a new CPI, incrementing the `--cpi-version`:

{{< tabs name="build-cpi">}}
{{% tab name="Bash" %}}
```shell
./corda-cli.sh package create-cpi \
--cpb <CPB_FILE> \
--group-policy <GROUP_POLICY_FILE_> \
--cpi-name "<CPI_Name>" \
--cpi-version "2.0.0.0-SNAPSHOT" \
--file <CPI_FILE_NAME> \
--keystore <SIGNING_KEY> \
--storepass "<SIGNING_KEY_PASSWORD>" \
--key "<SIGNING_KEY_NAME>"
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd package create-cpi `
--cpb <CPB_FILE> `
--group-policy <GROUP_POLICY_FILE_> `
--cpi-name "<CPI_Name>" `
--cpi-version "2.0.0.0-SNAPSHOT" `
--file <CPI_FILE_NAME>`
--keystore <SIGNING_KEY> `
--storepass "<SIGNING_KEY_PASSWORD>" `
--key "<SIGNING_KEY_NAME>"
```
{{% /tab %}}
{{< /tabs >}}

Once created, the Cluster Administrator can [apply the new version of the CPI]({{< relref "../../deploying-operating/vnodes/upgrade-cpi.md">}}).
