---
date: '2023-08-1237'
title: "Contract Testing"
project: corda5-tools
section_menu: corda5-tools
version: tools
menu:
  corda5-tools:
    weight: 1000
---

The Contract Testing library enables {{< tooltip >}}CorDapp{{< /tooltip >}} Developers to test {{< tooltip >}}UTXO{{< /tooltip >}} contracts locally, at an early stage of the development cycle. With this library, you can check that your CorDapp contracts behave as expected before you write the flows.

## Prerequisites

* {{< tooltip >}}CSDE{{< /tooltip >}} — contains Contract Testing library [examples](#examples).
* Contract and state classes

## Importing the Library

To import the library to your CorDapp, add it to your `contracts` `build.gradle` dependencies:
```
testImplementation "com.r3.corda.ledger.utxo:contract-testing:1.0.0-beta”
```

If you are using Kotlin, you can also add the Kotlin DSL:
```
testImplementation "com.r3.corda.ledger.utxo:contract-testing-kotlin:1.0.0-beta”
```

You can now extend the `ContractTest` interface.

## Testing with the Library

All tests should extend `ContractTest` as a starting point. This provides the `ledgerService` and `signingService` and also some useful
test data:

<style>
table th:first-of-type {
    width: 40%;
}
table th:nth-of-type(2) {
    width: 60%;
}
</style>

| X.500 Legal Identities | Public Keys |
|-----------------------|-------------|
| aliceName             | aliceKey    |
| bobName               | bobKey      |
| charlieName           | charlieKey  |
| daveName              | daveKey     |
| eveName               | eveKey      |
| bankAName             | bankAKey    |
| bankBName             | bankBKey    |
| notaryName            | notaryKey   |

### Happy Path Testing

If you expect your test to pass the contract validation, use `assertVerifies`. For example:
```java
@Test
    public void happyPath() {
        UtxoSignedTransaction transaction = getLedgerService()
            .createTransactionBuilder()
            .addInputState(inputState)
            .addOutputState(outputState)
            .addCommand(new MyContract.MyCommand())
            .addSignatories(List.of(bankAKey, bankBKey, notaryKey))
            .toSignedTransaction();
          assertVerifies(transaction);
    }
```

### Negative Path Testing

If you expect the contract validation to reject the transaction, make use of `assertFailsWith`. For example:
```java
@Test
    public void negativePath() {
        UtxoSignedTransaction transaction = getLedgerService()
            .createTransactionBuilder()
            .addInputState(invalidInputState)
            .addOutputState(outputState)
            .addCommand(new MyContract.MyCommand())
            .addSignatories(List.of(bankAKey, bankBKey, notaryKey))
            .toSignedTransaction();
          assertFailsWith(transaction, "Validation message here");
    }
```

## Examples

The CSDE contains Contract Testing examples in the following locations:
* [CSDE-cordapp-template-kotlin repository](https://github.com/corda/CSDE-cordapp-template-kotlin/tree/release/corda-5-0) - `contracts/src/test/kotlin/com/r3/developers`
* [CSDE-cordapp-template-java repository](https://github.com/corda/CSDE-cordapp-template-java/tree/release/corda-5-0) - `contracts/src/test/java/com/r3/developers`

### Apples

The `apples` example tests the `AppleStampContract` and `BasketOfApplesContract` contracts written as part of the [Building Your First CorDapp tutorial]({{< relref "../../platform/corda/5.0/developing-applications/basic-cordapp/contract.md" >}}).

### Chat

The `utxoexample` example tests the `ChatContract` of the [UTXO chat application]({{< relref "../../platform/corda/5.0/developing-applications/getting-started/utxo-ledger-example-cordapp/cordapp-chat/_index.md" >}}) delivered with the CSDE.