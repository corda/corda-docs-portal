---
date: '2020-07-15T12:00:00Z'
title: "Services"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-services
    weight: 5500
section_menu: corda-5-dev-preview
---

When building your CorDapps, make use of the suite of APIs, or Corda Services , which can be injected into your flows and other Corda Services. In the Corda 5 Developer Preview, these APIs are modulated to enable you to build quickly and only use the services your business logic requires.

You can also write your own custom Corda Services .


Corda Services are classes that provide methods to both flows and other Corda Services. Each service and method allows flows and Corda Services to perform specific functions.

In technical terms, a Corda Service is any class that needs to be a long-lived singleton that can be injected into flows and other services via the @CordaInject dependency injection mechanism. You can use them to create classes external to flows where you can logically group code that isn’t directly related to the execution of a flow.
