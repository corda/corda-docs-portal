---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Creating Transfer Requests"
    weight: 1300
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-creating-transfer-requests
    description: "Digital Currencies documentation describing how to transfer tokens via the GUI"
title: "Creating Transfer Requests"
---

A transfer is the movement of tokens (value) between two or more entities (for example, wholesale banks, bank branches, retailers, retailer branches or franchises) on a Corda network to exchange goods and services. The transfer process can work both ways: both *requests to send* and *requests to receive* can be made.

* **Request to send:** Transacting Entity A requests to ‘pay’ Transacting Entity B. Transacting Entity B confirms amount and Transacting Entity A completes the transfer by signing the transaction which turn alters the ownership of the tokens to Transacting Entity B. 
* **Request to receive:** Transacting Entity A requests Transacting Entity B to ‘pay’ a disclosed amount. Transacting Entity B, confirms and transfers token by signing the transaction which in turn alters the ownership of the tokens to Transacting Entity A.  

1. In the left-hand menu, click on **Transfers**.

   The following page is displayed:
   
   {{< 
      figure
	  src="images/commercial-bank-transfers-page.png"
      width=100%
	  figcaption="Transfers Page"
	  alt="Transfers Page"
>}}

  The page shows the following panels related to transfers:

  * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0-beta/developing/ledger/vault.md" >}}).
  * **Request Transfer**: Allows you to perform a transfer request.
  * **Transfer Requests:** Lists any existing transfer requests and their status; see [Viewing Transfer Requests](viewing-transfer-requests.md).

2. In the **Request Transfer** panel, specify the following values:

   * **Token Definition**: Select the [token definition](tokens-overview.md#token-definitions) for the token you want to transfer.
   * **Amount**: Enter the number of tokens you want to request.
   
3. Click **Request**. 

   The message *Successfully submitted a transfer request* is displayed:

   {{< 
      figure
	  src="images/successfully-submitted-transfer-request-message.png"
      width=40%
	  alt="'Successfully submitted a transfer request' Message"
	  figcaption="'Successfully submitted a transfer request' Message"
   >}}

   The transfer flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/running-flows-request-tokens.png"
      width=50%
	  figcaption="Transferring Tokens - Flow Running"
	  alt="Transferring Tokens - Flow Running"
   >}}  

   Once the transfer flow finishes, the message *Your transfer request has been successfully created* is displayed:

   {{< 
      figure
	  src="images/transfer-request-successfully-created-message.png"
      width=50%
	  alt="'Your transfer request has been successfully created' Message"
	  figcaption="'Your transfer request has been successfully created' Message"
   >}}

   The **Transfer Requests** pane is updated to display the pending transfer request:
   
   {{< 
      figure
	  src="images/pending-transfer-request.png"
      width=50%
	  alt="Transfer Requests Pane"
	  figcaption="Transfer Requests Pane"
   >}}
   


   
   
   
   
   