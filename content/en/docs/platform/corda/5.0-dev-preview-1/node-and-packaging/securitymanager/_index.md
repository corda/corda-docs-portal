---
title: "Corda Security Manager"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-node-packaging
    weight: 500
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Documents the constraints imposed by the Corda Security Manager.
---
# Corda Security Manager

The Corda Security Manager is a platform component that prevents CPK (CorDapp Package) code from performing dangerous operations.

## Rationale

By default, Java and the OSGi framework do not impose any limitations on what actions CPK code can perform.

Since users control which CPKs they install (and in future versions of the platform, nodes will likely download CPKs
automatically from counterparties on the network), this means that we (R3) cannot inspect the CPK code to ensure it
does not perform dangerous operations. Users could choose to perform this inspection, but there is ample room for
error.

An example of a dangerous operation is a sandboxed CPK installing bundles outside of the sandbox.

The Corda Security Manager addresses this issue by limiting the operations CPK code can perform, making the platform
more secure.

## Background

The OSGi framework grants or denies code the permission to perform specific actions using the
[OSGi security layer](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.security.html). For example,
specific code can be granted the permission to read files using a `FilePermission`, or denied the ability to import a
given package using a `PackagePermission`.

## Installation and usage

The Corda Security Manager starts automatically upon node start. No user interaction is required.

## Impact

The Corda Security Manager leverages the OSGi security layer to deny the following permissions to all CPK bundles:

* `AdminPermission.LIFECYCLE` - required to install, update or uninstall bundles
* `AdminPermission.EXECUTE` - required to start, stop or modify the start level of bundles
* `AdminPermission.EXTENSIONLIFECYCLE` - as above, but for extension bundles
* `AdminPermission.RESOLVE` - required to resolve or refresh bundles

Any attempt by CPK code to perform one of the operations above will cause an `AccessControlException` to be thrown.

For example, the following flow will fail with an exception, because the permission to start a bundle is denied for
CPK code:

```
class IllegalFlow : Flow<Unit> {
    @Suspendable
    override fun call() {
        val thisBundle = FrameworkUtil.getBundle(this::class.java)
        thisBundle.start()
    }
}
```

Note that these permission restrictions are in addition to any permission restrictions that the bundle imposes on
itself via the `local permissions` mechanism described in section 50.11 of the
[OSGi specification](http://docs.osgi.org/download/r8/osgi.core-8.0.0.pdf).

## Implementation

We have enabled the security layer for the OSGi framework that Corda runs in.

The `CordaSecurityManager` is a component that is started automatically. It uses the
[`ConditionalPermissionAdmin` service](https://docs.osgi.org/specification/osgi.core/8.0.0/service.condpermadmin.html)
to deny the required permissions to any bundle in a location starting with the prefix "sandbox", which is where our
sandboxed bundles are installed. Code is also granted all other permissions.
