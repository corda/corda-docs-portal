---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Burning Tokens"
    weight: 1700
    identifier: digital-currencies-burning-tokens
    description: "Digital Currencies documentation describing how to burn tokens via the GUI"
title: "Burning Tokens"
---

The introduction of {{< tooltipdc >}}CBDC{{< /tooltipdc >}} will inject a new source of liquidity into the economy. However, many central banks peg their currency to the US dollar and as such hold dollar reserves to stabilize their currency. As a result, central banks will have a minimum threshold of foreign reserves - this can differ country to country. 

As a result, central banks, which have [defined]({{< relref "../defining/_index.md" >}}) and [issued]({{< relref "../issuing/_index.md" >}}) tokens, need the ability to burn and thereby redeem them for US dollar to maintain a stable domestic currency value and a certain amount of currency in circulation, or {{< tooltipdc >}}CIC{{< /tooltipdc >}}.

To burn tokens:

1. Select **Token Manager**.

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
   * **Mint Tokens:** Enables you to mint tokens; see [Minting Tokens]({{<relref "../minting/_index.md" >}}).
   * **Burn Tokens:** Enables you to burn tokens.
      
2. In the **Burn Tokens** pane, specify the following values:

   * **Token Definition:** Select the relevant token definition (previously created as described in [Creating Token Definitions]({{< relref "../defining/creating-token-definitions.md" >}})).
   * **Amount:** Type the number of tokens you want to burn; for example *100*.

3. Click **Burn**.
  
   The *Successfully submitted tokens to burn* message is displayed:
   
   {{< figure src="images/successfully-submitted-tokens-to-burn-message.png" width=40% figcaption="'Successfully submitted tokens to burn' Message" alt="'Successfully submitted tokens to burn' Message" >}}

   The **Burn Tokens** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/running-flows-burn-tokens.png"
      width=50%
	  figcaption="Burn Tokens - Flow Running"
	  alt="Burn Tokens - Flow Running"
   >}}  
   
   Once the **Burn Tokens** flow completes, the message *Tokens have been successfully burned, check your vault balance for new balance* is displayed:

   {{< 
      figure
	  src="images/tokens-have-been-successfully-burned-message.png"
      width=50%
	  figcaption="'Tokens have been successfully burned...' Message"
	  alt="'Tokens have been successfully burned...' Message"
   >}}  
   
   The vault balance for the token definition will now show the updated amount in the central bank's vault, minus the burned tokens:
   
   {{< 
      figure
	  src="images/updated-vault-balance.png"
      width=30%
	  figcaption="Updated Vault Balance"
	  alt="Updated Vault Balance"
   >}}
