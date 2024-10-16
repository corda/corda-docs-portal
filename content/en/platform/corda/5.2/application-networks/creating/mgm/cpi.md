---
description: "Learn how to build an MGM CPI and upload it to your network."
date: '2023-04-07'
title: "Build the MGM CPI"
menu:
  corda52:
    parent: corda52-networks-mgm
    identifier: corda52-networks-mgm-cpi
    weight: 1000
---

# Build the MGM CPI

This section describes how to build an {{< tooltip >}}MGM{{< /tooltip >}} {{< tooltip >}}CPI{{< /tooltip >}} and upload it to the network. It contains the following:

1. [Set Variables]({{< relref "#set-variables" >}})
2. [Select a Certificate Authority]({{< relref "#select-a-certificate-authority" >}})
3. [Create the Group Policy File]({{< relref "#create-the-group-policy-file" >}})
4. [Create the CPI File]({{< relref "#create-the-cpi-file" >}})
5. [Import Code Signing Certificates]({{< relref "#import-code-signing-certificates" >}})
6. [Upload the CPI]({{< relref "#upload-the-cpi" >}})

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

    These values vary depending on where you have deployed your {{< tooltip >}}cluster{{< /tooltip >}} and how you have forwarded the ports. For example, if `corda-p2p-gateway-worker` is the name of the P2P gateway {{< tooltip >}}Kubernetes{{< /tooltip >}} service and `corda-cluster-a` is the namespace that the Corda cluster is deployed within, set `$P2P_GATEWAY_HOST` to `corda-p2p-gateway-worker.corda-cluster-a`. Alternatively, you can specify the IP address of the gateway, instead of the hostname. For example, `192.168.0.1`. If you are using an [Ingress service in front of the P2P gateway]({{< relref "../../../deploying-operating/deployment/deploying/_index.md#p2p-gateway">}}), the hostname should be one of the values under `hosts` and the port set to 443 (the default port for HTTPS).

2. Set the REST API URL. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export REST_API_URL="https://$REST_API_HOST:$REST_API_PORT/api/v5_2"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $REST_API_URL="https://${REST_API_HOST}:${REST_API_PORT}/api/v5_2"
   ```
   {{% /tab %}}
   {{< /tabs >}}

3. Set the authentication information for the REST API:
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

4. Set the working directory for storing temporary files:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export WORK_DIR=creating-mgm-cpi
   mkdir -p "$WORK_DIR"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $WORK_DIR = "creating-mgm-cpi"
   md $WORK_DIR
   ```
   {{% /tab %}}
   {{< /tabs >}}

## Select a Certificate Authority

Corda uses an external {{< tooltip >}}CA{{< /tooltip >}} for the keys it generates.
This is mandatory for P2P {{< tooltip >}}TLS{{< /tooltip >}} certificates, and optionally, they may also be used for [session certificates]({{< relref "../optional/session-certificates.md">}}), depending on the network configuration defined by the {{< tooltip >}}MGM{{< /tooltip >}} operator.
This root CA certificate in {{< tooltip >}}PEM{{< /tooltip >}} format must be included later when onboarding the MGM.

## Create the Group Policy File

As most of the information in a {{< tooltip >}}group policy{{< /tooltip >}} file is exported by the MGM, the initial MGM group policy is a much smaller file than that needed to create a member.

The MGM group policy file only requires a flag to indicate that a group ID must be generated during {{< tooltip >}}virtual node{{< /tooltip >}} onboarding and information about how to register itself as part of the group.
Registration for an MGM is essentially finalizing setup of the group, but currently the registration terminology is kept in-line with the member setup.

This is a simple file that you can construct manually.
For example, to manually create the `GroupPolicy.json` file in your working directory:

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

## Create the CPI File

Build a CPI using the {{< tooltip >}}Corda CLI{{< /tooltip >}}, passing in your generated `GroupPolicy.json` file:

   {{< tabs name="build-cpi">}}
   {{% tab name="Bash" %}}
   ```shell
   ./corda-cli.sh package create-cpi \
    --group-policy "$WORK_DIR/GroupPolicy.json" \
    --cpi-name "MGM" \
    --cpi-version "1.0.0.0-SNAPSHOT" \
    --file "$WORK_DIR/MGM-1.0.0.0-SNAPSHOT.cpi"\
    --keystore <SIGNING_KEY> \
    --storepass "<SIGNING_KEY_PASSWORD>" \
    --key "<SIGNING_KEY_NAME>"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd package create-cpi `
    --group-policy "$WORK_DIR/GroupPolicy.json" `
    --cpi-name "MGM" `
    --cpi-version "1.0.0.0-SNAPSHOT" `
    --file "$WORK_DIR/MGM-1.0.0.0-SNAPSHOT.cpi" `
    --keystore <SIGNING_KEY> `
    --storepass "<SIGNING_KEY_PASSWORD>" `
    --key "<SIGNING_KEY_NAME>"
   ```
   {{% /tab %}}
   {{< /tabs >}}

{{< note >}}
Unlike other CPIs, an MGM CPI does not require a CPB file.
{{< /note >}}

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
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -F alias="<unique-key-alias>" -F certificate=@<signingkey1.pem> $REST_API_URL/certificate/cluster/code-signer
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$REST_API_URL/certificate/cluster/code-signer"  -Form @{
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

To upload the CPI to your network, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```bash
export CPI_PATH="$WORK_DIR/MGM-1.0.0.0-SNAPSHOT.cpi"
curl -k -u $REST_API_USER:$REST_API_PASSWORD -F upload=@$CPI_PATH $REST_API_URL/cpi/
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_PATH = "$WORK_DIR/MGM-1.0.0.0-SNAPSHOT.cpi"
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

The result contains the `cpiFileChecksum`. You need this to [create the virtual node]({{< relref "./virtual-node.md" >}}) for the MGM.
