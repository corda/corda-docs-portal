---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Roles Overview"
    weight: 800
    parent: digital-currencies
    identifier: digital-currencies-roles-overview
    description: "Digital Currencies documentation describing the concept of roles."
title: "Roles Overview"
---

The following roles are present on a network:

* **Business Network Operator (BNO):** Each network has a single BNO which creates the network, attests to memberships across the network and provides security through network governance.  

* **Token Defining Entities:** Each network has one or more Token Defining Entities who define and update token types. A TDE can define multiple token types. A TDE requires a TIE (Token Issuing Entity) node. 

* **Token Definition Authorities (TDA):** Each network has one or more Token Definition Authorities. 

* **Token Issuing Entities (TIE):** Each network has one or more Token Issuing Entity (TIE)s. They are responsible for minting and burning token types for tokens with collateral. 

* **Transacting Entities (TE)** Each network has one or more Transacting Entities (TE). Transacting Entities are the consumers of tokens on the network. Transacting Entities can request tokens from a Token Issuing Entity, transact with other Transacting Entities, and redeem token with a Token Issuing Entity.

* **Custodians:** Each network must have one or more custodian nodes which maintain the underlying collateral funds for tokens created by the TIE on the network. The custodians verify collateral payments that are received from a network actor through banking deposits either held with a central bank or a commercial bank. 

* **Observers:** Each network can have one or more observers. Observers only have read permissions and would view issuances, transfers and redemptions to keep track of economic statistics. They are unable to make transfers or hold tokens. Such a role might be used by regulatory authorities or risk departments.

## Role Permissions

| ROLE           | CREATE | TRANSFER | REDEEM | RULES                                                                                                                                                                                                                 |
| -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TE             | N      | Y        | Y      | Transacting Entity A wants to transfer a set number of tokens to another Transacting Entity (on the same network) or request an Transacting Entity (on the same network) to transfer a set number of tokens to itself |
| TE (receiving) | N      | Y        | Y      | A receiving Transacting Entity must approve or reject set number of tokens from another Transacting Entity                                                                                                            |
| TE (sending)   | N      | Y        | Y      | Transacting Entity will sign the transaction to handover ownership of the tokens. Smart contract is updated to reflect the new owner                                                                                  |
| Custodian      | N      | N        | N      | Custodian has no knowledge the token ownership has changed hands                                                                                                                                                      |
| TIE            | N      | N        | N      | TIE has no knowledge the token ownership has changed hands                                                                                                                                                            |
| Custodian      | N      | N        | N      | Custodian could also play the observer role so they can determine where tokens have been moved                                                                                                                        |
| TE (receiving) | N      | Y        | N      | Transacting Entity receiving tokens will also see an increase in the balance of tokens for that token type                                                                                                            |
| TE (sending)   | N 
<!-- https://jor3cev.sharepoint.com/:w:/r/teams/R3Squads/_layouts/15/Doc.aspx?sourcedoc=%7B8407F5F0-355E-4F1F-BAE3-FD0998EFE962%7D&file=Feature_Roles.docx&_DSL=1&action=default&mobileredirect=true -->