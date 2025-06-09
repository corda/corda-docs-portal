---
date: '2024-04-09'
title: "Importing the Framework"
menu:
  corda5-tools:
    weight: 1000
    identifier: contract-testing-importing
    parent: contract-testing
---
# Importing the Framework

## Adding the Framework as a Dependency

To use the framework with your CorDapp, add the following dependency to the `build.gradle` file:

```gradle
dependencies {
    testImplementation 'com.r3.corda.ledger.utxo:contract-testing:2.0.0'
}
```

If your CorDapp is written in Kotlin, you can also add a Kotlin DSL framework, as follows:
```gradle
dependencies {
    testImplementation 'com.r3.corda.ledger.utxo:contract-testing:2.0.0'
    testImplementation 'com.r3.corda.ledger.utxo:contract-testing-kotlin:2.0.0'
}
```

You can now extend the `ContractTest` interface to create a test class for your smart contracts. Your contract test classes must inherit from the `ContractTest` base class, as follows:

```kotlin
class ExampleIdentifiableContractCreateCommandTests : ContractTest() {
    ...
}
```

## Testing with the Framework

All tests should extend `ContractTest` as a starting point. The `ContractTest` class provides functions to easily write contract tests, the `UTXOLedgerService` and `MockSigningService` classes, and also the following useful test data:

<style>
table th:first-of-type {
    width: 40%;
}
table th:nth-of-type(2) {
    width: 60%;
}
</style>

| X.500 Legal Identities | Public Keys |
| ---------------------- | ----------- |
| aliceName              | aliceKey    |
| bobName                | bobKey      |
| charlieName            | charlieKey  |
| daveName               | daveKey     |
| eveName                | eveKey      |
| bankAName              | bankAKey    |
| bankBName              | bankBKey    |
| notaryName             | notaryKey   |
