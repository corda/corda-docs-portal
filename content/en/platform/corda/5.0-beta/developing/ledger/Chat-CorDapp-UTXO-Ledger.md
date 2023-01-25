---
date: '2023-01-23'
title: "Chat CorDapp"
menu:
  corda-5-beta:
    parent: corda-5-beta-ledger
    identifier: corda-5-beta-chatstate
    weight: 5000
section_menu: corda-5-beta
---
## ChatState

The foundation for the Chat app is the ChatState which is the data model for facts recorded to the ledger. It can be represented in the CDL as follows:

{{< 
  figure
	 src="images/chat-state.png"
	 figcaption="Data model for facts recorded to the ledger"
>}}


Where:

* id is a unique identifier for the chat, it is the equivalent of a linearId in Corda 4, in other words it is the common identifier for all the states in the backchain for a particular chat between two participants. (LinearStates and LinearId are not implemented yet in Corda 5 as of Beta-1).

* chatName is a human readable name for the chat, it does not guarantee uniqueness.

* messageFrom is the MemberX500Name for the virtual node which created this ChatState.

* message is the message in the Chat.

* participants is the list of PublicKeys belonging to the Vnodes of the participants of the chat.

The history of a chat will be recorded in the backchain of the chat.

### Chat Smart Contract

The Smart Contract (combination of the ChatState and ChatContract) can be represented by a simple Smart Contract View diagram:

{{< 
  figure
	 src="images/chat-smart-contract-view.png"
	 figcaption="Smart Contract View diagram""
>}}

Points to note:

* In CDL the arrows represent transactions with the indicated command type. The state at the beginning of the arrow represents the input state, the state at the end of the arrow represents the output state for the transaction.
* There is no ChatState status in this simple design.

* The multiplicities (numbers on the arrows) indicate that for the create command there should be no input state and one output ChatState.

* The multiplicities for the update command indicates there should be one input ChatState and one output ChatState.

* SC: indicates the signing constraint, that is who needs to sign the transaction. In this case both participants for both the create and update commands.

* The Universal Constraint applies to all transactions, in this case that there should always be only two  participants in the ChatState.

### Chat State Evolution

The evolution of the ledger when stepping through the walkthrough steps can be shown using the CDL State evolution view:

{{< 
  figure
	 src="images/chat-state-evolution-view.png"
	 figcaption="CDL State evolution view""
>}}

* The Create transaction has no input and starts a new chat with a unique id. The id operates similarly to the Corda 4  LinearStateId, which has not been implemented yet in Corda 5.
* Each Update transaction creates the new ChatState as an output and consumes the previous ChatState as an input.
* To recreate the historic conversation the back chain is traversed from newest (unconsummed) state to oldest.

### Chat Flows

There are six flows in the Chat Application:

{{< table >}}
 | Flow                      | Flow type        | Inputs |            Action|
 |---------------------------|------------------|--------------------|-----------------|
 | CreateNewChatFlow         | RPCStartableFlow | chatName, otherMember, message   | Forms a draft transaction using the transaction builder, which creates a new ChatState with the details provided. Signs the draft transaction with the VNodes first Ledger Key. Calls FinalizeChatSubFlow which finalizes the transaction.|
 | UpdateChatFlow            | RPCStartableFlow | id, message        | Locates the last message in the backchain for the given id. Creates a draft transaction which consumes the last message in the chain and creates a new chatState with the latest message. Signs the draft transaction with the VNodes first Ledger Key. Calls FinalizeChatSubFlow which finalises the transaction.  |
 | ListChatsFlow             | RPCStartableFlow | <none>   |Calls FinalizeChatSubFlow which finalises the transaction.|
 | GetChatsFlow              | RPCStartableFlow | id, numberofRecords | Reads the backchain to a depth of ‘numberOfRecords’ for a given id. Returns the list of messages together with who sent them. |
 | FinalizeChatFlow          | SubFlow          | signedTransaction (to finalize), otherMember | The common subflow used by both CreateNewChatFlow and UpdateChatFlow. This removes the need to duplicate the responder code.  Sets up a session with the FinalizeChatResponderFlow and calls the finality() function. finality()/ receiveFinality() functions, collects required signatures, notarises the transaction and stores the finalized transaction to the respective vaults. |
 | FinalizeChatResponderFlow | ResponderFlow    | FlowSession           | Runs the receiveFinality() function which performs the responder side of the finality() function. ReceiveFinality() takes a Lambda verifier which runs validations on the transactions. The validator checks for banned words and checks that the message comes from the same party as the messageFrom field. |
 {{< /table >}}
