---
aliases:
- /releases/release-V4.1/quickstart-build.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-1:
    identifier: corda-os-4-1-quickstart-build
    parent: corda-os-4-1-quickstart-index
    weight: 1020
tags:
- quickstart
- build
title: Building your own CorDapp
---




# Building your own CorDapp

After examining a functioning CorDapp, the next challenge is to create one of your own. We’re going to build a simple supply chain CorDapp representing a network between a car dealership, a car manufacturer, and a bank.

To model this network, you need to create one state (representing cars), one contract (to control the rules governing cars), and one flow (to create cars). This CorDapp will be very basic, but entirely functional and deployable.


## Step One: Download a template CorDapp

The first thing you need to do is clone a CorDapp template to modify.


* Open a terminal and navigate to a directory to store the new project.
* Run the following command to clone the template CorDapp: `git clone https://github.com/corda/cordapp-template-kotlin.git`
* Open IntelliJ and open the CorDapp template project.
* Click **File** >  **Project Structure**. To set the project SDK click **New…** > **JDK**, and navigating to the installation directory of your JDK. Click **Apply**.
* Select **Modules** > **+** > **Import Module**. Select the `cordapp-template-kotlin` folder and click **Open**. Select **Import module from external model** > **Gradle** > **Next** > tick the **Use auto-import** checkbox > **Finish** > **Ok**. Gradle will now download all the project dependencies and perform some indexing.


## Step Two: Creating states

Since the CorDapp models a car dealership network, a state must be created to represent cars. States are immutable objects representing on-ledger facts. A state might represent a physical asset like a car, or an intangible asset or agreement like an IOU. For more information on states, see the [state documentation](key-concepts-states.md).


