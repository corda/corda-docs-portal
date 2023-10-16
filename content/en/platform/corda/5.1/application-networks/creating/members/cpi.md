---
date: '2023-08-10'
version: 'Corda 5.1'
title: "Build and Upload the Member CPI"
menu:
  corda51:
    identifier: corda51-networks-members-cpi
    parent: corda51-networks-members
    weight: 1000
section_menu: corda51
---

# Build and Upload the Member CPI

This section describes how to build a {{< tooltip >}}member{{< /tooltip >}} {{< tooltip >}}CPI{{< /tooltip >}} and upload it to the network. It contains the following:
1. [Set Variables]({{< relref "#set-variables" >}})
2. [Generate the Group Policy File]({{< relref "#generate-the-group-policy-file" >}})
3. [Create the CPI File]({{< relref "#create-the-cpi-file" >}})
4. [Import Code Signing Certificates]({{< relref "#import-code-signing-certificates" >}})
5. [Upload the CPI]({{< relref "#upload-the-cpi" >}})

{{< note >}}
If you want to use mutual TLS, see [Configuring Mutual TLS]({{< relref "../optional/mutual-tls-connections.md#modify-the-cluster-configurations" >}}) for additional configuration steps before you upload the CPI.
{{< /note >}}

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
   ```
   {{% /tab %}}
   {{< /tabs >}}

   These values vary depending on where you have deployed your {{< tooltip >}}clusters{{< /tooltip >}} and how you have forwarded the ports. For example, if `corda-p2p-gateway-worker` is the name of the P2P gateway {{< tooltip >}}Kubernetes{{< /tooltip >}} service and `corda-cluster-a` is the namespace that the Corda cluster is deployed within, set `$P2P_GATEWAY_HOST` to `corda-p2p-gateway-worker.corda-cluster-a`. Alternatively, you can specify the IP address of the gateway, instead of the hostname; for example, `192.168.0.1`. 
   
 If you are using an [Ingress service in front of the P2P gateway]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#p2p-gateway">}}), the hostname should be one of the values under `hosts` and the port set to 443 (the default port for HTTPS).

2. Set the REST API URL. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export REST_API_URL="https://$REST_API_HOST:$REST_API_PORT/api/v5_1"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $REST_API_URL = "https://${REST_API_HOST}:${REST_API_PORT}/api/v5_1"
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Set the authentication information for the REST API:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export REST_API_USER="<username>"
   export REST_API_PASSWORD="<password>"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
    $REST_API_USER = "<username>"
    $REST_API_PASSWORD = "<password>"
    $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("${REST_API_USER}:${REST_API_PASSWORD}" -f $username,$password)))
   ```
   {{% /tab %}}
   {{< /tabs >}}

3. Set the working directory for storing temporary files.

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export WORK_DIR=creating-members-cpi
   mkdir -p "$WORK_DIR"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $WORK_DIR = "creating-members-cpi"
   md $WORK_DIR
   ```
   {{% /tab %}}
   {{< /tabs >}}

## Generate the Group Policy File

To join a group, members must use a {{< tooltip >}}group policy{{< /tooltip >}} file exported from the {{< tooltip >}}MGM{{< /tooltip >}} of that group. To retrieve the `GroupPolicy.json` file from the MGM:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export MGM_REST_HOST=localhost
   export MGM_REST_PORT=8888
   export MGM_REST_URL="https://$MGM_REST_HOST:$MGM_REST_PORT/api/v5_1"
   export MGM_HOLDING_ID=<MGM-holding-ID>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $MGM_REST_HOST = "localhost"
   $MGM_REST_PORT = "8888"
   $MGM_REST_URL = "https://$MGM_REST_HOST:$MGM_REST_PORT/api/v5_1"
   $MGM_HOLDING_ID = <MGM-holding-ID>
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$MGM_REST_URL/mgm/$MGM_HOLDING_ID/info" | ConvertTo-Json -Depth 4 > $WORK_DIR/GroupPolicy.json
   ```
   {{% /tab %}}
   {{< /tabs >}}
   If using Bash, create the `GroupPolicy.json` by exporting it using the MGM, by running this Curl command:
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X GET $MGM_REST_URL/mgm/$MGM_HOLDING_ID/info > "$WORK_DIR/GroupPolicy.json"
   ```
## Create the CPI File

{{< note >}}
If you are onboarding a notary, you need to import the [notary CPB code signing certificate]({{< relref "../notaries.md#import-notary-cpb-code-signing-certificate" >}}) before you create the notary CPI.
{{< /note >}}

Build a CPI using the {{< tooltip >}}Corda CLI{{< /tooltip >}}, passing in the member CPB, the `GroupPolicy.json` file exported from the MGM, and the details of the keystore certificate used to sign the CPB. 

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

## Import Code Signing Certificates

{{< note >}}
You do not have to repeat this step if a CPI previously uploaded to the network uses the same certificate.
{{< /note >}}

Corda validates that uploaded CPIs are signed with a trusted key. To trust your signing keys:

1. Export the signing key certificate from the keystore:
    ```shell
    keytool -exportcert -rfc -alias "<key-alias>" -keystore <signingkeys.pfx> -storepass "<keystore-password>" -file <signingkey1.pem>
    ```
2. Import the signing key into Corda:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -F alias="<unique-key-alias>" -F certificate=@<signingkey1.pem> $REST_API_URL/certificates/cluster/code-signer
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$REST_API_URL/certificates/cluster/code-signer"  -Form @{
   certificate=@<signingkey1.pem>
   alias="<unique-key-alias>"
   }
   ```
   {{% /tab %}}
   {{< /tabs >}}

{{< note >}}
Use an alias that will remain unique over time, taking into account that certificate expiry will require new certificates with the same X.500 name as existing certificates.
{{< /note >}}
## Upload the CPI

To upload the CPI to the network, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export CPI_PATH="$WORK_DIR\mgm-5.1.0.0-SNAPSHOT-package.cpi"
curl -k -u $REST_API_USER:$REST_API_PASSWORD -F upload=@$CPI_PATH $REST_API_URL/cpi/
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_PATH = "$WORK_DIR\mgm-5.1.0.0-SNAPSHOT-package.cpi"
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
export CPI_ID=<CPI-ID>
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/cpi/status/$CPI_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_ID = $CPI_UPLOAD_RESPONSE.id
$CPI_STATUS_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/cpi/status/$CPI_ID"
```
{{% /tab %}}
{{< /tabs >}}

The result contains the `cpiFileChecksum`. You need this to [create the member virtual node]({{< relref "./virtual-node.md" >}}).