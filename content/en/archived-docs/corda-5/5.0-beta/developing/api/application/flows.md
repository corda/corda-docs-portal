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

The `flows` package contains interfaces and annotations for defining flows. The main interfaces are <a href="../../../../../../api-ref/corda/5.0-beta/java/net/corda/v5/application/flows/ClientStartableFlow.html" target="_blank">`ClientStartableFlow`</a> for flows expected to be started via the REST API, and <a href="../../../../../../api-ref/corda/5.0-beta/java/net/corda/v5/application/flows/ResponderFlow.html" target="_blank">`ResponderFlow`</a> for flows expected to be started via a peer-to-peer session. Annotations in this package are used to customize flow behaviour by marking properties for service injection (<a href="../../../../../../api-ref/corda/5.0-beta/java/net/corda/v5/application/flows/CordaInject.html" target="_blank">`CordaInject`</a>) or marking either side of a peer-to-peer session (<a href="../../../../../../api-ref/corda/5.0-beta/java/net/corda/v5/application/flows/InitiatingFlow.html" target="_blank">`InitiatingFlow`</a> and <a href="../../../../../../api-ref/corda/5.0-beta/java/net/corda/v5/application/flows/InitiatedBy.html" target="_blank">`InitiatedBy`</a>).
