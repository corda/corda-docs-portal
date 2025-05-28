---
date: '2024-04-09'
title: "Examples"
menu:
  corda5-tools:
    weight: 4000
    identifier: contract-testing-examples
    parent: contract-testing
---
# Examples

## No Service Injection

This example shows how to create a very simple state and a corresponding contract. The example creates an issuable state that only has a single command called `Issue`. The issuance contract validates the following:

* The transaction contains exactly one command of type `SampleCommand`.
* The transaction does not have any input states.
* The transaction has output states.
* The output states are all of type `SampleState`.

{{< note >}}
This is a basic example for illustration purposes only, and not production-ready code. The state and contract code is written in Kotlin.
{{< /note >}}

The following shows the example state code:

```kotlin
@BelongsToContract(SampleContract::class)
class SampleState( private val participants : List<PublicKey>, val value: Int, val owner: PublicKey ) : ContractState {
    override fun getParticipants(): List<PublicKey> {
        return participants
    }
}
```

The following shows the example contract code:

```kotlin
class SampleContract : Contract {
    override fun verify(transaction: UtxoLedgerTransaction) {
        val command = transaction.commands.singleOrNull {
            it is SampleCommand
        }
        requireNotNull(command){
            "Transactions must have exactly one command of type SampleCommand."
        }
        when (command) {
            is SampleCommand.Issue -> runIssueVerification(transaction)
        }
    }

    private fun runIssueVerification(transaction: UtxoLedgerTransaction){
        require(transaction.inputStateRefs.isEmpty()) {
            "Issuance can't have inputs"
        }
        require(transaction.outputContractStates.isNotEmpty()) {
            "Issuance must have outputs"
        }
        require(transaction.outputContractStates.all {
            it is SampleState
        }){
            "Must only issue sample states"
        }
    }
}

sealed class SampleCommand : Command {
    class Issue : SampleCommand()
}
```

### Happy Path Test

The following happy path test case creates a transaction with a single output state of type `SampleState` and command `SampleCommand.Issue`. According to our contract, this transaction should pass our contract verification.

{{< tabs >}}
{{% tab name="Java" %}}
```java
@Test
public void TestSampleContractIssuanceHappyPath(){
    UtxoSignedTransaction issueTransaction = getLedgerService()
            .createTransactionBuilder()
            .addOutputState(new SampleState(List.of(aliceKey), 10, aliceKey))
            .addSignatories(aliceKey)
            .addCommand(new SampleCommand.Issue())
            .toSignedTransaction();
    assertVerifies(issueTransaction);
}
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```kotlin
@Test
fun `test sample contract issuance happy path`(){
    val issueTransaction = buildTransaction {
        addOutputState(SampleState(listOf(aliceKey), 10, aliceKey))
        addCommand(SampleCommand.Issue())
        addSignatories(aliceKey)
    }
    assertVerifies(issueTransaction)
}
```
{{% /tab %}}
{{< /tabs >}}

### Negative Path Test

The following negative path test case creates a transaction with a single output state of type `SampleState` and command `SampleCommand.Issue` but the transaction has an input state. According to our contract, this transaction should fail our contract verification because issuance transactions should not have any input states.

{{< tabs >}}
{{% tab name="Java" %}}
```java
@Test
public void TestSampleContractIssuanceFails(){
    UtxoSignedTransaction issueTransaction1 = getLedgerService()
        .createTransactionBuilder()
        .addOutputState(new SampleState(List.of(aliceKey), 10, aliceKey))
        .addSignatories(aliceKey)
        .toSignedTransaction();
        
    UtxoSignedTransaction issueTransaction2 = getLedgerService()
        .createTransactionBuilder()
        .addOutputState(new SampleState(List.of(aliceKey), 10, aliceKey))
        .addInputState(issueTransaction1.getOutputStateAndRefs().get(0).getRef())
        .addSignatories(aliceKey)
        .addCommand(new SampleCommand.Issue())
        .toSignedTransaction();
        
    assertFailsWith(issueTransaction2, "Issuance can't have inputs");
}
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```kotlin
@Test
fun `test sample contract issuance fails`(){
    val issueTransaction1 = buildTransaction {
        addOutputState(SampleState(listOf(aliceKey), 10, aliceKey))
        addSignatories(aliceKey)
    }
    
    val issueTransaction2 = buildTransaction {
        addOutputState(SampleState(listOf(aliceKey), 10, aliceKey))
        addInputState(issueTransaction1.getOutputStateAndRefs().get(0).getRef())
        addSignatories(aliceKey)
        addCommand(new SampleCommand.Issue())
    }
    
    assertFailsWith(issueTransaction2, "Issuance can't have inputs")
}
```
{{% /tab %}}
{{< /tabs >}}

