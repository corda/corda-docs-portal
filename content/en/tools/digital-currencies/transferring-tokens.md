---
date: '2023-06-23'
lastmod: '2023-06-23'
section_menu: tools
menu:
  tools:
    name: "Transferring Tokens"
    weight: 1200
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-transferring-tokens
    description: "Digital Currencies documentation describing how to transfer tokens via the GUI"
title: "Transferring Tokens"
---

Once a participant has been [issued tokens]({{< relref "issuing-tokens.md" >}}) after [requesting them]({{< relref "creating-issuance-requests.md" >}}), they be involved in transfers. The following transfer method are available:

* The holder of tokens can send transfers to another participant as a 'push transfer'. looks like can send it to any participant - central bank, 
* Create a push transfer requesting
* Create a pull transfer request







, new tokens of that type can be issued. Such tokens can then be used as for currency or utility purposes and allows the issuing party to maintain monetary policy and provide easily accessible digital currency tokens to specific entities.

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
   
   * **Vault Balances:** Displays the number of tokens available for each token definition for the current participant.
   * **Mint Tokens:** Enables you to mint tokens of a certain token definition.
   * **Burn Tokens:** Enables you to burn tokens; see [Burning Tokens]({{< relref "burning-tokens.md" >}})).
   
4. In the **Mint Tokens** pane, specify the following values:

   * **Token Definition:** Select the relevant token definition (previously created as described in [Creating Token Definitions]({{< relref "creating-token-definitions.md" >}})).
   * **Amount:** Enter the number of token you want; for example *100*.
   
5. Click **Create**.
  
   The *Successfully submitted the minting of new tokens* message is displayed:
   
   {{< figure src="images/successfully-submitted-minting-new-tokens.png" width=40% figcaption="'Successfully submitted the minting of new tokens' Message" alt="'Successfully submitted the minting of new tokens' Message" >}}

   The token creation flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/running-flows-mint-tokens.png"
      width=50%
	  figcaption="Mint Tokens - Flow Running"
	  alt="Mint Tokens - Flow Running"
   >}}  
   
   Once the token definition flow completes, the message *Tokens have been successfully created, check your vault balance for new balance* is displayed:

   {{< 
      figure
	  src="images/tokens-successfully-created-message.png"
      width=50%
	  figcaption="'Tokens have been successfully created...' Message"
	  alt="'Tokens have been successfully created...' Message"
   >}}  
   
   The vault balance for the token definition will now show the new amount:
   
   {{< 
      figure
	  src="images/updated-vault-balance.png"
      width=40%
	  figcaption="Updated Vault Balance"
	  alt="Updated Vault Balance"
   >}}
   
  