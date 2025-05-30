---
aliases:
- /releases/release-1.2/certificate-revocation.html
- /docs/cenm/head/certificate-revocation.html
- /docs/cenm/certificate-revocation.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-certificate-revocation
    parent: cenm-1-2-concepts-and-overview
    weight: 60
tags:
- certificate
- revocation
title: Certificate revocation list
---


# Certificate Revocation List

The certificate revocation list (CRL) consists of certificate serial numbers of issued certificates that are no longer valid.
It is used by nodes when they establish a TLS connection between each other and need to ensure on certificate validity.
In order to add entries to the certificate revocation list there is the certificate revocation process that resembles
the one from the certificate signing request (CSR).

For context on how the certificate revocation list fits into the wider context, please see [Certificate hierarchy guide]({{< relref "pki-guide.md" >}}).

Note that, once added the entries cannot be removed from the certificate revocation list.

In the similar vein as CSR, by default the approval workflow for revocation requests is integrated with the Jira tool,
and the submitted requests follow exactly the same lifecycle. To support the above functionality, there are two
externally available REST endpoints: one for the certificate revocation request submission and
one for the certificate revocation list retrieval.

Since the certificate revocation list needs to be signed, the revocation process integrates with the HSM Signing Service.
The certificate revocation list signing process requires human interaction and there is a separate tool designed for that purpose.
Once signed the certificate revocation list replaces the current one.

{{< note >}}
It is assumed that the signed certificate revocation list is always available - even if it’s empty. Nodes
will refuse to make TLS connections if they cannot verify the revocation status of certificates in the
remote peer’s chain, and therefore the CRL must remain available for the network to operate.

{{< /note >}}
{{< note >}}
CRLs should be signed manually from time to time depending on its’ `nextUpdate` property. Further details
on CRL lifecycle are covered under [Lifecycle](#lifecycle).

{{< /note >}}

## HTTP certificate revocation protocol

The set of REST endpoints for the revocation service are determined by the CRL file names provided in the PKI tool configuration.
The example below shows the relevant part of such a PKI configuration along with the respective endpoints.

```guess
certificates = {
    "::CORDA_TLS_CRL_SIGNER" = {
        crl = {
          crlDistributionUrl = "http://identitymanager:10000/certificate-revocation-list/tls"
          indirectIssuer = true
          issuer = "CN=Corda TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
          file = "/etc/corda/crl-files/tls.crl"
        }
    },
    "::CORDA_ROOT" = {
        crl = {
          crlDistributionUrl = "http://identitymanager:10000/certificate-revocation-list/root"
          file = "/etc/corda/crl-files/root.crl"
        }
    },
    "::CORDA_SUBORDINATE" = {
        crl = {
          crlDistributionUrl = "http://identitymanager:10000/certificate-revocation-list/subordinate"
          file = "/etc/corda/crl-files/subordinate.crl"
        }
    }
)
```


{{< table >}}

|Request method|Path|Description|
|----------------|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
|POST|/certificate-revocation-request|Uploads a certificate revocation request.|
|GET|/certificate-revocation-list/subordinate|Retrieves the certificate revocation list issued by the Subordinate CA. The Subordinate CA is the intermediary certificate between the root, and the Doorman CA. Returns an ASN.1 DER-encoded CRL, as defined in RFC 3280.|
|GET|/certificate-revocation-list/tls|Retrieves the certificate revocation list of the TLS root CA. This TLS hierarchy is used for communication between CENM services (not Corda nodes). Returns an ASN.1 DER-encoded CRL, as defined in RFC 3280.|
|GET|/certificate-revocation-list/root|Retrieves the certificate revocation list issued by the Root CA. Returns an ASN.1 DER-encoded CRL, as defined in RFC 3280.|

{{< /table >}}


## Empty certificate revocation list

The TLS-level certificate revocation check validates the entire certificate chain. It means that for each certificate in the
certificate path the corresponding CRL will be downloaded and the certificate will be checked against that CRL.
However, this introduces a requirement on each Certificate Authority (including the Node CA) to provide a CRL for the
certificates it issues. Since this requirement cannot be always met especially by the Node CA, the alternative approach
is to use a CRL signed by the trusted CA. Since each Corda node trusts the Root CA an additional empty CRL signed by the
Root CA is provided on one of the revocation service endpoints (see the table above) and can be used for any certificate
issued by the Node CA.


## Certificate revocation request submission

Submission of the certificate revocation requests expects the following fields to be present in the request payload:


* **certificateSerialNumber**:
Serial number of the certificate that is to be revoked.


* **csrRequestId**:
Certificate signing request identifier associated with the certificate that is to be revoked.


* **legalName**:
Legal name associated with the certificate that is to be revoked.


* **reason**:
Revocation reason (as specified in the java.security.cert.CRLReason). The following values are allowed:


* **KEY_COMPROMISE**:
This reason indicates that it is known or suspected that the certificate subject’s private key has been compromised. It applies to end-entity certificates only.


* **CA_COMPROMISE**:
This reason indicates that it is known or suspected that the certificate subject’s private key has been compromised. It applies to certificate authority (CA) certificates only.


* **AFFILIATION_CHANGED**:
This reason indicates that the subject’s name or other information has changed.


* **SUPERSEDED**:
This reason indicates that the certificate has been superseded.


* **CESSATION_OF_OPERATION**:
This reason indicates that the certificate is no longer needed.


* **PRIVILEGE_WITHDRAWN**:
This reason indicates that the privileges granted to the subject of the certificate have been withdrawn.




* **reporter**:
Issuer of this certificate revocation request.



Also, Corda AMQP serialization framework is used as the serialization framework.Because of the proprietary serialization mechanism, it is assumed that those endpoints are used by dedicated tools that support this kind of data encoding.


## Internal protocol

There is an internal communication protocol between the Signing Service and the HSM Signing Service for producing the signed CRLs.
This does not use HTTP to avoid exposing any web vulnerabilities to the signing process.



## Lifecycle

CRLs contain a field, “next update”, after which the CRL is no longer valid. This is to ensure
an up-to-date CRL is distributed in the network before the previous one expires. Conventionally they have a
lifecycle of 6 months and are manually signed every 3 months. Such a schedule gives plenty of time for
any signing issues to be resolved.

See [Signing services]({{< relref "signing-service.md" >}}) for details on building and signing CRLs, and especially the “updatePeriod”
configuration field which is used to determine the next update deadline. See also [CRL Endpoint Check Tool]({{< relref "crl-endpoint-check-tool.md" >}})
for more information how to check CRLs’ update deadlines.
