---
date: '2021-04-24T00:00:00Z'
section_menu: releases
menu:
  projects:
    name: Releases
    weight: 8
    identifier: homepage-releases
    project: releases
project: releases
version: 'releases'
title: Alerts
---
# Alerts and releases

This page provides updates on all major alerts, fixes and forthcoming patch releases. Check the top of the page for most urgent alerts. Scroll down for [current release information](#current-releases).

## Apache Log4j announcement

### Update December 20 2021

Investigations are in progress following the release of Log4j 2.17.0. As Corda’s explicit disabling of Java
serialisation is an effective countermeasure against the vulnerabilities, the update to Log4j 2.17.0 (or the latest version
at that time) will be available at the end of January 2022.

CENM 1.3.4 and Business Network Manager tool 1.1.1 updates have been released. Please check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue)
for the updated schedule of outstanding patches.

All fixes move dependencies to Log4j 2.16.0.

### Update December 17 2021

All planned Corda OS and Corda Enterprise updates have been released. CENM 1.2.5 has been released. Please check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue) for the updated schedule of outstanding patches. Some CENM patches have been pushed back from Dec 17 to Dec 20.

All fixes move dependencies to the latest secure patch of Apache Log4j - 2.16.0.

### Update December 16 2021

Patch releases to upgrade Corda and CENM to a safe version of Apache Log4j have been accelerated. Please check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue) for new dates. Many patches have been brought forward and are now due for release on December 16.

For details of each release, and to get access to downloads, check the release notes page for your version of Corda and CENM in the docs.

### Update December 15 2021

{{< note >}}
A new vulnerability has been discovered in version 2.15.0 of the log4j logging library, as described here: https://nvd.nist.gov/vuln/detail/CVE-2021-45046.
Additional patches are in progress for all current supported software versions for this issue. New patches will upgrade Corda and CENM dependencies to Log4j 2.16.0.
{{< /note >}}


