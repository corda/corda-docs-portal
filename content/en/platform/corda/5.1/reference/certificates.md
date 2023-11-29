---
title: "Corda Keys and Certificates"
date: '2023-11-28'
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-certificates
    parent: corda51-references
    weight: 4000
section_menu: corda51
---

# Corda Keys and Certificates

This section describes the different types of keys and certificates used by Corda 5. It contains the following:

{{< toc >}}

## Keys

Corda uses the following types of keys:

| Key                                     | Use with Certificate | Description                                                                                                                                                                                                                                                                  | Key Type/Algorithm  |
| --------------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| P2P TLS key                             | Yes                  | Part of TLS encryption at Corda cluster gateway level.                                                                                                                                                                                                                       |                     |
| Session initiation key                  | Yes                  | Used during end-to-end session handshake between 2 clusters, used to sign group parameters.                                                                                                                                                                                  |                     |
| ECDH (MGM)                              | No                   | Used for encryption/decryption of registration requests sent to MGM by members.                                                                                                                                                                                              |                     |
| Notary key                              | No                   | Combination of Notary Key and X500 Name, at Notarisation stage of Finality, the Notary Key is used to sign a transaction. Once a transaction is signed using the Notary Key, a transaction is deemed Notarised.                                                              | ECDSA key pair      |
| REST TLS key                            | Yes                  | Stored on local files, supplied via command line arguments to the REST worker.                                                                                                                                                                                               |                     |
| REST SSO keys                           | TBD                  | AzueAD OIDC/OAuth2                                                                                                                                                                                                                                                           |                     |
| Master wrapping key                     | No                   | A set of master wrapping keys are specified in the configuration of the crypto processor, as SALT and passphrase parameters for key derivation function. This produces a symmetric key which is used for wrapping (i.e. encrypting at rest) all corda managed wrapping keys. | AES                 |
| Corda managed wrapping key              | No                   | These are symmetric keys used to wrap higher level asymmetric private keys. They are stored, wrapped by a master wrapping key, in Crypto databases in both the cluster and per vnode.                                                                                        | AES                 |
| CPI publisher key                       | TBD                  | In some cases this will be managed by the clients, but in some cases it could be managed by R3,for example, Notary CPI.                                                                                                                                                      | Asymmetric key pair |
| Ledger Key                              | TBD                  | Also known as VNode private ledger signing key public and private VNode ledger keys. Key is used to sign flows and consume Corda network ledger states. This key is critical for availability                                                                                | Asymmetric key pair |
| Encryption secrets service wrapping key | No                   | This is a single master wrapping key specified via a salt and passphrase in the environment of the Corda workers, which are used to derive a symmetric key.                                                                                                                  |                     |
| HTTP Gateway TLS key                    | No                   | TLS key for HTTP Gateway / REST API connections                                                                                                                                                                                                                              | ECDSA private key   |

## PKI assets

Corda supports the following PKI assets:

| PKI name                                       | Description                                                                                                                                                                                                                | Type               |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| Client Kafka credentials for a specific worker | Kafka credentials (username and password) Kafka client credentials are created at deployment time and stored by default in Kubernetes ETCD as secret configuration. This value is passed to worker pods memory at runtime. | Unencrypted string |
| Cluster DB credentials                         | Cluster DB credentials                                                                                                                                                                                                     | Unencrypted string |
| Kafka truststore                               | Kafka truststore for server authentication (TLS)                                                                                                                                                                           | PEM                |

## List of Credentials

Corda uses the following credentials:

| Credential name                                | Description                                                                                                                                                                                                                |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SSO config credentials                         | SSO credentials living inside the HTTP Gateway process. The credential is currently an API\_ID (long randon string) provided by Azure AD.                                                                                  |
| Installation credentials creation              | Creation of the installation credentials with enough entropy                                                                                                                                                               |
| Client Kafka credentials for a specific worker | Kafka credentials (username and password) Kafka client credentials are created at deployment time and stored by default in Kubernetes ETCD as secret configuration. This value is passed to worker pods memory at runtime. |
| Kubernetes secrets creation via API            | The Infrastructure operator creates the secrets in the Kubernetes (etcd) to be used by the installation scripts (helm charts). This is executed optionally when Helm charts overrides are not used in alternative.         |
| Kubernetes secrets configured in Helm charts   | Secrets are configured (overrides) inside helm charts; using this as an alternate option to DF\_K8S\_SECRET\_CONFIG.                                                                                                       |
| HELM chart execution                           | Corda cluster installation HELM chart execution targeting a Kubernetes environment                                                                                                                                         |
| CLUSTER\_OPERATOR user credentials             | Cluster operator user credentials                                                                                                                                                                                          |