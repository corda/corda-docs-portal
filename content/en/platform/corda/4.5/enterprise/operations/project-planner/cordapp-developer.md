---
date: '2020-06-18T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-ops-project-planning
tags:
- operations
- deployment
- planning
title: CorDapp developer project planning
weight: 100
---

# CorDapp development project planning

When planning to develop a CorDapp, consider the following factors:

- CorDapp development requirements
- CorDapp development and testing environments

## Prerequisites for CorDapp development

There are a number of pre-requisites for CorDapp development.

- You must use the **Java 8 JVM**, version 8u171 and onwards are supported, but version 9 and later is not supported.
- Gradle 5.4.1
- An IDE of your choice. We use IntelliJ because it has strong Kotlin support.
- Git, for running example projects.
- The following operating systems are supported in development:

{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Microsoft Windows|x86-64|10, 8.x|
|Microsoft Windows Server|x86-64|2016, 2012 R2, 2012|
|Apple macOS|x86-64|10.9 and above|

{{< /table >}}


## CorDapp testing and performance

When developing CorDapps, you should have three initial environments:

1. A development environment.
2. An initial testing environment.
3. A more fully-featured performance and verification testing environment.

### Development environment

A CorDapp development environment can be hosted on a typical development machine, running Windows, Linux, or macOS.

For more information on developing CorDapps, see [developing CorDapps](../../cordapps/cordapp-overview.md/).

### Testing environment

While in development a CorDapp should be regularly tested using a local testing environment to ensure the flows CorDapp
is delivering the intended function. Nodes can be created locally using the network bootstrapper tool.

A local testing environment should use nodes in **devMode** with no other network components.

For more information on testing CorDapps, see [debugging and testing](../../cordapps/debugging-a-cordapp.md/).
