---
date: '2023-01-05'
title: "Network Member Roles"
menu:
  corda-5-beta:
    parent: corda-5-beta-notaries
    identifier: corda-5-beta-network-member-roles
    weight: 5000
section_menu: corda-5-beta

---

# Network Member Roles

With the introduction of the UTXO ledger and notaries, network operators must be aware of the different roles that exist on a network. As of Beta 1, network participants can take one of three roles:

* **Application:** Members which run a CPI (Corda Package Installer) containing a CPB (Corda Package Bundle) which provides a CorDapp to run on the network. Most members fulfil this role, and would be our archtypical “Alice”, “Bob” nodes etc.

* **Notary:** Members which run a CPI containing a CPB which provide a notarization service to the network. These are effectively representatives of a notary service, similar to how “notary workers” represented a notary service in a Corda 4 high availability notary setup.

* **MGM:** The Membership Group Manager. In the context of notaries, this special role can be ignored as the deployment of a MGM virtual node is handled transparently by our deployments.