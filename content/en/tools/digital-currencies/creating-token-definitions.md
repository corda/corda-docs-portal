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


Before tokens can be created, a [token definition]({{< relref "tokens-overview.md#token-definitions" >}}), which specifies all that parameters of that token, must be created. 

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

   * **Token Issuer:** The name of the Token Issuing Entity; this is the party on the network that can issue tokens of this type.  This party will make the final decision whether an issuance happens or not.
   * **Custodian:** The name of the Custodian; they are the party on the network responsible for the exchange of off-ledger collateral when a non-issuing party requests tokens of this token definition state from the Token Issuer. This party’s responsibility is to inform the issuer that a requesting bank has paid for the token they are requesting. This setting is optional and can be "None".



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
   
   The token definition flow begins and its progress can be checked in the pull-out flow tracker on the right-hand side of the screen:
    
   {{< 
      figure
	  src="images/define-token-flow-running.png"
      width=50%
	  figcaption="Creating Token Definitions - Flow Running"
	  alt="Creating Token Definitions - Flow Running"
   >}}  
   
   Once the token definition flow completes, the flow status is displayed as **Completed**:
   
     
   {{< 
      figure
	  src="images/define-token-flow-completed.png"
      width=50%
	  figcaption="Creating Token Definitions - Flow Completed"
	  alt="Creating Token Definitions - Flow Completed"
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
   
Now that a token definition has been created, you can:

* [View existing token definitions]({{< relref "viewing-token-definitions.md" >}})
* [Create tokens based on that definition]({{< relref "creating-tokens.md" >}})
   
   
 