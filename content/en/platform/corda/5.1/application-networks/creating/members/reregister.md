---
date: '2023-10-04'
version: 'Corda 5.1'
title: "Re-register a Member"
menu:
  corda51:
    identifier: corda51-networks-members-reregister
    parent: corda51-networks-members
    weight: 6000
section_menu: corda51
---

# Re-register a Member

In certain cases, a {{< tooltip >}}member{{< /tooltip >}} may request to update its own member-provided context, for example,
after key rotation or changes to its endpoint information. Additionally, a member who previously attempted to register but
failed may wish to try again. The membership re-registration steps described in this section can be followed for both of these scenarios.

The instructions on this page assume that you have completed the [registration]({{< relref "register.md" >}}) steps.

You can learn more about configuring the registration process in the [Managing Members section]({{< relref "../../managing/registration-requests/_index.md" >}}).

This section contains the following:
1. [Inspect Member-Provided Context]({{< relref "#inspect-member-provided-context" >}})
2. [Re-register a Member]({{< relref "#re-register-a-member-1" >}})
3. [Optional: Include Serial Number in the Registration Context]({{< relref "#optional-include-serial-number-in-the-registration-context" >}})
4. [Request Queue]({{< relref "#request-queue" >}})

## Inspect Member-Provided Context

Currently, updates to the member-provided context are limited to custom properties (keys with the `ext.` prefix) and endpoint
information only. Changes to other Corda platform properties are not supported at the moment.

A member may inspect its current member-provided context either by performing a member lookup, or by looking up its latest
registration request. For example, to look up Alice:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl --insecure -u admin:admin -X GET $API_URL/members/$HOLDING_ID?O=Alice
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$HOLDING_ID?O=Alice" | ConvertTo-Json -Depth 4
```
{{% /tab %}}
{{< /tabs >}}

Alternatively, to retrieve the registration request:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
export REGISTRATION_ID=<registration ID>
curl --insecure -u admin:admin -X GET $API_URL/membership/$HOLDING_ID/$REGISTRATION_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REGISTRATION_ID = <registration ID>
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$HOLDING_ID/$REGISTRATION_ID"
```
{{% /tab %}}
{{< /tabs >}}

To retrieve information about key pairs (for example, key ID required for the registration context) belonging to a
holding identity, use:

```bash
curl --insecure -u admin:admin -X GET $API_URL/keys/$HOLDING_ID
```

## Re-register a Member

Consider a member who has previously registered successfully with the following member-provided context:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
REGISTRATION_CONTEXT='{
  "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
  "corda.session.keys.0.signature.spec": "SHA256withECDSA",
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
  'corda.session.keys.0.id' =  $SESSION_KEY_ID
  'corda.session.keys.0.signature.spec' = "SHA256withECDSA"
  'corda.ledger.keys.0.id' = $LEDGER_KEY_ID
  'corda.ledger.keys.0.signature.spec' = "SHA256withECDSA"
  'corda.endpoints.0.connectionURL' = "https://$P2P_GATEWAY_HOST`:$P2P_GATEWAY_PORT"
  'corda.endpoints.0.protocolVersion' = "1"
}
```
{{% /tab %}}
{{< /tabs >}}

The member now wishes to add a custom property to its member-provided context, and must re-register with the updated context:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
export REGISTRATION_CONTEXT='{
  "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
  "corda.session.keys.0.signature.spec": "SHA256withECDSA",
  "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
  "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1",
  "ext.sample": "apple"
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
  'corda.endpoints.0.connectionURL' = "https://$P2P_GATEWAY_HOST`:$P2P_GATEWAY_PORT"
  'corda.endpoints.0.protocolVersion' = "1",
  'ext.sample' = "apple"
}
```
{{% /tab %}}
{{< /tabs >}}

The updated context contains the new custom property with the `ext.` prefix. The member sends a re-registration request
using the common registration/re-registration endpoint:

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
export REGISTRATION_REQUEST='{"memberRegistrationRequest":{"context": '$REGISTRATION_CONTEXT'}}'
curl --insecure -u admin:admin -d "$REGISTRATION_REQUEST" $API_URL/membership/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$RESGISTER_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/membership/$HOLDING_ID" -Body (ConvertTo-Json -Depth 4 @{
    memberRegistrationRequest = @{
        context = $REGISTRATION_CONTEXT
    }
})
$RESGISTER_RESPONSE.registrationStatus
```
{{% /tab %}}
{{< /tabs >}}

This sends the request to the MGM, which should return a successful response with status `SUBMITTED`. You can check if the
request was approved by checking the status of the registration request.

After successful re-registration, you should be able to see the member's information containing the `ext.sample` field in
their member-provided context. The member retains its most recent status in the group, for example, a suspended member
will remain suspended after successful re-registration.

## **Optional:** Include Serial Number in the Registration Context

The `corda.serial` Corda platform property is embedded in the `MemberInfo` of all members. It acts as the `MemberInfo`'s version,
and is incremented by 1 after each registration.

This serial number may be optionally included in the registration context to specify which version of the `MemberInfo` was
intended to be updated. If no serial number is provided while re-registering, the platform will use the member's latest
serial number by default. Only the latest `MemberInfo` version may be updated - requests with an older serial number are declined.
It is recommended to provide the serial number to avoid unintentional updates, in case you have an outdated version of the `MemberInfo`.

You can retrieve the serial number from the MGM-provided context of the `MemberInfo` by performing a member lookup.

{{< note >}}
For first-time registration the serial number should be 0, if provided.
{{< /note >}}

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
export REGISTRATION_CONTEXT='{
  "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
  "corda.session.keys.0.signature.spec": "SHA256withECDSA",
  "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
  "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1",
  "ext.sample": "apple",
  "corda.serial": "1"
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
  'corda.endpoints.0.connectionURL' = "https://$P2P_GATEWAY_HOST`:$P2P_GATEWAY_PORT"
  'corda.endpoints.0.protocolVersion' = "1",
  'ext.sample' = "apple",
  'corda.serial' = "1"
}
```
{{% /tab %}}
{{< /tabs >}}

## Request Queue

If a member submits more than one registration request at the same time, the MGM will queue the requests and process them
one by one, treating each subsequent request in the queue as a re-registration attempt.

If a member submits multiple re-registration requests with the same serial number, the first request will be processed
(if the serial number is valid). However, the other requests will be declined because the serial number specified in
those requests would be outdated after the first request is completed.
