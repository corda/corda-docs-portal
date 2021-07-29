---
title: LinearId constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-linearId-constraints"
    weight: 70

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# LinearId Constraints

The implementation of LinearID constraints have a few more complexities.

LinearIDs are used when we want to represent a linear chain of evolving states on the ledger. There is an implicit assumption that to avoid branching of the linear chain there will be at most one primary input state and one primary output state.

Later the Path constraints will explicitly state that cannot be more than one primary input or primary output state. However, we should program defensively, so we add a pre-check that will throw a meaningful error if the transaction has more than one primary input or primary output state.

After the pre-check, we need to identify the situations where it is appropriate to check for matching LinearIds. This will be wherever there is both an primary input state and a primary output state and the Multiplicity is marked as '1: Matched'

From the diagram we can see that occurs for the Reject, Repropose and Agree commands:

{{< figure zoom="../resources/cdl-agreement-smart-contract-full.png" width="1000" title="Click to zoom image in new tab/window" >}}

Hence, we will perform a switch (`when` in Kotlin) on the commands and apply the linear ID check for those commands.


AgreementContract.kt:

{{< tabs name="linearId constraints" >}}
{{% tab name="kotlin" %}}
```kotlin
    fun verifyLinearIDConstraints(tx: LedgerTransaction){

        val command = tx.commands.requireSingleCommand<AgreementContract.Commands>()
        val inputStates = tx.inputsOfType<AgreementState>()
        val outputStates = tx.outputsOfType<AgreementState>()

        // Assume that if using LinearID we want a maximum of one Primary input state and a maximum one Primary output state
        // This is a guard which shouldn't be triggered because the Path constraints should have already ensured there is
        // a maximum of one Primary input state and a maximum one Primary output state
        requireThat{
            "When using LinearStates there should be a maximum of one Primary input state." using (inputStates.size <= 1)
            "When using LinearStates there should be a maximum of one Primary output state." using (outputStates.size <= 1)
        }

        val inputState = inputStates.singleOrNull()
        val outputState = outputStates.singleOrNull()

        val commandName = command.value::class.java.simpleName
        when (command.value){
            is Commands.Reject,
            is Commands.Repropose,
            is Commands.Agree-> {
                requireThat {"When the Command is $commandName the LinearID must not change." using(inputState?.linearId == outputState?.linearId)}
            }
        }
    }
```
{{% /tab %}}
{{< /tabs >}}
