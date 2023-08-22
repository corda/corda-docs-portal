---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Decommissioning Token Definitions"
    weight: 800
    parent: digital-currencies-token-definitions
    identifier: digital-currencies-decommissioning-token-definitions
    description: "Digital Currencies documentation describing how to decommission token definitions via the GUI"
title: "Decommissioning Token Definitions"
---

This topic describes how to decommission a {{< tooltipdc>}}token definition{{< /tooltipdc >}}. Only the definer of a token can decommission it.

As a central bank:

1. In the Digital Currencies GUI, [view existing token definitions]({{< relref "viewing-token-definitions.md" >}}).

   The **Token Definitions** page is displayed:

   {{< 
      figure
	  src="images/token-definitions-page.png"
      width=100%
	  alt="Token Definitions Page"
	  figcaption="Token Definitions Page"
   >}}
  
2. In the **Active Token Definitions** pane, click **Decommission** for the relevant token definition:

   {{< 
      figure
	  src="images/active-token-definitions-decommission-button.png"
      width=60%
	  alt="Active Token Definitions - Decommission Button"
	  figcaption="Active Token Definitions - Decommission Button"
   >}}
   
   If the **Decommission** button is not displayed, you do not have permission to decommission the token.
   
   The following dialog box is displayed:
   
   {{< 
      figure
	  src="images/decommission-token-confirm.png"
      width=60%
	  alt="Active Token Definitions - Confirm Decommission"
	  figcaption="Active Token Definitions - Confirm Decommission"
   >}}
   
3. Click **Confirm**.
   
   The message *Token definition decommission submitted* is displayed:

   {{< 
      figure
	  src="images/token-definition-decommission-submitted.png"
      width=50%
	  alt="'Token definition decommission submitted' Message"
	  figcaption="Token definition decommission submitted' Message"
   >}}

   The **Decommission token definition** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/running-flows-decommission-token-definition.png"
      width=50%
	  figcaption="Decommissioning Token Definitions - Flow Running"
	  alt="Decommissioning Token Definitions - Flow Running"
   >}}  

   Once the **Decommission token definition** flow finishes, the message *Token definition has been successfully decommissioned* is displayed:

   
   {{< 
      figure
	  src="images/token-definition-successfully-decommissioned-message.png"
      width=50%
	  alt="'Token definition has been successfully decommissioned' Message"
	  figcaption="'Token definition has been successfully decommissioned' Message"
   >}}
   
   The decommissioned token definition is now displayed in the **Decommissioned Tokens Definitions** panel:
   
   {{< 
      figure
	  src="images/decommissioned-token-definitions.png"
      width=60%
	  alt="'Decommissioned Tokens Definitions' Panel"
	  figcaption="'Decommissioned Tokens Definitions' Panel"
   >}}
   
   
   
   
   
   
   