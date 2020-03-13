---
aliases:
- /releases/release-1.0/generating-key-certificate-hsm.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- generating
- certificate
- hsm
title: Generating HSM Keys and Certificates
---


# Generating HSM Keys and Certificates

This document describes the entire process for generating a key pair and the associated certificate on the Utimaco HSM
using the ENM tools.

The process can be summarised in the following three steps:


## 1. Generating the key pair and the certificate signing request.

This step results in the key pair being generated on the HSM
as well as a certificate signing request file being created locally in the file system. The file consists of the public
part of the generated key pair as well as the subject, which are then used in next step of the process.
See tool-key-csr-generator for more details.

Example command:

```guess
java -jar utilities.jar key-csr-generator --config-file key-csr-generator.conf
```

where the key-csr-generator.conf could be as follows:

```guess
keyStore = {
        host = 127.0.0.1
        port = 3001
        users = [
        {
                username = "USER"
                mode = PASSWORD
                password = "PASSWORD"
        }
        ]
}
key = {
    keyGroup = "EXAMPLE.GROUP"
    keySpecifier = 1
    keyAlias = "rootca"
    storeKeysExternal = false
    keyOverride = 0
    keyExport = 1
    keyCurve = "NIST-P256"
    keyGenMechanism = 4
}
subject = "CN=Root CA, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
csrFile = "root.csr"
```


## 2. Signing the Certificate Signing Request

This step takes the certificate signing request produced in the previous step and signs it with a key specified in
the configuration file. As a result a new certificate is produced and stored in the JKS file. The certificate has
the subject and public key specified in the certificate signing request.

Example command:

```guess
java -jar utilities.jar csr-signer --config-file csr-sign.conf
```

where the csr-sign.conf could be as follows:

```guess
keyStore = {
        host = 192.168.56.101
        port = 3001
        users = [
        {
                username = "USER"
                mode = PASSWORD
                password = "PASSWORD"
        }
        ]
}
csrFile = "cna1.csr"
certificatesStore {
    storeFile = "./certificateStore.jks"
    storePassword = "password"
    certificateAlias = "cna1"
}
certificate = {
        signingKey = {
                keyAlias = "rootca"
                keyGroup = "EXAMPLE.GROUP"
                keySpecifier = 1
        }
    signatureAlgorithm = "SHA384withECDSA"
    validDays = 7300
    keyUsages = [ DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN ],
    keyPurposes = [ SERVER_AUTH, CLIENT_AUTH ]
    issuesCertificates = true
    cpsUrl = "https://trust.corda.network"
    crlDistributionUrl = "http://crl.corda.network/cr1.crl"
    authorityAccessInfo = {
        ocspUrl = "http://ocsp.corda.network/cfr"
    }
}
certificateAlias = "cna1"
```


## 3. Uploading the certificate to the HSM

This step takes the JKS file produced in the previous step and uploads the certificate generated in the previous step
to the HSM.

Example command:

```guess
java -jar utilities.jar cert-updater --config-file cert-update.conf
```

where the cert-update.conf could be as follows:

```guess
keyStore = {
        host = 127.0.0.1
        port = 3001
        users = [
        {
                username = "USER"
                mode = PASSWORD
                password = "PASSWORD"
        }
        ]
}
certificatesStore {
    storeFile = "./certificateStore.jks"
    storePassword = "password"
    certificateAlias = "cna1"
}
key = {
        keyAlias = "cna1"
        keyGroup = "EXAMPLE.GROUP"
        keySpecifier = 1
```


## 4. Copying certificates between local JKS certificate stores

This step takes the JKS file produced in the previous step and another (target) JKS file. If the target JKS file does not exist it will create a new one.

Example command:

```guess
java -jar utilities.jar local-cert-copier --config-file cert-copier.conf
```

where the cert-copier.conf could be as follows:

```guess
sourceCertificatesStore {
    file = "./certificateStore.jks"
    password = "password"
    certificateAlias = "stgrootca"
}
targetCertificatesStore {
    file = "./network-root-truststore.jks"
    password = "trustpass"
    certificateAlias = "cordarootca"
}
```

