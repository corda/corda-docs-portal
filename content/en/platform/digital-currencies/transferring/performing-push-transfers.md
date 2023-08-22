---
date: '2023-07-12'
lastmod: '2023-07-12'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Performing Push Transfers"
    weight: 2500
    parent: digital-currencies-tokens-transferring
    identifier: digital-currencies-push-transfer
    description: "Digital Currencies documentation describing how to perform a push transfer of tokens via the GUI"
title: "Performing Push Transfers"
---

This topic describes how to perform a push transfer. A push transfer occurs when the initiator of the transfer, which possesses tokens, wants to transfer those tokens to a recipient. Once the push transfer is performed, the tokens are immediately transferred to the recipient. 

You could instead [create a push transfer request]({{< relref "creating-push-transfer-requests.md" >}}). The difference between that and performing a push transfer is that, when creating a push transfer request, the recipient must approve the request before the tokens are transferred.

As a commercial bank:

1. In the left-hand menu, click on **Transfers**.

   The following page is displayed:
   
   {{< 
      figure
	  src="images/transfers-page-centralbank1.png"
      width=100%
	  figcaption="Transfers Page"
	  alt="Transfers Page"
   >}}

   The page shows the following panels related to transfers:

   * **Vault Balances**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
   * **Request**: Allows you to create a pull or push transfer request; see:
      * [Creating Pull Transfer Requests]({{< relref "creating-pull-transfer-requests.md" >}})
      * [Creating Push Transfer Requests]({{< relref "creating-push-transfer-requests.md" >}})
   * **Transfer:** Allows you to perform a push transfer which does not require approval from the recipient. 
   * **Transfer Requests:** Lists all transfer requests associated with the current participant.
  
2. Click the **Transfer** tab.

   The **Push Transfer** panel is displayed:

   {{< 
      figure
	  src="images/push-transfer-panel.png"
      width=50%
	  figcaption="Push Transfer Panel"
	  alt="Push Transfer Panel"
   >}} 
  
3. In the **Push Transfer** panel, specify the following values:

   * **Token Definition:** Select the token definition for the token you want to transfer.
   * **Receiving Party:** Select the participant (such as another commercial bank) who will receive the tokens. 
   * **Amount:** Enter the number of tokens to send.
      
4. Click **Send**. 

   The message **Successfully submitted a transfer of tokens** is displayed:

   {{< 
      figure
	  src="images/successfully-submitted-transfer-tokens-message.png"
      width=40%
	  alt="'Successfully submitted a transfer of tokens' Message"
	  figcaption="'Successfully submitted a transfer of tokens' Message"
   >}}

   The **Push Transfer** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/push-transfer-flow.png"
      width=50%
	  figcaption="Push Transfer - Flow Running"
	  alt="Push Transfer - Flow Running"
   >}}  

   Once the **Push Transfer** flow finishes, the message **Tokens have been transferred successfully** is displayed:

   {{< 
      figure
	  src="images/tokens-have-been-transferred-successfully-message.png"
      width=50%
	  alt="'Tokens have been transferred successfully' Message"
	  figcaption="'Tokens have been transferred successfully' Message"
   >}}

   The vault balances of the sender and receiver are immediately updated to show their new balances.