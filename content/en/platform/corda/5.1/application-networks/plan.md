---
description: "Plan your application network (business network) by considering cluster deployment and topology, onboarding processes, security policy, and data sovereignty."
date: '2023-04-07'
version: 'Corda 5.1'
title: "Planning Application Networks"
menu:
  corda51:
    identifier: corda51-networks-plan
    parent: corda51-networks
    weight: 1000
section_menu: corda51
---
# Planning Application Networks

Planning an {{< tooltip >}}application network{{< /tooltip >}} (business network) requires some thought and consideration with regard to {{< tooltip >}}cluster{{< /tooltip >}} deployment and topology, onboarding processes, security policy, and data sovereignty.

## Network Onboarding

Corda is a permissioned network, where the Network Operator makes decisions as to who can and cannot join the network. Typically, there are commercial and contractual agreements defined as part of the onboarding process.

The onboarding process may fall under regulations, such as Know Your Customer (KYC) in order to address anti-money laundering. Network Operators must decide the level of due diligence that must be performed before participants can be onboarded to their network. Network Operators will also decide whether to use automated approval or manual approval processes to accept and decline registration requests.

## Security Policy

Network participants are identified by an {{< tooltip >}}X.509{{< /tooltip >}} certificate issued to that {{< tooltip >}}entity{{< /tooltip >}}. The certificate issuing authority (Certificate Authority) is part of a ({{< tooltip >}}PKI{{< /tooltip >}}) that is trusted by the Network Operator. The PKI could be a public infrastructure whose public keys are published and typically stored in web browsers, so that they do not need to be manually downloaded and trusted.

Alternatively, the PKI used to issue certificates to network participants could be a private PKI, typically owned and managed by the Network Operator. These private Certificate Authorities must be trusted by the network participants.

## Data Sovereignty

Network participants will each have a virtual node in the Corda infrastructure. The virtual node's data, specifically its view of the {{< tooltip >}}distributed ledger{{< /tooltip >}}, will be stored in its database {{< tooltip >}}vault{{< /tooltip >}}.

If there is a need to distribute network participant virtual nodes across geographic regions, this leads to a multi-cluster deployment topology and a more decentralized network model.

## Network Decentralization

A key planning consideration for deploying Corda application networks is the level of decentralization of the network and participants. Questions to consider are:

* Who is responsible for the governing policy for application distribution?
* Who decides participation in the network?
* Who is performing data processing?

The Corda cluster can be deployed either in a single cluster or multi-cluster topology, depending on the level of centralization:
description:

* In a centralized model (typically a single Corda cluster approach) the application network is managed centrally, along with managing any participating members, all under a single infrastructure.
* In a decentralized model (typically a multi-cluster approach) the network participants run their own Corda infrastructure and deploy their own virtual nodes. Network Operators will need to consider the security of inter-cluster communications and latency.

Additionally, there is the consideration of the {{< tooltip >}}notary{{< /tooltip >}} virtual node and the Corda infrastructure that it is to be deployed to, whether centralized or de-centralized.
