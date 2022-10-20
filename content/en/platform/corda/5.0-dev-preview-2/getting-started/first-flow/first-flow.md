---
date: '2022-09-20'
title: "Your First Flow"
menu:
  corda-5-dev-preview2:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-flow
    weight: 5000
section_menu: corda-5-dev-preview2
---

The `MyFirstFlow` and `MyFirstResponderFlow` flows are basic flows that illustrate the main features of Corda 5 flows.
Many of the features will be familiar to those Developers who have written Corda 4 CorDapps. However, there are some important differences when using Corda 5:
* Services are injected on an as-needed basis.
* Flows are started via HTTP RPC, rather than a Java client sending Java classes over AMQP.
* Initiating and responder flows are linked with a protocol rather than class names.
* Singletons should be avoided in flow code because there is no guarantee that the same flow worker will continue to execute a flow after it has been check-pointed and restarted.

It is also worth noting that, as of Developer Preview 2, there is no ledger service available to the flows. This means that you cannot create tokens, transactions, or states yet.

## MyFirstFlow Use Case

The use case in the example is very simple:
1. The initiating flow is called on the initiating node with another member of the application network, the recipient,  specified as the input argument.
2. The initiating flow sends the message "Hello from <initiator>." to the specified recipient.
3. The responder flow receives the message and replies with "Hello <initiator>, best wishes from <responder>."
4. The initiator returns the message received from the responder as a String.
