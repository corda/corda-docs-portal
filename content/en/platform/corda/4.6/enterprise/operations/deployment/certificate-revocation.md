---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-operations-guide-deployment-cenm-certificate-revocation
    parent: corda-enterprise-4-6-operations-guide-deployment-cenm
    weight: 60
tags:
- certificate
- revocation
title: Certificate revocation FAQ
---

# Certificate Revocation FAQ

## What is the expected behaviour if a certificate is revoked?

Once a certificate is revoked (including the signing of a new CRL), nodes on the network should identify the change quickly. In CENM 1.4, this takes around 30 seconds. In future releases this time frame is likely to increase because having every node in a network poll for changes is a poor scaling experience.
At this point Nodes will refuse to accept signatures from the revoked certificate. As a result, any transactions that have not yet been notarised, as well as any future transactions the revoked certificate would have signed, will be invalidated.
In addition, the Network Map Service(s) will refresh their internal cache of the CRL and will refuse to serve node info for the affected nodes. As a result, any new nodes joining the network will be completely unaware of the affected node.

## What is the expected behaviour if a node tries to transact to a revoked certificate (irrespective of their configuration)?

Nodes do not check certificates on transactions, only on communication. The purpose of this is to avoid scenarios where a node operator revokes their certificate to stop an attacker modifying the node operator’s states (for example, if the key was compromised), but as result it cannot modify their own states.

## What is the expected behaviour if the CRL is not reachable due to a network error?

This depends on whether the nodes are configured for hard or soft failure. However, in the recommended production setup (hard failure) any and all certificate validation will fail until the endpoint is reachable. This is addressed in the updated CENM 1.4 documentation on highly available CRL endpoints using an HTTP proxy.

## What is the expected behaviour if the CRL expires on existing nodes and new prospect nodes?

CRL expiration is treated identically as a failure to reach the CRL endpoint, and as such all validations will fail until a new CRL is signed and available from the Identity Manager Service.

## What are the CA certificates and who manages their CRL?

Node CA certificates are responsible for signing the separate legal identity and TLS certificates for a node. There can be confidential identity certificates under the legal identity certificate, although this approach to confidential identities is deprecated.
In theory, node CAs could have a CRL. In practice, there is no provision for this and it is impractical to do so. The Identity Manager Service (formerly Doorman) CRL is the CRL that covers the node CA certificates.

## What is an Identity Manager Service (formerly Doorman) CRL and what purpose does it serve?

Each CRL affects certificates immediately below it, although revoking any certificate implicitly revokes any certificates signed by the revoked certificates, and so on down the hierarchy. The Identity Manager CRL therefore contains a list of revoked node CA certificates.

## What are the typical cases when a certificate revocation is required? What are the implications for the node?

Certificate revocation is typically required if a certificate was incorrectly issued (for example, if someone managed to impersonate another legal entity), if the key associated with the certificate was compromised, or if the key associated with the certificate was lost. No process is currently available for re-issuing certificates, so certificate revocation is irreversible for the legal identity affected. Therefore certificate revocation must *not* be used for disabling a node temporarily.

## What is the recommended configuration for the CRL?

You should use a High Availability deployment in order to avoid any impact caused by temporary downtimes.
See [Identity Manager Service](../../../../cenm/1.4/identity-manager.md) for an example configuration of such a deployment.

See [Certificate Revocation List](../../../../cenm/1.4/certificate-revocation.md) for instructions on revoking certificates, and [Signing Services](../../../../cenm/1.4/signing-service.md) for
configuration of the Signing Service for CRLs (especially the `updatePeriod` option).
