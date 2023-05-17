---
title: "Configuration Secrets"
date: '2023-05-16'
menu:
  corda5:
    identifier: corda5-cluster-secrets
    parent: corda5-cluster-config
    weight: 3000
section_menu: corda5
---

The Corda configuration system allows for any string configuration value to be marked as “secret”. When this configuration value is used, Corda delegates the resolution of this value to one of the following configured secrets lookup service:
* [Default Secrets Service]({{< relref "#default-secrets-service">}})
* [External Secrets Service]({{< relref "#external-secrets-service-hahahugoshortcode-s6-hbhb">}}) {{< enterprise-icon >}}

{{< note >}}
Any configuration items can be configured as sensitive or not. It is up to you to decide if a particular configuration item should be treated as sensitive.
{{< /note >}}

## Default Secrets Service

Corda 5 provides a default secrets lookup service. Implementation of this service is in the form of a service that uses symmetric encryption so that the value can be stored encrypted at rest and decrypted with a key derived from a configured salt and passphrase when needed. The salt and passphrase must be specified in the [deployment configuration]({{< relref "../deploying/deploying.md#default-secrets-service" >}}).

For example, the following is a standard configuration:

```
{
  "user": "name",
  "pass": "mypassword"
}
```

You can specify the `pass` value as a secret using the `configSecret` value, as follows:

```
{
  "user": "name",
  "pass": {
    "configSecret": {
      "encryptedSecret": "<encrypted-password>"
    } 
  }
}
```

You can use the Corda CLI <a href = "../../reference/corda-cli/secret-config.md">`secret-config` command</a> to generate the configuration for an encrypted value.

You can also use the default secrets lookup service with deployment configurations by using the `configSecret.encryptedSecret` prefix. For example:

```
-ddatabase.user=db-user
-ddatabase.pass.configSecret.encryptedSecret=<encryped-db-password>
-ddatabase.jdbc.url=jdbc:postgresql://db-address:5432/cordacluster
-ddatabase.jdbc.directory=/opt/corda/drivers
```

For more information about manually specifying the database deployment configuration, see [Manual Bootstrapping]({{< relref "../deploying/bootstrapping.md#database" >}}).

## External Secrets Service {{< enterprise-icon >}}

In some instances, the default secrets lookup service may not be sufficient. For example, in the case of [Database Connection Configuration]({{< relref "./database-connection.md#configuration-database" >}}), the salt and passphrase used for the encryption would be present in the same set of start-up parameters as the configuration that may be sensitive. This may be adequate if you can ensure that these start-up parameters are sufficiently protected. However, in other cases, it may be preferable to manage these credentials outside Corda.

Corda Enterprise supports integration with [HashiCorp Vault](https://www.vaultproject.io/) as an external secret management system. The URL at which the Vault instance is reachable, the Vault token, and the path to corda created secrets must be specified in the [deployment configuration]({{< relref "../deploying/bootstrapping.md#external-secrets-service" >}}).

For example, the following is a standard configuration:

```
{
  "user": "name",
  "pass": "123password"
}
```

You can specify `pass` as a secret, as follows:

```
{
  "user": "name",
  "pass": {
    "configSecret": {
      "vaultPath": "<secret-path>",
      "vaultKey": "<secret-key>"
    } 
  }
}
```

You can use the Corda CLI <a href = "../../reference/corda-cli/secret-config.md">`secret-config` command</a> to generate the configuration for a value stored in Vault.

You can update a configuration value mantained in Vault in one of the following ways:
* Change the value in Vault. Corda caches configuration values for a short period of time. For this reason, you must handle changes so that old values remain valid for a short period of time to avoid downtime. For example, when changing database credentials, create the new credential before revoking the old one to guarantee a smooth transition.
* Add a new value in Vault, on a different path, and update the Corda configuration through the REST API. The relevant worker processes will pick up this new value asynchronously.
