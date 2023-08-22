---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Creating Issuance Requests"
    weight: 200
    parent: digital-currencies-token-issuance
    identifier: digital-currencies-creating-issuance-requests
    description: "Digital Currencies documentation describing how to request an issuance of tokens via the GUI"
title: "Creating Issuance Requests"
---

The following topic describes how to create an {{< tooltipdc >}}issuance{{< /tooltipdc >}} request.

The following assumes you are logged in as an entity capable of creating an issuance request, such as a commercial bank.

Create a redemption request:

1. Click **Issuances** in the left-hand sidebar.

   The **Issuances** page is displayed:

   {{<
      figure
	  src="images/issuances-page-commercial-bank.png"
      width=100%
	  figcaption="Issuances Page (Commercial Bank)"
	  alt="Issuances Page"
   >}}
   
  The page shows the following panels related to redemptions:

  * **Vault Balances**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
  * **Request Issuance**: Allows you to perform an issuance request.
  * **Issuance Requests:** Lists any existing issuance requests and their status; see [Viewing Issuance Requests]({{< relref "viewing-issuance-requests.md" >}}).

2. In the **Request Issuance** panel, specify the following values:

   {{< 
      figure
	  src="images/request-issuance-panel.png"
      width=50%
	  figcaption="Request Issuance Panel"
	  alt="Request Issuance Panel"
   >}}

   * **Token Definition**: Select the token definition for the token you want to request.
   * **Amount**: Type the number of tokens you want to request.
   
3. Click **Request**. 

   The following message is displayed:
   
   {{< 
      figure
	  src="images/successfully-submitted-issuance-request-message.png"
      width=50%
	  figcaption="'Successfully submitted an issuance request' message"
	  alt="'Successfully submitted an issuance request' message"
   >}}
   
   The **Request Tokens** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:

   {{< 
      figure
	  src="images/request-tokens-flow.png"
      width=50%
	  figcaption="'Successfully submitted an issuance request' message"
	  alt="'Successfully submitted an issuance request' message"
   >}}
   
   Once the **Request Tokens** flow finishes, the message **Your issuance request has been successfully created** is displayed:

   {{< 
      figure
	  src="images/issuance-request-successfully-created-message.png"
      width=50%
	  figcaption="'Your issuance request has been successfully created' message"
	  alt="'Your issuance request has been successfully created' message"
   >}}

The new request is now listed in the **Issuance Requests** panel:

   {{< 
      figure
	  src="images/issuance-requests-panel-issuer.png"
      width=90%
	  figcaption="Issuance Requests Panel"
	  alt="Issuance Requests Panel"
   >}}

The issuer and the custodian of the digital currency both now need to [approve this request]({{< relref "approving-or-rejecting-issuance-requests.md" >}}).








