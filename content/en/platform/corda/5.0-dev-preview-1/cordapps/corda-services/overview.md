---
date: '2020-09-08'
title: Corda Services
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-corda-services
    weight: 1000
project: corda-5
section_menu: corda-5-dev-preview
---


Corda Services are classes that provide methods to both Flows and other Corda Services. Each service and method allow flows and Corda Services to perform specific functions. Use these guides to discover key Corda Services, and the process of injecting those services into flows and other Corda Services.

In technical terms, a Corda Service is any class that needs to be a long-lived singleton that can be injected into flows and other services via the @CordaInject dependency injection mechanism. They can be used to create classes external to flows where you can logically group code that isn't directly related to the execution of a flow.

For a complete overview of each Corda Service, and its methods, use the [Corda 5 Developer Preview API reference](../api/corda-5-dev-preview.html).
