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
If you are not part of the current beta program, the Corda 5.0 Beta documentation is for information only.
R3 will be running a beta program for Corda 5.0 beginning in 2023. Contact R3 to register your interest.
{{< /note >}}

## Enhancements

This section describes the new features in Corda 5.0 Beta 1.

## Resolved Issues

This section describes the issues resolved in Corda 5.0 Beta 1.

### Multiple CPIs with Same Group ID in Same Cluster

It was not possible to upload a CPI that contained a group policy file associated to a group ID of a CPI that was already present in the cluster.
As of this release, this validation has been removed and Corda only checks that a CPI does not have the same name, version, and signer of an existing CPI. 
This facilitates Notary plugin CPIs and other scenarios where two different CPBs must use the same group ID to interact with each other on the same cluster.

## Known Limitations

* Corda 4 CorDapps will not run on Corda 5; it is a different set of incompatible APIs.
* Upgrade from Corda 4 to Corda 5 is not supported; a future version will provide migration guidance and tooling.
* There is no support for the Corda 4 Accounts SDK.
* There is no support for the Corda 4 Tokens SDK.
* There is no support for upgrades from the early access beta versions.