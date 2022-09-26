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
Corda 4 required that all Corda networks use the custom PKI (x509 extensions) dictated by Corda.
Membership of a Corda Network was granted through Corda operating as a certificate authority with the signing of a CSR tying a legal identity to a public key granting membership of a network.
This was achieved through the use of the Identity Manager and Network Map services run as part of the CENM product.

Corda 5 radically alters the way identities are onboarded to a network.
Identities can present an identity certificate to the new [Membership Group Manager (MGM)](key-concepts.html#membership-management) when requesting registration. The choice to do so is optional, a policy set by the network operator, as is the choice of the root certificate to trust and thus which CAs will be considered as suitable.
As a result, registration of an identity is done directly with the MGM, without the prior step of obtaining a Corda Identity Certificate. Membership permission and onboarding is still conducted by the network operator during this phase, and as ever, it is up to that operator to set the rules they wish to apply to the attestation that a registrant is who they claim to be.

## MGM
As mentioned above, the [Membership Group Manager (MGM)]((key-concepts.html#membership-management)) replaces the CENM suite ** entry to a network. Unlike CENM, the MGM operates as a part of the Corda infrastructure natively and does not require additional servers and services to operate.

## Application Networks
Prior to Corda 5, Corda had a two-layered model surrounding network membership that separated the permisioning of an identity onto the network from joining a business network. Initially, an identity would join a Corda Network known to be hoisting various applications. The network operator attesting their identity is valid. Then they could elect to join a business network. Now, it was of course possible for a business network to be the network operator, meaning a network would only be hosting a single application. However, in that case the chances of interoperation with other applications would be zero as interop was predicated on being in the same network.

Corda 5 changes this by allowing inter-network interoperation and focuses on one network per application. This allows identity rules to be set by each network as suitable.

## Restful Interfaces
Corda 4 used AMQP as its communication mechanism, this means all RPC commands required an intermediate client to interoperate with CorDapps, complicating development and deployment. Corda 5 switches RPC over to industry standard REST calls, removing the need for that client and allowing applications to directly interact with Corda.

## Corda CLI
The Corda Command Line Interface replaces the Corda Shell from older versions of Corda. It understands the new RESTful RPC mechanics as well as the much improved RBAC system Corda 5 employs, allowing for managed sessions to be executed by different users with differing permission levels.

Through a plugin mechanism the CLI is extensible such that all aspects of Corda can be managed from it, including both the developer and operator lifecycles as well as CorDapp operators.

## Packaging
CorDapps are no longer created as fat JAR files but are now built using the Corda [packaging](key-concepts.html#packaging) format to enhance distributability and reuse.

## Interface Based APIs
Corda’s APIs for CorDapp developers have switched into their own repository and become pure Interfaces. This means details of the Corda implementations of the system level functions will no longer pollute user space and allow Corda to upgrade its implementations without requiring CorDapps to upgrade themselves

## Containerized and Clustered
Corda 4 and below is delivered as a single JAR that is either executed as a normal process or run from within a single container. Corda 5 breaks that monolith apart delivering functionality through a series of services hosted by Kubernetes or some other cloud-style orchestration tool

## Kafka
Corda 5 replaces the message bus at the heart of the system moving away from Artemis to defaulting to Apache Kafka. The shift allows Corda to be deployed in a HH/AA configuration, moving away from the Hot/Warm strategy of Corda 4.

Additionally, rather than embedding the message bus as part of the actual Corda protocol, the message bus in Corda 5 merely acts as a guaranteed, fault-tolerant, message delivery system within a single cluster

## Gateway replaces the Corda Firewall
Corda 4 used the Corda Firewall to allow the egress of Corda messages to the wider internet in a secure manner. This took the form of the Float / Bridge application pair, configured separately and deployed into the DMZ to bridge Corda and the wider internet whilst sitting behind load balancers and proxies. Much like CENM these represented additional, different, software stacks to learn, configure, and operate.

Corda 5 uses the Gateway (and session manager) to achieve similar goals. However, now Corda communicates with other clusters via HTTPS instead of AMQP these services can be deployed into an ingress zone behind the corporate firewall and load balancing proxies.

## All-in-One Worker
The worker architure allows us to deliver Corda in various guises. For highly available, fault tolerant, systems, the fully distributed collection of workers can be used. However, when developing ones CorDapps, the ability to run a small, lightweight version of this is paramount. Thus, the all in one worker collpases the collection of workers into a single “all in one” worker, delivering the same characteristics of the mode complex deployment in a much smaller package.

This can be augmented through the addition of an in-memory message bus, fdoresaking Kafka, that allows deterministic testing and better observability when running through the full SDLC on ones mlaptop

## Pluggable Ledger Model
Corda version of yore tightly embedded the UTXO ledger model at the heart of the architecture. Corda 5, with its layers approach, makes this pluggable. This means various ledger models, from UTXO, through Xonasentual, to some form of rules based implementation are all possible to deploy ontop of the same tech stack and run in parallel. The ability is there to now select the right tool for the job rather than requiring the full lset of #UTXO and smart contract features that can over complicated applications that don’t mesh with that paradigm well,
