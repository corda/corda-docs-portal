---
title: "Corda Enterprise Release notes"
date: 2020-01-08T09:59:25Z
---


# Corda Enterprise Release notes

## Corda Enterprise 4.4
This release extends the [Corda Enterprise 4.3 release](https://docs.corda.r3.com/releases/4.3/release-notes-enterprise.html)
                with

Corda Enterprise 4.4 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. Please refer to product documentation for details.

Corda Enterprise 4.4 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.3, 4.2, 4.1, 4.0 and 3.x, while providing enterprise-grade features and performance.


{{< note >}}
The compatibility and interoperability assurances apply to nodes running at the latest patch level for any given integer version.
                    For example, at the time of writing, the Corda Enterprise 4.4 interoperability and compatibility assurance is with respect to Corda 3.4, Corda Enterprise 3.3, Corda 4.1, Corda Enterprise 4.0 and Corda Enterprise 4.1.


{{< /note >}}

### Key new features and components

#### Further Hardware Security Module (HSM) support
> 
> This release adds support for storing the node’s CA and legal identity key in a [nCipher nShield Connect](https://www.ncipher.com/products/general-purpose-hsms/nshield-connect) HSM.
>                             Please refer to the associated section of the cryptoservice-configuration page for more details.


#### Corda Open Core
> 
> Starting with Corda Enterprise 4.4, Corda Enterprise and Open Source will share the same core and API libraries - the Enterprise version
>                             will have a binary dependency on the matching Open Source release. This will reduce the maintenance overhead, and improve API compatibility
>                             and interoperability between the Open Source and Enterprise versions.


### Known issues

### Upgrade notes
As per previous major releases, we have provided a comprehensive upgrade notes ([Upgrading CorDapps to Corda Enterprise 4.4]({{< relref "app-upgrade-notes-enterprise" >}})) to ease the upgrade
                    of CorDapps to Corda Enterprise 4.4. In line with our commitment to API stability, code level changes are fairly minimal.

For **developers**, switching CorDapps built using Corda (open source) 4.x to Corda Enterprise 4.4 is mostly effortless,
                    and simply requires making the Corda Enterprise binaries available to Gradle, and changing two variables in the build file:

```shell
ext.corda_release_version = '4.4'
ext.corda_release_distribution = 'com.r3.corda'
```

