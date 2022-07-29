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

*sandboxing (support for multi-tenancy), see Dries' blog*

Sandboxes are security mechanisms for separating running programs. They are the foundation that [virtual nodes](#virtual-nodes) run on, keeping contracts, workflows, and libraries separate from other code. The contents of these sandboxes are packaged up and shared for deployment by creating a [CPI file](#package-installer-CPI).

Each [virtual node](#virual-nodes) runs on top of one or more sandboxes. Unlike isolation, which hides code from users that should not be able to see it, sandboxing prevents code from touching other parts of a system, where it could precipitate a failure or spread vulnerabilities.

Typically, a virtual node has sandboxes for its:

* Contract code. When you verify a contract on Corda, it checks that all versions of that contract comply with the code that existed in that sandbox when the contract was signed.
* Workflow.
* Third party libraries, if present.
