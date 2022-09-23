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

## Restful Interfaces

## Corda CLI

## Packaging
CorDapps are no longer created as fat JAR files but are now built using the Corda [packaging](key-concepts/packaging.html) format to enhance distributability and reuse.

## Interface Based APIs

## Containerized

## Pluggable Ledger Model
