---
aliases:
- /releases/3.0/upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-upgrade-notes
    parent: corda-enterprise-3-0-building-a-cordapp-index
    weight: 1030
tags:
- upgrade
- notes
title: Upgrading a CorDapp to a new platform version
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Upgrading a CorDapp to a new platform version

These notes provide instructions for upgrading your CorDapps from previous versions of Corda to version Corda Enterprise 3.0.



## Upgrading from Corda Open Source

A prerequisite to upgrade to Corda Enterprise 3.0 is to ensure your CorDapp is upgraded to Open Source Corda 3.x.
Please follow the instructions in [Corda V3.1 upgrade notes](https://docs.corda.net/releases/release-V3.1/upgrade-notes.html#v3-0-to-v3-1)
and [Corda V3.0 upgrade notes](https://docs.corda.net/releases/release-V3.0/upgrade-notes.html#v2-0-to-v3-0) section to complete this initial step.

{{< note >}}
There is no requirement to upgrade your CorDapp to Corda Enterprise in order to run it on Corda Enterprise. If
you wish your CorDapp to be compatible with nodes running Open Source, then compiling against Open Source Corda V3.x
will suffice.

{{< /note >}}
Upgrading to Corda Enterprise 3.0 from Open Source 3.x requires updating build file properties. For Gradle:

```kotlin
shell

ext.corda_release_distribution = 'com.r3.corda'
ext.corda_release_version = '3.0'
ext.corda_gradle_plugins_version = '4.0.25'
```


and specifying an additional repository entry to point to the location of the Corda Enterprise distribution. As an example:

```shell
repositories {
    maven {
        credentials {
            username "username"
            password "XXXXX"
        }
        url 'https://artifactory.mycompany.com/artifactory/corda-enterprise'
    }
}
```

{{< note >}}
Corda Enterprise 3.0 binaries are not available in a public repository. In order to make the dependencies available for development, either create a mirror repository and upload them there, or add them to the local Maven repository.

{{< /note >}}
{{< note >}}
While the Corda Gradle Plugins need no changes apart from the version, ensure that Corda Enterprise dependencies are referenced with the right distribution. As an example:

{{< /note >}}
```shell
    cordaCompile "net.corda:corda-core:$corda_release_version"

becomes:

.. sourcecode:: shell

    cordaCompile "$corda_release_distribution:corda-core:$corda_release_version"
```

Corda Enterprise 3.0 uses Kotlin API and language version 1.2. The specifics are

```shell
ext.kotlin_version = '1.2.50'
```

{{< note >}}
Explicit overriding of properties *ext.quasar_group* and *ext.quasar_version* is not necessary anymore for CorDapps depending on the *quasar-utils* plugin. You can remove these two lines from which ever file.

{{< /note >}}

### Certificate Revocation List (CRL) support

The newly added feature of certificate revocation (see [Certificate Revocation List](certificate-revocation.md)) introduces a few changes to the node configuration.
In the configuration file it is required to explicitly specify how strictly the node should apply the CRL check. For that purpose the *crlCheckSoftFail*
parameter is now expected to be set explicitly in the node’s SSL configuration.
Setting the *crlCheckSoftFail* to true, relaxes the CRL checking policy. In this mode, the SSL communication
will fail only when the certificate revocation status can be checked and the certificate is revoked. Otherwise it will succeed.
If *crlCheckSoftFail* is false, then an SSL failure can occur if the certificate revocation status cannot be checked (e.g. due to a network failure), as well as when
a certificate is revoked.

Older versions of Corda do not have CRL distribution points embedded in the SSL certificates.
As such, in order to be able to reuse node and SSL certificates generated in those versions of Corda, the *crlCheckSoftFail* needs
to be set to true.

{{< note >}}
Mitigation of this issue and thus being able to use the *strict* mode (i.e. with *crlCheckSoftFail* = false)
of the CRL checking with the certificates generated in previous versions of Corda is going to be added in the near future.

{{< /note >}}

## Upgrading from Corda Enterprise 3.0 Developer Preview 3.0

A limited distribution preview of Corda Enterprise 3.0 was made available to a small number of users. If your app uses this version, here are some specific notes on how to upgrade to the Generally Available release:


* Update versions in your build files, for Gradle, as an example:

```kotlin
shell

ext.corda_release_version = '3.0'
ext.corda_gradle_plugins_version = '4.0.25'
ext.kotlin_version = '1.2.50'
```


{{< note >}}
Explicit overriding of properties *ext.quasar_group* and *ext.quasar_version* is not necessary anymore for CorDapps depending on the *quasar-utils* plugin. You can remove these two lines from which ever file.{{< /note >}}

* For CorDapps depending on the *cordapp-plugin*, version *4.0.25* allows specifying distribution information. As an example:{{< note >}}
Properties *name* and *version* of a CorDapp’s distribution information are derived automatically by the *cordapp-plugin* if not provided. The *vendor* property should be provided explicitly. A warning is raised by Corda Enterprise nodes for CorDapps that do not specify the *vendor* property.{{< /note >}}



### Certificate Revocation List (CRL) support

The newly added feature of certificate revocation (see [Certificate Revocation List](certificate-revocation.md)) introduces a few changes to the node configuration.
In the configuration file it is required to explicitly specify how strictly the node should apply the CRL check. For that purpose the *crlCheckSoftFail*
parameter is now expected to be set explicitly in the node’s SSL configuration.
Setting the *crlCheckSoftFail* to true, relaxes the CRL checking policy. In this mode, the SSL communication
will fail only when the certificate revocation status can be checked and the certificate is revoked. Otherwise it will succeed.
If *crlCheckSoftFail* is false, then an SSL failure can occur if the certificate revocation status cannot be checked (e.g. due to a network failure), as well as when
a certificate is revoked.

Older versions of Corda do not have CRL distribution points embedded in the SSL certificates.
As such, in order to be able to reuse node and SSL certificates generated in those versions of Corda, the *crlCheckSoftFail* needs
to be set to true.

{{< note >}}
Mitigation of this issue and thus being able to use the *strict* mode (i.e. with *crlCheckSoftFail* = false)
of the CRL checking with the certificates generated in previous versions of Corda is going to be added in the near future.

{{< /note >}}
