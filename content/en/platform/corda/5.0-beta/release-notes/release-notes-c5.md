---
date: '2022-11-15'
title: "Release Notes"
menu:
  corda-5-beta:
    identifier: corda-5-beta-release-notes
    weight: 6000
section_menu: corda-5-beta
---

Corda 5.0 Beta is a pre-release version for testing purposes only.
{{< note >}}
If you are not part of the beta programme, the Corda 5.0 Beta documentation is for information only.
R3 will be running a Beta program for Corda 5.0 beginning in 2023. Contact R3 to register your interest.
{{< /note >}}

## Enhancements

This section describes the new features in Corda 5.0 Beta 1.

## Resolved Issues

This section describes the issues resolved in Corda 5.0 Beta 1.

### Multiple CPIs with Same Group ID in Same Network

It was not possible to upload a CPI that contained a group policy file associated to a group ID of a CPI that was already present in the network.
As of this release, this validation has been removed and Corda only checks that a CPI does not have the same name, version, and signer of an existing CPI. 
This facilitates Notary plugin CPIs and other scenarios where two different CPBs must use the same group ID to interact with each other on the same network.