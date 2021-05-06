---
title: Keep it structured
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-contract-to-code-keep-it-structured"
    weight: 10

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---

# Keep It Structured

The CDL Smart Contract view deliberately separates the design into a set of considerations either to do with data structures or constraints over those data structures. You can show this diagrammatically:

{{< figure zoom="../resources/cdl-to-code-smart-contract-to-concerns.png" width="1000" title="Click to zoom image in new tab/window" >}}

To minimise the risks of making mistakes when implementing the smart contract, you should consider each of the considerations separately. Narrowing the focus can give you greater confidence that each consideration is implemented correctly.

In the Agreement example, as implemented in the cdl-example CorDapp, the CDL considerations map to the following code structures:

{{< figure zoom="../resources/cdl-to-code-concerns-to-structures.png" width="650" title="Click to zoom image in new tab/window" >}}

You can see in this diagram that:

* CDL states map to the `AgreementState`.
* `Commands` and the `verify()` functions are implemented in the `AgreementContract`.
* The CDL constraints are implemented in the `verify()` function.
* As the `verify()` function is too complicated to manage in one function, it is broken up in to a series of sub-verify functions each one dealing with a different CDL constraint.
* The verification of Path constraints is more complicated than the other constraints, hence some of this has been moved out of the `verifyPathConstraints()` function and into `ContractUtils.kt`.

For each of the sub-verify functions we will aim for a standard structure to implement that type of constraint. The closer we can get to a standard template with the specific details of the smart contract being akin to configuration, the more reliable the implementation will become.

For example, the code for verifying Status constraints is as follows:

{{< tabs name="status-example" >}}
{{% tab name="kotlin" %}}
```kotlin
fun verifyStatusConstraints(tx: LedgerTransaction){

        val allStates = tx.inputsOfType<AgreementState>() + tx.outputsOfType<AgreementState>()

        for (s in allStates) {
            when(s.status){
                PROPOSED -> {
                    requireThat {
                        "When status is Proposed rejectionReason must be null" using (s.rejectionReason == null)
                        "When status is Rejected rejectedBy must be null" using (s.rejectedBy == null)
                    }
                }
                REJECTED -> {
                    requireThat {
                        "When status is Rejected rejectionReason must not be null" using (s.rejectionReason != null)
                        "When status is Rejected rejectedBy must not be null" using (s.rejectedBy != null)
                        "When the Status is Rejected rejectedBy must be the buyer or seller" using (listOf(s.buyer, s.seller).contains(s.rejectedBy))
                    }
                }
                AGREED -> {}
            }
        }
    }
```
{{% /tab %}}
{{< /tabs >}}

Which can be generalised to be applicable for any CorDapp which uses statuses:

{{< tabs name="generic-status" >}}
{{% tab name="kotlin" %}}
```kotlin
fun verifyStatusConstraints(tx: LedgerTransaction){

        val allStates = tx.inputsOfType<MyState>() + tx.outputsOfType<MyState>()

        for (s in allStates) {
            when(s.status){
                MY_STATUS_1 -> {
                    requireThat {
                        // Checks on states in status MY_STATUS_1
                    }
                }
                MY_STATUS_2 -> {
                    requireThat {
                        // Checks on states in status MY_STATUS_2
                    }
                }
            }
        }
    }
```
{{% /tab %}}
{{< /tabs >}}

The remaining sections will go through the implementation of each CDL consideration.
