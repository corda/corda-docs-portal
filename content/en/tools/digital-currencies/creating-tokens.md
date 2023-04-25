---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Creating Tokens"
    weight: 900
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-creating-token-types
    description: "Digital Currencies documentation describing how to create tokens via the GUI"
title: "Creating Tokens"
---

Once a token definition has been created, new tokens of that type can be issued. Such tokens can then be used as for currency or utility purposes and allows the issuing party to maintain monetary policy and provide easily accessible digital currency tokens to specific entities.

1. Click **Token Manager** in the left-hand sidebar.

   The **Token Manager** page is displayed:
   
   {{< 
      figure
	  src="images/token-manager-page.png"
      width=100%
	  figcaption="Token Manager Page"
	  alt="Token Manager Page"
   >}}
   
   The page contains the following panes:
   
   * **Vault Balances:** Displays the number of tokens available for each token definition.
   * **Create Tokens:** Enables you to create tokens of a certain token definition.
   * **Burn Tokens:** Enables you to burn tokens; see [Burning Tokens]({{< relref "burning-tokens.md" >}})).
   
4. In the **Create Tokens** pane, specify the following values:

   * **Token Definition:** Select the relevant token definition (previously created as described in [Creating Token Definitions]({{< relref "creating-token-definitions.md" >}})).
   * **Amount:** Enter the number of token you want; for example *100*.
   
5. Click **Create**.
  
   The *Successfully submitted the creation of new tokens* message is displayed:
   
   {{< figure src="images/successfully-submitted-creation-tokens-message.png" width=40% figcaption="'Successfully submitted creation of new tokens' Message" alt="'Successfully submitted creation of new tokens' Message" >}}

   The token creation flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/running-flows-create-tokens.png"
      width=50%
	  figcaption="Creating Tokens - Flow Running"
	  alt="Creating Tokens - Flow Running"
   >}}  
   
   Once the token definition flow completes, the message *A new token definition has been successfully created* is displayed:

   {{< 
      figure
	  src="images/a-new-token-definition-created-message.png"
      width=50%
	  figcaption="'A new token definition has been successfully created' Message"
	  alt="'A new token definition has been successfully created' Message"
   >}}  
   
   The vault balance for the token definition will now show the new amount:
   
   {{< 
      figure
	  src="images/updated-vault-balance.png"
      width=80%
	  figcaption="Updated Vault Balance"
	  alt="Updated Vault Balance"
   >}}
   
  