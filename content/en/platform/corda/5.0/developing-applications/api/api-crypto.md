---
date: '2023-06-21'
version: 'Corda 5.0'
title: "net.corda.v5.crypto"
menu:
  corda5:
    identifier: corda5-api-crypto
    parent: corda5-api
    weight: 5000
section_menu: corda5
---
# net.corda.v5.crypto

The `crypto` package provides services and types for performing cryptographic operations. The list of services available are:

* The `CompositeKey` is a tree data structure that enables the representation of composite public keys, which are used to represent the signing requirements for multi-signature scenarios.
* The `DigestAlgorithmName` is to be used in Corda hashing API.
* The `DigitalSignature` is for identifying who is the owner of the signing key used to create this signature.
* The `SecureHash` is a cryptographically secure hash value, computed by a specified digest algorithm.
* The `SignatureSpec` is a digital signature scheme.

## Implementing Signature Schemes

Corda supports the following `SignatureSpecs` (signature schemes) for creating the following objects:

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

Use `SignatureSpecService` to retrieve the `SignatureSpec`.

Initially the above list of signature spec was available to users. However, they could be passing the wrong signature spec for a signing key type (e.g. an RSA key with an SHA256withECDSA), which would lead to an error when attempting to generate the signature.

Instead, `SignatureSpecService` was introduced. It takes in a key (and a digest algorithm optionally) and returns a default signature spec for those.