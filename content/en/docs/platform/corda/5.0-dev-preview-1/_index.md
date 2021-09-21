---
date: '2020-07-15T12:00:00Z'
menu:
  versions:
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
title: Corda 5 Dev Preview
version: 'dev-preview'
---

# Introducing Corda 5 Developer Preview

Corda is a trust technology platform. You can use it to build verified blockchain networks, create applications that represent your business on the network, and interact in a completely secure ecosystem.

This is a developer preview of Corda's next major iteration: Corda 5. You can experiment with two key aspects of the future of Corda:

* A modular API structure. This lets you build applications to use on Corda (CorDapps) and test them efficiently.
* A HTTPS API, based on RESTful principles. This lets you control your node—your presence on a Corda network—remotely.

In this preview, you can:

* Deploy a local Corda 5 developer network for building and testing CorDapps.
* Trial a new Corda 5 sample CorDapp, using HTTPS node operations via a new RESTful API.
* Follow a step-by-step guide to create a Corda 5 CorDapp.
* Try the new CorDapp packaging plugin to convert your code to the Corda 5 `.cpk` file—the new extension for Corda 5 CorDapps.
* Experiment with the discovery and identity API for network memberships.

## New concepts in Corda 5 Dev Preview

If you have worked with Corda before, you will see major advances when you start developing in the Corda 5 Developer Preview. Previous versions of Corda focused on building an ecosystem of networks. Corda 5 is  application-focused: your end users can access CorDapps through multiple application networks, making it easier to build and distribute CorDapps.

To simplify the CorDapp development process, Corda 5 breaks the operational and developmental power of Corda into layers. You choose the technologies that matter to you.

### CorDapp Development changes

The Corda 5 flow interface and CorDapp packaging makes building CorDapps simpler and more concise. The Flow interface allows you to create flows and inject your preferred methods (now called Corda Services) into the flow.

The `FlowLogic` abstract class has been broken up into a set of smaller interfaces.  In place of `FlowLogic`, you can now implement the `Flow` interface which holds the `call` method.

Methods that previously existed on `FLowlogic` have been broken out into injectable **Corda services**.

The move away from an abstract class to injectable services allows you to use only the services you need. Features that you don't use will not need to be present on your flow classes.

Packaging your code has been made easier with a new CorDapp packaging plugin. Individual CorDapps can be bundled together to create your enterprise solution using a simple Command Line Interface (CLI).

### Network and node changes

You can easily bootstrap a local Corda 5 network using the new CLI. This deployment creates a developer network in which you can test your own Corda 5 CorDapps or try the new node HTTP commands to initiate flows on a demo CorDapp.

New identity and discovery features make onboarding members to a network smoother, without loss of security controls.

Read bout Corda 5 networks [Link to network documentation - including Nodes]


## Architecture in Corda 5 Dev Preview

The architecture of Corda 5 is centred around you applications, with network membership enabled by virtual nodes.

[Illustration required here]

* Run Corda CLI
* Set up a dev network (local)
* Run a sample CorDapp
* Develop
  * CorDapps
  * Nodes
* Operate
* Deploy
* Maintain