In response to news of the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228), and subsequent [vulnerability in the patch Log4j 2.15.0 patch](https://nvd.nist.gov/vuln/detail/CVE-2021-45046), new patches for all supported versions of Corda Open Source, Corda Enterprise, and CENM are in progress.

You do not need to patch CorDapps— they inherit Apache Log4j from the Corda runtime.

Check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue) for expected patch release dates for your version of Corda or CENM. Use the [mitigation guide](#what-you-can-do-now) to reduce your risk before upgrading to the new patch.

## What you can do now

While you wait for the release of the required emergency patch, you can apply one of the following steps to mitigate the threat implied by the Apache Log4j vulnerability:

### For Corda OS/ENT 4.3 and above and CENM 1.3 and above

Use the `log4j2.formatMsgNoLookups` Java property. Set this property to true when specifying it as a Java parameter when running Corda as follows:

`java -Dlog4j2.formatMsgNoLookups=true -jar corda.jar`

Alternatively, you can configure a system environment variable which has the same effect. For example, in Linux:

`export LOG4J_FORMAT_MSG_NO_LOOKUPS=true`

In both cases, the Corda node must be restarted for these mitigations to take effect.

### Older versions of Corda

For Corda and CENM versions using an older version of log4j prior to 2.10, the mitigation outlined for later versions does not work. You should continue to check these pages as new mitigation steps are being tested and will be added as soon as possible.
Refer to https://nvd.nist.gov/vuln/detail/CVE-2021-44228 or https://logging.apache.org/log4j/2.x/security.html for information in the mean time.


## Corda and CENM patch release timetable for Apache Log4J issue

This table was last updated on December 20 2021 16:30 GMT.

**All patches listed upgrade to Log4j 2.16.0**

| Version with new patch | Patch target shipping date | Interim mitigation available |
|:---------------------- |:-------------------------- |:---------------------------- |
| Corda OS/CE 4.8.5      | **Released** Dec 16        | Yes                          |
| Corda OS/CE 4.6.7      | **Released** Dec 16        | Yes                          |
| Corda OS/CE 4.5.8      | **Released** Dec 16        | Yes                          |
| Corda OS/CE 4.7.5      | **Released** Dec 16        | Yes                          |
| Corda OS/CE 4.4.10     | **Released** Dec 16        | Yes                          |
| Corda OS/CE 4.3.10     | **Released** Dec 16        | Yes                          |
| CENM 1.2.5             | **Released** Dec 17        | No                           |
| CENM 1.5.3             | Dec 21                     | Yes                          |
| CENM 1.3.4             | **Released** Dec 20        | Yes                          |
| CENM 1.4.3             | Dec 21                     | Yes                          |
| Corda 5 Developer Preview                | Dec 21                  | NA - not used in production  |
| Business Network Manager tool 1.1.1      | **Released** Dec 17     | No                           |
| Business Network Manager tool 1.0.1      | Dec 22                  | No                           |
| CENM management console (Gateway Plugin) | Dec 21                  | No                           |
| Node management console                  | Dec 21                  | No                           |
| Flow management console                  | Dec 21                  | No                           |

{{< note >}}
These patch releases are valid for the stated supported versions of Corda and CENM only. If you are not using a supported version of Corda or CENM, please upgrade to one of the above versions.
{{< /note >}}


## Current releases

Release notes for R3 products let you see what's new, what's been enhanced, what's been fixed, and any known issues. Alongside release notes you can also view third-party license information and reference to release files and their artifact checksums.

Find here the release notes for the latest versions of Corda open source, Corda Enterprise, and Corda Enterprise Network Manager (CENM), plus links to historic release notes for reference.

## Corda 5 Developer Preview

[The Corda 5 Developer Preview](../../en/platform/corda/5.0-dev-preview-1/release-notes-c5dp1.md) is a hands-on advanced look at Corda’s next major iteration, Corda 5. You can experiment with three key aspects of Corda 5:

* A new modular API structure. This lets you build applications to use on Corda (CorDapps) and test them efficiently.
* An HTTPS API, based on Open API principles. This allows you to control nodes and initiate flows remotely.
* Package your CordApps with a new Gradle plugin that allows for multi-tenancy applications in future releases.

## Corda open source 4.8

Corda open source 4.8 is the latest open source version of Corda, with commitments to wire and API stability. It introduces several fixes and improvements. States and CorDapps from version 3.0 and above are compatible with Corda 4.8. See the [full 4.8 release notes](../../en/platform/corda/4.8/open-source/release-notes.md).

### Previous versions of Corda open source

* [Corda open source 4.7](../../en/platform/corda/4.7/open-source/release-notes.md)
* [Corda open source 4.6](../../en/platform/corda/4.6/open-source/release-notes.md)
* [Corda open source 4.5](../../en/platform/corda/4.5/open-source/release-notes.md)
* [Corda open source 4.4](../../en/platform/corda/4.4/open-source/release-notes.md)
* [Corda open source 4.3](../../en/platform/corda/4.3/open-source/release-notes.md)
* [Corda open source 4.1](../../en/platform/corda/4.1/open-source/release-notes.md)
* [Corda open source 4.0](../../en/platform/corda/4.0/open-source/release-notes.md)

## Corda Enterprise 4.8

Corda Enterprise 4.8 is a long-term support release, with commitments to wire and API stability. It introduces several fixes and improvements. States and CorDapps from version 3.0 and above are compatible with Corda Enterprise 4.8. See the [full 4.8 release notes](../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md).

### Previous versions of Corda Enterprise

* [Corda Enterprise 4.7](../../en/platform/corda/4.7/enterprise/release-notes-enterprise.md)
* [Corda Enterprise 4.6](../../en/platform/corda/4.6/enterprise/release-notes-enterprise.md)
* [Corda Enterprise 4.5](../../en/platform/corda/4.5/enterprise/release-notes-enterprise.md)
* [Corda Enterprise 4.4](../../en/platform/corda/4.4/enterprise/release-notes-enterprise.md)
* [Corda Enterprise 4.3](../../en/platform/corda/4.3/enterprise/release-notes-enterprise.md)
* [Corda Enterprise 4.2](../../en/platform/corda/4.2/enterprise/release-notes-enterprise.md)
* [Corda Enterprise 4.1](../../en/platform/corda/4.1/enterprise/release-notes-enterprise.md)
* [Corda Enterprise 4.0](../../en/platform/corda/4.0/enterprise/release-notes-enterprise.md)

## Corda Enterprise Network Manager (CENM) 1.5

The Corda Enterprise Network Manager (CENM) lets Corda Enterprise customers deploy, operate, and set consensus rules for their networks. CENM versions are released separately from Corda Enterprise versions and follow an independent version sequence. The latest version of CENM is [CENM 1.5](../../en/platform/corda/1.5/cenm/release-notes.md), which introduces a new CENM management console, single sign-on functionality for Azure AD for Corda services, and the ability to reissue node legal identity keys and certificates. While this release is backward-compatible, you should consider upgrading to this release from earlier versions of CENM.

### Previous versions of CENM

* [CENM 1.4](../../en/platform/corda/1.4/cenm/release-notes.md)
* [CENM 1.3](../../en/platform/corda/1.3/cenm/release-notes.md)
* [CENM 1.2](../../en/platform/corda/1.2/cenm/release-notes.md)
* [CENM 1.1](../../en/platform/corda/1.1/cenm/release-notes.md)
* [CENM 1.0](../../en/platform/corda/1.0/cenm/release-notes.md)

## Archived release documentation of older, non-supported Corda releases

All documentation for older historic releases of Corda open source (versions 1.0, 2.0, and 3.0 to 3.3) and Corda Enterprise (versions 3.0 to 3.4), including release notes, is accessible from the [archived docs](https://github.com/corda/corda-docs-portal/tree/main/archived-docs) directory in the [corda/corda-docs-portal](https://github.com/corda/corda-docs-portal) repository.
