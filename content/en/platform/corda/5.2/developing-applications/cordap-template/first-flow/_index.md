---
date: '2023-11-01'
title: "Your First Flow"
description: Learn how to write flows using the CorDapp template.
menu:
  corda52:
    parent: corda52-develop-get-started
    identifier: corda52-flow
    weight: 5000

---
# Your First Flow

The `MyFirstFlow` and `MyFirstResponderFlow` flows are basic flows that illustrate the main features of Corda 5 flows.
Many of the features will be familiar to those Developers who have written Corda 4 {{< tooltip >}}CorDapps{{< /tooltip >}}. However, there are some important differences when using Corda 5:

* Services are injected on an as-needed basis.
* Flows are started via a REST endpoint, rather than a Java client sending Java classes over AMQP.
* Initiating and responder flows are linked with a protocol rather than class names.
* Singletons should be avoided in flow code because there is no guarantee that the same {{< tooltip >}}flow worker{{< /tooltip >}} will continue to execute a flow after it has been check-pointed and restarted.

## MyFirstFlow Use Case

The use case in the example flows is very simple:

1. The initiating flow is called on the initiating node with another member of the {{< tooltip >}}application network{{< /tooltip >}}, the recipient, specified as the input argument.
2. The initiating flow sends the message `Hello from <initiator>.` to the specified recipient.
3. The responder flow receives the message and replies with `Hello <initiator>, best wishes from <responder>.`.
4. The initiator returns the message received from the responder as a String.

## MyFirstFlow Code

The following sections describe the flow code in more detail:
{{< childpages >}}
