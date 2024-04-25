---
description: "List of CPI commands for the Corda CLI. Use these commands to upload or fetch CPIs."
date: '2024-04-24'
menu:
  corda53:
    identifier: corda53-cordacli-cpi
    weight: 500
    parent: corda53-cli-reference
title: "cpi"
---
# cpi

This section lists the Corda CLI `cpi` arguments. You can use these commands to upload CPIs to your Corda cluster and also list any existing CPIs.

## upload

The `upload` command uploads a CPI present in the specified `.cpi` file into your Corda cluster, so that virtual nodes can be created using this CPI at a later point.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument           | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| -t, \-\-target     | The target address of the REST server, for example, https://host:port. |
| -p, \-\-password   | The REST password.                                                         |
| -u, \-\-user       | The REST user name.                                                        |
| -c, \-\-cpi        | The CPI file to upload.                                                |
| -w, \-\-wait       | Wait for the checksum to populate. If not specified, you'll receive a standard ID, which you can later use to retrieve the checksum.  |
| -k, \-\-insecure   | Allows invalid server-side SSL certificates.                        |

{{< tabs name="DDL-user">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh cpi upload -t https://localhost:8888 -u admin -p password --cpi mycpifile.cpi -w -k
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd cpi upload -t https://localhost:8888 -u admin -p password --cpi mycpifile.cpi -w -k
```
{{% /tab %}}
{{< /tabs >}}

## list

The `list` command fetches the CPIs present in your Corda cluster.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument           | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| -t, \-\-target     | The target address of the REST server, for example, https://host:port. |
| -p, \-\-password   | The REST password.                                                         |
| -u, \-\-user       | The REST user name.                                                        |
| -k, \-\-insecure   | Allows invalid server-side SSL certificates.                        |

{{< tabs name="DDL-user">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh cpi list -t https://localhost:8888 -u admin -p password -k
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd cpi list -t https://localhost:8888 -u admin -p password -k
```
{{% /tab %}}
{{< /tabs >}}
