---
date: '2021-08-03'
menu:
  corda-enterprise-4-8:
    identifier: "corda-enterprise-4-8-cordapp-upgrade"
    parent: corda-enterprise-4-8-upgrading-menu
tags:
- app
- upgrade
- notes
title: Upgrading a CorDapp to a newer platform version
weight: 30
---

# Upgrading a CorDapp to a newer platform version

{{< warning >}}
Corda Enterprise Edition 4.8 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise Edition 4.8, read the guidance on [upgrading your notary service](notary/upgrading-the-ha-notary-service.md).
{{< /warning >}}

This guide shows you how to upgrade your CorDapp from previous platform versions to benefit
from the new features in the latest release.

Most of Corda's public, non-experimental APIs are backwards compatible. See the [full list of stable APIs](cordapps/api-stability-guarantees.html). If you are working with a stable API, you don't need to update your CorDapps. However, there are usually new features and other opt-in changes that may improve the security, performance, or usability of your
CorDapp that are worth considering for any actively maintained software.


{{< warning >}}
Sample CorDapps found in the Corda and Corda samples repositories should not be used in production.
If you do use them, re-namespace them to a package namespace you control and sign/version them.

{{< /warning >}}

## Platform version matrix

{{< table >}}
| Corda release  | Platform version |
| :------------- | :------------- |
| 4.8 | 10 |
| 4.7 | 9 |
{{< /table >}}

## Upgrading apps to platform version 9 and 10

No manual upgrade steps are required.

## Upgrading apps to platform version 8 or lower

If you need to upgrade your apps to platform version 8 or lower,
follow instructions published in our [GitHub documentation repository](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-enterprise/4.6/enterprise/app-upgrade-notes.md).
