---
date: '2021-10-26'
title: "Onboarding Members to Static Networks"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-static-onboarding
    parent: corda-5-alpha-onboarding-tutorials
    weight: 4000
section_menu: corda-5-alpha
---
This section describes the onboarding process for [static networks](../../network-types.html#static-networks).

{{< note >}}
Static networks do not use an MGM. If you require an MGM, see [Dynamic Onboarding](dynamic-onboarding.html).
{{< /note >}}

## Create the Group Policy

1. Create a directory to store your files. For example:
   ```shell
   mkdir -p ~/Desktop/register-member/
   ```
.........
<!--
Build the `mgm` plugin in the [corda-runtime-os](https://github.com/corda/corda-runtime-os) repo using the following command:
```
./gradlew :tools:plugins:mgm:build
```

Build the [corda-cli-plugin-host](https://github.com/corda/corda-cli-plugin-host) repo:
```
./gradlew build
```

Copy `mgm-5.0.0.0-SNAPSHOT.jar` from `corda-runtime-os`:
```
cd tools/plugins/mgm/build/libs
```

To the `corda-cli-plugin-host` repo's `build/plugins` directory. Run the following command to generate your `GroupPolicy` file:
```
./build/generatedScripts/corda-cli.sh mgm groupPolicy --name="C=GB, L=London, O=Alice" --name="C=GB, L=London, O=Bob" --name="C=GB, L=London, O=Charlie" --endpoint-protocol=1 --endpoint="http://localhost:1080" > ~/Desktop/register-member/GroupPolicy.json
```

For more options to generate `GroupPolicy` file follow [this](https://github.com/corda/corda-runtime-os/blob/release/os/5.0/tools/plugins/mgm/README.md) readme.
-->

## Create a CPI

Create a CPI by following the instructions in *[CorDapp Packaging](), using the group policy file that you generated in the [Create the Group Policy]() section.

## Upload the CPI

To upload the generated CPI, run the following, replacing `<CPI-name>.cpi` with the name of your CPI:
```shell
export CPI_PATH=./<CPI-name>.cpi
curl --insecure -u admin:admin -F upload=@./$CPI_PATH https://localhost:8888/api/v1/cpi/
```
This returns the identifier of the CPI. For example, `{"id":"f0a0f381-e0d6-49d2-abba-6094992cef02"}`.

Alternatively, using jq, you can run the following to set `CPI ID` to the identifier:
```shell
CPI_ID=$(curl --insecure -u admin:admin -F upload=@$CPI_PATH $API_URL/cpi | jq -r '.id')
```

Use the CPI identifier to obtain the checksum of the CPI:
```shell
curl --insecure -u admin:admin https://localhost:8888/api/v1/cpi/status/<CPI-ID>
```

## Create Virtual Nodes for Each Member

To create a virtual node for each member, run the following, replacing `<CPI-checksum>` with the checksum obtained in the [Upload the CPI](#upload-the-cpi) section:
```
curl --insecure -u admin:admin -d '{ "request": { "cpiFileChecksum": "<CPI-checksum>", "x500Name": "<member's name>"  } }' https://localhost:8888/api/v1/virtualnode
```

This returns the holding identity ID short hashes.

## Register Members
<!-- The available key schemes are viewable through `KeysRpcOps`. One of them is used as an example in the command below.-->

To register a member, run the following, replacing `<ID-short-hash>` with the holding identity ID short hash obtained in the [Create Virtual Nodes for Each Member](#create-virtual-nodes-for-each-member) section:
```shell
curl --insecure -u admin:admin -d '{ "memberRegistrationRequest": { "action": "requestJoin", "context": { "corda.key.scheme": "CORDA.ECDSA.SECP256R1" } } }' https://localhost:8888/api/v1/membership/<ID-short-hash>
```
Run this command for each member defined in the `staticNetwork` section of your `GroupPolicy.json` file.

Perform a lookup to ensure all members have registered successfully and are visible to each other:
```shell
curl --insecure -u admin:admin -X GET https://localhost:8888/api/v1/members/<ID-short-hash>
```
{{< note >}}
Only members with `ACTIVE` membership status should be visible.
{{< /note >}}
