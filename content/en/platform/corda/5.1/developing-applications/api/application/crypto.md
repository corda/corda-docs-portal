---
date: '2023-08-10'
version: 'Corda 5.1'
title: "application.crypto"
menu:
  corda51:
    identifier: corda51-api-app-crypto
    parent: corda51-api-application
    weight: 1000
section_menu: corda51
---
# net.corda.v5.application.crypto
The `crypto` package provides services and types for performing cryptographic operations. The main services available to applications are:

* The <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/crypto/SigningService.html" target="_blank">`SigningService`</a> is for signing and removing objects.
* The <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/crypto/DigitalSignatureVerificationService.html" target="_blank">`DigitalSignatureVerificationService`</a> is for verifying signatures.
* The <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/crypto/DigestService.html" target=" blank">`DigestService`</a> provides hashing capabilities to {{< tooltip >}}CorDapps{{< /tooltip >}}.

For more information, see the documentation for the package in the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/crypto/package-summary.html" target=" blank">Java API documentation</a>.
