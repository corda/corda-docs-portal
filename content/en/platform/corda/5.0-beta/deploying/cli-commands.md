---
date: '2022-12-13'
menu:
  corda-5-beta:
    identifier: corda-5-beta-cordacli-deploy-commands
    weight: 4000
    parent: corda-5-beta-deploy
section_menu: corda-5-beta
title: "Corda CLI Commands"
---

This section describes the [Corda CLI](../../installing-corda-cli.html) MGM commands. Use these commands to execute membership operations.

Running the `groupPolicy` command without any arguments prints a sample `GroupPolicy.json` file that you can manually tweak.
```shell
./corda-cli.sh mgm groupPolicy
```
Alternatively, the following command line arguments can be used to define the static network section of the GroupPolicy:

| Argument            | Description                                                          |
|---------------------|----------------------------------------------------------------------|
| --file, -f          | The path to a JSON or YAML file that contains static network information. |
| --name              | The X.500 name of the member.          |
| --endpoint          | The endpoint base URL.             |
| --endpoint-protocol | The version of end-to-end authentication protocol.              |

### Generating GroupPolicy Using File Input

To generate GroupPolicy using file input:

```shell
./corda-cli.sh mgm groupPolicy --file="app/build/resources/src.yaml"
```
{{< note >}}
* Only one of `memberNames` and `members` blocks may be present.
* As ingle endpoint is assumed for all members when `memberNames` is used.
* Endpoint information specified under `members` overrides endpoint information set at the root level. An error is thrown if endpoint information is not provided at all.
{{< /note >}}
#### Sample Files

JSON with `memberNames`:
```json
{
  "endpoint": "http://dummy-url",
  "endpointProtocol": 5,
  "memberNames": ["C=GB, L=London, O=Member1", "C=GB, L=London, O=Member2"]
}
```

JSON with `members`:
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

YAML with `memberNames`:
```yaml
endpoint: "http://dummy-url"
endpointProtocol: 5
memberNames: ["C=GB, L=London, O=Member1", "C=GB, L=London, O=Member2"]
```

YAML with `members` which all use a common endpoint, and Member1 overrides the protocol version:
```yaml
endpoint: "http://dummy-url"
endpointProtocol: 5
members:
    - name: "C=GB, L=London, O=Member1"
      status: "PENDING"
      endpointProtocol: 10
    - name: "C=GB, L=London, O=Member2"
```

### Generating GroupPolicy Using String Parameters

To generate GroupPolicy using file input:
```shell
./corda-cli.sh mgm groupPolicy --name="C=GB, L=London, O=Member1" --name="C=GB, L=London, O=Member2" --endpoint-protocol=5 --endpoint="http://dummy-url"
```
{{< note >}}
* Passing one or more `--name` arguments without specifying endpoint information throws an error.
* Not passing any `--name` arguments returns a GroupPolicy with an empty list of static members.
* A single endpoint is assumed for all members.
{{< /note >}}

## Package
The `package` commands execute operations for working with CPB and CPI files.

| Argument            | Description                                                          |
|---------------------|----------------------------------------------------------------------|
| --create-cpb         |  |
| --create         | |
| --verify         | |
| --sign         | |
| --create-cpi         | |

You can learn how to package your CorDapp in the Developer tutorial [here](../../developing/tutorials/packaging.html).
