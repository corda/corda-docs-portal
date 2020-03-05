+++
date = "2020-01-08T09:59:25Z"
title = "Writing a contract test"
aliases = [ "/releases/4.4/ZZPotential-delete-docs/tutorial-test-dsl.html",]
tags = [ "tutorial", "test", "dsl",]

[menu.corda-enterprise-4-4]
parent = "corda-enterprise-4-4-tutorial"
+++



# Writing a contract test

This tutorial will take you through the steps required to write a contract test using Kotlin and Java.

The testing DSL allows one to define a piece of the ledger with transactions referring to each other, and ways of
            verifying their correctness.


## Setting up the test

Before writing the individual tests, the general test setup must be configured:


{{< tabs name="tabs-1" >}}


{{% tab name="kotlin" %}}
```kotlin
class CommercialPaperTest {
    private val miniCorp = TestIdentity(CordaX500Name("MiniCorp", "London", "GB"))
    private val megaCorp = TestIdentity(CordaX500Name("MegaCorp", "London", "GB"))
    private val ledgerServices = MockServices(listOf("net.corda.finance.schemas"), megaCorp, miniCorp)
    ...
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
public class CommercialPaperTest {
    private TestIdentity megaCorp = new TestIdentity(new CordaX500Name("MegaCorp", "London", "GB"));
    private TestIdentity miniCorp = new TestIdentity(new CordaX500Name("MiniCorp", "London", "GB"));
    MockServices ledgerServices = new MockServices(Arrays.asList("net.corda.finance.schemas"), megaCorp, miniCorp);
    ...
}
```
{{% /tab %}}
{{< /tabs >}}

The `ledgerServices` object will provide configuration to the `ledger` DSL in the individual tests.


## Testing single transactions

We start with the empty ledger:


{{< tabs name="tabs-2" >}}


{{% tab name="kotlin" %}}
```kotlin
class CommercialPaperTest {
    @Test
    fun emptyLedger() {
        ledgerServices.ledger {
            ...
        }
    }
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
public class CommercialPaperTest {
    @Test
    public void emptyLedger() {
        ledger(ledgerServices, l -> {
            ...
            return null;
        });
    }
}
```
{{% /tab %}}
{{< /tabs >}}

The DSL keyword `ledger` takes a closure that can build up several transactions and may verify their overall
                correctness. A ledger is effectively a fresh world with no pre-existing transactions or services within it.

We will start with defining helper function that returns a `CommercialPaper` state:


{{< tabs name="tabs-3" >}}

{{< /tabs >}}

It’s a `CommercialPaper` issued by `MEGA_CORP` with face value of $1000 and maturity date in 7 days.

Let’s add a `CommercialPaper` transaction:


{{< tabs name="tabs-4" >}}


{{% tab name="kotlin" %}}
```kotlin
@Test
fun simpleCPDoesntCompile() {
    val inState = getPaper()
    ledger {
        transaction {
            input(CommercialPaper.CP_PROGRAM_ID) { inState }
        }
    }
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
@Test
public void simpleCPDoesntCompile() {
    ICommercialPaperState inState = getPaper();
    ledger(ledgerServices, l -> {
        l.transaction(tx -> {
            tx.input(inState);
        });
        return Unit.INSTANCE;
    });
}
```
{{% /tab %}}
{{< /tabs >}}

We can add a transaction to the ledger using the `transaction` primitive. The transaction in turn may be defined by
                specifying `input`s, `output`s, `command`s and `attachment`s.

The above `input` call is a bit special; transactions don’t actually contain input states, just references
                to output states of other transactions. Under the hood the above `input` call creates a dummy transaction in the
                ledger (that won’t be verified) which outputs the specified state, and references that from this transaction.

The above code however doesn’t compile:


{{< tabs name="tabs-5" >}}


{{% tab name="kotlin" %}}
```kotlin
Error:(29, 17) Kotlin: Type mismatch: inferred type is Unit but EnforceVerifyOrFail was expected
```
{{% /tab %}}

{{% tab name="java" %}}
```java
Error:(35, 27) java: incompatible types: bad return type in lambda expression missing return value
```
{{% /tab %}}
{{< /tabs >}}

This is deliberate: The DSL forces us to specify either `verifies()` or ``fails with`("some text")` on the
                last line of `transaction`:


{{< tabs name="tabs-6" >}}

{{< /tabs >}}

Let’s take a look at a transaction that fails.


{{< tabs name="tabs-7" >}}

{{< /tabs >}}

When run, that code produces the following error:


{{< tabs name="tabs-8" >}}


{{% tab name="kotlin" %}}
```kotlin
"net.corda.core.contracts.TransactionVerificationException$ContractRejection: java.lang.IllegalArgumentException: Failed requirement: the state is propagated"
```
{{% /tab %}}

{{% tab name="java" %}}
```java
net.corda.core.contracts.TransactionVerificationException$ContractRejection: java.lang.IllegalStateException: the state is propagated
```
{{% /tab %}}
{{< /tabs >}}

The transaction verification failed, because we wanted to move paper but didn’t specify an output - but the state should be propagated.
                However we can specify that this is an intended behaviour by changing `verifies()` to ``fails with`("the state is propagated")`:


{{< tabs name="tabs-9" >}}

{{< /tabs >}}

We can continue to build the transaction until it `verifies`:


{{< tabs name="tabs-10" >}}

{{< /tabs >}}

`output` specifies that we want the input state to be transferred to `ALICE` and `command` adds the
                `Move` command itself, signed by the current owner of the input state, `MEGA_CORP_PUBKEY`.

We constructed a complete signed commercial paper transaction and verified it. Note how we left in the `fails with`
                line - this is fine, the failure will be tested on the partially constructed transaction.

What should we do if we wanted to test what happens when the wrong party signs the transaction? If we simply add a
                `command` it will permanently ruin the transaction… Enter `tweak`:


{{< tabs name="tabs-11" >}}

{{< /tabs >}}

`tweak` creates a local copy of the transaction. This makes possible to locally “ruin” the transaction while not
                modifying the original one, allowing testing of different error conditions.

We now have a neat little test that tests a single transaction. This is already useful, and in fact testing of a single
                transaction in this way is very common. There is even a shorthand top-level `transaction` primitive that creates a
                ledger with a single transaction:


{{< tabs name="tabs-12" >}}

{{< /tabs >}}


## Chaining transactions

Now that we know how to define a single transaction, let’s look at how to define a chain of them:


{{< tabs name="tabs-13" >}}

{{< /tabs >}}

In this example we declare that `ALICE` has $900 but we don’t care where from. For this we can use
                `unverifiedTransaction`. Note how we don’t need to specify `verifies()`.

Notice that we labelled output with `"alice's $900"`, also in transaction named `"Issuance"`
                we labelled a commercial paper with `"paper"`. Now we can subsequently refer to them in other transactions, e.g.
                by `input("alice's $900")` or `"paper".output<ICommercialPaperState>()`.

The last transaction named `"Trade"` exemplifies simple fact of selling the `CommercialPaper` to Alice for her $900,
                $100 less than the face value at 10% interest after only 7 days.

We can also test whole ledger calling `verifies()` and `fails()` on the ledger level.
                To do so let’s create a simple example that uses the same input twice:


{{< tabs name="tabs-14" >}}

{{< /tabs >}}

The transactions `verifies()` individually, however the state was spent twice! That’s why we need the global ledger
                verification (`fails()` at the end). As in previous examples we can use `tweak` to create a local copy of the whole ledger:


{{< tabs name="tabs-15" >}}

{{< /tabs >}}


