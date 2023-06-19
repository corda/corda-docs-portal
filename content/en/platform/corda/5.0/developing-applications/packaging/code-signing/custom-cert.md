---
date: '2023-05-18'
version: 'Corda 5.0 Beta 4'
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

However, you can configure the plugin to use a custom certificate using the `cordapp signing` section of the Gradle plugin:

{{< note >}}
When a custom certificate is used, it will need to be uploaded to the cluster using the
[/api/v1/certificates/cluster/code-signer API endpoint](../../../reference/rest-api/C5_OpenAPI.html#tag/Certificates-API/operation/put_certificates_cluster__usage_).
For example:
`curl -k -u admin:admin -X PUT -F alias="your-key" -F certificate=@your-key.pem https://localhost:8888/api/v1/certificates/cluster/code-signer`
{{< /note >}}

```
cordapp {
    ...

    signing {
        enabled = (true | false)
        options {
            alias = 'The alias to sign under'
            storePassword = 'Keystore password'
            keyStore = 'Keystore location'
            storeType= 'Keystore type (PKCS12 | JKS)'
            keyPassword = 'Password for private key (if different)'
            signatureFileName = '$alias'
            verbose = 'Verbose output when signing (true | false)'
            strict = 'Strict checking when signing (true | false)'
            internalSF = 'Include the .SF file inside the signature block (true | false)'
            sectionsOnly = 'Don't compute hash of entire manifest (true | false)'
            lazy = 'Flag to control whether the presence of a signature file means a JAR is signed (true | false)'
            maxMemory = 'Specifies the maximum memory the jarsigner JVM will use'
            preserveLastModified = 'Give the signed files the same last modified time as the original jar files (true | false)'
            tsaUrl = 'Timestamp server URL'
            tsaCert = 'Alias in the keystore for a timestamp authority for timestamped JAR files in Java 5+'
            tsaProxyHost = 'TSA proxy server'
            tsaProxyPort = 'TSA proxy server port'
            executable = 'Path to alternate jarsigner'
            force = 'Force signing of the JAR file even if it doesn't seem to be out of date or already signed (true | false)'
            signatureAlgorithm = 'Name of the signature algorithm'
            digestAlgorithm = 'Name of the digest algorithm	'
            tsaDigestAlgorithm = 'Name of the TSA digest algorithm'
        }
    }
}
```
