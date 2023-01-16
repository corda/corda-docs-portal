---
date: '2021-09-15'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-state
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1030
tags:
- tutorial
- cordapp
title: "Write a simple state"
expiryDate: '2022-09-28'
---

In Corda, states are immutable objects. One or more Corda nodes agree that these states exist at a specific point in time. These objects can represent any information—in this example, the states represent the voucher for a trip to Mars (`MarsVoucher`) and a ticket (`BoardingTicket`) given to the customer when they redeem their voucher. These states represent information that Mars Express and the customer share and have agreed upon.

States associated to a specific party's identity are stored in that entity's vault. They are also stored in the vaults of other parties involved in transactions with that state. For a state to evolve, the current state must be marked as historic and a new, updated state must be created. The `MarsVoucher` state is issued by the company Mars Express to Peter, so it is stored in both parties' vaults. When Peter redeems his voucher, the `MarsVoucher` state is spent and this information is updated in both vaults. It's a similar process for the `BoardingTicket` state. The state is issued by Mars Express and spent when Peter takes his trip. Both the voucher and ticket are valid for single-use only—when the states are spent, it guarantees that they cannot be used again.

When you create a state, you include the relevant information about the fact you are storing. The `MarsVoucher` state includes a description of the voucher and the names of the issuer and holder. The `BoardingTicket` includes trip information, the issuer and owner of the ticket, and the days left until the rocket launch. You also include a reference to the contract that governs how the states should evolve over time. The state must implement <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#contractstate">`ContractState`</a> or one of its dependents.

This tutorial guides you through writing the `MarsVoucher` state. You will be creating this state in the `contracts/src/main/kotlin/net/corda/missionMars/states/` directory. Refer to the `TemplateState.kt` file in this directory to see a template state.

## Learning objectives

After you have completed this tutorial and the tutorial on [writing advanced states](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-state-2.md), you will know how to create and implement states in a Corda 5 Developer Preview CorDapp.

## Before you start

Before you start building states, read [Key concepts: States](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-states.md).

## Clone the CorDapp template repo

The easiest way to write any CorDapp is to start from a template. This ensures that you have the correct files to begin building.

1. Clone the CorDapp template repo in the directory of your choice:

   {{< tabs name="tabs-1" >}}
   {{% tab name="Kotlin" %}}
   ```console
   git clone https://github.com/corda/corda5-cordapp-template-kotlin.git
   ```
   {{% /tab %}}

   {{% tab name="Java" %}}
   ```console
   git clone https://github.com/corda/corda5-cordapp-template-java.git
   ```
   {{% /tab %}}

   {{< /tabs >}}

