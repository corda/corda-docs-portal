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

## Corda Enterprise Network Manager 1.4.4

CENM 1.4.4 fixes an urgent security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Fixed issues

* The Log4j dependency has been updated to version 2.17.1 to fix pre-existing Log4j issues.

## Corda Enterprise Network Manager 1.4.3

{{< note >}}

This is a direct upgrade from 1.4.1. No version 1.4.2 was released.

{{< /note >}}

CENM 1.4.3 fixes an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version 2.16.0.

{{< warning >}}
Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.
{{< /warning >}}

### Fixed issues

We have updated the Log4j dependency to version 2.16.0 to mitigate CVE-2021-44228.

## Corda Enterprise Network Manager 1.4.1

CENM 1.4.1 introduces fixes to known issues in CENM 1.4.

### Enhancements

We have updated the default value of the optional `timeout` parameter, introduced in CENM 1.4, from 10000 ms to 30000 ms. This allows for better scalability of network map updates when a large number of nodes are registered on the network.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by CENM was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in CENM 1.2) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [PKI Tool]({{< relref "pki-tool.md" >}}) now generates certificates with serial number sizes of up to 16 octets/bytes.
* We have fixed an issue where the [PKI Tool]({{< relref "pki-tool.md" >}}) would throw an error when using [securosys HSM](https://www.securosys.com/) with multiple partitions.
* We have fixed an issue where the [signing request status command](#check-the-connection-status-of-the-signing-service) in the [CENM Command-line Interface]({{< relref "cenm-cli-tool.md" >}}) did not work for requests with `COMPLETED` status.
* We have fixed an issue where the `APP VERSION` column was not shown when running helm charts while bootstrapping CENM.

## Corda Enterprise Network Manager 1.4

CENM 1.4 introduces a range of new features and enhancements, including a [CENM error condition knowledge base](#cenm-error-condition-knowledge-base), a number of [Network Map Service performance enhancements](#network-map-service-performance-enhancements), a [new Signing Service plug-in functionality](#new-signing-service-plug-in-functionality-replaces-the-smr-signable-material-retriever-service) that replaces the SMR (Signable Material Retriever) Service, and [extended support for AWS native network deployment](#aws-native-network-deployment---reference-deployment-on-aws-eks-cloudhsm-postgresql) using [EKS](https://aws.amazon.com/eks/), [CloudHSM](https://aws.amazon.com/cloudhsm/), and [AWS PostgreSQL](https://aws.amazon.com/rds/postgresql/).

While this release is backward-compatible, you should consider upgrading to this release from earlier versions of the Corda Enterprise Network Manager.

{{< warning >}}

**Important upgrade notes**

Upgrading from CENM 1.3 to CENM 1.4 requires the following actions:

* Manual update of all existing Signing Service configurations.

  The SMR (Signable Material Retriever) Service, which prior to CENM 1.4 was used to handle plug-ins for signing data, [has been replaced](#new-signing-service-plug-in-functionality-replaces-the-smr-signable-material-retriever-service) by a plug-in loading logic inside the Signing Service. As a result, **all users must update their existing Signing Service configuration** when upgrading to CENM 1.4 - see the [CENM Upgrade Guide]({{< relref "upgrade-notes.md#manual-update-of-all-existing-signing-service-configurations" >}}) for details.

* Zone Service database migration.

  If you are upgrading to CENM 1.4 from CENM 1.3, you **must** set `runMigration = true` in the database configuration. See the [CENM Upgrade Guide]({{< relref "upgrade-notes.md#zone-service-database-migration" >}}) for details. This is required due to a [Zone Service database schema change](#network-map-service-performance-enhancements).

{{< /warning >}}

Read more about improvements of this release below.

### New features and enhancements

#### CENM error condition knowledge base

In CENM 1.4, we have adapted to CENM the internal Corda error handling logic introduced in Corda 4.5 and Corda Enterprise Edition 4.5 for Corda nodes.

As a result, CENM exceptions are now treated as CENM error codes and an error code is generated for each exception. The initial set of error codes, related to configuration parsing/validation errors, are described in the new [CENM error codes documentation page]({{< relref "cenm-error-codes.md" >}}). This is the start of a growing CENM error condition knowledge base, which will expand in future releases.

#### Network Map service performance enhancements

CENM 1.4 introduces performance improvements in the Network Map Service to ensure stable operations with a large amount of active participants in a network.

Performance and reliability improvements can be observed on the unsigned Network Map nodes' response, due to the serialization of fewer fields during the database information retrieval. This speeds up the response generation and avoids potential deadlocks, which could happen in previous CENM versions when more than one unsigned network map node calls were executed simultaneously.

Performance is enhanced through the following combination of changes:

* A new, optional `timeout` parameter now enables you to set specific [Signing Service timeouts]({{< relref "signing-service.md#signing-service-configuration-parameters" >}}) for communication to each of the services used within the signing processes defined in the network map, in a way that allows high node count network maps to get signed and to operate at reliable performance levels. You can also use the `timeout` parameter to set specific Network Map Service timeouts for communication to the [Identity Manager and Revocation services]({{< relref "network-map.md#identity-manager-and-revocation-communication" >}}). The `timeout` parameter's values are stored in a new `timeout` column in the [Zone Service]({{< relref "zone-service.md#signing-services-configuration" >}})'s database tables `socket_config` and `signer_config` (refer to the [CENM Upgrade Guide]({{< relref "upgrade-notes.md#zone-service-database-migration" >}}) for important details about migrating the Zone Service database from CENM 1.3).

* A [new API endpoint]({{< relref "network-map-overview.md#http-network-map-protocol" >}}), `GET network-map/node-infos`, enables you to retrieve a list of all signed `NodeInfo` objects for _all_ the nodes in the network at once.

* The following [new headers]({{< relref "network-map-overview.md#http-network-map-protocol" >}}) for Network Map API responses now make headers more closely aligned with HTTP standards:
  * The new header `X-Corda-Server-Version` has been added for all Network Map API responses (except for internal error responses with code 5xx) indicates the version of the Network Map and the available calls. It has a default value of `2`.
  * The new header `X-Corda-Platform-Version` replaces `Platform-version`. The old header name continues to be supported.
  * The new header `X-Corda-Client-Version` replaces `Client-version`. The old header name continues to be supported.

#### New Signing Service plug-in functionality replaces the SMR (Signable Material Retriever) Service

The SMR (Signable Material Retriever) Service was introduced in CENM 1.2 with the purpose of handling plug-ins for signing data. In CENM 1.4 we have replaced it with a plug-in loading logic as part of the Signing Service by fetching the signable data from the Identity Manager Service and the Network Map Service and sending it to either the new plug-in (if specified) or to the default Signing Service processing logic.

As a result we have removed the SMR Service completely, thus reducing the number of CENM services and eliminating the need to maintain RPC servers and storage previously created by the default SMR plug-in.

A range of new functionality and changes, introduced to that effect, are described below. See the [Signing Service]({{< relref "signing-service.md" >}}) documentation for full details.

**Configuration changes**

* The new `serviceLocation` property replaces `serviceLocationAlias`.

  The Signing Service configuration has been changed so that each signing task must now take in a `serviceLocation` property instead of a `serviceLocationAlias`.
  Multiple locations (one for each subzone) can be defined for non-CA signing tasks (Network Map, Network Parameters) using the new property.
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
* RPC function changes. To enable the complex task of returning Asynchronous Signing tracking ids and statuses when the signing is done via RPC, a number of changes have been made to RPC functions, including changes to requests and the addition of four new RPC requests used to query the status of each request via RPC. See the [Signing Service]({{< relref "signing-service.md" >}}) documentation for more information.

**Code changes**

* Common signers. We have the `common` module, making signer classes abstract and adding two implementation for each signer - one for the default logic and another one for the plug-in logic.
* `SigningServicePluginLoader`. This class is used to load the defined plug-ins from the configuration. It uses a Java `URLClassLoader` and a parent `ClassLoader` that can be provided as a constructor argument.

**Example CA plug-in**

CENM 1.4 ships with an example CA plug-in, which equips users with everything they need to know when creating their own plug-in. See the [Signing Service]({{< relref "signing-service.md" >}}) documentation for more information.


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

See the [CENM deployment]({{< relref "aws-deployment-guide.md" >}}) section for more information.

#### Other changes
* We have added support for PostgreSQL 10.10 and 11.5 (JDBC 42.2.8), as noted in [CENM Databases]({{< relref "database-set-up.md#supported-databases" >}}) and [CENM support matrix]({{< relref "cenm-support-matrix.md#cenm-databases" >}}).
* A `non-ca-plugin.jar` has been added to `signing-service-plugins` in Artifactory.
* We have renamed the FARM Service, introduced in CENM 1.3, to [Gateway Service]({{< relref "gateway-service.md" >}}). As a result, if you are [upgrading]({{< relref "upgrade-notes.md" >}}) from CENM 1.3 to CENM 1.4, the FARM Service JAR file used in CENM 1.3 should be replaced with the Gateway Service JAR file used in CENM 1.4.
* In CENM 1.4 we have changed the way `subZoneID` is set in Signing Service configurations - see the [CENM upgrade guide]({{< relref "upgrade-notes.md#signing-service-configuration-changes" >}}) for more details.

### Fixed issues

* We have fixed an issue where the [Auth Service]({{< relref "auth-service.md" >}}) could not start during database schema initialisation for PostgreSQL.
* We have fixed an issue where the Signing Service failed to start, following setup without the SMR (Signable Material Retriever) Service, producing a `serviceLocations` configuration error. Note that the SMR Service has been removed in CENM 1.4 and its functionality has been merged with the Signing Service - see the [New features and enhancements](#new-features-and-enhancements) section above for more details.
* We have fixed an issue where the `azure-keyvault-with-deps.jar` and `out.pkcs12` files were not copied to the `pki-pod` and PKI generation failed as a result.
* We have fixed an issue where HSM passwords were not hidden in service logs.
* We have fixed an issue where the Zone Service removed the `mode` field from the Signing Service's configuration with Utimaco and then failed to return this field to the Angel Service.
* Commands for the Identity Manager Service and the Network Map Service, which previously returned no information, now indicate when no data is available.
* We have fixed an issue where [Gateway Service]({{< relref "gateway-service.md" >}}) (previously called FARM Service in CENM 1.2) logs were not available in the `logs-farm` container.
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
