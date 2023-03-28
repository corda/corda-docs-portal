---
date: '2023-02-02'
title: "Onboarding the MGM"
menu:
  corda-5-beta:
    identifier: corda-5-beta-mgm-onboarding
    parent: corda-5-beta-tutorials-deploy-dynamic
    weight: 1000
section_menu: corda-5-beta
---

This section describes how to configure the MGM, through which a membership group is created for a [dynamic network](../../../deploying/network-types.html#dynamic-networks).

{{< note >}}
The PowerShell commands listed on this page are for use with  PowerShell 7.0 and will not execute correctly with PowerShell 5.x.
{{< /note >}}

## Set Variables
Set the values of variables for use in later commands:

1. Set the P2P gateway host and port and the [REST API](../../../operating/operating-tutorials/rest-api.html) host and port.
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
   $AUTH_INFO = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("admin:admin" -f $username,$password)))
   ```
   }
   {{% /tab %}}
   {{< /tabs >}}

These values can vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
Specifically, `P2P_GATEWAY_HOST` and `P2P_GATEWAY_PORT` correspond to the hostname that other clusters should be able to connect to
in order to send messages to this cluster.

If we assume that all clusters are set up in a single k8s cluster, then you can set those values to
the hostname and the port the corresponding k8s service is listening to.
For example, if `corda-p2p-gateway-worker` is the name of the P2P gateway Kubernetes service and `corda-cluster-a`
is the namespace that the Corda cluster is deployed within, you can set `$P2P_GATEWAY_HOST` to `corda-p2p-gateway-worker.corda-cluster-a`.

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
This is mandatory for P2P TLS certificates, and optionally, they may also be used for [session certificates](session-certificates.html), depending on the network configuration defined by the MGM operator.
This root CA certificate in PEM format must be included later when onboarding the MGM.

## Create the CPB

The MGM only requires a `GroupPolicy` file and an empty CPB is sufficient for the CPI.
You can run the following to use the MGM test CPB included in `corda-runtime-os`, or alternatively you can use any empty CPB:
``` shell
cd "$RUNTIME_OS"
./gradlew testing:cpbs:mgm:build
cp testing/cpbs/mgm/build/libs/mgm-5.0.0.0-SNAPSHOT-package.cpb "$WORK_DIR"
```

## Create the Group Policy File

Create the [GroupPolicy.json file](../../../deploying/group-policy.html#mgm-group-policy) in the same directory as the CPB:
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

## Build the CPI

Build a CPI using the Corda CLI packaging plugin, passing in your generated MGM `GroupPolicy.json` file. For more information about creating CPIs, see the [CorDapp Packaging section]({{< relref "../../../developing/development-tutorials/cordapp-packaging.md" >}}).

## Upload the CPI

To upload the CPI, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export CPI_PATH=<CPI-directory/CPI-filename.cpi>
curl --insecure -u admin:admin -F upload=@$CPI_PATH $API_URL/cpi/
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

To create a virtual node for the MGM, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export CPI_CHECKSUM=<CPI checksum>
curl --insecure -u admin:admin -d '{ "request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "C=GB, L=London, O=MGM"}}' $API_URL/virtualnode
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$VIRTUAL_NODE_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/virtualnode" -Method Post -Body (ConvertTo-Json @{
    request = @{
       cpiFileChecksum = $CPI_STATUS_RESPONSE.cpiFileChecksum
       x500Name = "C=GB, L=London, O=MGM"
    }
})

$MGM_HOLDING_ID = $VIRTUAL_NODE_RESPONSE.holdingIdentity.shortHash
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, run the following, replacing `<holding-identity-ID>` with the ID returned in `holdingIdentity.shortHash` (for example, `58B6030FABDD`).
```
export MGM_HOLDING_ID=<holding-identity-ID>
```

## Assign Soft HSM and Generate Session Initiation and ECDH Key Pair

To assign a soft high security module (HSM) and generate a session initiation key pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$MGM_HOLDING_ID/SESSION_INIT
curl --insecure -u admin:admin -X POST $API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/hsm/soft/$MGM_HOLDING_ID/SESSION_INIT"
$SESSION_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1"
$SESSION_KEY_ID = $SESSION_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, the result contains `session key ID` (e.g. 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```shell
export SESSION_KEY_ID=<session key ID>
```
{{< note >}}
You can use a certificate in addition to the session initiation key pair. For more information, see [Configuring Optional Session Certificates](session-certificates.html).
{{< /note >}}

To generate an Elliptic-curve Diffie–Hellman (ECDH) key pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$MGM_HOLDING_ID/PRE_AUTH
curl --insecure -u admin:admin -X POST $API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-auth/category/PRE_AUTH/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/hsm/soft/$MGM_HOLDING_ID/PRE_AUTH"
$ECDH_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-auth/category/PRE_AUTH/scheme/CORDA.ECDSA.SECP256R1"
$ECDH_KEY_ID = $ECDH_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}
If using Bash, the result contains `key ID` (e.g. 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```
export ECDH_KEY_ID=<ecdh key ID>
```

You can use the following schemes for ECDH key derivation:
* ECDSA_SECP256R1
* ECDSA_SECP256K1
* X25519
* SM2

## Configure the Cluster TLS Key Pair and Certificate
{{< note >}}
This step is only necessary if setting up a new cluster.
When using cluster-level TLS, it is only necessary to do this once per cluster.
{{< /note >}}

To set up the TLS key pair and certificate for the cluster:

1. Create a TLS key pair at the P2P cluster level by running this command:
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
2. Create a certificate for the TLS key pair. In order to do so, you must create a certificate signing request (CSR). To generate a CSR, run this command:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u admin:admin  -X POST -H "Content-Type: application/json" -d '{"x500Name": "CN=CordaOperator, C=GB, L=London, O=Org", "subjectAlternativeNames": ["'$P2P_GATEWAY_HOST'"]}' $API_URL"/certificates/p2p/"$TLS_KEY_ID > "$WORK_DIR"/request1.csr
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/certificates/p2p/$TLS_KEY_ID" -Body (ConvertTo-Json @{
       x500Name = "CN=CordaOperator, C=GB, L=London, O=Org"
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
   ```shell
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

