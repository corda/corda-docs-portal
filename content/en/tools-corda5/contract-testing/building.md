---
date: '2024-04-09'
title: "Building and Verifying Transactions"
menu:
  corda5-tools:
    weight: 3000
    identifier: contract-testing-building
    parent: contract-testing
---
# Building and Verifying Transactions

## Building Transactions

Testing your contracts requires transactions. Building a test transaction is similar to a real-world CorDapp. The following sections contain example chains of function calls:

* [Java Transactions](#java-transactions)
* [Kotlin Transactions](#kotlin-transactions)

For more information, see the full [Transaction Builder API documentation](../../en/api-ref/corda/{{<latest-c5-version>}}/net/corda/v5/ledger/utxo/transaction/UtxoTransactionBuilder.html).

### Java Transactions

In Java, you must explicitly get the UTXO Ledger Service and create a transaction builder:

```java
UtxoSignedTransaction issueTransaction = getLedgerService()
                .createTransactionBuilder()
                .addCommand(new SampleCommand.Issue())
                .addOutputState(new SampleState(List.of(aliceKey), 10, aliceKey))
                .setNotary(notaryName)
                .setTimeWindowUntil(Instant.now().plus(Duration.ofSeconds(60)))
                .addSignatories(aliceKey)
                .toSignedTransaction();
```

### Kotlin Transactions

In Kotlin, the transaction building process becomes simpler using the Kotlin DSL:

```kotlin
val issueTransaction = buildTransaction {
    addCommand(new SampleCommand.Issue())
    addOutputState(new SampleState(List.of(aliceKey), 10, aliceKey))
    setNotary(notaryName)
    setTimeWindowUntil(Instant.now().plus(Duration.ofSeconds(60)))
    addSignatories(aliceKey)
}
```

## Verifying Transactions

Once you have built your transaction, you can verify it by calling one of the following assertion functions:

* `assertVerifies` — use if you are expecting your test to pass the contract validation.
* `assertFailsWith` — use if you are expecting your test to fail contract validation with an exception message exactly matching the provided string.
* `assertFailsWithMessageContaining` — use if you are expecting your test to fail contract validation with an error message containing the provided string.