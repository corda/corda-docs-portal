---
date: '2022-11-16'
title: "Onboarding Members to Dynamic Networks"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-dynamic-onboarding
    parent: corda-5-alpha-tutorials-deploy-dynamic
    weight: 3000
section_menu: corda-5-alpha
---
This section describes how to configure a [dynamic network](../../network-types.html#dynamic-networks) to onboard new members. It assumes you have configured the [MGM for the network](mgm-onboarding.html).

{{< note >}}
The PowerShell commands listed on this page are for use with  PowerShell 7.0 and will not execute correctly with PowerShell 5.x.
{{< /note >}}

## Set Variables
Set the values of variables for use in later commands:

1. Set the P2P gateway host and port and the [REST API](../../../developing/rest-api/rest-api.html) host and port. This may also vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export RPC_HOST=localhost
   export RPC_PORT=8888
   export P2P_GATEWAY_HOST=localhost
   export P2P_GATEWAY_PORT=8080
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $RPC_HOST = "localhost"
   $RPC_PORT = 8888
   $P2P_GATEWAY_HOST = "localhost"
   $P2P_GATEWAY_PORT = 8080
   $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("admin:admin" -f $username,$password)))
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Set the [REST API](../../../developing/rest-api/rest-api.html) URL. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export API_URL="https://$RPC_HOST:$RPC_PORT/api/v1"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $API_URL = "https://$RPC_HOST:$RPC_PORT/api/v1"
   ```
   {{% /tab %}}
   {{< /tabs >}}
3. Set the working directory for storing temporary files.

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export WORK_DIR=~/Desktop/register-member
   mkdir -p $WORK_DIR
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $WORK_DIR = "$HOME/register-member"
   md $WORK_DIR -Force
   ```
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
   {{% /tab %}}
   {{< /tabs >}}

## Generate the Group Policy File

To onboard members to a group, a [running MGM](mgm-onboarding.html) is required. To join, members must use a [group policy file](../../group-policy.html) exported from the MGM of that group.

To retrieve the `GroupPolicy.json` file from the MGM:

