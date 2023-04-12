---
date: '2023-04-07'
title: "Building the MGM CPI"
menu:
  corda-5-beta:
    parent: corda-5-beta-app-networks-mgm
    identifier: corda-5-beta-app-networks-mgm-cpi
    weight: 1000
section_menu: corda-5-beta
---

## Set Variables
Set the values of variables for use in later commands:

1. Set the P2P gateway host and port and the [REST API](../../../operating/operating-tutorials/rest-api.html) host and port. For example:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export REST_HOST=localhost
   export REST_PORT=8888
   export P2P_GATEWAY_HOST=localhost
   export P2P_GATEWAY_PORT=8080
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $REST_HOST = "localhost"
   $REST_PORT = 8888
   $P2P_GATEWAY_HOST = "localhost"
   $P2P_GATEWAY_PORT = 8080
   $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("$REST_API_USER:$REST_API_PASSWORD" -f $username,$password)))
   ```
   }
   {{% /tab %}}
   {{< /tabs >}}

   These values can vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   Specifically, `P2P_GATEWAY_HOST` and `P2P_GATEWAY_PORT` correspond to the hostname that other clusters should be able to connect to in order to send messages to this cluster.

   Assuming all clusters are set up in a single k8s cluster, you can set those values to the hostname and the port that the corresponding k8s service is listening to.
   For example, if `corda-p2p-gateway-worker` is the name of the P2P gateway Kubernetes service and `corda-cluster-a` is the namespace that the Corda cluster is deployed within, you can set `$P2P_GATEWAY_HOST` to `corda-p2p-gateway-worker.corda-cluster-a`.

2. Set the [REST API](../../../operating/operating-tutorials/rest-api.html) URL. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export API_URL="https://$REST_HOST:$REST_PORT/api/v1"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $API_URL="https://$REST_HOST:$REST_PORT/api/v1"
   ```
   }
   {{% /tab %}}
   {{< /tabs >}}

3. Set the working directory for storing temporary files:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export WORK_DIR=~/Desktop/register-mgm
   mkdir -p "$WORK_DIR"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $WORK_DIR = "$HOME/register-mgm"
   md $WORK_DIR -Force
   ```
   }
   {{% /tab %}}
   {{< /tabs >}}

4. Set the path to your local clone of `corda-runtime-os`:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export RUNTIME_OS=~/dev/corda-runtime-os
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $RUNTIME_OS = "~/dev/corda-runtime-os"
   ```
   }
   {{% /tab %}}
   {{< /tabs >}}

## Select a Certificate Authority

Corda uses an external Certificate Authority (CA) for the keys it generates.
This is mandatory for P2P TLS certificates, and optionally, they may also be used for [session certificates]({{< relref "../optional/session-certificates.md">}}), depending on the network configuration defined by the MGM operator.
This root CA certificate in PEM format must be included later when onboarding the MGM.

## Create the CPB

As with all CPI files, the MGM CPI requires a group policy file and a CPB file. For MGM CPIs, an empty CPB file is sufficient.
You can run the following to use the MGM test CPB included in `corda-runtime-os`, or alternatively you can use any empty CPB:
``` shell
cd "$RUNTIME_OS"
./gradlew testing:cpbs:mgm:build
cp testing/cpbs/mgm/build/libs/mgm-5.0.0.0-SNAPSHOT-package.cpb "$WORK_DIR"
```

## Create the Group Policy File

As most of the information in a group policy file is exported by the MGM, the initial MGM group policy is a much smaller file than that needed to create a member.

The MGM group policy file only requires a flag to indicate that a group ID must be generated during virtual node onboarding and information about how to register itself as part of the group.
Registration for an MGM is essentially finalising setup of the the group, but the registration terminology is kept in-line with the member setup.

This is a simple file that you can construct manually. You can also use the Corda CLI to export a default version. For more infromation about the Corda CLI `mgm groupPolicy` command, see [Creating MGM Group Policy with Corda CLI]({{< relref "./cli-mgm.md" >}}).

For example, to manually create the [GroupPolicy.json file](../../../deploying/group-policy.html#mgm-group-policy) in the same directory as the CPB created in the previous example:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
echo '{
  "fileFormatVersion" : 1,
  "groupId" : "CREATE_ID",
  "registrationProtocol" :"net.corda.membership.impl.registration.dynamic.mgm.MGMRegistrationService",
  "synchronisationProtocol": "net.corda.membership.impl.synchronisation.MgmSynchronisationServiceImpl"
}' > "$WORK_DIR"/GroupPolicy.json
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Add-Content $WORK_DIR/GroupPolicy.json @"
{
  "fileFormatVersion" : 1,
  "groupId" : "CREATE_ID",
  "registrationProtocol" :"net.corda.membership.impl.registration.dynamic.mgm.MGMRegistrationService",
  "synchronisationProtocol": "net.corda.membership.impl.synchronisation.MgmSynchronisationServiceImpl"
}
"@
```
{{% /tab %}}
{{< /tabs >}}

## Create the CPI

Build a CPI using the Corda CLI, passing in your generated MGM CPB and `GroupPolicy.json` files:

   {{< tabs name="build-cpi">}}
   {{% tab name="Bash" %}}
   ```shell 
   ./corda-cli.sh package create-cpi \
    --cpb <CPB_FILE> \
    --group-policy <GROUP_POLICY_FILE_> \
    --cpi-name "<CPI_Name>" \
    --cpi-version "1.0.0.0-SNAPSHOT" \
    --file <CPI_FILE_NAME> \
    --keystore <SIGNING_KEY> \
    --storepass "<SIGNING_KEY_PASSWORD>" \
    --key "<SIGNING_KEY_NAME>"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell 
   corda-cli.cmd package create-cpi `
    --cpb <CPB_FILE> `
    --group-policy <GROUP_POLICY_FILE_> `
    --cpi-name "<CPI_Name>" `
    --cpi-version "1.0.0.0-SNAPSHOT" `
    --file <CPI_FILE_NAME>`
    --keystore <SIGNING_KEY> `
    --storepass "<SIGNING_KEY_PASSWORD>" `
    --key "<SIGNING_KEY_NAME>"
   ```
   {{% /tab %}}
   {{< /tabs >}}

For more information about creating CPIs, see the [CorDapp Packaging section]({{< relref "../../../developing/development-tutorials/cordapp-packaging.md" >}}).

## Upload the CPI

To upload the CPI to your network, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```bash
export CPI_PATH=<CPI_DIRECTORY/CPI-FILENAME.cpi>
curl -u $REST_API_USER:$REST_API_PASSWORD -F upload=@$CPI_PATH $REST_API_URL/cpi/
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_PATH = <CPI_DIRECTORY/CPI-FILENAME.cpi>
$CPI_UPLOAD_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/cpi/" -Method Post -Form @{
    upload = Get-Item -Path $CPI_PATH
}
```
{{% /tab %}}
{{< /tabs >}}

The returned identifier (for example `f0a0f381-e0d6-49d2-abba-6094992cef02`) is the `CPI ID`.
Use this identifier to get the checksum of the CPI:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export CPI_ID=<CPI ID>
curl -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/cpi/status/$CPI_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_ID = $CPI_UPLOAD_RESPONSE.id
$CPI_STATUS_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/cpi/status/$CPI_ID"
```
{{% /tab %}}
{{< /tabs >}}

The result contains the `cpiFileChecksum`. You need this to [create the virtual node]({{< relref "./virtual-node.md" >}}) for the MGM.