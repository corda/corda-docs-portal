---
date: '2023-02-23'
title: "Notaries"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-notaries
    parent: corda5-develop
    weight: 4500
section_menu: corda5
---
# Notaries

This section outlines how to get a notary up and running on a Corda application network.

{{< note >}} 
Notary virtual nodes use an additional “uniqueness” database for capturing state data for double-spend prevention. This is similar to the existing “crypto” and “vault” databases. Currently, when auto-provisioning virtual node databases, a uniqueness database is always provisioned, regardless of whether it is a notary virtual node or not. This will be addressed in a future release.
{{< /note >}} 

# Network Member Roles

With the introduction of the UTXO ledger and notaries, network operators must be aware of the different roles that exist on a network. Network participants can take one of three roles:

* **Application:** Members which run a CPI (Corda Package Installer) containing a CPB (Corda Package Bundle) which provides a CorDapp to run on the network. Most members fulfil this role, and would be our archetypical “Alice” or “Bob” nodes.
* **Notary:** Members which run a CPI containing a CPB which provide a notarization service to the network. These are effectively representatives of a notary service, similar to how notary workers represented a notary service in a Corda 4 high-availability notary setup.
* **MGM:** The Membership Group Manager. In the context of notary functionality, there is nothing special or different about the MGM. The MGM virtual node is deployed as part of your standard network setup.
