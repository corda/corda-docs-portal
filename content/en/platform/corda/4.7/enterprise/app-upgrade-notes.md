---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    identifier: "corda-enterprise-4-7-cordapp-upgrade"
    parent: corda-enterprise-4-7-upgrading-menu
tags:
- app
- upgrade
- notes
title: Upgrading a CorDapp to a newer platform version
weight: 30
---

# Upgrading a CorDapp to a newer platform version

{{< warning >}}
Corda Enterprise Edition 4.7.1 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise Edition 4.7.1 please read the guidance on [upgrading your notary service](../../../../../en/platform/corda/4.7/enterprise/notary/upgrading-the-ha-notary-service.md).
{{< /warning >}}

These notes provide instructions for upgrading your CorDapps from previous versions. Corda provides backwards compatibility for public,
non-experimental APIs that have been committed to. A list can be found in the api-stability-guarantees page.

This means that you can upgrade your node across versions *without recompiling or adjusting your CorDapps*. You just have to upgrade
your node and restart.

However, there are usually new features and other opt-in changes that may improve the security, performance or usability of your
application that are worth considering for any actively maintained software. This guide shows you how to upgrade your app to benefit
from the new features in the latest release.


{{< warning >}}
The sample apps found in the Corda repository and the Corda samples repository are not intended to be used in production.
If you are using them you should re-namespace them to a package namespace you control, and sign/version them yourself.

{{< /warning >}}

## Upgrading apps to platform version 9

No manual upgrade steps are required.

## Upgrading apps to platform version 8 or lower

If you need to upgrade your apps to platform version 8 or lower,
follow instructions published in our [GitHub documentation repository](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-enterprise/4.6/enterprise/app-upgrade-notes.md).
