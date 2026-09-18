---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-14:
    identifier: corda-enterprise-4-14-corda-nodes-operating-hsm
    name: "Using an HSM with Corda Enterprise"
    parent: corda-enterprise-4-14-corda-nodes-operating
tags:
- cryptoservice
- configuration
title: Using an HSM with Corda Enterprise
weight: 2
---

# Using an HSM with Corda Enterprise

By default, the private keys that belong to the node CA, legal identity and TLS are stored in key store files in the node’s certificates
directory. Users may wish to instead store this key in a hardware security module (HSM) or similar.


See the [Hardware security modules (HSM)]({{< relref "../../platform-support-matrix.md#hardware-security-modules-hsm" >}})for supported HSMs and their features.

The cryptographic operations that are performed by the HSM are key generation and signing. The private key material is
stored in the HSM if the node is configured to use an HSM. The public keys are stored in the HSM (if configured for the node)
and the respective key stores, which is the node key store (`nodekeystore.jks`) for the node CA key (`nodeca`) and legal identity
(`identity-private-key`). The certificate chain is stored in the key store with a dummy private key as the Java API does not
allow to create an entry for a certificate chain without a private key. The certificate chain is not stored in the HSM.

{{< note >}}
The dummy private key entry does not contain any sensitive private key data.

{{< /note >}}

Operations involving the private keys (for example, signature generation) will be delegated by the node to the HSMs, while operations
involving the public keys (for example, signature verification) will be performed by the node.

A Corda node, including a notary node, must have its node CA and legal identity keys in the same key store or HSM.
Splitting these keys across a combination of different key stores and HSMs is not supported. TLS keys can be configured
either in the same key store/HSM, as node legal identity, or separately.

{{< note >}}
Importing existing keys from the file-based key store into a HSM is not supported.

{{< /note >}}

## Configuration

As mentioned in the description of the configuration file ([Node configuration]({{< relref "../setup/corda-configuration-file.md" >}})), the `node.conf` has three relevant fields:
* `cryptoServiceName`
* `cryptoServiceConf`
* Optional: `cryptoServiceTimeout`

If you do not add the `cryptoServiceTimeout` parameter, it defaults to 10000 milliseconds. You can increase it to mitigate the time-out error.

{{< warning >}}
The file containing the configuration for the HSM (referenced by the `cryptoServiceConf` field) contains sensitive information. For this reason, we strongly advise you to use the [Configuration Obfuscator]({{< relref "../../tools-config-obfuscator.md" >}}) tool.

{{< /warning >}}

Available configuration options for HSM usage are given below with information about storage and purpose of the keys:

{{< table >}}
|node.conf section |Certificate store |Stored keys |
|-------------------------|-------------------------|-------------------------|
|`cryptoServiceName` `cryptoServiceConf` |`nodekestore.jks` |Node CA and legal identity keys |
|`tlsCryptoServiceConfig` |`sslkeystore.jks` |Node TLS key without running Corda Firewall |
|`artemisCryptoServiceConfig` |As configured by `messagingServerSslConfiguration.sslKeystore` |TLS key for communications with the external Artemis server when running Corda Firewall |

{{< /table >}}

## Utimaco

