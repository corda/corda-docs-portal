---
date: '2023-02-10'
title: "application.messaging"
menu:
  corda52:
    identifier: corda52-api-app-messaging
    parent: corda52-api-application
    weight: 5000
---
# net.corda.v5.application.messaging
The `messaging` package provides services and types for creating and working with peer-to-peer sessions. The <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/messaging/FlowMessaging.html" target="_blank">`FlowMessaging`</a> service allows you to create new sessions with counterparties. Once created, a <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/messaging/FlowSession.html" target="_blank">`FlowSession`</a> can be used to send and receive messages from a peer.

Corda creates a `FlowSession` instance for a {{< tooltip >}}flow{{< /tooltip >}} created via a peer-to-peer message (one implementing `ResponderFlow` in the `flows` package) for communication with the peer that initiated the flow.

For more information, see the documentation for the package in the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/messaging/package-summary.html" target=" blank">Java API documentation</a>.
