---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-obfuscated-config-file-changes
    parent: cenm-1-4-operations
    weight: 165
tags:
- obfuscated
- obfuscation-tool
title: Obfuscation configuration file changes
---
# Obfuscated configuration file changes

When you work with obfuscated configuration files, note the following:
1. Use the Corda Enterprise Configuration Obfuscator tool. See [Configuration Obfuscator](https://docs.corda.net/docs/corda-enterprise/tools-config-obfuscator.html) for more information.

2. The updated arguments, required to run the service with obfuscation options, are as follows:

* `--config-obfuscation-passphrase[=<cliPassphrase>]` - the passphrase used in the key derivation function when generating an AES key.

* `--config-obfuscation-seed[=<cliSeed>]` - the seed used in the key derivation function to create a salt.

3. If the configuration for the given service is obfuscated, one or both of `--config-obfuscation-passphrase` and `--config-obfuscation-seed` **must** be defined, or the service will not know that the configuration is obfuscated.

    If one of the above values are defined, the other one will default to the same value as in the Corda Enterprise Configuration Obfuscator tool. For example, if a configuration is obfuscated with the default seed and passphrase via the Corda Enterprise Configuration Obfuscator tool, the seed or the passphrase still has to be defined when running the CENM service.

    As the default seed in the Corda Enterprise Configuration Obfuscator tool is `Corda`, the service should be run with the `--config-obfuscation-seed=Corda` option.
4. If a configuration is uploaded to Zone Service and it contains an obfuscated password property inside `ssl.keyStore`, then the `keyPassword` property should be provided and obfuscated as well. See the examples below.

    Obfuscated configuration that will be acepted:

        ```ssl {
        ...
            keyStore {
                ...
                keyPassword="<{4OfEUdZ4bJwmJKbh7hLLMU+Yt+OYBvQo3TfyqDe9odE=:K05YPAm2ZWabN4gghcIWkCqDxmPPVmiR}>"
                password="<{RphkU+W9fTUKYjD4ss+0lclIvrKh+QdoAMKHe8f1rhs=:gIt5CroFf3XlXsfTA28O3btzlP+JYXXV}>"
                ...
            }
        ...
        }```

    Obfuscated configuration that will not be accepted:


        ```ssl {
        ...
            keyStore {
                ...
                password="<{RphkU+W9fTUKYjD4ss+0lclIvrKh+QdoAMKHe8f1rhs=:gIt5CroFf3XlXsfTA28O3btzlP+JYXXV}>"
                ...
            }
        ...
        }```

5. You can obfuscate CENM 1.1 and 1.2 configuration files with CENM 1.3 (and above), but for any further obfuscation, use the new version of the Configuration Obfuscator tool.

{{< note >}}
If a configuration file is uploaded to the Zone Service, any host fields in the configuration file must not be obfuscated.
{{< /note >}}
