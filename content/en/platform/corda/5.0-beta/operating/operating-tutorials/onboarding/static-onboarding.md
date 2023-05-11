---
date: '2021-10-26'
title: "Onboarding Members to Static Networks"
menu:
  corda-5-beta:
    identifier: corda-5-beta-static-onboarding
    parent: corda-5-beta-tutorials-deploy-static
    weight: 4000
section_menu: corda-5-beta
---
This section describes the onboarding process for [static networks](../../../deploying/network-types.html#static-networks).

{{< note >}}
Static networks do not use an [MGM](../../../introduction/key-concepts.html#membership-management). If you require an MGM, see [Dynamic Onboarding](dynamic-onboarding.html).
{{< /note >}}

To run a static network, you must complete the following high-level steps:
1. [Start a Corda cluster](../../../deploying/deployment-tutorials/deploy-corda-cluster.html).
2. [Define the members in the group in the GroupPolicy.json file](#create-the-group-policy-file).
3. [Package the GroupPolicy.json file into a CPI](#create-a-cpi).
4. [Upload the CPI to your cluster](#upload-the-cpi).
5. [Create a virtual node in your cluster for each member defined in the group policy file](#create-virtual-nodes-for-each-member).
6. [Register each member in the group](#register-members).

## Create the Group Policy File

Use the [Corda CLI](../../../developing/getting-started/installing-corda-cli.html) to generate a [GroupPolicy.json file](../../../deploying/group-policy.html#static-network-member-group-policy), where `group-policy-folder` is the path to the folder in which you want to generate the file:
```shell
corda-cli.sh mgm groupPolicy --name="C=GB, L=London, O=Alice" --name="C=GB, L=London, O=Bob" --name="C=GB, L=London, O=Charlie" --endpoint-protocol=1 --endpoint="http://localhost:1080" > <group-policy-folder/GroupPolicy.json>
```

## Create a CPI

Build a CPI using the Corda CLI packaging plugin, passing in your generated `GroupPolicy.json` file. For more information about creating CPIs, see the [CorDapp Packaging section]({{< relref "../../../developing/development-tutorials/cordapp-packaging.md" >}}).

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

To register a member, run the following, replacing `<ID-short-hash>` with the holding identity ID short hash obtained in the [Create Virtual Nodes for Each Member](#create-virtual-nodes-for-each-member) section:
```shell
curl --insecure -u admin:admin -d '{ "memberRegistrationRequest": { "context": { "corda.key.scheme": "CORDA.ECDSA.SECP256R1" } } }' https://localhost:8888/api/v1/membership/<ID-short-hash>
```
{{< note >}}
The available key schemes are viewable through `KeysRpcOps`. One of them is used as an example in this command.
<!-- Needs more info -->
{{< /note >}}
Run this command for each member defined in the `staticNetwork` section of your `GroupPolicy.json` file.

Perform a lookup to ensure that all members have registered successfully and are visible to each other:
```shell
curl --insecure -u admin:admin -X GET https://localhost:8888/api/v1/members/<ID-short-hash>
```
{{< note >}}
Only members with `ACTIVE` membership status should be visible.
{{< /note >}}

If you are registering a member as a notary service representative, you must add the following as the context when registering:
```shell
"context": { "corda.key.scheme": "CORDA.ECDSA.SECP256R1", "corda.roles.0" : "notary", "corda.notary.service.name" : <notary-service-X500-name>, "corda.notary.service.plugin" : "net.corda.notary.NonValidatingNotary" }
```
