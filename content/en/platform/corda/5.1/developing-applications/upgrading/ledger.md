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

## Contract

The contract code executed during contract verification of new transactions always uses the contract of the current CPI. The verification rule for the contract upgrade may differ from the previous one. You must ensure that newer contracts can continue to verify states, created with an older version of the contract, that already exist on the ledger.

## State

State upgrades have specific requirements. To ensure smooth functioning across different versions of states within a CPI, you must serialize states using AMQP [serialization]({{< relref "../api/serialization/_index.md" >}}). For information about how to make your states serializable across versions, see [Default Class Evolution]({{< relref "../api/serialization/amqp-serialization-default-evolution.md" >}}). Neglecting this guideline can cause deserialization issues when attempting to access states from the vault by querying with the API, retrieving from the transaction, or accessing in contract code.

## Ledger Service API

The retrieved states from APIs use the state class of the current CPI.

## Backchain

The backchain is designed to work seamlessly with transactions from various versions, ensuring compatibility across different versions.
