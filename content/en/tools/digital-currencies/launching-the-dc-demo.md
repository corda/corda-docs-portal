---
date: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: Launching the Digital Currencies Demo
    weight: 150
    parent: digital-currencies
    identifier: digital-currencies-launching-demo
    description: "Digital Currencies documentation describing how to launch the Digital Currencies demo"
title: Launching the the Digital Currencies Demo
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

The initial page let you select the network participant you want to act as. For each participant, the following details are displayed:

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
  * **Define Token**: See [Creating Token Definitions]({{< relref "creating-token-definitions.md" >}})
  * **Token Definitions**: See [Viewing Token Definitions]({{< relref "viewing-token-definitions.md" >}})
  * **Token Manager**: See:
    * [Minting Tokens]({{< relref "minting-tokens.md" >}})
    * [Burning Tokens]({{< relref "burning-tokens.md" >}})
    * [Viewing Vault Balances]({{< relref "viewing-vault-balances.md" >}})
  * **Issuances**: See [Creating Issuance Requests]({{< relref "creating-issuance-requests.md"  >}})
  * **Redemptions**: See:
    
* The **Settings** button (![](images/setting-buttons.png)): See [Viewing the GUI Settings]({{< relref "viewing-the-gui-settings.md" >}}). 
* The flow tracker button (![](images/flow-drawer-button.png)): When performing flows such as creating token definitions and minting tokens, click this button to display a pop-out flow tracker which displays the current status of flows. By default, the five most recent flows are displayed.
  

