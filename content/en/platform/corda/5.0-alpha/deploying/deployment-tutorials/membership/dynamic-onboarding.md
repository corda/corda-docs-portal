---
date: '2022-11-15'
title: "Onboarding Members to Dynamic Networks"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-dynamic-onboarding
    parent: corda-5-alpha-membership-tutorials
    weight: 3000
section_menu: corda-5-alpha
---
This section describes how to configure a [dynamic network](../../network-types.html#dynamic-networks) to onboard new members.

## Set Variables
Set the values of variables for use in later commands:

1. Set the P2P gateway host and port and the RPC API host and port. This may also vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   ```shell
   export RPC_HOST=localhost
   export RPC_PORT=8888
   export P2P_GATEWAY_HOST=localhost
   export P2P_GATEWAY_PORT=8080
   ```

2. Set the RPC API URL. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   ```
   export API_URL="https://$RPC_HOST:$RPC_PORT/api/v1"
   ```

3. Set the working directory for storing temporary files.
   ```
   export WORK_DIR=~/Desktop/register-member
   mkdir -p $WORK_DIR
   ```

4. Set the path to your local clone of `corda-runtime-os`:
    ```shell
    export RUNTIME_OS=~/dev/corda-runtime-os
    ```

## Generate the Group Policy File

To onboard members to a group, a [running MGM](mgm-onboarding.html) is required. To join, members must use a [group policy file](../../group-policy.html) exported from the MGM of that group.

To create the `GroupPolicy.json` file:

1. Set the MGM properties, by running these commands:
   ```shell
   export MGM_RPC_HOST=localhost
   export MGM_RPC_PORT=8888
   export MGM_API_URL="https://$MGM_RPC_HOST:MGM_RPC_PORT/api/v1"
   export MGM_HOLDING_ID=<MGM Holding ID>
   ```

2. Create the `GroupPolicy.json` by exporting it using the MGM, by running this command:
   ```shell
   curl --insecure -u admin:admin -X GET $MGM_API_URL/mgm/$MGM_HOLDING_ID/info > $WORK_DIR/GroupPolicy.json
   ```

## Build the CPI
*copy from updated MGM section*
10. Add the group policy to the CPI file:
    ```shell
    cd $WORK_DIR
    zip $CPI_PATH -j ./GroupPolicy.json
    ```

## Upload the CPI
*copy below from updated MGM section??*
```
curl --insecure -u admin:admin -F upload=@$CPI_PATH $API_URL/cpi/
```

The returned identifier (e.g. the return will look like `{"id":"f0a0f381-e0d6-49d2-abba-6094992cef02"}` and the identifier is the id, or, using jq, one can run `CPI_ID=$(curl --insecure -u admin:admin -F upload=@$CPI_PATH $API_URL/cpi | jq -r '.id')`) ) is the `CPI ID`, use it below to get the checksum of the CPI.
```
export CPI_ID=<CPI ID>
curl --insecure -u admin:admin $API_URL/cpi/status/$CPI_ID
```
The result contains the `cpiFileChecksum`. Save this for the next step.

## Create a Virtual Node
To create a virtual node for the member, run the following commands, changing the X500 name:
```shell
export CPI_CHECKSUM=<CPI checksum>
export X500_NAME="C=GB, L=London, O=Alice"
curl --insecure -u admin:admin -d '{"request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "'$X500_NAME'"}}' $API_URL/virtualnode
```
*copy below from updated MGM section??*
The result contains the `holdingIdentity.shortHash` (e.g. 58B6030FABDD), save this for use in subsequent steps.
Replace `<holding identity ID>` with the ID from the previous step.
```
export HOLDING_ID=<holding identity ID>
```
## Assign HSM and generate key pairs
*copy below from updated MGM section??*
```
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$HOLDING_ID/SESSION_INIT
curl --insecure -u admin:admin -X POST $API_URL'/keys/'$HOLDING_ID'/alias/'$HOLDING_ID'-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1'
```
The result contains `session key ID` (e.g. `id` - 3B9A266F96E2); save this for use in subsequent steps.
```
export SESSION_KEY_ID=<session key ID>
```

```
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$HOLDING_ID/LEDGER
curl --insecure -u admin:admin -X POST $API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-ledger/category/LEDGER/scheme/CORDA.ECDSA.SECP256R1
```
The result contains `ledger key ID` (e.g. `id` for example 3B9A266F96E2); save this for subsequent steps.
```
export LEDGER_KEY_ID=<ledger key ID>
```

## Configure the TLS Key Pair and Certificate

{{< note >}}
This step is only necessary if setting up a new cluster.
When using cluster-level TLS, it is only necessary to do this once per cluster.
{{< /note >}}

You must perform the same steps that you did for setting up the MGM to enable the locally hosted identities P2P communication. If the fake CA tool was used when onboarding the MGM, it should be re-used for members. If a real CA was used for the MGM onboarding, then the same CA should be used for members.

