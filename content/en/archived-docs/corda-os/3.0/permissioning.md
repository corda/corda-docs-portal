---
aliases:
- /releases/release-V3.0/permissioning.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-0:
    identifier: corda-os-3-0-permissioning
    parent: corda-os-3-0-corda-networks-index
    weight: 1020
tags:
- permissioning
title: Network permissioning
---


# Network permissioning


Corda networks are *permissioned*. To connect to a network, a node needs three keystores in its
`<workspace>/certificates/` folder:


* `truststore.jks`, which stores trusted public keys and certificates (in our case, those of the network root CA)
* `nodekeystore.jks`, which stores the node’s identity keypairs and certificates
* `sslkeystore.jks`, which stores the node’s TLS keypairs and certificates

Production deployments require a secure certificate authority.
Most production deployments will use an existing certificate authority or construct one using software that will be
made available in the coming months. Until then, the documentation below can be used to create your own certificate
authority.


## Certificate hierarchy

A Corda network has four types of certificate authorities (CAs):


* The **root network CA**
* The **doorman CA**
    * The doorman CA is used instead of the root network CA for day-to-day
key signing to reduce the risk of the root network CA’s private key being compromised


* The **node CAs**
    * Each node serves as its own CA in issuing the child certificates that it uses to sign its identity
keys and TLS certificates


* The **legal identity CAs**> 

    * Node’s well-known legal identity, apart from signing transactions, can also issue certificates for confidential legal identities




The following constraints are also imposed:


* Doorman certificates are issued by a network root which certificate doesn’t contain the extension
* Well-known service identity certificates are issued by an entity with a Doorman certificate
* Node CA certificates are issued by an entity with a Doorman certificate
* Well known legal identity/TLS certificates are issued by a certificate marked as node CA
* Confidential legal identity certificates are issued by a certificate marked as well known legal identity
* Party certificates are marked as either a well known identity or a confidential identity
* The structure of certificates above Doorman/Network map is intentionally left untouched, as they are not relevant to
the identity service and therefore there is no advantage in enforcing a specific structure on those certificates. The
certificate hierarchy consistency checks are required because nodes can issue their own certificates and can set
their own role flags on certificates, and it’s important to verify that these are set consistently with the
certificate hierarchy design. As as side-effect this also acts as a secondary depth restriction on issued
certificates

All the certificates must be issued with the custom role extension (see below).

We can visualise the permissioning structure as follows:

![certificate structure](/en/images/certificate_structure.png "certificate structure")

## Keypair and certificate formats

You can use any standard key tools or Corda’s `X509Utilities` (which uses Bouncy Castle) to create the required
public/private keypairs and certificates. The keypairs and certificates should obey the following restrictions:


* The certificates must follow the [X.509 standard](https://tools.ietf.org/html/rfc5280)> 

    * We recommend X.509 v3 for forward compatibility



* The TLS certificates must follow the [TLS v1.2 standard](https://tools.ietf.org/html/rfc5246)
* The root network CA, doorman CA and node CA keys, as well as the node TLS
keys, must follow one of the following schemes:> 

    * ECDSA using the NIST P-256 curve (secp256r1)
    * RSA with 3072-bit key size





## Certificate role extension

Corda certificates have a custom X.509 v3 extension that specifies the role the certificate relates to. This extension
has the OID `1.3.6.1.4.1.50530.1.1` and is non-critical, so implementations outside of Corda nodes can safely ignore it.
The extension contains a single ASN.1 integer identifying the identity type the certificate is for:


* Doorman
* Network map
* Service identity (currently only used as the shared identity in distributed notaries)
* Node certificate authority (from which the TLS and well-known identity certificates are issued)
* Transport layer security
* Well-known legal identity
* Confidential legal identity

In a typical installation, node administrators needn’t be aware of these. However, when node certificates are managed
by external tools (such as an existing PKI solution deployed within an organisation), it is important to understand
these constraints.

Certificate path validation is extended so that a certificate must contain the extension if the extension was present
in the certificate of the issuer.


## Creating the root and doorman CAs


### Creating the root network CA’s keystore and truststore


* Create a new keypair
* This will be used as the root network CA’s keypair


* Create a self-signed certificate for the keypair. The basic constraints extension must be set to `true`
* This will be used as the root network CA’s certificate


* Create a new keystore and store the root network CA’s keypair and certificate in it for later use
* This keystore will be used by the root network CA to sign the doorman CA’s certificate


* Create a new Java keystore named `truststore.jks` and store the root network CA’s certificate in it using the
alias `cordarootca`
* This keystore must then be provisioned to the individual nodes later so they can store it in their `certificates` folder




{{< warning >}}
The root network CA’s private key should be protected and kept safe.

{{< /warning >}}



### Creating the doorman CA’s keystore


* Create a new keypair
* This will be used as the doorman CA’s keypair


* Obtain a certificate for the keypair signed with the root network CA key. The basic constraints extension must be
set to `true`
* This will be used as the doorman CA’s certificate


* Create a new keystore and store the doorman CA’s keypair and certificate chain
(i.e. the doorman CA certificate *and* the root network CA certificate) in it for later use
* This keystore will be used by the doorman CA to sign the nodes’ identity certificates




## Creating the node CA keystores and TLS keystores


### Creating the node CA keystores


* For each node, create a new keypair
* Obtain a certificate for the keypair signed with the doorman CA key. The basic constraints extension must be
set to `true`
* Create a new Java keystore named `nodekeystore.jks` and store the keypair in it using the alias `cordaclientca`
* The node will store this keystore locally to sign its identity keys and anonymous keys




### Creating the node TLS keystores


* For each node, create a new keypair
* Create a certificate for the keypair signed with the node CA key. The basic constraints extension must be set to
`false`
* Create a new Java keystore named `sslkeystore.jks` and store the key and certificates in it using the alias
`cordaclienttls`
* The node will store this keystore locally to sign its TLS certificates




## Installing the certificates on the nodes

For each node, copy the following files to the node’s certificate directory (`<workspace>/certificates/`):


* The node’s `nodekeystore.jks` keystore
* The node’s `sslkeystore.jks` keystore
* The root network CA’s `truststore.jks` keystore