4. To upload the certificate chain to the Corda cluster, run this command, where `certificate-folder` is the path to the folder in which you saved the certificate received from the CA:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u admin:admin -X PUT  -F certificate=<certificate-folder>/certificate.pem -F alias=p2p-tls-cert $API_URL/certificates/cluster/p2p-tls
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$API_URL/certificates/cluster/p2p-tls"  -Form @{
       certificate = Get-Item -Path <certificate-folder>\certificate.pem
       alias = "p2p-tls-cert"
   }
   ```
   {{% /tab %}}
   {{< /tabs >}}

   You can optionally omit the root certificate.
   {{< note >}}
   If you upload a certificate chain consisting of more than one certificate, ensure that `-----END CERTIFICATE-----` and `-----BEGIN CERTIFICATE-----` from the next certificate are separated by a new line with no empty spaces in between.
   {{< /note >}}

### Disable Revocation Checks
If the CA has not been configured with revocation (for example, via CRL or OCSP), you can disable revocation checks:
* [Disable Revocation Checks Using Bash](#disable-revocation-checks-using-bash)
* [Disable Revocation Checks Using PowerShell](#disable-revocation-checks-using-powershell)
By default, revocation checks are enabled.
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

## Build Registration Context

To register the MGM, you must first generate the registration context:
* [Build Registration Context Using Bash](#build-registration-context-using-bash)
* [Build Registration Context Using PowerShell](#build-registration-context-using-powershell)

The examples in this section set `corda.group.key.session.policy` to `Distinct`, indicating that the ledger and session initiation key must not be the same key. Alternatively, setting `corda.group.key.session.policy` to `Combined` means that the ledger key used by a member must be the same as the session initiation key.

You can also optionally set the session certificate trustroot using the property `corda.group.truststore.session.0`, similar to `corda.group.truststore.tls.0`. However, when `corda.group.pki.session` is set to `NoPKI`, the session certificates are not validated against a session trustroot. For more information, see [Configuring Optional Session Certificates](session-certificates.html).

{{< note >}}
* If using session certificates for the P2P layer, see [Configuring Optional Session Certificates](session-certificates.html#build-registration-context-for-mgm-registration) for information about the additional JSON fields required.
* If using mutual TLS, you must set the `corda.group.tls.type` field to `Mutual`. For more information, see [Configuring Mutual TLS](mutual-tls.html#set-the-tls-type-in-the-mgm-context). 
{{< /note >}}

### Build Registration Context Using Bash

To build the registration context using Bash, run the following command, replacing `<TLS-CA-PEM-certificate>` with the PEM format certificate of the CA. This is the trustroot used to validate member certificates.
The certificate must all be on one line in the curl command. Replace new lines with `\n`.
```shell
export TLS_CA_CERT=$(cat /tmp/ca/ca/root-certificate.pem | awk '{printf "%s\\n", $0}')
export REGISTRATION_CONTEXT='{
  "corda.session.key.id": "'$SESSION_KEY_ID'",
  "corda.ecdh.key.id": "'$ECDH_KEY_ID'",
  "corda.group.protocol.registration": "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
  "corda.group.protocol.synchronisation": "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
  "corda.group.protocol.p2p.mode": "Authenticated_Encryption",
  "corda.group.key.session.policy": "Distinct",
  "corda.group.pki.session": "NoPKI",
  "corda.group.pki.tls": "Standard",
  "corda.group.tls.type": "OneWay",
  "corda.group.tls.version": "1.3",
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1",
  "corda.group.truststore.tls.0" : "'$TLS_CA_CERT'"
}'
```
### Build Registration Context Using PowerShell

To build the registration context using PowerShell, run the following command, setting `TLS_CA_CERT_PATH` to the certificate path:
```shell
$TLS_CA_CERT_PATH = "$env:TEMP\tmp\ca\ca\root-certificate.pem"
$REGISTRATION_CONTEXT = @{
  'corda.session.key.id' =  $SESSION_KEY_ID
  'corda.ecdh.key.id' = $ECDH_KEY_ID
  'corda.group.protocol.registration' = "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService"
  'corda.group.protocol.synchronisation' = "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl"
  'corda.group.protocol.p2p.mode' = "Authenticated_Encryption"
  'corda.group.key.session.policy' = "Distinct"
  'corda.group.pki.session' = "NoPKI"
  'corda.group.pki.tls' = "Standard"
  'corda.group.tls.version' = "1.3"
  'corda.endpoints.0.connectionURL' = "https://$P2P_GATEWAY_HOST:$P2P_GATEWAY_PORT"
  'corda.endpoints.0.protocolVersion' = "1"
  'corda.group.truststore.tls.0'  =  [IO.File]::ReadAllText($TLS_CA_CERT_PATH)
}
```

## Register the MGM

You can now use the registration context to register the MGM on the network:
* [Register the MGM using Bash](#register-the-mgm-using-bash)
* [Register the MGM using PowerShell](#register-the-mgm-using-powershell)

### Register the MGM using Bash

To register the MGM using Bash, run this command:
```shell
REGISTRATION_REQUEST='{"memberRegistrationRequest":{"action": "requestJoin", "context": '$REGISTRATION_CONTEXT'}}'
curl --insecure -u admin:admin -d "$REGISTRATION_REQUEST" $API_URL/membership/$MGM_HOLDING_ID
```
For example:
``` shell
curl --insecure -u admin:admin -d '{ "memberRegistrationRequest": { "action": "requestJoin", "context": {
  "corda.session.key.id": "D2FAF709052F",
  "corda.ecdh.key.id": "E2FCF719062B",
  "corda.group.protocol.registration": "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
  "corda.group.protocol.synchronisation": "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
  "corda.group.protocol.p2p.mode": "Authenticated_Encryption",
  "corda.group.key.session.policy": "Distinct",
  "corda.group.pki.session": "NoPKI",
  "corda.group.pki.tls": "Standard",
  "corda.group.tls.type": "OneWay",
  "corda.group.tls.version": "1.3",
  "corda.endpoints.0.connectionURL": "https://localhost:8080",
  "corda.endpoints.0.protocolVersion": "1",
  "corda.group.truststore.tls.0" : "-----BEGIN CERTIFICATE-----\nMIIBLjCB1aADAgECAgECMAoGCCqGSM49BAMCMBAxDjAMBgNVBAYTBVVLIENOMB4X\nDTIyMDgyMzA4MDUzN1oXDTIyMDkyMjA4MDUzN1owEDEOMAwGA1UEBhMFVUsgQ04w\nWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAASG6ijAvbmaIaIwKpZZqTeKmMKfoOPb\ncCK/BqdtKXVTt5AjJtiP/Uoq+481UEQyaUZYXGf5rC1owjT40U2B71qdoyAwHjAP\nBgNVHRMBAf8EBTADAQH/MAsGA1UdDwQEAwIBrjAKBggqhkjOPQQDAgNIADBFAiEA\n1h6WEfdWUXSjBcenf5ycXPkYQQzI92I54q2WaVVjQHwCIEBk1ov/hYp9RCCDPnJx\nk8WgCZIyhFe0pEmow7MuI/Zk\n-----END CERTIFICATE-----"
} } }' https://localhost:8888/api/v1/membership/EF19BF67E77C
```

Alternatively, using jq:
```shell
curl --insecure -u admin:admin -d $(
jq -n '.memberRegistrationRequest.action="requestJoin"' | \
  jq --arg session_key_id $SESSION_KEY_ID '.memberRegistrationRequest.context."corda.session.key.id"=$session_key_id' | \
  jq --arg ecdh_key_id $ECDH_KEY_ID '.memberRegistrationRequest.context."corda.ecdh.key.id"=$ecdh_key_id' | \
  jq '.memberRegistrationRequest.context."corda.group.protocol.registration"="net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService"' | \
  jq '.memberRegistrationRequest.context."corda.group.protocol.synchronisation"="net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl"' | \
  jq '.memberRegistrationRequest.context."corda.group.protocol.p2p.mode"="Authenticated_Encryption"' | \
  jq '.memberRegistrationRequest.context."corda.group.key.session.policy"="Distinct"' | \
  jq '.memberRegistrationRequest.context."corda.group.pki.session"="NoPKI"' | \
  jq '.memberRegistrationRequest.context."corda.group.pki.tls"="Standard"' | \
  jq '.memberRegistrationRequest.context."corda.group.tls.version"="1.3"' | \
  jq '.memberRegistrationRequest.context."corda.group.key.session.policy"="Distinct"' | \
  jq --arg p2p_url "https://$P2P_GATEWAY_HOST:$P2P_GATEWAY_PORT" '.memberRegistrationRequest.context."corda.endpoints.0.connectionURL"=$p2p_url' | \
  jq '.memberRegistrationRequest.context."corda.endpoints.0.protocolVersion"="1"' | \
  jq --rawfile root_certicicate /tmp/ca/ca/root-certificate.pem '.memberRegistrationRequest.context."corda.group.truststore.tls.0"=$root_certicicate' \
) $API_URL/membership/$MGM_HOLDING_ID
```

### Register the MGM using PowerShell

To register the MGM using PowerShell, run this command:
```shell
$REGISTER_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/membership/$MGM_HOLDING_ID" -Body (ConvertTo-Json -Depth 4 @{
    memberRegistrationRequest = @{
        action = "requestJoin"
        context = $REGISTRATION_CONTEXT
    }
})
$REGISTER_RESPONSE.registrationStatus
```
### Confirm Registration

Registration should return a successful response with the status `SUBMITTED`.
You can confirm if the MGM was onboarded successfully by checking the status of the registration request:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export REGISTRATION_ID=<registration ID>
curl --insecure -u admin:admin -X GET $API_URL/membership/$MGM_HOLDING_ID/$REGISTRATION_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$MGM_HOLDING_ID/${RESGISTER_RESPONSE.registrationId}"
```
{{% /tab %}}
{{< /tabs >}}
If successful, you should see the `APPROVED` registration status.

