---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Viewing Token Definitions"
    weight: 400
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-viewing-token-definitions
    description: "Digital Currencies documentation describing how to create token definitions via the GUI"
title: "Viewing Token Definitions"
---

Once [token definitions]({{< relref "tokens-overview.md#token-definitions" >}}) have been created, they can be viewed on the **Token Definitions** page.

* In the Digital Currencies GUI, select **Token Definitions**.

   The **Token Definitions** page is displayed:
   
   {{< 
      figure
	  src="images/token-definitions-page.png"
      width=80%
	  alt="Token Definitions Page"
	  figcaption="Token Definitions Page"
   >}}
   
The page displays two panels:
   
* **Active Token Definitions:** This panel lists any active token definitions; for each token, the following parameters are displayed:

    * **Name:** The name of the token definition; normally the full name of the currency; for example, *Canadian Dollar*
    * **Symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *CAD*
    * **Definition Date:** The date and time at which the token definition was committed to the Corda ledger, in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601); this value is specified automatically when the token definition is defined
    * **Decimals:** An integer that specifies the number of decimal places for the currency; for many currencies this is 2; for example, the Canadian dollar (€9.99)
    * **Definer:** The [X.500](https://en.wikipedia.org/wiki/X.500) name of the Token Defining Entity that defined the token definition. This value is set automatically when the token definition is defined.
    * **Issuer:** The name of the Token Issuing Entity that can mint and burn tokens of this type <!-- only one in initial release -->
    * **Custodian:** The name of the Custodian responsible for the exchange of off-ledger collateral when a non-issuing party requests tokens of this token definition state from the Token Issuer; this setting is optional and can be "None"
    * **ID:** The unique ID for the token definition; this setting is specified automatically when the token definition is defined
    <!--* **Version:** An integer specifying the version of the token definition -->
* **Decommisioned Token Definitions:** This panel lists any decommissioned token definitions
   
<!-- From this page, you can perform the following actions:

* [Decommission token definitions]({{< relref "decommissioning-token-definitions.md" >}}) -->
  