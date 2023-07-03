---
date: '2023-06-21'
version: 'Corda 5.0 Beta 4'
title: "net.corda.v5.crypto"
menu:
  corda5:
    identifier: corda5-api-crypto
    parent: corda5-api
    weight: 5000
section_menu: corda5
draft: true
---
# net.corda.v5.crypto

The `corda-crypto` module 

## Implementing Signature Schemes

Corda supports the following `SignatureSpecs` (signature schemes) for creating `java.security.Signature` objects:
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
