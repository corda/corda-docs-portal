---
date: '2021-09-07'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    weight: 9400
section_menu: corda-5-dev-preview
title: Testing contracts using the Ledger DSL
expiryDate: '2022-09-28'
---

The Ledger DSL makes it easy to write unit tests that test your contract code. It provides this via the `TransactionDSL` within the `ledger-dsl` artifact.

Using this DSL helps you form "mock" transactions, complete with inputs, outputs, and attachments. After building a transaction, you can verify that the contract code executed by `TransactionBuilder.verify` and `LedgerTransaction.verify` does what you intended it to do. This verification tells you if the transaction works as expected.

## Testing with Ledger DSL vs Corda CLI

The feedback time when using the DSL is much quicker than using the `corda-cli` to test your contract code. It removes the need to write any test flows and RPC client code to trigger these flows by fully removing the Corda node from the equation. You create your transaction within a `TransactionDSL` block, verify it, and then check the outcome. The tests themselves should execute extremely quickly as there is no requirement for a Corda node, and a low number of components contained within the DSL.

## Get the Ledger DSL from Mavern Central

You can download the Ledger DSL for Corda 5 Developer Preview here:

https://repo1.maven.org/maven2/net/corda/corda-ledger-dsl/

## Include the Ledger DSL in your project

To use the Ledger DSL in your project, include the following dependency:

```groovy
testImplementation "net.corda:corda-ledger-dsl:$cordaVersion"
```

## Build a transaction using the `TransactionDSL`

There are two different functions that provide access to a `TransactionDSL` instance, one for Kotlin users and another for Java users:

- `net.corda.testing.ledger.dsl.transactions.TransactionDSL.Companion.transaction` for convenient Kotlin usage.
- `net.corda.testing.ledger.dsl.transactions.transaction` for convenient Java usage (accessed via `TransactionJavaDSL.transaction`).

Calling one of these functions instantiates a `TransactionDSL` that you can access within the function/lambda block of the `transaction` function. Inside this block, you have access to `TransactionDSL`'s methods, which allow you to construct your transaction.

Below is an example of building a transaction using the DSL:

{{< note >}}

We use Mockito to create mock party instances.

{{< /note >}}

**Kotlin:**

  ```kotlin
  private val notary: Party = mock()

  transaction(notary) {
      input(MyState(UniqueIdentifier(), listOf(alice), "input 1"), notary)
      reference(MyState(UniqueIdentifier(), listOf(alice), "reference 1"), notary)
      output(MyState(UniqueIdentifier(), listOf(alice), "output 1"), notary)
      output(MyState(UniqueIdentifier(), listOf(alice), "output 2"), notary)
  }
  ```

  > `this` within the scope of the block above is the `TransactionDSL` instance.

**Java:**

  ```java
  private final Party notary = mock(Party.class);

  transaction(notary, dsl -> {
      dsl.input(new MyState(new UniqueIdentifier(), List.of(alice), "input 1"), notary);
      dsl.reference(new MyState(new UniqueIdentifier(), List.of(alice), "reference 1"), notary);
      dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 1"), notary);
      dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 2"), notary);
  }
  ```

## Build methods available to `TransactionDSL`

The `TransactionDSL` provides overloads of a number of its methods that allow you to decide how you want to build your test transactions. These include:

* `input` - adds an input state.
* `reference` - adds a reference state.
* `output` - adds an output state.
* `attachment` - adds an attachment.
* `command` - adds a command.
* `timeWindow` - adds a time window.


The following methods require further explanation:

* `input`
* `reference`
* `attachment`

Each has more than one approach or 'flavor' for use, described in the following sections.

### `input`

There are 3 different flavors of this method, explained with the snippets below:

  * Creates a new `StateAndRef` with a random transaction id and adds it to the transaction. This is the easiest way to add a new input for testing:

**Kotlin**

```kotlin
input(MyState(UniqueIdentifier(), listOf(alice), "input 1"), notary)
```

**Java**

```java
dsl.input(new MyState(new UniqueIdentifier(), List.of(alice), "input 1"), notary);
```

* Creates a new `StateAndRef` with the passed-in transaction id (`txId`) and adds it to the transaction. This is useful if your contract verification validates any transaction ids.

**Kotlin**

```kotlin
input(MyState(UniqueIdentifier(), listOf(alice), "input 1"), notary, txId)
```

**Java**

```java
dsl.input(new MyState(new UniqueIdentifier(), List.of(alice), "input 1"), notary, txId);
```

* Adds the passed in `StateAndRef` to the transaction. This `StateAndRef` could come from another transaction or could be built manually. This method matches `TransactionBuilder.addInputState` and allows you to write code that matches your production code more closely.

**Kotlin**

```kotlin
input(stateAndRef)
```

**Java**

```java
dsl.input(stateAndRef);
```

### `reference`

There are 3 different flavors of this method, explained alongside the snippets below:

* Creates a new `StateAndRef` with a random transaction id and adds it to the transaction. This is the easiest way to add a new reference for testing.

**Kotlin**

```kotlin
reference(MyState(UniqueIdentifier(), listOf(alice), "input 1"), notary)
```

**Java**

```java
dsl.reference(new MyState(new UniqueIdentifier(), List.of(alice), "input 1"), notary);
```

* Creates a new `StateAndRef` with the passed-in transaction id (`txId`) and adds it to the transaction. This is useful if your contract verification validates any transaction ids.

**Kotlin**

```kotlin
reference(MyState(UniqueIdentifier(), listOf(alice), "input 1"), notary, txId)
```

