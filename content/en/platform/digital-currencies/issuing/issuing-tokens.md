---
date: '2023-06-23'
lastmod: '2023-06-23'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Issuing Tokens"
    weight: 800
    parent: digital-currencies-token-issuance
    identifier: digital-currencies-issuing-tokens
    description: "Digital Currencies documentation describing how to issue tokens via the GUI"
title: "Issuing Tokens"
---

Once an [issuance request has been created]({{< relref "creating-issuance-requests.md" >}}) and then subsequently [approved by both the issuer and the custodian]({{< relref "approving-or-rejecting-issuance-requests.md" >}}), new tokens of that type can be issued by the issuer to the participant that made the approved request.

Such tokens can then be used as for currency or utility purposes and allow the issuing party to maintain monetary policy and provide easily accessible digital currency tokens to specific entities.

As an issuer:

1. Click **Issuances** in the left-hand sidebar.

   The **Issuances** page is displayed:

   {{<
      figure
	  src="images/issuances-page-both-approved.png"
      width=100%
	  figcaption="Issuances Page"
	  alt="Issuances Page"
   >}}

   The **Issuance Requests** panel lists any issuance requests for tokens to the currently-logged-in issuer.

2. In the **Issuance Requests** pane, click on any request which has been approved by both the issuer and the custodian (that is, the values of **Issuer Status** and **Custodian Status** are both **Approved**).

   The **Issuance Request** dialog box is displayed:

   {{<
      figure
	  src="images/issuance-request-dialog.png"
      width=40%
	  figcaption="Issuance Request Dialog Box"
	  alt="Issuance Request Dialog Box"
   >}}

3. Click **Issue**.

   The *Successfully submitted the issuance of tokens* message is displayed:

   {{< figure src="images/successfully-submitted-issuance-tokens-message.png" width=50% figcaption="'Successfully submitted the issuance of tokens' Message" alt="'Successfully submitted the issuance of tokens' Message" >}}

   The **Issue tokens** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:

   {{<
      figure
	  src="images/issue-tokens-flow.png"
      width=50%
	  figcaption="Issue Tokens - Flow Running"
	  alt="Issue Tokens - Flow Running"
   >}}

   Once the **Issue tokens** flow completes, the message *Issuance of tokens has been successful* is displayed:

   {{<
      figure
	  src="images/issuance-tokens-successful-message.png"
      width=50%
	  figcaption="'Issuance of tokens has been successful' Message"
	  alt="'Issuance of tokens has been successful' Message"
   >}}

   The issuance request disappears from the **Issuance Requests** panel.
   
   The vault balance of the requesting participant is updated to show the issuance:
   
   {{<
      figure
	  src="images/vault-balances-panel-after-issue.png"
      width=40%
	  figcaption="Vault Balances Panel After Issue"
	  alt="Vault Balances Panel After Issue"
   >}}

