---
title: "TLS Certification Installation on REST Worker"
version: 'Corda 5.0'
date: '2023-05-29'
menu:
  corda5:
    identifier: corda5-tls-certification-installation
    parent: corda5-cluster-config
    weight: 3075
section_menu: corda5
---

# TLS Certificate Installation on REST Worker

The REST Worker TLS certificate is presented to a client any time a HTTPS connection is made.
If no specific parameters are provided, the self-signed certificate is used and the connection to the REST Worker is always HTTPS. However, a warning will be emitted into the REST log explaining how to provide parameters for custom TLS certificates.
There are two ways that a TLS certificate can be made available to the REST Worker. For either method, there are three pieces of information required to install a valid TLS certificate.

* The TLS certificate itself is signed by a Certification Authority (CA) or an intermediary.
* A private key corresponding to the public key is included in the TLS certificate.
* The Certification Chain leads up to CA.

## Certificate Information Provided in PEM Format

REST Worker now accepts optional command line arguments: 

* PEM representation of a TLS certificate to be used: `-rtls.crt.path=<path to tls.crt>`

* PEM representation of the private key and of the CA certificate. This could also be a certification path where CA certificate is listed as the last one on the file: `-rtls.key.path=<path to tls.key>`

## Use with Helm Chart

When deploying the C5 cluster to Kubernetes using Helm, certificate information can be provided as a Kubernetes secret. 
The Cluster administrator can either create a Kubernetes secret manually to hold the certificate information or allow Helm to generate a new secret.

You can specify the secret name in the Helm values file under the parameter  `Values.workers.rest.tls.secretName`. If this optional value is not provided, Helm generates the certificate data at installation time and automatically creates a Kubernetes secret for the REST Worker to use.

{{< note >}}
If the TLS certificate has been installed as a Kubernetes secret and subsequently secret data modified, REST Worker Pod will not currently detect a change in the TLS certificate data until Pod is restarted.
{{</ note >}}

## Certificate Information Provided as PKCS12 Key Store

Alternatively, it is possible to supply information as a password protected PKCS12 key store.

To pass a PKCS12 key store to the REST Worker, the following start-up arguments can be used:

* The full path to a key store file: `-rtls.keystore.path=<path to a keystore>`
* Password is used for opening the key store: `-rtls.keystore.password=<password>`

{{< note >}}
R3 recommend passing the password through an environment variable.
{{< /note >}}