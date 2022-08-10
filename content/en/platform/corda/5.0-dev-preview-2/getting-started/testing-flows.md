---
date: '2020-07-15T12:00:00Z'
title: "Testing and debugging flows"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-test-flows
    weight: 4000
section_menu: corda-5-dev-preview
---


As a CorDapp developer,
I want to be able to run test against my flows which identify errors in the code.
I want to be able to test sub-components of the Flow Code in isolation (Unit test)
I want to be able to test individual Flows (single class) with mocked out sub components. (Unit test)
I want to be able to test individual Flows (single class) with mocked out interactions with the counterparty flow (unit Test)
I want to be able to run tests which accurately simulate initiator and responder Flows interacting between Virtual Nodes, with a fast (10s of seconds) turn around. (Flow Tests)
I do not want the overhead of writing large quantities of Mocking code.
So that I can verify that my Flow code executes according to my expectations/ the spec.
**
