---
date: '2023-04-13'
title: "Register the Member"
menu:
  corda5:
    identifier: corda5-networks-members-register
    parent: corda5-networks-members
    weight: 5000
section_menu: corda5

---

This section describes how to register a member on a network. You can learn more about configuring the registration process in the [Managing Members section]({{< relref "../../managing/registration-requests/registration-approval.md" >}}).
This section contains the following:
1. [Build Registration Context]({{< relref "#build-registration-context" >}})
2. [Register the Member]({{< relref "#register-the-member" >}})
3. [Confirm Registration]({{< relref "#confirm-registration" >}})

## Build Registration Context
{{< note >}}
You can retrieve the names available for signature-spec through `KeysRpcOps`. One of them is used as an example below.
{{< /note >}}<!--will need more info-->

To build the registration context, run the following command, replacing the endpoint URL with the endpoint of the P2P gateway.
For example, `https://corda-p2p-gateway-worker.corda-cluster-a:8080`, where `corda-p2p-gateway-worker` is the name of the P2P gateway Kubernetes service and `corda-cluster-a` is the namespace that the Corda cluster is deployed within.
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

## Register the Member

To register a member, run the following command:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -u $REST_API_USER:$REST_API_PASSWORD -d '{ "memberRegistrationRequest": { "context": '$REGISTRATION_CONTEXT' } }' $API_URL/membership/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
$REGISTER_RESPONSE = Invoke-RestMethod -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/membership/$HOLDING_ID" -Body (ConvertTo-Json -Depth 4 @{
    memberRegistrationRequest = @{
       context = $REGISTRATION_CONTEXT
    }
})
$REGISTER_RESPONSE.registrationStatus
```
{{% /tab %}}
{{< /tabs >}}

This sends a join request to the MGM. The response should be `SUBMITTED`.

If you are using the Swagger UI, use the following:
```shell
{
  "memberRegistrationRequest":{
    "context": <registration-context>
  }
}
```

## Confirm Registration

You can confirm if the member was onboarded successfully by checking the status of the registration request:
{{< tabs >}}
{{% tab name="Bash"%}}
```
export REGISTRATION_ID=<registration-ID>
curl -u $REST_API_USER:$REST_API_PASSWORD -X GET $API_URL/membership/$HOLDING_ID/$REGISTRATION_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$HOLDING_ID/${REGISTER_RESPONSE.registrationId}"
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
 Invoke-RestMethod -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/membership/$HOLDING_ID" | ConvertTo-Json -Depth 4
```
{{% /tab %}}
{{< /tabs >}}