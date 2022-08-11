---
date: '2020-07-15T12:00:00Z'
title: "Introduction to Corda"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-intro
    weight: 1050
section_menu: corda-5-dev-preview
---

what is Corda 5?? This needs to be clear - will be asked over and over!!
solve the same problems as Corda 4 BUT new infrastructure
- modular
- horizontal-scaling
- virtual nodes
- Containers automation
- show people it's not too hard to use!
security details and requirements for "project planners" - cross-ref prerequities
cross-ref key concepts

What is Corda 5???
multi-tenancy - host multiple virtual nodes on one deployment of Corda - enabled by sandboxing
cross-ref to architecture section
* a more application centric model. - optimising the platform around a user journey that starts from the developer and puts applications at the center, rather than starting layering abstractions starting from the node and working our way up to a business network.
* Applications networks are now simplified Corda networks. They are still permissioned and the run time responsibilities of membership management moves from a dedicated series of services (Corda Enterprise Network Manager) to a simple, extensible application running on a node — removing the need to run dedicated infrastructure to manage a network of peers. Previous versions of Corda focused on building an ecosystem of networks. Corda 5 is application-focused, making it easier to build, test, and distribute CorDapps.
* We have rewritten our APIs to be interface-based and modular.

An intro to the basics needed to get started with Corda 5.
* Prerequisites
* Installing Corda

A Corda Network is a peer-to-peer network of Nodes, each representing a party on the network. These Nodes run Corda applications (CorDapps) , and transact between Nodes using public or confidential identities.
Corda 5 features a fully redundant, worker-based architecture to be applied to all critical services that are required to run a node. We use a Kafka cluster as the message broker to facilitate communication between node services.


A Modular API. Corda’s core API module has been split into packages and versioned.
Dependency upgrades to Gradle 6, Java 11, and Kotlin 1.4. This enables the latest Gradle CorDapp packaging plugins, letting you create CorDapps faster.
Node interaction upgrades. You can interface with a node using HTTP and auto-generate CorDapp endpoints.
Upgrades to packaging:
CorDapps are no longer packaged as .jar files.
A Corda Package, .cpk is now the unit of software that executes within a single sandbox.
CorDapps are a set of versioned .cpks that define a deployable application.
A new integration test framework that reflects real node behavior.
An API for pluggable uniqueness service (notary). This is interface-only.
 one of our key objectives of the re-architecture — making Corda 5 highly available and scalable to power distributed critical systems.

The runtime of a node will no longer be confined to a single JVM, instead the deployment topology will look more like a cluster of workers listening to a message bus (Kafka) for events to process (in its HA configuration). A worker is an instance of a Java Virtual Machine containing a group of processing modules/services — you can think of it as a container you deploy.

The key take away is that we are changing a lot of the properties (non-functionals) of the platform but none of its DNA:

We aim with our Modular APIs, new tools, and packaging to make developing in Corda faster and more enjoyable.
The new artefact — Installer — combined with simpler Application network — should make your go to market, onboarding and version management experience much simpler.
The new architecture should give you the flexibility to evolve your operating model as you grow, with the ability to move the operations of virtual nodes across worker clusters.
The app-based network management and virtual nodes should make Corda less expensive to run for everybody involved.
Finally, Corda’s new event driven architecture should give us enough h?eadroom to go after the most sophisticated enterprise multi-party use cases and power the next central bank digital currency, global payment network or critical market infrastructure.



................

Corda is a Distributed ledger technology (DLT) platform
Corda 5 Developer Preview (DP) 2 is a developer preview of the next major iteration of Corda, Corda 5. While this version enables you to solve the same problems as Corda 4, the new Corda 5 architecture and deployment methods are designed to deliver high availability and scalability.
*
