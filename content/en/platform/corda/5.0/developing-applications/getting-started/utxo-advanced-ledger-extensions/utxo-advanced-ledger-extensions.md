---
date: '2023-05-17'
title: "UTXO Advanced Ledger Extensions Library"
menu:
  corda5:
    parent: "corda5-develop-get-started"
    identifier: corda5-utxo-ledger-extensions
    weight: 8000
section_menu: corda5
---

# UTXO Advanced Ledger Extensions Library

The Corda 5 Advanced UTXO Ledger Extensions library provides several powerful features to Corda 5's UTXO ledger.
These features have been selected and designed to solve common problems that CorDapp developers face when building states and contracts on Corda.

## Feature Overview

The following definitions provide an overview of each major feature or component that has been implemented in the Corda 5 Advanced UTXO Ledger Extensions library. These features can be used together; for example, a state could be designed to be fungible, issuable and ownable.

| State             | Description                                                                            |
| ----------------- | ----------------------------------------------------------------------------------- |
| Chainable         | Represents strictly linear state chains, where every state in the chain points to the previous state in the chain. This could be thought of as a similar concept to a blockchain, where each new block points to the previous block.     |
| Fungible          | Represents states that have a scalar numeric quantity, and can be split, merged, and mutually exchanged with other fungible states of the same class. Fungible states represent the building blocks for states like tokens.             |
| Identifiable      | Represents states that have a unique identifier that is guaranteed unique at the network level. Identifiable states are designed to evolve over time, where unique identifiers can be used to resolve the history of the identifiable state.                                                      |
| Issuable          | Represents states that have an issuer. Typically an issuer is responsible for signing transactions where issuable states are issued or redeemed.                                                                    |
| Ownable           | Represents states that have an owner. Typically an owner is responsible for signing transactions where ownable states are transferred from one owner to another.                                  |
