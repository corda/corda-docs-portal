---
aliases:
- /release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-5:
    identifier: cenm-1-5-release-notes
    parent: cenm-1-5-cenm-releases
    weight: 80
tags:
- release
- notes
title: Release notes
---


# Corda Enterprise Network Manager release notes

## Corda Enterprise Network Manager 1.5

Corda Enterprise Network Manager (CENM) 1.5 introduces a number of new features and enhancements, including a new [CENM Console](cenm-console.md), single sign-on for Azure AD for Corda services, and the ability to reissue node legal identity keys and certificates.

While this release is backward-compatible, you should consider upgrading to this release from earlier versions of the Corda Enterprise Network Manager.

{{< warning >}}
Make sure to check out the [Upgrading Corda Enterprise Network Manager](upgrade-notes.md) page.
{{< /warning >}}

### New features and enhancements

#### CENM Console

The [CENM management console](cenm-console.md) is a new CENM web UI that enables you to view CSR and CRR requests, display nodes in the network map, run a flag day, and update services configuration.

#### Single sign-on for Azure AD

CENM 1.5 introduces support for Azure Active Directory (AAD) as a Single sign-on (SSO) for the CENM [Auth Service](auth-service.md), which supports full Role-Based Access Control (RBAC) and provides a web-based management interface for system administrators to create and manage user groups and entitlements. As a result, you can now operate a SSO set-up between Corda services and Azure AD, with a [simple configuration](azure-ad-sso.md) to both your Azure AD and Corda Auth services.

#### Certificate rotation: ability to reissue node legal identity keys and certificates

Corda Enterprise 4.7 introduces a capability for reissuing node legal identity keys and certificates, allowing CENM to re-register a node (including a notary node) with a new certificate in the Network Map.

{{< warning >}}
The introduction of this functionality may require changes to your custom Identity Manager Workflow Plugins, regardless of using certificate reissuance functionality in your system. Make sure to check the [Upgrading Corda Enterprise Network Manager](upgrade-notes.md) page.
{{< /warning >}}

For more information about this feature, contact [R3 support](https://www.r3.com/support/).

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
* When a CSR is rejected with a [rejection code](workflow.md#certificate-signing-request-rejection-reasons) between 1 and 11 via the JIRA workflow, the node notification is incorrect - the `Additional remark` field output contains technical data instead of a description of the rejection reason.

{{< note >}}
The list above contains known issues specific to CENM 1.5. See the release notes for previous CENM releases further down on this page for information about known issues specific to those versions.
{{< /note >}}
