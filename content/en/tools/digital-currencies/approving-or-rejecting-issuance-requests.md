---
date: '2023-04-25'
lastmod: '2023-04-25'
section_menu: tools
menu:
  tools:
    name: "Approving or Rejecting Issuance Requests (as Issuer)"
    weight: 1370
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-approving-rejecting-issuance-requests-issuer
    description: "Digital Currencies documentation describing how to approve or reject issuance requests via the GUI"
title: "Approving or Rejecting Issuance Requests"
---

An inssuance request must be approved by both:

* The issuer of the digital currency
* The custodian of the digital currency

To approve or reject an issuance request (as either an issuer or a custodian):

1. In the left-hand menu, click on **Issuances**.

   The following page is displayed:
   
   {{< 
      figure
	  src="images/issuances-page-central-bank.png"
      width=100%
	  figcaption="Issuances Page"
	  alt="Issuances Page"
   >}}

   The page shows the following panels related to transfers:

   * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0-beta/developing/ledger/vault.md" >}}).
   * **Issuance Requests:** Lists any existing issuance requests and their status.
  
   {{< 
      figure
	  src="images/issuance-requests-panel.png"
      width=100%
	  figcaption="Issuance Requests Panel"
	  alt="Issuance Requests Panel"
   >}}
   
   For each issuance request, the following information is displayed:
   
   * **Issuer Status:** Whether or not the issuer has approved the issuance request
   * **Custodian Status:** Whether or not the custodian has approved the issuance request
   * **Token name:** The name of the token definition; normally the full name of the currency; for example, Canadian Dollar
   * **Token symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *CAD*
   * **Amount:** The number of tokens requested
   * **Issuer:** The Transacting Entity who either (1) has to approve the receipt of tokens (if the other party made a Request to Send) or (2) has to approve the sending of tokens (if the other party made a Request to Receive)
   * **Last Updated:** The date and time at which the request was last updated
   
   {{< 
      figure
	  src="images/approving-issuance-request.png"
      width=60%
	  figcaption="Issuance Requests Panel"
	  alt="Issuance Requests Panel"
   >}}
   
7. Click **Approve**.

   The message **Successfully submitted your issuance request** is displayed:
   
   {{< 
      figure
	  src="images/successfully-submitted-issuance-request-update-message.png"
      width=40%
	  figcaption="'Successfully submitted your issuance request' Message"
	  alt="'Successfully submitted your issuance request' Message"
   >}}
   
   The **Update Approval Request** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen: 
   
   {{< 
      figure
	  src="images/update-approval-request-flow.png"
      width=60%
	  figcaption="Update Approval Request Flow"
	  alt="Update Approval Request Flow"
   >}}
   
   Once the **Update Approval Request** flow finishes, the message **Your request update has been successful** is displayed:

   
   {{< 
      figure
	  src="images/request-update-successful-message.png"
      width=40%
	  figcaption="'Your request update has been successful' Message"
	  alt="'Your request update has been successful' Message"
   >}}
  
   If you are an issuer, in the **Issuance Requests** panel, you can now see that the **Issuer Status** of the issuance request is **Approved**:  
  
   {{< 
      figure
	  src="images/issuance-requests-panel-issuer-approved.png"
      width=100%
	  figcaption="Issuance Requests Panel - Approved by Issuer"
	  alt="Issuance Requests Panel - Approved by Issuer"
   >}}
   

   {{< 
      figure
	  src="images/issuance-requests-panel-custodian.png"
      width=100%
	  figcaption="Issuance Requests Panel - Approved by Issuer"
	  alt="Issuance Requests Panel - Approved by Issuer"
   >}}
   
   
   
   
   
   approving-issuance-request-custodian.png
   
   
   
