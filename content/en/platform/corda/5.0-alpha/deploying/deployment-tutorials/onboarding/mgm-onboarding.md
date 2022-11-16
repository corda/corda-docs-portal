---
date: '2022-11-15'
title: "Onboarding the MGM"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-mgm-onboarding
    parent: corda-5-alpha-membership-tutorials
    weight: 2000
section_menu: corda-5-alpha
---

This section describes how to configure the MGM, through which a membership group is created for a [dynamic network](../../network-types.html#dynamic-networks).

## Set Variables
Set the values of variables for use in later commands:

1. Set the P2P gateway host and port and the RPC API host and port. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   ```shell
   export RPC_HOST=localhost
   export RPC_PORT=8888
   export P2P_GATEWAY_PORT=8080
   ```

2. Set the RPC API URL. This may vary depending on where you have deployed your cluster(s) and how you have forwarded the ports.
   ```shell
   export API_URL="https://$RPC_HOST:$RPC_PORT/api/v1"
   ```

3. Set the working directory for storing temporary files:
   ```shell
   export WORK_DIR=~/Desktop/register-mgm
   mkdir -p $WORK_DIR
   ```

4. Set the path to your local clone of `corda-runtime-os`:
   ```shell
   export RUNTIME_OS=~/dev/corda-runtime-os
   ```

## Select a Certificate Authority
Corda uses an external Certificate Authority (CA) for the keys it generates.
Currently, this is just for P2P TLS certificates, but, in the future, they may also be used for session certificates.
This root CA certificate in PEM format must be included later when onboarding the MGM.

### Create a Fake CA

For the purposes of testing in a development environment, you can use a fake CA, which is a development tool within `corda-runtime-os`.
{{< note >}}
If you have previously generated a fake CA, you can reuse that CA and you do not need to generate a new one.
{{< /note >}}
To create a fake CA in the temporary location `/tmp/ca`, run these commands:
```shell
cd $RUNTIME_OS
./gradlew :applications:tools:p2p-test:fake-ca:clean :applications:tools:p2p-test:fake-ca:appJar
java -jar ./applications/tools/p2p-test/fake-ca/build/bin/corda-fake-ca-5.0.0.0-SNAPSHOT.jar -m /tmp/ca -a RSA -s 3072 ca
```

This outputs the name and location of the generated file, which you should take note of.

## Create the CPB

The MGM only requires a `GroupPolicy` file and an empty CPB is sufficient for the CPI.
You can run the following to use the MGM test CPB:
``` shell
cd $RUNTIME_OS
./gradlew testing:cpbs:mgm:build
cp testing/cpbs/mgm/build/libs/mgm-5.0.0.0-SNAPSHOT-package.cpb $WORK_DIR
```

## Create the Group Policy File

Create the [GroupPolicy.json file](../../group-policy.html#mgm-group-policy) in the same directory as the CPB:
```shell
echo '{
  "fileFormatVersion" : 1,
  "groupId" : "CREATE_ID",
  "registrationProtocol" :"net.corda.membership.impl.registration.dynamic.mgm.MGMRegistrationService",
  "synchronisationProtocol": "net.corda.membership.impl.synchronisation.MgmSynchronisationServiceImpl"
}' > $WORK_DIR/GroupPolicy.json
```

## Build the CPI

Build the CPI using the `corda-cli` packaging plugin, passing in the [MGM CPB](#create-the-cpb) and [group policy](#create-the-group-policy-file) files.

*To review*
See this [CorDapp Packaging]() for more details.

Previously, the following commands were used to generate a V1 CPI. Corda will prevent V1 CPIs from being uploaded soon so these steps are no longer advised and are only here while we are still transitioning to V2 only CPIs. These instructions will be removed from this wiki page in the coming days.
```
cd $RUNTIME_OS
./gradlew testing:cpbs:mgm:build
cp testing/cpbs/mgm/build/libs/mgm-5.0.0.0-SNAPSHOT-package.cpb $WORK_DIR
cd $WORK_DIR
zip mgm-5.0.0.0-SNAPSHOT-package.cpb -j ./GroupPolicy.json
```

## Upload the CPI
*To review*
```
export CPI_PATH=<CPI PATH>
curl --insecure -u admin:admin -F upload=@$CPI_PATH $API_URL/cpi/
```

The returned identifier (for example `f0a0f381-e0d6-49d2-abba-6094992cef02`) is the `CPI ID`, use it below to get the checksum of the CPI.

```
export CPI_ID=<CPI ID>
curl --insecure -u admin:admin $API_URL/cpi/status/$CPI_ID
```

The result contains the `cpiFileChecksum`. Save this for the next step.

## Create a Virtual Node
*To review*
To create a virtual node for the MGM, run the following:
```shell
export CPI_CHECKSUM=<CPI checksum>
curl --insecure -u admin:admin -d '{ "request": {"cpiFileChecksum": "'$CPI_CHECKSUM'", "x500Name": "C=GB, L=London, O=MGM"}}' $API_URL/virtualnode
```
Replace `<holding identity ID>` with the ID from the previous step (in `holdingIdentity.shortHash` for example: `58B6030FABDD`).
```
export MGM_HOLDING_ID=<holding identity ID>
```

## Assign soft HSM, generate session initiation and each key pair
*To review*
```
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$MGM_HOLDING_ID/SESSION_INIT
curl --insecure -u admin:admin -X POST $API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-session/category/SESSION_INIT/scheme/CORDA.ECDSA.SECP256R1
```
The result contains `key ID` (e.g. 3B9A266F96E2), save this for use in subsequent steps.
```
export SESSION_KEY_ID=<session key ID>
```

```
curl --insecure -u admin:admin -X POST $API_URL/hsm/soft/$MGM_HOLDING_ID/PRE_AUTH
curl --insecure -u admin:admin -X POST $API_URL/keys/$MGM_HOLDING_ID/alias/$MGM_HOLDING_ID-auth/category/PRE_AUTH/scheme/CORDA.ECDSA.SECP256R1
```
The result contains `key ID` (e.g. 3B9A266F96E2), save this for use in subsequent steps.
```
export ECDH_KEY_ID=<ecdh key ID>
```

The schemes that can be used for ECDH key derivation are the following: ECDSA_SECP256R1, ECDSA_SECP256K1, X25519 and SM2

## Configure the Cluster TLS Key Pair and Certificate
{{< note >}}
This step is only necessary if setting up a new cluster.
When using cluster-level TLS, it is only necessary to do this once per cluster.
{{< /note >}}

To set up the TLS key pair and certificate for the cluster:

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
   curl -k -u admin:admin  -X POST -H "Content-Type: application/json" -d '{"x500Name": "CN=CordaOperator, C=GB, L=London", "subjectAlternativeNames": ["'$P2P_GATEWAY_HOST'"]}' $API_URL"/certificates/p2p/"$TLS_KEY_ID > $WORK_DIR/request1.csr
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

   Alternatively, if using the fake CA dev tool, use the [fake CA created previously](#create-a-fake-ca) to sign the CSR and create a certificate:
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

## Build Registration Context

{{< note >}}
Currently, a separate HSM category for ECDH key is not present. As a result, you can specify the same session initiation key in both places.  
{{< /note >}}

To build the registration context, run the following command, replacing `<TLS-CA-PEM-certificate>` with the PEM format certificate of the CA.
The certificate must all be on one line in the curl command. Replace new lines with `\n`.
```shell
export TLS_CA_CERT=<TLS-CA-PEM-certificate>
export REGISTRATION_CONTEXT='{
  "corda.session.key.id": "'$SESSION_KEY_ID'",
  "corda.ecdh.key.id": "'$ECDH_KEY_ID'",
  "corda.group.protocol.registration": "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
  "corda.group.protocol.synchronisation": "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
  "corda.group.protocol.p2p.mode": "Authenticated_Encryption",
  "corda.group.key.session.policy": "Combined",
  "corda.group.pki.session": "NoPKI",
  "corda.group.pki.tls": "Standard",
  "corda.group.tls.version": "1.3",
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1",
  "corda.group.truststore.tls.0" : "'$TLS_CA_CERT'"
}'
```
<!--Optionally, you can set the session certificate trustroot with the property `corda.group.truststore.session.0`, similar to `corda.group.truststore.tls.0`, however when `corda.group.pki.session` is set to `NoPKI` the session certificates are not validated against a session trustroot. At time of writing session certificates are not supported at the P2P level.-->

## Register MGM

To register the MGM, run this command:
```
curl --insecure -u admin:admin -d '{"memberRegistrationRequest":{"action": "requestJoin", "context": '$REGISTRATION_CONTEXT'}}' $API_URL/membership/$MGM_HOLDING_ID
```

For example:
``` shell
curl --insecure -u admin:admin -d '{ "memberRegistrationRequest": { "action": "requestJoin", "context": {
  "corda.session.key.id": "D2FAF709052F",
  "corda.ecdh.key.id": "D2FAF709052F",
  "corda.group.protocol.registration": "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
  "corda.group.protocol.synchronisation": "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
  "corda.group.protocol.p2p.mode": "Authenticated_Encryption",
  "corda.group.key.session.policy": "Distinct",
  "corda.group.pki.session": "NoPKI",
  "corda.group.pki.tls": "Standard",
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
  jq --arg session_key_id $SESSION_KEY_ID '.memberRegistrationRequest.context."corda.ecdh.key.id"=$session_key_id' | \
  jq '.memberRegistrationRequest.context."corda.group.protocol.registration"="net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService"' | \
  jq '.memberRegistrationRequest.context."corda.group.protocol.synchronisation"="net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl"' | \
  jq '.memberRegistrationRequest.context."corda.group.protocol.p2p.mode"="Authenticated_Encryption"' | \
  jq '.memberRegistrationRequest.context."corda.group.key.session.policy"="Combined"' | \
  jq '.memberRegistrationRequest.context."corda.group.pki.session"="NoPKI"' | \
  jq '.memberRegistrationRequest.context."corda.group.pki.tls"="Standard"' | \
  jq '.memberRegistrationRequest.context."corda.group.tls.version"="1.3"' | \
  jq '.memberRegistrationRequest.context."corda.group.key.session.policy"="Combined"' | \
  jq --arg p2p_url "https://$P2P_GATEWAY_HOST:$P2P_GATEWAY_PORT" '.memberRegistrationRequest.context."corda.endpoints.0.connectionURL"=$p2p_url' | \
  jq '.memberRegistrationRequest.context."corda.endpoints.0.protocolVersion"="1"' | \
  jq --rawfile root_certicicate /tmp/ca/ca/root-certificate.pem '.memberRegistrationRequest.context."corda.group.truststore.tls.0"=$root_certicicate' \
) $API_URL/membership/$MGM_HOLDING_ID
```

This should return a successful response with the status `SUBMITTED`. You can confirm if the MGM was onboarded successfully by checking the status of the registration request:
```shell
export REGISTRATION_ID=<registration ID>
curl --insecure -u admin:admin -X GET $API_URL/membership/$MGM_HOLDING_ID/$REGISTRATION_ID
```
If successful, you should see the `APPROVED` registration status.

## Configure the Virtual Node as a Network Participant

To configure the MGM virtual node with properties required for P2P messaging, run this command:

```shell
curl -k -u admin:admin -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "p2pTlsTenantId": "p2p", "sessionKeyId": "'$SESSION_KEY_ID'"}' $API_URL/network/setup/$MGM_HOLDING_ID
```

This configures the locally hosted identity, which is required in order for the P2P messaging to work.
* `p2pTlsCertificateChainAlias` refers to the alias used when importing the TLS certificate.
* `p2pTlsTenantId` refers to the tenant ID under which the TLS cert was stored ("p2p" for cluster level).
* `sessionKeyId` refers to the session key ID previously generated**.


## Export the Group Policy

Now that the MGM is onboarded, the MGM can export a group policy file with the connection details of the MGM. To output the full contents of the `GroupPolicy.json` file that should be packaged within the CPI for members, run this command:
```shell
mkdir -p ~/Desktop/register-member
curl --insecure -u admin:admin -X GET $API_URL/mgm/$MGM_HOLDING_ID/info > ~/Desktop/register-member/GroupPolicy.json
```

You can now use the MGM to [set up members in your network](dynamic-onboarding.html).
