---
date: '2023-03-21'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    identifier: digital-currencies-launching-demo
    name: Launching the Digital Currencies Demo
    description: "Digital Currencies documentation describing how to launch the Digital Currencies demo"
title: Launching the Digital Currencies Demo
weight: 150
---

In a browser access the relevant URL:

* Development: [http://localhost:5174](http://localhost:5174)
* Production: [http://localhost:5174](http://localhost:4173)
* Docker: [http://localhost:80](http://localhost:80)

The **Participants** page is displayed:

{{< 
      figure
	  src="images/participants-page.png"
      width=100%
	  figcaption="Participants Page"
	  alt="Participants Page"
>}}

The initial page lets you select the network participant you want to act as. For each participant, the following details are displayed:

* Title
* X.500 name
* Permissions

Choose from one of the available roles by clicking the relevant **Select** button:

* Central bank
* Commercial bank
* Commercial bank 2
* Custodian

The Digital Currencies GUI is displayed:

{{< 
      figure
	  src="images/dc-gui.png"
      width=100%
	  figcaption="Digital Currencies GUI"
	  alt="Digital Currencies GUI"
>}}

Note that you can select the network participant you are at any time by using the **Settings** button; see [Viewing the GUI Settings]({{< relref "viewing-the-gui-settings.md" >}}).
The GUI has the following elements:

* A left-hand sidebar contains the following options (depending on which participant you selected, not all will be shown):
  * **Define Token:** See [Creating Token Definitions]({{< relref "defining/creating-token-definitions.md" >}})
  * **Token Definitions:** See [Viewing Token Definitions]({{< relref "defining/viewing-token-definitions.md" >}})
  * **Token Manager**: See:
    * [Minting Tokens]({{< relref "minting/_index.md" >}})
    * [Burning Tokens]({{< relref "burning/_index.md" >}})
    * [Viewing Vault Balances]({{< relref "viewing-vault-balances.md" >}})
  * **Issuances:** See [Working with Token Issuance]({{< relref "issuing/_index.md"  >}})
  * **Transfers:** See [Working with Token Transfers]({{< relref "transferring/_index.md" >}})
  * **Redemptions:** See [Working with Token Redemption]({{< relref "redeeming/_index.md" >}})
    
* The **Settings** button (![](images/setting-buttons.png)): See [Viewing the GUI Settings]({{< relref "viewing-the-gui-settings.md" >}}) 
* The flow tracker button (![](images/flow-drawer-button.png)): When performing flows such as creating token definitions and minting tokens, click this button to display a pop-out flow tracker which displays the current status of flows. By default, the five most recent flows are displayed.
  

