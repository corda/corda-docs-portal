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

* **Token Defining Entities:** Each network has one or more Token Defining Entities. This role is used to create token definitions. A TDE can create multiple token definitions. In a central bank, this role might be held by someone from the Currency vault management; in a Commercial bank, the Head of Treasury. 

* **Token Definition Authorities (TDA):** Each network has one or more token definition authorities. This role is used to approve any token definitions. There can be multiple users across the entity which reside in different departments. Their function is to review the token definition presented and approve or reject. In a central bank, this role might be held by a Board of Governors; in a commercial bank, it might be Head of Legal Services or Head of Regulation/Compliance.

* **Token Issuing Entities (TIE):** Each network has one or more Token Issuing Entity (TIE)s. They are responsible for receiving attestation from custodians with regards to the backing of the collateral and issuing (creating then transfering) tokens to recipients. 

* **Transacting Entities (TE)** Each network has one or more transacting entities (TE). Transacting Entities are the consumers of tokens on the network. Transacting entities can request tokens from token issuing entities, use them to transact with other transacting entities, and then redeem tokens with a token issuing entity.

* **Custodians:** Each network must have one or more custodians. A custodian attests to the reception of the underlying collateral funds for tokens created by the TIE on the network. It verifies collateral payments that are received from a network participant through banking deposits either held with a central bank or a commercial bank.  

* **Regulators:** Each network can have one or more regulators. Observers only have read permissions and can view issuances, transfers and redemptions to keep track of economic statistics. They are unable to make transfers or hold tokens. Such a role might be used by regulatory authorities or risk departments.

## Role Permissions

| ROLE           | CREATE | TRANSFER | REDEEM | RULES                                                                                                                                                                                                                 |
| -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TE             | N      | Y        | Y      | Transacting Entity A wants to transfer a set number of tokens to another Transacting Entity (on the same network) or request an Transacting Entity (on the same network) to transfer a set number of tokens to itself |
| TE (receiving) | N      | Y        | Y      | A receiving Transacting Entity must approve or reject set number of tokens from another Transacting Entity                                                                                                            |
| TE (sending)   | N      | Y        | Y      | Transacting Entity will sign the transaction to handover ownership of the tokens. Smart contract is updated to reflect the new owner                                                                                  |
| Custodian      | N      | N        | N      | Custodian has no knowledge the token ownership has changed hands                                                                                                                                                      |
| TIE            | N      | N        | N      | TIE has no knowledge the token ownership has changed hands                                                                                                                                                            |
| Custodian      | N      | N        | N      | Custodian could also play the regulator role so they can determine where tokens have been moved                                                                                                                        |
| TE (receiving) | N      | Y        | N      | Transacting Entity receiving tokens will also see an increase in the balance of tokens for that token type                                                                                                            |
| TE (sending)   | N 
<!-- https://jor3cev.sharepoint.com/:w:/r/teams/R3Squads/_layouts/15/Doc.aspx?sourcedoc=%7B8407F5F0-355E-4F1F-BAE3-FD0998EFE962%7D&file=Feature_Roles.docx&_DSL=1&action=default&mobileredirect=true -->