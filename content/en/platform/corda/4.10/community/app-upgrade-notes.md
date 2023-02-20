---
aliases:
- /head/app-upgrade-notes.html
- /HEAD/app-upgrade-notes.html
- /app-upgrade-notes.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-app-upgrade-notes
    parent: corda-community-4-10-upgrading
    weight: 20
tags:
- app
- upgrade
- notes
title: Upgrading CorDapps to newer platform versions
---

# Upgrading CorDapps to newer platform versions

These notes provide information on upgrading your CorDapps from previous versions. Corda provides backwards compatibility for public,
non-experimental APIs that have been committed to. A list can be found in the [API stability guarantees](api-stability-guarantees.md) page.

This means that you can upgrade your node across versions *without recompiling or adjusting your CorDapps*. You just have to upgrade
your node and restart.

However, there are usually new features and other opt-in changes that may improve the security, performance or usability of your
application that are worth considering for any actively maintained software.

{{< warning >}}
The sample apps found in the Corda repository and the Corda samples repository are not intended to be used in production.
If you are using them you should re-namespace them to a package namespace you control, and sign/version them yourself.
{{< /warning >}}

## Platform version matrix

{{< table >}}
| Corda release  | Platform version |
| :------------- | :------------- |
| 4.10 | 12 |
| 4.9 | 11 |
| 4.8 | 10 |
| 4.7 | 9 |
{{< /table >}}

## Upgrading apps to platform version 9, 10, 11, and 12

No manual upgrade steps are required.

## Upgrading apps to platform version 8 or lower

If you need to upgrade your apps to platform version 8 or lower,
follow instructions published in our [GitHub documentation repository](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-os/4.6/app-upgrade-notes.md).
