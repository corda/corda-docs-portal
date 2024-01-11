---
description: "List of mgm commands for the Corda 5.1 CLI. You can use these commands to execute membership operations for static networks used for testing purposes."  
date: '2022-12-20'
version: 'Corda 5.2'
menu:
  corda52:
    identifier: corda52-cordacli-mgm
    weight: 3000
    parent: corda52-cli-reference
section_menu: corda52
title: "mgm"
---
# mgm

This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `mgm` arguments. You can use these commands to execute membership operations for static networks used for testing purposes.

Running the `groupPolicy` command without any arguments prints a sample `GroupPolicy.json` file that you can manually tweak.

{{< tabs name="groupPolicy">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh mgm groupPolicy
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd mgm groupPolicy
```
{{% /tab %}}
{{< /tabs >}}

Alternatively, use the following command line arguments to define the static network section of the GroupPolicy:

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

|Argument| Description                                                                                                                                                        |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| \-\-file, -f                            | The path to a JSON or YAML file that contains static network information; see [Generating GroupPolicy Using File Input](#generating-groupPolicy-using-file-input). |
| \-\-name                                | The {{< tooltip >}}X.500{{< /tooltip >}} name of the {{< tooltip >}}member{{< /tooltip >}}; see [Generating GroupPolicy Using String Parameters](#generating-grouppolicy-using-string-parameters).                               |
| \-\-endpoint                            | The endpoint base URL; see [Generating GroupPolicy Using String Parameters](#generating-grouppolicy-using-string-parameters).                                      |
| \-\-endpoint-protocol                   | The version of end-to-end authentication protocol; see [Generating GroupPolicy Using String Parameters](#generating-grouppolicy-using-string-parameters).          |

## Generating GroupPolicy Using File Input

To generate GroupPolicy using file input:
   {{< tabs name="groupPolicy-file">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh mgm groupPolicy --file="app/build/resources/src.yaml"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd mgm groupPolicy --file="app/build/resources/src.yaml"
   ```
   {{% /tab %}}
   {{< /tabs >}}

{{< note >}}
* Only `memberNames` or `members` blocks may be present.
* A single endpoint is assumed for all members when `memberNames` is used.
* Endpoint information specified under `members` overrides endpoint information set at the root level. An error is thrown if no endpoint information is provided.
{{< /note >}}

### Sample Files

* JSON with `memberNames`:
  ```json
  {
    "endpoint": "http://dummy-url",
    "endpointProtocol": 5,
    "memberNames": ["C=GB, L=London, O=Member1", "C=GB, L=London, O=Member2"]
  }
  ```

* JSON with `members`:
  ```json
  {
    "members": [
        {
        "name": "C=GB, L=London, O=Member1",
        "status": "PENDING",
        "endpoint": "http://dummy-url",
        "endpointProtocol": 5
        },
        {
          "name": "C=GB, L=London, O=Member2",
          "endpoint": "http://dummy-url2",
          "endpointProtocol": 5
        }
      ]
  }
  ```
* YAML with `memberNames`:
  ```yaml
  endpoint: "http://dummy-url"
  endpointProtocol: 5
  memberNames: ["C=GB, L=London, O=Member1", "C=GB, L=London, O=Member2"]
  ```

* YAML with `members` which all use a common endpoint, and Member1 overrides the protocol version:
  ```yaml
  endpoint: "http://dummy-url"
  endpointProtocol: 5
  members:
    - name: "C=GB, L=London, O=Member1"
      status: "PENDING"
      endpointProtocol: 10
    - name: "C=GB, L=London, O=Member2"
  ```

## Generating GroupPolicy Using String Parameters

To generate GroupPolicy using parameters:
   {{< tabs name="groupPolicy-params">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh mgm groupPolicy --name="C=GB, L=London, O=Member1" --name="C=GB, L=London, O=Member2" --endpoint-protocol=5 --endpoint="http://dummy-url"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd mgm groupPolicy --name="C=GB, L=London, O=Member1" --name="C=GB, L=London, O=Member2" --endpoint-protocol=5 --endpoint="http://dummy-url"
   ```
   {{% /tab %}}
   {{< /tabs >}}

{{< note >}}
* Passing one or more `--name` arguments without specifying endpoint information throws an error.
* Not passing any `--name` arguments returns a GroupPolicy with an empty list of static members.
* A single endpoint is assumed for all members.
{{< /note >}}
