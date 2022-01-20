---
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2021-06-29'
menu:
  corda-community-4-9:
    identifier: corda-community-4-9-release-notes
    weight: 1
tags:
- release
- notes
title: Release notes
---


# Corda release notes

## Apache Log4j update

### Updated December 16 2021

Download the [latest version of Corda 4.8](https://github.com/corda/corda) to fix the urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency.

{{< warning >}}

Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.

{{< /warning >}}


## Corda 4.8 release notes

Corda 4.8, released on April 21st 2021, includes several fixes and improvements.

{{< note >}}
You can use states and CorDapps valid in Corda 3.0 and above with Corda 4.8.


For the commitment Corda makes to wire and API stability, see [API stability guarantees](../../../../../en/platform/corda/4.8/open-source/api-stability-guarantees.md).
{{< /note >}}

## Long-term support release

Corda 4.8 and [Corda Enterprise 4.8](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md) are our long-term support (LTS) platform versions.

R3 provides LTS for this release for 30 months starting April 21st 2021. This is 6 months longer than the support periods for previous releases, giving Corda customers extra time to plan for the next upgrade.

## Platform version change

Corda 4.8 uses platform version 10.

For more information about platform versions, see [Versioning](../../../../../en/platform/corda/4.8/open-source/versioning.md).

## Fixed issues

Corda 4.8 fixes:

* Transaction verification being performed outside of the attachments class loader.
* Inconsistencies in source code comments.
* Privileges escalation caused by flows disabling validation.
* Attachment presence cache containing the attachment contents.
* Permissions failing for `StartFlowWithClientId`.
* Service loader leaking `jar_cache` handles.
* A security issue in a Corda dependency.
* `CordaPersistence.transaction` failing to flush correctly.
