---
date: '2020-07-15T12:00:00Z'
menu:
  homepage:
    parent: homepage-getting-started
    identifier: get-started-corda-5
    name: Getting started with Corda 5 Dev Preview
title: Getting started with Corda 5 Dev Preview
weight: 300
---

# Introducing the Corda 5 Developer Preview

Corda is a trust technology platform on which you can build verified blockchain networks, create applications that represent your business on the network, and interact in a completely secure ecosystem.

In this developer preview of the forthcoming Corda 5, you can experiment with two key aspects of the future of Corda:

* A modular API structure, which allows you to build applications to use on Corda (CorDaps) and test them efficiently.
* A HTTPS API, based on RESTful principles that allows you to control your node - your presence on a Corda network - remotely.

In this preview, you can:

* Delpoy a local Corda 5 developer network for building and testing CorDapps.
* Trial a new Corda 5 sample CorDapp, using HTTPS node operations via a new RESTful API.
* Follow a step by step guide to create a Corda 5 CorDapp.
* Try the new CorDapp packaging plugin to convert your code to the Corda 5 `.cpk` file - the new extension for Corda 5 CorDapps.
* Experiment with the discovery and identity API for network memberships.

## New concepts in Corda 5

If you are experienced in working with Corda 4, you will start to see major advances from the first steps of development in the Corda 5 dev preview. Just as Corda 4 and earlier iterations were focused on building an eco-system of networks, Corda 5 is now centred around your applications - making it easier for you to build and distribute CorDapps that your end-users can easily access by connecting to multiple application networks.

To remove complexity from the CorDapp development process, Corda 5 breaks the operational and developmental power of Corda into layers, allowing you to make use of the technologies that matter to you.

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
