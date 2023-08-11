---
date: '2023-07-12'
lastmod: '2023-07-12'
section_menu: tools
menu:
  tools:
    name: "Creating Push Transfer Requests"
    weight: 1000
    parent: digital-currencies-tokens-transferring
    identifier: digital-currencies-creating-push-transfer-requests
    description: "Digital Currencies documentation describing how to create push transfer requests via the GUI"
title: "Creating Push Transfer Requests"
---

This topic describes how to create a push transfer request. A push transfer occurs when the initiator of the transfer, which possesses tokens, wants to transfer those tokens to a recipient. Once the push transfer request is created, it must then be [approved by the recipient]({{< relref "approving-or-rejecting-transfer-requests.md" >}}).

You could instead [perform a push transfer]({{< relref "performing-push-transfers.md" >}}). The difference between that and creating a push transfer request is that, when preforming a push transfer, no approval by the recipient is required and the tokens are immediately transferred.


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

   * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
   * **Request**: Allows you to create a push or pull transfer request; for more on creating pull requests, see [Creating Pull Transfer Requests]({{< relref "creating-pull-transfer-requests.md" >}}).
   * **Transfer:** Allows you to perform a push transfer which does not require approval from the recipient; see [Performing Push Transfers]({{< relref "performing-push-transfers.md" >}}).
   * **Transfer Requests:** Lists all transfer requests associated with the current participant.

2. Click the **Request** tab.

   The **Request Transfer** panel is displayed:

   {{< 
      figure
	  src="images/request-transfer-panel.png"
      width=50%
	  figcaption="Request Transfer Panel"
	  alt="Request Transfer Panel"
   >}} 
  
2. In the **Request Transfer** panel, specify the following values:

   * **Request Transfer Type:** Select **Push**.
   * **Receiving Party:** Select the participant to receive the tokens.
   * **Token Definition**: Select the token definition for the token you want to transfer.
   * **Amount**: Enter the number of tokens you want to request.
   
   In this example, Commercial Bank 1 will create a push request for 100,000 tokens to Commercial Bank 2.

   
3. Click **Request**. 

   The message *Successfully submitted a transfer request* is displayed:

   {{< 
      figure
	  src="images/successfully-submitted-transfer-request-message.png"
      width=40%
	  alt="'Successfully submitted a transfer request' Message"
	  figcaption="'Successfully submitted a transfer request' Message"
   >}}

   The Request Transfer flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/request-transfer-flow.png"
      width=50%
	  figcaption="Request Transfer - Flow Running"
	  alt="Request Transfer - Flow Running"
   >}}  

   Once the transfer flow finishes, the message *Your transfer request has been successfully created* is displayed:

   {{< 
      figure
	  src="images/your-transfer-request-has-been-successfully-created-message.png"
      width=50%
	  alt="'Your transfer request has been successfully created' Message"
	  figcaption="'Your transfer request has been successfully created' Message"
   >}}

   The **Transfer Requests** pane is updated to display the new transfer request, with a status of Pending:
   
   {{< 
      figure
	  src="images/transfer-requests-panel-push-pending.png"
      width=80%
	  alt="Transfer Requests Pane"
	  figcaption="Transfer Requests Pane"
   >}}
   
The recipient must now approve the transfer request; see [Approving Transfer Requests]({{< relref "approving-or-rejecting-transfer-requests" >}}).