---
date: '2020-07-15T12:00:00Z'
title: "Identities and membership management"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 4000
section_menu: corda-5-dev-preview
---
## Corda Identity

A Corda identity represents any person or business that wants to interact with other people or businesses using Corda. Identities are identified by an X500 name.

[An identity claim with a unique X-500 name in a membership group. Each Corda identity is associated with a session key, which validates the P2P sessions. The session key may be part of a PKI certificate according to the membership group defined by the MGM.]: #

## Membership group manager

MGM is the successor to CENM from Corda 4.

Overview of the **membership group manager** (MGM)....
* Static
* Dynamic - not in CordaCon release??

Application networks will be created by the Membership Group Manager (MGM), a CorDapp which runs as a virtual node, meaning you can create/operate many application networks using the same Corda deployment. This avoids having to deploy and maintain separate software, keeping operational costs low.

The MGM:

Approves/declines joining requests
Temporarily/permanently suspends members
Distributes network parameters
Organizes and schedules Corda and CorDapp upgrades
Monitors member’s Corda version
Monitors member’s CorDapp versions


Static networks:


* Overview
* Group Policy (How-to also?)
* Static network member registration (How-to also?)
* "Local development with Kubernetes" How-to
