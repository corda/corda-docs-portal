---
title: "Building CorDapps"
date: 2023-07-26
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cordapp-dev-build
    parent: corda5-key-concepts-cordapp-dev
    weight: 2000
section_menu: corda5
---

# Tech Stack

CorDapps, consisting of flows, and optionally states and contracts, are “pieces of code” hosted by the Corda runtime. This code can be written in a JVM compatible language. Java and Kotlin are officially supported. Currently, Corda 5 supports CorDapps compiled using Azul Zulu JDK 17. Other OpenJDK compatible Java 11 SDKs may also work but have not been fully tested.

CorDapps are simply code, written in a JVM compatible language, compiled into a special type of JAR called a {{< tooltip >}}CPK{{< /tooltip >}}. These CPKs are compiled using the [Gradle plugin]({{< relref "../../../developing-applications/packaging/cpk-plugin.md" >}}). See the [Corda 5 Samples repository](https://github.com/corda/corda5-samples) for an example of a typical CorDapp.

{{< 
  figure
	 src="cpks.png"
   width="50%"
	 figcaption="Example CPKs"
>}}

A CorDapp must be installed in a Corda Cluster to make it available to virtual nodes. To enable this, the CorDapp must be packaged up into a {{< tooltip >}}CPB{{< /tooltip >}}, which comprises of all CPKs necessary for a CorDapp to be complete, and their dependencies. 
The CPB must then be combined with network metadata into a {{< tooltip >}}CPI{{< /tooltip >}} before it can be installed in the cluster. For more information, see [Packaging]({{< relref "../../../developing-applications/packaging/_index.md" >}}).

{{< 
  figure
	 src="packaging.png"
   width="50%"
	 figcaption="CorDapp Packaging"
>}}

While CPBs and CPIs use the `.cpb` and `.cpi` file extension, the files conform to the JAR file specification, and therefore JAR tools can be used to inspect them. For example:

```
❯ jar tf iou-app.cpb
META-INF/MANIFEST.MF
META-INF/CORDAPP.SF
META-INF/CORDAPP.EC
META-INF/
workflows-1.0-SNAPSHOT.jar
contracts-1.0-SNAPSHOT.jar
```

## Corda Programming Model

Using a JVM compatible language for creating workflows, states, and contracts is very powerful. As a CorDapp developer, you have very effective languages such as Java and Kotlin at your disposal, as well as the rich JVM ecosystem.

Corda enhances the programming experience not just by offering access to a familiar tech stack and tooling, but also by introducing a familiar programming model to distributed application development.

Consider the previous IOU issue flow example. The following is the code for the initiating flow:

```kotlin
...

// Create the IOUState from the input arguments and member information.
val iou = IOUState(
    amount = flowArgs.amount.toInt(),
    lender = lenderInfo.name,
    borrower = myInfo.name,
    paid = 0,
    linearId = UUID.randomUUID(),
    listOf(myInfo.ledgerKeys[0],lenderInfo.ledgerKeys[0])
)

...
// Convert the transaction builder to a UTXOSignedTransaction. Verifies the content of the
// UtxoTransactionBuilder and signs the transaction with any required signatories that belong to
// the current node.
val signedTransaction = txBuilder.toSignedTransaction()

...
// Calls the Corda provided finalise() function which gathers signatures from the counterparty,
// notarises the transaction and persists the transaction to each party's vault.
// On success returns the ID of the transaction created.
val finalizedSignedTransaction = ledgerService.finalize(
   signedTransaction,
   sessions
)
...
```

Some detail has been omitted for simplicity, but the above code highlights three important stages of the initiating flow:

1. Creating the state
2. Signing the transaction
3. Requesting the peer(s) to review the transaction and sign it

The responder flow looks something like this:

```kotlin
// Calls receiveFinality() function which provides the responder to the finalise() function
// in the Initiating Flow. Accepts a lambda validator containing the business logic to decide whether
// the responder should sign the transaction.
val finalizedSignedTransaction = ledgerService.receiveFinality(session) { ledgerTransaction ->

    val state = ledgerTransaction.getOutputStates(IOUState::class.java).singleOrNull() ?:
    throw CordaRuntimeException("Failed verification - transaction did not have exactly one output IOUState.")

    ... // decide whether to "accept" this transaction
}
```

The following diagram describes this scenario:

{{< 
  figure
	 src="iou-model.png"
   width="80%"
	 figcaption="IOU App Programming Model"
>}}

## Continuance

As shown in the previous diagram, what seem like simple function calls in a CorDapp often represent complex “out-of-process” operations.
The most obvious one being the request to another party to respond. 
This involves a peer-to-peer session to initiate the responder flow at the other party’s Corda runtime. 
In the best case scenario, the other party responds quickly, but as with any distributed application, this cannot be guaranteed. 
The other party may, for example, suffer from an infrastructure failure and be unavailable for a short period of time, or the responder flow may simply be slow, maybe it integrates with another downstream system as part of the responder flow, with each “hop” potentially contributing to a slow response.
This unpredictability poses a challenge on the initiating side. 
Firstly, “waiting” can be expensive and resources should be made available as soon as possible so they can be reused. 
Secondly, a long wait increases the probability of being interrupted.

In order to avoid these long waits, and also to facilitate building fault tolerant workflows, Corda uses a suspend/resume model. 
In practice, every time one of these “out-of-process” operations happens, such as, signing, persisting, or peer-to-peer communications, the flow should suspend and a checkpoint created. 
When the out-of-process operation completes, the checkpoint can be restored and the flow resumes from this checkpoint.

Returning to the IOU example, the following diagram shows suspension and resumption points in the flow:

{{< 
  figure
	 src="iou-points.png"
   width="75%"
	 figcaption="IOU App Suspension and Resumption points"
>}}

Corda manages suspending and resuming. However, it may be necessary for a CorDapp Developer to inform Corda of certain suspension points. This is achieved by adding the `@Suspendable` annotation to functions. 

## Workflow Versus Contract

CorDapps typically consist of flows, states, and contracts, all written in a JVM compatible language, and deployed as JARs. Corda, however, makes a distinction between workflow and contract CPKs (JARs). This is identified in the Gradle CorDapp configuration.
Workflow CPK:
```
cordapp {
    workflow {
        name "WorkflowsModuleNameHere"
        versionId 1
        vendor "VendorNameHere"
    }
}
```
Contract CPK:
```
cordapp {
    contract {
        name "ContractsModuleNameHere"
        versionId 1
        vendor "VendorNameHere"
    }
}
```

The following rules identify which CPK type is applicable:
* Flow code (anything implementing the [Flow interface]({{< relref "../../../developing-applications/api/application/flows.md" >}})) can only exist in a workflow CPK.
* Contracts and states (implementing `Contract` and `ContractState`) can only exist in a contract CPK.
* Entity classes used in the [persistence]({{< relref "../../../developing-applications/api/application/persistence.md" >}}) API (annotated with `@Entity`), along with their database migration scripts, can only exist in a contract CPK.
* Workflow CPKs can reference contract CPKs, but never the other way around.

As a CorDapp Developer, it is usually sufficient to remember the above rules. 
However, to understand a little bit more about why there are different CPKs, you must understand where and when the code in these CPKs is executed.
The distributed architecture of Corda is based on worker processes. 
There are different types of workers that each have their own operational responsibility and, because it is possible for each type of worker to scale horizontally, they are all stateless.

{{< 
  figure
	 src="workers.png"
   width="75%"
	 figcaption="Corda Workers"
>}}

Two of these worker types, the flow worker and the database worker, are special because they host CorDapp code. 
They act as an application server for the code in the CPKs that are part of the CorDapp. 
This code runs inside a Corda sandbox. There are three different types of sandboxes:
* Flow - the flow engine host. This exists in the flow worker and is responsible for executing all flow code.
* Persistence - hosted by the database worker. This takes instructions from the flow engine to persist states or custom objects. For this reason, it needs to parse custom entity classes that are part of the CorDapp.
* Verify - this is hosted by the flow worker but is exclusively responsible for contract verification.

This relates to the separation of contract and workflow CPKs, as follows:
* Flow sandbox — requires both workflow and contract CPKs in order to execute an initiating or responder flow. 
* Persistence sandbox — has special privileges as it is allowed to interact with the virtual node’s databases. However, it only requires the custom entities and states that are part of the contract CPK. Workflow CPKs are never loaded into the persistence sandbox.
* Verify sandbox — exclusively used for verifying the contract. Therefore, it only needs the contract CPK. Workflow CPKs are never loaded into the verify sandbox. During backchain verification, it is sometimes necessary to verify “old” states that require the previous version of the contract to verify. This is another reason why it is wise to separate contract CPKs from workflow CPKs as their version lifecycle may be different.
