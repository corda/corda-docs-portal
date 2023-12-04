---
date: '2023-08-10'
version: 'Corda 5.1'
title: "crypto.extensions"
menu:
  corda51:
    identifier: corda51-api-crypto-extensions
    parent: corda51-api
    weight: 5050
section_menu: corda51
---
# net.corda.v5.crypto.extensions
The `corda-crypto-extensions` package of the `Corda Crypto API` defines low-level crypto capabilities that can be used to extend functionality of the Corda Crypto Library by implementing them in a {{< tooltip >}}CPK{{< /tooltip >}}. For more information, see the documentation for the package in the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/crypto/extensions/package-summary.html" target=" blank">Java API documentation</a>.

# Extending Supported Digest Algorithms

The Corda Crypto Library implements a wide variety of digest algorithms out of the box. However, you can use a digest algorithm that is not supported by the library by simply implementing some interfaces and adding the code into the CPK with the {{< tooltip >}}CorDapp{{< /tooltip >}} code. Corda picks up any custom algorithms at runtime. We recommend adding custom digest code in a separate Java module.

{{< note >}}
Digest algorithms must be cryptographically strong. For example, MD5 is not a strong algorithm and is therefore not supported by the library.
{{< /note >}}

Double SHA-256 is supported by the platform, but let us assume that you want to support Triple SHA-256 where the first pass calculates the message digest and subsequent passes calculate the digest of the previous pass result. The following sections show how to achieve this.

## TripleSha256Digest.kt
{{< tabs name="TripleSha256Digest">}}
{{% tab name="Kotlin" %}}
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
{{% /tab %}}
{{% tab name="Java" %}}
```java
package com.example.crypto;

import net.corda.v5.crypto.DigestAlgorithmName;
import net.corda.v5.crypto.extensions.DigestAlgorithm;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.io.InputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class TripleSha256Digest implements DigestAlgorithm {
    public static String ALGORITHM = "SHA-256-TRIPLE";
    public static int STREAM_BUFFER_SIZE = 8192;

    @NotNull
    @Override
    public String getAlgorithm() {
        return ALGORITHM;
    }

    @Override
    public int getDigestLength() {
        return 32;
    }

    @NotNull
    @Override
    public byte[] digest(@NotNull byte[] bytes) {
        try {
            return sha256Bytes(sha256Bytes(sha256Bytes(bytes)));
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    @NotNull
    @Override
    public byte[] digest(@NotNull InputStream inputStream) {
        try {
            MessageDigest messageDigest = MessageDigest.getInstance(DigestAlgorithmName.SHA2_256.getName());
            byte[] buffer = new byte[STREAM_BUFFER_SIZE];
            while (true) {
                int read = inputStream.read(buffer);
                if (read <= 0) break;
                messageDigest.update(buffer, 0, read);
            }
            return sha256Bytes(sha256Bytes(messageDigest.digest()));
        } catch (NoSuchAlgorithmException | IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static byte[] sha256Bytes(byte[] bytes) throws NoSuchAlgorithmException {
        return MessageDigest.getInstance(DigestAlgorithmName.SHA2_256.getName()).digest(bytes);
    }
}
```
{{% /tab %}}
{{< /tabs >}}

## TripleSha256.kt
{{< tabs name="TripleSha256">}}
{{% tab name="Kotlin" %}}
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
{{% /tab %}}
{{% tab name="Java" %}}
```java
package com.example.crypto;

import net.corda.v5.crypto.extensions.DigestAlgorithm;
import net.corda.v5.crypto.extensions.DigestAlgorithmFactory;
import org.jetbrains.annotations.NotNull;

public class TripleSha256 implements DigestAlgorithmFactory {

    @NotNull
    @Override
    public String getAlgorithm() {
        return TripleSha256Digest.ALGORITHM;
    }

    @NotNull
    @Override
    public DigestAlgorithm getInstance() {
        return new TripleSha256Digest();
    }
}
```
{{% /tab %}}
{{< /tabs >}}

## build.gradle
{{< tabs name="build">}}
{{% tab name="Kotlin" %}}
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
}
```
{{% /tab %}}
{{% tab name="Java" %}}
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
    cordaProvided 'net.corda:corda-crypto'
    cordaProvided 'net.corda:corda-crypto-extensions'
}
```
{{% /tab %}}
{{< /tabs >}}
{{< note >}}
You must reference `net.corda:corda-crypto-extensions`.
{{< /note >}}