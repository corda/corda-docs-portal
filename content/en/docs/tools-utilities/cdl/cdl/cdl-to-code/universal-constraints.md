---
title: Universal constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-universal-constraints"
    weight: 50

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# Universal Constraints

Universal Constraints are probably the most straight forward type of constraint, they apply to all states irrespective of what `status` they are in. The approach taken here is to take all the Primary states, then apply all the tests to each state:

AgreementContract.kt:

{{< tabs name="universal constraints" >}}
{{% tab name="kotlin" %}}
```kotlin
    fun verifyUniversalConstraints(tx: LedgerTransaction){

        val allStates = tx.inputsOfType<AgreementState>() + tx.outputsOfType<AgreementState>()

        for (s in allStates) {
            requireThat {
                "The buyer and seller must be different Parties." using (s.buyer != s.seller)
                "The proposer must be either the buyer or the seller." using (listOf(s.buyer, s.seller).contains(s.proposer))
                "The consenter must be either the buyer or the seller." using (listOf(s.buyer, s.seller).contains(s.consenter))
                "The consenter and proposer must be different Parties." using (s.consenter != s.proposer)
            }
        }
    }
```
{{% /tab %}}
{{< /tabs >}}
