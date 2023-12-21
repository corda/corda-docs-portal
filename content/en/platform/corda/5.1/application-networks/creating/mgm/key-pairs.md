---
description: "Learn how to configure key pairs and certificates for the MGM."
date: '2023-04-07'
version: 'Corda 5.1'
title: "Configure Key Pairs and Certificates for the MGM"
menu:
  corda51:
    parent: corda51-networks-mgm
    identifier: corda51-networks-mgm-key-pairs
    weight: 3000
    name:  "Configure Key Pairs and Certificates"
section_menu: corda51
---
# Configure Key Pairs and Certificates for the MGM

This section describes how to configure key pairs and certificates for the MGM. It contains the following:

1. [Generate a Session Initiation Key Pair]({{< relref "#generate-a-session-initiation-key-pair">}})
2. [Generate ECDH Key Pair]({{< relref "#generate-ecdh-key-pair">}})
3. [Configure the Cluster TLS Key Pair]({{< relref "#configure-the-cluster-tls-key-pair">}})
4. [Disable Revocation Checks]({{< relref "#disable-revocation-checks">}})

## Generate a Session Initiation Key Pair

To assign a soft hardware security module (HSM) and generate a {{< tooltip >}}session initiation key{{< /tooltip >}} pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/hsm/soft/$MGM_HOLDING_ID/SESSION_INIT
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/hsm/soft/$MGM_HOLDING_ID/SESSION_INIT"
$SESSION_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1"
$SESSION_KEY_ID = $SESSION_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, the result contains the session key ID (for example, 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```shell
export SESSION_KEY_ID=<session-key-ID>
```
{{< note >}}
You can use a certificate in addition to the session initiation key pair. For more information, see [Configuring Optional Session Certificates]({{< relref "../optional/session-certificates.md" >}}).
{{< /note >}}

## Generate ECDH Key Pair

To generate an Elliptic-Curve Diffie–Hellman ({{< tooltip >}}ECDH{{< /tooltip >}}) key pair:
{{< tabs >}}
{{% tab name="Bash"%}}
```
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/hsm/soft/$MGM_HOLDING_ID/PRE_AUTH
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-auth/category/PRE_AUTH/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/hsm/soft/$MGM_HOLDING_ID/PRE_AUTH"
$ECDH_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-auth/category/PRE_AUTH/scheme/CORDA.ECDSA.SECP256R1"
$ECDH_KEY_ID = $ECDH_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}
If using Bash, the result contains the key ID (for example, 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```
export ECDH_KEY_ID=<ECDH-key-ID>
```

You can use the following schemes for ECDH key derivation:

* ECDSA_SECP256R1
* ECDSA_SECP256K1
* X25519
* SM2

## Configure the Cluster TLS Key Pair
{{< note >}}
This step is only necessary if setting up a new cluster.
It is only required once per cluster, allowing you to re-use the same TLS key and certificate for the whole cluster.
{{< /note >}}

To set up the {{< tooltip >}}TLS{{< /tooltip >}} key pair and certificate for the cluster:

1. Create a TLS key pair at the cluster level by running this command:
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

   If using Bash, the endpoint returns the TLS key ID. Run the following command to save this ID for use in subsequent steps:
   ```shell
   export TLS_KEY_ID=<TLS-key-ID>
   ```
2. Create a certificate for the TLS key pair. In order to do so, you must create a certificate signing request (CSR). To generate a CSR, run this command:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD  -X POST -H "Content-Type: application/json" -d '{"x500Name": "CN=CordaOperator, C=GB, L=London, O=Org", "subjectAlternativeNames": ["'$P2P_GATEWAY_HOST'"]}' $REST_API_URL"/certificates/p2p/"$TLS_KEY_ID > "$WORK_DIR"/request1.csr
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/certificates/p2p/$TLS_KEY_ID" -Body (ConvertTo-Json @{
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

3. Provide the chosen {{< tooltip >}}CA{{< /tooltip >}}with this CSR and request for certificate issuance.

4. To upload the certificate chain to the Corda cluster, run this command, where `certificate-folder` is the path to the folder in which you saved the certificate received from the CA:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT  -F certificate=@<certificate-folder>/certificate.pem -F alias=p2p-tls-cert $REST_API_URL/certificates/cluster/p2p-tls
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$REST_API_URL/certificates/cluster/p2p-tls"  -Form @{
       certificate = Get-Item -Path <CERTIFICATE_FOLDER>\certificate.pem
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

If the CA has not been configured with revocation (for example, via CRL or OCSP), you can disable {{< tooltip >}}revocation checks{{< /tooltip >}} :

* [Disable Revocation Checks Using Bash]({{< relref "#disable-revocation-checks-using-bash">}})
* [Disable Revocation Checks Using PowerShell]({{< relref "#disable-revocation-checks-using-powershell">}})

By default, revocation checks are enabled.
You only need to disable revocation checks once per cluster.

#### Disable Revocation Checks Using Bash

If using Bash, to disable revocation checks, do the following:

1. Retrieve the current gateway configuration version:
   ```shell
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/config/corda.p2p.gateway
   ```
2. Save the displayed version number from the response as a variable:
   ```shell
   export CONFIG_VERSION=<configuration-version>
   ```
3. Send the following request to disable revocation checks for the specified {{< tooltip >}}gateway worker{{< /tooltip >}}:
   ```
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
