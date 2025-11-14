---
description: "Learn how to integrate Corda into the wider ecosystem using the REST API or the external messaging API."
title: "Integrating Corda into the Wider Ecosystem"
date: 2023-07-26
menu:
  corda51:
    identifier: corda51-cordapp-dev-ecosystem
    parent: corda51-key-concepts-cordapp-dev
    weight: 4000
---

# Integrating Corda into the Wider Ecosystem

Corda is usually deployed as part of a wider ecosystem of applications in a modern enterprise. There are two possible integration points:

* [Corda REST API]({{< relref "#corda-rest-api">}})
* [External Messaging API]({{< relref "#external-messaging-api">}}) {{< enterprise-icon >}}

Each integration point has a specific purpose.

## Corda REST API

The [Corda REST API]({{< relref "../../../reference/rest-api/_index.md">}}) is the primary way in which external applications interact with {{< tooltip >}}CorDapps{{< /tooltip >}}. This API allows external systems to start {{< tooltip >}}flows{{< /tooltip >}}, monitor the flow status, and retrieve the output of a flow. This REST API uses JSON for requests and responses, and flows can output data in any text representations. This provides flexibility to external systems around how they interact with Corda.

Because flows have access to a JVM compatible language along with a REST API, they can be built to create a rich, custom CorDapp not just to initiate flows that interact with peers, but also flows that return or search the data in the {{< tooltip >}}vault{{< /tooltip >}} of a {{< tooltip >}}virtual node{{< /tooltip >}}, for example.

{{<
  figure
	 src="rest-api.png"
   width="40%"
	 figcaption="Corda REST API"
>}}

## External Messaging API {{< enterprise-icon >}}

The [external messaging]({{< relref "../../../developing-applications/external-messaging.md">}}) API provides a second way to interact with external systems. This API allows a CorDapp, from within flow code, to publish a message on a predefined {{< tooltip >}}Kafka{{< /tooltip >}} topic which can then be consumed by an external system. This provides an integration point from within a CorDapp, as opposed to the REST API which provides integration points around a CorDapp.

{{< version >}} provides only outbound connectivity.
That is, a flow can send a message, but not receive one.
A future version may support both send and send-and-receive messages.

{{<
  figure
	 src="external-messaging.png"
   width="40%"
	 figcaption="External Messaging API"
>}}
