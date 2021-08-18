---
date: '2021-07-03'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-tutorial-basic-cordapp-state
    parent: corda-os-4-8-tutorial-basic-cordapp-intro
    weight: 1030
tags:
- tutorial
- cordapp
title: Write the states
---

This tutorial guides you through writing the two states you need in your CorDapp: `AppleStamp` and `BasketofApples`. You will be creating these states in the `contracts/src/main/java/com/template/states/` directory in this tutorial. Refer to the `TemplateState.java` file in this directory for guidance.

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


3. Once you have successfully cloned the CorDapp template, open the `cordapp-template-kotlin` or `cordapp-template-java` in [IntelliJ IDEA](https://www.jetbrains.com/idea/).

   If you are unsure of how to open a CorDapp in IntelliJ, see the documentation on [Running a sample CorDapp](tutorial-cordapp.html##opening-the-sample-cordapp-in-intellij-idea).

## Create the `AppleStamp` state

First create the `AppleStamp` state. This state is the voucher issued to customers.

1. Right-click the **states** folder, select **New > Java Class** and create a file called `AppleStamp`.

2. Open the file.

### Add annotations

The first thing you should do when writing a state is add the `@BelongsToContract` annotation. This annotation establishes the relationship between a state and a contract. Without this, your state does not know which contract is used to verify it.

1. If you've copied in the template state, remove any pre-existing annotations in the template.

2. Add the annotation `@BelongsToContract(AppleStampContract.class)` to your state.

This what your code should look like so far:

```java
@BelongsToContract(AppleStampContract.class)
```

When naming states, it's best practice to match your contract and state names. In this case the state is called `AppleStamp`, so the contract is called `AppleStampContract`. Follow this naming convention when you write an original CorDapp to avoid confusion.

{{< note >}}
You've probably noticed that the state template includes imports at the top of the file. Don't worry, we'll get back to these in a little while.
{{< /note >}}

### Implement the contract state

The next line of code you add defines the type of [`ContractState`](api-states.html#contractstate) you implement with the `AppleStamp` class. Add this line to ensure that Corda recognizes the `AppleStamp` as a state.

In this case, use a `LinearState` to tie the `AppleStamp` to a `LinearID`.

1. Add the public class `AppleStamp` implementing a `LinearState`.

This is what your code should look like now:

```java
@BelongsToContract(AppleStampContract.class)
public class AppleStamp implements LinearState {
```

### Add private variables

Next, add the private variables for the stamp description (`stampDesc`), the issuer of the stamp (`issuer`), and the current owner of the stamp (`holder`).

After adding these variables, your code should look like this:

```java
@BelongsToContract(AppleStampContract.class)
public class AppleStamp implements LinearState {

    //Private Variables
    private String stampDesc; //For example: "One stamp can be exchanged for a basket of Gala apples."
    private Party issuer; //The person who issued the stamp.
    private Party holder; //The person who currently owns the stamp.
  }
```

### Add required variables and parameters

1. All `LinearState`s must have a variable for the state's linear ID. Add this variable under the private variables:

```java
private UniqueIdentifier linearID;
```

2. All Corda states must include a parameter to indicate the parties that store the states. Add this parameter below the `LinearStare` variable:

```java
private List<AbstractParty> participants;
```

After adding these sections, your code should look like this:

```java
@BelongsToContract(AppleStampContract.class)
public class AppleStamp implements LinearState {

    //Private Variables
    private String stampDesc; //For example: "One stamp can exchange for a basket of HoneyCrispy Apple"
    private Party issuer; //The person who issued the stamp
    private Party holder; //The person who currently owns the stamp

    //LinearState required variable.
    private UniqueIdentifier linearID;

    //Parameter required by all Corda states to indicate storing parties
    private List<AbstractParty> participants;

  }
```

### Add the constructor

Add a constructor to initalize the objects in the `AppleStamp` state.

If you're using IntelliJ, you can generate the constructor with a shortcut.

1. On MacOS, press **Command** + **N**.

    On Windows, press **Alt** + **Insert**.

2. Select **Constructors** in the **Generate** menu.

3. Select all the constructors that appear and click **OK**.

4. Add the following annotation before the constructor to ensure that all variables appear: `@ConstructorForDeserialization`

{{< note >}}
When building a CorDapp, your constructor parameters must have the same name as the private variables you declared earlier.
{{< /note >}}

After adding the constructor, your code should look like this:

```java
@BelongsToContract(AppleStampContract.class)
public class AppleStamp implements LinearState {

    //Private Variables
    private String stampDesc; //For example: "One stamp can exchange for a basket of HoneyCrispy Apple"
    private Party issuer; //The person who issued the stamp
    private Party holder; //The person who currently owns the stamp

    //LinearState required variable.
    private UniqueIdentifier linearID;

    //ALL Corda States must have this parameter to indicate storing parties.
    private List<AbstractParty> participants;

    //Constructor Tips: Command + N in IntelliJ can auto generate constructor.
    @ConstructorForDeserialization
    public AppleStamp(String stampDesc, Party issuer, Party holder, UniqueIdentifier linearID) {
        this.stampDesc = stampDesc;
        this.issuer = issuer;
        this.holder = holder;
        this.linearID = linearID;
        this.participants = new ArrayList<AbstractParty>();
        this.participants.add(issuer);
        this.participants.add(holder);
    }
```

### Add getters

To access a private variable outside of its class in Java, you must use a getter. If you do not use getters, your Corda node cannot pick up the variables.

1. Add a getter for each variable.

After you've added the getters, your code should look like this:

```java
@BelongsToContract(AppleStampContract.class)
public class AppleStamp implements LinearState {

    //Private Variables
    private String stampDesc; //For example: "One stamp can exchange for a basket of HoneyCrispy Apple"
    private Party issuer; //The person who issued the stamp
    private Party holder; //The person who currently owns the stamp

    //LinearState required variable.
    private UniqueIdentifier linearID;

    //ALL Corda State required parameter to indicate storing parties
    private List<AbstractParty> participants;

    //Constructor Tips: Command + N in IntelliJ can auto generate constructor.
    @ConstructorForDeserialization
    public AppleStamp(String stampDesc, Party issuer, Party holder, UniqueIdentifier linearID) {
        this.stampDesc = stampDesc;
        this.issuer = issuer;
        this.holder = holder;
        this.linearID = linearID;
        this.participants = new ArrayList<AbstractParty>();
        this.participants.add(issuer);
        this.participants.add(holder);
    }

    @NotNull
    @Override
    public List<AbstractParty> getParticipants() {
        return this.participants;
    }

    @NotNull
    @Override
    public UniqueIdentifier getLinearId() {
        return this.linearID;
    }

    //Getters
    public String getStampDesc() {
        return stampDesc;
    }

    public Party getIssuer() {
        return issuer;
    }

    public Party getHolder() {
        return holder;
    }

}
```

### Add imports

If you're using IntelliJ or another IDE, the IDE will automatically add the imports you need.

IntelliJ indicates that an import is missing with red text. To add the import:

1. Click the red text. You will see a pop-up that says "Unresolvable reference: {name of the missing input}".

2. On MacOS, press **Option** + **Enter** to automatically import that variable.

    On Windows, press **Alt** + **Enter** to automatically import that variable.

3. Repeat this process with all missing imports.

Once you have added all imports, your code should look like this and you have finished writing the `AppleStamp` state:

```java
package com.tutorial.states;

import com.tutorial.contracts.AppleStampContract;
import net.corda.core.contracts.BelongsToContract;
import net.corda.core.contracts.LinearState;
import net.corda.core.contracts.UniqueIdentifier;
import net.corda.core.identity.AbstractParty;
import net.corda.core.identity.Party;
import net.corda.core.serialization.ConstructorForDeserialization;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

@BelongsToContract(AppleStampContract.class)
public class AppleStamp implements LinearState {

    //Private Variables
    private String stampDesc; //For example: "One stamp can exchange for a basket of HoneyCrispy Apple"
    private Party issuer; //The person who issued the stamp
    private Party holder; //The person who currently owns the stamp

    //LinearState required variable.
    private UniqueIdentifier linearID;

    //ALL Corda State required parameter to indicate storing parties
    private List<AbstractParty> participants;

    //Constructor Tips: Command + N in IntelliJ can auto generate constructor.
    @ConstructorForDeserialization
    public AppleStamp(String stampDesc, Party issuer, Party holder, UniqueIdentifier linearID) {
        this.stampDesc = stampDesc;
        this.issuer = issuer;
        this.holder = holder;
        this.linearID = linearID;
        this.participants = new ArrayList<AbstractParty>();
        this.participants.add(issuer);
        this.participants.add(holder);
    }

    @NotNull
    @Override
    public List<AbstractParty> getParticipants() {
        return this.participants;
    }

    @NotNull
    @Override
    public UniqueIdentifier getLinearId() {
        return this.linearID;
    }

    //Getters
    public String getStampDesc() {
        return stampDesc;
    }

    public Party getIssuer() {
        return issuer;
    }

    public Party getHolder() {
        return holder;
    }

}
```

## Create the `BasketOfApples` state

The `BasketOfApples` state is the basket of apples that Farmer Bob self-issues to prepare the apples for Peter. Now that you've written your first state, try writing the `BasketOfApples` state using the following information.

Private variables:
* `description` - The brand or type of apple. Use type `String`.
* `farm` - The origin of the apples. Use type `Party`.
* `owner` - The person exchanging the basket of apples for the voucher (Farmer Bob). Use type `Party`.
* `weight` - The weight of the basket of apples. Use type `int`.

### Check your work

Once you've written the `BasketOfApples` state, check your code against the sample below. Your code should look something like this:

```java
package com.tutorial.states;

import com.tutorial.contracts.BasketOfAppleContract;
import net.corda.core.contracts.BelongsToContract;
import net.corda.core.contracts.ContractState;
import net.corda.core.identity.AbstractParty;
import net.corda.core.identity.Party;
import net.corda.core.serialization.ConstructorForDeserialization;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

@BelongsToContract(BasketOfAppleContract.class)
public class BasketOfApple implements ContractState {

    //Private Variables
    private String description; //Brand or type
    private Party farm; //Origin of the apple
    private Party owner; //The person who exchange the basket of apple with the stamp.
    private int weight;

    //ALL Corda State required parameter to indicate storing parties
    private List<AbstractParty> participants;

    //Constructors
    //Basket of Apple creation. Only farm name is stored.
    public BasketOfApple(String description, Party farm, int weight) {
        this.description = description;
        this.farm = farm;
        this.owner=farm;
        this.weight = weight;
        this.participants = new ArrayList<AbstractParty>();
        this.participants.add(farm);
    }

    //Constructor for object creation during transaction
    @ConstructorForDeserialization
    public BasketOfApple(String description, Party farm, Party owner, int weight) {
        this.description = description;
        this.farm = farm;
        this.owner = owner;
        this.weight = weight;
        this.participants = new ArrayList<AbstractParty>();
        this.participants.add(farm);
        this.participants.add(owner);
    }

    @NotNull
    @Override
    public List<AbstractParty> getParticipants() {
        return participants;
    }

    //getters
    public String getDescription() {
        return description;
    }

    public Party getFarm() {
        return farm;
    }

    public Party getOwner() {
        return owner;
    }

    public int getweight() {
        return weight;
    }

    public BasketOfApple changeOwner(Party buyer){
        BasketOfApple newOwnerState = new BasketOfApple(this.description,this.farm,buyer,this.weight);
        return newOwnerState;
    }

}
```

## Next steps

Follow the [Write the contracts](tutorial-basic-cordapp-contract.md) tutorial to continue on this learning path.

## Related content

* [API: States](api-states.md#api-states)
* [Reissuing states](reissuing-states.md)
