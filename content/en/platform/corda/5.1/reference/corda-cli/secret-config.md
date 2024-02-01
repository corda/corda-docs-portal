---
description: "List of secret-config commands for the Corda 5.1 CLI. You can use these commands to generate the configuration for use with a secrets lookup service."  
date: '2023-05-12'
menu:
  corda51:
    identifier: corda51-cordacli-secret-config
    weight: 4050
    parent: corda51-cli-reference
title: "secret-config"
---

# secret-config

This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `secret-config` arguments. You can use these commands to generate the configuration for use with the [configured secrets lookup service]({{< relref "../../deploying-operating/deployment/deploying/_index.md#encryption" >}}).

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument    | Description                                                                             |
| ----------- | --------------------------------------------------------------------------------------- |
| \-\-create  | Encrypts a configuration value for the secrets lookup service. See [create](#create).   |
| \-\-decrypt | Decrypts a value for the Corda default secrets lookup service. See [decrypt](#decrypt). |

## create

The `create` argument generates the configuration string for use with the specified secrets lookup service using the following arguments:

| Argument            | Description                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| \-p, \-\-passphrase | The passphrase for the default secrets lookup service. This must be the same value in the [deployment configuration]({{< relref "../../deploying-operating/deployment/deploying/_index.md#default-secrets-service" >}}).                                                                                                                                                         |
| \-s, \-\-salt       | The salt for the default secrets lookup service. This must be the same value in the [deployment configuration]({{< relref "../../deploying-operating/deployment/deploying/_index.md#default-secrets-service" >}}).                                                                                                                                                               |
| \-t, \-\-type       | The secrets lookup service type. This can be one of the following: <ul><li>`corda` — encrypts the specified value using the specified salt and passphrase and generates the configuration to use that value.</li><li>`vault` —  generates the configuration to use a value from the HashiCorp Vault based on the specified key and Vault path. {{< enterprise-icon >}}</li></ul> |
| \-v, \-\-vault-path | The path in the HashiCorp Vault that stores the configuration value.                                                                                                                                                                                                                                                                                                             |
| \<value\>           | The configuration value to encrypt for the default secrets lookup service or the key of the secret for the HashiCorp Vault.                                                                                                                                                                                                                                                      |

For example, to generate the configuration to use to specify a value encrypted using the default Corda secrets service:

   {{< tabs name="create-default">}}
   {{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh secret-config -t corda -p "red yellow green" -s f1nd1ngn3m0 mypassword create
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   ./corda-cli.cmd secret-config -t corda -p "red yellow green" -s f1nd1ngn3m0 mypassword create
   ```
   {{% /tab %}}
   {{< /tabs >}}

For example, to generate the configuration to use to specify a value stored in a HashiCorp Vault:

   {{< tabs name="create-hashicorp">}}
   {{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh secret-config -v myPath -t vault passwordKey create
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   ./corda-cli.cmd secret-config -v myPath -t vault passwordKey create
   ```
   {{% /tab %}}
   {{< /tabs >}}

## decrypt

The `decrypt` argument decrypts a value encrypted by the Corda default secrets lookup service.

| Argument            | Description                                                                                                                                                                                                              |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| \-p, \-\-passphrase | The passphrase for the default secrets lookup service. This must be the same value in the [deployment configuration]({{< relref "../../deploying-operating/deployment/deploying/_index.md#default-secrets-service" >}}). |
| \-s, \-\-salt       | The salt for the default secrets lookup service. This must be the same value in the [deployment configuration]({{< relref "../../deploying-operating/deployment/deploying/_index.md#default-secrets-service" >}}).       |
| \<value\>           | The configuration value to decrypt using the default secrets lookup.                                                                                                                                                     |

For example:

   {{< tabs name="decrypt">}}
   {{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh secret-config -p "red yellow green" -s f1nd1ngn3m0 QuPOUSHXrnC8gJWgKdGq6Pgb45S9RPatPUCHTI9SuEgBiKfDQ2M= decrypt
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   ./corda-cli.cmd secret-config -p "red yellow green" -s f1nd1ngn3m0 QuPOUSHXrnC8gJWgKdGq6Pgb45S9RPatPUCHTI9SuEgBiKfDQ2M= decrypt
   ```
   {{% /tab %}}
   {{< /tabs >}}
