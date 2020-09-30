---
date: '2020-09-29T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-corda-nodes-secrets
    name: "Corda Secrets"
    parent: corda-enterprise-4-6-corda-nodes

title: Corda secrets
weight: 110
---
# Corda secrets

This page documents the secrets that are managed and required by a Corda installation. The secrets fall into two categories:

* Cryptogtaphic keys.
* Passwords.

The relationships between the secrets and Corda components is shown in the following diagram.

{{% figure zoom="secrets/secrets.png" alt="Diagram showing the relationships between the secrets and components" %}}

## Node

Secrets managed by a Corda Node

{{< table >}}
| Secret | Location | Path | Protection | Accessible by | Description |
|--------|----------|------|------------|---------------|-------------|
| Node CA private key | Disk | `certificates/nodekeystore.jks` | JKS | Node |Node CA certificate issued by the Doorman (`cordaclientca`) |
| Legal Identity private key | Disk | `certificates/nodekeystore.jks` | JKS | Node | Legal identity used to sign transactions (`identity-private-key`) |
| TLS private key | Disk | `certificates/sslkeystore.jks` | JKS | Node | Certificate used for TLS communication (`cordaclienttls`) |
| Node CA private key | HSM | - | - | - | Node CA certificate issued by the Doorman |
| Legal Identity private key | HSM | - | - | - | Legal identity used to sign transactions |
| Confidential identity | DB | Vault database (`NODE_OUR_KEY_PAIRS`) |  | Node | Confidential Identity private keys, stored unencrypted |
| Node keystore password | Disk | `node.conf` | | | Node	Password used to protect the integrity of the node keystore |
| TSL keystore password | Disk | `node.conf` | | |Node	Password used to protect the integrity of the SSL keystore |
| Truststore password | Disk | `node.conf` |  | Node | Password used to protect the integrity of the trust store |
| HSM credentials | Disk | `hsm.conf` | | Node | Credentials for accessing the HSM, if configured. |
| Vault DB connection | Disk | `node.conf` | | Node | Database connection string that includes username & password |
| RPC credentials connection | Disk | `node.conf` | | Node | Database connections string for storing RPC credentials |
| RPC credentials | DB | Creds databse | Salted + Hashed (SHA256) | Node | Usernames & salted (& hashed) passwords in external data store |
{{< /table >}}


## Notary
Additional secrets managed by a Corda Notary

{{< table >}}
| Secret | Location | Path | Protection | Accessible by | Description |
|--------|----------|------|------------|---------------|-------------|
| Notary service key | Disk | `certificates/nodekeystore.jks` | JKS | Notary | Notary service identity issued by the Doorman (`distributed-notary-private-key`) |
{{< /table >}}

## Float & Bridge
Secrets managed by the Corda Float & Bridge

{{< table >}}
| Secret | Location | Path | Description |
|--------|----------|------|-------------|
| TLS private key | Disk | `certificates/sslkeystore.jks`  | Certificate used for TLS communication |
| TLS keystore password | Disk | `node.conf` || Password used to protect the integrity of the SSL keystore |
| Trust store password | Disk | `node.conf` |  Password used to protect the integrity of the trust store |
{{< /table >}}
