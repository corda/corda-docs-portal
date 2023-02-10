---
date: '2023-02-10'
title: "net.corda.v5.application.flows"
menu:
  corda-5-beta:
    identifier: corda-5-beta-api-app-flows
    parent: corda-5-beta-api-application
    weight: 2000
section_menu: corda-5-beta
---

The `flows` package contains interfaces and annotations for defining flows. The main interfaces are `RPCStartableFlow` for flows expected to be started via the REST API, and `ResponderFlow` for flows expected to be started via a peer-to-peer session. Annotations in this package are used to customize flow behaviour by marking properties for service injection (`@CordaInject`) or marking either side of a peer-to-peer session (`@InitiatingFlow` and `@InitiatedBy`).