---
date: '2020-07-15T12:00:00Z'
title: Corda 5 Dev Preview 1
section_menu: corda-5-dev-preview
project: corda
version: 'Corda 5 Developer Preview 1'
menu:
  versions:
    weight: -648
  corda-5-dev-preview:
    weight: 10
aliases:
- ../5.0-dev-preview-1.html
- ./5.0-dev-preview-1.html
- 5.0-dev-preview-1.html
- ../5.0-dev-preview-1/overview.html
- ./5.0-dev-preview-1/overview.html
- 5.0-dev-preview-1/overview.html
- ../5.0-dev-preview-1/index.html
- ./5.0-dev-preview-1/index.html
- 5.0-dev-preview-1/index.html
---
# Corda 5 Developer Preview 1

{{< attention >}}
This developer preview of Corda 5 has been replaced by Developer Preview 2. Refer to the [Developer Preview 2 documentation](https://docs.r3.com/en/platform/corda/5.0-dev-preview-2.html).
{{< /attention >}}

Corda is a trust technology platform. You can use it to build verified blockchain networks, create applications that represent your business on the network, and interact in a completely secure ecosystem.

This is a developer preview of Corda's next major iteration, Corda 5. Here, you can experiment with three key aspects of Corda 5:

* A modular API structure. This lets you [build applications to use on Corda (CorDapps) and test them efficiently](../../../../en/platform/corda/5.0-dev-preview-1/tutorials/overview.md).
* An HTTPS API, based on Open API principles, that allows you [control nodes, and initiate flows remotely](../../../../en/platform/corda/5.0-dev-preview-1/nodes/nodes-homepage.md).
* Package your CordApps with a new Gradle plugin that allows for multi-tenancy applications in future releases.

{{< note >}}
**Your feedback helps.** Please [send the Documentation Team an e-mail](mailto:docs@r3.com) with your feedback so we can make the upcoming versions of Corda work harder for you than ever.
{{< /note >}}

In this preview, you can:

* Deploy a local Corda 5 developer network for building and testing CorDapps.
* Trial a new Corda 5 sample CorDapp, using HTTPS node operations via a new RESTful API.
* Follow a step-by-step guide to create a Corda 5 CorDapp.
* Try the new CorDapp packaging plugin to convert your code to the Corda 5 `.cpk` file—the new extension for Corda 5 CorDapps.
* Experiment with the discovery and identity API for network memberships.

{{< warning >}}
This is a developer preview, and not for production or commercial deployment. You should perform all tasks in the tutorials and any further development work locally only.
{{< /warning >}}

## New concepts in Corda 5 Developer Preview

If you have worked with Corda before, you will see major advances when you start developing in the Corda 5 Developer Preview. Previous versions of Corda focused on building an ecosystem of networks. Corda 5 is application-focused, making it easier to build, test, and distribute CorDapps.

To simplify the CorDapp development process, Corda 5 breaks the operational and developmental power of Corda into layers. Allowing you to choose the technologies that matter to you.

Notably, as a developer, you will notice a substantial restructuring of the available APIs for creating CorDapps and initiating flows remotely using HTTPS.

A full list of what's new in Corda 5 Developer Preview:

- A Modular API. Corda's core API module has been split into packages and versioned.
- Dependency upgrades to Gradle 6, Java 11, and Kotlin 1.4. This enables the latest Gradle CorDapp packaging plugins, letting you create CorDapps faster.
- Node interaction upgrades. You can interface with a node using HTTP and auto-generate CorDapp endpoints.
- Upgrades to packaging:
  - CorDapps are no longer packaged as `.jar` files.
  - A Corda Package, `.cpk` is now the unit of software that executes within a single sandbox.
  - CorDapps are a set of versioned `.cpks` that define a deployable application.
- A new integration test framework that reflects real node behavior.
- An API for pluggable uniqueness service (notary). This is interface-only.

### CorDapp Development changes

The Corda 5 flow interface and CorDapp packaging makes building CorDapps simpler and more concise. The Flow interface allows you to create flows and inject your preferred methods (now called Corda Services) into the flow.

The `FlowLogic` abstract class has been broken up into a set of smaller interfaces.  In place of `FlowLogic`, you can now implement the `Flow` interface which holds the `call` method.

Methods that previously existed on `FLowlogic` have been broken out into injectable **Corda services**.

The move away from an abstract class to injectable services allows you to use only the services you need. Features that you don't use will not need to be present on your flow classes.

Packaging your code has been made easier with a new CorDapp packaging plugin. Individual CorDapps can be bundled together to create your enterprise solution using a simple Command Line Interface (CLI).

### Network and node changes

You can easily bootstrap a local Corda 5 network using the new CLI. This deployment creates a developer network in which you can test your own Corda 5 CorDapps or try the new node HTTP commands to initiate flows on a demo CorDapp.

## Next steps

Dive into the [tutorials to get started with the Corda 5 Developer Preview](../../../../en/platform/corda/5.0-dev-preview-1/tutorials/overview.md).
