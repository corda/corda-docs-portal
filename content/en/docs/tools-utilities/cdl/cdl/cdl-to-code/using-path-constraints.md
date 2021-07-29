---
title: Using Path constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-using-path-constraints"
    weight: 120

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# Using Path Constraints

The classes for `Paths` and `PathConstraints` are all provided in the `ContractUtlis.kt` file, this means that the verifyPathConstraints() function is actually very simple to write:

1. Use `ContractUtlis` to extract the Path from the transaction being verified.

2. Create `allowedPaths` which uses a when statement to map the input status to the PathConstraints that should be applied for that status.

3. You now have a single `requireThat` statement that passes the `txPath` and the `allowedPaths` to the `verifyPath()` helper function in `ContractUtils` that returns true if the path is allowed and false if it is not.

ContractUtils.kt:

{{< tabs name="path constraint usage" >}}
{{% tab name="kotlin" %}}
```kotlin
    fun <T: StatusState> verifyPathConstraints(tx: LedgerTransaction, primaryStateClass: Class<T>){

        val commandValue = tx.commands.requireSingleCommand<AgreementContract.Commands>().value    // get the command

        val txPath = getPath(tx, primaryStateClass, commandValue)       // call the getPath() utility function to get the Path of the transaction

        val inputStatus = requireSingleInputStatus(tx, primaryStateClass)       // get the Primary state status

        val allowedPaths: List<PathConstraint<T>> = when (inputStatus){        // populate the when clause mapping: statuses -> allowed constraints
            null -> listOf(
                    PathConstraint(Commands.Propose(), PROPOSED, MultiplicityConstraint(0))
            )
            PROPOSED -> listOf(
                    PathConstraint(Commands.Reject(), REJECTED),
                    PathConstraint(Commands.Agree(), AGREED)
            )
            REJECTED -> listOf(
                    PathConstraint(Commands.Repropose(), PROPOSED)
            )
            AGREED -> listOf(
                    PathConstraint(Commands.Complete(), null, outputMultiplicityConstraint = MultiplicityConstraint(0))
            )
            else -> listOf()
        }

        requireThat {
            "txPath must be allowed by PathConstraints for inputStatus $inputStatus." using verifyPath(txPath, allowedPaths) // call the utility function to check the paths
        }
    }
```
{{% /tab %}}
{{< /tabs >}}

Because a lot of the heavy lifting has been moved to the `ContractUtils.kt`, this pattern can be replicated for other Smart Contracts by substituting in the specific statuses and the `PathConstraints`.
