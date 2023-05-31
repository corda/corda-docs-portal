---
title: "Personas"
date: 2023-04-21
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-personas
    parent: corda5-intro
    weight: 4050
section_menu: corda5
---
# Personas

The Corda documentation is written from the perspectives of a collection of people; each with their own problems to solve. Relevant sections of the documentation should resonate with you, depending on the persona whose goals you share. The documentation currently addresses the following personas:
* [Architect]({{< relref "#architect">}})
* [CorDapp Developer]({{< relref "#cordapp-developer">}})
* [Corda Administrator]({{< relref "#corda-administrator">}})
* [Network Operator]({{< relref "#network-operator">}})

## Architect

As an Architect considering or planning a project with Corda, you:
* are curious about the benefits of adopting DLT technology, but also concerned about any risks.
* want to know why DLT is a better fit for your business problem than a centralized solution.
* are for looking for answers and guidance to the following questions:
   * Who has access to my vault data and how is privacy preserved in Corda?
   * How do I manage the compromising of cryptographic key material?
   * How do I maintain compliance with GDPR (and other data protection regulations) if personal data is stored in Corda?
   * How do I scale Corda?
   * How do I maintain business continuity for Corda?
   * How do I deploy Corda into my enterprise infrastructure and integrate it with my enterprise applications?

As an Architect working with Corda, all sections of the Corda documentation are of interest to you, but particularly the [Key Concepts]({{< relref "../key-concepts/_index.md">}}).

## CorDapp Developer

A CorDapp Developer uses Corda to:
* explore DLT and create their own chain of shared facts to experiment with.
* design an enterprise production-grade distributed application.
* work as part of a team to build an enterprise production-grade distributed application.
* understand the software development lifecycle (SDLC) of a distributed application.
* implement a method in the API to make something simpler.
* discover best practice design tips for distributed applications.

To get started developing CorDapps, see the [Developing Applications]({{< relref "../developing-applications/_index.md">}}) section.

## Corda Administrator

A Corda administrator is responsible for:
* making informed decisions to deliver the prerequisites for Corda.
* installing and operating the Corda software.
* integrating Corda into Continuous Integration and Delivery CI/CD pipelines.
* understanding how Corda manages errors to deliver continuous execution.
* the disaster recovery story for Corda.
* monitoring the health metrics of Corda.

To learn more, see the [Operating Corda Clusters]({{< relref "../deploying-operating/_index.md">}}) section.

## Network Operator

The network operator is concerned with: 
* how Corda delivers on the _permissioned_ aspect of a private permissioned DLT platform.
* service levels for participants on the business network.
* defining permissions for actions on the business network.
* “know your customer” (KYC) regulations.

The network operator:
* onboards participants of a business network.
* manages the lifecycle of participants on the network.
* defines and applies network membership rules for participation in the business network.
* distributes CorDapps to network participants.

To learn more, see the [Managing Application Networks]({{< relref "../application-networks/_index.md">}}) section.