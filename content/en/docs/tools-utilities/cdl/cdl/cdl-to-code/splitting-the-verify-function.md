---
title: Splitting the verify function
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-spliting-the-verify-function"
    weight: 40

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# Splitting the Verify Function

As smart contracts become more complicated, the risk of missing some important control grows. To reduce this risk, the smart contract verification is split up into sub-verify functions which each deal with one of the types of constraints defined in CDL Smart Contract view.

The exception to this is that the blue Flow constraints are not implemented in the Contract and are more like notes on what the Flows should be doing.


AgreementContract.kt:

{{< tabs name="split the verify" >}}
{{% tab name="kotlin" %}}
```kotlin
    override fun verify(tx: LedgerTransaction) {

        verifyPathConstraints(tx, AgreementState::class.java)
        verifyUniversalConstraints(tx)
        verifyStatusConstraints(tx)
        verifyLinearIDConstraints(tx)
        verifySigningConstraints(tx)
        verifyCommandConstraints(tx)
    }

```
{{% /tab %}}
{{< /tabs >}}

Later, you may notice that by splitting the verification into the sub-verify functions there is some duplication, eg multiple switch (`when` in Kotlin) statements on `command.value`. The principle is that it is better to have some duplication if it allows better clarity and structure of the smart contract because this reduces the risk of making mistakes.

For all the sub-verify functions passed in the `LedgerTransaction`, this is so each sub-verify has access to the whole resolved transaction. For `verifyPathConstraints()` you also need to pass in the class of the `AgreementState`.

The following sections consider the implementation of each constraint in turn.
