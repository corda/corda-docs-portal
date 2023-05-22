---
date: '2023-05-18'
version: 'Corda 5.0'
title: "Signing Packages with a Custom Certificate"
menu:
  corda5:
    parent: corda5-develop-packaging-code-signing
    identifier: corda5-develop-packaging-code-signing-custom-cert
    weight: 1000
section_menu: corda5
---

# Signing Packages with a Custom Certificate

As described in [Build a CPB]({{< relref "../cpb.md" >}}) and [Build a CPK]({{< relref "../cpk.md" >}}), the Gradle plugin uses, by default,
a development certificate to sign a CPB or CPK package.

However, you can configure the plugin to use a custom certificate using the `cordapp` `signing` section of the Gradle plugin:

{{< note >}}
When a custom certificate is used, it will need to be uploaded to the cluster using the /api/v1/certificates/cluster/code-signer API endpoint [insert link].
For example:
`curl --insecure -u admin:admin -X PUT -F alias="your-key" -F certificate=@your-key.pem https://localhost:8888/api/v1/certificates/cluster/code-signer`
{{< /note >}}

```
cordapp {
    ...

    signing {
        enabled = (true | false)
        options {
            alias = '??'
            storePassword = '??'
            keyStore = file('/path/to/keystore')
            storeType= ('PKCS12' | 'JKS')
            keyPassword = '$storePassword'
            signatureFileName = '$alias'
            verbose = (true | false)
            strict = (true | false)
            internalSF = (true | false)
            sectionsOnly = (true | false)
            lazy = (true | false)
            maxMemory = '??'
            preserveLastModified = (true | false)
            tsaUrl = '??'
            tsaCert = '??'
            tsaProxyHost = '??'
            tsaProxyPort = '??'
            executable = file('/path/to/alternate/jarsigner')
            force = (true | false)
            signatureAlgorithm = '??'
            digestAlgorithm = '??'
            tsaDigestAlgorithm = '??'
        }
    }
}
```
