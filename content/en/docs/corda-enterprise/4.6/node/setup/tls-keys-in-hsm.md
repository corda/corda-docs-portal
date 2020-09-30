---
date: '2020-05-03T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-configuring
tags:
- hsm
- tls
- keys
title: Storing node TLS keys in HSM without running the Corda Enterprise Firewall
weight: 40
---

# Storing node TLS keys in HSM without running the Corda Enterprise Firewall

You can store node TLS keys in HSM by using the optional `tlsCryptoServiceConfig` and `tlsKeyAlias` configuration fields in the `enterpriseConfiguration` [configuration block](corda-configuration-fields.md#enterpriseConfiguration) of the [node configuration file](corda-configuration-file.md).

## Configuration

### Configuration fields in `node.conf`

* `tlsCryptoServiceConfig` is an optional crypto service configuration to store node's TLS private key in HSM. If this option is missing, the TLS private key will be stored in the file-based `sslkeystore.jks`. Parameters:
  * `cryptoServiceName`: the name of the CryptoService provider to be used.
  * `cryptoServiceConf`: the path to the configuration file for the CryptoService provider.

* `tlsKeyAlias` is the alias of the TLS key. It can consist of up to 100 lowercase alphanumeric characters and the hyphen (-). Default value: `cordaclienttls`.


### Related configuration options

You should also consider the following related configuration options in the node configuration file, as follows:

* `messagingServerSslConfiguration`: TLS configuration used to connect to external P2P Artemis message server. Required when `messagingServerExternal` = `true`. Also, it can be optionally used with embedded Artemis when external Bridge is configured.

* `artemisCryptoServiceConfig`: an optional crypto service configuration which will be used for HSM TLS signing when interacting with the Artemis message server. This option only makes sense when `messagingServerSslConfiguration` is specified: either to connect to a standalone Artemis messaging server, or when external Bridge is configured. If this option is missing, the local file system will be used to store private keys inside JKS key stores, as defined by `messagingServerSslConfiguration`.

* `messagingServerConnectionConfiguration`, `messagingServerBackupAddresses`, and `artemisCryptoServiceConfig` must be inside the `enterpriseConfiguration` section, but not inside `messagingServerSslConfiguration`.

### HA Utilities and self-signed internal Artemis SSL keystore

The HA Utilities tool produces the following files:

* `artemisbridge.jks`: used by the standalone bridge. The path to this file should be specified in the `artemisSSLConfiguration` section in `firewall.conf`.
* `artemisnode.jks`: optionally used by the node. When used, the path to this file should be specified in the `messagingServerSslConfiguration` section in `node.conf`.
* `artemis.jks`: used by the standalone P2P Artemis broker.
* `artemis-truststore.jks`: must be placed together with any of the above keystore files.

### Storing TLS certificates in HSM

A file-based keystore is still required to store TLS certificates, even if corresponding TLS keys are stored in CryptoService.

{{< table >}}

| CryptoService config       | Certificate store|
|:---------------------------|:----------------|
| tlsCryptoServiceConfig     | sslkeystore.jks|
| artemisCryptoServiceConfig | as configured by `messagingServerSslConfiguration.sslKeystore`|

{{< /table >}}

## Changes in Corda Enterprise 4.6

### Using external bridge and embedded Artemis

The TLS keystore used by the node for P2P connections in Corda Enterprise 4.6 has been changed for configuration with external bridge and embedded Artemis. Prior to Corda Enterprise 4.6, `sslkeystore.jks` was used at all times; from Corda Enterprise 4.6, `messagingServerSslConfiguration.sslKeystore` is used if configured, otherwise `sslkeystore.jks` is used as before.

This change allows for configuring different Artemis TLS keys for the node and the bridge when using HSM. The table below shows what options are supported in HSM:

{{< table >}}
| Artemis | Bridge | HSM support | Keystore|
|:--------|:-------|:------------|:----------|
| in      | in     | yes | `sslkeystore.jks`|
| out     | out    | yes | as configured by `messagingServerSslConfiguration`|
| in      | out    | no | `sslkeystore.jks` - if `messagingServerSslConfiguration` is not specified|
| in      | out    | yes | as configured by `messagingServerSslConfiguration` (if present)|
| out     | in     | - | not supported|

{{< /table >}}

### Strict check for `messagingServerSslConfiguration`

Prior to Corda Enterprise 4.6, `messagingServerSslConfiguration` was required `if (messagingServerExternal && messagingServerAddress != null)`; from Corda Enterprise 4.6, `messagingServerSslConfiguration` is unconditionally required for external Artemis (`messagingServerExternal` != `null`).

### sslkeystore.jks is not always required

Prior to Corda Enterprise 4.6, the node was unable to start without `sslkeystore.jks`, even if this keystore was not used - for example, with external bridge and external Artemis; from Corda Enterprise 4.6, if `messagingServerSslConfiguration` is used for Artemis authentication, the node can be started without sslkeystore.jks. In this case, node's TLS key and certificate are only used by the bridge.

## Configuration examples

### All-in-one node with TLS keys in HSM

`node.conf`:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
enterpriseConfiguration = {
    tlsCryptoServiceConfig = {
       cryptoServiceName="AWS_CLOUD"
       cryptoServiceConf="aws_cloud.conf"
    }
}
```
{{% /tab %}}
{{< /tabs >}}

### External bridge + embedded Artemis: simple configuration without HSM

`node.conf`:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
messagingServerAddress = "172.31.15.60:11005"
messagingServerExternal = false
enterpriseConfiguration = {
    externalBridge = true
}
```
{{% /tab %}}
{{< /tabs >}}


`firewall.conf`:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
outboundConfig {
    artemisBrokerAddress = "172.31.15.60:11005"
}
```
{{% /tab %}}
{{< /tabs >}}

### External bridge + embedded Artemis: HSM for Artemis keys

`node.conf`:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
messagingServerAddress = "172.31.15.60:11005"
messagingServerExternal = false
enterpriseConfiguration = {
    externalBridge = true
    messagingServerSslConfiguration {
        sslKeystore = "artemiscerts/artemisnode.jks"
        keyStorePassword = "cordacadevpass"
        trustStoreFile = "artemiscerts/artemis-truststore.jks"
        trustStorePassword = "trustpass"
    }
    artemisCryptoServiceConfig = {
        cryptoServiceName = AWS_CLOUD
        cryptoServiceConf = awshsm.conf
    }
}
```
{{% /tab %}}
{{< /tabs >}}

`firewall.conf`:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
outboundConfig {
    artemisBrokerAddress = "172.31.15.60:11005"
    artemisSSLConfiguration {
        sslKeystore = "artemiscerts/artemisbridge.jks"
        keyStorePassword = "cordacadevpass"
        trustStoreFile = "artemiscerts/artemis-truststore.jks"
        trustStorePassword = "trustpass"
    }
}
artemisCryptoServiceConfig {
   name = AWS_CLOUD
   conf = awshsm.conf
}
```
{{% /tab %}}
{{< /tabs >}}

## Migration notes

To migrate from a file-based node's TLS keystore to HSM:

1. Add a `tlsCryptoServiceConfig` section the node configuration file.
2. Renew the TLS certificate and keys, as described in  the [Renewing TLS certificates](../../ha-utilities.md#renewing-tls-certificates) section in [HA Utilities](../../ha-utilities.md).