1. Set the MGM properties, by running these commands:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export MGM_RPC_HOST=localhost
   export MGM_RPC_PORT=8888
   export MGM_API_URL="https://$MGM_RPC_HOST:MGM_RPC_PORT/api/v1"
   export MGM_HOLDING_ID=<MGM Holding ID>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $MGM_RPC_HOST = "localhost"
   $MGM_RPC_PORT = "8888"
   $MGM_API_URL = "https://$MGM_RPC_HOST:$MGM_RPC_PORT/api/v1"
   $MGM_HOLDING_ID = <MGM Holding ID>
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$MGM_API_URL/mgm/$MGM_HOLDING_ID/info" | ConvertTo-Json -Depth 4 > $WORK_DIR/GroupPolicy.json
   ```
   {{% /tab %}}
   {{< /tabs >}}
   If using Bash, create the `GroupPolicy.json` by exporting it using the MGM, by running this command:
   ```shell
   curl --insecure -u admin:admin -X GET $MGM_API_URL/mgm/$MGM_HOLDING_ID/info > $WORK_DIR/GroupPolicy.json
   ```

## Build the CPI

Build the CPI using the [Corda CLI](../../installing-corda-cli.html) packaging plugin, passing in the member CPB and [group policy](#create-the-group-policy-file) files.

<!--Add link when ready
See this [CorDapp Packaging]() for more details.-->


## Upload the CPI

To upload the CPI, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```
curl --insecure -u admin:admin -F upload=@$CPI_PATH $API_URL/cpi/
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
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
export CPI_ID=<CPI ID>
curl --insecure -u admin:admin $API_URL/cpi/status/$CPI_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$CPI_ID = $CPI_UPLOAD_RESPONSE.id
$CPI_STATUS_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/cpi/status/$CPI_ID"
```
{{% /tab %}}
{{< /tabs >}}

The result contains the `cpiFileChecksum`. Save this for the next step.

## Create a Virtual Node

To create a virtual node for the member, run the following commands, changing the X500 name:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export CPI_CHECKSUM=<CPI checksum>
export X500_NAME="C=GB, L=London, O=Alice"
curl --insecure -u admin:admin -d '{"request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "'$X500_NAME'"}}' $API_URL/virtualnode
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$X500_NAME = "C=GB, L=London, O=Alice"
$VIRTUAL_NODE_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/virtualnode" -Method Post -Body (ConvertTo-Json @{
    request = @{
       cpiFileChecksum = $CPI_STATUS_RESPONSE.cpiFileChecksum
       x500Name = $X500_NAME
    }
})

$HOLDING_ID = $VIRTUAL_NODE_RESPONSE.holdingIdentity.shortHash
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, run the following, replacing `<holding identity ID>` with the ID returned in `holdingIdentity.shortHash` (for example, `58B6030FABDD`).
```
export MGM_HOLDING_ID=<holding identity ID>
```

## Configure the P2P Session Initiation Key Pair and Certificate

To assign a soft high security module (HSM) and generate a session initiation key pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$HOLDING_ID/SESSION_INIT
curl --insecure -u admin:admin -X POST $API_URL'/keys/'$HOLDING_ID'/alias/'$HOLDING_ID'-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/hsm/soft/$HOLDING_ID/SESSION_INIT"
$SESSION_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1"
$SESSION_KEY_ID = $SESSION_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, the result contains `session key ID` (e.g. 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```shell
export SESSION_KEY_ID=<session key ID>
```
## Configure the Ledger Key Pair and Certificate

To assign a soft high security module (HSM) and generate a ledger key pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$HOLDING_ID/LEDGER
curl --insecure -u admin:admin -X POST $API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-ledger/category/LEDGER/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/hsm/soft/$HOLDING_ID/LEDGER"
$LEDGER_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-ledger/category/LEDGER/scheme/CORDA.ECDSA.SECP256R1"
$LEDGER_KEY_ID = $LEDGER_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, the result contains the ledger key ID (e.g. 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```shell
export LEDGER_KEY_ID=<ledger key ID>
```

## Configure the TLS Key Pair and Certificate

{{< note >}}
This step is only necessary if setting up a new cluster.
When using cluster-level TLS, it is only necessary to do this once per cluster.
{{< /note >}}

You must perform the same steps that you did for setting up the MGM to enable P2P communication for the locally hosted identities. Use the CA whose trustroot certificate was configured in the MGM's registration context.

1. Create a TLS key pair at the P2P cluster-level by running this command:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u admin:admin -X POST -H "Content-Type: application/json" $API_URL/keys/p2p/alias/p2p-TLS/category/TLS/scheme/CORDA.RSA
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $TLS_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/keys/p2p/alias/p2p-TLS/category/TLS/scheme/CORDA.RSA"
   $TLS_KEY_ID = $TLS_KEY_RESPONSE.id
   ```
   {{% /tab %}}
   {{< /tabs >}}

   If using Bash, the endpoint returns the TLS key ID:
   ```shell
   export TLS_KEY_ID=<TLS-key-ID>
   ```

