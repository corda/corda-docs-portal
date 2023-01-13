---
aliases:
- /releases/release-V3.1/writing-a-cordapp.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-1:
    identifier: corda-os-3-1-writing-a-cordapp
    parent: corda-os-3-1-building-a-cordapp-index
    weight: 1020
tags:
- cordapp
title: Writing a CorDapp
---


# Writing a CorDapp



## Overview

CorDapps can be written in either Java, Kotlin, or a combination of the two. Each CorDapp component takes the form
of a JVM class that subclasses or implements a Corda library type:


* Flows subclass `FlowLogic`
* States implement `ContractState`
* Contracts implement `Contract`
* Services subclass `SingletonSerializationToken`
* Serialisation whitelists implement `SerializationWhitelist`


## Web content and RPC clients

For testing purposes, CorDapps may also include:


* **APIs and static web content**: These are served by Corda’s built-in webserver. This webserver is not
production-ready, and should be used for testing purposes only
* **RPC clients**: These are programs that automate the process of interacting with a node via RPC

In production, a production-ready webserver should be used, and these files should be moved into a different module or
project so that they do not bloat the CorDapp at build time.



## Structure

You should base the structure of your project on the Java or Kotlin templates:


* [Java Template CorDapp](https://github.com/corda/cordapp-template-java)
* [Kotlin Template CorDapp](https://github.com/corda/cordapp-template-kotlin)

The project should be split into two modules:


* A `cordapp-contracts-states` module containing classes such as contracts and states that will be sent across the
wire as part of a flow
* A `cordapp` module containing the remaining classes

Each module will be compiled into its own CorDapp. This minimises the size of the JAR that has to be sent across the
wire when nodes are agreeing ledger updates.


### Module one - cordapp-contracts-states

Here is the structure of the `src` directory for the `cordapp-contracts-states` module:

```kotlin
.
└── main
    └── java
        └── com
            └── template
                ├── TemplateContract.java
                └── TemplateState.java
```

The directory only contains two class definitions:


* `TemplateContract`
* `TemplateState`

These are definitions for classes that we expect to have to send over the wire. They will be compiled into their own
CorDapp.


### Module two - cordapp

Here is the structure of the `src` directory for the `cordapp` module:

```kotlin
.
├── main
│   ├── java
│   │   └── com
│   │       └── template
│   │           ├── TemplateApi.java
│   │           ├── TemplateClient.java
│   │           ├── TemplateFlow.java
│   │           ├── TemplateSerializationWhitelist.java
│   │           └── TemplateWebPlugin.java
│   └── resources
│       ├── META-INF
│       │   └── services
│       │       ├── net.corda.core.serialization.SerializationWhitelist
│       │       └── net.corda.webserver.services.WebServerPluginRegistry
│       ├── certificates
│       └── templateWeb
├── test
│   └── java
│       └── com
│           └── template
│               ├── ContractTests.java
│               ├── FlowTests.java
│               └── NodeDriver.java
└── integrationTest
    └── java
        └── com
            └── template
                └── DriverBasedTest.java
```

The `src` directory is structured as follows:


* `main` contains the source of the CorDapp
* `test` contains example unit tests, as well as a node driver for running the CorDapp from IntelliJ
* `integrationTest` contains an example integration test

Within `main`, we have the following directories:


* `resources/META-INF/services` contains registries of the CorDapp’s serialisation whitelists and web plugins
* `resources/certificates` contains dummy certificates for test purposes
* `resources/templateWeb` contains a dummy front-end
* `java` (or `kotlin` in the Kotlin template), which includes the source-code for our CorDapp

The source-code for our CorDapp breaks down as follows:


* `TemplateFlow.java`, which contains a dummy `FlowLogic` subclass
* `TemplateState.java`, which contains a dummy `ContractState` implementation
* `TemplateContract.java`, which contains a dummy `Contract` implementation
* `TemplateSerializationWhitelist.java`, which contains a dummy `SerializationWhitelist` implementation

In developing your CorDapp, you should start by modifying these classes to define the components of your CorDapp. A
single CorDapp can define multiple flows, states, and contracts.

The template also includes a web API and RPC client:


* `TemplateApi.java`
* `TemplateClient.java`
* `TemplateWebPlugin.java`

These are for testing purposes and would be removed in a production CorDapp.


## Resources

In writing a CorDapp, you should consult the following resources:


* [Getting Set Up](getting-set-up.md) to set up your development environment
* The Hello, World! tutorial to write your first CorDapp
* [Building a CorDapp](cordapp-build-systems.md) to build and run your CorDapp
* The API docs to read about the API available in developing CorDapps
    * There is also a [cheatsheet](cheat-sheet.md) recapping the key types


* The [Flow cookbook](flow-cookbook.md) to see code examples of how to perform common flow tasks
* [Sample CorDapps](https://www.corda.net/samples/) showing various parts of Corda’s functionality

