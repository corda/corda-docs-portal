---
date: '2023-04-07'
version: 'Corda 5.0'
title: "Register the MGM"
menu:
  corda5:
    parent: corda5-networks-mgm
    identifier: corda5-networks-mgm-register
    weight: 4000
section_menu: corda5
---

# Register the MGM

This section describes how to register the MGM on a network. It contains the following:
1. [Build Registration Context]({{< relref "#build-registration-context" >}})
2. [Register the MGM]({{< relref "#register-the-mgm" >}})
3. [Confirm Registration]({{< relref "#confirm-registration" >}})

## Build Registration Context

To register the MGM, you must first generate the registration context:
* [Build Registration Context Using Bash]({{< relref "#build-registration-context-using-bash">}})
* [Build Registration Context Using PowerShell]({{< relref "#build-registration-context-using-powershell">}})

The examples in this section set `corda.group.key.session.policy` to `Distinct`, indicating that the ledger and session initiation key must not be the same key. Alternatively, setting `corda.group.key.session.policy` to `Combined` means that the ledger key used by a member must be the same as the session initiation key.

{{< note >}}
* If you want to use certificates for session initiation keys for peer-to-peer communication, see [Configuring Optional Session Certificates]({{< relref "../optional/session-certificates.html#build-registration-context-for-mgm-registration" >}}) for information about the additional JSON fields required in the registration context.
* If you want to use mutual TLS, see [Configuring Mutual TLS]({{< relref "../optional/mutual-tls-connections.md#set-the-tls-type-in-the-mgm-context" >}}) for additonal configuration steps. 
{{< /note >}}

### Build Registration Context Using Bash

To build the registration context using Bash, run the following command, replacing `<TLS-CA-CERT>` with the PEM format certificate of the CA. This is the trustroot used to validate member certificates.
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
  "corda.group.trustroot.tls.0" : "'$TLS_CA_CERT'"
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
  'corda.group.trustroot.tls.0'  =  [IO.File]::ReadAllText($TLS_CA_CERT_PATH)
}
```
## Register the MGM

You can now use the registration context to register the MGM on the network:
* [Register the MGM using Bash]({{< relref "#register-the-mgm-using-bash">}})
* [Register the MGM using PowerShell]({{< relref "#register-the-mgm-using-powershell">}})

### Register the MGM using Bash

To register the MGM using Bash, run this command:
```shell
REGISTRATION_REQUEST='{"memberRegistrationRequest":{"context": '$REGISTRATION_CONTEXT'}}'
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -d "$REGISTRATION_REQUEST" $REST_API_URL/membership/$MGM_HOLDING_ID
```
For example:
``` shell
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -d '{ "memberRegistrationRequest": { "context": {
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
  "corda.group.trustroot.tls.0" : "-----BEGIN CERTIFICATE-----\nMIIBLjCB1aADAgECAgECMAoGCCqGSM49BAMCMBAxDjAMBgNVBAYTBVVLIENOMB4X\nDTIyMDgyMzA4MDUzN1oXDTIyMDkyMjA4MDUzN1owEDEOMAwGA1UEBhMFVUsgQ04w\nWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAASG6ijAvbmaIaIwKpZZqTeKmMKfoOPb\ncCK/BqdtKXVTt5AjJtiP/Uoq+481UEQyaUZYXGf5rC1owjT40U2B71qdoyAwHjAP\nBgNVHRMBAf8EBTADAQH/MAsGA1UdDwQEAwIBrjAKBggqhkjOPQQDAgNIADBFAiEA\n1h6WEfdWUXSjBcenf5ycXPkYQQzI92I54q2WaVVjQHwCIEBk1ov/hYp9RCCDPnJx\nk8WgCZIyhFe0pEmow7MuI/Zk\n-----END CERTIFICATE-----"
} } }' https://localhost:8888/api/v1/membership/EF19BF67E77C
```

Alternatively, using jq:
```shell
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -d $(
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
  jq --rawfile root_certicicate /tmp/ca/ca/root-certificate.pem '.memberRegistrationRequest.context."corda.group.trustroot.tls.0"=$root_certicicate' \
) $REST_API_URL/membership/$MGM_HOLDING_ID
```

### Register the MGM using PowerShell

To register the MGM using PowerShell, run this command:
```shell
$REGISTER_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$REST_API_URL/membership/$MGM_HOLDING_ID" -Body (ConvertTo-Json -Depth 4 @{
    memberRegistrationRequest = @{
        context = $REGISTRATION_CONTEXT
    }
})
$REGISTER_RESPONSE.registrationStatus
```
### Confirm Registration

Registration should return a successful response with the status `SUBMITTED`.
You can confirm that the MGM was onboarded successfully by checking the status of the registration request. The registration ID is returned from the member regsitration request:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
export REGISTRATION_ID=<registration-ID>
curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/membership/$MGM_HOLDING_ID/$REGISTRATION_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/membership/$MGM_HOLDING_ID/${RESGISTER_RESPONSE.registrationId}"
```
{{% /tab %}}
{{< /tabs >}}
If successful, you should see the `APPROVED` registration status.
