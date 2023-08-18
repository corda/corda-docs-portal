---
title: "Certificates Keys and Certificates in Corda 5.1"
date: 2023-04-21
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-certficates
    parent: corda51-intro
    weight: 5000
section_menu: corda51
---

This page is to document different types of keys and certificates in Corda 5 and their purpose.

## List of Keys

<table>
<col style="width:20%">
<col style="width:15%">
<col style="width:50%">
<col style="width:15%">
<thead>
<tr>
<th>Key name</th>
<th>Is it used with Certificate</th>
<th>Description</th>
<th>Key type/algorithm</th>
</tr>
</thead>
<tbody>
<tr>
<td>P2P TLS key </td>
<td><code>Yes</code></td>
<td>Part of TLS encryption at Corda cluster gateway level.</td>
<td> </td>
</tr>
<tr>
<td>Session initiation key</td>
<td>Yes</td>
<td>Used during end-to-end session handshake between 2 clusters, used to sign group parameters.</td>
<td> </td>
</tr>
<tr>
<td>ECDH (MGM)</td>
<td><code>No </code></td>
<td>Used for encryption/decryption of registration requests sent to MGM by members.</td>
<td> </td>
</tr>
<tr>
<td>Notary key</td>
<td>No </td>
<td>Combination of Notary Key + X500 Name,at Notarisation stage of Finality, the Notary Key is used to sign a transaction. Once a transaction is signed using the Notary Key, a transaction is deemed Notarised.</td>
<td> ECDSA key pair </td>
</tr>
<tr>
<td>REST TLS key</td>
<td>Yes</td>
<td>Stored on local files, supplied via command line arguments to the REST worker.</td>
<td> </td>
</tr>
<tr>
<td>REST SSO keys</td>
<td> TBD</td>
<td> AzueAD OIDC/OAuth2 </td>
<td> </td>
</tr>
<tr>
<td>Master wrapping key</td>
<td> No</td>
<td> A set of master wrapping keys are specified in the configuration of the crypto processor, as SALT and passphrase parameters for key derivation function. This produces a symmetric key which is used for wrapping (i.e. encrypting at rest) all corda managed wrapping keys. </td>
<td>AES </td>
</tr>
<tr>
<td>Corda managed wrapping key</td>
<td> No</td>
<td> These are symmetric keys used to wrap higher level asymmetric private keys. They are stored, wrapped by a master wrapping key, in Crypto databases in both the cluster and per vnode.  </td>
<td>AES </td>
</tr>
<tr>
<td>CPI publisher key</td>
<td> TBD </td>
<td> In some cases this will be managed by the clients, but in some cases it could be managed by R3,for example, Notary CPI.  </td>
<td> Asymmetric key pair </td>
</tr>
<tr>
<td> Ledger Key</td>
<td> TBD </td>
<td> Also known as VNode private ledger signing key public and private VNode ledger keys. Key is used to sign flows and consume Corda network ledger states. This key is critical for availability  </td>
<td>  Asymmetric key pair </td>
</tr>
<tr>
<td>Encryption secrets service wrapping key</td>
<td> No</td>
<td> This is a single master wrapping key specified via a salt and passphrase in the environment of the Corda workers, which are used to derive a symmetric key.  </td>
<td> </td>
</tr>
<tr>
<td>HTTP Gateway TLS key</td>
<td> No</td>
<td> TLS key for HTTP Gateway / REST API connections </td>
<td> ECDSA private key </td>
</tr>
</tbody>
</table>

## PKI assets

A list of PKI assest supported by Corda 5.

<table>
<col style="width:20%">
<col style="width:15%">
<col style="width:50%">
<col style="width:15%">
<thead>
<tr>
<th>PKI name</th>
<th>Description</th>
<th>Type</th>
</tr>
</thead>
<tbody>
<tr>
<td>Client Kafka credentials for a specific worker</td>
<td> Kafka credentials (username and password) Kafka client credentials are created at deployment time and stored by default in Kubernetes ETCD as secret configuration. This value is passed to worker pods memory at runtime. </td>
<td> Unencrypted string </td>
</tr>
<tr>
<td>Cluster DB credentials</td>
<td> Cluster DB credentials </td>
<td> Unencrypted string </td>
</tr>
<tr>
<td>Kafka truststore</td>
<td> Kafka truststore for server authentication (TLS) </td>
<td> PEM </td>
</tr>
</tbody>
</table>

## List of Credentials

<table>
<col style="width:20%">
<col style="width:15%">
<col style="width:50%">
<col style="width:15%">
<thead>
<tr>
<th>Credential name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>SSO config credentials</td>
<td> SSO credentials living inside the HTTP Gateway process. The credential is currently an API_ID (long randon string) provided by Azure AD. </td>
</tr>
<tr>
<td>Installation credentials creation</td>
<td>Creation of the installation credentials with enough entropy </td>
</tr>
<tr>
<td>Client Kafka credentials for a specific worker</td>
<td> Kafka credentials (username and password) Kafka client credentials are created at deployment time and stored by default in Kubernetes ETCD as secret configuration. This value is passed to worker pods memory at runtime. </td>
</tr>
<tr>
<td>Kubernetes secrets creation via API</td>
<td> The Infrastructure operator creates the secrets in the Kubernetes (etcd) to be used by the installation scripts (helm charts). This is executed optionally when Helm charts overrides are not used in alternative. </td>
</tr>
<tr>
<td>Kubernetes secrets configured in Helm charts</td>
<td> Secrets are configured (overrides) inside helm charts; using this as an alternate option to DF_K8S_SECRET_CONFIG. </td>
</tr>
<tr>
<td>HELM chart execution</td>
<td> Corda cluster installation HELM chart execution targeting a Kubernetes environment</td>
</tr>
<tr>
<td>CLUSTER_OPERATOR user credentials</td>
<td> Cluster operator user credentials</td>
</tr>
</tbody>
</table>