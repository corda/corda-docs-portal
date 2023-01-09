---
date: '2023-01-05'
title: "Vault"
menu:
  corda-5-beta:
    parent: corda-5-beta-ledger
    identifier: corda-5-beta-vault
    weight: 7000
section_menu: corda-5-beta
---

A Corda vault is a database containing all data from the ledger relevant to a participant. The database tracks spent and unspent (consumed and unconsumed) states. From a business perspective, this means a record of all of the transaction states that you can spend as a participant, and a record of all spent states from transactions relevant to you. You can compare it to a cryptocurrency wallet — a record of what you have spent and how much you have available to spend. 

## Spent and Unspent States

Unspent or unconsumed states represent:
* Fungible states available for spending. 
* States available to transfer to another party. 
* Linear states available for evolution. For example, in response to a lifecycle event on a deal.

Spent or consumed states represent a ledger immutable state. These are kept for the purpose of: 
* Transaction reporting. 
* Audit and archives, including the ability to perform joins with app-private data, like customer notes.

You can use data in your vault to create transactions that send value to another party by combining fungible states, and possibly adding a change output that makes the values balance. This process is referred to as ‘coin selection’.
Spending from the vault in this way ensures that transactions respect fungibility rules. The issuer and reference data is preserved as the assets pass between parties.

## Data Management on and off Ledger
The vault supports the management of data in both authoritative on-ledger form and, where appropriate, shadow off-ledger form:
* On-ledger data refers to distributed ledger state (cash, deals, trades) to which a party is participant. The on-ledger store tracks unconsumed states. The node updates it internally when all participants verify and sign a smart contract and commit a transaction to the ledger.
* Off-ledger data refers to a party’s internal reference, static, and systems data.

In Corda 5.0 Beta 1, the vault query API is limited to either load outputs from a known transaction ID or find all unconsumed states of a specific type.
Transaction recording flows use a vault update API internally.

## Soft Locking to Prevent Double Spend Attempts
Soft locking automatically or explicitly reserves states to prevent multiple transactions within the same node from trying to use the same output simultaneously. Whilst any double spend attempts would ultimately be detected by a notary, soft locking provides a mechanism of early detection for such unwarranted and invalid scenarios.
Soft locking is implemented using token selection.