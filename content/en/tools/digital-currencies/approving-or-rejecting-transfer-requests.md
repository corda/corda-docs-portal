---
date: '2023-04-25'
lastmod: '2023-04-25'
section_menu: tools
menu:
  tools:
    name: "Approving or Rejecting Transfer Requests"
    weight: 1350
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-approving-rejecting-transfer-requests
    description: "Digital Currencies documentation describing how to approve or reject transfer requests via the GUI"
title: "Approving or Rejecting Transfer Requests"
---

To approve or reject a transfer:

1. In the left-hand menu, click on **Transfers**.

   The following page is displayed:
   
   {{< 
      figure
	  src="images/transfers-page.png"
      width=100%
	  figcaption="Transfers Page"
	  alt="Transfers Page"
   >}}

   The page shows the following panels related to transfers:

   * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0-beta/developing/ledger/vault.md" >}}).
   * **Request Transfer**: Allows you to create a transfer request; see [Creating Transfer Requests](creating-transfer-requests.md)
   * **Transfer Requests:** Lists any existing transfer requests and their status.
  
   {{< 
      figure
	  src="images/transfer-requests-panel.png"
      width=100%
	  figcaption="Transfer Requests Panel"
	  alt="Transfer Requests Panel"
   >}}
   
   For each transfer request, the following information is displayed:
   
   * **Status:** The status of the request
   * **Token name:** The name of the token definition; normally the full name of the currency; for example, Canadian Dollar
   * **Token symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *CAD*
   * **Amount:** The number of tokens requested
   * **Approver:** The Transacting Entity who either (1) has to approve the receipt of tokens (if the other party made a Request to Send) or (2) has to approve the sending of tokens (if the other party made a Request to Receive)
   * **Last Updated:** The date and time at which the request was last updated