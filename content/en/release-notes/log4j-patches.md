---
date: '2021-04-24T00:00:00Z'
menu:
  releases:
    name: Log4j patches
    identifier: log4j-patches
    title: Log4j patches
weight: 50
---

# Log4j patch releases

## Apache Log4j vulnerability patches

These patch releases address the Log4j vulnerability discovered December 9, 2021.


### Update February 11 2022

A patch has been released to move dependencies to Log4j 2.17.1 for Corda 5 Developer Preview 1.0.1.

You can find more information about this patch release in the [Corda 5 Developer Preview release notes](../../en/platform/corda/5.0-dev-preview-1/release-notes-c5dp1.md).

### Update February 7 2022


A patch has been released to move dependencies to Log4j 2.17.1 for Corda Enterprise 4.8.6.

You can find more information about this patch release in the [Corda Enterprise release notes](../../en/release-notes/corda-enterprise-4.8.html#previous-versions-of-corda-enterprise).


### Update February 1 2022

A patch has been released to move dependencies to Log4j 2.17.1 for:
* CENM 1.5.4
* CENM 1.4.4
* CENM 1.3.5
* CENM 1.2.6

You can find more information about this patch release in the [CENM release notes](../../en/release-notes/cenm-1.5.md).

### Update January 25 2022

A patch has been released to move dependencies to Log4j 2.17.1 for:
* Corda Enterprise 4.7.6
* Corda Enterprise 4.6.8
* Corda Enterprise 4.5.9
* Corda Enterprise 4.4.11
* Node management console 1.0.3
* Flow management console 1.0.3
* Business Network membership management 1.1.2

You can find more information about this patch release in the [release notes](../../en/release-notes/corda-enterprise-4.8.html#previous-versions-of-corda-enterprise).

### Update December 24 2021

Business Network Manager tool 1.0.1 update has been released. Please check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue)
for the updated schedule of outstanding patches.

All fixes move dependencies to Log4j 2.16.0.

### Update December 22 2021

An update for CENM 1.4.3 has been released, and version 1.0.2 has been released for the node management and flow management consoles. Please check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue) for the updated schedule of outstanding patches.

All fixes move dependencies to Log4j 2.16.0.

### Update December 21 2021

Investigations are in progress following the release of Log4j 2.17.0. However, as effective countermeasures against the
vulnerabilities identified in earlier versions have now been implemented, the update to Log4j 2.17.0 (or the latest
version at that time) will be available at the end of January 2022.

Updates for CENM 1.5.3 and the CENM Management Console have been released. Please check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue) for the updated schedule of outstanding patches.

All fixes move dependencies to Log4j 2.16.0.

### Update December 20 2021

Investigations are in progress following the release of Log4j 2.17.0. As Corda’s explicit disabling of Java
serialization is an effective countermeasure against the vulnerabilities, the update to Log4j 2.17.0 (or the latest version
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

Check the [patch release timetable](#corda-and-cenm-patch-release-timetable-for-apache-log4j-issue) for expected patch release dates for your version of Corda or CENM. Use the [mitigation guide](#what-you-can-do-now) to reduce your risk before upgrading to the new patch.

## What you can do now

If a patch has been released for your current version of Corda, follow the instructions for [upgrading nodes to a new minor version](../en/platform/corda/4.8/enterprise/minor-version-node-upgrade.md). You do not need to patch CorDapps— they inherit Apache Log4j from the Corda runtime.

If you are waiting for the release of the required emergency patch for your current version, you can apply one of the following steps to mitigate the threat implied by the Apache Log4j vulnerability:

### For Corda OS/ENT 4.3 and above and CENM 1.3 and above

Use the `log4j2.formatMsgNoLookups` Java property. Set this property to true when specifying it as a Java parameter when running Corda as follows:

`java -Dlog4j2.formatMsgNoLookups=true -jar corda.jar`

Alternatively, you can configure a system environment variable which has the same effect. For example, in Linux:

`export LOG4J_FORMAT_MSG_NO_LOOKUPS=true`

In both cases, the Corda node must be restarted for these mitigations to take effect.

### Older versions of Corda

For Corda and CENM versions using an older version of log4j prior to 2.10, the mitigation outlined for later versions does not work. You should continue to check these pages as new mitigation steps are being tested and will be added as soon as possible.
Refer to https://nvd.nist.gov/vuln/detail/CVE-2021-44228 or https://logging.apache.org/log4j/2.x/security.html for information in the mean time.


## Corda Enterprise and CENM patch release timetable for Apache Log4J issue

This table was last updated on February 11 2022 14:00 GMT.

**All patches listed upgrade to Log4j 2.16.0, except Corda 5 Developer Preview 1.1 which is an upgrade to Log4j 2.17.1**

| Version with new patch                   | Patch target shipping date | Interim mitigation available |
|:---------------------------------------- |:-------------------------- |:---------------------------- |
| Corda Enterprise 4.8.5                   | **Released** Dec 16        | Yes                          |
| Corda Enterprise 4.7.5                   | **Released** Dec 16        | Yes                          |
| Corda Enterprise 4.6.7                   | **Released** Dec 16        | Yes                          |
| Corda Enterprise 4.5.8                   | **Released** Dec 16        | Yes                          |
| Corda Enterprise 4.4.10                  | **Released** Dec 16        | Yes                          |
| Corda Enterprise 4.3.10                  | **Released** Dec 16        | Yes                          |
| CENM 1.5.3                               | **Released** Dec 21        | Yes                          |
| CENM 1.4.3                               | **Released** Dec 22        | Yes                          |
| CENM 1.3.4                               | **Released** Dec 20        | Yes                          |
| CENM 1.2.5                               | **Released** Dec 17        | No                           |
| Corda 5 Developer Preview 1.1            | **Released** Feb 11        | NA - not used in production  |
| Business Network Manager tool 1.1.1      | **Released** Dec 17        | No                           |
| Business Network Manager tool 1.0.1      | **Released** Dec 24        | No                           |
| CENM management console (Gateway Plugin) | **Released** Dec 21        | No                           |
| Node management console 1.0.2            | **Released** Dec 22        | No                           |
| Flow management console 1.0.2            | **Released** Dec 22        | No                           |

{{< note >}}
These patch releases are valid for the stated supported versions of Corda Enterprise and CENM only. If you are not using a supported version of Corda Enterprise or CENM, please upgrade to one of the above versions.
{{< /note >}}

## Corda OS

Patch releases are not available for Corda OS.

Corda OS 4.3-4.8 Log4j dependency has been updated to v2.17.1.
