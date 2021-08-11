---
aliases:
- /release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-release-notes
    parent: cenm-1-4-cenm-releases
    weight: 80
tags:
- release
- notes
title: Release notes
---


# Corda Enterprise Network Manager release notes

## Corda Enterprise Network Manager 1.4.1

CENM 1.4.1 introduces fixes to known issues in CENM 1.4.

### Enhancements

We have updated the default value of the optional `timeout` parameter, introduced in CENM 1.4, from 10000 ms to 30000 ms. This allows for better scalability of network map updates when a large number of nodes are registered on the network.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by CENM was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in CENM 1.2) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [PKI Tool](pki-tool.md) now generates certificates with serial number sizes of up to 16 octets/bytes.
* We have fixed an issue where the [PKI Tool](pki-tool.md) would throw an error when using [securosys HSM](https://www.securosys.com/) with multiple partitions.
* We have fixed an issue where the [signing request status command](cenm-cli-tool.md#check-the-connection-status-of-the-signing-service) in the [CENM Command-line Interface Tool](cenm-cli-tool.md) did not work for requests with `COMPLETED` status.
* We have fixed an issue where the `APP VERSION` column was not shown when running helm charts while bootstrapping CENM.

## Corda Enterprise Network Manager 1.4

CENM 1.4 introduces a range of new features and enhancements, including a [CENM error condition knowledge base](#cenm-error-condition-knowledge-base), a number of [Network Map Service performance enhancements](#network-map-service-performance-enhancements), a [new Signing Service plug-in functionality](#new-signing-service-plug-in-functionality-replaces-the-smr-signable-material-retriever-service) that replaces the SMR (Signable Material Retriever) Service, and [extended support for AWS native network deployment](#aws-native-network-deployment---reference-deployment-on-aws-eks-cloudhsm-postgresql) using [EKS](https://aws.amazon.com/eks/), [CloudHSM](https://aws.amazon.com/cloudhsm/), and [AWS PostgreSQL](https://aws.amazon.com/rds/postgresql/).

While this release is backward-compatible, you should consider upgrading to this release from earlier versions of the Corda Enterprise Network Manager.

{{< warning >}}

**Important upgrade notes**

Upgrading from CENM 1.3 to CENM 1.4 requires the following actions:

* Manual update of all existing Signing Service configurations.

  The SMR (Signable Material Retriever) Service, which prior to CENM 1.4 was used to handle plug-ins for signing data, [has been replaced](#new-signing-service-plug-in-functionality-replaces-the-smr-signable-material-retriever-service) by a plug-in loading logic inside the Signing Service. As a result, **all users must update their existing Signing Service configuration** when upgrading to CENM 1.4 - see the [CENM Upgrade Guide](upgrade-notes.md#manual-update-of-all-existing-signing-service-configurations) for details.

* Zone Service database migration.

  If you are upgrading to CENM 1.4 from CENM 1.3, you **must** set `runMigration = true` in the database configuration. See the [CENM Upgrade Guide](upgrade-notes.md#zone-service-database-migration) for details. This is required due to a [Zone Service database schema change](#network-map-service-performance-enhancements).

{{< /warning >}}

Read more about improvements of this release below.

### New features and enhancements

#### CENM error condition knowledge base

In CENM 1.4, we have adapted to CENM the internal Corda error handling logic introduced in [Corda 4.5](../../corda-os/4.5/error-codes.md) and [Corda Enterprise 4.5](../../corda-enterprise/4.5/node/operating/error-codes.md) for Corda nodes.

As a result, CENM exceptions are now treated as CENM error codes and an error code is generated for each exception. The initial set of error codes, related to configuration parsing/validation errors, are described in the new [CENM error codes documentation page](cenm-error-codes.md). This is the start of a growing CENM error condition knowledge base, which will expand in future releases.

#### Network Map Service performance enhancements

CENM 1.4 introduces performance improvements in the Network Map Service to ensure stable operations with a large amount of active participants in a network.

Performance and reliability improvements can be observed on the unsigned Network Map nodes' response, due to the serialization of fewer fields during the database information retrieval. This speeds up the response generation and avoids potential deadlocks, which could happen in previous CENM versions when more than one unsigned network map node calls were executed simultaneously.

Performance is enhanced through the following combination of changes:

* A new, optional `timeout` parameter now enables you to set specific [Signing Service timeouts](signing-service.md#signing-service-configuration-parameters) for communication to each of the services used within the signing processes defined in the network map, in a way that allows high node count network maps to get signed and to operate at reliable performance levels. You can also use the `timeout` parameter to set specific Network Map Service timeouts for communication to the [Identity Manager and Revocation services](network-map.md#identity-manager--revocation-communication). The `timeout` parameter's values are stored in a new `timeout` column in the [Zone Service](zone-service.md#signing-services-configuration)'s database tables `socket_config` and `signer_config` (refer to the [CENM Upgrade Guide](upgrade-notes.md#zone-service-database-migration) for important details about migrating the Zone Service database from CENM 1.3).

* A [new API endpoint](network-map-overview.md#http-network-map-protocol), `GET network-map/node-infos`, enables you to retrieve a list of all signed `NodeInfo` objects for _all_ the nodes in the network at once.

* The following [new headers](network-map-overview.md#http-network-map-protocol) for Network Map API responses now make headers more closely aligned with HTTP standards:
  * The new header `X-Corda-Server-Version` has been added for all Network Map API responses (except for internal error responses with code 5xx) indicates the version of the Network Map and the available calls. It has a default value of `2`.
  * The new header `X-Corda-Platform-Version` replaces `Platform-version`. The old header name continues to be supported.
  * The new header `X-Corda-Client-Version` replaces `Client-version`. The old header name continues to be supported.

#### New Signing Service plug-in functionality replaces the SMR (Signable Material Retriever) Service

The SMR (Signable Material Retriever) Service was introduced in CENM 1.2 with the purpose of handling plug-ins for signing data. In CENM 1.4 we have replaced it with a plug-in loading logic as part of the Signing Service by fetching the signable data from the Identity Manager Service and the Network Map Service and sending it to either the new plug-in (if specified) or to the default Signing Service processing logic.

As a result we have removed the SMR Service completely, thus reducing the number of CENM services and eliminating the need to maintain RPC servers and storage previously created by the default SMR plug-in.

A range of new functionality and changes, introduced to that effect, are described below. See the [Signing Service](signing-service.md) documentation for full details.

**Configuration changes**

* The new `serviceLocation` property replaces `serviceLocationAlias`.

  The Signing Service configuration has been changed so that each signing task must now take in a `serviceLocation` property instead of a `serviceLocationAlias`.
  Multiple locations (one for each sub-zone) can be defined for non-CA signing tasks (Network Map, Network Parameters) using the new property.
  The `serviceLocationAlias` property cannot be used in CENM 1.4 (if used it will cause a configuration parsing error).

* Option to configure plug-in based or default signing.

  Each signing task has a new property called `plugin`, which consists of `pluginJar` and `pluginClass`. If the `plugin` property is set, the Signing Service will use the plug-in to sign data; if not set, the Signing Service will use the default signing mechanism. If the `plugin` property is used, `signingKeyAlias` must not be present because the default Signing Service keys will not be used. The `plugin` property must be the same for signing tasks of the same type - CA (CSR or CRL) or non-CA (Network Map or Network Parameters); however, plug-in based and default signing can be mixed - for example, you can use plug-in based signing for CA Signing Services (CSR/CRL), and default signing for non-CA Signing Services (Network Map / Network Parameters). If both CA and non-CA signing tasks use plug-ins, the `signingKeys` property must not be set.

**Asynchronous signing**

Asynchronous signing is a new feature inside the plug-in API, which allows to delay signing when the Signing Service plug-in is used: when a signing request is sent to the plug-in, it might not be signed immediately and in that case it will return a `PENDING` status.

How it works:
1. The Signing Service polls for status changes of the signing request. If the status returned from the plug-in is `PENDING`, the Signing Service keeps polling. There is no maximum set timeout for a request status change to be returned - the Signing Service keeps polling until the status becomes either `COMPLETED` or `FAILED`.
2. If the returned status is `FAILED`, the request is not persisted.
3. If the status is `COMPLETED`, the request is marked as done and it is persisted to the respective CENM services (Identity Manager Service or Network Map Service).

The following changes have been made as a result of the introduction of asynchronous signing:

* API changes. To allow the Signing Service to query the signing status from the plug-in, new functions have been added for CA and non-CA plug-ins. In addition, all response classes now contain an optional `requestId` that is filled in by the plug-in - if the status is returned as `PENDING` but no `requestId` (tracking id) is provided, the signing will stop and the request will be discarded.
* Shell signing. If the signing is done via Shell, the asynchronous tracking ids and statuses are printed to the console. In addition, new Shell menu items have been added for each signing task, which allow you to track the Asynchronous Signing request status.
* RPC function changes. To enable the complex task of returning Asynchronous Signing tracking ids and statuses when the signing is done via RPC, a number of changes have been made to RPC functions, including changes to requests and the addition of four new RPC requests used to query the status of each request via RPC. See the [Signing Service](signing-service.md) documentation for more information.

**Code changes**

* Common signers. We have the `common` module, making signer classes abstract and adding two implementation for each signer - one for the default logic and another one for the plug-in logic.
* `SigningServicePluginLoader`. This class is used to load the defined plug-ins from the configuration. It uses a Java `URLClassLoader` and a parent `ClassLoader` that can be provided as a constructor argument.

**Example CA plug-in**

CENM 1.4 ships with an example CA plug-in, which equips users with everything they need to know when creating their own plug-in. See the [Signing Service](signing-service.md) documentation for more information.


#### AWS native network deployment - reference deployment on AWS EKS, CloudHSM, PostgreSQL

We are expanding our support to AWS native network deployment by supporting EKS in our Kubernetes & Helm reference deployment, using.:
* [EKS](https://aws.amazon.com/eks/).
* [CloudHSM](https://aws.amazon.com/cloudhsm/).
* [AWS PostgreSQL](https://aws.amazon.com/rds/postgresql/).

Supported deployment scenarios in CENM 1.4:
* AWS with external PostgreSQL.
* Azure with PostgreSQL deployed in cluster.
* Azure with external PostgreSQL.

Not supported in CENM 1.4:
* AWS with PostgreSQL deployed in cluster.

See the [CENM deployment](aws-deployment-guide.md/) section for more information.

#### Other changes
* We have added support for PostgreSQL 10.10 and 11.5 (JDBC 42.2.8), as noted in [CENM Databases](database-set-up.md#supported-databases) and [CENM support matrix](cenm-support-matrix.md#cenm-databases).
* A `non-ca-plugin.jar` has been added to `signing-service-plugins` in Artifactory.
* We have renamed the FARM Service, introduced in CENM 1.3, to [Gateway Service](gateway-service.md). As a result, if you are [upgrading](upgrade-notes.md) from CENM 1.3 to CENM 1.4, the FARM Service `.jar` file used in CENM 1.3 should be replaced with the Gateway Service `.jar` file used in CENM 1.4.
* In CENM 1.4 we have changed the way `subZoneID` is set in Signing Service configurations - see the [CENM upgrade guide](upgrade-notes.md#change-in-setting-subzoneid-in-signing-service-configurations) for more details.

### Fixed issues

* We have fixed an issue where the [Auth service](auth-service.md) could not start during database schema initialisation for PostgreSQL.
* We have fixed an issue where the Signing Service failed to start, following setup without the SMR (Signable Material Retriever) Service, producing a `serviceLocations` configuration error. Note that the SMR Service has been removed in CENM 1.4 and its functionality has been merged with the Signing Service - see the [New features and enhancements](#new-features-and-enhancements) section above for more details.
* We have fixed an issue where the `azure-keyvault-with-deps.jar` and `out.pkcs12` files were not copied to the `pki-pod` and PKI generation failed as a result.
* We have fixed an issue where HSM passwords were not hidden in service logs.
* We have fixed an issue where the Zone Service removed the `mode` field from the Signing Service's configuration with Utimaco and then failed to return this field to the Angel Service.
* Commands for the Identity Manager Service and the Network Map Service, which previously returned no information, now indicate when no data is available.
* We have fixed an issue where [Gateway Service](gateway-service.md) (previously called FARM Service in CENM 1.2) logs were not available in the `logs-farm` container.
* We have fixed an issue where submitting a CRR request with CENM Command-line Interface Tool failed with the unexpected error `method parameters invalid`.
* When using the Signing Service to manually perform signing tasks with multiple accounts for each task and the option to authenticate `ALL` users is selected, the Signing Service now indicates which user should enter their password.
with multiple accounts for each task The Signing Service now prompts a specific user to login in while all are being authenticated.
* The `context current` command now shows the current active user and the current URL.

### Known issues

* Cloud deployment of CENM 1.4 on Azure or AWS will not work on the same cluster if CENM 1.2 or 1.3 is already running on that cluster (and vice versa). This is due to a conflict in the naming of some Kubernetes components used in both deployments, which currently prevents versions 1.2/1.3 and 1.4 from running on the same cluster.
* The Command-line Interface Tool `request status` command does not work for completed requests.
* When there are incorrect `signer-ca` settings or a `ca-plugin` has stopped, an exception appears instead of a description of the issue.
* There are currently two different logs that services write error codes to (`DUMP` and `OPS`), with some services writing to both.
* Error codes are not yet thrown consistently in logs or console across all services.
* When multiple CRR requests are submitted, the certificates are not updated correctly from `VALID` to `REVOKED`. This issue does not affect the CRL.
* When creating an AWS Postgres database, users are unable to connect to the database when they have selected the Virtual Private Cloud (VPC) of their Elastic Kubernetes Service (EKS) Cluster. However, they are able to connect when they have selected the default VPC.

## Corda Enterprise Network Manager 1.3.2

CENM 1.3.2 introduces fixes to known issues in CENM 1.3.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by CENM was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in CENM 1.2) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [PKI Tool](pki-tool.md) now generates certificates with serial number sizes of up to 16 octets/bytes.
* We have fixed an issue where the [PKI Tool](pki-tool.md) would throw an error when using [securosys HSM](https://www.securosys.com/) with multiple partitions.

## Corda Enterprise Network Manager 1.3.1

CENM 1.3.1 introduces fixes to known issues in CENM 1.3.

### Fixed issues

* Fixed an issue where an error occurred when generating the PKI data for Kubernetes as the `out.pkcs12` file could not be found in the `/opt/cenm/HSM` directory of the Kubernetes pod for PKI.
* Fixed an issue where HSM passwords were not hidden in CENM Services' logs.
* Fixed an issue where the Zone Service accidentally removed the `mode` field from the Signing Service's configuration with Utimaco, and failed to return it to the Angel Service.
* Fixed an issue where `keyPassword` was not hidden in log files for each CENNM Service with a configuration file.
* Fixed an issue with an unclear error message for unhandled exceptions.

## Corda Enterprise Network Manager 1.3

CENM 1.3 introduces a new Command-Line Interface (CLI) tool for network operators to manage CENM services. This functionality ships with new services that enable you to manage CENM configurations (the new Zone Service), to create new users and roles (the new User Admin tool), and to authenticate and authorise users (the new Auth Service). The Auth Service supports full Role-Based Access Control (RBAC) and provides a web-based management interface for system administrators to create and manage user groups and entitlements.

While this release is backward-compatible, you should consider upgrading to this release from CENM 1.2 (or earlier) as this is a major upgrade with the introduction of several new services.

Read more about improvements of this release below.

### New features and enhancements

#### New Command-Line Interface (CLI) tool
 The new CENM Command-Line Interface (CLI) tool is supported by the new authentication and authorisation (Auth) service and enables users to access many of the functionalities included in this release, such as central log retrieval, configuration management, and multi-step service orchestration. Users are now able to authenticate through the new CLI tool and to perform actions according to their user-permissions (for example, run a Flag Day), thus eliminating the need to access the host of each individual service and its respective shell.
#### New User Admin tool
The User Admin tool that allows CENM administrators to connect securely via a web browser to create and manage new CENM users, groups, and roles for performing tasks on CENM services. The application supports the new authentication and authorisation (Auth) - which is used to check the credentials and permissions of each user.

#### New Auth Service for user authentication and authorisation
CENM 1.3 introduces a new authentication and authorisation service, allowing Network operators to manage users, groups and roles (along with fine grain permissions associated with roles) through a new management interface provided alongside. This service will first be used by internal services and via a new Command Line Tool and will allow authentication and enforcement of entitlements across all network operations.

#### New Zone Service for configuration management
The new Zone Service enables you to store configurations for the Identity Manager Service, the Network Map Service, and the Signing Service. The configuration composition capability allows you to use your updates to individual service configurations to trigger automatic updates to other services as needed.

#### Improvements to Kubernetes reference deployment
We have updated the Kubernetes reference deployment to use Helm@3 and to support the new services introduced in CENM 1.3. The updated documentation provides guidance on how to use this deployment with external databases.

#### Configuration obfuscation
Configuration obfuscation support in CENM 1.3 now involves the use of the [Corda Enterprise Configuration Obfuscator tool](https://docs.corda.net/docs/corda-enterprise/tools-config-obfuscator.html). Legacy (pre-1.3) obfuscated configurations are still supported, however you should update any such configuration files using the latest version of the Corda Enterprise Configuration Obfuscator tool.

#### Highly available Certificate Revocation List
Our documentation now provides some deployment recommendations on how to make the CRL highly available in a typical network deployment.

#### Other changes
- We have added the new Angel Service to enable the management of the Identity Manager Service, the Network Map Service, and other services. This feature includes a standardised health check API, functionality for fetching configuration from the Zone Service, and capability to enable remote access to service logs to assist with diagnosing issues.
- We have added the new Front-end Application for Remote Management (FARM) Service that acts as a gateway to enable the orchestration of requests from user interfaces (command-line interface or web UI) to back-end services.
- We have added support for managing the Flag Day process via the command-line interface, replacing the need for the network operator to directly log in to the Network Map and Signing Services. However, note that in the recommended deployment, the signing of parameters is done via systems in a restricted access network, and therefore network operators still need to access the Signing Service from within that restricted network.
- We have added support for labelling of Sub Zones (Network Map Services) in order to give them a human-readable identifier.
- We have removed the `NotaryRegistrationTool`, which had been shipped as part of the Notary tools for several versions before.
- We have updated the Corda base used in CENM from version 4.0 to version 4.3. This does not affect compatibility, but it updates a number of shared dependencies.
- We have updated the Bouncy Castle library from version 1.60 to version 1.64.

### Fixed issues
- Fixed an issue where an unhandled exception was thrown when attempting incompatible service database schema changes.
- Added missing parameters in the documentation example for the CENM PostgreSQL setup, which resulted in service database misconfigurations.
- Fixed an issue where SMR RPC calls could sometimes cause undefined behaviour due to multiple threads operating on data.
- Fixed an issue where attempts to parse the Identity Manager Service configuration as text would sometimes result in a parsing error.
- Fixed an issue where an attempt to authenticate all accounts when signing a network map via the Signing Service CLI resulted in an unexpected error.
- Fixed an issue where selecting an invalid account index when signing a network map via the Signing Service CLI caused the Signing Service to authenticate all accounts.
- Fixed an issue where the Signing Service CLI authentication interface was inconsistent between accounts.
- Fixed an issue with a missing entry in the `workflow_csr` table after registering a service identity using `corda_tools_notary_registration.jar`.

### Known issues

- The Signable Material Retriever does not support configuration via the Angel Service, and must be configured using the old process used for CENM 1.2.
- The bootstrap deployment script does not set up an Angel Service for the Signing Service, and any changes to the configuration must be made using the old process used for CENM 1.2 (in this scenario only). The Signing Service does support the Angel Service, and can be configured via the Zone Service if managed by an Angel Service.
- The `netmap netparams` update status CLI command renders raw `JSON` only.

## Corda Enterprise Network Manager 1.2.3

CENM 1.2.3 introduces fixes to known issues in CENM 1.2.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by CENM was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in CENM 1.2) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [PKI Tool](pki-tool.md) now generates certificates with serial number sizes of up to 16 octets/bytes.
* We have fixed an issue where the [PKI Tool](pki-tool.md) would throw an error when using [securosys HSM](https://www.securosys.com/) with multiple partitions.

## Corda Enterprise Network Manager 1.2.2

CENM 1.2.2 introduces fixes to known issues in CENM 1.2.

### Fixed issues

* Using `csr_token` as part of a node registration causes the registration to fail when the Identity Manager is set up to use a supported version of Oracle DB.
* Creating and signing the CRL fails when upgrading from CENM 0.4 if the existing revoked certificates lacked a revocation reason.

## Corda Enterprise Network Manager 1.2

### Major Features

**Support for Docker and Kubernetes**
We are expanding our support for Docker to Corda Enterprise Network Manager.

Furthermore, we are introducing a first reference deployment with Helm and Kubernetes.
Out of the box - you will be able to deploy in minutes an ephemeral representative test network to complement your development cycle.

See [Kubernetes deployment documentation](deployment-kubernetes.md) for more details.

**Support for third party CAs**

To satisfy clients who wish to use third party software or service providers to handle the supported lifecycle of certificates and network services signing events in a Corda network, the Signing Service has been separated into Signable Material Retriever Service (SMR) and CENM Signing Service in order to offer a pluggable interface.

The new service (SMR) extracts signable material from the Identity Manager and Network Map services, and then delegates signing to a plug-in. Customers can implement their own plug-ins to integrate with external signing infrastructure and return signed material back to SMR to pass to the relevant CENM service.

See [Signing Services](signing-service.md) for more details. Also see [EJBCA Sample plug-in](ejbca-plugin.md) for a sample open source CA implementation.

**CRL Endpoint Check tool**

As a diagnostic aid in case of problems with TLS connections, CENM 1.2 introduces a CRL Endpoint Check tool.
This stand alone tool checks CRL endpoint health of all certificates in a provided keystore, as a simpler
alternative to manually extracting CRL endpoints individually from the certificate and then verifying them.

See [CRL Endpoint Check Tool](crl-endpoint-check-tool.md) for usage and further details.


### Minor Features

**Assisted Node Registration**

We introduced a new field in both Corda and Network Manager that can be used to enable a variety of onboarding workflows that might start prior to and continue after the Certificate Signing Request of the Node. In doing so, a Network Operator can embed the node registration process as part of a larger onboarding workflow or simply speed up/automate the process of reviewing a CSR and issuing a certificate. This feature requires nodes on Corda or Corda Enterprise 4.4 or above.

See identity.manager for more information on how to make use of this feature.

**Bundled Service**

While deploying services individually makes sense for production deployments at scale, for smaller deployments or testing purposes we introduce possibility of running multiple services in parallel from one Jar file. We call it Bundled Service. Users need to specify which services to run and the corresponding configuration files.
It is possible to have service deduction from the configuration file which makes this feature backwards compatible
with CENM 1.1.

**Notary Whitelist**

For high availability (HA) notaries only, the network map will now fetch the node info automatically from the
Identity Manager, rather than requiring that the files are copied in manually. Support for non-HA notaries
is not anticipated, customers are encouraged to deploy all notaries in a high availability configuration.


### Other Improvements


* We have expanded our HSM supported list to include AWS Cloud HSM
* Default log file paths now include the name of the service (i.e. “network-map”) that generates them,
so if multiple services run from the same folder, their dump log filenames do not collide.
* Shell interface (Signing Service and Identity Manager) no longer provide Java scripting permissions.
* Remove private network maps - this functionality was never completed, and the changes should not be user visible. This
does not yet remove them from the database schema, which will be in a future release. Related quarantined and staging
node info tables are not used as of CENM 1.1.
* Improve logging of database errors, so that the underlying cause is reported rather than only that a failure occurred.
* Dump logs are now written into service specific folders, so that if multiple services run from the same directory,
the logs files do not conflict.
* Correct service healthcheck command when executed from the CRaSH shell.
* Add new command to Network Map shell to view list of nodes that have accepted (or haven’t) a given parameters update
(“view nodesAcceptedParametersUpdate accepted: <true/false>, parametersHash: <parameters update hash value>”),
which can help to monitor the procedure of [Updating the network parameters](updating-network-parameters.md).
* Add working directory argument for CENM services, which is a path prefix for config and certificate files.
* Add `run networkParametersRegistration`, `run flagDay` and `run cancelUpdate` commands to the Network Map
service shell, to enable running flag days without restarting the service. See [Updating the network parameters](updating-network-parameters.md) for
full details.
* Add `view publicNetworkNodeInfos` command to Network Map service shell, to see all public network participants’ node
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


* Shell interface (Signing Service and Identity Manager) no longer allow access to commands which allow scripting

of Java.


### Known Issues


* Identity Manager’s WorkflowPlugin keeps trying to create new request in an external system,
until the request is REJECTED or APPROVED. This means the external system needs to internally record which requests
are currently being processed and reject surplus creation attempts. The Identity Manager records this in logs
as warning: “There is already a ticket: ‘<TICKET ID>’ corresponding to *Request ID* = <VALUE>, not creating a new one.”


## Corda Enterprise Network Manager 1.1

The R3 Network Services team is excited to announce the release of CENM 1.1,
introducing support for a number of additional HSMs as well as adding support for Oracle DB.
For deployments of pre-1.0 CENM a migration tool has been added to rewrite legacy
configurations to be compatible with 1.1.


### Major New Features

**Oracle Database Support**

Support has been added for Oracle DB versions 12cR2 and 11gR2 as a backend data store.
For full setup instructions see [CENM Databases](database-set-up.md).

**Configuration Migration Tool**

To simplify the upgrade process from early versions of CENM a configuration migration tool has been
added. This is intended to upgrade v0.2.2 / v0.3+ configurations to v1.1, including both restructuring
changes to the configuration file and updating the value of fields (such as database driver class).
See [Config migration tool](tool-config-migration.md) for details on this tool.

**Hardware Security Module Support**

Support for HSMs has been significantly extended, and as part of this work the HSM Jar files are
now dynamically loaded and should be provided by the user. Support has been added for Azure Key Vault,
as well as for Gemalto and Securosys HSMs in both the PKI Tool and Signing Service.


### Other Improvements


* CENM now supports encryption of passwords in configuration files, using encryption keys derived from
hardware attributes. An obfuscation tool ships with CENM, to process configuration files and encrypt
marked fields. For more details on usage see [Config Obfuscation Tool](../../corda-enterprise/4.6/tools-config-obfuscator.md/).
* Fixed an internal error which occurred when using H2 versions below 1.4.198 due to use of unsupported
lock types.
* Added `run purgeAllStagedNodeInfos` and `run purgeStagedNodeInfo nodeInfoHash: <node_info_hash>` commands
to the Network Map interactive shell, allowing for the moving of nodes out of the staging table and into the
main node info table of the Network Map. This provides a solution to the scenario whereby a node gets stuck
in the staging table (see *Troubleshooting Common Issues* section).
* Simplified configuration by removing configuration options for private network maps. This feature is being
removed in preference of using subzones, and therefore these configuration options merely add complexity.


### Known Issues


* The PKI tool fails if the password for a key store and key are different. This only applies to local key
stores. Please ensure key passwords match the key store password to avoid this issue.
* Logging in case of Gemalto HSM call failures is limited, which complicates diagnosis. This is to be improved in a future version.
* Config migration tool displays configuration output version as 1.0, actual target
is 1.1.
* Config migration tool does not generate a `shell` configuration section, and therefore the generated configurations may not be usable as-is.
This is intentional in order as the operator needs to make decisions on this configuration, for example password.
* PKI tool reports “Error whilst attempt to read config lines.” if it cannot find a configuration file, rather than a more specific error message.


## Corda Enterprise Network Manager 1.0

R3 and The Network Services team are proud to deliver the inaugural release of the Corda Enterprise
Network Manager version 1.0. The CENM can be used to operate a bespoke Corda network when the requirement
for an entity to be in complete control of the consensus rules, identity, and deployment topology exists.

This is the same software used to operate the global Corda Network on behalf of the Corda
Network Foundation since its launch in 2018.

Please note, whilst this is the first public release of the Corda Enterprise Network Manager, these
release notes and any associated documentation should be read from the perspective of those coming
fresh to the product but also those who are upgrading from pre-release versions.


### Major New Features

**The Signing Service**

The Signing Service is a new addition to the suite of CENM services, sitting alongside the Identity Manager and Network
Map. It provides a network operator with full control over the signing of node identity data (CSRs and CRRs) and global
network data (Network Map and Network Parameters) and includes features such as HSM integration, signing scheduling and
support for multiple Network Map services. See [Signing Services](signing-service.md) to learn more about this service.

**Brand new PKI tooling**

The PKI Tool enables a network operator to easily generate Corda-compliant certificate hierarchy (keys and
certificates) as well as certificate revocation lists. The tool supports both local and HSM key stores and can be
customized with the configuration file. See [Public Key Infrastructure (PKI) Tool](pki-tool.md) to learn about all the features of the PKI Tool.

**Full End to End SSL communication**

All CENM components now communicate over SSL with one another, this completes the removal of the “database as message
queue” of older versions. See [Configuring the CENM services to use SSL](enm-with-ssl.md) for more information.

**Security And Performance Fixes**


### Minor Features

**Postgresql Support**

As well as SQLServer, the CENM suite now supports postgresql as a backend data store.

**Protocol Separation**

In pre release versions of CENM the user information REST endpoints shared a namespace with the core
Corda Network Map protocol. This was done to better draw distinction between the protocol itself as
required by Corda nodes, and the more free-form functionality offered to users. This will allow for future
versioned changes to the protocol without changing that which the Corda nodes depend upon.


### Major New Features


* `/network-map`
* `/network-map-user`

The Signing Service is a new addition to the suite of CENM services, sitting alongside the Identity Manager and Network
Map. It provides a network operator with full control over the signing of node identity data (CSRs and CRRs) and global
network data (Network Map and Network Parameters) and includes features such as HSM integration, signing scheduling and
support for multiple Network Map services. See [Signing Services](signing-service.md) to learn more about this service.

**Epoch Control**

The PKI Tool enables a network operator to easily generate Corda-compliant certificate hierarchy (keys and
certificates) as well as certificate revocation lists. The tool supports both local and HSM key stores and can be
customized with the configuration file. See [Public Key Infrastructure (PKI) Tool](pki-tool.md) to learn about all the features of the PKI Tool.

**Shell**

Migrated the private network management utility tool into the Network Map interactive shell. The new command within the
shell is an interactive command, allowing a user to run the same management tools without having to worry about passing
in a configuration file or remembering the correct start up flag.

**Config Debugability**

Added multi-phase parsing of config files. Parsing and validation errors are now batched before being presented to
the user, eliminating the frustration from having to address errors one by one.

**Security And Performance Fixes**


### Minor Features

**Postgresql Support**

Due to the database schema separation outlined below, the 0.3 release now supports segregated sub zones. That is,
sub-zones of nodes that operate in what appear to the nodes to be isolated networks, with their own notary(ies) and
network parameters. Critically, however, their certificate governance remains under the jurisdiction of a global
Doorman. This way, temporary benefits such as higher privacy, differential network parameters upgrade schedules or use
of temporary private notaries can be delivered. Note that the ability to merge one sub-zone into another is not
currently supported. See the [Sub Zones](sub-zones.md) documentation for more information.

**Protocol Separation**

In pre release versions of CENM the user information REST endpoints shared a namespace with the core
Corda Network Map protocol. This was done to better draw distinction between the protocol itself as
required by Corda nodes, and the more free-form functionality offered to users. This will allow for future
versioned changes to the protocol without changing that which the Corda nodes depend upon.

The two top-level endpoints are now


* `/network-map`
* `/network-map-user`

see [Network Map Overview](network-map-overview.md) for more information.

Another change that is introduced in the newest release is the ability to interact with the Doorman and Network Map
services via a shell. The commands available currently mainly allow an operator to inspect the state of the service,
for example by viewing the current set of nodes within the public network, or viewing the list of Certificate Signing
Requests that are awaiting approval. See the [Embedded Shell](shell.md) documentation for more information.

Added support for overriding the default “increment previous value by 1” behaviour for epoch values during network
parameter updates/initialisation. This allows a user to specify the epoch within the parameter config file and it
facilitates arbitrary jumps in epoch values. This is necessary for the day-to-day management of multiple sub-zones as
well as the merging of one sub-zone into another.

**Shell**

Migrated the private network management utility tool into the Network Map interactive shell. The new command within the
shell is an interactive command, allowing a user to run the same management tools without having to worry about passing
in a configuration file or remembering the correct start up flag.

**Config Debugability**

Added multi-phase parsing of config files. Parsing and validation errors are now batched before being presented to
the user, eliminating the frustration from having to address errors one by one.

The service-based architecture requires tooling around service state monitoring. Currently (i.e. with the 0.3 release),
there is no dedicated utility that would address that issue. As for now, the network operator needs to rely only on service logs and manual service endpoint pinging in order to
assess in what state the service is.


* Identity Manager: `http://<<IDENTITY_MANAGER_ADDRESS>>/status`
* Network Map: `http://<<NETWORK_MAP_SERVICE_ADDRESS>>/network-map/my-hostname`
* Revocation Service (currently part of the Identity Manager): `http://<<REVOCATION_SERVICE_ADDRESS>>/status`
