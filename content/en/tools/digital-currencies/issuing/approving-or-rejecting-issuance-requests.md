---
date: '2023-04-25'
lastmod: '2023-04-25'
section_menu: tools
menu:
  tools:
    name: "Approving or Rejecting Issuance Requests"
    weight: 600
    parent: digital-currencies-token-issuance
    identifier: digital-currencies-approving-rejecting-issuance-requests-issuer
    description: "Digital Currencies documentation describing how to approve or reject issuance requests via the GUI"
title: "Approving or Rejecting Issuance Requests"
---

An issuance request must be approved by both:

* The issuer of the digital currency.
* The custodian of the digital currency.

The issuer must perform the first approval, followed by the custodian. 

Once approved, the tokens are then transferred to the requesting entity.

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

   * **Vault Balance**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
   * **Issuance Requests:** Lists any existing issuance requests and their status.
  
  If you are logged in as the issuer, the panel will look like this:
  
   {{< 
      figure
	  src="images/issuance-requests-panel-issuer.png"
      width=100%
	  figcaption="Issuance Requests Panel (as Issuer)"
	  alt="Issuance Requests Panel (as Issuer)"
   >}}
   
   If you are logged in as the custodian, the panel may look like this if the issuer has already approved the request:
     
   {{< 
      figure
	  src="images/issuance-requests-panel-custodian.png"
      width=100%
	  figcaption="Issuance Requests Panel (as Custodian)"
	  alt="Issuance Requests Panel (as Custodian)"
   >}}
   
   For each issuance request, the following information is displayed:
   
   * **Issuer Status:** Whether or not the issuer has approved the issuance request.
   * **Custodian Status:** Whether or not the custodian has approved the issuance request.
   * **Token name:** The name of the token definition; normally the full name of the currency; for example, Canadian Dollar.
   * **Token symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *CAD*.
   * **Amount:** The number of tokens requested.
   * **Requester:** The entity making the issuance request.
   * **Last Updated:** The date and time at which the request was last updated.
   
2. Click the relevant request.

   The following dialog box is displayed:
   
   {{< 
      figure
	  src="images/approving-issuance-request.png"
      width=40%
	  figcaption="Issuance Request Confirmation Dialog"
	  alt="Issuance Request Confirmation Dialog"
   >}}  
   
   If the dialog box looks like the following image, that means the current participant is a custodian but the issuer has not yet approved the request:
   
   {{< 
      figure
	  src="images/approving-issuance-request-issuer-not-approved.png"
      width=40%
	  figcaption="Issuance Request Confirmation Dialog - Not Approved by Issuer"
	  alt="Issuance Request Confirmation Dialog - Not Approved by Issuer"
   >}}
   
3. Click **Approve**.

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
  
   If you are an issuer, in the **Issuance Requests** panel, you can see that the **Issuer Status** of the issuance request is now **Approved**:  
  
   {{< 
      figure
	  src="images/issuance-requests-panel-issuer-approved.png"
      width=100%
	  figcaption="Issuance Requests Panel - Approved by Issuer"
	  alt="Issuance Requests Panel - Approved by Issuer"
   >}}
   
   If you are a custodian, in the **Issuance Requests** panel, you can see that the **Custodian Status** of the issuance request is now **Approved**:  

   {{< 
      figure
	  src="images/issuance-requests-panel-custodian-approved.png"
      width=100%
	  figcaption="Issuance Requests Panel - Approved by Issuer"
	  alt="Issuance Requests Panel - Approved by Issuer"
   >}}
   
   
Once both the issuer and the custodian have approved the issuance request, the participant that created the request will see their request has been approved. However, they will not see their vault balance updated until the issuer actually [issues the tokens]({{< relref "issuing-tokens.md" >}}).
   
   
   
   
