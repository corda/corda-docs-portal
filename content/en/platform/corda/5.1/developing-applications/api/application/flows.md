---
date: '2023-08-10'
version: 'Corda 5.1'
title: "application.flows"
menu:
  corda51:
    identifier: corda51-api-app-flows
    parent: corda51-api-application
    weight: 2000
section_menu: corda51
---
# net.corda.v5.application.flows
The `flows` package contains interfaces and annotations for defining {{< tooltip >}}flows{{< /tooltip >}}. The main interfaces are:

* The <a href="../../../../../../api-ref/corda/{{<version-num>}}/net/corda/v5/application/flows/ClientStartableFlow.html" target="_blank">`ClientStartableFlow`</a> is for flows expected to be started via the REST API.
* The  <a href="../../../../../../api-ref/corda/{{<version-num>}}/net/corda/v5/application/flows/ResponderFlow.html" target="_blank">`ResponderFlow`</a> for flows expected to be started via a peer-to-peer session. Annotations in this package are used to customize flow behaviour by marking properties for service injection (<a href="../../../../../../api-ref/corda/{{<version-num>}}/net/corda/v5/application/flows/CordaInject.html" target="_blank">`CordaInject`</a>) or marking either side of a peer-to-peer session (<a href="../../../../../../api-ref/corda/{{<version-num>}}/net/corda/v5/application/flows/InitiatingFlow.html" target="_blank">`InitiatingFlow`</a> and <a href="../../../../../../api-ref/corda/{{<version-num>}}/net/corda/v5/application/flows/InitiatedBy.html" target="_blank">`InitiatedBy`</a>).

For more information, see the documentation for the package in the <a href="../../../../../../api-ref/corda/{{<version-num>}}/net/corda/v5/v5/application/flows/package-summary.html" target=" blank">Java API documentation</a>.
