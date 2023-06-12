---
date: '2023-02-10'
title: "net.corda.v5.application.messaging"
menu:
  corda-5-beta:
    identifier: corda-5-beta-api-app-messaging
    parent: corda-5-beta-api-application
    weight: 5000
section_menu: corda-5-beta
---

The `messaging` package provides services and types for creating and working with peer-to-peer sessions. The <a href="../../../../../../api-ref/corda/5.0-beta/java/net/corda/v5/application/messaging/FlowMessaging.html" target="_blank">`FlowMessaging`</a> service allows you to create new sessions with counterparties. Once created, a <a href="../../../../../../api-ref/corda/5.0-beta/java/net/corda/v5/application/messaging/FlowSession.html" target="_blank">`FlowSession`</a> can be used to send and receive messages from a peer.

Corda creates a `FlowSession` instance for a flow created via a peer-to-peer message (one implementing `ResponderFlow` in the `flows` package) for communication with the peer that initiated the flow.