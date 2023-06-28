---
date: '2023-02-10'
version: 'Corda 5.0 Beta 4'
title: "net.corda.v5.crypto.extensions"
menu:
  corda5:
    identifier: corda5-api-crypto-extensions
    parent: corda5-api
    weight: 5050
section_menu: corda5
---
# net.corda.v5.crypto.extensions
The `corda-crypto-extensions` module of the `Corda Crypto API` defines low-level crypto capabilities that can be used to extend functionality of the Corda Crypto Library by implementing them in a CPK. 

# Extending Supported Digest Algorithms

The Corda Crypto Library implements a wide variety of digest algorithms out of the box. However, you can use a digest algorithm that is not supported by the library by simply implementing some interfaces and adding the code into the CPK with the CorDapp code. Corda picks up any custom algorithms at runtime. We recommend adding custom digest code in a separate Java module.

{{< note >}}
* Digest algorithms must be cryptographically strong. For example, MD5 is not a strong algorithm and so is not supported by the library.
* Custom algorithms cannot be used as an implicit part of the digital signing. For example, you cannot specify a signature specification such as 'SHA-256-TRIPLEwithRSA'. You must calculate the digest first and then sign/verify the produced hash using built-in signature specs.
{{< /note >}}

Double SHA-256 is supported by the platform but let us assume that you want to support Triple SHA-256 where the first pass calculates the message digest and subsequent passes calculate the digest of the previous pass result. The following sections show how to acheive this.

## TripleSha256Digest.kt

```kotlin
package com.example.crypto

import net.corda.v5.crypto.DigestAlgorithmName
import net.corda.v5.crypto.extensions.DigestAlgorithm
import java.io.InputStream
import java.security.MessageDigest

class TripleSha256Digest : DigestAlgorithm {
    companion object {
        const val ALGORITHM = "SHA-256-TRIPLE"
        const val STREAM_BUFFER_SIZE = DEFAULT_BUFFER_SIZE
    }

    override fun getAlgorithm() = ALGORITHM
    override fun getDigestLength() = 32
    override fun digest(bytes: ByteArray): ByteArray = bytes.sha256Bytes().sha256Bytes().sha256Bytes()
    override fun digest(inputStream: InputStream): ByteArray {
        val messageDigest = MessageDigest.getInstance(DigestAlgorithmName.SHA2_256.name)
        val buffer = ByteArray(STREAM_BUFFER_SIZE)
        while (true) {
            val read = inputStream.read(buffer)
            if (read <= 0) break
            messageDigest.update(buffer, 0, read)
        }
        return messageDigest.digest().sha256Bytes().sha256Bytes()
    }
}

private fun ByteArray.sha256Bytes(): ByteArray =
    MessageDigest.getInstance(DigestAlgorithmName.SHA2_256.name).digest(this)
```

## TripleSha256.kt

```kotlin
package com.example.crypto

import net.corda.v5.crypto.extensions.DigestAlgorithm
import net.corda.v5.crypto.extensions.DigestAlgorithmFactory

/**
 * This class should show up in the jar manifest
 */
class TripleSha256 : DigestAlgorithmFactory {
    override fun getAlgorithm() = TripleSha256Digest.ALGORITHM

    override fun getInstance(): DigestAlgorithm = TripleSha256Digest()
}
```

## build.gradle

```groovy
plugins {
    id 'org.jetbrains.kotlin.jvm'
    id 'net.corda.plugins.cordapp-cpk2'
}

description 'Corda Crypto Custom Digest One'

group 'com.example.crypto'

cordapp {
    targetPlatformVersion 999 as Integer
    workflow {
        name 'Custom Crypto Digest One CPK'
        versionId 1
        vendor 'R3'
    }
}

dependencies {
    cordaProvided platform("net.corda:corda-api:$cordaApiVersion")
    cordaProvided 'org.jetbrains.kotlin:kotlin-osgi-bundle'
    cordaProvided 'net.corda:corda-crypto'
    cordaProvided 'net.corda:corda-crypto-extensions'
    cordaProvided 'org.slf4j:slf4j-api'
}
```
{{< note >}}
You must reference `net.corda:corda-crypto-extensions`.
{{< /note >}}