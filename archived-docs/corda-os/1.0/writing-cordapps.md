---
aliases:
- /releases/release-V1.0/writing-cordapps.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-1-0:
    identifier: corda-os-1-0-writing-cordapps
    parent: corda-os-1-0-building-a-cordapp-index
    weight: 1020
tags:
- cordapps
title: Writing a CorDapp
---


# Writing a CorDapp

When writing a CorDapp, you are writing a set of files in a JVM language that defines one or more of the following
Corda components:


* States (i.e. classes implementing `ContractState`)
* Contracts (i.e. classes implementing `Contract`)
* Flows (i.e. classes extending `FlowLogic`)
* Web APIs
* Services


## CorDapp structure

Your CorDapp project’s structure should be based on the structure of the
[Java Template CorDapp](https://github.com/corda/cordapp-template-java) or the
[Kotlin Template CorDapp](https://github.com/corda/cordapp-template-kotlin), depending on which language you intend
to use.

The `src` directory of the Template CorDapp, where we define our CorDapp’s source-code, has the following structure:

```kotlin
src
├── main
│   ├── java
│   │   └── com
│   │       └── template
│   │           ├── Main.java
│   │           ├── api
│   │           │   └── TemplateApi.java
│   │           ├── client
│   │           │   └── TemplateClientRPC.java
│   │           ├── contract
│   │           │   └── TemplateContract.java
│   │           ├── flow
│   │           │   └── TemplateFlow.java
│   │           ├── plugin
│   │           │   └── TemplatePlugin.java
│   │           ├── service
│   │           │   └── TemplateService.java
│   │           └── state
│   │               └── TemplateState.java
│   └── resources
│       ├── META-INF
│       │   └── services
│       │       ├── net.corda.core.serialization.SerializationWhitelist
│       │       └── net.corda.webserver.services.WebServerPluginRegistry
│       ├── certificates
│       │   ├── sslkeystore.jks
│       │   └── truststore.jks
│       └──templateWeb
│           ├── index.html
│           └── js
│               └── template-js.js
└── test
    └── java
        └── com
            └── template
                └── contract
                    └── TemplateTests.java
```

