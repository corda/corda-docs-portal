---
date: '2023-06-21'
version: 'Corda 5.0'
title: "crypto"
menu:
  corda5:
    identifier: corda5-api-crypto
    parent: corda5-api
    weight: 5000
section_menu: corda5
---
# net.corda.v5.crypto

The `crypto` package provides types used by services in `net.corda.v5.application.crypto`. The following types are available:

* `DigitalSignature` is used to identify the owner of the signing key used to create the signature.
* `SecureHash` is a cryptographically secure hash value, computed by a specified digest algorithm.
* `SignatureSpec` is a digital signature scheme.

## Implementing Signature Schemes

Corda supports the following `SignatureSpec`s (signature schemes) for creating the following objects:

* SHA256withRSA
* SHA384withRSA
* SHA512withRSA
* RSASSA-PSS with SHA256
* RSASSA-PSS with SHA384
* RSASSA-PSS with SHA512
* RSASSA-PSS with SHA256 and MGF1
* RSASSA-PSS with SHA384 and MGF1
* RSASSA-PSS with SHA512 and MGF1
* SHA256withECDSA
* SHA384withECDSA
* SHA512withECDSA
* EdDSA
* SHA512withSPHINCS256
* SM3withSM2
* SHA256withSM2
* GOST3411withGOST3410

SignatureSpecService ensures that you do not pass the wrong signature spec for a signing-key type. It takes in a key and, optionally, a digest algorithm, and returns the appropriate default signature spec.