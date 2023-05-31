---
date: '2023-05-16'
title: "Network Member Roles"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: network-member-roles
    parent: corda5-develop-notaries
    weight: 4600
section_menu: corda5
---
# Network Member Roles

With the introduction of the UTXO ledger and notaries, network operators must be aware of the different roles that exist on a network. Network participants can take one of three roles:

* **Application:** Members which run a CPI (Corda Package Installer) containing a CPB (Corda Package Bundle) which provides a CorDapp to run on the network. Most members fulfil this role, and would be our archetypical “Alice” or “Bob” nodes.
* **Notary:** Members which run a CPI containing a CPB which provide a notarization service to the network. These are effectively representatives of a notary service, similar to how notary workers represented a notary service in a Corda 4 high-availability notary setup.

* **MGM:** The Membership Group Manager. In the context of notary functionality, there is nothing special or different about the MGM. The MGM virtual node is deployed as part of your standard network setup.
