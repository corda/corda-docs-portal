---
title: The Corda paradigm
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-corda-paradigm"
    weight: 40

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
- corda paradigm
---



# The Corda Paradigm

Corda smart contracts define what you can't do, not what you can.

The normal programming paradigm is that in a given context you have a set of available functions that take inputs and produce outputs. Other Blockchains, for example Ethereum, use this approach: what you can do with a Solidity smart contract is defined by the methods which are made available to the user of the smart contract.

Corda smart contracts work in a different way. Corda lets the creator of the transaction do what ever they want as long as it conforms to the rules set out in the Contract class. This approach gives massive flexibilty for the CorDapp developer, but that flexibility shouldn't necessarily be passed on to the user of the Smart Contract as it can increase the risk of misuse.

In the extreme case, if the contract class verify() function is empty the transaction can contain anything. This might be fine depending on what your CorDapp is doing, but, for example, it's not fine if the security of the CorDapp assumes that your counterparty can't change the price that they are agreeing to pay for the goods you are shipping them when, because of a lack of adequate constraints, they can.

So if the actions that a smart contract user can take need to be limited, which is most cases, then the smart contract designer needs to have confidence that the constraints in the smart contract adequately box in the user.

The structure provided by CDL aims to help the Smart Contract designer make sure there are no 'Holes in the Fence' which unwanted behaviour can slip through.

{{< note >}}
In most CorDapps the actions a user can take are limited by the Flows which are provided in the CorDapp. But it is important to remember that Flows can be, and to an extent are intended to be, rewritten by each Counterparty to suit their particular implementation requirements. The Corda guarantee of shared data and logic is only valid at the smart contract/ transaction level. Controls written into the Flows are by their nature not as secure as controls written into the Smart Contracts.
{{< /note >}}
