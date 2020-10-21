---
title: Command constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-command-constraints"
    weight: 80

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# Command Constraints

Command constraints are implemented using a switch on the command.

This is to ensure that you have good structure in the code so, you will have a `when` case for every possible value of the `command.value`. In the cases of `Propose`, `Repropose` and `Complete` commands, there is no command constraint specified in the CDL.

You can explicitly show there is no check to be done by leaving the case block blank `{}` because it is better to ensure there is a complete set of cases rather than risk missing one out.

AgreementContract.kt:

{{< tabs name="command constraints" >}}
{{% tab name="kotlin" %}}
```kotlin

    fun verifyCommandConstraints(tx: LedgerTransaction){

        val command = tx.commands.requireSingleCommand<AgreementContract.Commands>()

        when (command.value){
            is Commands.Propose -> {
            }
            is Commands.Reject -> {
                // Path Constraints have already checked there is only one input and one output
                val inputState = tx.inputsOfType<AgreementState>().single()
                val outputState = tx.outputsOfType<AgreementState>().single()

                // Note, to check the majority of properties haven't change the code copies the outputstate but sets the changing properties to that of the input state. if all the other properties are the same, the copy should match the input state.
                requireThat {"When the command is Reject no properties can change except status, rejectionReason and rejectedBy." using (outputState.copy(
                        status = inputState.status,
                        rejectionReason = inputState.rejectionReason,
                        rejectedBy = inputState.rejectedBy) == inputState)}
            }
            is Commands.Repropose -> {
            }
            is Commands.Agree -> {
                requireThat {
                    // Path Constraints have already checked there is only one input and one output
                    val inputState = tx.inputsOfType<AgreementState>().single()
                    val outputState = tx.outputsOfType<AgreementState>().single()
                    requireThat {"When the command is Agree no properties can change except status." using (outputState.copy(status = inputState.status) == inputState)}
                }
            }
            is Commands.Complete -> {}
        }
    }

```
{{% /tab %}}
{{< /tabs >}}
