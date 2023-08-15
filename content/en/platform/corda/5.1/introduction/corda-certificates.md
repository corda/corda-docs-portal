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
<td> </td>
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
<td> </td>
</tr>
<tr>
<td>Encryption secrets service wrapping key</td>
<td> No</td>
<td> This is a single master wrapping key specified via a salt and passphrase in the environment of the Corda workers, which are used to derive a symmetric key.  </td>
<td> </td>
</tr>
</tbody>
</table>