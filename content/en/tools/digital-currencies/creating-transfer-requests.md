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
	  src="images/transfers-page.png"
      width=100%
	  figcaption="Transfers Page"
	  alt="Transfers Page"
>}}

  The page shows the following panels related to transfers:

  * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0-beta/developing/ledger/vault.md" >}}).
  * **Request Transfer**: Allows you to perform a transfer request.
  * **Transfer Requests:** Lists any existing transfer requests and their status; see [Viewing Transfer Requests](viewing-transfer-requests.md).

2. In the **Transfer Request** panel, specify the following values:

   * **Token Definition**: Select the [token definition](tokens-overview.md#token-definitions) for the token you want to transfer.
   * ** **Amount**: Enter the number of tokens you want to request.
   
3. Click **Request**. 
