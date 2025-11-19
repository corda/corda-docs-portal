---
date: '2023-09-12'
menu:
  cenm-1-5:
    identifier: cenm-1-5-release-notes
    parent: cenm-1-5-cenm-releases
    weight: 80
tags:
- cenm
- release
- notes
title: Release notes
---

# Corda Enterprise Network Manager release notes

## Corda Enterprise Network Manager 1.5.9

CENM 1.5.9 introduces fixes to known issues in CENM 1.5.

### Fixed Issues

* The JDK version used by CENM has been upgraded from JDK 8.0.322 to JDK 8.0.382.
* Fixed an issue where the signing service, specifically using Gemalto Luna HSM, would deadlock when there was more than one outstanding signing task on starting the signing service.
* The PostgreSQL database driver shipped with CENM Docker images has been updated from version 42.2.25 to 42.5.2.
* When a CENM service starts, the startup log message generated now includes the service version.
* This release includes the following vulnerability fixes to third-party software:
   * org.springframework updated to 5.3.27
   * com.google.guava updated to 32.1.1-jre
   * org.apache.tomcat.embed updated to 9.0.80
   * Java 8 version 8u322 updated to 8u382
   * Postgres driver 42.2.25 updated to 42.5.2
   * removed MySQL references

## Corda Enterprise Network Manager 1.5.8

CENM 1.5.8 introduces fixes to known issues in CENM 1.5.

### Fixed Issues

* The duplicate response header `Transfer-Encoding` while accessing the endpoint `/api/v1/authentication/config` has been removed.

## Corda Enterprise Network Manager 1.5.7

CENM 1.5.7 introduces enhancements and fixes to known issues in CENM 1.5.

### Enhancements

* The 'Organization' column filter has been removed from the CRR/CRL status tab.
* The Java serialization in CENM has been disabled as a security mitigation against access being obtained maliciously to perform remote code execution.
* A synchronous call will now be made to the `IDManager` instead of an asynchronous call when a node requests to publish `nodeInfo`.

### Fixed Issues

* Improved error messages are returned when submitting a second CRR request for the same node via the CRR submission tool.
* Reduced deadlocks associated with the insert and/or update of `NodeInfoEntity` records.
* Fixed the hanging network map issue.
* The validity period of a child's certificate cannot be longer than the validity period of the parent's certificate. If the expiration date of the child's certificate is set to be longer than the parent's certificate, it will now be adjusted to fit within the expiration time window of the parent's certificate.
* The **Reset** button is now always enabled in the CENM UI, so any configuration changes made can be reverted.

## Corda Enterprise Network Manager 1.5.6

CENM 1.5.6 fixes two vulnerabilities by:

* excluding Jackson Databind.
* excluding Spring Framework.

## Corda Enterprise Network Manager 1.5.5

In CENM 1.5.5 nodes can be quarantined using the Network Map shell. Several bugs have also been fixed, introducing a more organised operational logic when two nodes are marked as 'current'. Several UI improvements have also been made.

* Revoked nodes can now be quarantined on demand, and quarantine functionality has been added to the admin shell.
  * A node is quarantined using its hash. To find the hash, use the command `view nodeInfoHashes` in the admin shell.
  * To view quarantined nodes, use the command: `view quarantinedNodeInfos`.
  * To purge a node from quarantine, use its hash and the command: `run purgeQuarantinedNodeInfo nodeInfoHash <hash>`.
  * All commands can also be found by using the `help` command in the Network Map shell.
  * Nodes with revoked certificates will be quarantined automatically.
* CENM 1.5.5 now uses Log4j's JSON log formatting for the Network Map and Signer, improving legibility and clarity of logs.
* The 'Remove Edit' button has now been enabled throughout the configuration process. This means syntax issues can be fixed more quickly and easily.

### Fixed issues

* If multiple nodes are marked as 'current' in the database and share the same legal name, only the incoming node is processed. Others are now suppressed with a warning in the logs.
* The copyright year (as visible in the UI) has been updated to reflect the current year.
* In the CRR status view, the defunct **Organization** filter has been replaced by an operational **Reporter** filter.
* The CRR submission tool produced an HTTP ERROR 500 in cases where several CRR requests were sent to the same node. This has now been resolved.
* Defunct subzones which have been merged into the MainZone will now always be empty, retaining no data.


## Corda Enterprise Network Manager 1.5.4

CENM 1.5.4 fixes an urgent security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Fixed issues

* The Log4j dependency has been updated to version 2.17.1 to fix pre-existing Log4j issues.

## Corda Enterprise Network Manager 1.5.3

{{< note >}}

This is a direct upgrade from 1.5.1. No version 1.5.2 was released.

{{< /note >}}

