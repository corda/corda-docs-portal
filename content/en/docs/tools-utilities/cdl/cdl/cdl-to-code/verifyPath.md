---
title: verifyPath()
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-verify-path"
    weight: 130

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---




# verifyPaths()

In the previous section we described how the `verifyPathConstraints()` function calls the `verifyPath()` function from `ContractUtils`. In this section you can see how `verifyPath()` works. You can also see the implementation of `VerifyPaths` in the [cdl-example](https://github.com/corda/cdl-example) code repo.

This diagram shows an example of an implementation of `VerifyPaths`:

{{< figure zoom="../resources/cdl-contractutils-verifypath-simple.png" width="800" title="Click to zoom image in new tab/window" >}}

From the `LedgerTransaction` you can establish the `Path` in the transaction, as well as the status of the Primary input state. From the status of the Primary input state you can establish the set of allowed `PathConstraints` for the status of that input state. The `verifyPath()` function then takes the Path and checks it against each `PathConstraint`. If it can find a `PathConstraint` which allows the transaction `Path` then it returns `true`, if not, it will return `false` which will cause the `verifyPathConstraints()` function to throw a verification error.

Looking in detail, you can see the properties in `Path` and `PathConstraint` respectively, together with the checks that each `PathConstraint` property applies to its corresponding `Path` property:

{{< figure zoom="../resources/cdl-contractutils-verifypath-with-properties.png" width="800" title="Click to zoom image in new tab/window" >}}


Then, for the full description, you must add in the `additionalStates` checks in which each required `additionStatesConstraint` must be satisfied by at least one of the `additionalStates` in the transaction:

{{< figure zoom="../resources/cdl-contractutils-verifypath-full.png" width="800" title="Click to zoom image in new tab/window" >}}
