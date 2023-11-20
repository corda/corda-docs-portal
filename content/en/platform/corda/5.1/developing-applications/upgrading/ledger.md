---
date: '2023-11-20'
title: "Ledger Implications of Upgrading CorDapps"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-upgrading-ledger
    parent: corda51-upgrading
    weight: 1000
section_menu: corda51
---
# Ledger Implications of Upgrading CorDapps

When upgrading a CorDapp you should consider the following implications for the ledger:
{{< toc >}}

## Contract upgrade

The contract code executed during contract verification of new transactions always uses the contract of the current CPI. The verification rule for the contract upgrade can be the different than the previous one. It is important that newer contracts can still verify states that already exist on the ledger, potentially created with an older version of the contract.

## State upgrade

State upgrades have specific requirements. To ensure smooth functioning across different versions of states within CPI, it’s essential to serialize states using AMQP serialization. Default Class Evolution page provides details on how to make your states serializable across versions. Neglecting this guideline might lead to deserialization issues when attempting to access states from the vault such as querying with API, getting from transaction and accessing in contract code.

## Impact on Ledger Service API

The retrieved states from APIs will use the state class of the new version / current CPI.

## Backchain upgrade

The backchain is designed to work seamlessly with transactions from various versions,
ensuring compatibility across different versions.
