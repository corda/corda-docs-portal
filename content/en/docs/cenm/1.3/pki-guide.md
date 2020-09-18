---
aliases:
- /pki-guide.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-pki-guide
    parent: cenm-1-3-public-key-infrastructure
    weight: 310
tags:
- pki
- guide
title: Certificate Hierarchy Guide
---


# Certificate Hierarchy Guide



## Overview

The Corda security design heavily relies on the use of Public Key Infrastructure (PKI). The platform itself operates with the assumption that a
certificate authority will manage the node on-boarding and permissioning processes. As such, there is an inherent requirement
to provide an easy approach towards certificate hierarchy generation and deployment.
The PKI Tool provides a simple way to define and create all the keys and certificates for your PKI.

In Corda, we distinguish between two types of PKI entities: Certificate Authorities (CA) and Signers (non-CA).
The difference between the two is that CA can issue certificates and non-CA cannot. The latter one is limited only to signing data.
Each of those entities maintains its own key pair (public and private keys) that is used to authenticate and sign data.
Moreover, each of them needs to be certified (i.e. hold a certificate issued) by another CA.
An entity’s certificate binds the legal name of the entity to its public key, with the signature of the certificate’s issuer providing the attestation to this binding.
As well as issuing certificates, each CA is also responsible for maintaining information about certificate’s validity.
Certificates can become invalid due to different reasons (e.g. keys being compromised or cessation of operation) and as such need to be revoked.

To be able to know whether a certificate has been revoked, each CA maintains a Certificate Revocation List (CRL).
That CRL needs to be published such that it can be accessed by anybody who may participate in the network. By
default the CRL is exposed via the Identity Manager Service, although it is recommended that this endpoint is
wrapped in a caching HTTP proxy. This proxy layer can be behind a load balancer, providing high availability for
delivery of the CRL.

With all of the above in mind, the output of the PKI Tool execution is a certificate hierarchy comprising of the key pairs (for each defined entity)
accompanied with the certificates associated with those key pairs as well as signed static certificate revocation lists.

The PKI Tool is intended to make it easy to generate all the certificates needed for a Corda deployment.
The tool generates the keys in the desired key store(s) and outputs a set of certificates necessary for correct Corda Network operation.


## Corda Requirements

Corda nodes operate with the following assumptions on the certificates hierarchy:

* There are two certificates, one corresponding to the Identity Manager Service and the other one to the Network Map Service.
* They need to have the common root certificate, which is present in the node’s truststore.
  The length of the certificate chain can be arbitrary. As such, there can be any number of certificates between the Identity Manager Service and Network Map Service certificates as long
  as they root to the same certificate.