2. Create a certificate for the TLS key pair by running the following command to generate a certificate signing request (CSR):
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u admin:admin  -X POST -H "Content-Type: application/json" -d '{"x500Name": "CN=CordaOperator, C=GB, L=London", "subjectAlternativeNames": ["'$P2P_GATEWAY_HOST'"]}' $API_URL/certificates/p2p/$TLS_KEY_ID > $WORK_DIR/request1.csr
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/certificates/p2p/$TLS_KEY_ID" -Body (ConvertTo-Json @{
       x500Name = "CN=CordaOperator, C=GB, L=London"
       subjectAlternativeNames = @($P2P_GATEWAY_HOST)
   }) > $WORK_DIR/request1.csr
   ```
   {{% /tab %}}
   {{< /tabs >}}

   You can inspect the `request1.csr` file by running this command:
   ```shell
   openssl req -text -noout -verify -in ./request1.csr
   ```
   The contents should resemble the following:
   ```properties
   -----BEGIN CERTIFICATE REQUEST-----
   MIIDkjCCAfwCAQAwLjELMAkGA1UEBhMCR0IxDzANBgNVBAcTBkxvbmRvbjEOMAwG
   A1UEAxMFQWxpY2UwggGiMA0GCSqGSIb3DQEBAQUAA4IBjwAwggGKAoIBgQChJ9CW
   9bpnlKOg0OkRRSEPuo2CBMY4r9hDqgLPiadHqBh+QcXqZv23ftHDgFl7CnidG9xc
   1t8oCcOYSd9SfLTuxINF+eUoBZ5n4Igj210z1kp20bGc31qi7chzNHiLgpDXrh0x
   5AItxnHV+/grD4y3FxOxA6M0rGjMHsVWrxytTchEVN1cCEwUXWG0sjO3y4loctln
   nBAQyjxo0au1K5r9jzjz8dorkgCALYuSpr4eyjRij+/DuStH9VHcz+XdFz9MlW/B
   k4c8VzpqGhXs8w5UagnB81ZOmm+xoQOrELeZ1RPAEqCV8kAOO0xjfpTUIzOqz5bC
   U0luWEM0Gw0BsNdrdaQtrpAs0mv3Rmq6pMD6jlXTqJ8NbravrAnP1DMqHZKKMWnU
   PEyAuDJB3ndukJfRA03UpRmonvus1UXvheUgRG2f0RIbefvBLUqt+MBucgkUNQmf
   qyPuD2XaCcOLfSZ+FTtMg2P2E4l2cAnhmzeGL3kHTvilm3ZWlWBUEfJ4BZ0CAwEA
   AaAhMB8GCSqGSIb3DQEJDjESMBAwDgYDVR0PAQH/BAQDAgeAMAsGCSqGSIb3DQEB
   DQOCAYEAYtt2Fpgelb81jAEDayLHKISuwRXThGQv3xuZtwxdiC3gWdJbV9H6IWzv
   cmlxXUrnaju30eQ/LkB8tzuy++p2fIctO8y8Hiw743hddy6dEd21PxQHsNTAS5Ko
   1yikmzzRwT5JwMY+EZDxDxXfYViq0xaZoHPbcr3LmwkipqRnZo4e2i5jUCQjFMYq
   ZThLbl1NKHR98O2/akekmlpuGgtLFOLlSHYkZvZY7K1IEkLZAdbo4fhimDDxQg7T
   v59nY3SSGbNirFlqz4UfAjKpPyV+UVgRNcFNxJyA6/eL/J8Wedb3zqat2utilLb7
   6nicgQ0S3Xb5gPsTUXcsHRuD+FVJG+eJ1qEvh2srIZ57Nnjr9FTy6mqqN4Ln3g31
   k9GLOv2kll+tFWjAZEDSRX2VqxkVOlEuKeGXcdrJ2EXz3G444A0wtiTgppwdy9Az
   YCOEnQMQQUE3gXBax1UsQwl7M71it1/QuhtsBccLfX6rB8BNldwRibADPD16Y6PY
   LwkiaZXc
   -----END CERTIFICATE REQUEST-----
   ```

3. Provide the chosen CA with this CSR and request for certificate issuance.

4. To upload the certificate chain to the Corda cluster, run this command:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u admin:admin -X PUT  -F certificate=@/tmp/ca/request1/certificate.pem -F alias=p2p-tls-cert $API_URL/certificates/cluster/p2p-tls
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$API_URL/certificates/cluster/p2p-tls"  -Form @{
       certificate = Get-Item -Path $env:TEMP\tmp\ca\request1\certificate.pem
       alias = "p2p-tls-cert"
   }
   ```
   {{% /tab %}}
   {{< /tabs >}}

   You can optionally omit the root certificate.
   {{< note >}}
   If you upload a certificate chain consisting of more than one certificates, ensure that `-----END CERTIFICATE-----` and `-----BEGIN CERTIFICATE-----` from the next certificate are separated by a new line with no empty spaces in between.
   {{< /note >}}

### Disable Revocation Checks

If the CA has not been configured with revocation (for example, via CRL or OCSP), you can disable revocation checks. By default, revocation checks are enabled.
This only needs to be done once per cluster.
#### Disable Revocation Checks Using Bash

If using Bash, to disable revocation checks, do the following:
1. Retrieve the current gateway configuration version:
   ```shell
   curl --insecure -u admin:admin -X GET $API_URL/config/corda.p2p.gateway
   ```
2. Save the displayed version number from the response as a variable:
   ```shell
   export CONFIG_VERSION=<configuration-version>
   ```
3. Send the following request to disable revocation checks for the specified gateway worker:
   ```
   curl -k -u admin:admin -X PUT -d '{"section":"corda.p2p.gateway", "version":"'$CONFIG_VERSION'", "config":"{ \"sslConfig\": { \"revocationCheck\": { \"mode\": \"OFF\" }  }  }", "schemaVersion": {"major": 1, "minor": 0}}' $API_URL"/config"
   ```

#### Disable Revocation Checks Using PowerShell