* From IntelliJ expand the source files and navigate to the following state template file: `contracts > src > main > kotlin > com.template > states > TemplateState.kt`.
* Right-click on **TemplateState.kt** in the project navigation on the left. Select **Refactor** > **Copy**.
* Rename the file to `CarState` and click **OK**.
* Double-click the new state file to open it. Add the following imports to the top of the state file:>
{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
package com.template.states

import com.template.contracts.CarContract
import com.template.contracts.TemplateContract
import net.corda.core.contracts.BelongsToContract
import net.corda.core.contracts.ContractState
import net.corda.core.contracts.UniqueIdentifier
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.Party
```
{{% /tab %}}

{{< /tabs >}}





It’s important to specify what classes are required in each state, contract, and flow. This process must be repeated with each file as it is created.



* Update `@BelongsToContract(TemplateContract:class)` to specify `CarContract::class`.
* Add the following fields to the state:



* `owningBank` of type `Party`
* `holdingDealer` of type `Party`
* `manufacturer` of type `Party`
* `vin` of type `String`
* `licensePlateNumber` of type `String`
* `make` of type `String`
* `model` of type `String`
* `dealershipLocation` of type `String`
* `linearId` of type `UniqueIdentifier`

Don’t worry if you’re not sure exactly how these should appear, you can check your code shortly.



* Remove the `data` and `participants` parameters.
* Add a body to the `CarState` class that overrides participants to contain a list of `owningBank`, `holdingDealer`, and `manufacturer`.
* The `CarState` file should now appear as follows:>
{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
package com.template.states

import com.template.contracts.CarContract
import com.template.contracts.TemplateContract
import net.corda.core.contracts.BelongsToContract
import net.corda.core.contracts.ContractState
import net.corda.core.contracts.UniqueIdentifier
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.Party

// *********
// * State *
// *********

@BelongsToContract(CarContract::class)
data class CarState(
        val owningBank: Party,
        val holdingDealer: Party,
        val manufacturer: Party,
        val vin: String,
        val licensePlateNumber: String,
        val make: String,
        val model: String,
        val dealershipLocation: String,
        val linearId: UniqueIdentifier
) : ContractState {
    override val participants: List<AbstractParty> = listOf(owningBank, holdingDealer, manufacturer)
}
```
{{% /tab %}}

{{< /tabs >}}



* Save the `CarState.kt` file.

The `CarState` definition has now been created. It lists the properties and associated types required of all instances of this state.


## Step Three: Creating contracts

After creating a state, you must create a contract. Contracts define the rules that govern how states can be created and evolved. For example, a contract for a Cash state should check that any transaction that changes the ownership of the cash is signed by the current owner and does not create cash from thin air. To learn more about contracts, see the [contracts documentation](key-concepts-contracts.md).


* From IntelliJ, expand the project source and navigate to: `contracts > src > main > kotlin > com > template > contracts > TemplateContract.kt`
* Right-click on **TemplateContract.kt** in the project navigation on the left. Select **Refactor > Copy**.
* Rename the file to `CarContract` and click **OK**.
* Double-click the new contract file to open it.
* Add the following imports to the top of the file:>
{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
package com.template.contracts

import com.template.states.CarState
import net.corda.core.contracts.CommandData
import net.corda.core.contracts.Contract
import net.corda.core.contracts.requireSingleCommand
import net.corda.core.contracts.requireThat
import net.corda.core.transactions.LedgerTransaction
```
{{% /tab %}}

{{< /tabs >}}



* Update the class name to: `CarContract`
* Replace `const val ID = "com.template.contracts.TemplateContract"` with `val ID = CarContract::class.qualifiedName!!`. This ID field is used to identify contracts when building a transaction. This ID declaration ensures that the contract name is created dynamically and can simplify code refactoring.
* Update the `Action` command to an `Issue` command. This represents an issuance of an instance of the `CarState` state.


Commands are the operations that can be performed on a state. A contract will often define command logic for several operations that can be performed on the state in question, for example, issuing a state, changing ownership, and marking the state retired.



* Add `val command = tx.commands.requireSingleCommand<Commands>().value` at the beginning of the `verify()` method. The `verify()` method defines the verification rules that commands must satisfy to be valid.
* The final function of the contract is to prevent unwanted behaviour during the flow. After the `val command = tx.commands...` line, add the following requirement code:{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
when(command) {
  is Commands.Issue -> requireThat {
    "There should be no input state" using (tx.inputs.isEmpty())
  }
}
```
{{% /tab %}}

{{< /tabs >}}


* Inside the `requireThat` block add additional lines defining the following requirements:



* There should be one output state.
* The output state must be of the type `CarState`.
* The `licensePlateNumber` must be seven characters long.



* The `CarContract.kt` file should look as follows:{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
package com.template.contracts

import com.template.states.CarState
import net.corda.core.contracts.CommandData
import net.corda.core.contracts.Contract
import net.corda.core.contracts.requireSingleCommand
import net.corda.core.contracts.requireThat
import net.corda.core.transactions.LedgerTransaction

class CarContract : Contract {
    companion object {
        const val ID = "com.template.contracts.CarContract"
    }

    override fun verify(tx: LedgerTransaction) {

        val command = tx.commands.requireSingleCommand<Commands>().value

        when(command) {
          is Commands.Issue -> requireThat {
            "There should be no input state" using (tx.inputs.isEmpty())
            "There should be one output state" using (tx.outputs.size == 1)
            "The output state must be of type CarState" using (tx.outputs.get(0).data is CarState)
            val outputState = tx.outputs.get(0).data as CarState
            "The licensePlateNumber must be seven characters long" using (outputState.licensePlateNumber.length == 7)
          }
        }
    }

    interface Commands : CommandData {
        class Issue : Commands
    }
}
```
{{% /tab %}}

{{< /tabs >}}


* Save the `CarContract.kt` file. The contract file now defines rules that all transactions creating car states must follow.


## Step Four: Creating a flow


* From IntelliJ, expand the project source and navigate to: `workflows > src > main > kotlin > com.template.flows > Flows.kt`
* Right-click on **Flows.kt** in the project navigation on the left. Select **Refactor > Copy**.
* Rename the file to `CarFlow` and click **OK**.
* Add the following imports to the top of the file:>
{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
package com.template.flows

import co.paralleluniverse.fibers.Suspendable
import com.template.contracts.CarContract
import com.template.states.CarState
import net.corda.core.contracts.Command
import net.corda.core.contracts.UniqueIdentifier
import net.corda.core.contracts.requireThat
import net.corda.core.flows.*
import net.corda.core.identity.Party
import net.corda.core.node.ServiceHub
import net.corda.core.transactions.SignedTransaction
import net.corda.core.transactions.TransactionBuilder
```
{{% /tab %}}

{{< /tabs >}}



* Double-click the new flow file to open it.
* Update the name of the `Initiator` class to `CarIssueInitiator`.
* Update the name of the `Responder` class to `CarIssueResponder`.
* Update the `@InitiatedBy` property of `CarIssueResponder` to `CarIssueInitiator::class`.
* Now that the flow structure is in place, we can begin writing the code to create a transaction to issue a car state. Add parameters to the `CarIssueInitiator` class for all the fields of the `CarState` definition, except for `linearId`.
* Inside the `call()` function of the initiator, create a variable for the notary node: `val notary = serviceHub.networkMapCache.notaryIdentities.first()`


{{< note >}}
The **networkMapCache** contains information about the nodes and notaries inside the network.

{{< /note >}}


* Create a variable for an `Issue` command.


The first parameter of the command must be the command type, in this case `Issue`. As discussed above, the command tells other nodes what the purpose of the transaction is.

The second parameter of the command must be a list of keys from the relevant parties, in this case `owningBank`, `holdingDealer`, and `manufacturer`. As well as informing parties what the purpose of  the transaction is, the command also specifies which signatures must be present on the associated transaction in order for it to be valid.



* Create a `CarState` object using the parameters of `CarIssueInitiator`.


The last parameter for `CarState` must be a new `UniqueIdentifier()` object.



* The `CarFlow.kt` file should look like this:{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
@InitiatingFlow
@StartableByRPC
class CarIssueInitiator(
        val owningBank: Party,
        val holdingDealer: Party,
        val manufacturer: Party,
        val vin: String,
        val licensePlateNumber: String,
        val make: String,
        val model: String,
        val dealershipLocation: String
) : FlowLogic<Unit>() {

    @Suspendable
    override fun call() {
        val notary = serviceHub.networkMapCache.notaryIdentities.first()
        val command = Command(CarContract.Commands.Issue(), listOf(owningBank, holdingDealer, manufacturer).map { it.owningKey })
        val carState = CarState(owningBank, holdingDealer, manufacturer, vin, licensePlateNumber, make, model, dealershipLocation, UniqueIdentifier())
    }
}

@InitiatedBy(CarIssueInitiator::class)
class CarIssueResponder(val counterpartySession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call(){

        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}


* Update the `FlowLogic<Unit>` to `FlowLogic<SignedTransaction>` in both the initiator and responder class. This indicates that the `SignedTransaction` produced by this flow is returned from `call` and sent to the caller of the flow. If left unchanged, `FlowLogic<Unit>` will return nothing.
* Update the return type of both `call()` transactions to be of type `SignedTransaction`.
* In the `call()` function, create a `TransactionBuilder` object similarly. The `TransactionBuilder` class should take in the notary node. The output state and command must be added to the `TransactionBuilder`.
* Verify the transaction by calling `verify(serviceHub)` on the `TransactionBuilder`.
* Sign the transaction and store the result in a variable, using the following [serviceHub](api-service-hub.md) method:{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin
val notary = serviceHub.networkMapCache.notaryIdentities.first()
```
{{% /tab %}}

{{< /tabs >}}


* Delete the `progressTracker` as it won’t be used in this tutorial.
* The `CarFlow.kt` file should now look like this:{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}
```kotlin
@InitiatingFlow
@StartableByRPC
class CarIssueInitiator(
        val owningBank: Party,
        val holdingDealer: Party,
        val manufacturer: Party,
        val vin: String,
        val licensePlateNumber: String,
        val make: String,
        val model: String,
        val dealershipLocation: String
) : FlowLogic<SignedTransaction>() {

    @Suspendable
    override fun call(): SignedTransaction {

        val notary = serviceHub.networkMapCache.notaryIdentities.first()
        val command = Command(CarContract.Commands.Issue(), listOf(owningBank, holdingDealer, manufacturer).map { it.owningKey })
        val carState = CarState(
                owningBank,
                holdingDealer,
                manufacturer,
                vin,
                licensePlateNumber,
                make,
                model,
                dealershipLocation,
                UniqueIdentifier()
        )

        val txBuilder = TransactionBuilder(notary)
                .addOutputState(carState, CarContract.ID)
                .addCommand(command)

        txBuilder.verify(serviceHub)
        val tx = serviceHub.signInitialTransaction(txBuilder)
    }
}

@InitiatedBy(CarIssueInitiator::class)
class CarIssueResponder(val counterpartySession: FlowSession) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {

        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}


* To finish the initiator’s `call()` function, other parties must sign the transaction. Add the following code to send the transaction to the other relevant parties:{{< tabs name="tabs-10" >}}
{{% tab name="kotlin" %}}
```kotlin
val sessions = (carState.participants - ourIdentity).map { initiateFlow(it as Party) }
val stx = subFlow(CollectSignaturesFlow(tx, sessions))
return subFlow(FinalityFlow(stx, sessions))
```
{{% /tab %}}

{{< /tabs >}}




The first line creates a `List<FlowSession>` object by calling `initiateFlow()` for each party other than the initiating party. The second line collects signatures from the relevant parties and returns a signed transaction. The third line calls `FinalityFlow()`, finalizes the transaction using the notary or notary pool.

{{< note >}}
Sessions are used for sending and receiving objects between nodes. `ourIdentity` is removed from the list of participants to open sessions to because a session does not need to be opened to the initiating party.

{{< /note >}}


* Lastly, the body of the responder flow must be completed. The following code checks the transaction contents, signs it, and sends it back to the initiator:{{< tabs name="tabs-11" >}}
{{% tab name="kotlin" %}}
```kotlin
@Suspendable
override fun call(): SignedTransaction {
    val signedTransactionFlow = object : SignTransactionFlow(counterpartySession) {
        override fun checkTransaction(stx: SignedTransaction) = requireThat {
            val output = stx.tx.outputs.single().data
            "The output must be a CarState" using (output is CarState)
        }
    }
    val txWeJustSignedId = subFlow(signedTransactionFlow)
    return subFlow(ReceiveFinalityFlow(counterpartySession, txWeJustSignedId.id))
}
```
{{% /tab %}}

{{< /tabs >}}




{{< note >}}
The `checkTransaction` function should be used *only* to model business logic. A contract’s `verify` function should be used to define what is and is not possible within a transaction.

{{< /note >}}


* The completed `CarFlow.kt` should look like this:{{< tabs name="tabs-12" >}}
{{% tab name="kotlin" %}}
```kotlin
package com.template.flows

import co.paralleluniverse.fibers.Suspendable
import com.template.contracts.CarContract
import com.template.states.CarState
import net.corda.core.contracts.Command
import net.corda.core.contracts.UniqueIdentifier
import net.corda.core.contracts.requireThat
import net.corda.core.flows.*
import net.corda.core.identity.Party
import net.corda.core.node.ServiceHub
import net.corda.core.transactions.SignedTransaction
import net.corda.core.transactions.TransactionBuilder

@InitiatingFlow
@StartableByRPC
class CarIssueInitiator(
        val owningBank: Party,
        val holdingDealer: Party,
        val manufacturer: Party,
        val vin: String,
        val licensePlateNumber: String,
        val make: String,
        val model: String,
        val dealershipLocation: String
) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {

        val notary = serviceHub.networkMapCache.notaryIdentities.first()
        val command = Command(CarContract.Commands.Issue(), listOf(owningBank, holdingDealer, manufacturer).map { it.owningKey })
        val carState = CarState(
                owningBank,
                holdingDealer,
                manufacturer,
                vin,
                licensePlateNumber,
                make,
                model,
                dealershipLocation,
                UniqueIdentifier()
        )

        val txBuilder = TransactionBuilder(notary)
                .addOutputState(carState, CarContract.ID)
                .addCommand(command)

        txBuilder.verify(serviceHub)
        val tx = serviceHub.signInitialTransaction(txBuilder)

        val sessions = (carState.participants - ourIdentity).map { initiateFlow(it as Party) }
        val stx = subFlow(CollectSignaturesFlow(tx, sessions))
        return subFlow(FinalityFlow(stx, sessions))
    }
}

@InitiatedBy(CarIssueInitiator::class)
class CarIssueResponder(val counterpartySession: FlowSession) : FlowLogic<SignedTransaction>() {

    @Suspendable
    override fun call(): SignedTransaction {
        val signedTransactionFlow = object : SignTransactionFlow(counterpartySession) {
            override fun checkTransaction(stx: SignedTransaction) = requireThat {
                val output = stx.tx.outputs.single().data
                "The output must be a CarState" using (output is CarState)
            }
        }
        val txWeJustSignedId = subFlow(signedTransactionFlow)
        return subFlow(ReceiveFinalityFlow(counterpartySession, txWeJustSignedId.id))
    }
}
```
{{% /tab %}}

{{< /tabs >}}




## Step Five: Update the Gradle build

The Gradle build files must be updated to change the node configuration.


* Navigate to the `build.gradle` file in the root `cordapp-template-kotlin` directory.
* In the `deployNodes` task, update the nodes to read as follows:>
{{< tabs name="tabs-13" >}}
{{% tab name="kotlin" %}}
```kotlin
node {
    name "O=Notary,L=London,C=GB"
    notary = [validating : false]
    p2pPort 10002
    rpcSettings {
        address("localhost:10003")
        adminAddress("localhost:10043")
    }
}
node {
    name "O=Dealership,L=London,C=GB"
    p2pPort 10005
    rpcSettings {
        address("localhost:10006")
        adminAddress("localhost:10046")
    }
    rpcUsers = [[ user: "user1", "password": "test", "permissions": ["ALL"]]]
}
node {
    name "O=Manufacturer,L=New York,C=US"
    p2pPort 10008
    rpcSettings {
        address("localhost:10009")
        adminAddress("localhost:10049")
    }
    rpcUsers = [[ user: "user1", "password": "test", "permissions": ["ALL"]]]
}
node {
    name "O=BankofAmerica,L=New York,C=US"
    p2pPort 10010
    rpcSettings {
        address("localhost:10007")
        adminAddress("localhost:10047")
    }
    rpcUsers = [[ user: "user1", "password": "test", "permissions": ["ALL"]]]
}
```
{{% /tab %}}

{{< /tabs >}}





The `nodeDefaults` defines what CorDapps are installed on the nodes by default. To install additional CorDapps on the nodes, update the `nodeDefaults` definition, or add the CorDapps to each node definition individually.



* Save the updated `build.gradle` file.


## Step Six: Deploying your CorDapp locally

Now that the CorDapp code has been completed and the build file updated, the CorDapp can be deployed.


* Open a terminal and navigate to the root directory of the project.
* To deploy the nodes on Windows run the following command: `gradlew clean deployNodes`


To deploy the nodes on Mac or Linux run the following command: `./gradlew clean deployNodes`



* To start the nodes on Windows run the following command: `build\nodes\runnodes`


To start the nodes on Mac/Linux run the following command: `build/nodes/runnodes`

{{< note >}}
Maintain window focus on the node windows, if the nodes fail to load, close them using `ctrl + d`. The `runnodes` script opens each node directory and runs `java -jar corda.jar`.

{{< /note >}}


* To run flows in your CorDapp, enter the following flow command from any non-notary terminal window:>
{{< tabs name="tabs-14" >}}
{{% tab name="kotlin" %}}
```kotlin
``flow start CarIssueInitiator owningBank: BankofAmerica, holdingDealer: Dealership, manufacturer: Manufacturer, vin: "abc", licensePlateNumber: "abc1234", make: "Honda", model: "Civic", dealershipLocation: "NYC"``
```
{{% /tab %}}

{{< /tabs >}}



* To check that the state was correctly issued, query the node using the following command:


`run vaultQuery contractStateType: com.template.states.CarState`

The vault is the node’s repository of all information from the ledger that involves that node, stored in a relational model. After running the query, the terminal should display the state created by the flow command. This command can be run from the terminal window of any non-notary node, as all parties are participants in this transaction.



## Next steps

The getting started experience is designed to be lightweight and get to code as quickly as possible, for more detail, see the following documentation:


* [CorDapp design best practice](writing-a-cordapp.md)
* [Testing CorDapp contracts](tutorial-test-dsl.md)

For operational users, see the following documentation:


* [Node structure and configuration]({{% ref "./corda-nodes-index.md" %}})
* [Deploying a node to a server](deploying-a-node.md)
* [Notary documentation](running-a-notary.md)
