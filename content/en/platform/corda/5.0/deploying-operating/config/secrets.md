---
title: "Configuration Secrets"
date: '2023-05-12'
menu:
  corda5:
    identifier: corda5-cluster-secrets
    parent: corda5-cluster-config
    weight: 3000
section_menu: corda5
---

The Corda configuration system allows for any string configuration value to be marked as “secret”. When this configuration value is used, Corda delegates the resolution of this value to the configured `SecretsLookupService`.

## Default Secrets Service

Corda 5 provides a default `SecretsLookupService`. Implementation of this service is in the form of a service that uses symmetric encryption so that the value can be stored encrypted at rest and decrypted with a key derived from a configured salt and passphrase when needed. The salt and passphrase must be passed in as start-up parameters:

```
-s salt=<salt> -s passphrase=<passphrase>
```

For example, the following is a standard configuration:

```
{
  "foo": "bar",
  "fred": 123
}
```

You can specify `foo` as a secret, as follows:

```
{
  "foo": "bar",
  "fred": {
    "configSecret": {
      "encryptedSecret": "<encrypted-value>"
    } 
  }
}
```

You can use the Corda CLI [secret-config command]({{< relref "../../reference/corda-cli/secret-config.md" >}}) to to generate the encrypted value based on a salt and passphrase.

You can also use the default `SecretsLookupService` with start-up configuration. For example:

```
-ddatabase.user=db-user
-ddatabase.pass.configSecret.encryptedSecret=<encryped-db-password>
-ddatabase.jdbc.url=jdbc:postgresql://db-address:5432/cordacluster
-ddatabase.jdbc.directory=/opt/corda/drivers
```

{{< note >}}
Any configuration items can be configured as sensitive or not. It is up to you to decide if a particular configuration item should be treated as sensitive.
{{< /note >}}

## External Secrets Service < enterprise-icon >

In some instances, the default implementation of `SecretsLookupService` may not be sufficient. For example, in the case of [Database Connection Configuration]({{< relref "./database-connection.md" >}}), the salt and passphrase used for the encryption is present in the same set of start-up parameters as the configuration that may be sensitive. This may be adequate if you can ensure that these start-up parameters are sufficiently protected. However, in other cases it may be preferable to manage these credentials outside Corda.

Corda Enterprise supports integration with HashiCorp Vault integration as an external secret management system. 