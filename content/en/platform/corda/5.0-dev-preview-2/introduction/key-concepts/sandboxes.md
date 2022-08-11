---
date: '2020-07-15T12:00:00Z'
title: "Sandboxes"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 7000
section_menu: corda-5-dev-preview
---

[In Corda 4, we assume that you’re running your own node, which is akin to you playing with your own sand in your own garden. And we also assume that you’re a responsible adult: we trust you to take care and we assume you’re not going to deliberately ruin your grass. So Corda didn’t have a sandbox. In Corda 5 we can’t make these assumptions. In Corda 5, it’s more like the garden is shared amongst multiple houses or apartments. We can’t assume everybody will be careful and some of them may be positively malicious.]: #

Sandboxes are security mechanisms for separating running programs. They are an essential part of the high-availability (HA) and multi-tenant architecture of Corda 5, ensuring stability and security. 

Sandboxes are the foundation that virtual nodes run on, keeping contracts, workflows, and libraries separate from other code. Each [virtual node](virtual-nodes.html) runs on top of one or more sandboxes. Typically, a virtual node has sandboxes for:
* Contract code. When you verify a contract on Corda, it checks that all versions of that contract comply with the code that existed in that sandbox when the contract was signed.
* Workflow.
* Third party libraries, if present.
 Isolating CorDapp classes and dependencies in this way also isolate them from the Corda host process. CorDapps do not share libraries with Corda itself and therefore can use their own version of 3rd party dependencies, for example.

Sandboxes support the HA architecture by providing the ability to install and upgrade CorDapps without impacting other CorDapps operating in the same Corda instance. You can upgrade CorDapps without the need to stop existing flows or the host process and potentially load multiple versions of a particular CorDapp or library.
