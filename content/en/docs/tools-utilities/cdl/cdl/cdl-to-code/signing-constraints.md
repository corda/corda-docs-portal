---
title: Signing constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-signing-constraints"
    weight: 90

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# Signing Constraints

Signing constraints are implement using a switch on the command.

The slight modification to be added to signing constraints in this example is that the check being performed is always of the same form - does the `command.signers` contain the required signer per the CDL diagram?

To make the code more efficient you can define a `checkSigners()` function for which you use a switch on `command.value` to send different arguments based on the CDL required signers for each command.

There is also a similar guard to `verifyLinearIDConstraints()` to ensure there is only one primary input and primary output state, which allows you to simplify the implementation.

AgreementContract.kt:

{{< tabs name="signing constraints" >}}
{{% tab name="kotlin" %}}
```kotlin

    fun verifySigningConstraints(tx: LedgerTransaction){

        // This implementation assumes there is a maximum of one Primary input state and a maximum one Primary output state.
        // For Contracts which assume multiple Primary inputs or Output a different approach will be required

        val command = tx.commands.requireSingleCommand<AgreementContract.Commands>()
        val inputStates = tx.inputsOfType<AgreementState>()
        val outputStates = tx.outputsOfType<AgreementState>()

        // This is a guard which shouldn't be triggered because the Path constraints should have already ensured there is
        // a maximum of one Primary input state and a maximum one Primary output state
        requireThat{
            "when checking signing constraints there should be a maximum of one Primary input state." using (inputStates.size <= 1)
            "When checking signing constraints there should be a maximum of one Primary output state." using (outputStates.size <= 1)
        }

        val inputState = inputStates.singleOrNull()
        val outputState = outputStates.singleOrNull()

        val commandName = command.value::class.java.simpleName

        fun checkSigner(signerDescription: String, signer: Party?){
            requireThat { "When the Command is $commandName the $signerDescription must sign." using (command.signers.contains(signer?.owningKey))}

        }

        when (command.value){
            is Commands.Propose -> {
                checkSigner("output.proposer", outputState?.proposer)   // Can add multiple signing check against each Command
            }
            is Commands.Reject -> {
                checkSigner("output.rejectedBy", outputState?.rejectedBy)
            }
            is Commands.Repropose -> {
                checkSigner("output.proposer", outputState?.proposer)
            }
            is Commands.Agree -> {
                checkSigner("input.consenter", inputState?.consenter )
            }
            is Commands.Complete -> {
                checkSigner("input.seller", inputState?.seller)
            }
        }
    }
```
{{% /tab %}}
{{< /tabs >}}
