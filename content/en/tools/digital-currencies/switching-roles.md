---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Switching Roles"
    weight: 400
    parent: digital-currencies
    identifier: digital-currencies-switching-roles
    description: "Digital Currencies documentation describing how to switches roles in the GUI"
title: "Switching Roles"
---

This topic describes how to change the currently active participant in the GUI.

The list of available participants is initially defined in the file appConfig.json as described in [Installing the Digital Currencies Demo - Specify Virtual Nodes for Digital Currencies UI]({{< relref "installing-the-dc-demo#specify-virtual-nodes-for-digital-currencies-ui" >}}).

1. Click the **Settings** button (![](images/setting-buttons.png)).

   The following page is displayed:
  
   {{< 
      figure
	  src="images/settings-page.png"
      width=80%
	  figcaption="Settings Page"
	  alt="Settings Page"
   >}}
     
   The **Select App Config** field of the **VNode Details** panel displays the currently-active role; in this case, *Central Bank*.    

2. Click the **Select App Config** field and select the required participant from the list displayed:

   {{< 
      figure
	  src="images/select-app-config-values.png"
      width=40%
	  figcaption="Select App Config field"
	  alt="Select App Config field"
   >}}


   The left-hand menu and the GUI color scheme is updated to match the role selected.