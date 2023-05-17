---
date: '2023-04-13'
title: "Configure Key Pairs and Certificates"
menu:
  corda5:
    identifier: corda5-networks-members-key-pairs
    parent: corda5-networks-members
    weight: 3000
section_menu: corda5
---

This section describes how to configure key pairs and certificates. It contains the following:
1. [Generate a Session Initiation Key Pair]({{< relref "#generate-a-session-initiation-key-pair">}})
2. [Generate a Ledger Key Pair]({{< relref "#generate-a-ledger-key-pair">}})
3. [Generate a TLS Key Pair]({{< relref "#generate-a-tls-key-pair">}})
4. [Disable Revocation Checks]({{< relref "#disable-revocation-checks">}})

## Generate a Session Initiation Key Pair

To assign a soft hardware security module (HSM) and generate a session initiation key pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```Bash
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/hsm/soft/$HOLDING_ID/SESSION_INIT
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL'/keys/'$HOLDING_ID'/alias/'$HOLDING_ID'-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/hsm/soft/$HOLDING_ID/SESSION_INIT"
$SESSION_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1"
$SESSION_KEY_ID = $SESSION_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, the result contains the session key ID (for example, 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```shell
export SESSION_KEY_ID=<session-key-ID>
```

## Generate a Ledger Key Pair

To assign a soft hardware security module (HSM) and generate a ledger key pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/hsm/soft/$HOLDING_ID/LEDGER
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-ledger/category/LEDGER/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/hsm/soft/$HOLDING_ID/LEDGER"
$LEDGER_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-ledger/category/LEDGER/scheme/CORDA.ECDSA.SECP256R1"
$LEDGER_KEY_ID = $LEDGER_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, the result contains the ledger key ID (for example, 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```shell
export LEDGER_KEY_ID=<ledger-key-ID>
```

## Generate a TLS Key Pair

{{< note >}}
This step is only necessary when setting up a new cluster.
It is only required once per cluster, allowing you to re-use the same TLS key and certificate for the whole cluster.
{{< /note >}}

You must perform the same steps as those for setting up the MGM to enable peer-to-peer communication for the locally hosted identities.
Use the Certificate Authority (CA) whose trustroot certificate was configured in the registration context of the MGM.

If using mutual TLS, you must must add the certificate subject to the allowed list of the MGM. For more information, see [Update the MGM Allowed Certificate Subject List]({{< relref "../optional/mutual-tls-connections.md#update-the-mgm-allowed-certificate-subject-list" >}}).

1. Create a TLS key pair at the cluster-level by running this command:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X POST -H "Content-Type: application/json" $REST_API_URL/keys/p2p/alias/p2p-TLS/category/TLS/scheme/CORDA.RSA
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $TLS_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/keys/p2p/alias/p2p-TLS/category/TLS/scheme/CORDA.RSA"
   $TLS_KEY_ID = $TLS_KEY_RESPONSE.id
   ```
   {{% /tab %}}
   {{< /tabs >}}

   If using Bash, the endpoint returns the TLS key ID:
   ```shell
   export TLS_KEY_ID=<TLS-key-ID_>
   ```

2. Create a certificate for the TLS key pair by running the following command to generate a certificate signing request (CSR):
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD  -X POST -H "Content-Type: application/json" -d '{"x500Name": "CN=CordaOperator, C=GB, L=London, O=Org", "subjectAlternativeNames": ["'$P2P_GATEWAY_HOST'"]}' $REST_API_URL/certificates/p2p/$TLS_KEY_ID > "$WORK_DIR"/request2.csr
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/certificates/p2p/$TLS_KEY_ID" -Body (ConvertTo-Json @{
       x500Name = "CN=CordaOperator, C=GB, L=London"
       subjectAlternativeNames = @($P2P_GATEWAY_HOST)
   }) > $WORK_DIR/request2.csr
   ```
   {{% /tab %}}
   {{< /tabs >}}

   You can inspect the `request2.csr` file by running this command:
   ```shell
   openssl req -text -noout -verify -in ./request.csr
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

4. To upload the certificate chain to the Corda cluster, run this command, where `<certificate-folder>` is the path to the folder in which you saved the certificate received from the CA:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT  -F certificate=<certificate-folder>/certificate.pem -F alias=p2p-tls-cert $REST_API_URL/certificates/cluster/p2p-tls
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$REST_API_URL/certificates/cluster/p2p-tls"  -Form @{
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

If the CA has not been configured with revocation (for example, via CRL or OCSP), you can disable revocation checks. 
* [Disable Revocation Checks Using Bash]({{< relref "#disable-revocation-checks-using-bash">}})
* [Disable Revocation Checks Using PowerShell]({{< relref "#disable-revocation-checks-using-powershell">}})

By default, revocation checks are enabled.
You only need to disable revocation checks once per cluster.

#### Disable Revocation Checks Using Bash

If using Bash, to disable revocation checks, do the following:
1. Retrieve the current gateway configuration version:
   ```bash
   curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/config/corda.p2p.gateway
   ```
2. Save the displayed version number from the response as a variable:
   ```bash
   export CONFIG_VERSION=<configuration-version>
   ```
3. Send the following request to disable revocation checks for the specified gateway worker:
   ```bash
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"section":"corda.p2p.gateway", "version":"'$CONFIG_VERSION'", "config":"{ \"sslConfig\": { \"revocationCheck\": { \"mode\": \"OFF\" }  }  }", "schemaVersion": {"major": 1, "minor": 0}}' $REST_API_URL"/config"
   ```

#### Disable Revocation Checks Using PowerShell

If using PowerShell, to disable revocation checks, run the following:
```shell
$CONFIG_VERSION = (Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/config/corda.p2p.gateway").version
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$REST_API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
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