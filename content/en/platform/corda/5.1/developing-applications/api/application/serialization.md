---
date: '2023-02-10'
title: "application.serialization"
menu:
  corda51:
    identifier: corda51-api-app-serialization
    parent: corda51-api-application
    weight: 7000
---
# net.corda.v5.application.serialization
The `serialization` package provides services for working with data marked as `@CordaSerializable`, in order to render it into a form suitable for sending to a counterparty. Usually this is handled by the messaging layer (see the <a href="messaging.md">`messaging` package</a>), but if you require access to serialization directly it is exposed here. The main service for serialization is the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/serialization/SerializationService.html" target="_blank">`SerializationService`</a>. At present, the only scheme available via this service is AMQP.
