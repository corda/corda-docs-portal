---
date: '2023-07-12'
lastmod: '2023-07-12'
section_menu: tools
menu:
  tools:
    name: "Approving or Rejecting Transfer Requests"
    weight: 2000
    parent: digital-currencies-tokens-transferring
    identifier: digital-currencies-approving-rejecting-transfer-requests
    description: "Digital Currencies documentation describing how to approve or reject transfer requests via the GUI"
title: "Approving or Rejecting Transfer Requests"
---

To approve or reject a transfer:

1. In the left-hand menu, click on **Transfers**.

   The **Transfers** page is displayed, showing the following panels related to transfers:

   * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
   * **Request Transfer**: Allows you to create a transfer request; see [Creating Transfer Requests](creating-transfer-requests.md)
   * **Transfer Requests:** Lists any existing transfer requests and their status.
  
   {{< 
      figure
	  src="images/transfer-requests-panel-pull-pending.png"
      width=80%
	  figcaption="Transfer Requests Panel"
	  alt="Transfer Requests Panel"
   >}}
   
   For each transfer request, the following information is displayed:
   
   * **Status:** The status of the request.
   * **Token name:** The name of the token definition; normally the full name of the currency; for example, UAE Dirham.
   * **Token symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *AED*.
   * **Amount:** The number of tokens requested.
   * **Approver:** The participant who either (1) has to approve the receipt of tokens (if the other party made a push request) or (2) has to approve the sending of tokens (if the other party made a pull request).
   * **Requester:** The participant who create the transfer request.
   * **Last Updated:** The date and time at which the request was last updated.
   
2. Click on the relevant transfer request.

   The **Transfer Request** dialog box is displayed:
  
   {{< 
      figure
	  src="images/transfer-request-dialog-pending.png"
      width=40%
	  figcaption="Transfer Request Pane"
	  alt="Transfer Request Pane"
   >}}

3. Click **Approve**. 

   (Alternately, you can click **Reject** if you do not want the transfer to proceed.)
   
   The message *Your token transfer approval update has been successfully submitted* is displayed:

   {{< 
      figure
	  src="images/token-transfer-approval-update-successful-message.png"
      width=40%
	  alt="'Your token transfer approval update has been successfully submitted' Message"
	  figcaption="'Your token transfer approval update has been successfully submitted' Message"
   >}}

   The Update Transfer Request flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/update-transfer-request-flow.png"
      width=50%
	  figcaption="Update Transfer Request - Flow Running"
	  alt="Update Transfer Request - Flow Running"
   >}}  

   Once the Update Transfer Request flow finishes, the message *Your request update has been successful* is displayed:

   {{< 
      figure
	  src="images/your-request-update-has-been-successful-message.png"
      width=50%
	  alt="'Your request update has been successful' Message"
	  figcaption="'Your request update has been successful' Message"
   >}}
   
   The **Transfer Requests** pane is updated to display the transfer request with a status of Approved:
   
   {{< 
      figure
	  src="images/transfer-requests-panel-push-approved.png"
      width=80%
	  alt="Transfer Requests Pane"
	  figcaption="Transfer Requests Pane"
   >}}
   
   <TBD>