* They need to have a custom extension defining the role of the certificate in the context of Corda. See
  [here](https://docs.corda.net/permissioning.html#certificate-role-extension) for more details.


Other than that, Corda nodes stay agnostic to the certificate hierarchy (in particular the depth of the certificate hierarchy tree).

![hierarchy agnostic](/en/images/hierarchy-agnostic.png "hierarchy agnostic")
At the time of writing this document, the Corda Network assumes the certificate hierarchy that can be found [here](https://docs.corda.net/head/permissioning.html) .


### Certificate Revocation List (CRL)

Every time two nodes communicate with each other they exchange their certificates and validate them against the Certificate Revocation List.
In Corda, the certificate chains of the nodes are validated only during the TLS handshake.
This means that every time an TLS connection is established between two nodes, the TLS certificates (together with the
remaining certificate chain ending at the root certificate) are exchanged and validated at each node.

The network operator is responsible for certificate issuance and maintenance for each certificate starting at the Root certificate and ending
at the Identity Manager and Network Map certificates. The rest of the certificate chain (i.e. every certificate below the Identity Manager certificate) falls into
node operator responsibility.

![tls hierarchy](/en/images/tls-hierarchy.png "tls hierarchy")
The certificate revocation list verification applies to the entire chain. This means that every certificate in the chain
is going to be validated against the corresponding certificate revocation list during the SSL handshake.
Consequently, this means that a node operator is expected to provide and maintain the certificate revocation list for the Node CA.
Even though Corda supports this scenario, it might be a tedious task that a node operator does not want to deal with.
As such, Corda offers also an alternative solution, which allows a node to benefit from the certificate revocation list validation and at the
same time waives away the necessity of the certificate revocation list maintenance from the node operator.

The certificate revocation list validation process allows the certificate revocation list to be signed by a third party
authority (i.e. associated key pair) as long as its certificate is self-signed and trusted (i.e. it is present in the node’s trust store).
As such, in Corda, the certificate revocation list for the TLS level is signed by a dedicated self-signed certificate called TLS Signer,
which is then added to node’s trust store (in a similar way as the Corda Root certificate - distributed with the `network-trust-store.jks`).
During the certificate revocation list validation process the trust store is consulted for the presence of the TLS Signer certificate.

#### FAQ

**What is the expected behaviour if a certificate is revoked?**

Once a certificate is revoked (including the signing of a new CRL), nodes on the network should identify the change quickly. In CENM 1.3, this takes around 30 seconds. In future releases this time frame is likely to increase because having every node in a network poll for changes is a poor scaling experience.
At this point Nodes will refuse to accept signatures from the revoked certificate. As a result, any transactions that have not yet been notarised, as well as any future transactions the revoked certificate would have signed, will be invalidated.
In addition, the Network Map Service(s) will refresh their internal cache of the CRL and will refuse to serve node info for the affected nodes. As a result, any new nodes joining the network will be completely unaware of the affected node.

**What is the expected behaviour if a node tries to transact to a revoked certificate (irrespective of their configuration)?**

Nodes do not check certificates on transactions, only on communication. The purpose of this is to avoid scenarios where a node operator revokes their certificate to stop an attacker modifying the node operator’s states (for example, if the key was compromised), but as result it cannot modify their own states.

**What is the expected behaviour if the CRL is not reachable due to a network error?**

This depends on whether the nodes are configured for hard or soft failure. However, in the recommended production setup (hard failure) any and all certificate validation will fail until the endpoint is reachable. This is addressed in the updated CENM 1.3 documentation on highly available CRL endpoints using an HTTP proxy.

**What is the expected behaviour if the CRL expires on existing nodes and new prospect nodes?**

CRL expiration is treated identically as a failure to reach the CRL endpoint, and as such all validations will fail until a new CRL is signed and available from the Identity Manager Service.

**What are the CA certificates and who manages their CRL?**

Node CA certificates are responsible for signing the separate legal identity and TLS certificates for a node. There can be confidential identity certificates under the legal identity certificate, although this approach to confidential identities is deprecated.
In theory, node CAs could have a CRL. In practice, there is no provision for this and it is impractical to do so. The Identity Manager Service (formerly Doorman) CRL is the CRL that covers the node CA certificates.

**What is an Identity Manager Service (formerly Doorman) CRL and what purpose does it serve?**

Each CRL affects certificates immediately below it, although revoking any certificate implicitly revokes any certificates signed by the revoked certificates, and so on down the hierarchy. The Identity Manager CRL therefore contains a list of revoked node CA certificates.

**What are the typical cases when a certificate revocation is required? What are the implications for the node?**

Certificate revocation is typically required if a certificate was incorrectly issued (for example, if someone managed to impersonate another legal entity), if the key associated with the certificate was compromised, or if the key associated with the certificate was lost. No process is currently available for re-issuing certificates, so certificate revocation is irreversible for the legal identity affected. Therefore certificate revocation must *not* be used for disabling a node temporarily.

**What is the recommended configuration for the CRL?*

You should use a High Availability deployment in order to avoid any impact caused by temporary downtimes.
See [Identity Manager Service](identity-manager.md) for an example configuration of such a deployment.

See [Certificate Revocation List](certificate-revocation.md) for instructions on revoking certificates, and [Signing Services](signing-service.md) for
configuration of the Signing Service for CRLs (especially the `updatePeriod` option).


## Example Scenario

As an example, let us consider the following certificate hierarchy:

![example hierarchy](/en/images/example-hierarchy.png "example hierarchy")
The certificate hierarchy presented above is currently (as of the time of writing this document) used in the Corda Network.
It follows practices applicable for certificate authorities providing a balance between security and simplicity of usage.
In this scenario, a network operator wants to create a CA hierarchy where the self-signed Root CA issues a certificate for the Subordinate CA which in turn issues
two certificates for both Identity Manager CA and Network Map (note that the Network Map is not a CA-type entity).
The root certificate is self-signed and its keys are to be protected with the highest security level. In normal circumstances,
they would be used just once to sign lover-level certificates (in this case the Subordinate CA) and then placed in some secure location,
preferably not being accessed anymore.
Further down in the hierarchy, the Subordinate certificate is then used to issue other certificates for other CAs.
Additionally, there is the TLS CRL signer entity, which is also self-signed and does not act as a CA.
As a matter of fact, for the purpose of signing the TLS CRL, we could reuse the Root CA certificate (as it is self-signed and is assumed to be in the network trust store),
however to keep the split of responsibilities let us assume that the network operator uses a separate certificate for that purpose.
Therefore, the TLS CRL signer certificate’s sole purpose is to sign a certificate revocation list, therefore the security constraints can be relaxed in this case,
compared to those applied to the Root CA.

As mentioned at the beginning of this document, each CA needs to maintain its own certificate revocation list.
Therefore, along with the keys and certificates being created for all of those four entities, three certificate revocation lists
need to be created and signed by Root CA, Subordinate CA and TLS CRL Signer respectively. The TLS CRL Signer differs from the others as,
although it is not a CA, it still signs a certificate revocation list.
That list is used by nodes during the SSL handshake process and in case where a node (which is a CA) is not able to
provide for its own certificate revocation list.
Regarding the Identity Manager, here we assume that the certificate revocation list is kept in the database and therefore no
static (i.e. file based) certificate revocation list signing is required.

With all of those in mind we can see the certificate revocation list of the TLS chain validation process as follows:

* The Root CA certificate is self-signed and trusted - present in the node’s trust store. As such it does not require any certificate revocation list validation.
* The Subordinate CA certificate is validated by checking the certificate revocation list signed by the Root CA. In the diagram in the previous section, it is given as a static file called `root.crl`.
* The Identity Manager Service CA certificate is validated by checking the certificate revocation list signed by the Subordinate CA. In the diagram in the previous section, it is given as a static file called `subordinate.crl`.
* The Node CA certificate is validated by checking the certificate revocation list signed by the Identity Manager Service CA. This list is dynamically maintained and stored in the database.
* The TLS certificate is validated by checking the certificate revocation list signed by the TLS CRL signer. In the diagram in the previous section, it is given as a static file called `tls.crl`.

Alternatively, the node operator may choose to use its own certificate revocation list infrastructure. However, this setup is out of the scope of the example scenario.


To generate all the artifacts of this scenario, a user needs to pass the correct configuration file to the PKI Tool.
The following is the example of the configuration file that will result in generating the above certificate hierarchy:

```docker
defaultPassword = "password"
keyStores = {
    "identity-manager-key-store" = {
        type = LOCAL
        file = "./key-stores/identity-manager-key-store.jks"
    }
    "network-map-key-store" = {
        type = LOCAL
        file = "./key-stores/network-map-key-store.jks"
    }
    "subordinate-key-store" = {
        type = LOCAL
        file = "./key-stores/subordinate-key-store.jks"
    }
    "root-key-store" = {
        type = LOCAL
        file = "./key-stores/root-key-store.jks"
    }
    "tls-crl-signer-key-store" = {
        type = LOCAL
        file = "./key-stores/tls-crl-signer-key-store.jks"
    }
}
certificatesStores = {
    "truststore" = {
        file = "./trust-stores/network-root-truststore.jks"
    }
}
certificates = {
    "cordatlscrlsigner" = {
        key = {
            type = LOCAL
            includeIn = ["tls-crl-signer-key-store"]
        }
        isSelfSigned = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["truststore"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        }
    },
    "cordarootca" = {
        key = {
            type = LOCAL
            includeIn = ["root-key-store"]
        }
        isSelfSigned = true
        subject = "CN=Test Foundation Service Root Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["truststore"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasubordinateca" = {
        key = {
            type = LOCAL
            includeIn = ["subordinate-key-store"]
        }
        signedBy = "cordarootca"
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        key = {
            type = LOCAL
            includeIn = ["identity-manager-key-store"]
        }
        signedBy = "cordasubordinateca"
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        role = DOORMAN_CA
    },
    "cordanetworkmap" = {
        key = {
            type = LOCAL
            includeIn = ["network-map-key-store"]
        }
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        role = NETWORK_MAP
    }
}
```

To simplify things even more, the PKI Tool assumes default values as much as possible so the user
is only required to provide only essential information to the tool. At the same time, the tool allows for overriding those
defaults and have the configuration adjusted to the specific needs of different scenarios.

{{< note >}}
To learn more about running the tool, see [Public Key Infrastructure (PKI) Tool](pki-tool.md).

{{< /note >}}