If using PowerShell, to disable revocation checks, run the following:
```shell
$CONFIG_VERSION = (Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/config/corda.p2p.gateway").version
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
    section = "corda.p2p.gateway"
    version = $CONFIG_VERSION
    config = @{
        sslConfig = @{
            revocationCheck = @{
                mode = "OFF"
            }
        }
    }
    schemaVersion = @{
        major = 1
        minor = 0
    }
})
```

## Configure the Member Virtual Node for Network Communication

You must configure the virtual node as a network participant with the properties required for P2P messaging. The order is slightly different to MGM onboarding in that for members you must do this before registering.
To configure the member virtual node, run this command:
{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u admin:admin -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeyId": "'$SESSION_KEY_ID'"}' $API_URL/network/setup/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/network/setup/$HOLDING_ID" -Method Put -Body (ConvertTo-Json @{
    p2pTlsCertificateChainAlias = "p2p-tls-cert"
    useClusterLevelTlsCertificateAndKey = $true
    sessionKeyId = $SESSION_KEY_ID
})
```
{{% /tab %}}
{{< /tabs >}}

* `p2pTlsCertificateChainAlias` — the alias used when importing the TLS certificate.
* `useClusterLevelTlsCertificateAndKey` - true if the TLS certificate and key are cluster-level certificates and keys
* `sessionKeyId` — the [session key ID previously generated](#assign-hsm-and-generate-key-pairs).

## Build Registration Context
{{< note >}}
You can retrieve the names available for signature-spec through `KeysRpcOps`. One of them is used as an example below.
{{< /note >}}<!--will need more info-->

To build the registration context, run the following command, replacing the endpoint URL with the endpoint of the P2P gateway.
If you are testing in a single cluster, this value isn't important so you can use something like `https://localhost:8080`. If the network is a multi-cluster environment, must be a valid P2P gateway URL. For example, `https://corda-p2p-gateway-worker.corda-cluster-a:8080`, where `corda-p2p-gateway-worker` is the name of the P2P gateway Kubernetes service and `corda-cluster-a` is the namespace the Corda cluster is deployed within.
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export REGISTRATION_CONTEXT='{
  "corda.session.key.id": "'$SESSION_KEY_ID'",
  "corda.session.key.signature.spec": "SHA256withECDSA",
  "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
  "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1"
}'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REGISTRATION_CONTEXT = @{
  'corda.session.key.id' =  $SESSION_KEY_ID
  'corda.session.key.signature.spec' = "SHA256withECDSA"
  'corda.ledger.keys.0.id' = $LEDGER_KEY_ID
  'corda.ledger.keys.0.signature.spec' = "SHA256withECDSA"
  'corda.endpoints.0.connectionURL' = "https://$P2P_GATEWAY_HOST:$P2P_GATEWAY_PORT"
  'corda.endpoints.0.protocolVersion' = "1"
}
```
{{% /tab %}}
{{< /tabs >}}

## Register Members

To register a member, run the following command:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl --insecure -u admin:admin -d '{ "memberRegistrationRequest": { "action": "requestJoin", "context": '$REGISTRATION_CONTEXT' } }' $API_URL/membership/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REGISTER_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/membership/$HOLDING_ID" -Body (ConvertTo-Json -Depth 4 @{
    memberRegistrationRequest = @{
        action = "requestJoin"
        context = $REGISTRATION_CONTEXT
    }
})
$REGISTER_RESPONSE.registrationStatus
```
{{% /tab %}}
{{< /tabs >}}

This sends a join request to the MGM, the response should be `SUBMITTED`.

{{< note >}}
If you are using the Swagger UI, use this example:
```shell
{
  "memberRegistrationRequest":{
    "action":"requestJoin",
    "context": <registration context>
  }
}
```
{{< /note >}}

You can confirm if the member was onboarded successfully by checking the status of the registration request:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export REGISTRATION_ID=<registration ID>
curl --insecure -u admin:admin -X GET $API_URL/membership/$HOLDING_ID/$REGISTRATION_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$HOLDING_ID/${REGISTER_RESPONSE.registrationId}"
```
{{% /tab %}}
{{< /tabs >}}

If successful, you should see the `APPROVED` registration status.

After registration, you can use the look-up functions provided by the `MemberLookupRpcOps` to confirm that your member can see other members and has `ACTIVE` membership status:
{{< tabs >}}
{{% tab name="Bash"%}}
```
curl --insecure -u admin:admin -X GET $API_URL/members/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
 Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$HOLDING_ID" | ConvertTo-Json -Depth 4
```
{{% /tab %}}
{{< /tabs >}}
