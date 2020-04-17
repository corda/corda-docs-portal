---
aliases:
- /releases/4.1/design/certificate-hierarchies/design.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- design
title: Certificate hierarchies
---


# Certificate hierarchies


{{< important >}}
This design doc applies to the main Corda network. Other networks may use different certificate hierarchies.


{{< /important >}}


## Overview

A certificate hierarchy is proposed to enable effective key management in the context of managing Corda networks.
This includes certificate usage for the data signing process and certificate revocation process
in case of a key compromise. At the same time, result should remain compliant with
[OCSP](https://en.wikipedia.org/wiki/Online_Certificate_Status_Protocol) and [RFC 5280](https://www.ietf.org/rfc/rfc5280.txt)


## Background

Corda utilises public key cryptography for signing and authentication purposes, and securing communication
via TLS. As a result, every entity participating in a Corda network owns one or more cryptographic key pairs {*private,
public*}. Integrity and authenticity of an entity’s public key is assured using digital certificates following the
[X.509 standard](https://tools.ietf.org/html/rfc5280), whereby the receiver’s identity is cryptographically bonded to
his or her public key.

Certificate Revocation List (CRL) functionality interacts with the hierarchy of the certificates, as the revocation list
for any given certificate must be signed by the certificate’s issuer. Therefore if we have a single doorman CA, the sole
CRL for node CA certificates would be maintained by that doorman CA, creating a bottleneck. Further, if that doorman CA
is compromised and its certificate revoked by the root certificate, the entire network is invalidated as a consequence.

The current solution of a single intermediate CA is therefore too simplistic.

Further, the split and location of intermediate CAs has impact on where long term infrastructure is hosted, as the CRLs
for certificates issued by these CAs must be hosted at the same URI for the lifecycle of the issued certificates.


## Scope

Goals:


* Define effective certificate relationships between participants and Corda network services  (i.e. nodes, notaries, network map, doorman).
* Enable compliance with both [OCSP](https://en.wikipedia.org/wiki/Online_Certificate_Status_Protocol) and [RFC 5280](https://www.ietf.org/rfc/rfc5280.txt) (CRL)-based revocation mechanisms
* Mitigate relevant security risks (keys being compromised, data privacy loss etc.)

Non-goals:


* Define an end-state mechanism for certificate revocation.


## Requirements

In case of a private key being compromised, or a certificate incorrectly issued, it must be possible for the issuer to
revoke the appropriate certificate(s).

The solution needs to scale, keeping in mind that the list of revoked certificates from any given certificate authority
is likely to grow indefinitely. However for an initial deployment a temporary certificate authority may be used, and
given that it will not require to issue certificates in the long term, scaling issues are less of a concern in this
context.


## Design Decisions



* [Design Decision: Certificate hierarchy levels](decisions/levels.md)
    * [Background / Context](decisions/levels.md#background-context)
    * [Options Analysis](decisions/levels.md#options-analysis)
    * [Recommendation and justification](decisions/levels.md#recommendation-and-justification)


* [Design Decision: Certificate Hierarchy](decisions/tls-trust-root.md)
    * [Background / Context](decisions/tls-trust-root.md#background-context)
    * [Options Analysis](decisions/tls-trust-root.md#options-analysis)
    * [Recommendation and justification](decisions/tls-trust-root.md#recommendation-and-justification)






## **Target** Solution

[![cert structure v3](design/certificate-hierarchies/./images/cert_structure_v3.png "cert structure v3")](images/cert_structure_v3.png)
The design introduces discrete intermediate CAs below the network trust root for each logical service exposed by the doorman - specifically:


* Node CA certificate issuance
* Network map signing
* Certificate Revocation List (CRL) signing
* OCSP revocation signing

The use of discrete certificates in this way facilitates subsequent changes to the model, including retiring and replacing certificates as needed.

Each of the above certificates will specify a CRL allowing the certificate to be revoked. The root CA operator
(primarily R3) will be required to maintain this CRL for the lifetime of the process.

TLS certificates will remain issued under Node CA certificates (see [decision: TLS trust
root](decisions/tls-trust-root.md)).

Nodes will be able to specify CRL(s) for TLS certificates they issue; in general, they will be required to such CRLs for
the lifecycle of the TLS certificates.

In the initial state, a single doorman intermediate CA will be used for issuing all node certificates. Further
intermediate CAs for issuance of node CA certificates may subsequently  be added to the network, where appropriate,
potentially split by geographic region or otherwise.

