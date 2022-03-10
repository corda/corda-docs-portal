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


# Corda Community Edition 4.9 release notes

**Corda Community Edition** is here. This edition of Corda gives you the freedom of Corda's Open Source platform, with the benefits of affordable support. All the same fundamentals of Corda 4.8 are included, along with security updates, newly available APIs and sample code improvements. You can upgrade your existing Corda projects to Community Edition any time to be eligible for our support packages.

## Highlights

The Corda Community Edition features:

* Support for your open source projects. [Find out more about available support and how to upgrade](_index.html).
* An Open Source version of network map and doorman is available and recommended for Community Edition users, provided by Cordite. .
* Community Edition Docker images are now available.
* The `flowrpcops` API is available and documented.

## Platform version change

Corda 4.9 uses platform version 11.

For more information about platform versions, see [Versioning](../../../../../en/platform/corda/4.9/community/versioning.md).

## Fixed issues

Issues fixed in Corda Community 4.9:

* Corda Shell has been removed to its own repository for improved security. You can now use a stand alone shell outside of the node, or from within the node's drivers.
* Security updates to prevent possibility of Denial of Service attacks.
* Improvements to demos and sample code.
* Improvements to improve compatibility with Intel Macs.
* An issue affecting Node JVM deadlocks is resolved.
* An issue with failed attachments from a notary has been fixed.
* An issue preventing attachments to subflows in certain circumstances has been fixed.
