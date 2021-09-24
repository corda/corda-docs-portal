---
date: '2021-09-2012:00:00Z'
title: "CorDapp packaging"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-packaging
    weight: 1200
project: corda-5
section_menu: corda-5-dev-preview
---

# CorDapp packaging

In Corda 5 Development Preview, CorDapps are distributed as Corda package files (`.cpk` files), and Corda package bundles (`.cpb` files).

## Corda package files

Corda package files (`.cpk` files) are the standard way to distribute CorDapps for Corda 5 Development Preview. A Corda package file is a `.zip` file with a `.cpk` extension. It is a “jar-of-jars” single distributable for the CorDapp. It contains META-INF files for publisher content signing, and that define versioning and dependencies. The dependency information in the `.cpk` file defines dependencies based upon version, hash, and publisher key.

The `.cpk` file also contains the main CorDapp `.jar` file and its dependencies, except for Corda’s own `.jar` files and `.jar` files that are provided by Corda (such as Kotlin and Quasar).

The main `.jar` file contains enough OSGi metadata to be a valid OSGi bundle.

Corda package files are created using the [CorDapp CPK gradle plugin](gradle-plugin/overview.md).

## Corda package bundles

A Corda package bundle (`.cpb` file) contain `.cpk` files, plus a `MANIFEST.MF` and other Corda-related information.

They can be created with the [CorDapp Builder CLI tool](cordapp-builder.md) or with the [CorDapp CPB gradle plugin](gradle-plugin/overview.md).

The point of the `.cpb` file is to contain all of the `.cpk` files that are expected to be deployed together as a single application. So in a typical example, you would apply `net.corda.plugins.cordapp-cpk` for the contract CPK project, and `net.corda.plugins.cordapp-cpb` in the workflows CPB project. The  `.cpb` file would then contain both your contracts and your workflows' `.cpk`s.


## Inspecting Corda package files

You can use the `package` command in the Corda CLI command-line utility to inspect the contents of Corda package files. For more information, see [CPK inspection tool](../corda-cli/commands.md).

## Corda Security Manager

The Corda Security Manager prevents CorDapp packages from performing certain dangerous operations, such as a sandboxed package installing bundles outside the sandbox. The Corda Security Manager starts automatically on node startup; no user interaction is required.

The Corda Security Manager leverages the OSGi security layer to deny the following permissions to all `.cpb`s:

* `AdminPermission.LIFECYCLE` - required to install, update, or uninstall bundles.
* `AdminPermission.EXECUTE` - required to start, stop, or modify the start level of bundles.
* `AdminPermission.EXTENSIONLIFECYCLE` - as above, but for extension bundles.
* `AdminPermission.RESOLVE` - required to resolve or refresh bundles.

Any attempt by CPK code to perform one of the operations above will cause an `AccessControlException` to be thrown.

{{< note >}}

These permission restrictions are in addition to any permission restrictions that the `.cpb` requests via the local permissions mechanism described in section 50.11 of the [OSGi specification](http://docs.osgi.org/download/r8/osgi.core-8.0.0.pdf).

{{< /note >}}

## Installing Corda package files

To install a Corda package file, see [the corda-cli install command](../corda-cli/commands.md).
