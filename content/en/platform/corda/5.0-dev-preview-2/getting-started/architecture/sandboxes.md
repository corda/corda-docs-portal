---
date: '2020-07-15T12:00:00Z'
title: "Sandboxes"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-sandboxes
    parent: corda-5-dev-preview-architecture
    weight: 4000
section_menu: corda-5-dev-preview
---

*In Corda 4, we assume that you’re running your own node, which is akin to you playing with your own sand in your own garden. And we also assume that you’re a responsible adult: we trust you to take care and we assume you’re not going to deliberately ruin your grass. So Corda didn’t have a sandbox. In Corda 5 we can’t make these assumptions. In Corda 5, it’s more like the garden is shared amongst multiple houses or apartments. We can’t assume everybody will be careful and some of them may be positively malicious.*

sandboxing (support for multi-tenancy & HA)

In software engineering we define a sandbox as something—an environment or context—which is isolated in some way from another.

 an essential part of the Corda 5 architecture, used to support Corda’s stability and security when operating in a highly-available (HA) and multi-tenant configuration.

 Isolating CorDapp classes and dependencies in this way also means that they are isolated from the Corda host process. This means that CorDapps no longer share libraries with Corda itself, and therefore can use their own version of 3rd party dependencies, for example.

 HA requirements mean we need to be able to install and upgrade CorDapps without impacting other CorDapps operating in the same Corda process, and to provide a way to allow CorDapps to upgrade without the need to stop existing flows or the host process.

This requirement of being able to ‘hot load’ CorDapps, means we can potentially load multiple versions of a given CorDapp or library. Therefore, sandboxing and isolation are required in order to support HA.

Sandboxes are security mechanisms for separating running programs. They are the foundation that [virtual nodes](#virtual-nodes) run on, keeping contracts, workflows, and libraries separate from other code. The contents of these sandboxes are packaged up and shared for deployment by creating a [CPI file](#package-installer-CPI).

Each [virtual node](#virual-nodes) runs on top of one or more sandboxes. Unlike isolation, which hides code from users that should not be able to see it, sandboxing prevents code from touching other parts of a system, where it could precipitate a failure or spread vulnerabilities.

Typically, a virtual node has sandboxes for its:

* Contract code. When you verify a contract on Corda, it checks that all versions of that contract comply with the code that existed in that sandbox when the contract was signed.
* Workflow.
* Third party libraries, if present.
