---
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2021-06-29'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-release-notes
    weight: 1
    name: Release notes
tags:
- release
- notes
title: Release notes
---


# Corda Open Source 4.8 release notes

## Corda Open Source 4.8 Apache Log4j update release notes (December 16 2021)

Corda 4.8 was updated on December 16th 2021 to fix the urgent security issue - CVE-2021-44228 - caused by the Apache Log4j 2 dependency.

{{< warning >}}

Upgrade to avoid exposure to the [Apache Log4j 2 vulnerability to attack](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). This is the most secure way to mitigate any risks associated with this vulnerability.

{{< /warning >}}

To build the latest version of Corda 4.8:

1. Open a terminal window in the directory where you want to download the Corda repository.
2. Clone the Corda repository by running this command:
   `git clone https://github.com/corda/corda.git`
3. Checkout the release branch for Corda 4.8 by running this command:
   `git checkout origin/release/os/4.8`
4. Run the command:
   `./gradlew assemble`
5. Find `node/capsule/build/libs/corda-4.8-SNAPSHOT.jar`, this replaces your node's current `corda.jar`. To replace the superseded `.jar` file, follow the instructions on [upgrading your node to Corda 4.8](node-upgrade-notes.md).

## Corda Open Sourve 4.8 release notes

Corda 4.8, released on April 21st 2021, includes several fixes and improvements.

{{< note >}}
You can use states and CorDapps valid in Corda 3.0 and above with Corda 4.8.


For the commitment Corda makes to wire and API stability, see [API stability guarantees](../../../../../en/platform/corda/4.8/open-source/api-stability-guarantees.md).
{{< /note >}}

## Long-term support release

Corda 4.8 and [Corda Enterprise Edition 4.8](../../../../../en/platform/corda/4.8/enterprise/release-notes-enterprise.md) are our long-term support (LTS) platform versions.

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
