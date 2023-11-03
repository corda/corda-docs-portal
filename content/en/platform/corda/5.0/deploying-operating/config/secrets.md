---
title: "Configuration Secrets"
version: 'Corda 5.0'
date: '2023-05-16'
menu:
  corda5:
    identifier: corda5-cluster-secrets
    parent: corda5-cluster-config
    weight: 3000
section_menu: corda5
---

# Configuration Secrets

The Corda configuration system allows for any string configuration value to be marked as “secret”. When this configuration value is used, Corda delegates the resolution of this value to one of the following configured secrets lookup service:

* [Default Secrets Service]({{< relref "#default-secrets-service">}})
* [External Secrets Service]({{< relref "#external-secrets-service">}}) {{< enterprise-icon >}}

{{< note >}}

* Any configuration items can be configured as secret or not. It is up to you to decide if a particular configuration item should be treated as secret.
* You can not use both Default Secrets Service encrypted secrets and Vault secret references in the same Corda configuration.

{{< /note >}}

## Default Secrets Service

Corda 5 provides a default secrets lookup service. Implementation of this service is in the form of a service that uses symmetric encryption so that the value can be stored encrypted at rest and decrypted with an Advanced Encryption Standard (AES) key derived from a configured salt and passphrase when needed. The salt and passphrase must be specified in the [deployment configuration]({{< relref "../deployment/deploying/_index.md#default-secrets-service" >}}).

For example, the following is a standard configuration:

```json
{
  "database": {
     "pass": "mypassword"
  }
}
```

You can specify the `pass` value as a secret using the `configSecret` value, as follows:

```json
{
  "database": {
     "pass": {
         "configSecret": {
           "encryptedSecret": "<encrypted-db-password>"
         }
     }
  }
}
```

You can use the {{< tooltip >}}Corda CLI{{< /tooltip >}} <a href = "../../reference/corda-cli/secret-config.md">`secret-config` command</a> to generate the configuration for an encrypted value.

## External Secrets Service {{< enterprise-icon >}}

Corda Enterprise supports integration with [HashiCorp Vault](https://www.vaultproject.io/) as an external secret management system. In particular, Corda targets the widely used [HashiCorp Vault kv](https://developer.hashicorp.com/vault/docs/secrets/kv) secrets engine. This is the recommended deployment configuration. The URL at which the Vault instance is reachable, the Vault token, and the path to Corda created secrets must be specified in the [deployment configuration]({{< relref "../deployment/deploying/_index.md#external-secrets-service" >}}).

For example, the following is a standard configuration:

```json
{
  "database": {
     "pass": "mypassword"
  }
}
```

You can specify `pass` as a secret in Vault, as follows:

```json
{
  "database": {
     "pass": {
         "configSecret": {
           "vaultPath": "<secret-path>",
           "vaultKey": "<secret-key>"
         }
     }
  }
}
```

You can use the Corda CLI <a href = "../../reference/corda-cli/secret-config.md">`secret-config` command</a> to generate the configuration for a value stored in Vault.

You can update a configuration value maintained in Vault in one of the following ways:

* Change the value in Vault. Corda caches configuration values for a short period of time. For this reason, you must handle changes so that old values remain valid for a short period of time to avoid downtime. For example, when changing database credentials, create the new credential before revoking the old one to guarantee a smooth transition.
* Add a new value in Vault, on a different path, and update the Corda configuration through the REST API. The relevant {{< tooltip >}}worker{{< /tooltip >}} processes will pick up this new value asynchronously.
