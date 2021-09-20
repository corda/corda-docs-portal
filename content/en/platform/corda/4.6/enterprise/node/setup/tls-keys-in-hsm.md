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

A file-based `sslkeystore.jks` is still required to store TLS certificates, even if corresponding TLS keys are stored in CryptoService.

## Configuration example

`node.conf`:

```
enterpriseConfiguration = {
    tlsCryptoServiceConfig = {
       cryptoServiceName="AWS_CLOUD"
       cryptoServiceConf="aws_cloud.conf"
    }
}
```

## Migration notes

To migrate from a file-based node's TLS keystore to HSM:

1. Add a `tlsCryptoServiceConfig` section the node configuration file.
2. Renew the TLS certificate and keys, as described in  the [Renewing TLS certificates](../../ha-utilities.md#renewing-tls-certificates) section in [HA Utilities](../../ha-utilities.md).
