---
description: "Learn how to upgrade the member Corda Package Installers (CPIs) of your application network if an administrator upgrades the Corda cluster from 5.0 to 5.1."
date: '2023-11-22'
title: "Upgrading an Application Network"
menu:
  corda51:
    identifier: corda51-networks-upgrade
    parent: corda51-networks
    weight: 6000
---

# Upgrading an Application Network

After an administrator [upgrades a Corda cluster from 5.0 to 5.1]({{< relref "../../deploying-operating/deployment/upgrading/_index.md" >}}), you should upgrade the member {{< tooltip >}}CPIs{{< /tooltip >}} of your application network. The `MemberInfo` platform version is set at member registration time and so upgrading members ensures that this value reflects the current version. Upgrading members enables the correct implementation of the following:

* The MGM can make decisions about members based on their platform version. For example, excluding them from the network if they do not upgrade.
* Platform gating logic may be based on platform version.
* Ledger system flows can block transactions on members that are not on the current platform version.

{{< note >}}
There are no other technical limitations to running CorDapps built against Corda 5.0 after a platform upgrade to 5.1. Corda supports backwards compatibility but does not support forwards compatibility; 5.1 applications will not run on 5.0 Corda.
{{< /note >}}

The following sections describe how to upgrade your application network:

1. [Re-export the Group Policy from the MGM](#re-export-the-group-policy-from-the-mgm)
2. [Repackage the Member CPB](#repackage-the-member-cpb)
3. [Upload the CPI](#upload-the-cpi)
4. [Apply the New CPI to Each Virtual Node](#apply-the-new-cpi-to-each-virtual-node)

## Re-export the Group Policy from the MGM

To retrieve the {{< tooltip >}}group policy{{< /tooltip >}} file from the upgraded {{< tooltip >}}MGM{{< /tooltip >}}:

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

## Repackage the Member CPB

You must create a new CPI for each Corda-deployed CorDapp with the group policy file from the upgraded MGM. This CPI must have the same `Corda CPK CorDapp Name` as the existing CorDapp but with the `--cpi-version` incremented. For example:

{{< tabs name="build-cpi">}}
{{% tab name="Bash" %}}
```shell
./corda-cli.sh package create-cpi \
--cpb <CPB_FILE> \
--group-policy <UPGRADED_GROUP_POLICY_FILE_> \
--cpi-name "<CPI_Name>" \
--cpi-version "2.0.0.0-SNAPSHOT" \
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
--group-policy <UPGRADED_GROUP_POLICY_FILE_> `
--cpi-name "<CPI_Name>" `
--cpi-version "2.0.0.0-SNAPSHOT" `
--file <CPI_FILE_NAME>`
--keystore <SIGNING_KEY> `
--storepass "<SIGNING_KEY_PASSWORD>" `
--key "<SIGNING_KEY_NAME>"
```
{{% /tab %}}
{{< /tabs >}}

## Upload the CPI

To upload the upgraded CPI to the network, run the following:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
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
```shell
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

The result contains the `cpiFileChecksum`.

## Apply the New CPI to Each Virtual Node

The Cluster Administrator can [apply the new version of the CPI]({{< relref "../../deploying-operating/vnodes/upgrade-cpi.md">}}) using the CPI checksum.
