---
date: '2020-07-15T12:00:00Z'
title: "Membership group manager"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-mgm
    weight: 6000
section_menu: corda-5-dev-preview
---

the successor to CENM from Corda 4.

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