2. Open `corda5-cordapp-template-kotlin` in [IntelliJ IDEA](https://www.jetbrains.com/idea/).

   If you don't know how to open a CorDapp in IntelliJ, see the documentation on [running a sample CorDapp](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/run-demo-cordapp.html#open-the-sample-cordapp-in-intellij-idea).

3. If you want to customize the CorDapp template, [rename the package](https://www.jetbrains.com/help/idea/rename-refactorings.html#rename_package) to `missionMars`. This changes all instances of `template` in the project to `missionMars`.

## Create the `MarsVoucher` state

The `MarsVoucher` state represents the voucher that Mars Express will issue to its customers and must include:
* A description of the voucher. This includes any relevant information, such as an expiration date.
* The name of the issuer. The customer can then verify which company the voucher was purchased from.
* The name of the current holder. The company can then verify the identity of the customer who redeems the voucher.

The `MarsVoucher` state must be transferable between entities. A customer redeems their voucher by returning it to the company that issued it. The value of this voucher does not change until it is redeemed, when the state is consumed and the voucher cannot be used again.

### Set up the `MarsVoucher` class

1. Right-click the **states** folder, select **New > Kotlin Class/File**.

2. In the **New Kotlin Class/File** window, select **Class** and create a file called `MarsVoucher`.

3. Open the file.

### Define the `MarsVoucher` data class

Include these variables in the `MarsVoucher` data class:

*  `voucherDesc`: A description of the voucher. Use type `String`.
*  `issuer`: The issuer of the voucher. Use type `Party`.
*  `holder`: The current owner of the voucher. Use type `Party`.

Your code should now look like this:

{{< tabs name="tabs-2" >}}
{{% tab name="Kotlin" %}}
```kotlin
package net.corda.missionMars.states

import net.corda.v5.application.identity.Party

data class MarsVoucher (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
)
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.states;

import net.corda.v5.application.identity.Party;

public class MarsVoucher {

    private String voucherDesc;
    private Party issuer;
    private Party holder;
    private UniqueIdentifier linearId;
}
```
{{% /tab %}}

{{< /tabs >}}

### Implement the `LinearState` interface

You need a way to track the evolution of this state as it is transferred between parties. Use a <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#linearstate">`LinearState`</a> to tie the `MarsVoucher` to a `linearId`. When the state is transferred to a new holder, the state evolves. This creates a sequence of `LinearStates` with each evolution. The `LinearState`s share a `linearId`, so you can track the lifecycle of the `MarsVoucher` state.

The `LinearState` makes sense for this use case, but there are several types of <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#contractstate">`ContractState`s</a> that you can use when writing your own CorDapp:

* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#linearstate">`LinearState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#ownablestate">`OwnableState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#fungiblestate">`FungibleState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#the-queryablestate-and-schedulablestate-interfaces">`QueryableState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#the-queryablestate-and-schedulablestate-interfaces">`SchedulableState`</a>

`LinearState` allows Corda to use the `MarsVoucher` as a state. You must implement a method to populate the `participants` of the state. `participants` is a list of the `AbstractParty` that are involved with the state. The `participants`:

* Store the state in their vault.
* Need to sign any notary-change and contract-upgrade transactions involving this state.
* Receive any finalized transactions involving this state as part of `FinalityFlow`.

1. Implement the `LinearState` interface and define an [override varaible](https://kotlinlang.org/docs/inheritance.html#overriding-properties) for the `linearId` of the state. This is required for `LinearState`s.
2. Define another override variable for the `participants` of the state.

Your code should now look like this:


{{< tabs name="tabs-3" >}}
{{% tab name="Kotlin" %}}
```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.LinearState

data class MarsVoucher (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
        override val linearId: UniqueIdentifier,//LinearState required variable
) : LinearState{

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(issuer,holder)

    }
)
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.states;

import net.corda.v5.application.identity.AbstractParty;
import net.corda.v5.application.identity.Party;
import net.corda.v5.ledger.UniqueIdentifier;
import net.corda.v5.ledger.contracts.LinearState;

public class MarsVoucher implements LinearState {

    private String voucherDesc;
    private Party issuer;
    private Party holder;
    private UniqueIdentifier linearId;

    /* Constructor of your Corda state */
    public MarsVoucher(String voucherDesc, Party issuer, Party holder, UniqueIdentifier linearId) {
        this.voucherDesc = voucherDesc;
        this.issuer = issuer;
        this.holder = holder;
        this.linearId = linearId;
    }

    //getters
    public String getVoucherDesc() { return voucherDesc; }
    public Party getIssuer() { return issuer; }
    public Party getHolder() { return holder; }

    /* This method will indicate who are the participants and required signers when
     * this state is used in a transaction. */
    @NotNull
    @Override
    public List<AbstractParty> getParticipants() { return Arrays.asList(this.issuer, this.holder); }

    @NotNull
    @Override
    public UniqueIdentifier getLinearId() {
        return this.linearId;
    }
}
```
{{% /tab %}}

{{< /tabs >}}

### Implement the `JsonRepresentable` interface to use the Corda RPC Client

The Corda RPC Client takes in JSON parameters. You must pass JSON parameters if you want the output to be returned over RPC. All of your CorDapp's external interactions are now performed via HTTP-RPC REST APIs. The node will return information in the same way.

Implement the `JsonRepresentable` interface in `MarsVoucher` to ensure that it can be transmitted over RPC.

{{< note >}}
There are several ways to return your parameters in a JSON string. This tutorial shows you one method, but you are not restricted to using this specific method in Corda.
{{< /note >}}

1. Create a data transfer object that encapsulates the data of your `MarsVoucher` state—`MarsVoucherDto`. Include the same variables as the `MarsVoucher` class (`voucherDesc`, `issuer`, and `holder`) and mark all variables as type `String`. This sets up a template that the node uses to send this data class to the RPC Client.
2. Create a function that instantiates the `MarsVoucherDto` and populates the template with the actual variables of the class.
3. Create an [override function](https://kotlinlang.org/docs/inheritance.html#overriding-methods) that converts the `MarsVoucherDto` to JSON using the `toJson` method.

Your code should look like this:

{{< tabs name="tabs-4" >}}
{{% tab name="Kotlin" %}}
```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.LinearState

data class MarsVoucher (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
        override val linearId: UniqueIdentifier,//LinearState required variable
) : LinearState, JsonRepresentable{

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(issuer,holder)

    fun toDto(): MarsVoucherDto {
        return MarsVoucherDto(
                voucherDesc,
                issuer.name.toString(),
                holder.name.toString(),
                linearId.toString()
        )
    }

    override fun toJsonString(): String {
        return Gson().toJson(this.toDto())
    }
}

data class MarsVoucherDto(
      val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
      val issuer: String, //The party who issued the voucher
      val holder: String, //The party who currently owns the voucher
      val linearId: String,//LinearState required variable
)
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.states;

import net.corda.v5.application.identity.AbstractParty;
import net.corda.v5.application.identity.Party;
import net.corda.v5.application.utilities.JsonRepresentable;
import net.corda.v5.ledger.UniqueIdentifier;
import net.corda.v5.ledger.contracts.BelongsToContract;
import net.corda.v5.ledger.contracts.LinearState;
import org.jetbrains.annotations.NotNull;

import java.util.Arrays;
import java.util.List;
public class MarsVoucher implements LinearState, JsonRepresentable {

    private String voucherDesc;
    private Party issuer;
    private Party holder;
    private UniqueIdentifier linearId;

    /* Constructor of your Corda state */
    public MarsVoucher(String voucherDesc, Party issuer, Party holder, UniqueIdentifier linearId) {
        this.voucherDesc = voucherDesc;
        this.issuer = issuer;
        this.holder = holder;
        this.linearId = linearId;
    }

    //getters
    public String getVoucherDesc() { return voucherDesc; }
    public Party getIssuer() { return issuer; }
    public Party getHolder() { return holder; }

    @NotNull
    @Override
    public String toJsonString() {
        return "voucherDesc : " + this.voucherDesc +
                " issuer : " + this.issuer.getName().toString() +
                " holder : " + this.holder.getName().toString() +
                " linearId: " + this.linearId.toString();
    }

    /* This method will indicate who are the participants and required signers when
     * this state is used in a transaction. */
    @NotNull
    @Override
    public List<AbstractParty> getParticipants() { return Arrays.asList(this.issuer, this.holder); }

    @NotNull
    @Override
    public UniqueIdentifier getLinearId() {
        return this.linearId;
    }
}
```
{{% /tab %}}

{{< /tabs >}}

### Create a function to transfer the `MarsVoucher` state

As a user of the Mission Mars CorDapp, you may want to transfer a `MarsVoucher` state that you buy to another user. Maybe you want to gift them a trip to Mars.

Create a function called `changeOwner` that allows the `MarsVoucher` state to be transferred to a new owner.

You've finished writing the `MarsVoucher` state. This is what your code should look like now:

{{< tabs name="tabs-5" >}}
{{% tab name="Kotlin" %}}
```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.BelongsToContract
import net.corda.v5.ledger.contracts.LinearState

@BelongsToContract(MarsVoucherContract::class)
data class MarsVoucher (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars."
        val issuer: Party, //The person who issued the voucher.
        val holder: Party, //The person who currently owns the voucher.
        override val linearId: UniqueIdentifier,//LinearState required variable.
) : LinearState, JsonRepresentable{

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(issuer,holder)

    fun toDto(): MarsVoucherDto {
        return MarsVoucherDto(
                voucherDesc,
                issuer.name.toString(),
                holder.name.toString(),
                linearId.toString()
        )
    }

    fun changeOwner(newOwner: Party): MarsVoucher {
        return MarsVoucher(voucherDesc, issuer, newOwner, linearId)
    }


    override fun toJsonString(): String {
        return Gson().toJson(this.toDto())
    }
}

data class MarsVoucherDto(
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars."
        val issuer: String, //The person who issued the voucher.
        val holder: String, //The person who currently owns the voucher.
        val linearId: String,//LinearState required variable.
)
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.states;

import net.corda.v5.application.identity.AbstractParty;
import net.corda.v5.application.identity.Party;
import net.corda.v5.application.utilities.JsonRepresentable;
import net.corda.v5.ledger.UniqueIdentifier;
import net.corda.v5.ledger.contracts.BelongsToContract;
import net.corda.v5.ledger.contracts.LinearState;
import org.jetbrains.annotations.NotNull;

import java.util.Arrays;
import java.util.List;
public class MarsVoucher implements LinearState, JsonRepresentable {

    private String voucherDesc;
    private Party issuer;
    private Party holder;
    private UniqueIdentifier linearId;

    /* Constructor of your Corda state */
    public MarsVoucher(String voucherDesc, Party issuer, Party holder, UniqueIdentifier linearId) {
        this.voucherDesc = voucherDesc;
        this.issuer = issuer;
        this.holder = holder;
        this.linearId = linearId;
    }

    //helper method
    public MarsVoucher changeOwner(Party holder){
        MarsVoucher newOwnerState = new MarsVoucher(this.voucherDesc,this.issuer,holder,this.linearId);
        return newOwnerState;
    }


    //getters
    public String getVoucherDesc() { return voucherDesc; }
    public Party getIssuer() { return issuer; }
    public Party getHolder() { return holder; }

    @NotNull
    @Override
    public String toJsonString() {
        return "voucherDesc : " + this.voucherDesc +
                " issuer : " + this.issuer.getName().toString() +
                " holder : " + this.holder.getName().toString() +
                " linearId: " + this.linearId.toString();
    }

    /* This method will indicate who are the participants and required signers when
     * this state is used in a transaction. */
    @NotNull
    @Override
    public List<AbstractParty> getParticipants() { return Arrays.asList(this.issuer, this.holder); }

    @NotNull
    @Override
    public UniqueIdentifier getLinearId() {
        return this.linearId;
    }
}
```
{{% /tab %}}

{{< /tabs >}}

## Next steps

Now that you have written the first state for the Mission Mars CorDapp, <a href="../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-state-2.md">write the `BoardingTicket` state</a>.  
