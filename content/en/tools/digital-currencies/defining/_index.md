---
date: '2023-07-04'
lastmod: '2023-07-04'
section_menu: tools
menu:
  tools:
    name: "Working with Token Definitions"
    weight: 500
    parent: digital-currencies
    identifier: digital-currencies-token-definitions
    description: "Digital Currencies documentation describing how to create token definitions via the GUI"
title: "Working with Token Definitions"
---

A *token definition* specifies all the properties that a token of that type can have. Token definitions are created by users of the role Token Defining Entity (TDE). 

Token definitions have the following properties:

* **Name:** The name of the token definition; normally the full name of the currency; for example, *Canadian Dollar*.
* **Symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *CAD*.
* **Decimals:** An integer that specifies the number of decimal places for the currency; for many currencies this is 2; for example, the Canadian Dollar ($9.99).
* **Token Issuer:** The name of the Token Issuing Entity; this is the party on the network that can issue tokens of this type. This party will make the final decision whether an issuance happens or not. <!-- only one in initial release -->
* **Token Definers:** The name of the Token Defining Entity that defined the token definition. This value is set automatically when the token definition is defined.
* **Custodian:** The name of the custodian; they are the party on the network responsible for the exchange of off-ledger collateral when a non-issuing party requests tokens of this token definition state from the Token Issuer. This party’s responsibility is to inform the issuer that a requesting bank has paid for the token they are requesting. This setting is optional and can be "None".
* **Timestamp:** The date and time at which the token definition was committed to the Corda ledger; this setting is specified automatically when the token definition is defined.
* **ID:** The unique ID for the token definition; this setting is specified automatically when the token definition is defined.
* **Version:** An integer specifying the version of the token definition.

This section describes the tasks associated with token definitions. It contains the following:
{{< childpages >}}