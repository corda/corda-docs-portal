---
aliases:
- /releases/4.4/release-notes-enterprise.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-release-notes
tags:
- release
- notes
- enterprise
title: Corda Enterprise Release notes
---


# Corda Enterprise Release notes


## Corda Enterprise 4.4

This release extends the [Corda Enterprise 4.3 release](https://docs.corda.net/docs/corda-enterprise/4.3/release-notes-enterprise.html)
with further performance, resilience and operational improvements.

Corda Enterprise 4.4 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. Please refer to product documentation for details.

Corda Enterprise 4.4 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.3, 4.2, 4.1, 4.0 and 3.x, while providing enterprise-grade features and performance.


### Key new features and components


#### Corda Open Core


Starting with Corda Enterprise 4.4, Corda Enterprise and Open Source share the same core and API libraries - the Enterprise version
now has a binary dependency on the matching Open Source release. This reduces maintenance overhead, and improves API compatibility
and interoperability between the Open Source and Enterprise versions.

This change has some implications on the upgrade process (see “Upgrade Notes” section later on).



#### Further Hardware Security Module (HSM) support


This release adds support for storing the node’s CA and legal identity key in a [nCipher nShield Connect](https://www.ncipher.com/products/general-purpose-hsms/nshield-connect) HSM.
Please refer to the associated section of the cryptoservice-configuration page for more details.

We also have extended the set of HSMs available for the storage of a highly-available notary’s shared service key. The notary’s shared service key can now be stored in the following HSM types:


* Utimaco
* Gemalto Luna
* nCipher



#### Performance improvements


This release introduces an optimisation for sharing transaction backchains. Corda Enterprise nodes can request backchain items in bulk instead of one at a time (the configuration property `backchainFetchBatchSize` can be used to define the size of the batch).

Responding nodes (Enterprise or Open Source) running at platform version >= 6 will supply backchain items in bulk up to half of the network’s allowed maximum message size (minimum one item; items exceeding the limit are sent in subsequent batches). Nodes running on older platform version will still supply backchain items one at a time.

The release also includes the ability to configure the timeout and buffer size that ActiveMQ Artemis uses to flush produced messages to disk and send acknowledgements back to the client. This is exposed via a set of additional node configuration properties (`journalBufferTimeout`, `journalBufferSize` and `brokerConnectionTtlCheckIntervalMs`). Optimizing these values for your particular use case may result in improved latency depending on the characteristics of the hardware infrastructure.



#### HA Notary registration process improvements


We have introduced a set of improvements to make it easier to register a highly-available notary onto a Corda network:


* The keystore containing the notary identity key that is generated during registration is given a name that clearly disambiguates it from a regular node keystore
* The notary can now be registered using its X500 name, as an alternative to providing a node info file. This allows the notary to be added to the network parameters before the notary is registered, and avoids the need to copy the node info file around between notary workers
* HA notary workers can retrieve the notary’s service certificate from the network map service, avoiding the need to manually copy it around between the various workers
* HA notary workers check they have access to the shared notary service key and certificate before they register with the notary



#### Corda Health Survey improvements


We have improved the Corda Health Survey tool to support a fuller range of node commissioning tasks, including:


* Verifying connectivity with other peers and Notaries
* Validating more complex deployments of Corda Enterprise (including HA node-Firewall combinations)
* Further connectivity checks on network infrastructure (check CRL endpoint via the Bridge)
* Further validation of node functionality (RPC connectivity)
* Warning operators that the node or Firewall configuration files are not obfuscated

Furthermore, we have improved the overall usability of the tool by adding support for running the tool via RPC.

The new version of the tool can only be used on Corda Enterprise 4.4 (and above) nodes. Peer connectivity checks can target any node or Notary running on the same network.



#### Configuration Obfuscator improvements


The Configuration Obfuscator has been improved to:


* Use a more robust key derivation function (PBKDF2 with HMAC-SHA256)
*
    * keyboard input (stdin)
    * Command-line
    * Environment variables



The new version of the tool is also able to de-obfuscate files obfuscated with older versions.

The new version of the tool can only be used with Corda Enterprise 4.4 (and above) node and Firewall configuration files.



### Known issues


### Upgrade notes

From Corda Enterprise 4.4 onwards, we are moving towards an open core strategy. Common APIs shared by Corda Enterprise will only be available in Corda Open Source. Therefore, any CorDapps written against Corda Enterprise 4.4 or later will have to depend on the open source version of `corda-core`.

As per previous major releases, we have provided a comprehensive upgrade notes ([Upgrading CorDapps to Corda Enterprise 4.4](app-upgrade-notes-enterprise.md)) to ease the upgrade
of CorDapps to Corda Enterprise 4.4.
