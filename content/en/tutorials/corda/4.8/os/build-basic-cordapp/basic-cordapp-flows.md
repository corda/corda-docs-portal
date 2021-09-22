---
aliases:
- /docs/corda-os/4.8/flow-state-machines.html
- /docs/platform/corda/4.8/os/flow-state-machines.html
date: '2021-09-22'
section_menu: tutorials
menu:
  tutorials:
    identifier: corda-os-4-8-tutorial-basic-cordapp-flows
    parent: corda-os-4-8-tutorial-basic-cordapp-intro
    weight: 1045
tags:
- tutorial
- cordapp
title: Write flows
---

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell the node how to achieve a specific ledger update, such as issuing an asset or making a deposit. Nodes communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties.

This tutorial guides you through writing the three flows you need in your CorDapp. These are:

* `CreateAndIssueAppleStamp` flow
* `PackageApples` flow
* `RedeemApples` flow

You will be creating these flows in the `workflows/src/main/java/com/tutorial/flows` directory in this tutorial. Refer to the `TemplateInitiator.java` and `TemplateResponder.java` files in this directory to see template initiator and responder flows.

## Learning objectives

After you have completed this tutorial, you will know how to write and implement flows in a CorDapp.

## Before you start

Before you start writing flows, read [Key concepts: Flows](../../../../../platform/corda/4.8/open-source/key-concepts-flows.md).

## Write the `CreateAndIssueAppleStamp` flow

The `CreateAndIssueAppleStamp` flow creates the `AppleStamp` and issues it to the customer.

### Write the initiator flow

The `CreateAndIssueAppleStamp` flow action requires interaction between the issuer and the customer. For this reason, you must create and initiator flow and a responder flow.

#### Implement the `CreateAndIssueAppleStamp` class

Add the `CreateAndIssueAppleStamp` public class. When naming a public class, the class name must match the name of the file. You will fill this class in subsequent sections of the tutorial.

#### Add annotations

1. Add the `@InitiatingFlow` annotation. This indicates that this flow is the initiating flow.
2. Add the `@StartableByRPC` annotation. This annotation allows the flow to be started by RPC. You **must** use this annotation if you want to run the flow with the RPC client.

So far your code should look like this:

```java
package com.tutorial.flows;

public class CreateAndIssueAppleStamp {

    @InitiatingFlow
    @StartableByRPC
}
```

#### Add the `CreateAndIssueAppleStampInitiator` subclass

Add the `CreateAndIssueAppleStampInitiator` public static class to extend `FlowLogic`. Include a `SignedTransaction` return type.

#### Add variables

Add the following private variables to the subclass:

* `stampDescription` - Information included with the `AppleStamp`. This must be a `String` type.
* `holder` - The holder of the `AppleStamp`. This must be a `Party` type.

{{< note >}}
When writing flows, it's important to consider who is calling the flow-this affects the parameters you need.
{{< /note >}}

#### Add a constructor

The constructor must have the same name as the subclass. Include the `holder` and `stampDescription` variables in the constructor.

Let's check in on your code. It should now look like this:

```java
package com.tutorial.flows;

public class CreateAndIssueAppleStamp {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateAndIssueAppleStampInitiator  extends FlowLogic<SignedTransaction>{

        private String stampDescription;
        private Party holder;

        public CreateAndIssueAppleStampInitiator(String stampDescription,  Party holder) {
            this.stampDescription = stampDescription;
            this.holder = holder;
        }
```

#### Add the `call` method

1. Add the `@Suspendable` annotation.
2. Add the `@Override` annotation.
3. Add the `call` method with a `SignedTransaction` return type.

#### Obtain a reference for the notary

You must obtain a reference for the notary

## Write the `PackageApples` flow

## Write the `RedeemApples` flow
