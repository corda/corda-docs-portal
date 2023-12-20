---
date: '2023-03-21'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Minting Tokens"
    weight: 600
    identifier: digital-currencies-minting-tokens
    description: "Digital Currencies documentation describing how to mint tokens via the GUI"
title: "Minting Tokens"
---

Once a [token definition has been created]({{< relref "../defining/creating-token-definitions.md " >}}), new tokens of that type can be minted. Such tokens can then be used as for currency or utility purposes and allow the issuing party to maintain monetary policy and provide easily accessible digital currency tokens to specific entities.

As a central bank:

1. Click **Token Manager** in the left-hand sidebar.

   The **Token Manager** page is displayed:
   
   {{< 
      figure
	  src="images/token-manager-page.png"
      width=80%
	  figcaption="Token Manager Page"
	  alt="Token Manager Page"
   >}}
   
   The page contains the following panes:
   
   * **Vault Balances:** Displays the number of tokens available for each token definition for the current participant.
   * **Mint Tokens:** Enables you to mint tokens of a certain token definition.
   * **Burn Tokens:** Enables you to burn tokens; see [Burning Tokens]({{< relref "../burning/_index.md" >}}).
   
2. In the **Mint Tokens** pane, specify the following values:

   * **Token Definition:** Select the relevant token definition (previously created as described in [Creating Token Definitions]({{< relref "../defining/creating-token-definitions.md" >}})).
   * **Amount:** Type the number of tokens you want; for example *1000000*.
   
3. Click **Create**.
  
   The *Successfully submitted the minting of new tokens* message is displayed:
   
   {{< figure src="images/successfully-submitted-minting-new-tokens.png" width=40% figcaption="'Successfully submitted the minting of new tokens' Message" alt="'Successfully submitted the minting of new tokens' Message" >}}

   The **Mint Tokens** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/running-flows-mint-tokens.png"
      width=50%
	  figcaption="Mint Tokens - Flow Running"
	  alt="Mint Tokens - Flow Running"
   >}}  
   
   Once **Mint Tokens** flow completes, the message *Tokens have been successfully minted, check your vault balance for new balance* is displayed:

   {{< 
      figure
	  src="images/tokens-successfully-minted-message.png"
      width=50%
	  figcaption="'Tokens have been successfully minted...' Message"
	  alt="'Tokens have been successfully minted...' Message"
   >}}  
   
   The vault balance for the relevant token definition will now show the new amount:
   
   {{< 
      figure
	  src="images/updated-vault-balance.png"
      width=30%
	  figcaption="Updated Vault Balance"
	  alt="Updated Vault Balance"
   >}}
   
Once tokens have been minted, they can be [issued]({{< relref "../issuing/_index.md" >}}).
  