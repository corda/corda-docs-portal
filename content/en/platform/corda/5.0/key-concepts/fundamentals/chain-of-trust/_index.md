---
title: "Chain of Trust"
date: 2023-06-07
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-fundamentals-chain-trust
    parent: corda5-fundamentals
    weight: 6000
section_menu: corda5
---

# Chain of Trust

Corda's chain of trust is configured when a Network Operator installs a new CPI. At this point, the code-signing certificates of the CPI, CPB, and CPK publishers are validated and their Certificate Authority (CA) trust roots are checked. 
These code-signing trust roots may be self-signed publisher certificates, or they may be well-known public CAs. 
Either way, the trust roots establish the standard of proof that the CorDapp code (and any future upgrades) has come from the expected publisher. 
The Network Operator must establish that they trust the code-signing trust roots and upload them to the cluster to proceed with CPI installation. 
In choosing to install and trust the CPI, the Network Operator is crucially accepting the network details presented by the CPI and, in particular, the network credentials of the MGM, which subsequently act as authentication and a distribution root for the entire network.

The MGM trust root information is defined statically in the `GroupPolicy.json` file of the CPI. 
Corda updates this when virtual nodes are upgraded to a more recent CPI from the publisher. 
This allows for gradual rotation and replacement of the trust roots. 
More dynamically, the MGM publishes a `GroupParameters` data structure, which is signed with its key and contains global network facts and configurations.
For example, the declaration of allowed notaries, or application-specific information such as issuer keys/member names.

Virtual nodes must abide by the policy rules of the MGM. 
For example, the MGM defines suitable [TLS trust roots]({{< relref "../../../application-networks/creating/mgm/key-pairs.md#configure-the-cluster-tls-key-pair" >}}) and the [type of TLS used]({{< relref "../../../application-networks/creating/optional/mutual-tls-connections.md">}}). 
The Network Operator must lobby the MGM to accept their membership details before they can join the network or make a change to their details. 
The session initiation keys, ledger keys, and other data included in the membership application become the published identity facts of the virtual node available to peers, presented with signatures from both MGM and virtual node private keys. 
Under its signature, the MGM also includes data that only it controls, such as membership active/suspended flags. This shared authenticated data is exposed to flows as the `MemberInfo` data structure. 
`MemberInfo` is often used to locate peer keys to validate against, to advertise specific peer roles, or to control flow behaviour.