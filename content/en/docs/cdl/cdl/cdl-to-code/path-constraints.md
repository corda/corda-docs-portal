---
title: Path constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-path-constraints"
    weight: 110

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# Path Constraints

You can use `PathConstraints` to restrict the `Path` that is allowed in a transaction. The smart contract defines a set of `PathConstraints` for each Primary state status, for example when in status X you can follow `PathConstraint` A or B, but when you are in state Y you can only follow `PathConstraint` C.

In order to pass verification, the Path in the transaction must comply with at least one of the allowed `PathConstraints` for the `status` of the Primary input state.

PathConstraints are implemented as follows:

ContractUtils.kt:

{{< tabs name="path constraints" >}}
{{% tab name="kotlin" %}}
```kotlin

class PathConstraint<T: StatusState>(val command: CommandData,
                                     val outputStatus: Status?,
                                     val inputMultiplicityConstraint: MultiplicityConstraint = MultiplicityConstraint(),
                                     val outputMultiplicityConstraint: MultiplicityConstraint = MultiplicityConstraint(),
                                     val additionalStatesConstraints: Set<AdditionalStatesConstraint> =  setOf()){

    infix fun allows(p: Path<T>): Boolean { ... }

    infix fun doesNotAllow(p: Path<T>): Boolean = !this.allows(p)

    private fun additionalStatesCheck(constraints: Set<AdditionalStatesConstraint>, additionalStates: Set<AdditionalStates>) :Boolean{ ... }
}

```
{{% /tab %}}
{{< /tabs >}}

Where:

* `command` is the class of the command required.
* `outputStatus` is the outputStatus of the Primary state that is required.
* `inputMultiplicityConstraint` defines the range of number of inputs of Primary type that is required.
* `outputMultiplicityConstraint` defines the range of number of outputs of Primary type that is required.
* `additionalStatesConstraint` defines which additional states must be present in the transaction.

A Path in a transaction will only be allowed by the PathConstraint if it passes all these requirements.

`additionalStatesConstraint` are implemented as follows:

ContractUtils.kt:

{{< tabs name="additional states constraints" >}}
{{% tab name="kotlin" %}}
```kotlin
class AdditionalStatesConstraint(val type: AdditionalStatesType ,
                                 val statesClass: Class<out ContractState>,
                                 val requiredNumberOfStates: MultiplicityConstraint = MultiplicityConstraint()) {

    infix fun isSatisfiedBy(additionalStates: AdditionalStates ):Boolean {...}

    infix fun isNotSatisfiedBy (additionalStates: AdditionalStates): Boolean = !isSatisfiedBy(additionalStates)
}

```
{{% /tab %}}
{{< /tabs >}}

Where:

* `type` is `INPUT`, `OUTPUT` or `REFERENCE`.
* `statesClass` is the required type of the additional states.
* `requiredNumberOfStates` defines how many AdditionalStates of this type are allowed using a `MultiplicityConstraint`.

MultiplicityConstraint are defined as follows:

ContractUtils.kt:

{{< tabs name="multiplicity constraints" >}}
{{% tab name="kotlin" %}}
```kotlin
class MultiplicityConstraint(val from: Int = 1,
                             val bounded: Boolean = true,
                             val upperBound: Int = from){

    infix fun allows(numberOfStates: Int): Boolean { ... }

    infix fun doesNotAllow(numberOfStates: Int): Boolean = !this.allows(numberOfStates)
}

```
{{% /tab %}}
{{< /tabs >}}

Where:

* `from` is the minimum number of states.
* `bounded` specifies if there is an upper limit.
* `upperbound` specifies the upper bound, which is only applied if bounded is true.

Note, the structure above allows for quite complex definition of what is allowed, in most cases these won't be needed. To simplify the use of PathConstraints most properties are defaulted. So for example you can specify a Path constraint simply as:

{{< tabs name="path constraint simple" >}}
{{% tab name="kotlin" %}}
```kotlin
PathConstraint(Commands.Reject(), REJECTED)

```
{{% /tab %}}
{{< /tabs >}}

Which would default to:

* 1 Input of Primary State type.
* 1 output Primary State type.
* No additional states required.

Or they could get much more complicated as in this example from the `ContractUtils` test scripts:

{{< tabs name="path constraint complex" >}}
{{% tab name="kotlin" %}}
```kotlin
PathConstraint(Commands.Command2(), TestState2A.TestStatus.STATUSA2, additionalStatesConstraints = setOf(
        AdditionalStatesConstraint(AdditionalStatesType.INPUT, TestState2B::class.java, MultiplicityConstraint(2, false)),
        AdditionalStatesConstraint(AdditionalStatesType.REFERENCE, TestState2C::class.java),
        AdditionalStatesConstraint(AdditionalStatesType.OUTPUT, TestState2D::class.java)
))
```
{{% /tab %}}
{{< /tabs >}}
