---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-cordapps
tags:
- cordapp
title: CorDapp Structure
weight: 30
---


# CorDapp Structure

In this document, you will find:
* A description of CorDapp structures and why specific structures work.
* A guide to R3's CorDapp templates and how they are structured.
* An explanation of how to alter a CorDapp template for production use.

## Glossary

*module*
    A module is a software component or part of a program that contains one or more routines.
*class*
    A class defines a set of properties and methods that are common to all objects of one type. Classes are written in a defined structure to create a Java or Kotlin object.
*dependency*  
    When one object uses another object's function.


CorDapp source code is typically divided into two or more modules. Each module is compiled into a separate `.jar`. Together, these `.jar`s form a single CorDapp.

CorDapps are usually independent structures which contain all the classes they need to run. However, some CorDapps are designed as libraries for other CorDapps, and cannot be run independently.

The best-practice structure for most CorDapps is:

* One module containing *only* the CorDapp’s contracts and/or states and core data types. This is the portion of the CorDapp that is published to the ledger.
* A second module containing all other app components, such as flows and support code. This module is not attached to any transactions and can be structured however you like.

If you were to put all your states, contracts, flows, and support code into a single Java or Kotlin module, your entire CorDapp would be published to the ledger. That would cause the ledger to interpret any changes to your flows or support code as a new CorDapp, potentially triggering unnecessary upgrade procedures.

However, some CorDapp use cases call for a different structure. Common examples include:

* Library CorDapps. These only contain contracts and states in a single module.
* CorDapps with multiple sets of contracts and states that **do not** depend on each other. Place each independent set of
contracts and states in its own module to reduce transaction size.
* CorDapps with multiple sets of contracts and states that **do** depend on each other. Keep all of the contracts and states in the same module, or create separate modules for each set which depend on each other.



## CorDapp Templates

R3 provides CorDapp templates in Java and Kotlin to help you get started:

* [Java CorDapp template ](https://github.com/corda/cordapp-template-java)
* [Kotlin CorDapp template ](https://github.com/corda/cordapp-template-kotlin)

Use the branch of the template that corresponds to the major version of Corda that you are using. For example,
if you are building a CorDapp on Corda 4.10, use the `release-V4` branch.


### Build system

The templates are built using Gradle. A Gradle wrapper is provided in the `wrapper` folder, and the dependencies are
defined in the `build.gradle` files. See [Building and installing a CorDapp](../../../../../../en/platform/corda/4.10/enterprise/cordapps/cordapp-build-systems.md) for more information.

No templates are currently provided for Maven or other build systems.


### Modules

The templates are split into two modules:

* A `cordapp-contracts-states` module containing the contracts and states.
* A `cordapp` module containing the classes that depends on the `cordapp-contracts-states` module.

These modules will be compiled into two `.jar`s - a `cordapp-contracts-states` `.jar` and a `cordapp` `.jar`. Together, these form the template CorDapp.


#### Module one: `cordapp-contracts-states`

Here is the structure of the `src` directory for the `cordapp-contracts-states` module of the Java template:

```none
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

These are definitions for classes that you expect to send over the network. They will be compiled into their own
CorDapp.


#### Module two: `cordapp`

Here is the structure of the `src` directory for the `cordapp` module of the Java template:

```none
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

* `main` contains the CorDapp source.
* `test` contains example unit tests and a node driver for running the CorDapp from IntelliJ.
* `integrationTest` contains an example integration test.

`main` contains the following directories:

* `java`, which contains the CorDapp's source code:

    * `TemplateFlow.java`, which contains a template `FlowLogic` subclass.
    * `TemplateState.java`, which contains a template `ContractState` implementation.
    * `TemplateContract.java`, which contains a template `Contract` implementation.
    * `TemplateSerializationWhitelist.java`, which contains a template `SerializationWhitelist` implementation.
    * `TemplateApi.java`, which contains a template API for the deprecated Corda webserver.
    * `TemplateWebPlugin.java`, which registers the API and front-end for the deprecated Corda webserver.
    * `TemplateClient.java`, which contains a template RPC client for interacting with our CorDapp.


* `resources/META-INF/services`, which contains registries:

    * `net.corda.core.serialization.SerializationWhitelist`, which registers the CorDapp’s serialisation whitelists.
    * `net.corda.webserver.services.WebServerPluginRegistry`, which registers the CorDapp’s web plugins.


* `resources/templateWeb`, which contains a template frontend.

In a production CorDapp:

* Remove the files related to the deprecated Corda webserver (`TemplateApi.java`,
`TemplateWebPlugin.java`, `resources/templateWeb`, and `net.corda.webserver.services.WebServerPluginRegistry`)
and replace them with a production-ready webserver.
* Move `TemplateClient.java` into a separate module to exclude it from the CorDapp.
