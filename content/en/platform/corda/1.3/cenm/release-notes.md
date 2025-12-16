---
aliases:
- /release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-release-notes
    parent: cenm-1-3-cenm-releases
    weight: 80
tags:
- release
- notes
title: Release notes
---


# Release notes

## Corda Enterprise Network Manager 1.3.5

CENM 1.3.5 fixes an urgent security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Fixed issues

* The Log4j dependency has been updated to version 2.17.1 to fix pre-existing Log4j issues.

## Corda Enterprise Network Manager 1.3.4

{{< note >}}

This is a direct upgrade from 1.3.2 No version 1.3.3 was released.

{{< /note >}}

CENM 1.3.4 fixes an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version 2.16.0.

{{< warning >}}
Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.
{{< /warning >}}

### Fixed issues

We have updated the Log4j dependency to version 2.16.0 to mitigate CVE-2021-44228.

## Corda Enterprise Network Manager 1.3.2

CENM 1.3.2 introduces fixes to known issues in CENM 1.3.

### Fixed issues

* We have fixed an issue where the maximum length of a certificate's serial number allowed by CENM was 28 digits (`NUMBER(28)` format in the database) - roughly about 93 bits of data. To extend the support (introduced in CENM 1.2) for third-party CAs such as [SwissPKI](https://www.swisspki.com/), the Identity Manager Service can now handle certificate serial numbers with sizes up to 20 octets/bytes (160 bits) to comply with [RFC 5280](https://tools.ietf.org/html/rfc5280). In addition, the [PKI Tool]({{< relref "pki-tool.md" >}}) now generates certificates with serial number sizes of up to 16 octets/bytes.
* We have fixed an issue where the [PKI Tool]({{< relref "pki-tool.md" >}}) would throw an error when using [securosys HSM](https://www.securosys.com/) with multiple partitions.

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
 The new CENM Command-Line Interface (CLI) tool is supported by the new authentication and authorisation (Auth) service and enables users to access many of the functionalities included in this release, such as central log retrieval, configuration management, and multi-step service orchestration. Users are now able to authenticate through the new CLI tool and to perform actions according to their user-permissions (for example, run a flag day), thus eliminating the need to access the host of each individual service and its respective shell.
#### New User Admin tool
The User Admin tool that allows CENM administrators to connect securely via a web browser to create and manage new CENM users, groups, and roles for performing tasks on CENM services. The application supports the new authentication and authorisation (Auth) - which is used to check the credentials and permissions of each user.

#### New Auth Service for user authentication and authorisation
CENM 1.3 introduces a new authentication and authorisation service, allowing Network operators to manage users, groups and roles (along with fine grain permissions associated with roles) through a new management interface provided alongside. This service will first be used by internal services and via a new Command Line Tool and will allow authentication and enforcement of entitlements across all network operations.

#### New Zone Service for configuration management
The new Zone Service enables you to store configurations for the Identity Manager Service, the Network Map Service, and the Signing Service. The configuration composition capability allows you to use your updates to individual service configurations to trigger automatic updates to other services as needed.

#### Improvements to Kubernetes reference deployment
We have updated the Kubernetes reference deployment to use Helm@3 and to support the new services introduced in CENM 1.3. The updated documentation provides guidance on how to use this deployment with external databases.

#### Configuration obfuscation
Configuration obfuscation support in CENM 1.3 now involves the use of the Corda Enterprise {{< cordalatestrelref "enterprise/tools-config-obfuscator.md" "configuration obfuscator tool" >}}. Legacy (pre-1.3) obfuscated configurations are still supported, however you should update any such configuration files using the latest version of the Corda Enterprise configuration obfuscator tool.

#### Highly available Certificate Revocation List
Our documentation now provides some deployment recommendations on how to make the CRL highly available in a typical network deployment.

#### Other changes
- We have added the new Angel Service to enable the management of the Identity Manager Service, the Network Map Service, and other services. This feature includes a standardised health check API, functionality for fetching configuration from the Zone Service, and capability to enable remote access to service logs to assist with diagnosing issues.
- We have added the new Front-end Application for Remote Management (FARM) Service that acts as a gateway to enable the orchestration of requests from user interfaces (command-line interface or web UI) to back-end services.
- We have added support for managing the flag day process via the command-line interface, replacing the need for the network operator to directly log in to the Network Map and Signing Services. However, note that in the recommended deployment, the signing of parameters is done via systems in a restricted access network, and therefore network operators still need to access the Signing Service from within that restricted network.
- We have added support for labelling of subzones (Network Map Services) in order to give them a human-readable identifier.
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