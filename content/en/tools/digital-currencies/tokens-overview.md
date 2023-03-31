---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Tokens Overview"
    weight: 600
    parent: digital-currencies
    identifier: digital-currencies-tokens-overview
    description: "Digital Currencies documentation describing the concept of tokens."
title: "Tokens Overview"
---

Digital Currencies from Corda enables central banks and commercial banks to define their own digital currency token definitions, mint tokens based on those definitions, and enable transacting entities on the same network to transfer these tokens to each other.

## Token Definitions

A token definition specifies all the properties that a token of that type can have. Token definitions are created by users of the role Token Defining Entity (TDE). 

Token definitions have the following properties:

* **Name:** The name of the token definition; normally the full name of the currency; for example, *Canadian Dollar*
* **Symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *CAD*
* **Decimals:** An integer that specifies the number of decimal places for the currency; for many currencies this is 2; for example, the Canadian dollar (€9.99)
* **Token Issuer:** The name of the Token Issuing Entity; this is the party on the network that can issue tokens of this type.  This party will make the final decision whether an issuance happens or not. <!-- only one in initial release -->
* **Token Definers:** The name of the Token Defining Entity that defined the token definition. This value is set automatically when the token definition is defined.
* **Custodian:** The name of the Custodian; they are the party on the network responsible for the exchange of off-ledger collateral when a non-issuing party requests tokens of this token definition state from the Token Issuer. This party’s responsibility is to inform the issuer that a requesting bank has paid for the token they are requesting. This setting is optional and can be "None".
* **Timestamp:** The date and time at which the token definition was committed to the Corda ledger; this setting is specified automatically when the token definition is defined
* **ID:** The unique ID for the token definition; this setting is specified automatically when the token definition is defined
* **Version:** An integer specifying the version of the token definition

<!-- in future, this value is automatically incremented by 1 each time the version is updated.-->


## Token Definition Statuses

Each token definition also has a status:

* **Pending**: When a Token Defining Entity is in the process defining a token definition, it is editable and not sharable at this point

* **Active**: Once the Token Defining Entity is satisfied with their token definition, they can change its status from Pending to Active. This allows the definition to be shared across the network, allowing other nodes to request tokens of this definition. Once a node holds such a token, they transfer it to other nodes, and redeem the token. Having a status of Active indicates that the token definition is available for transactions.

* **Decommissioned:** Once a token definition is decommissioned, no more tokens of that definition can be created. Existing tokens of that definition will now have a status of decommissioned. Currently, such tokens can still be transferred and redeemed. A decommissioned token definition can be set back to Active.

<!-- a token As token definition states will never (or not regularly) be completely deleted from the vault of the token definition state creator and others referencing this state, they must be ‘decommissioned’. Much like how £10 note today is decommissioned, currency has a lifecycle. Once decommissioned, the token definition status is of the decommissioned, those tokens in circulation will contain a ‘decommissioned’ status but in this version can still be transfered and redeemed. We will be applying expiry date in a future release to restrict this circulation. When a token is decommissioned you can redeem but the issuing party cannot create a digital currency based on a decommissioned definition. Additionally, should the token definer wish to reinstate the decommissioned definition they can reset the definition back to active. They cannot reset to pending and then edit the definition.   token definition state cannot be issued or transacted with, but they can be redeemed.

## Token Definition Actions

The following actions can be performed on token definitions:

* Creating states
* Query vault for token definition state
* Sharing states


### Sharing Token Definitions



## Token Actions

The following actions can be performed on token

## Creating Tokens (CreateTokenFlow)

Input state: none

Returns: an output state of a number of tokens of a specific token definition state.

see [IssueTokenCommand] for contract rules

## Burning Tokens

Burning tokens removes them from existence. This action can only be performed by the Token Issuer of the token.


## Requesting Tokens

A non-issuer party on the network, such as a Transacting Entity, can request tokens of a specific definition from its Token Issuer.

To make such a request, the requesting party initiates a CreateTokenManagementApprovalFlow process. This request must be approved by both the issuer and a custodian (but only if the token definition as a Custodian setting specified).

 -->

