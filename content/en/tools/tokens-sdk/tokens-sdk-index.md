---
date: '2021-04-24T00:00:00Z'
section_menu: tools
menu:
  tools:
    name: Tokens SDK
    weight: 100
    identifier: tools-tokens-sdk
title: Welcome to Tokens SDK
---

The Tokens SDK provides you with the fastest and easiest way to create tokens that represent any kind of asset on your network. This asset can be anything you want it to be—conceptual or physical, valuable or not. You can create a token to represent something outside the network, or something that only exists on the ledger—such as a Corda-native digital currency.

With the SDK, you can define your token and its attributes, then add functionality to a CorDapp so the token can be issued, moved, and redeemed on a ledger.

## Tokens SDK Documentation

Tokens SDK documentation can be found [here](../../../en/platform/corda/4.10/enterprise/cordapps/token-sdk-introduction.md).

## Upgrading

If you have developed a CorDapp that uses the Tokens SDK 1.1 or 1.2.1, you can upgrade to 1.2.3.

## Compatibility

Versions 1.2.1 and 1.2.3 of the Tokens SDK are compatible with **Corda release version 4.6** and higher.

Version 1.2.4 of the Tokens SDK is compatible with **Corda release version 4.8** and higher.

## Changes in Tokens SDK 1.2.4

Previously, the in-memory token selector would start loading its tokens in parallel to the vault being initialised, which may have resulted in some tokens not being loaded into the selector. This issue has now been resolved.

## Changes in Tokens SDK 1.2.3

In Tokens SDK 1.2.3, the `holder` column in the `fungible_token` and `non_fungible_token` tables is now nullable.

## Changes in Tokens SDK 1.2.2

In 1.2.2, a new [Token Selection]({{< relref "../../../../../../en/platform/corda/4.10/enterprise/cordapps/token-selection.md" >}}) feature allows the exception `InsufficientNotLockedBalanceException` to be thrown when sufficient funds appear to exist for a transaction to take place, but an excess of those funds are soft locked by other in-flight transactions. The warning tells you that there are insufficient funds that have not been soft locked to satisfy the transaction amount.

## Changes in Tokens SDK 1.2.1

The main changes in the Tokens SDK from 1.1 to 1.2.1 are designed to improve application of the SDK for those using a Java code base.

Overview of changes:

* All of the utility methods, subflows and RPC enabled flows have been annotated with @JVMOverloads to ensure the appropriate Java constructors are generated where the source Kotlin constructor contains nullable arguments. This ensures a seamless experience when using the Tokens SDK from a Java code base.
* The `selection` and `money` JAR files have been moved into the `workflows` JAR file.
* Upgraded database interaction for compatibility with Corda 4.6 and Corda Enterprise Edition 4.6.

