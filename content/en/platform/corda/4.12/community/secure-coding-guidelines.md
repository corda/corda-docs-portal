---
aliases:
- /head/secure-coding-guidelines.html
- /HEAD/secure-coding-guidelines.html
- /secure-coding-guidelines.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-12:
    identifier: corda-community-4-12-secure-coding-guidelines
    parent: corda-community-4-12-building-a-cordapp-index
    weight: 1080
tags:
- secure
- coding
- guidelines
title: Secure coding guidelines
---


# Security best practices

Corda is designed to be secure by default. However, the platform cannot create a secure environment on its own - you need to follow security best practices when developing CorDapps.

This document explains:
* Why you should write secure CorDapps, even if you trust the counterparties you transact with.
* Where and how security issues can be introduced to your transaction.
* Security best practices.


## Why write secure CorDapps when I trust the other party?
If you trust the counterparties you are currently doing business with, it may be tempting to skip security measures. However, you may want to add additional counterparties in the future. Building secure CorDapps from the start lets you add additional counterparties quickly without extensive vetting.

Once you have signed a transaction, there is nothing you can do to prevent the transaction's counterparty from committing it to the ledger. Make sure you know what you are signing and that the counterparty has not changed any details in the course of the transaction.

## Entry points for attacks
Your CorDapp is vulnerable at two points:
* **Flows**. Flows let your CorDapp communicate with other parties on the network. That means insecure flows can be an entry point for malicious data.
* **Contracts**. Contracts are arbitrary functions inside a JVM sandbox, so it is important that they behave as expected.

### Secure flows

Counterparties on a network have the ability to run their own code - it's possible that they may not be running the code you provided to take part in the flow. This means it's up to you to validate everything you receive over the network.

The `receive` methods remind you to validate this data by wrapping it in the `UntrustworthyData<T>` marker type. This type does not add any functionality, it is only a reminder.

Make sure this type of data:

* Matches any partial transaction built or proposed earlier in the flow. For example, you propose to trade a cash state worth $100 for an asset. When the other side returns your proposal, you must ensure it points to the $100 cash state you indicated. A malicious counterparty could attempt to get you to sign a transaction that results in you spending a higher-value state, if they know that state's ID.
* Matches the expected transaction type. There are two transaction types: general and notary change. If you are expecting a general transaction type but accidentally authorize a notary change, you could transfer your assets to a hostile notary.
* Does not contain any unexpected changes to the states in a transaction. The best way to check this is to re-run the builder logic and compare the resulting states to make sure the result is as expected. For example, if both parties have the data required to construct the next state, they can share the function to calculate the transaction they want to mutually agree between the classes implementing both sides of the flow.



### Secure contracts
Make sure your contracts are secure. Check that:

* All changes in states are allowed by the current state transition. Check each field to make sure any changes are intentional.
* You do not accidentally catch and discard any exceptions thrown by the validation logic.
* If you call into any other contracts virtually, you know what those contracts are and what they do.



## Related content
Learn more about:
* [Writing flows]({{< relref "../enterprise/flow-state-machines.md" >}})
* [Contracts]({{< relref "../enterprise/cordapps/api-contracts.md" >}})
