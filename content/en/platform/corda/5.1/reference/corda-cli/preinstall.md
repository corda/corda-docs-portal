---
date: '2023-08-10'
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-cordacli-preinstall
    weight: 6000
    parent: corda51-cli-reference
section_menu: corda51
title: "preinstall"
---
# preinstall
This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `preinstall` arguments. You can use these commands to manually
check Corda's configuration.

## check-limits

The `check-limits` argument verifies if the resource limits have been assigned correctly.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument | Description                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| <path>                             | The YAML file containing resource limit overrides for the Corda install.   |

{{< tabs name="create">}}
{{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh preinstall check-limits <path>
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```shell
   ./corda-cli.cmd preinstall check-limits <path>
   ```
{{% /tab %}}
{{< /tabs >}}


## check-postgres

The `check-postgres` argument verifies if the PostgreSQL database is up and if the credentials work.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument | Description                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| <path> | The YAML file containing the user name and password values for PostgreSQL - either as values, or as secret references. |
|  -n, --namespace=<namespace> | The namespace in which to look for PostgreSQL secrets, if there are any. |

{{< tabs name="create">}}
{{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh preinstall check-postgres [-n=<namespace>] <path>
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```shell
   ./corda-cli.cmd preinstall check-postgres [-n=<namespace>] <path>
   ```
{{% /tab %}}
{{< /tabs >}}

## check-kafka

The `check-kafka` argument verifies if Kafka is up and if the credentials work.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument | Description                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| <path> | The YAML file containing the Kafka, SASL, and TLS configurations. |
| -n, --namespace=<namespace> | The namespace in which to look for the Kafka secrets if TLS or SASL is enabled. |
| -t, --timeout=<timeout> | The timeout in milliseconds for testing the Kafka connection - defaults to 3000. |

{{< tabs name="create">}}
{{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh preinstall check-kafka [-n=<namespace>] [-t=<timeout>] <path>
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```shell
   ./corda-cli.cmd preinstall check-kafka [-n=<namespace>] [-t=<timeout>] <path>
   ```
{{% /tab %}}
{{< /tabs >}}

## run-all

The `run-all` argument runs all pre-install checks.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument | Description                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| <path> | The YAML file containing all configurations. |
| -n, --namespace=<namespace> | The namespace in which to look for both the PostgreSQL and Kafka secrets. |
| -t, --timeout=<timeout> | The timeout in milliseconds for testing the Kafka connection - defaults to 3000. |

{{< tabs name="create">}}
{{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh preinstall run-all [-n=<namespace>] [-t=<timeout>] <path>
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```shell
   ./corda-cli.cmd preinstall run-all [-n=<namespace>] [-t=<timeout>] <path>
   ```
{{% /tab %}}
{{< /tabs >}}
