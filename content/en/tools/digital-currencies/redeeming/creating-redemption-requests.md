---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Creating Redemption Requests"
    weight: 200
    parent: digital-currencies-token-redemption
    identifier: digital-currencies-creating-redemption-requests
    description: "Digital Currencies documentation describing how to request a redemption of tokens via the GUI"
title: "Creating Redemption Requests"
---

This topic describes how to create a {{< tooltip >}}redemption{{< definitiondc term="redemption" >}}{{< /tooltip >}} request.

The following assumes you are logged in as an entity capable of creating a redemption request, such as a commercial bank, and that you possess tokens in your vault to redeem.

1. In the left-hand menu, click on **Redemptions**.

   The following page is displayed:
   
   {{< 
      figure
	  src="images/redemptions-page-commercial-bank.png"
      width=100%
	  figcaption="Redemptions Page"
	  alt="Redemptions Page"
   >}}

  The page shows the following panels related to redemptions:

  * **Vault Balances:** A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
  * **Request Redemption:** Allows you to perform a redemption request.
  * **Redemption Requests:** Lists any existing redemption requests and their status; see [Viewing Redemption Requests]({{< relref "viewing-redemption-requests.md" >}}).

2. In the **Request Redemption** panel, specify the following values:

   {{< 
      figure
	  src="images/request-redemption-panel.png"
      width=50%
	  figcaption="Request Redemption Panel"
	  alt="Request Redemption Panel"
   >}}


   * **Token Definition**: Select the token definition for the token you want to redeem.
   * **Amount**: Type the number of tokens you want to redeem.
   
3. Click **Request**. 

   The following message is displayed:
   
   {{< 
      figure
	  src="images/successfully-submitted-redemption-request-message.png"
      width=50%
	  figcaption="'Successfully submitted a redemption request' message"
	  alt="'Successfully submitted a redemption request' message"
   >}}
   
   The **Request Redemption** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:

   {{< 
      figure
	  src="images/request-redemption-flow.png"
      width=50%
	  figcaption="Request Redemption - Flow Running"
	  alt="Request Redemption - Flow Running"
   >}}
   
   Once the **Request Redemption** flow finishes, the message **Your redemption request has been successfully created** is displayed:

   {{< 
      figure
	  src="images/your-redemption-request-successfully-created-message.png"
      width=50%
	  figcaption="'Your redemption request has been successfully created' message"
	  alt="'Your redemption request has been successfully created' message"
   >}}

The new request is now listed in the **Redemption Requests** panel:

   {{< 
      figure
	  src="images/redemptions-request-panel-pending.png"
      width=90%
	  figcaption="Redemption Requests Panel"
	  alt="Redemption Requests Panel"
   >}}

The issuer and the custodian of the digital currency both now need to [approve this request]({{< relref "approving-or-rejecting-redemption-requests.md" >}}).