CENM 1.5.3 fixes an urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version 2.16.0.

To get started with this upgrade, request the download link by raising a ticket with [support](https://r3-cev.atlassian.net/servicedesk/customer/portal/2).

{{< warning >}}
Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.
{{< /warning >}}

### Fixed issues

We have updated the Log4j dependency to version 2.16.0 to mitigate CVE-2021-44228. This includes an update to the [CENM management console]({{< relref "cenm-console.md" >}}).

## Corda Enterprise Network Manager 1.5.1

CENM 1.5.1 introduces fixes to known issues in CENM 1.5.

### Enhancements

* CENM 1.5.1 now supports [Oracle Database 19c](https://docs.oracle.com/en/database/oracle/oracle-database/19/index.html).
* We have bumped the supported version of the AWS CloudHSM client library from 3.0.0 to 3.2.1.
* Configuration passwords are now hidden in both **CODE VIEW** and **FORM VIEW** modes in the [CENM management console]({{< relref "cenm-console.md" >}}) **CONFIGURATION**.

### Fixed issues

* We have fixed an issue where some certificate revocation reasons supported by the CENM Command-line Interface Tool (CLI) were not supported by the Identity Manager service. All CLI revocation reasons are now supported by the Identity Manager service.
* We have fixed an issue where service configurations were sometimes recorded in the logs by mistake. This problem was also present in CENM 1.3 and 1.4 and the fix has been ported back to these versions as well.
* We have fixed an issue where the signing CRL did not give sufficient details about the revocation after a revocation submission request was made using the CRR tool, and as a result the user had to inspect the Identity Manager Service logs for more information. The revoking node now shows more details, for example:
  ```
  Successfully signed request. The following certificates were added to the CRL:
  DN: O=PartyB, L=Chicago, C=US, Serial Number: 92919584395295172078852936608980933912
  ```
* We have fixed an issue where the signing request status command in the CENM Command-line Interface Tool (CLI) did not work for asynchronous signing.
* We have fixed an issue where the Network Map Service failed to start with an EC public key used in the `packageOwnership` configuration in the network parameters, and an `Unrecognised algorithm` error was thrown.
* We have fixed an issue where, if a CSR was rejected with a [rejection code]({{< relref "workflow.md#certificate-signing-request-rejection-reasons" >}}) between 1 and 11 via the Jira workflow, the node notification would be incorrect - the `Additional remark` field output would contain technical data instead of a description of the rejection reason.

#### Fixed issues specific to the CENM management console

We have also fixed the following issues specific to the [CENM management console]({{< relref "cenm-console.md" >}}):

* We have fixed an issue where removing scheduled times in **FORM VIEW** mode in the **SIGNER** tab of **CONFIGURATION** showed configuration details in **CODE VIEW** mode, which might result is Signing Service configuration failures.
* We have fixed an issue where the **Remove Edits** option in **CONFIGURATION** did not work for a number of fields for all configuration types.
* We have fixed an issue where the database properties field **AdditionalProperties** did not show `connectionInitSql` in **FORM VIEW** mode.
* We have fixed an issue where the SSL dropdown list did not shown in the **IDENTITY MANAGER** tab of **CONFIGURATION** in **FORM VIEW** mode.
* We have fixed an issue where the UI would freeze indefinitely with a "Deployment failure" error if an invalid configuration was deployed due to incorrect database credentials or missing plug-in details.
* We have fixed an issue where boolean parameters for the **ADMIN LISTENER** were not properly saved or set in **FORM VIEW** mode for Network Map configurations.
* We have fixed an issue with the `Removing signing key` option in the **SIGNER** tab of **CONFIGURATION** in **FORM VIEW** mode, which might prevent the user from confirming whether the signing key was actually removed or not.
* We have fixed an issue with setting scheduled signing time in **FORM VIEW** mode.
* We have fixed an issue where editing or renaming the alias for either issuance or revocation workflow type in the **IDENTITY MANAGER** tab of **CONFIGURATION** would result in complete removal of the workflow in **FORM VIEW** mode.
* We have fixed an issue where the CENM management console would fail to show a new zone after initial setup.
* We have fixed an issue where network parameters could not be set and flag day dates would default to the current time.
* We have fixed an issue where the **Update Config** remained enabled even without a configuration value change.
* We have fixed an issue where the CENM management console crashed and hung when attempting to deploy a valid configuration in **CODE VIEW** mode.
* We have fixed an issue where the `RequestID` and `Certificate Signing Request ID` fields on the **CRR/CRL Status** tab showed the same data.
* We have fixed an issue where the details for `Auth Service configuration`, which existed in the back-end configuration, were not shown for any of the configuration types in any of the two views - **CODE VIEW** and **FORM VIEW**.
* We have fixed an issue where removing an HSM Library from the **SIGNER** configuration in **FORM VIEW** mode resulted in a blank screen, which prompted the user to refresh the entire application.
* We have fixed an issue where the Angel Service did not get restored to the last working configuration and might stop polling when the SSL Keystore/TrustStore files were not found.
* We have fixed an issue where there was no indication shown when the user token was expired.
* We have fixed an issue where the theme, language, and font size in the **CONFIGURATION** tab were not saved when the user switched to a different tab.
* We have fixed an issue where changes in **CODE VIEW** mode were not reflected in **FORM VIEW** mode when the user switched over.
* We have fixed an issue where clicking **Cancel Flag Day** before the flag day was run would fail to cancel the flag day.

### Known issues

* There is still an option to view configuration passwords in **FORM VIEW** mode in the [CENM management console]({{< relref "cenm-console.md" >}}) **CONFIGURATION**.

{{< note >}}
The known issue listed above is specific to CENM 1.5.1. See the release notes for previous CENM releases further down on this page for information about known issues specific to those versions.
{{< /note >}}

## Corda Enterprise Network Manager 1.5

Corda Enterprise Network Manager (CENM) 1.5 introduces a number of new features and enhancements, including a new [CENM management console]({{< relref "cenm-console.md" >}}), single sign-on for Azure AD for Corda services, and the ability to reissue node legal identity keys and certificates.

While this release is backward-compatible, you should consider upgrading to this release from earlier versions of the Corda Enterprise Network Manager.

{{< warning >}}
Make sure to check out the [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}}) page.
{{< /warning >}}

