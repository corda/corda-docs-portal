---
aliases:
- /releases/release-1.2/release-notes.html
- /docs/cenm/head/release-notes.html
- /docs/cenm/release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-release-notes
    parent: cenm-1-2-cenm-releases
    weight: 80
tags:
- release
- notes
title: Release notes
---

# Release notes

## Corda Enterprise Network Manager 1.2.6

CENM 1.2.6 fixes an urgent security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Fixed issues

* The Log4j dependency has been updated to version 2.17.1 to fix pre-existing Log4j issues.

## Corda Enterprise Network Manager 1.2.5

{{< note >}}

This is a direct upgrade from 1.2.3. No version 1.2.4 or 1.2.3 was released.

{{< /note >}}

CENM 1.2.5 fixes an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version 2.16.0.

To get started with this upgrade, request the download link by raising a ticket with [support](https://r3-cev.atlassian.net/servicedesk/customer/portal/2).

{{< warning >}}
Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.
{{< /warning >}}

### Fixed issues

We have updated the Log4j dependency to version 2.16.0 to mitigate CVE-2021-44228.

## Corda Enterprise Network Manager 1.2.3

CENM 1.2.3 introduces fixes to known issues in CENM 1.2.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by CENM was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in CENM 1.2) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [PKI Tool]({{< relref "pki-tool.md" >}}) now generates certificates with serial number sizes of up to 16 octets/bytes.
* We have fixed an issue where the [PKI Tool]({{< relref "pki-tool.md" >}}) would throw an error when using [securosys HSM](https://www.securosys.com/) with multiple partitions.

## Corda Enterprise Network Manager 1.2.2

CENM 1.2.2 introduces fixes to known issues in CENM 1.2.

### Fixed issues

* Using `csr_token` as part of a node registration causes the registration to fail when the Identity Manager is set up to use a supported version of Oracle DB.
* Creating and signing the CRL fails when upgrading from CENM 0.4 if the existing revoked certificates lacked a revocation reason.

## Corda Enterprise Network Manager 1.2

### Major New Features

**Support for Docker and Kubernetes**
We are expanding our support for Docker to Corda Enterprise Network Manager.

Furthermore, we are introducing a first reference deployment with Helm and Kubernetes.
Out of the box - you will be able to deploy in minutes an ephemeral representative test network to complement your development cycle.

See [Kubernetes deployment documentation]({{< relref "deployment-kubernetes.md" >}}) for more details.

**Support for third party CAs**

To satisfy clients who wish to use third party software or service providers to handle the supported lifecycle of certificates and network services signing events in a Corda network, the Signing Service has been separated into Signable Material Retriever Service (SMR) and CENM Signing Service in order to offer a pluggable interface.

The new service (SMR) extracts signable material from the Identity Manager and Network Map Services, and then delegates signing to a plugin. Customers can implement their own plugins to integrate with external signing infrastructure and return signed material back to SMR to pass to the relevant CENM service.

See [Signing services]({{< relref "signing-service.md" >}}) for more details. Also see [EJBCA sample plugin]({{< relref "ejbca-plugin.md" >}}) for a sample open source CA implementation.

**CRL Endpoint Check tool**

As a diagnostic aid in case of problems with TLS connections, CENM 1.2 introduces a CRL Endpoint Check tool.
This stand alone tool checks CRL endpoint health of all certificates in a provided keystore, as a simpler
alternative to manually extracting CRL endpoints individually from the certificate and then verifying them.

See [CRL Endpoint Check Tool]({{< relref "crl-endpoint-check-tool.md" >}}) for usage and further details.

### Minor Features

**Assisted Node Registration**

We introduced a new field in both Corda and Network Manager that can be used to enable a variety of onboarding workflows that might start prior to and continue after the Certificate Signing Request of the Node. In doing so, a Network Operator can embed the node registration process as part of a larger onboarding workflow or simply speed up/automate the process of reviewing a CSR and issuing a certificate. This feature requires nodes on Corda or Corda Enterprise Edition 4.4 or above.

See identity.manager for more information on how to make use of this feature.

**Bundled Service**

While deploying services individually makes sense for production deployments at scale, for smaller deployments or testing purposes we introduce possibility of running multiple services in parallel from one Jar file. We call it Bundled Service. Users need to specify which services to run and the corresponding configuration files.
It is possible to have service deduction from the configuration file which makes this feature backwards compatible
with CENM 1.1.

**Notary Whitelist**

For high availability (HA) notaries only, the network map will now fetch the node info automatically from the
identity manager, rather than requiring that the files are copied in manually. Support for non-HA notaries
is not anticipated, customers are encouraged to deploy all notaries in a high availability configuration.

### Other Improvements

* We have expanded our HSM supported list to include AWS Cloud HSM
* Default log file paths now include the name of the service (i.e. “network-map”) that generates them,
so if multiple services run from the same folder, their dump log filenames do not collide.
* Shell interface (Signer and Identity Manager Services) no longer provide Java scripting permissions.
* Remove private network maps - this functionality was never completed, and the changes should not be user visible. This
does not yet remove them from the database schema, which will be in a future release. Related quarantined and staging
node info tables are not used as of CENM 1.1.
* Improve logging of database errors, so that the underlying cause is reported rather than only that a failure occurred.
* Dump logs are now written into service specific folders, so that if multiple services run from the same directory,
the logs files do not conflict.
* Correct service healthcheck command when executed from the CRaSH shell.
* Add new command to Network Map shell to view list of nodes that have accepted (or haven’t) a given parameters update
(“view nodesAcceptedParametersUpdate accepted: <true/false>, parametersHash: <parameters update hash value>”),
which can help to monitor the procedure of [Updating the network parameters]({{< relref "updating-network-parameters.md" >}}).
* Add working directory argument for CENM services, which is a path prefix for config and certificate files.
* Add `run networkParametersRegistration`, `run flagDay` and `run cancelUpdate` commands to the Network Map
service shell, to enable running flag days without restarting the service. See [Updating the network parameters]({{< relref "updating-network-parameters.md" >}}) for
full details.
* Add `view publicNetworkNodeInfos` command to Network Map Service shell, to see all public network participants’ node
infos, including its’ platform version.
* Bug fix: Certificate name rules are now enforced during issuance in accordance with Corda network rules,
previously it was possible to register nodes with names which the node cannot use.
* Registration Web Service (CSR and CRL) was returning incorrect HTTP Error Code 500 instead of 400
for requests with invalid client version or platform version.
* Improved logs created by Registration Web Service - request validation exceptions (e.g. invalid character in a subject name,
invalid platform version) are now logged with WARN level instead of ERROR level.
* Bug fix: The configuration option ‘database.initialiseSchema’, which was used for H2 database only, is now deprecated,
use ‘database.runMigration’ instead.

### Security Improvements

* Shell interface (Signer and Identity Manager Services) no longer allow access to commands which allow scripting
of Java.

### Known Issues

* Identity Manager’s WorkflowPlugin keeps trying to create new request in an external system,
until the request is REJECTED or APPROVED. This means the external system needs to internally record which requests
are currently being processed and reject surplus creation attempts. The Identity Manager Service records this in logs
as warning: “There is already a ticket: ‘<TICKET ID>’ corresponding to *Request ID* = <VALUE>, not creating a new one.”
