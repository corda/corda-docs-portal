---
date: '2022-09-10'
title: "Changes from Corda 4"
menu:
  corda-5-dev-preview2:
    parent: corda-5-dev-preview-intro
    identifier: corda-5-dev-preview-c4-differences
    weight: 3000
section_menu: corda-5-dev-preview2
---

## Relaxed PKI
 
Corda 4 required that all Corda networks used the custom PKI (X.509 extensions). Membership of a Corda network was granted by Corda operating as a certificate authority. The signing of a CSR tied a legal identity to a public key, thereby granting membership of a network. This was achieved using Identity Manager and Network Map services, which are run as part of the Corda Enterprise Network Manager (CENM) product.

Corda 5 radically alters the way that identities are onboarded to a network.
Identities can present an identity certificate to the new [Membership Group Manager (MGM)](key-concepts.html#membership-management) when requesting registration. The choice to do so is optional, which is a policy set by the network operator. This is because it is the choice of the root certificate to trust and therefore decide which Certificate Authorities (CAs) will be considered as suitable.

As a result, registration of an identity is done directly with the MGM, without the prior step of obtaining a Corda identity certificate. Membership permission and onboarding is still conducted by the network operator during this phase. As usual, it is up to that operator to set the rules that they wish to apply for the attestation that a registrant is who they claim to be.

## MGM
As mentioned above, the [Membership Group Manager (MGM)](key-concepts.html#membership-management) replaces the CENM suite as the method for permissioning entry to a network. Unlike CENM, MGM operates as a part of the Corda 5 infrastructure natively and does not require additional servers and services to operate.

## Application networks
Prior to Corda 5, Corda had a two-layer model for network membership that separated the permissioning of an identity onto a network from joining a business network. Initially, an identity would join a Corda network known to be hosting various applications. The network operator would attest their identity is valid. Then the identity could elect to join a business network. It was possible for a business network to also be the network operator, meaning that a network would only be hosting a single application. However, in that case the chances of interoperability with other applications would be zero, since interoperability was predicated on the basis of being in the same network.

Corda 5 changes this by allowing inter-network interoperability and focusing on one network per application. This allows identity rules to be set by each network as suitable.

## Restful interfaces
Corda 4 used Advanced Message Queuing Protocol (AMQP) as its communication mechanism. This meant that all RPC commands required an intermediate client to interoperate with CorDapps, complicating development and deployment. Corda 5 switches RPC over to industry standard REST calls, removing the need for that client and allowing applications to directly interact with Corda.

## Corda CLI
The Corda Command Line Interface (CLI) replaces the Corda Shell from older versions of Corda. It understands the new RESTful RPC mechanics, as well as the much improved RBAC system which Corda 5 employs. This allows for managed sessions to be executed by different users with differing permission levels.

Through a plugin mechanism, the CLI is extensible so that all aspects of Corda can be managed from it, including both the developer and operator lifecycles, as well as CorDapp operators.

## Packaging
CorDapps are no longer created as fat JAR files, but are now built using the Corda [packaging](key-concepts.html#packaging) format to enhance distributability and reuse.

## Interface based APIs
The Corda APIs for CorDapp developers have switched to their own repository and become pure interfaces. This means that details of the Corda implementations of the system-level functions will no longer pollute user space. It also allows Corda to upgrade its implementations without requiring CorDapps to upgrade themselves.

## Containerized and clustered
Corda 4 and below is delivered as a single JAR that is either executed as a normal process or run from within a single container. Corda 5 breaks that monolith apart, delivering functionality through a series of services hosted by Kubernetes or other cloud-style orchestration tools.

## Apache Kafka
Corda 5 replaces the message bus at the heart of the system, moving away from Artemis and defaulting to Apache Kafka. This shift allows Corda to be deployed in a Hot-Hot/Active-Active configuration, moving away from the Hot/Warm strategy of Corda 4.

Additionally, rather than embedding the message bus as part of the actual Corda protocol, the message bus in Corda 5 merely acts as a guaranteed, fault-tolerant, message delivery system within a single cluster.

## Gateway replaces the Corda Firewall
Corda 4 used the Corda Firewall to allow the egress of Corda messages to the wider internet in a secure manner. This took the form of the Float/Bridge application pair. This was configured separately and deployed into the DMZ to bridge Corda and the wider internet, whilst sitting behind load-balancers and proxies. Much like CENM, these represented additional and different software stacks to learn, configure, and operate.

Corda 5 uses the Gateway (and session manager) to achieve similar goals. However, now that Corda communicates with other clusters via HTTPS instead of AMQP, these services can be deployed into an ingress zone behind the corporate firewall and load-balancing proxies.

## Combined worker
The worker architecture allows us to deliver Corda in various guises. For highly available fault-tolerant systems, the fully distributed collection of workers can be used. However, when developing CorDapps, the ability to run a small and lightweight version of this is paramount. Therefore, a collection of workers can be collapsed into a *combined worker*, delivering the same characteristics of the mode-complex deployment in a much smaller package.

This can be augmented through the addition of an in-memory message bus, foresaking Kafka. This allows deterministic testing and better observability when running through the full software development lifecycle on a laptop.

## Pluggable Ledger Model
Past Corda versions tightly embedded the UTXO ledger model at the heart of the architecture. Corda 5, with its layered approach, makes this model pluggable. This means that various ledger models, from UTXO through consensual, to some form of rules-based implementation, are all possible to deploy on top of the same tech stack and run in parallel. The right tool for the job can be selected, rather than requiring the full set of UTXO and smart contract features, which can overcomplicate applications that do not mesh well with that paradigm.