## With Service Injection

This example uses the same state as the [example with no service injection](#no-service-injection) but changes the contract to have an injectable service and an extra verification based on that service. In this example, we check the default digest algorithm that the `DigestService` returns. The rest of the contract code remains the same:

```kotlin
class SampleContract : Contract {

    @CordaInject
    lateinit var digestService: DigestService

    override fun verify(transaction: UtxoLedgerTransaction) {
        
        val defaultAlgo = digestService.defaultDigestAlgorithm()
        require(defaultAlgo == DigestAlgorithmName.SHA2_256D) {
            "Default digest algorithm must be \"SHA2_256D\"."
        }
        // Rest of the verification logic is the same as in the above example
        ...
    }
}
```

{{< note >}}
This is a basic example for illustration purposes only, and not production-ready code. The state and contract code is written in Kotlin.
{{< /note >}}

### Happy Path Test

The following happy path test defines a class-level mock of the `DigestService` so that the happy path test cases pass without having to pass in the mock service to the assert call each time.

First, create two mocks, one valid and one invalid:

{{< tabs >}}
{{% tab name="Java" %}}
```java
@BeforeAll
public static void setup() {
    // Default happy path mock
    when(digestService.defaultDigestAlgorithm()).thenReturn(DigestAlgorithmName.SHA2_256D);
    
    // Invalid mock
    when(invalidDigestService.defaultDigestAlgorithm()).thenReturn(DigestAlgorithmName.SHA2_384);
}
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```kotlin
// Default happy path mock
private val digestService = mock<DigestService> {
    on { defaultDigestAlgorithm() } doReturn DigestAlgorithmName.SHA2_256D
}

// Invalid mock
private val invalidDigestService = mock<DigestService> {
    on { defaultDigestAlgorithm() } doReturn DigestAlgorithmName.SHA2_384
}
```
{{% /tab %}}
{{< /tabs >}}

Next, define the class-level mock services:

{{< tabs >}}
{{% tab name="Java" %}}
```java
@NotNull
@Override
protected final Map<Class<?>, Object> classLevelMockServices() {
    return Map.of(DigestService.class, digestService);
}
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```kotlin
override fun classLevelMockServices() = mapOf(
    DigestService::class.java to digestService
)
```
{{% /tab %}}
{{< /tabs >}}

The following shows the happy path tests:

{{< tabs >}}
{{% tab name="Java" %}}
```java
@Test
public void TestSampleContractIssuanceHappyPath(){
    UtxoSignedTransaction issueTransaction = getLedgerService()
            .createTransactionBuilder()
            .addOutputState(new SampleState(List.of(aliceKey), 10, aliceKey))
            .addSignatories(aliceKey)
            .addCommand(new SampleCommand.Issue())
            .toSignedTransaction();
    assertVerifies(issueTransaction);
}
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```kotlin
@Test
fun `test sample contract issuance happy path`(){
    val issueTransaction = buildTransaction {
        addOutputState(SampleState(listOf(aliceKey), 10, aliceKey))
        addCommand(SampleCommand.Issue())
        addSignatories(aliceKey)
    }
    assertVerifies(issueTransaction)
}
```
{{% /tab %}}
{{< /tabs >}}

### Negative Path Test

The negative path test cases explicitly pass in the invalid service mock to the assertion call. This overwrites the class-level mock.

{{< tabs >}}
{{% tab name="Java" %}}
```java
@Test
public void TestSampleContractWithInjectionInvalidDigestServiceInjected() {
    UtxoSignedTransaction issueTransaction = getLedgerService()
            .createTransactionBuilder()
            .addCommand(new SampleCommand.Issue())
            .addOutputState(new SampleStateWithInjection(List.of(aliceKey)))
            .setNotary(notaryName)
            .setTimeWindowUntil(Instant.now().plus(Duration.ofSeconds(60)))
            .toSignedTransaction();
            
    assertFailsWith(
            issueTransaction,
            "Default digest algorithm must be \"SHA2_256D\".",
            Map.of(DigestService.class, invalidDigestService)
    );
}
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```kotlin
@Test
fun `test sample contract with injection when digest service returns an invalid default algorithm`() {
    val issueTransaction = buildTransaction {
        addOutputState(SampleStateWithInjection(listOf(aliceKey)))
        addCommand(SampleCommand.Issue())
        addSignatories(aliceKey)
    }
    assertFailsWith(
        issueTransaction,
        "Default digest algorithm must be \"SHA2_256D\".",
        mapOf(DigestService::class.java to invalidDigestService)
    )
}
```
{{% /tab %}}
{{< /tabs >}}
