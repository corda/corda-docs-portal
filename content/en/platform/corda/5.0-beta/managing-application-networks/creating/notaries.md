---
date: '2023-02-23'
title: "Onboarding Notaries"
menu:
  corda-5-beta:
    identifier: corda-5-beta-app-networks-notaries
    parent: corda-5-beta-app-networks-create
    weight: 3000
section_menu: corda-5-beta
---
This section describes how to onboard a new member as a notary service representative. It assumes that you have configured the [MGM for the network]({{< relref "./mgm/overview.md" >}}). Onboarding a notary member is similar to any other member, but with the exceptions outlined on this page. The sections must be completed in the order in which they are presented:

1. [Build the member CPI]({{< relref "./members/cpi.md">}}). For information about developing a notary CPB, see [Notary Plugin CorDapps]({{< relref "../../developing/notaries/plugin-cordapps-notary.md" >}}).
2. [Create a member virtual node]({{< relref "./members/virtual-node.md">}}).
3. [Generate a notary key pair]({{< relref "#generate-a-notary-key-pair">}}).
4. [Configure the member communication properties]({{< relref "./members/config-node.md">}}).
5. [Register the notary.]({{< relref "#register-the-notary">}}).

{{< note >}}
The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.
{{< /note >}}

## Generate a Notary Key Pair

{{< note >}}
This step is only necessary if you are onboarding a member as a notary.
{{< /note >}}

Generate notary keys in a similar way as done for other key types. First, create a HSM, then generate the key and store the ID:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -u $REST_API_USER:$REST_API_PASSWORD -X POST $API_URL/hsm/soft/$HOLDING_ID/NOTARY
curl -u $REST_API_USER:$REST_API_PASSWORD -X POST $API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-notary/category/NOTARY/scheme/CORDA.ECDSA.SECP256R1
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/hsm/soft/$HOLDING_ID/NOTARY"
$LEDGER_KEY_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/keys/$HOLDING_ID/alias/$HOLDING_ID-notary/category/NOTARY/scheme/CORDA.ECDSA.SECP256R1"
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
  "corda.session.key.id": "'$SESSION_KEY_ID'",
  "corda.session.key.signature.spec": "SHA256withECDSA",
  "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
  "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
  "corda.notary.keys.0.id": "$NOTARY_KEY_ID",
  "corda.notary.keys.0.signature.spec": "SHA256withECDSA"
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1",
  "corda.roles.0": "notary",
  "corda.notary.service.name": <An X500 name for the notary service>,
  "corda.notary.service.plugin": "net.corda.notary.NonValidatingNotary"
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
  "corda.notary.keys.0.id" = "$NOTARY_KEY_ID",
  "corda.notary.keys.0.signature.spec" = "SHA256withECDSA"
  'corda.endpoints.0.connectionURL' = "https://$P2P_GATEWAY_HOST`:$P2P_GATEWAY_PORT"
  'corda.endpoints.0.protocolVersion' = "1"
  'corda.roles.0' = "notary",
  'corda.notary.service.name' = <An X500 name for the notary service>,
  'corda.notary.service.plugin' = "net.corda.notary.NonValidatingNotary"
}
```
{{% /tab %}}
{{< /tabs >}}

### Register the Notary

To register a member, run the following command:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -u $REST_API_USER:$REST_API_PASSWORD -d '{ "memberRegistrationRequest": { "action": "requestJoin", "context": '$REGISTRATION_CONTEXT' } }' $API_URL/membership/$HOLDING_ID
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

This sends a join request to the MGM. The response should be `SUBMITTED`.

### Confirm Registration

You can confirm if the notary was onboarded successfully by checking the status of the registration request:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export REGISTRATION_ID=<registration-ID>
curl -u $REST_API_USER:$REST_API_PASSWORD -X GET $API_URL/membership/$HOLDING_ID/$REGISTRATION_ID
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
```bash
curl -u $REST_API_USER:$REST_API_PASSWORD -X GET $API_URL/members/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
 Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$HOLDING_ID" | ConvertTo-Json -Depth 4
```
{{% /tab %}}
{{< /tabs >}}