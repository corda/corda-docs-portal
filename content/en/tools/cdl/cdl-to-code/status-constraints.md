---
title: Status constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-status-constraints"
    weight: 60

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# Status Constraints

To verify the Status constraints, you must obtain all of the Primary states (i.e. the `AgreementStates`). You can then apply a different set of tests based on the `status` of the `AgreementState` in question:


AgreementContract.kt:

{{< tabs name="status constraints" >}}
{{% tab name="kotlin" %}}
```kotlin
    fun verifyStatusConstraints(tx: LedgerTransaction){
        val allStates = tx.inputsOfType<AgreementState>() + tx.outputsOfType<AgreementState>()

        // Note, in kotlin non-nullable properties must be populated, hence only need to check the nullable properties of the AgreementState
        for (s in allStates) {

            when(s.status){
                PROPOSED -> {
                    requireThat {
                        "When status is Proposed rejectionReason must be null." using (s.rejectionReason == null)
                        "When status is Rejected rejectedBy must be null." using (s.rejectedBy == null)
                    }
                }
                REJECTED -> {
                    requireThat {
                        "When status is Rejected rejectionReason must not be null." using (s.rejectionReason != null)
                        "When status is Rejected rejectedBy must not be null." using (s.rejectedBy != null)
                        "When the Status is Rejected rejectedBy must be the buyer or seller." using (listOf(s.buyer, s.seller).contains(s.rejectedBy))
                    }
                }
                AGREED -> {}
            }
        }
    }
```
{{% /tab %}}
{{< /tabs >}}
