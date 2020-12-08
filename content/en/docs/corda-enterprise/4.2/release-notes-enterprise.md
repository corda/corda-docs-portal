---
aliases:
- /releases/4.2/release-notes-enterprise.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-release-notes-enterprise
    weight: 20
tags:
- release
- notes
- enterprise
title: Release notes
---


# Release notes

## Corda Enterprise 4.2.2

Corda Enterprise 4.2.2 is a patch release of Corda Enterprise that introduces fixes to known issues in Corda Enterprise 4.2.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](https://docs.corda.net/docs/corda-enterprise/release-notes-enterprise.html).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issues listed below are relevant to your work.

### Fixed issues

* We have fixed a security issue relating to potential signature forgery. To do so, we have introduced batch signing capability in the `signTransactionAndSendResponse` of the `NotaryServiceFlow` flow so that a Merkle Tree is built with a single transaction to be signed, and then the transaction signature is constructed with the partial Merkle tree containing that single transaction.

## Corda Enterprise 4.2.1

Corda Enterprise 4.2.1 is a patch release of Corda Enterprise 4.2 that introduces a fix to a new issue related to a recent third-party dependency update.

### Upgrade recommendation

As a developer, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) as soon as possible. Check the latest Corda Enterprise release notes and upgrade guide [here](https://docs.corda.net/docs/corda-enterprise/release-notes-enterprise.html).

As a node operator, you should upgrade to the [latest released version of Corda](https://docs.corda.net/docs/corda-enterprise/index.html) if the fixed issue listed below is relevant to your work.

### Fixed issues

A recent JDK update has broken the way we used delegated signatures for TLS (Transport Layer Security) handshakes. We have fixed this issue through patches on all affected Corda Enterprise versions (4.2+) to allow users to upgrade to the latest versions of compatible JDK distributions. If you have not upgraded to one of the patched releases yet, do not upgrade to Java 8 version `8u252` or higher.

## Corda Enterprise 4.2

This release extends the [Corda Enterprise 4.1 release](https://docs.corda.net/docs/corda-enterprise/4.1/release-notes-enterprise.html)
with new mission critical enterprise capabilities to enhance support for HSM (hardware security module) signing devices and improved logging for profiling time spent
outside of Corda.

Corda Enterprise 4.2 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. Please refer to product documentation for details.

Corda Enterprise 4.2 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.1, 4.0 and 3.x, while providing enterprise-grade features and performance.

{{< note >}}
The compatibility and interoperability assurances apply to nodes running at the latest patch level for any given integer version.
For example, at the time of writing, the Corda Enterprise 4.2 interoperability and compatibility assurance is with respect to Corda 3.4, Corda Enterprise 3.3, Corda 4.1, Corda Enterprise 4.0 and Corda Enterprise 4.1.

{{< /note >}}

### Key new features and components


* **Further Hardware Security Module (HSM) support**>
This release adds full support for the Corda Firewall to hold all TLS 1.2 keys in an HSM, thus allowing the private keys which authenticate communication with peers to be
more fully protected. The `float` component of the Corda Firewall which receives inbound peer connections does not require any direct connection to an HSM from the DMZ.
Tooling is provided to support node TLS key generation on an HSM during the node registration process.This release adds support for storing the node’s CA and legal identity key in a [Securosys Primus X](https://www.securosys.ch/product/high-availability-high-performance-hardware-security-module) HSM. Please refer to the associated section of the [HSM support for legal identity keys](cryptoservice-configuration.md) page for more details.This release adds support for more secure storage of confidential identity keys using an HSM. With this feature, nodes can create and use confidential identity keys that are fully secured by an HSM, while not being subject to any capacity constraints of the HSM.
These keys can now be stored in the database in an encrypted form with the encryption key stored inside the HSM. Any operations using these keys (e.g. signing a transaction) can be forwarded to the associated HSM, so that this key material is not exposed to the node at all.
This is supported only for the Securosys Primus X HSM in this release. Please refer to the [Options for confidential identities](confidential-identities-hsm.md) page for more details.

* **Improved logging for HSM and vault operations**>
Previous logging coverage was not sufficient to allow users to tell apart the time spent by a CorDapp on internal Corda operations and the time spent outside of Corda (i.e. while performing a DB query or accessing
an HSM). Corda Enterprise 4.2 logs additional information in the detailed log file, information which can be used for profiling the duration of HSM and vault operations. The new logging lines follow a structured format that
is both human readable and easily parsable. Please refer to the **Logging** section of [Node administration](node-administration.md) page for more details.



### Further improvements, additions and changes


* Added Notary registration tool. See the [Notary Registration Tool](notary-reg-tool.md) page for more details.
* Previous log statements in the *details log* file have been reworked for better parsing support. See the [Node administration](node-administration.md) page for more details.
* This release includes improvements in access to the network CRL (Certificate Revocation List) servers from the Corda Firewall to simplify deployment.
In particular, the `float` component of the Corda Firewall can now be configured in new CRL checking modes that don’t initiate outbound links.
The `float` can now request that CRL checks be routed via the `bridge` component, or if local policy allows CRL checking of inbound peer connections can be turned off
(N.B. other certificate checks operate as normal and the message reply path via the `bridge` component will still require CRL checks).
Additionally, the `bridge` CRL requests will automatically use the same proxy path as the peer to peer messaging if a proxy is specified.
* Several improvements have been made to the AMQP reconnection state machine (used between peer nodes) to ensure more reliable operation under packet loss and repeated disconnection.
* Additional logging has been added to the Corda Firewall to enhance fault finding when there are connectivity and configuration issues.
* Added the checkpoint dumper tool. This tool outputs information about flows running on a node. This is useful for diagnosing the causes of stuck flows. Using the generated output,
corrective actions can be taken to resolve the issues flows are facing. Further information can be found in the [Checkpoint Tooling](checkpoint-tooling.md) page.


### Known issues

Please refer to same section in [Corda Enterprise 4](https://docs.corda.net/docs/corda-enterprise/4.0/release-notes-enterprise.html)


### Upgrade notes

As per previous major releases, we have provided a comprehensive upgrade notes ([Upgrading CorDapps to Corda Enterprise 4.2](app-upgrade-notes-enterprise.md)) to ease the upgrade
of CorDapps to Corda Enterprise 4.2. In line with our commitment to API stability, code level changes are fairly minimal.

For **developers**, switching CorDapps built using Corda (open source) 4.x to Corda Enterprise 4.2 is mostly effortless,
and simply requires making the Corda Enterprise binaries available to Gradle, and changing two variables in the build file:

```shell
ext.corda_release_version = '4.2'
ext.corda_release_distribution = 'com.r3.corda'
```

For **node operators**, it is advisable to follow the instructions outlined in [Upgrading a Corda Node](node-upgrade-notes.md).

{{< note >}}
If the finance CorDapp is being used in a mixed-distribution network, the open source finance contract CorDapp should be deployed on both Corda 4.x (open source) and Corda Enterprise 4.2 nodes.

{{< /note >}}
Visit the [https://www.r3.com/corda-enterprise](https://www.r3.com/corda-enterprise/) for more information about Corda Enterprise.
Customers that have purchased support can access it online at  [https://support.r3.com](https://support.r3.com/).
