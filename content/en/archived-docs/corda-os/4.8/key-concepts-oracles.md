---
aliases:
- /head/key-concepts-oracles.html
- /HEAD/key-concepts-oracles.html
- /key-concepts-oracles.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-oracles
    parent: corda-os-4-8-key-concepts
    weight: 1110
tags:
- concepts
- oracles
title: Oracles
---


# Oracles

## Summary

* Oracles let [smart contracts](key-concepts-contracts.md) execute based on real-world data.
* They query, validate, and authenticate information at the request of a [node](key-concepts-node.md).
* You can minimize the amount of [transaction](key-concepts-transactions.md) data that an oracle sees by [tearing off](key-concepts-tearoffs.md) the portions that the oracle does not need to access.

## Video

{{% vimeo 214157956 %}}

## What is an oracle?
Oracles are network services that supply external information to smart contracts. They serve as bridges between Corda networks and the outside world, broadening the uses for [smart contracts](key-concepts-contracts.md) to include agreements that require off-ledger information to execute. This could include anything from the current exchange rate for a transfer of funds, to the weather in Minnesota for an insurance policy.

Oracles are not the source of information—they're an entity that queries, verifies, and authenticates external data sources, then relays that information back to a [smart contract](key-concepts-contracts.md).

For example, Alice sells Bob an insurance policy that covers a crop failure due to drought. They agree that Alice will pay Bob $50,000 if temperatures on his farm rise above 100 degrees Fahrenheit for seven consecutive days. They can write this into a smart contract that depends on a mutually-trusted API reporting the weather from the National Weather Service. If Bob puts in a claim, the oracle queries the API to determine that the defined drought conditions have been met. If they have, the smart contract executes and Bob receives $50,000 from Alice.

## How oracles work
If a node wants to assert a fact when proposing a transaction (for example, Bob claiming that his farm is experiencing drought), they can request a command that asserts that fact from the oracle. If the oracle determines the fact to be true (for example, by querying the National Weather Service's API), they send the node the required command. The node can then include the fact (in the form of the command) in their transaction, and the oracle signs the transaction to assert the validity of the fact.

Some oracles monetize their services. In that case, you'll need to pay the oracle before they sign the transaction.

## Oracles and privacy
The oracle doesn't need to see the whole contract–only the part it needs to validate. The node proposing the transaction can [tear off](key-concepts-tearoffs.md) unrelated parts of the contract before the oracle sees it. For example, in Alice and Bob's contract, the oracle is only attesting to the temperature on Bob's farm, so it doesn't need to know how much the insurance policy is for. Bob could tear off that information.


