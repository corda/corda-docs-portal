---
aliases:
- /releases/4.0/cryptoservice-configuration.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- cryptoservice
- configuration
title: HSM support for legal identity keys
---


# HSM support for legal identity keys

By default, the private keys that belong to the node CA and legal identity are stored in a key store file in the node’s certificates directory. Users may wish to instead store this key in a hardware security module (HSM) or similar. For this purpose, Corda Enterprise supports HSMs by [Utimaco](https://hsm.utimaco.com), [Gemalto](https://www.gemalto.com), and [Azure KeyVault](https://azure.microsoft.com/en-gb/services/key-vault).

Note that only the private and public key of node CA and the legal identity are stored this way. The certificate chain is still stored in a file-based key store.



## Configuration

As mentioned in the description of the configuration file ([Node configuration](corda-configuration-file.md)), the `node.conf` has two relevant fields, `cryptoServiceName` and `cryptoServiceConf`.


{{< warning >}}
The file containing the configuration for the HSM (referenced by the `cryptoServiceConf` field) contains sensitive information. So, we strongly advise using the Configuration Obfuscator tool for it, as documented here: [Configuration Obfuscator](tools-config-obfuscator.md)

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

In addition to the configuration, the node needs to access binaries provided by Utimaco. The `CryptoServerJCE.jar` for release 4.21.1, which can be obtained from Utimaco, needs to be placed in the node’s drivers folder.


## Gemalto Luna

Corda Enterprise nodes can be configured to store their legal identity keys in [Gemalto Luna](https://safenet.gemalto.com/data-encryption/hardware-security-modules-hsms/safenet-network-hsm) HSMs running firmware version 7.3.

In the `node.conf`, the `cryptoServiceName` needs to be set to “GEMALTO_LUNA”, and `cryptoServiceConf` should contain the path to a configuration file, the content of which is explained further down.

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

Note that the Gemalto’s JCA provider has to be installed as described in the documentation for the Gemalto Luna.


## Azure KeyVault

In the `node.conf`, the `cryptoServiceName` needs to be set to “AZURE_KEY_VAULT” and `cryptoServiceConf` should cointain the path to the configuration for Azure KeyVault, as shown below.

```kotlin
cryptoServiceName: "AZURE_KEY_VAULT"
cryptoServiceConf: "az_keyvault.conf"
```

The configuration file for Azure KeyVault contains the fields listed below. For details refer to the [Azure KeyVault documentation](https://docs.microsoft.com/en-gb/azure/key-vault).


* **path**: 
path to the key store for login. Note that the .pem file that belongs to your service principal needs to be created to pkcs12. One way of doing this is by using openssl: `openssl pkcs12 -export -in /home/username/tmpdav8oje3.pem -out keyvault_login.p12`.


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