### New features and enhancements

#### CENM management console

The [CENM management console]({{< relref "cenm-console.md" >}}) is a new CENM web UI that enables you to view CSR and CRR requests, display nodes in the network map, run a flag day, and update services configuration.

#### Single sign-on for Azure AD

CENM 1.5 introduces support for Azure Active Directory (AAD) as a single sign-on (SSO) for the CENM {{< cordalatestrelref "enterprise/node/auth-service.md" "Auth Service" >}}, which supports full Role-Based Access Control (RBAC) and provides a web-based management interface for system administrators to create and manage user groups and entitlements. As a result, you can now operate an SSO set-up between Corda services and Azure AD, with a {{< cordalatestrelref "enterprise/node/azure-ad-sso/_index.md" "simple configuration" >}} to both your Azure AD and Corda Auth services.

#### Certificate rotation: ability to reissue node legal identity keys and certificates

Corda Enterprise Edition 4.7 introduces a capability for reissuing node legal identity keys and certificates, allowing CENM to re-register a node (including a notary node) with a new certificate in the Network Map. You must not change the node's `myLegalName` during certificate rotation.

{{< warning >}}
The introduction of this functionality may require changes to your custom Identity Manager Workflow Plugins, regardless of using certificate reissuance functionality in your system. Make sure to check the [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}}) page.
{{< /warning >}}

For more information about this feature, contact your R3 account manager.

### Fixed issues

* We have fixed an issue where Network Map Service updates were stuck after more than approximately 1300 nodes were registered.
* We have fixed an issue where the Network Map Service was not fully started during CENM deployment on a Kubernetes cluster.

### Known issues

* When deploying a Network Map using the CENM Command-line Interface (CLI) Tool, the signing process for the Network Map could fail with the following error: "No NETWORK_PARAMETERS type signing process set up". The workaround for this issue is to stop the Angel Service and the Signing Service, and to manually kill the `signer.jar` process.
* The CENM Command-line Interface (CLI) Tool signing request `status` command fails when used for asynchronous signing.
* Running the CENM Command-line Interface (CLI) Tool command to cancel network parameters (`./cenm netmap netparams update cancel`) returns no message so it is unclear if it was run successfully or not.
* Insufficient revocation details are provided about signing a CRL after a revocation submission request is run by the CRR tool.
* The CENM Command-line Interface (CLI) Tool does not return a message if a token has expired when running `signer` commands.
* The Identity Manager Service shows an incorrect error when the `workflow.enmListener.port` parameter is missed.
* When setting up CENM services with Shell support, the Signing Service and the Network Map Service hang after running the `shutdown` command.
* When a CSR is rejected with a [rejection code]({{< relref "workflow.md#certificate-signing-request-rejection-reasons" >}}) between 1 and 11 via the Jira workflow, the node notification is incorrect - the `Additional remark` field output contains technical data instead of a description of the rejection reason.

{{< note >}}
The list above contains known issues specific to CENM 1.5. See the release notes for previous CENM releases further down on this page for information about known issues specific to those versions.
{{< /note >}}