1. Create a TLS key pair at the P2P cluster-level by running this command:
   ```shell
   curl -k -u admin:admin -X POST -H "Content-Type: application/json" $API_URL/keys/p2p/alias/p2p-TLS/category/TLS/scheme/CORDA.RSA
   ```
   The endpoint returns the TLS key ID:
   ```shell
   export TLS_KEY_ID=<TLS-key-ID>
   ```

2. Create a certificate for the TLS key pair. Regardless of whether you are using the fake development tool as a CA or using a real CA, you must create a  certificate signing request (CSR). To generate a CSR, run this command:
   ```shell
   curl -k -u admin:admin  -X POST -H "Content-Type: application/json" -d '{"x500Name": "CN=CordaOperator, C=GB, L=London", "subjectAlternativeNames": ["'$P2P_GATEWAY_HOST'"]}' $API_URL/certificates/p2p/$TLS_KEY_ID > $WORK_DIR/request1.csr
   ```
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

3. If you are using a real CA, provide the CA with this CSR and request a certificate.

   Alternatively, if using the fake CA dev tool, use the [fake CA created previously](mgm-onboarding.html#create-a-fake-ca) to sign the CSR and create a certificate:
   ```shell
   cd $RUNTIME_OS
   java -jar ./applications/tools/p2p-test/fake-ca/build/bin/corda-fake-ca-5.0.0.0-SNAPSHOT.jar -m /tmp/ca csr $WORK_DIR/request1.csr
   cd $WORK_DIR
   ```
   This command outputs the location of the signed certificate. For example:
   ```shell
   Wrote certificate to /tmp/ca/request1/certificate.pem
   ```

   4. To upload the certificate chain to the Corda cluster, run this command:
      ```shell
      curl -k -u admin:admin -X PUT  -F certificate=@/tmp/ca/request1/certificate.pem -F alias=p2p-tls-cert $API_URL/certificates/p2p
      ```
      You can optionally omit the root certificate.
      {{< note >}}
      If you upload a certificate chain consisting of more than one certificates, ensure that `-----END CERTIFICATE-----` and `-----BEGIN CERTIFICATE-----` from the next certificate are separated by a new line with no empty spaces in between.
      {{< /note >}}

      ### Disable Revocation Checks
      If the CA has not been configured with revocation (for example, via CRL or OCSP), you can disable revocation checks. By default, revocation checks are enabled.
      The fake CA dev tool does not support revocation and so, if you are using the fake CA, you must disable revocation checks. This only needs to be done once per cluster.

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

## Configure virtual node as network participant
At this point, the member virtual node must be configured with properties required for P2P messaging. The order is slightly different to MGM onboarding in that for members, we must do this before registering and for MGMs, it is the opposite.

```bash
curl -k -u admin:admin -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "p2pTlsTenantId": "p2p", "sessionKeyId": "'$SESSION_KEY_ID'"}' $API_URL/network/setup/$HOLDING_ID
```

This will set up the locally hosted identity required for the P2P messaging to work.
`p2pTlsCertificateChainAlias` refers to the alias used when importing the TLS certificate.
`p2pTlsTenantId` refers to the tenant ID under which the TLS cert was stored ("p2p" for cluster level)
`sessionKeyId` refers to the session key ID previously generated in this guide.

## Build Registration Context
{{ < note > }}
You can retrieve the names available for signature-spec through `KeysRpcOps`. One of them is used as an example below.
{{ < /note > }}

To build the registration context, run the following command, replacing

*To Review*
Configure the endpoint URL by replacing <Endpoint URL> with the endpoint of the P2P gateway.
If you are testing in a single cluster this value isn't important so you can set something like `https://localhost:8080`. If you need a multi cluster set up then this will need to be a valid p2p gateway URL. For example, `https://corda-p2p-gateway-worker.corda-cluster-a:8080` where `corda-p2p-gateway-worker` is the name of the P2P gateway k8s service and `corda-cluster-a` is the namespace the corda cluster is deployed within.
```
export REGISTRATION_CONTEXT='{
  "corda.session.key.id": "'$SESSION_KEY_ID'",
  "corda.session.key.signature.spec": "SHA256withECDSA",
  "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
  "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1"
}'
```

## Register Members

To register a member, run the following command:
```
curl --insecure -u admin:admin -d '{ "memberRegistrationRequest": { "action": "requestJoin", "context": '$REGISTRATION_CONTEXT' } }' $API_URL/membership/$HOLDING_ID
```
This sends a join request to the MGM, the response should be `SUBMITTED`.
*TO review*
{{< note >}}
If you are using the Swagger UI, use this example:
```
{
  "memberRegistrationRequest":{
    "action":"requestJoin",
    "context": <registration context>
  }
}
```
{{< /note >}}

You can confirm if the member was onboarded successfully by checking the status of the registration request:
```
export REGISTRATION_ID=<registration ID>
curl --insecure -u admin:admin -X GET $API_URL/membership/$HOLDING_ID/$REGISTRATION_ID
```
If successful, you should see the `APPROVED` registration status.

After registration, you can use the look-up functions provided by the `MemberLookupRpcOps` to confirm that your member can see other members and has `ACTIVE` membership status:
```
curl --insecure -u admin:admin -X GET $API_URL/members/$HOLDING_ID
```
