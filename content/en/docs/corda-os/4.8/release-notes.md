---
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2021-06-28T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-release-notes
    weight: 1
tags:
- release
- notes
title: Release notes
---


# Corda 4.8 release notes

This release introduces several fixes and improvements.

{{< note >}}
States and CorDapps valid in Corda 3.0 and above, are usable in Corda 4.8.


For the commitment Corda makes to wire and API stability, see [API stability guarantees](api-stability-guarantees.md).
{{< /note >}}

## Long-term support (LTS) release

As part of our first major Corda release for 2021, Corda 4.8 and [Corda Enterprise 4.8](../../corda-enterprise/4.8/release-notes-enterprise.md) are our long-term support (LTS) platform versions, which bring improvements and stability fixes that continue to enhance the maturity of the platform as a whole.

LTS for this release will be provided for 30 months from 21 April 2021, 6 months more than our previous support period, giving Corda customers extra time to plan for the next upgrade.

## Platform version change

The platform version of Corda 4.8 is 10.

For more information about platform versions, see [Versioning](versioning.md).

## Fixed issues

* We have fixed an issue that caused transaction verification to be performed outside of the attachments class loader.
* We have clarified some inconsistencies in source code comments.
* We have fixed an issue where flows could disable validation, leading to privileges escalation.
* We have fixed an issue where the attachment presence cache contained the attachment contents.
* We have fixed an issue where permissions were failing for `StartFlowWithClientId`.
* We have fixed an issue where the service loader could leak `jar_cache` handles.
* We have addressed a security issue in a Corda dependency.
* We have fixed an issue that caused `CordaPersistence.transaction` to fail to flush correctly.

