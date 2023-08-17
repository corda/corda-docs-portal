---
date: '2023-06-23'
lastmod: '2023-06-23'
section_menu: tools
menu:
  tools:
    name: "Completing Redemptions"
    weight: 800
    parent: digital-currencies-token-redemption
    identifier: digital-currencies-redeeming-tokens
    description: "Digital Currencies documentation describing how to complete the redemption of tokens via the GUI"
title: "Completing Redemptions"
---

Once a [redemption request has been created]({{< relref "creating-redemption-requests.md" >}}) and then subsequently [approved by both the issuer and the custodian]({{< relref "approving-or-rejecting-redemption-requests.md" >}}), the {{< tooltip >}}redemption{{< definitiondc term="redemption" >}}{{< /tooltip >}} process can be completed by the participant who initiated it.


As the participant who created the original request:

1. Click **Redemptions** in the left-hand sidebar.

   The **Redemptions** page is displayed:

   {{<
      figure
	  src="images/redemptions-page-commerical1-approved.png"
      width=100%
	  figcaption="Redemptions Page"
	  alt="Redemptions Page"
   >}}

   The **Redemption Requests** panel lists any redemption requests for tokens for the current participant.

2. In the **Redemption Requests** pane, click on any request which has been approved by both the issuer and the custodian (that is, the values of **Issuer Status** and **Custodian Status** are both **Approved**).

   The **Redemption Request** dialog box is displayed:

   {{<
      figure
	  src="images/redemption-request-dialog.png"
      width=40%
	  figcaption="Redemption Request Dialog Box"
	  alt="Redemption Request Dialog Box"
   >}}

3. Click **Complete Redemption**.

   The *Successfully submitted redemption finalisation request* message is displayed:

   {{< figure src="images/successfully-submitted-redemption-finalisation-request-message.png" width=50% figcaption="'Successfully submitted redemption finalisation request' Message" alt="'Successfully submitted redemption finalisation request' Message" >}}

   The **Redeem Token** flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:

   {{<
      figure
	  src="images/redeem-token-flow.png"
      width=50%
	  figcaption="Redeem Token - Flow Running"
	  alt="Redeem Token - Flow Running"
   >}}

   Once the **Redeem Token** flow completes, the message **Tokens have been redeemed successfully** is displayed:

   {{<
      figure
	  src="images/tokens-have-been-redeemed-successfully-message.png"
      width=50%
	  figcaption="'Tokens have been redeemed successfully' Message"
	  alt="'Tokens have been redeemed successfully' Message"
   >}}

   The redemption request disappears from the **Redemption Requests** panel.
   
   The vault balance of the requesting participant is updated to show the number of tokens that has been debited in accordance with the redemption:
   
   {{<
      figure
	  src="images/vault-balances-panel-after-redemption.png"
      width=40%
	  figcaption="Vault Balances Panel After Redemption"
	  alt="Vault Balances Panel After Redemption"
   >}}

   Similarly, the vault balance of the relevant issuer is updated to show the number of tokens that has been increased in accordance with the redemption.