## Configure the Virtual Node as a Network Participant

To configure the MGM virtual node with properties required for P2P messaging, run this command:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u admin:admin -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeyId": "'$SESSION_KEY_ID'"}' $API_URL/network/setup/$MGM_HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/network/setup/$MGM_HOLDING_ID" -Method Put -Body (ConvertTo-Json @{
    p2pTlsCertificateChainAlias = "p2p-tls-cert"
    useClusterLevelTlsCertificateAndKey = $true
    sessionKeyId = $SESSION_KEY_ID
})
```
{{% /tab %}}
{{< /tabs >}}

* `p2pTlsCertificateChainAlias` — the alias used when importing the TLS certificate.
* `p2pTlsTenantId` — the tenant ID under which the TLS cert was stored ("p2p" for cluster level).
* `sessionKeyId` — the [session key ID previously generated](#assign-soft-hsm-and-generate-session-initiation-and-ecdh-key-pair).
* `useClusterLevelTlsCertificateAndKey` - `true` if the TLS certificate and key are cluster-level certificates and keys.

## Export the Group Policy

Now that the MGM is onboarded, the MGM can export a group policy file with the connection details of the MGM. To output the full contents of the `GroupPolicy.json` file that should be packaged within the CPI for members, run this command:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
mkdir -p "~/Desktop/register-member"
curl --insecure -u admin:admin -X GET $API_URL/mgm/$MGM_HOLDING_ID/info > "~/Desktop/register-member/GroupPolicy.json"
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
md ~/register-member -Force
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/mgm/$MGM_HOLDING_ID/info" | ConvertTo-Json -Depth 4 > ~/register-member/GroupPolicy.json
```
{{% /tab %}}
{{< /tabs >}}

You can now use the MGM to [set up members in your network](dynamic-onboarding.html).
