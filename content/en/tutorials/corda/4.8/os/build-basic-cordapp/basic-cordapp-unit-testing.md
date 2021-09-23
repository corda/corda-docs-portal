---
aliases:
- /docs/corda-os/4.8/tutorial-test-dsl.html
- /docs/platform/corda/4.8/os/tutorial-test-dsl.html
- /docs/corda-os/4.8/flow-testing.html
- /docs/platform/corda/4.8/os/flow-testing.html
date: '2021-09-23'
section_menu: tutorials
menu:
  tutorials:
    identifier: corda-os-4-8-tutorial-basic-cordapp-unit-test
    parent: corda-os-4-8-tutorial-basic-cordapp-intro
    weight: 1070
tags:
- tutorial
- cordapp
title: Write unit tests
---

This tutorial guides you through writing unit tests for the states, contracts, and flows in your CorDapp. This allows you to test these elements of your CorDapp individually without dependency on the other elements.

You will be creating these unit tests in these directories:

* State tests - `contracts/src/test/java/com/tutorial/contracts`
* Contract tests - `contracts/src/test/java/com/tutorial/contracts`
* Flow tests - `workflows/src/test/java/com/tutorial/`

## Learning objectives

After you've completed this tutorial, you will be able to write state, contract, and flow unit tests for your CorDapp.

## Write a state test

Writing a state test for your CorDapp does not require Corda-specific knowledge. If you know how to write unit tests in Java, you can write a state test.

If you are unfamiliar with writing unit tests in Java, follow these steps:

1. Add a file called `StateTests`.
2. Add the `StateTests` public class. 

## Write a contract test

## Write a flow test

## Next steps

Now that you know how to write unit tests, learn how to [run your CorDapp](XXX) then write [Integration tests](../supplmentary-tutorials/tutorial-integration-testing.md).
