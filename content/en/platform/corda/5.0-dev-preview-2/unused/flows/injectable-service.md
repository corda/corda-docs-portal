---
date: '2020-07-15T12:00:00Z'
title: "Flow service injection"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-injectable
    parent: corda-5-dev-preview-flows
    weight: 5000
section_menu: corda-5-dev-preview
---

*	Using injectable service

n Corda 5, we’ve moved from the “serviceHub” mega-API-interface to a model where the CorDapp developer chooses which services they need.

Rather than requiring users to directly instantiate each service, we took this opportunity to separate the interface and implementation, so that apps refer to services by their interface, marked with the @CordaInjectable annotation

https://r3-cev.atlassian.net/wiki/spaces/CB/pages/4068573200/Flow+Service+Injection

The methods that previously existed on FlowLogic have been extracted into injectable services. Corda Services contains more information.

To use these services, define a field annotated with the @CordaInject annotation. The system will set the field before the call method is called.
