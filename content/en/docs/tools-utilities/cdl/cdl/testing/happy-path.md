---
title: Happy path
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: cdl-testing-cdl-code
    identifier: cdl-testing-happy-path
    weight: 10

tags:
- cdl
- cordapp design language
- smart contract testing
---

# Testing the Happy Path

To test the happy path we are going to use the same sequence of transactions as shown in the Ledger Evolution diagram we saw earlier:

{{< figure zoom="../resources/cdl-agreement-ledger-evolution-tx5.png" width="1000" title="Click to zoom image in new tab/window" >}}

We will use the Corda MockNetwork DSL to generate a sequence of transactions representing the transactions in the diagram:

{{< tabs name="happy path tests" >}}
{{% tab name="kotlin" %}}
```kotlin
@Test
    fun `check the happy path`() {

        val linearId = UniqueIdentifier()

        val proposed1 = AgreementState(AgreementStatus.PROPOSED,
                alice.party, bob.party, "One bunch of Bananas", Amount(10, Currency.getInstance("GBP")), alice.party, bob.party, linearId = linearId)
        val rejected = AgreementState(AgreementStatus.REJECTED,
                alice.party, bob.party, "One bunch of Bananas", Amount(10, Currency.getInstance("GBP")), alice.party, bob.party, "Run out of Bananas", bob.party, linearId = linearId)
        val proposed2 = AgreementState(AgreementStatus.PROPOSED,
                alice.party, bob.party, "One bag of grapes", Amount(8, Currency.getInstance("GBP")), bob.party, alice.party, linearId = linearId)
        val agreed = AgreementState(AgreementStatus.AGREED,
                alice.party, bob.party, "One bag of grapes", Amount(8, Currency.getInstance("GBP")), bob.party, alice.party, linearId = linearId)

        ledgerServices.ledger {
            transaction {
                command(alice.publicKey, AgreementContract.Commands.Propose())
                output(AgreementContract.ID, proposed1)
                verifies()
            }
            transaction {
                input(AgreementContract.ID, proposed1)
                command(bob.publicKey, AgreementContract.Commands.Reject())
                output(AgreementContract.ID, rejected)
                verifies()
            }
            transaction {
                input(AgreementContract.ID, rejected)
                command(bob.publicKey, AgreementContract.Commands.Repropose())
                output(AgreementContract.ID, proposed2)
                verifies()
            }
            transaction {
                input(AgreementContract.ID, proposed2)
                command(alice.publicKey, AgreementContract.Commands.Agree())
                output(AgreementContract.ID, agreed)
                verifies()
            }
            transaction {
                input(AgreementContract.ID, agreed)
                command(bob.publicKey, AgreementContract.Commands.Complete())
                verifies()
            }
        }
    }
```
{{% /tab %}}
{{< /tabs >}}

This gives us a base line to work off for the non-happy path tests.
