---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Creating Token Definitions"
    weight: 300
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-creating-token-definitions
    description: "Digital Currencies documentation describing how to create token definitions via the GUI"
title: "Creating Token Definitions"
---


Before tokens can be created, a token definition, which specifies all that parameters of that token, must be created. 

1. In the Digital Currencies GUI, select **Define Token**.

   The **Define Token** page is displayed:
   
   {{< 
      figure
	  src="images/define-token-page.png"
      width=80%
	  figcaption="Define Token Page"
	  alt="Define Token Page"
   >}}
   
   The page displays two panels:
   
   * **New Token Definition:** Enables you to define a new token definition
   * **Active Token Definitions:** Lists any existing token definitions
   
   The **New Token Definition** panel initially shows the **Details** stage of the user journey.
   
2. In the **New Token Definition** panel, specify the following parameters:

   * **Token Name:** The name of the token definition; normally the full name of the currency; for example, Canadian Dollar
   * **Token Symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217 for the currency; for example, CAD
   * **Token Decimal Place:** An integer that specifies the number of decimal places for the currency; for many currencies this is 2; for example, the Canadian dollar (€9.99)
   
   <!-- Keep the above descriptions in sync with those in the overview -->
   
   
3. Click **Next**.

   The **New Token Definition** panel is refreshed to show the **Parties** stage of the user journey:
   
   {{< 
      figure
	  src="images/new-token-definition-parties-stage.png"
      width=80%
	  figcaption="New Token Definition - Parties Stage"
	  alt="New Token Definition - Parties Stage"
   >}}
   
4. Specify the following parameters:

   * **Token Issuer:** The name of the Token Issuing Entity that can mint and burn tokens of this type
   * **Custodian:** The name of the Custodian responsible for the exchange of off-ledger collateral when a non-issuing party requests tokens of this token definition state from the Token Issuer; this setting is optional and can be "No custodian"



5. Click **Next**.

   The **New Token Definition** panel is refreshed to show the **Rules** stage of the user journey:
   
   {{< 
      figure
	  src="images/new-token-definition-rules-stage.png"
      width=80%
	  figcaption="New Token Definition - Rules Stage"
	  alt="New Token Definition - Rules Stage"
   >}}
   
   {{< note >}}
   This stage is not yet operative.
   {{</ note >}}
   
6. Click **Next**.

   The **New Token Definition** panel is refreshed to show the **Review** stage of the user journey: 
   
   {{< 
      figure
	  src="images/new-token-definition-review-stage.png"
      width=80%
	  figcaption="New Token Definition - Review Stage"
	  alt="New Token Definition - Review Stage"
   >}}
   
7. Select **I confirm that the details are correct** and click **Submit**.

   The token definition is submitted and a success message should be displayed:

   {{< 
      figure
	  src="images/token-definition-success.png"
      width=50%
	  figcaption="Token Definition Success"
	  alt="Token Definition Success"
   >}}
   
   The new token definition now appears in the **Active Token Definitions** pane:
   
   {{< 
      figure
	  src="images/active-token-definitions-new-token.png"
      width=50%
	  figcaption="Active Token Definitions - New Token"
	  alt="Active Token Definitions - New Token"
   >}}
   
   You can also view both the list of active token definitions and decommissioned token definitions by selecting **Token Definitions** in the left-hand toolbar to view the **Token Definitions** page:
   
   {{< 
      figure
	  src="images/token-definitions-page.png"
      width=50%
	  figcaption="Token Definitions Page"
	  alt="Token Definitions Page"
   >}}
   
   Now that a token definition has been created, you can create tokens based on that definition.
   
   
   
<!-- This process involves:

* A bank or financial institution requests a deposit in exchange for tokens, as described in *[Requesting Deposits](#requesting-deposits)*.
* A custodian approves the deposit request, as described in *[Accepting or Rejecting Deposit Requests](#accepting-or-rejecting-deposit-requests)*.
* The bank issues a payment to transfer collateral (off-ledger assets) to the custodian in exchange for the issuance of tokens, as described in *[Issuing Payments](#issuing-payments)*.
* The custodian accepts the payment, as described in *[Accepting or Rejecting Payments](#accepting-or-rejecting-payments)*. -->

