---
date: '2023-02-10'
title: "net.corda.v5.application.serialization"
menu:
  corda-5-beta:
    identifier: corda-5-beta-api-app-serialization
    parent: corda-5-beta-api-application
    weight: 7000
section_menu: corda-5-beta
---

The `serialization` package provides services for working with data marked as `@CordaSerializable`, in order to render it into a form suitable for sending to a counterparty. Usually this is handled by the messaging layer (see the <a href="messaging.md">`messaging` package</a>), but if you require access to serialization directly it is exposed here. The main service for serailization is the <a href="../../../../../../api-ref/corda/5.0-beta/kotlin/application/net.corda.v5.application.serialization/-serialization-service/index.html" target="_blank">`SerializationService`</a>. At present, the only scheme available via this service is AMQP.