Corda Enterprise nodes can be configured to store their legal identity keys in [Utimaco’s SecurityServer Se Gen2](https://hsm.utimaco.com/products-hardware-security-modules/general-purpose-hsm/securityserver-se-gen2/) running firmware version 4.21.1.

In the `node.conf`, the `cryptoServiceName` needs to be set to “UTIMACO”, and `cryptoServiceConf` should contain the path to the configuration for Utimaco, as shown below.

```kotlin
cryptoServiceName : "UTIMACO"
cryptoServiceConf : "utimaco.conf"
```

The configuration file for Utimaco has the fields described below. The entries are similar to the ones described in the documentation for the CryptoServer JCE provider, and you should refer to this documentation for more details. We cannot link to the documentation here, but you should have received a copy which contains the file `JCE-Documentation.html`.

* **host**:
address of the device or simulator.

* **port**:
port of the device or simulator.

* **connectionTimeout**:
(optional) timeout when establishing connection to the device, in milliseconds. The default is 30000.

* **keepSessionAlive**:
(optional) boolean, false by default. If set to false the connection to the device will terminate after 15 minutes. The node will attempt to automatically re-establish the connection.

* **keyGroup**:
The key group to be used when generating keys.

* **keySpecifier**:
The key specifier to be used when reading keys. The default is “*”.

* **keyOverride**:
(optional) boolean, the default is false.

* **keyExport**:
(optional) boolean, the default is false.

* **keyGenMechanism**:
the key generation mechanism to be used when generating keys.

* **authThreshold**:
(optional) integer, 1 by default.

* **username**:
the username.

* **password**:
the login password, or, if logging in with a key file, the password for the key file.

* **keyFile**:
(optional) key file for file-based log in.

Example configuration file:

```kotlin
host: "127.0.0.1"
port: 3001
connectionTimeout: 60000
keepSessionAlive: true
keyGroup: "*"
keySpecifier: 2
keyOverride: true
keyExport: false
keyGenMechanism: 4
authThreshold: 1
username: user
password: "my-password"
```

In addition to the configuration, the node needs to access binaries provided by Utimaco. The `CryptoServerJCE.jar` for release 4.21.1, which can be obtained from Utimaco, needs to be placed in the node’s `drivers` folder.

## Gemalto Luna

Corda Enterprise nodes can be configured to store their legal identity keys in [Gemalto Luna](https://safenet.gemalto.com/data-encryption/hardware-security-modules-hsms/safenet-network-hsm) HSMs running firmware version 7.0.3.

In the `node.conf`, the `cryptoServiceName` must set to “GEMALTO_LUNA”, and `cryptoServiceConf` should contain the path to a configuration file, the content of which is explained further down.

```kotlin
cryptoServiceName : "GEMALTO_LUNA"
cryptoServiceConf : "gemalto.conf"
```

The configuration file for Gemalto Luna has two fields. The `keyStore` field needs to specify a slot or partition. The `password` field contains the password associated with the slot or partition.

* **keyStore**:
specify the slot or partition.

* **password**:
the password associated with the slot or partition.

Example configuration file:

```kotlin
keyStore: "tokenlabel:my-partition"
password: "my-password"
```

In addition to the configuration, the Gemalto’s JCA provider (version 7.3) LunaProvider.jar needs to be placed in the node’s *drivers* folder if the node's keys are being stored on HSM.

## Futurex

Corda Enterprise nodes can be configured to store their legal identity keys in [Futurex Vectera Plus](https://www.futurex.com/products/vectera-series) HSMs running firmware version 6.1.5.8.

In the `node.conf`, the `cryptoServiceName` needs to be set to “FUTUREX”, and `cryptoServiceConf` should contain the path to a configuration file, the content of which is explained further down.

```kotlin
cryptoServiceName : "FUTUREX"
cryptoServiceConf : "futurex.conf"
```

The configuration file for Futurex has one field, `credentials` that contains the password (PIN) required to authenticate with the HSM.

Example configuration file:

```kotlin
credentials: "password"
```

When starting Corda the environment variables `FXPKCS11_CFG` and `FXPKCS11_MODULE` need to be set as detailed in Futurex’s documentation.
Corda must be running with the system property `java.library.path` pointing to the directory that contains the FutureX binaries (for example, `libfxjp11.so` for Linux).
Additionally, The JAR containing the Futurex JCA provider (version 3.1) must be put on the class path, or copied to the node’s `drivers` directory.
The following versions should be used for the required Futurex libraries: 3.1 for the PKCS#11 library and 1.17 for the Futurex JCA library.

## Azure Key Vault

There are two methods of authentication when using an Azure Key Vault:
 - Authentication using certificates.
 - Authentication using Azure Managed Identities.

### Authentication using certificates

In the `node.conf`, the `cryptoServiceName` needs to be set to "AZURE_KEY_VAULT" and `cryptoServiceConf` should contain the path to the configuration for Azure Key Vault, as shown below.

```kotlin
cryptoServiceName: "AZURE_KEY_VAULT"
cryptoServiceConf: "az_keyvault.conf"
```

The configuration file for Azure Key Vault contains the fields listed below. For details refer to the [Azure Key Vault documentation](https://docs.microsoft.com/en-gb/azure/key-vault).

* **path**:
The path to the key store for login. Note that the `.pem` file that belongs to your service principal must be created in the pkcs12 format. One way of doing this is by using openssl: `openssl pkcs12 -export -in /home/username/tmpdav8oje3.pem -out keyvault_login.p12`.

{{< note >}}
If a relative path is specified for the pkcs12 key store, it must be relative to the base directory of the running node, firewall or HA Utility.
{{< /note >}}

* **tenantId**:
alias of the key used for login.

* **password**:
password to the key store.

* **clientId**:
the client id for the login.

* **keyVaultURL**:
the URL of the key vault.

* **protection**:
If set to “HARDWARE”, ‘hard’ keys will be used, if set to “SOFTWARE”, ‘soft’ keys will be used [as described in the Azure Key Vault documentation](https://docs.microsoft.com/en-gb/azure/key-vault/about-keys-secrets-and-certificates#key-vault-keys).

Example configuration file:

```kotlin
path: keyvault_login.p12
password: "<password used in the key vault creation>"
clientId: "<app id from creation of the service principle>"
tenantId: "45ca2399-b7b3-7869-11ee-564aca9b634e"
keyVaultURL: "https://<key vault name>.vault.azure.net/"
protection: "SOFTWARE" # HARDWARE can be specified if using a premium vault
```

The drivers directory must contain a JAR file built by the gradle script below.

First copy the following text in to a new file called build.gradle anywhere on your file system.
Please do not change any of your existing build.gradle files.

```kotlin
plugins {
  id 'java'
  id 'com.github.johnrengelman.shadow' version '7.1.2'
}

repositories {
  mavenCentral()
}

dependencies {
  implementation 'com.azure:azure-security-keyvault-keys:4.2.3'
  implementation 'com.azure:azure-identity:1.2.0'
}

shadowJar {
  relocate 'okhttp3', 'shadow.okhttp3'
  archiveBaseName = 'azure-keyvault-with-deps.jar'
}
```

Then if gradle is on the path run the following command.

```kotlin
gradle shadowJar
```

or if gradle is not on the path but gradlew is in the current directory then run the following command.

```kotlin
./gradlew shadowJar
```

This will create a jar called azure-keyvault-with-deps.jar, copy this into the drivers directory.

### Authentication using Azure Managed Identities

If any of the parameters required for the certificate are not defined, or set to `null`, then the Azure Key Vault will use Azure Managed Identities.

The minimum configuration required for authentication using Azure Managed Identities is:

```
keyVaultURL="https://tck-test-vault.vault.azure.net
protection=SOFTWARE
```

To set up Azure Managed Identities, see the [Microsoft Azure Managed Identities documentation](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview).

## Securosys Primus X

Corda Enterprise nodes can be configured to store their legal identity keys in [Securosys Primus X](https://www.securosys.ch/product/high-availability-high-performance-hardware-security-module) HSMs running firmware version 2.7.4 or newer. Confidential identity keys can be used on Securosys PrimusX 2.8.5 or newer.

In the `node.conf`, the `cryptoServiceName` needs to be set to “PRIMUS_X”, and `cryptoServiceConf` should contain the path to a configuration file, the content of which is explained further down.

```kotlin
cryptoServiceName : "PRIMUS_X"
cryptoServiceConf : "primusx.conf"
```

The configuration file for Securosys Primus X has the following fields:

* **host**:
address of the device

* **port**:
port of the device

* **username**:
the username of the account

* **password**:
the login password of the account

Example configuration file:

```kotlin
host: "some-address.securosys.ch"
port: 2000
username: "my-username"
password: "my-password"
```

In addition to the configuration, the Securosys’ Primus X JCA provider (version 1.8.2 or newer) needs to be placed in the node’s `drivers` folder.

## nCipher nShield

Corda Enterprise nodes can be configured to generate keys in [nCipher nShield Connect](https://www.ncipher.com/products/general-purpose-hsms/nshield-connect) HSMs running firmware version 12.50.11.

Security World Software has to be installed and configured for use with nCipherKM JCA/JCE Cryptographic Service Provider (CSP), as described in the documentation for nShield.

In the `node.conf`, the `cryptoServiceName` needs to be set to “N_SHIELD”, and `cryptoServiceConf` should contain the path to a configuration file, the content of which is explained further down. The `cryptoServiceTimeout` needs to be increased to 10000 milliseconds to allow file-based keystore creation during initial node registration.

```kotlin
cryptoServiceName: "N_SHIELD"
cryptoServiceConf: "nshield.conf"
cryptoServiceTimeout: 10000
```

The configuration file for nShield HSM requires to specify path to `keyStore` file which is created during node registration and its `password`.

* **keyStore**:
path to the KeyStore data file, absolute or relative to cryptoServiceConf file path

* **password**:
password for KeyStore

Example configuration file:

```kotlin
keyStore: "certificates/keystore.nshield"
password: "my-password"
```

In addition to the configuration, the `nCipherKM.jar` needs to be placed in the node’s `drivers` folder.

Keys generated in HSM modules are stored in encrypted form (“key blob”) on the hard disk outside HSM, usually on the client side in Security World’s Key Management Data directory. In addition, nCipherKM JCA/JCE CSP creates KeyStore data files which are stored locally and separately from key blobs.

{{< note >}}
To use the generated keys on another host, you must copy or replicate KeyStore data file and the Security World’s Key Management Data directory, see nShield documentation for details. This may be necessary when registering nodes with standalone bridge using HA Utility.

{{< /note >}}
Module protection type is used for key generation and nCipherKM KeyStore instances.

{{< note >}}
The communication with the HSM is achieved via a daemon middleware process (called hardserver). If that process is restarted, the node also needs to be restarted to be able to communicate with the HSM. This can be done automatically by monitoring either that process or the node’s logs for CryptoService exceptions coming from operations with the HSM.
{{< /note >}}

## AWS CloudHSM

Corda Enterprise nodes can be configured to generate keys in [AWS CloudHSM](https://aws.amazon.com/cloudhsm/) using [AWS CloudHSM Software Library for Java](https://docs.aws.amazon.com/cloudhsm/latest/userguide/java-library.html).

{{< note >}}
See [Install and Use the AWS CloudHSM Software Library for Java](https://docs.aws.amazon.com/cloudhsm/latest/userguide/java-library-install.html) for the list of supported operating systems.
{{< /note >}}

In the ``node.conf``, the ``cryptoServiceName`` needs to be set to "AWS_CLOUD", and ``cryptoServiceConf`` should contain the path to a configuration file, the content of which is explained further down.

```text
cryptoServiceName : "AWS_CLOUD"
cryptoServiceConf : "aws_cloud.conf"
```

The configuration file for AWS CloudHSM has the following fields:

{{< table >}}
|key|value|
|---|-----|
|username| the name of CU user in HSM|
|password| the password for CU user|
|partition| HSM ID|
{{< /table >}}

Example configuration file:


```text
username:  "my-username"
password:  "my-password"
partition: "hsm-w4b6nnfio7z"
```


In addition to the configuration, the following steps are required:

1. `cloudhsm-3.1.2.jar` from AWS CloudHSM Software Library for Java needs to be placed in the node’s `drivers` folder.
2. Corda must be running with the system property `java.library.path` pointing to the directory that contains the AWS CloudHSM JCA provider binaries (for example, ``libcaviumjca.so`` for Linux). For example:
```text
java -Djava.library.path=/opt/cloudhsm/lib -jar corda.jar
```

## Azure Cloud HSM

Corda Enterprise nodes can be configured to generate keys in [Azure Cloud HSM](https://learn.microsoft.com/en-us/azure/cloud-hsm/overview) using the [Azure Cloud HSM Client SDK](https://github.com/microsoft/MicrosoftAzureCloudHSM) (tested with SDK version 2.0.2.5).

{{< note >}}
Unlike the other HSMs on this page, Azure Cloud HSM does not need a JCE/JCA driver JAR copied into the node's `drivers` folder. Corda talks to it directly through the JDK's own bundled PKCS11 support, so the only software prerequisite on the node's host is the Azure Cloud HSM Client SDK itself.
{{< /note >}}

Before starting the node, the Azure Cloud HSM Client SDK must be installed on the node's host, and its `azcloudhsm_client` daemon must be running and connected to the cluster - Corda's PKCS11 calls talk to this daemon over a local socket. If it is not running, the node fails to start with an error while loading the PKCS11 module (`Unable to load Azure Cloud HSM PKCS11 module at ...`).

{{< note >}}
The node already recovers automatically from an individual PKCS11 session going stale (for example, an idle timeout). A restart of the `azcloudhsm_client` daemon process itself is a different, more disruptive event: it severs every connection the node's PKCS11 module had open, and the node needs to be restarted to reconnect. This can be automated by monitoring either that process or the node's logs for CryptoService exceptions coming from operations with the HSM.
{{< /note >}}

{{< note >}}
Azure Cloud HSM support needs two extra JVM flags to access the JDK's own restricted PKCS11 bindings it's built on: `--add-modules=jdk.crypto.cryptoki` and `--add-exports=jdk.crypto.cryptoki/sun.security.pkcs11.wrapper=ALL-UNNAMED`. These are already included in the node capsule's own JVM arguments and applied automatically whenever you run `corda.jar` normally - no manual `java` flag is needed.
{{< /note >}}

In the `node.conf`, the `cryptoServiceName` needs to be set to "AZURE_CLOUD_HSM", and `cryptoServiceConf` should contain the path to a configuration file, the content of which is explained further down.

```kotlin
cryptoServiceName : "AZURE_CLOUD_HSM"
cryptoServiceConf : "azure_cloud_hsm.conf"
```

The configuration file for Azure Cloud HSM has the following fields:

{{< table >}}
|key|required|value|
|---|--------|-----|
|username|Yes|the name of the crypto user (CU) in the HSM|
|password|Yes|the password for the CU|
|partition|Yes|any distinguishing name for the HSM's partition. Corda does not send this value to the HSM - Azure Cloud HSM exposes exactly one logical partition per cluster, so there is nothing to select - it is only used to detect when two node configurations point at the same physical HSM. Microsoft's own [Azure Cloud HSM troubleshooting guide](https://learn.microsoft.com/en-us/azure/cloud-hsm/troubleshoot) uses `PARTITION_1` in its JCE login example.|
|wrapTransform|No|the AES key-wrap mechanism used when wrapping confidential identity keys - one of `KWP`, `LEGACY_PKCS5_PAD` or `CBC_PKCS5_PAD`. Defaults to `KWP` (real SP 800-38F KWP, FIPS-approved); the other two are available but are not FIPS-approved, and no Corda release has ever shipped wrapped keys under either of them. Each wrapped key remembers which transform it was wrapped under, so changing this setting only affects newly-wrapped keys - existing ones keep unwrapping correctly regardless.|
|libraryPath|No|absolute path to the Azure Cloud HSM PKCS11 library. Defaults to `/opt/azurecloudhsm/lib64/libazcloudhsm_pkcs11.so`, the SDK's standard install location.|
|requireTrustedWrappingKey|No|boolean, defaults to `true`. A CU session can never mark its own wrapping key `CKA_TRUSTED` - that requires a CO/SO session, set up out of band, to create the wrapping key object (under the alias Corda will use) before node registration runs. Set to `false` to let Corda generate and manage an ordinary, non-trusted wrapping key itself instead.|
{{< /table >}}

Example configuration file:

```kotlin
username:  "my-username"
password:  "my-password"
partition: "PARTITION_1"
```
