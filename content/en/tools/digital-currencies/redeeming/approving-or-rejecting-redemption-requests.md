---
date: '2023-04-25'
lastmod: '2023-04-25'
section_menu: tools
menu:
  tools:
    name: "Approving or Rejecting Redemption Requests"
    weight: 600
    parent: digital-currencies-token-redemption
    identifier: digital-currencies-approving-rejecting-redemption-requests
    description: "Digital Currencies documentation describing how to approve or reject redemption requests via the GUI"
title: "Approving or Rejecting Redemption Requests"
---

A {{< tooltip >}}redemption{{< definitiondc term="redemption" >}}{{< /tooltip >}} request must be approved by both:

* The issuer of the digital currency.
* The custodian of the digital currency.

The issuer must perform the first approval, followed by the custodian. 

Once approved, the participant who [created the request]({{< relref "creating-redemption-requests.md" >}}) can then [complete the token redemption]({{< relref "completing-redemptions.md" >}}).

To approve or reject a redemption request (as either an issuer or a custodian):

1. In the left-hand menu, click on **Redemptions**.

   The **Redemptions** page is displayed:
   
   {{< 
      figure
	  src="images/redemptions-page-central-bank.png"
      width=100%
	  figcaption="Redemptions Page"
	  alt="Redemptions Page"
   >}}

   The page shows the following panels:

   * **Vault Balances**: A Corda vault is a database containing all data from the ledger relevant to a participant. For more information, see [the Vault topic]({{< relref "/en/platform/corda/5.0/developing-applications/ledger/vault/_index.md" >}}).
   * **Redemption Requests:** Lists any existing issuance requests and their status.
  
  If you are logged in as the issuer, the panel will look like this:
  
   {{< 
      figure
	  src="images/redemption-requests-panel-issuer.png"
      width=100%
	  figcaption="Redemption Requests Panel (as Issuer)"
	  alt="Redemption Requests Panel (as Issuer)"
   >}}
   
   If you are logged in as the custodian, the panel may look like this if the issuer has already approved the redemption request:
     
   {{< 
      figure
	  src="images/redemption-requests-panel-custodian.png"
      width=100%
	  figcaption="Redemption Requests Panel (as Custodian)"
	  alt="Redemption Requests Panel (as Custodian)"
   >}}
   
   For each redemption request, the following information is displayed:
   
   * **Issuer Status:** APPROVED or PENDING, depending on if the issuer has approved the redemption request or not.
   * **Custodian Status:** APPROVED or PENDING, depending on if the custodian has approved the redemption request or not.
   * **Token name:** The name of the token definition; normally the full name of the currency; for example, UAE Dirham.
   * **Token symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *AED*.
   * **Amount:** The number of tokens to be redeemed.
   * **Requester:** The entity making the redemption request.
   * **Last updated:** The date and time at which the redemption request was last updated.
   
2. Click the relevant redemption request.

   The **Redemption Request** dialog box is displayed:
   
   {{< 
      figure
	  src="images/approving-redemption-request.png"
      width=40%
	  figcaption="Redemption Request Confirmation Dialog"
	  alt="Redemption Request Confirmation Dialog"
   >}}  
   
   If the dialog box looks like the following image, that means the current participant is a custodian but the issuer has not yet approved the redemption request:
   
   {{< 
      figure
	  src="images/approving-redemption-request-issuer-not-approved.png"
      width=40%
	  figcaption="Redemption Request Confirmation Dialog - Not Approved by Issuer"
	  alt="Redemption Request Confirmation Dialog - Not Approved by Issuer"
   >}}
   
3. Click **Approve**.

   The message **Successfully submitted your redemption approval request update** is displayed:
   
   {{< 
      figure
	  src="images/successfully-submitted-redemption-approval-request-update-message.png"
      width=40%
	  figcaption="'Successfully submitted your redemption approval request update' Message"
	  alt="'Successfully submitted your redemption approval request update' Message"
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
  
   If you are an issuer, you can now see that, in the **Redemption Requests** panel, the **Issuer Status** of the redemption request is now **Approved**:  
  
   {{< 
      figure
	  src="images/redemption-requests-panel-issuer-approved.png"
      width=100%
	  figcaption="Redemption Requests Panel - Approved by Issuer"
	  alt="Redemption Requests Panel - Approved by Issuer"
   >}}
   
   If you are a custodian, you can now see that, in the **Redemption Requests** panel, the **Custodian Status** of the redemption request is now **Approved**:  

   {{< 
      figure
	  src="images/issuance-requests-panel-custodian-approved.png"
      width=100%
	  figcaption="Redemption Requests Panel - Approved by Custodian"
	  alt="Redemption Requests Panel - Approved by Custodian"
   >}}
   
   
Once both the issuer and the custodian have approved the redemption request, the participant that created the request will see their request has been approved. However, they will not see their vault balance updated until the participant [completes the redemption]({{< relref "completing-redemptions.md" >}}).
   
   
   
   
