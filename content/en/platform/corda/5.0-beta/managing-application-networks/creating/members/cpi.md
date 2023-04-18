---
date: '2023-04-13'
title: "Build the Member CPI"
menu:
  corda-5-beta:
    identifier: corda-5-beta-app-networks-members-cpi
    parent: corda-5-beta-app-networks-members
    weight: 1000
section_menu: corda-5-beta
---

## Set Variables
Set the values of variables for use in later commands:

1. Set the P2P gateway host and port and the REST API host and port. For example:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export REST_API_HOST=localhost
   export REST_API_PORT=8888
   export P2P_GATEWAY_HOST=localhost
   export P2P_GATEWAY_PORT=8080
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $REST_API_HOST = "localhost"
   $REST_API_PORT = 8888
   $P2P_GATEWAY_HOST = "localhost"
   $P2P_GATEWAY_PORT = 8080
   $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("$REST_API_USER:$REST_API_PASSWORD" -f $username,$password)))
   ```
   {{% /tab %}}
   {{< /tabs >}}

   These values vary depending on where you have deployed your cluster(s) and how you have forwarded the ports. For example, if `corda-p2p-gateway-worker` is the name of the P2P gateway Kubernetes service and `corda-cluster-a` is the namespace that the Corda cluster is deployed within, set `$P2P_GATEWAY_HOST` to `corda-p2p-gateway-worker.corda-cluster-a`. Alternatively, you can specify the IP address of the gateway, instead of the hostname. For example, `192.168.0.1`.

2. Set the REST API URL. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export API_URL="https://$REST_API_HOST:$REST_API_PORT/api/v1"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $API_URL = "https://$REST_API_HOST:$REST_API_PORT/api/v1"
   ```
   {{% /tab %}}
   {{< /tabs >}}
3. Set the working directory for storing temporary files.

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export WORK_DIR=~/Desktop/register-member
   mkdir -p "$WORK_DIR"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $WORK_DIR = "$HOME/register-member"
   md $WORK_DIR -Force
   ```
   {{% /tab %}}
   {{< /tabs >}}

## Generate the Group Policy File

To join a group, members must use a {{< tooltip >}}group policy{{< definition word="group policy" >}}{{< /tooltip >}} file exported from the MGM of that group. To retrieve the `GroupPolicy.json` file from the MGM:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export MGM_REST_HOST=localhost
   export MGM_REST_PORT=8888
   export MGM_REST_URL="https://$MGM_REST_HOST:$MGM_REST_PORT/api/v1"
   export MGM_HOLDING_ID=<MGM-holding-ID>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $MGM_REST_HOST = "localhost"
   $MGM_REST_PORT = "8888"
   $MGM_API_URL = "https://$MGM_REST_HOST:$MGM_REST_PORT/api/v1"
   $MGM_HOLDING_ID = <MGM-holding-ID>
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$MGM_API_URL/mgm/$MGM_HOLDING_ID/info" | ConvertTo-Json -Depth 4 > $WORK_DIR/GroupPolicy.json
   ```
   {{% /tab %}}
   {{< /tabs >}}
   If using Bash, create the `GroupPolicy.json` by exporting it using the MGM, by running this command:
   ```shell
   curl -u $REST_API_USER:$REST_API_PASSWORD -X GET $MGM_API_URL/mgm/$MGM_HOLDING_ID/info > "$WORK_DIR/GroupPolicy.json"
   ```

## Create the CPI

Build a {{< tooltip >}}CPI{{< definition word="CPI" >}}{{< /tooltip >}} using the Corda CLI, passing in the member CPB and the `GroupPolicy.json` file exported from the MGM. 

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

To upload the CPI to the network, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export CPI_PATH=<CPI-directory/CPI-filename.cpi>
curl -u $REST_API_USER:$REST_API_PASSWORD -F upload=@$CPI_PATH $API_URL/cpi/
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_PATH = "$WORK_DIR\mgm-5.0.0.0-SNAPSHOT-package.cpi"
$CPI_UPLOAD_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/cpi/" -Method Post -Form @{
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
export CPI_ID=<CPI-ID>
curl -u $REST_API_USER:$REST_API_PASSWORD $API_URL/cpi/status/$CPI_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_ID = $CPI_UPLOAD_RESPONSE.id
$CPI_STATUS_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/cpi/status/$CPI_ID"
```
{{% /tab %}}
{{< /tabs >}}

The result contains the `cpiFileChecksum`. You need this to [create the member virtual node]({{< relref "./virtual-node.md" >}}).