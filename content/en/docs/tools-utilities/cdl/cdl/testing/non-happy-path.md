---
title: Non happy path
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: cdl-testing-cdl-code
    identifier: cdl-testing-non-happy-path
    weight: 20

tags:
- cdl
- cordapp design language
- smart contract testing
---

# Non Happy Path Tests

Once we have the happy path, we can start testing each of the constraints in turn to check they fail when they are meant to fail.

At the end of the testing we want to have confidence we have covered all of the failure conditions specified in the smart contract. There's going to be a lot of tests covering a lot of failure scenarios so we need to keep this very structured.

The approach used in the cdl-example builds up a layered tree structure:

{{< figure zoom="../resources/cdl-testing-structure.png" width="1000" title="Click to zoom image in new tab/window" >}}

We take each constraint in turn, for each constraint we take each of the predicates that drives the constraint's behaviour, then for each predicate value we identify a potential error type, then for each error type the error value.

Then we systematically implement those tests using the Corda MockServices DSL. The code snippet here shows the first Path constraint tests in the tree structure above, the rest of the test follow a similar structure.

AgreementContractTests.kt:

{{< tabs name="happy path tests" >}}
{{% tab name="kotlin" %}}
```kotlin
@Test
    fun `check paths constraints`() {

        val linearId = UniqueIdentifier()
        val proposedState = AgreementState(AgreementStatus.PROPOSED,
                alice.party, bob.party, "Some grapes", Amount(10, Currency.getInstance("GBP")), alice.party, bob.party, linearId = linearId)
        val rejectedState = AgreementState(AgreementStatus.REJECTED,
                alice.party, bob.party, "Some more grapes", Amount(10, Currency.getInstance("GBP")), alice.party, bob.party, "I don't like grapes", alice.party, linearId = linearId)
        val agreedState = AgreementState(AgreementStatus.AGREED,
                alice.party, bob.party, "Some more grapes", Amount(10, Currency.getInstance("GBP")), alice.party, bob.party, linearId = linearId)

        ledgerServices.ledger {

            // From null status
            // Incorrect Statuses
            transaction {
                command(alice.publicKey, AgreementContract.Commands.Propose())
                output(AgreementContract.ID, agreedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus null.")
            }
            transaction {
                command(alice.publicKey, AgreementContract.Commands.Propose())
                output(AgreementContract.ID, rejectedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus null.")
            }
            // Incorrect Commands
            transaction {
                command(alice.publicKey, AgreementContract.Commands.Agree())
                output(AgreementContract.ID, proposedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus null.")
            }
            transaction {
                command(alice.publicKey, AgreementContract.Commands.Reject())
                output(AgreementContract.ID, proposedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus null.")
            }
            transaction {
                command(alice.publicKey, AgreementContract.Commands.Repropose())
                output(AgreementContract.ID, proposedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus null.")
            }
            transaction {
                command(alice.publicKey, AgreementContract.Commands.Complete())
                output(AgreementContract.ID, proposedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus null.")
            }

            // from Proposed state
            // Incorrect Statuses
            transaction {
                input(AgreementContract.ID, proposedState)
                command(alice.publicKey, AgreementContract.Commands.Agree())
                `fails with`("txPath must be allowed by PathConstraints for inputStatus PROPOSED.")
            }
            transaction {
                input(AgreementContract.ID, proposedState)
                command(alice.publicKey, AgreementContract.Commands.Agree())
                output(AgreementContract.ID, proposedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus PROPOSED.")
            }
            transaction {
                input(AgreementContract.ID, proposedState)
                command(alice.publicKey, AgreementContract.Commands.Agree())
                output(AgreementContract.ID, rejectedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus PROPOSED.")
            }
            // Incorrect Commands
            transaction {
                input(AgreementContract.ID, proposedState)
                command(alice.publicKey, AgreementContract.Commands.Propose())
                output(AgreementContract.ID, agreedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus PROPOSED.")
            }
            transaction {
                input(AgreementContract.ID, proposedState)
                command(alice.publicKey, AgreementContract.Commands.Repropose())
                output(AgreementContract.ID, agreedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus PROPOSED.")
            }
            transaction {
                input(AgreementContract.ID, proposedState)
                command(alice.publicKey, AgreementContract.Commands.Complete())
                output(AgreementContract.ID, agreedState)
                `fails with`("txPath must be allowed by PathConstraints for inputStatus PROPOSED.")
            }

            etc ...


```
{{% /tab %}}
{{< /tabs >}}
