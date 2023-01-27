---
date: '2023-01-23'
title: " UXTO Ledger Example CorDapp"
menu:
  corda-5-beta:
    parent: corda-5-beta-utxo-ledger
    identifier: corda-5-beta-chatcordapp
    weight: 1000
section_menu: corda-5-beta
---

## Introduction

The CSDE template includes examples of CorDapp code for a simple UTXO (Unspent Transaction Output) chat application. The chat CorDapp allows pairs of participants on a Corda application network to do the following:

* Create and name a unique bilateral chat between the two virtual nodes.
* Update chats with new messages from either virtual node.
* Obtain a list of chats that the virtual node is a participant in.
* Retrieve a specified number of previous messages from a chat.

There is both a Kotlin and Java implementation of the Chat CorDapp in the respective `csde-cordapp-template-kotlin` and `csde-cordapp-template-java` repos.

## ChatState

The foundation for the Chat app is the ChatState which is the data model for facts recorded to the ledger. It can be represented in the CDL [CorDapp Design Language](../../../../../../../en/tools/cdl/cdl-overview.md) as follows:

{{< figure src="chat-state.png" figcaption="Data model for facts recorded to the ledger" alt="Data model for facts recorded to the ledger" >}}

Where:

* `id` is a unique identifier for the chat, it is the equivalent of a linearId in Corda 4, in other words it is the common identifier for all the states in the backchain for a particular chat between two participants. (`LinearStates` and `LinearId` are not implemented yet in Corda 5 as of Beta-1).

* `chatName` is a human readable name for the chat, it does not guarantee uniqueness.

* `messageFrom` is the `MemberX500Name` for the virtual node which created this ChatState.

* `message` is the message in the Chat.

* `participants` is the list of `PublicKeys` belonging to the vnodes of the participants of the chat.

The history of a chat will be recorded in the backchain of the chat.

### Chat Smart Contract

The Smart Contract (combination of the ChatState and ChatContract) can be represented by a simple Smart Contract View diagram:

{{< figure src="chat-smart-contract-view.png" figcaption="Smart Contract View diagram" alt="Smart Contract View diagram" >}}

 {{< note >}}

* In CDL the arrows represent transactions with the indicated command type. The state at the beginning of the arrow represents the input state, the state at the end of the arrow represents the output state for the transaction.
* There is no ChatState status in this simple design.

* The multiplicities (numbers on the arrows) indicate that for the create command there should be no input state and one output ChatState.

* The multiplicities for the update command indicates there should be one input ChatState and one output ChatState.

* SC: indicates the signing constraint, that is who needs to sign the transaction. In this case both participants for both the create and update commands.

* The universal constraint applies to all transactions, in this case that there should always be only two  participants in the ChatState.

 {{< /note >}}

### Chat State Evolution

The evolution of the ledger when stepping through the walkthrough steps can be shown using the CDL State evolution view:

{{< figure src="chat-state-evolution-view.png" figcaption="CDL state evolution view" alt="CDL state evolution view" >}}

* The Create transaction has no input and starts a new chat with a unique `id`. The `id` operates similarly to the Corda 4  `LinearStateId`, which has not been implemented yet in Corda 5.
* Each update transaction creates the new ChatState as an output and consumes the previous ChatState as an input.
* To recreate the historic conversation the back chain is traversed from newest (unconsummed) state to oldest.

### Chat Flows

There are six flows in the Chat Application:

<table>
<col style="width:20%">
<col style="width:15%">
<col style="width:15%">
<col style="width:50%">
<thead>
<tr>
<th>Flow</th>
<th>Flow type</th>
<th>Inputs</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>CreateNewChatFlow </code></td>
<td><code>RPCStartableFlow </code></td>
<td><code><li>chatName</li><li>otherMember</li><li>message</li></code></td>
<td> <li>Forms a draft transaction using the transaction builder, which creates a new ChatState with the details provided.</li> <li> Signs the draft transaction with the VNodes first Ledger Key.</li><li> Calls <code>FinalizeChatSubFlow</code> which finalizes the transaction.</li></td>
</tr>
<tr>
<td><code>UpdateChatFlow </code></td>
<td><code>RPCStartableFlow </code></td>
<td><code> <li>id</li><li>message</li> </code></td>
<td> <li>Locates the last message in the backchain for the given <code>id</code>.</li><li> Creates a draft transaction which consumes the last message in the chain and creates a new ChatState with the latest message.</li> <li>Signs the draft transaction with the vnodes first Ledger Key.</li><li> Calls <code>FinalizeChatSubFlow</code> which finalises the transaction.</li></td>
</tr>
<tr>
<td><code>ListChatsFlow </code></a></td>
<td><code>RPCStartableFlow </code></td>
<td><code><li>none</li></code></td>
<td><li>Calls <code>FinalizeChatSubFlow</code> which finalises the transaction.</li></td>
</tr>
<tr>
<td><code>GetChatsFlow </code></td>
<td><code>RPCStartableFlow </code></td>
<td><code><li>id</li><li>numberofRecords</li> </code></td>
<td><li>Reads the backchain to a depth of <code>numberOfRecords</code> for a given <code>id</code>.</li><li> Returns the list of messages together with who sent them.</li></td>
</tr>
<tr>
<td><code>FinalizeChatFlow </code></td>
<td><code>SubFlow </code></td>
<td><code><li>signedTransaction (to finalize)</li><li>otherMember</li> </code></td>
<td><li>The common subflow used by both by both <code>CreateNewChatFlow</code> and <code>UpdateChatFlow</code>.</li><li> This removes the need to duplicate the responder code.<li> Sets up a session with the <code>FinalizeChatResponderFlow</code> and calls the <code>finality()</code> function <code>finality()/ receiveFinality(</code> functions, collects required signatures, notarises the transaction, and stores the finalized transaction to the respective vaults.</li></td>
</tr>
<tr>
<td><code>FinalizeChatResponderFlow</code></td>
<td><code>ResponderFlow </code></td>
<td><code><li>FlowSession</li></code></td>
<td><li>Runs the <code>receiveFinality()</code> function which performs the responder side of the finality() function.<code>ReceiveFinality()</code> takes a Lambda verifier which runs validations on the transactions.</li><li> The validator checks for banned words and checks that the message comes from the same party as the <code>messageFrom</code> field.</li></td>
</tr>
</tbody>
</table>


