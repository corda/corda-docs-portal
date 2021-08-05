---
date: '2021-08-03'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-tutorial-basic-cordapp-state
    parent: corda-os-4-8-tutorial-basic-cordapp-intro
    weight: 1000
tags:
- tutorial
- cordapp
title: Write the states
---

This tutorial guides you through writing the two states you need in your CorDapp: `AppleStamp` and `BasketofApples`. You will be editing the `contracts/src/main/java/com/template/states/TemplateState.java` file in this tutorial.

## Learning objectives

Once you have completed this tutorial, you will know how to create and implement states in a CorDapp.

## Before you start

Before you start following this tutorial, check out:

* [Key concepts: States](key-concepts-states.md)

## Clone the CorDapp template repo

As you did in [Writing a CorDapp using a template](writing-a-cordapp-using-a-template.md), it's a good idea to start writing any CorDapp from a template. This ensures that you have the correct files in place to begin building.

1. Open a terminal window in the directory where you want to download the CorDapp template, and run the following command:

   {{< tabs name="tabs-1" >}}
   {{% tab name="kotlin" %}}
   ```kotlin
   git clone https://github.com/corda/cordapp-template-kotlin.git
   ```
   {{% /tab %}}

   {{% tab name="java" %}}
   ```java
   git clone https://github.com/corda/cordapp-template-java.git
   ```
   {{% /tab %}}

   {{< /tabs >}}

2. Once you have cloned the repository you wish to use, navigate to the correct subdirectory:

   {{< tabs name="tabs-2" >}}
   {{% tab name="kotlin" %}}
   ```kotlin
   cd cordapp-template-kotlin
   ```
   {{% /tab %}}

   {{% tab name="java" %}}
   ```java
   cd cordapp-template-java
   ```
   {{% /tab %}}

   {{< /tabs >}}


3. Once you have successfully cloned the CorDapp template, open the `cordapp-template-kotlin` or `cordapp-template-java` in [IntelliJ IDEA](https://www.jetbrains.com/idea/.

   If you are unsure of how to open a CorDapp in IntelliJ, see the documentation on [Running a sample CorDapp](tutorial-cordapp.html##opening-the-sample-cordapp-in-intellij-idea).

## Create the `AppleStamp` state

First create the `AppleStamp` state. Remember that this state is the voucher issued to customers.

### Add annotations

The first thing you should do when writing a state is add the `@BelongsToContract` annotation. This annotation establishes the relationship between a state and a contract. Without this, your state does not know which contract is used to verify it.

1. Remove any pre-existing annotations in the template.

2. Add the annotation `@BelongsToContract(AppleStampContract.class)` to your state.

When naming states, it's best practice to match your contract and state names. In this case the state is called `AppleStamp`, so the contract is called `AppleStampContract`. Follow this naming convention when you write an original CorDapp to avoid confusion.

{{< note >}}
You've probably noticed that we haven't touched the imports at the top of the file yet. Don't worry, we'll get back to these in a little while.
{{< /note >}}

###


## Next steps

Follow the [Write the contract](tutorial-basic-cordapp-contract.md) tutorial to continue on this learning path.

## Related content

* [API: States](api-states.md#api-states)
* [Reissuing states](reissuing-states.md)

