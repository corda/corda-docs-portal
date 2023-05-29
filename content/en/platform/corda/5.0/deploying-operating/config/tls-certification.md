---
title: "TLS Certification Installation on REST Worker"
version: 'Corda 5.0'
date: '2023-05-29'
menu:
  corda5:
    identifier: corda5-tls-certification-installation
    parent: corda5-cluster-config
    weight: 4000
section_menu: corda5
---

# TLS Certification Installation on REST Worker

For the Corda 5 GA release the TLS certificate on REST Worker is presented to a client any time HTTPS connection is made.
Before, a self-signed certificate shipped with the REST Worker. If no specific parameters are provided, the self-signed certificate will be used as a default option such that the connection to the REST Worker is always HTTPS. However, a warning will be emitted into the REST log explaining how to provide parameters for custom TLS certificates.
There are a few ways that a TLS certificate can be made available to the REST Worker. For eithr method there are three pieces of information required to install a valid TLS certificate.

1. The TLS certificate itself is signed by a Certification Authority (CA) or an intermediary;
2. A private key corresponding to the public key is included into the TLS certificate;
3. The Certification Chain leads up to CA

## Certificate Information Provided in PEM Format

REST Worker now accepts optional command line arguments: 

1. `-rtls.crt.path=<path to tls.crt>`
PEM representation of a TLS certificate to be used.

2. `-rtls.key.path=<path to tls.key>`
PEM representation of the private key.
PEM representation of the CA certificate. This could also be a certification path where CA certificate is listed as the last one on the file.

## Use with Helm Chart

When deploying the C5 cluster to Kubernetes (K8s) using Helm, certificate information can be provided as a K8s secret. 
The C5 Cluster operator can either create K8s secret which hold certificate information themselves or allow Helm to generate a new secret.

Our Helm values file now has a parameter to specifysecret name under `Values.workers.rest.tls.secretName`. If this optional value is not provided, Helm will generate certificate data at installation time and will automatically create K8s secret for REST Worker to use.

{{< note >}}
If the TLS certificate has been installed as a K8s secret and subsequently secret data modified, REST Worker Pod will not currently detect a change in the TLS certificate data until Pod is restarted.
{{</ note >}}

## Certificate information provided as PKCS12 key store

Alternatively, it is possible to supply such information as password protected PKCS12 key store.

In order to pass PKCS12 key store to REST Worker, the following start-up arguments can be used:

1. The full path to a key store file: `-rtls.keystore.path=<path to a keystore>`

2. Password is used for opening the key store: `-rtls.keystore.password=<password>`

{{< note >}}
It is best practice to pass the password through an environment variable.
{{< /note >}}