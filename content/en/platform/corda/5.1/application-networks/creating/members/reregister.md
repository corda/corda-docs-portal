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

A {{< tooltip >}}member{{< /tooltip >}} may request to update its own member-provided context, for example,
after key rotation or changes to its endpoint information. Additionally, a member who previously attempted to register but
failed may wish to try again. The membership re-registration steps described in this section can be followed for both of these scenarios.

The instructions on this page assume that you have completed the [registration]({{< relref "register.md" >}}) steps.

You can learn more about configuring the registration process in the [Managing Members section]({{< relref "../../managing/registration-requests/_index.md" >}}).

1. Inspect the member-provided context.

   Currently, updates to the member-provided context are limited to custom properties (keys with the `ext.` prefix) and endpoint
   information only. Changes to other Corda platform properties are not currently supported.

   You can inspect a member's current member-provided context either by performing a member lookup, or by looking up its latest
   registration request. For example, to look up Alice:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```bash
   curl -k -u admin:admin -X GET $API_URL/members/$HOLDING_ID?O=Alice
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
   curl -k -u admin:admin -X GET $API_URL/membership/$HOLDING_ID/$REGISTRATION_ID
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
   curl -k -u admin:admin -X GET $API_URL/keys/$HOLDING_ID
   ```

   The following is an example of a member-provided context for a member who has previously registered successfully:

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

2. Add a custom property to the member-provided context. In this example, the updated context contains the new custom property with the `ext.` prefix:

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

3. Optional: Include serial number in the registration context.

   The `corda.serial` Corda platform property is embedded in the `MemberInfo` of all members. It acts as the `MemberInfo`'s version,
   and is incremented by 1 after each registration.

   This serial number may be optionally included in the registration context to specify which version of the `MemberInfo` was
   intended to be updated. If no serial number is provided while re-registering, the platform uses the member's latest
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

4. Send a re-registration request using the common [registration/re-registration endpoint](../../../reference/rest-api/openapi.html#tag/Member-Registration-API/operation/get_membership__holdingidentityshorthash_).

   If a member submits more than one registration request at the same time, the MGM queues the requests and processes them
   one by one, treating each subsequent request in the queue as a re-registration attempt.

   If a member submits multiple re-registration requests with the same serial number, the MGM processes the first request
   (if the serial number is valid). The MGM declines the other requests because the serial number specified in
   those requests is outdated after the first request is completed.

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```bash
   export REGISTRATION_REQUEST='{"memberRegistrationRequest":{"context": '$REGISTRATION_CONTEXT'}}'
   curl -k -u admin:admin -d "$REGISTRATION_REQUEST" $API_URL/membership/$HOLDING_ID
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
