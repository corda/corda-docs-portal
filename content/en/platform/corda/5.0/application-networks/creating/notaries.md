---
date: '2023-02-23'
version: 'Corda 5.0'
title: "Onboarding Notaries"
menu:
  corda5:
    identifier: corda5-networks-notaries
    parent: corda5-networks-create
    weight: 3000
section_menu: corda5
---
# Onboarding Notaries 
This section describes how to onboard a new member as a notary service representative. It assumes that you have configured the [MGM for the network]({{< relref "./mgm/_index.md" >}}). Onboarding a notary member is similar to any other member, but with the exceptions outlined on this page. 

{{< note >}}
When onboarding a notary, you need to use the notary CPK to build a notary CPI.
{{< /note >}}

The sections must be completed in the following order:

1. Download the notary server CPB, which is available from our [GitHub release page](https://github.com/corda/corda-runtime-os/releases/).
2. [Build the notary member CPI]({{< relref "./members/cpi.md">}}) using the Notary CPB. For information about the notary CPB, see the [Notary section of Developing Applications]({{< relref "../../developing-applications/notaries/_index.md#notary-server-cpb" >}}).
3. [Import Notary CPB Code Signing Certificate]({{< relref "#import-notary-cpb-code-signing-certificate">}}). This is in addition to importing certificates for application CPKs or CPBs.
4. [Create a member virtual node]({{< relref "./members/virtual-node.md">}}), specifying the hash of the notary CPI.
5. [Generate a notary key pair]({{< relref "#generate-a-notary-key-pair">}}).
6. [Configure the member communication properties]({{< relref "./members/config-node.md">}}).
7. [Register the notary]({{< relref "#register-the-notary">}}).

{{< note >}}
The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.
{{< /note >}}

## Import Notary CPB Code Signing Certificate

The R3 notary server CPB is signed with a DigiCert KMS signing key. To use it, import the certificate as follows:
1. Save the following text into a file named `notary-ca-root.pem`:
   ```shell
   -----BEGIN CERTIFICATE-----
   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
   -----END CERTIFICATE-----
   ```

2. Import the `notary-ca-root.pem` file into the keystore:
   ```
   keytool -importcert -keystore signingkeys.pfx -storepass <keystore-password> -noprompt -alias notary-ca-root -file notary-ca-root.pem
   ```

3. Export the signing key certificate from the keystore:
   ```
   keytool -exportcert -rfc -alias notary-ca-root -keystore signingkeys.pfx -storepass <keystore-password> -file notary-ca-root.pem
   ```

4. Import the signing key into Corda:
   ```
   curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X PUT -F alias=notary-ca-root -F certificate=@notary-ca-root.pem $REST_API_URL/certificates/cluster/code-signer
   ```
## Generate a Notary Key Pair

Generate notary keys in a similar way as done for other key types. First, create a HSM, then generate the key and store the ID:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/hsm/soft/$HOLDING_ID/NOTARY
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X POST $REST_API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-notary/category/NOTARY/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/hsm/soft/$HOLDING_ID/NOTARY"
$LEDGER_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-notary/category/NOTARY/scheme/CORDA.ECDSA.SECP256R1"
$NOTARY_KEY_ID = $NOTARY_KEY_RESPONSE.id
```
{{% /tab %}}
{{< /tabs >}}

If using Bash, the result contains the notary key ID (for example, 3B9A266F96E2). Run the following command to save this ID for use in subsequent steps:
```shell
export NOTARY_KEY_ID=<notary-key-ID>
```

## Register the Notary

### Build the Notary Registration Context

Run the following command to build the registration context for a notary member:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export REGISTRATION_CONTEXT='{
  "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
  "corda.session.keys.0.signature.spec": "SHA256withECDSA",
  "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
  "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
  "corda.notary.keys.0.id": "$NOTARY_KEY_ID",
  "corda.notary.keys.0.signature.spec": "SHA256withECDSA"
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1",
  "corda.roles.0": "notary",
  "corda.notary.service.name": <An X.500 name for the notary service>,
  "corda.notary.service.flow.protocol.name": "com.r3.corda.notary.plugin.nonvalidating",
  "corda.notary.service.flow.protocol.version.0": "1"
}'
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REGISTRATION_CONTEXT = @{
  'corda.session.keys.0.id' =  $SESSION_KEY_ID
  'corda.session.keys.0.signature.spec' = "SHA256withECDSA"
  'corda.ledger.keys.0.id' = $LEDGER_KEY_ID
  'corda.ledger.keys.0.signature.spec' = "SHA256withECDSA"
  'corda.notary.keys.0.id' = "$NOTARY_KEY_ID",
  'corda.notary.keys.0.signature.spec' = "SHA256withECDSA"
  'corda.endpoints.0.connectionURL' = "https://$P2P_GATEWAY_HOST`:$P2P_GATEWAY_PORT"
  'corda.endpoints.0.protocolVersion' = "1"
  'corda.roles.0' = "notary",
  'corda.notary.service.name' = <An X.500 name for the notary service>,
  'corda.notary.service.flow.protocol.name' = "com.r3.corda.notary.plugin.nonvalidating",
  'corda.notary.service.flow.protocol.version.0' = "1"
}
```
{{% /tab %}}
{{< /tabs >}}

This sets the following notary specific values:
* `'corda.roles.0' : "notary"` -  This indicates that the virtual node is taking the role of a notary on the network.
* `"corda.notary.service.name" : <x500 name>` - This specifies an X.500 name for the notary service that this virtual node will represent. This is the name that will be used by CorDapps when specifying which notary to use for notarization.
* `"corda.notary.service.flow.protocol.name" : "com.r3.corda.notary.plugin.nonvalidating"` - This attribute replaces the validating Boolean flag in Corda 4. This is effectively the equivalent to setting `validating = false` in Corda 4.
* `"corda.notary.service.flow.protocol.version.0" : "1"` - This must be specified and currently must be set to version 1. The 0 at the end of the name reflects the fact that in future there may be multiple versions supported, with additional versions specified by 1,2, and so on. 

{{< note >}}
It is currently only possible to have a single notary virtual node associated with a notary service X.500 name. The eventual intent is to allow a many-to-one mapping, similar to the HA notary implementation in Corda 4. This will allow a notary service to be hosted across multiple Corda clusters/regions.
{{< /note >}}
### Register the Notary

To register a member, run the following command:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -d '{ "memberRegistrationRequest": { "context": '$REGISTRATION_CONTEXT' } }' $REST_API_URL/membership/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REGISTER_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/membership/$HOLDING_ID" -Body (ConvertTo-Json -Depth 4 @{
    memberRegistrationRequest = @{
        context = $REGISTRATION_CONTEXT
    }
})
$REGISTER_RESPONSE.registrationStatus
```
{{% /tab %}}
{{< /tabs >}}

This sends a join request to the MGM. The response should be `SUBMITTED`.

### Confirm Registration

You can confirm if the notary was onboarded successfully by checking the status of the registration request:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export REGISTRATION_ID=<registration-ID>
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/membership/$HOLDING_ID/$REGISTRATION_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/membership/$HOLDING_ID/${REGISTER_RESPONSE.registrationId}"
```
{{% /tab %}}
{{< /tabs >}}

If successful, you should see the `APPROVED` registration status.

After registration, you can use the look-up functions provided by the `MemberLookupRpcOps` to confirm that your member can see other members and has `ACTIVE` membership status:
{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/members/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
 Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/membership/$HOLDING_ID" | ConvertTo-Json -Depth 4
```
{{% /tab %}}
{{< /tabs >}}