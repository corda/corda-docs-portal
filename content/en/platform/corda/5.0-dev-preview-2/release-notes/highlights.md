---
date: '2022-06-29'
title: "Corda 5 Developer Preview 2 highlights"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-highlights
    parent: corda-5-dev-preview-release-notes
    weight: 10
    name: "Highlights"
section_menu: corda-5-dev-preview
---

Intended for local deployment, experimental development, and testing only, this preview includes:

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
Finally, Corda’s new event driven architecture should give us enough headroom to go after the most sophisticated enterprise multi-party use cases and power the next central bank digital currency, global payment network or critical market infrastructure.

## Feature 1

High-level description of feature 1.

## Feature 2

High-level description of feature 1.
