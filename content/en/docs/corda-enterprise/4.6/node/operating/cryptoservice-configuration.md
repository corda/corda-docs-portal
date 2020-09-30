---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-corda-nodes-operating-hsm
    name: "Using an HSM with Corda Enterprise"
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- cryptoservice
- configuration
title: Using an HSM with Corda Enterprise
weight: 2
---

# Using an HSM with Corda Enterprise

By default, the private keys that belong to the node CA and legal identity are stored in a key store file in the node’s certificates
directory. Users may wish to instead store this key in a hardware security module (HSM) or similar.

See the [Hardware Security Modules (HSM)](../../platform-support-matrix.md#supported-hsms) for supported HSMs and their features.

The cryptographic operations that are performed by the HSM are key generation and signing. The private key material is stored in the HSM if the node is configured to use an HSM. The public keys are stored in the HSM (if configured for the node) and the respective key stores, which is the node key store (nodekeystore.jks) for the node CA key (nodeca) and legal identity (identity-private-key). The certificate chain is stored there as well. The certificate chain is not stored in the HSM.

Operations involving the private keys (e.g. signature generation) will be delegated by the node to the HSMs, while operations involving the public keys (e.g. signature verification) will be performed by the node.

A Corda node, including a notary node, must have all its keys in the same keystore or HSM.
Splitting the keys across a combination of different keystores and HSMs is not supported.

{{< note >}}
Importing existing keys from the file-based keystore into a HSM is not supported.

{{< /note >}}

## Configuration

As mentioned in the description of the configuration file (corda-configuration-file), the `node.conf` has two relevant fields, `cryptoServiceName` and `cryptoServiceConf`.

{{< warning >}}
The file containing the configuration for the HSM (referenced by the `cryptoServiceConf` field) contains sensitive information. So, we strongly advise using the Configuration Obfuscator tool for it, as documented here: tools-config-obfuscator

{{< /warning >}}

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

Note that the Gemalto’s JCA provider (version 7.3) has to be installed as described in the documentation for the Gemalto Luna.

## Futurex

Corda Enterprise nodes can be configured to store their legal identity keys in [FutureX Vectera Plus](https://www.futurex.com/products/vectera-series) HSMs running firmware version 6.1.5.8.

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
Corda must be running with the system property `java.library.path` pointing to the directory that contains the FutureX binaries (e.g. `libfxjp11.so` for Linux).
Additionaly, The JAR containing the Futurex JCA provider (version 3.1) must be put on the class path, or copied to the node’s `drivers` directory.
The following versions should be used for the required FutureX libraries: 3.1 for the PKCS#11 library and 1.17 for the FutureX JCA library.

## Azure KeyVault

In the `node.conf`, the `cryptoServiceName` needs to be set to “AZURE_KEY_VAULT” and `cryptoServiceConf` should contain the path to the configuration for Azure KeyVault, as shown below.

```kotlin
cryptoServiceName: "AZURE_KEY_VAULT"
cryptoServiceConf: "az_keyvault.conf"
```

The configuration file for Azure KeyVault contains the fields listed below. For details refer to the [Azure KeyVault documentation](https://docs.microsoft.com/en-gb/azure/key-vault).

* **path**:
path to the key store for login. Note that the .pem file that belongs to your service principal needs to be created to pkcs12. One way of doing this is by using openssl: `openssl pkcs12 -export -in /home/username/tmpdav8oje3.pem -out keyvault_login.p12`.

{{< note >}}
If a relative path is specified for the pkcs12 key store, it must be relative to the base directory of the running node, firewall or HA Utility.

{{< /note >}}

* **alias**:
alias of the key used for login.

* **password**:
password to the key store.

* **clientId**:
the client id for the login.

* **keyVaultURL**:
the URL of the key vault.

* **protection**:
If set to “HARDWARE”, ‘hard’ keys will be used, if set to “SOFTWARE”, ‘soft’ keys will be used [as described in the Azure KeyVault documentation](https://docs.microsoft.com/en-gb/azure/key-vault/about-keys-secrets-and-certificates#key-vault-keys).

Example configuration file:

```kotlin
path: keyvault_login.p12
alias: "my-alias"
password: "my-password"
keyVaultURL: "[https:/](https:/)/<mykeyvault>.vault.azure.net/"
clientId: "a3d72387-egfa-4bc2-9cba-b0b27c63540e"
protection: "HARDWARE"
```

The drivers directory needs to contain an uber jar, built by the gradle script below.

First copy the following text in to a new file called build.gradle anywhere on your file system.
Please do not change any of your existing build.gradle files.

```kotlin
plugins {
  id 'com.github.johnrengelman.shadow' version '5.1.0'
  id 'java'
}

repositories {
    jcenter()
}

dependencies {
    compile 'com.microsoft.azure:azure-keyvault:1.2.1'
    compile 'com.microsoft.azure:adal4j:1.6.4'
}

shadowJar {
    relocate 'okhttp3', 'shadow.okhttp3'
    archiveName = 'azure-keyvault-with-deps.jar'
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

Note that okhttp3 needs to be shaded as the latest version of this library will raise an exception on a handle leak which version 1.2.1
of azure key vault has. For further details see [https://github.com/Azure/azure-sdk-for-java/issues/4879](https://github.com/Azure/azure-sdk-for-java/issues/4879)

## Securosys Primus X

Corda Enterprise nodes can be configured to store their legal identity keys in [Securosys Primus X](https://www.securosys.ch/product/high-availability-high-performance-hardware-security-module) HSMs running firmware version 2.7.4.

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

In addition to the configuration, the Securosys’ Primus X JCA provider (version 1.8.2) needs to be placed in the node’s `drivers` folder.

## nCipher nShield

Corda Enterprise nodes can be configured to generate keys in [nCipher nShield Connect](https://www.ncipher.com/products/general-purpose-hsms/nshield-connect) HSMs running firmware version 12.50.11.

Security World Software has to be installed and configured for use with nCipherKM JCA/JCE Cryptographic Service Provider (CSP), as described in the documentation for nShield.

In the `node.conf`, the `cryptoServiceName` needs to be set to “N_SHIELD”, and `cryptoServiceConf` should contain the path to a configuration file, the content of which is explained further down. The `cryptoServiceTimeout` needs to be increased to 10 seconds to allow file-based keystore creation during initial node registration.

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

1. `cloudhsm-3.0.0.jar` from AWS CloudHSM Software Library for Java needs to be placed in the node’s `drivers` folder.
2. Corda must be running with the system property `java.library.path` pointing to the directory that contains the AWS CloudHSM JCA provider binaries (e.g. ``libcaviumjca.so`` for Linux). For example:
```text
java -Djava.library.path=/opt/cloudhsm/lib -jar corda.jar
```
