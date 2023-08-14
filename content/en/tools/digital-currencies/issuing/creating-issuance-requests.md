---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Creating Issuance Requests"
    weight: 200
    parent: digital-currencies-token-issuance
    identifier: digital-currencies-creating-issuance-requests
    description: "Digital Currencies documentation describing how to request an issuance of tokens via the GUI"
title: "Creating Issuance Requests"
---

Once [tokens have been minted]({{< relref "../minting/_index.md" >}}), tokens of that type can be issued. Issuing tokens involves transferring them to the relevant entities.  

The general process of issuance, and the on-ledger actions involved will be very similar, if not identical, for both CBDCs and for stablecoins. However, the permissions of these on-ledger actions may be divided differently based on implementation. For example, in {{< tooltip >}}CBDC{{< definitiondc term="CBDC" >}}{{< /tooltip >}} issuance, the custodian and the token issuing entity will both be a central bank, while these roles may be divided for a stablecoin.

The following assumes you are logged in as an entity capable of creating an issuance request, such as a commercial bank.

Create a redemption request:

1. Click **Redemptions** in the left-hand sidebar.

   The **Redemptions** page is displayed:

   {{<
      figure
	  src="images/redemptions-page.png"
      width=100%
	  figcaption="Redemptions Page"
	  alt="Redemptions Page"
   >}}
   
  The page shows the following panels related to redemptions:

  * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
  * **Request Issuance**: Allows you to perform an issuance request.
  * **Issuance Requests:** Lists any existing issuance requests and their status; see [Viewing Issuance Requests]({{< relref "viewing-issuance-requests.md" >}}).

2. In the **Request Issuance** panel, specify the following values:

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
	  src="images/successfully-submitted-issuance-request-message.png"
      width=50%
	  figcaption="'Successfully submitted an issuance request' message"
	  alt="'Successfully submitted an issuance request' message"
   >}}
   
   The Request Tokens flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:

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