**Java**

```java
dsl.reference(new MyState(new UniqueIdentifier(), List.of(alice), "input 1"), notary, txId);
```

* Adds the passed-in `StateAndRef` to the transaction. This `StateAndRef` could come from another transaction or could be built manually. This method matches `TransactionBuilder.addReferenceState` and allows you to write code that matches your production code more closely.

**Kotlin**

```kotlin
reference(stateAndRef)
```

**Java**

```java
dsl.reference(stateAndRef);
```

### `attachment`

There are 2 overloads of this method, explained alongside the snippets below:

* Creates an attachment that reads the contents of a file found in the `resource` directory when accessed. This is the simplest version to use as you must provide the name of the file and nothing else.

**Kotlin**

```kotlin
attachment("important-data.csv")
```

**Java**

```java
dsl.attachment("important-data.csv");
```

*Accepts a mock `Attachment` instance that you can configure as desired.

**Kotlin**

```kotlin
val mockAttachment: Attachment = mock()
// mocking of attachment methods
attachment(mockAttachment)
```

**Java**

```java
Attachment mockAttachment = mock(Attachment.class);
// mocking of attachment methods
attachment(mockAttachment)
```

{{< note >}}
`Attachment.open` returns an `InputStream` representing a ZIP file. You should mock its functionality to reflect this, otherwise it will not give an accurate comparison to running your contracts in production.
{{< /note >}}

## Test your contract code using the `TransactionDSL`

`TransactionDSL` provides two methods that test your contract code:

- `verifies` - Executes `LedgerTransaction.verify` and expects it to succeed, throwing any errors caused by verification to the caller.
- `fails` - Executes `LedgerTransaction.verify` and expects it to fail. You are able to specify both the expected exception and message to support your testing.

An example using `verifies`:

{{< note >}}

We use Mockito to create mock party instances.

{{< /note >}}

**Kotlin**

```kotlin
private val notary: Party = mock()

transaction(notary) {
  input(MyState(UniqueIdentifier(), listOf(alice), "input 1"), notary)
  reference(MyState(UniqueIdentifier(), listOf(alice), "reference 1"), notary)
  output(MyState(UniqueIdentifier(), listOf(alice), "output 1"), notary)
  output(MyState(UniqueIdentifier(), listOf(alice), "output 2"), notary)

  verifies()
}
```

**Java**

```java
private final Party notary = mock(Party.class);

transaction(notary, dsl -> {
    dsl.input(new MyState(new UniqueIdentifier(), List.of(alice), "input 1"), notary);
    dsl.reference(new MyState(new UniqueIdentifier(), List.of(alice), "reference 1"), notary);
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 1"), notary);
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 2"), notary);

    dsl.verifies();
}
```

An example using `fails`:

**Kotlin**

```kotlin
transaction(notary) {
    input(MyState(UniqueIdentifier(), listOf(alice), "input 1"), notary)
    reference(MyState(UniqueIdentifier(), listOf(alice), "reference 1"), notary)
    output(MyState(UniqueIdentifier(), listOf(alice), "output 1"), notary)
    output(MyState(UniqueIdentifier(), listOf(alice), "output 2"), notary)

    fails<IllegalStateException>("Should have only one output state")
}
```

**Java**

```java
transaction(notary, dsl -> {
    dsl.input(new MyState(new UniqueIdentifier(), List.of(alice), "input 1"), notary);
    dsl.reference(new MyState(new UniqueIdentifier(), List.of(alice), "reference 1"), notary);
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 1"), notary);
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 2"), notary);

    dsl.fails(IllegalStateException.class, "Should have only one output state");
}
```

## Test workflows by chaining transactions together

Each `transaction` block returns the `LedgerTransaction` created by it. This allows you to store it within a variable and access it in further `transaction` blocks. Combining this with the `input` and `reference` methods that allow you to pass in `StateAndRef`s, you can model workflows that can closer resemble your production.

An example of chaining `transaction` blocks is shown below:

**Kotlin**

```kotlin
val transaction1 = transaction(notary) {
    output(MyState(UniqueIdentifier(), listOf(alice), "output 1"), notary)
    output(MyState(UniqueIdentifier(), listOf(alice), "output 2"), notary)

    verifies()
}
val transaction2 = transaction(notary) {
    input(transaction1.outputs[0])
    output(MyState(UniqueIdentifier(), listOf(alice), "output 3"), notary)
    output(MyState(UniqueIdentifier(), listOf(alice), "output 4"), notary)

    verifies()
}

transaction(notary) {
    input(transaction1.outputs[1])
    input(transaction2.outputs[0])
    input(transaction2.outputs[1])
    output(MyState(UniqueIdentifier(), listOf(alice), "output 5"), notary)

    fails<IllegalStateException>()
}
```

**Java**

```java
LedgerTransaction transaction1 = transaction(notary, dsl -> {
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 1"), notary);
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 2"), notary);

    dsl.verifies();
});

LedgerTransaction transaction2 = transaction(notary, dsl -> {
    dsl.input(transaction1.getOutputs().get(0));
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 3"), notary);
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 4"), notary);

    dsl.verifies();
});

transaction(notary, dsl -> {
    dsl.input(transaction1.getOutputs().get(1));
    dsl.input(transaction2.getOutputs().get(0));
    dsl.input(transaction2.getOutputs().get(1));
    dsl.output(new MyState(new UniqueIdentifier(), List.of(alice), "output 5"), notary);

    dsl.fails(IllegalStateException.class);
});
```
