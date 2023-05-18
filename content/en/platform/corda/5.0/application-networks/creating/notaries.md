---
date: '2023-02-23'
title: "Onboarding Notaries"
menu:
  corda5:
    identifier: corda5-networks-notaries
    parent: corda5-networks-create
    weight: 3000
section_menu: corda5
---
This section describes how to onboard a new member as a notary service representative. It assumes that you have configured the [MGM for the network]({{< relref "./mgm/_index.md" >}}). Onboarding a notary member is similar to any other member, but with the exceptions outlined on this page. The sections must be completed in the following order:

1. Download the notary server CPB, which is available from our [GitHub release page](https://github.com/corda/corda-runtime-os/releases/).
2. [Build the member CPI]({{< relref "./members/cpi.md">}}) using the Notary CPB. For information about the notary CPB, see the [Notary section of Developing Applications]({{< relref "../../developing-applications/notaries/_index.md" >}}).
3. [Import Notary CPB Code Signing Certificate]({{< relref "#import-notary-cpb-code-signing-certificate">}}). This is in addition to importing certificates for application CPKs or CPBs.
4. [Create a member virtual node]({{< relref "./members/virtual-node.md">}}), specifying the hash of the notary CPI.
5. [Generate a notary key pair]({{< relref "#generate-a-notary-key-pair">}}).
6. [Configure the member communication properties]({{< relref "./members/config-node.md">}}).
7. [Register the notary]({{< relref "#register-the-notary">}}).

{{< note >}}
The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.
{{< /note >}}

## Import Notary CPB Code Signing Certificate

The R3 notary server CPB is signed with a DigiCert signing key. To use it, import the certificate as follows:
1. Save the following text into a file named `notary-ca-root.pem`:
   ```shell
   -----BEGIN CERTIFICATE-----
   MIIGsDCCBJigAwIBAgIQCK1AsmDSnEyfXs2pvZOu2TANBgkqhkiG9w0BAQwFADBi
   MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
   d3cuZGlnaWNlcnQuY29tMSEwHwYDVQQDExhEaWdpQ2VydCBUcnVzdGVkIFJvb3Qg
   RzQwHhcNMjEwNDI5MDAwMDAwWhcNMzYwNDI4MjM1OTU5WjBpMQswCQYDVQQGEwJV
   UzEXMBUGA1UEChMORGlnaUNlcnQsIEluYy4xQTA/BgNVBAMTOERpZ2lDZXJ0IFRy
   dXN0ZWQgRzQgQ29kZSBTaWduaW5nIFJTQTQwOTYgU0hBMzg0IDIwMjEgQ0ExMIIC
   IjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1bQvQtAorXi3XdU5WRuxiEL1
   M4zrPYGXcMW7xIUmMJ+kjmjYXPXrNCQH4UtP03hD9BfXHtr50tVnGlJPDqFX/IiZ
   wZHMgQM+TXAkZLON4gh9NH1MgFcSa0OamfLFOx/y78tHWhOmTLMBICXzENOLsvsI
   8IrgnQnAZaf6mIBJNYc9URnokCF4RS6hnyzhGMIazMXuk0lwQjKP+8bqHPNlaJGi
   TUyCEUhSaN4QvRRXXegYE2XFf7JPhSxIpFaENdb5LpyqABXRN/4aBpTCfMjqGzLm
   ysL0p6MDDnSlrzm2q2AS4+jWufcx4dyt5Big2MEjR0ezoQ9uo6ttmAaDG7dqZy3S
   vUQakhCBj7A7CdfHmzJawv9qYFSLScGT7eG0XOBv6yb5jNWy+TgQ5urOkfW+0/tv
   k2E0XLyTRSiDNipmKF+wc86LJiUGsoPUXPYVGUztYuBeM/Lo6OwKp7ADK5GyNnm+
   960IHnWmZcy740hQ83eRGv7bUKJGyGFYmPV8AhY8gyitOYbs1LcNU9D4R+Z1MI3s
   MJN2FKZbS110YU0/EpF23r9Yy3IQKUHw1cVtJnZoEUETWJrcJisB9IlNWdt4z4FK
   PkBHX8mBUHOFECMhWWCKZFTBzCEa6DgZfGYczXg4RTCZT/9jT0y7qg0IU0F8WD1H
   s/q27IwyCQLMbDwMVhECAwEAAaOCAVkwggFVMBIGA1UdEwEB/wQIMAYBAf8CAQAw
   HQYDVR0OBBYEFGg34Ou2O/hfEYb7/mF7CIhl9E5CMB8GA1UdIwQYMBaAFOzX44LS
   cV1kTN8uZz/nupiuHA9PMA4GA1UdDwEB/wQEAwIBhjATBgNVHSUEDDAKBggrBgEF
   BQcDAzB3BggrBgEFBQcBAQRrMGkwJAYIKwYBBQUHMAGGGGh0dHA6Ly9vY3NwLmRp
   Z2ljZXJ0LmNvbTBBBggrBgEFBQcwAoY1aHR0cDovL2NhY2VydHMuZGlnaWNlcnQu
   Y29tL0RpZ2lDZXJ0VHJ1c3RlZFJvb3RHNC5jcnQwQwYDVR0fBDwwOjA4oDagNIYy
   aHR0cDovL2NybDMuZGlnaWNlcnQuY29tL0RpZ2lDZXJ0VHJ1c3RlZFJvb3RHNC5j
   cmwwHAYDVR0gBBUwEzAHBgVngQwBAzAIBgZngQwBBAEwDQYJKoZIhvcNAQEMBQAD
   ggIBADojRD2NCHbuj7w6mdNW4AIapfhINPMstuZ0ZveUcrEAyq9sMCcTEp6QRJ9L
   /Z6jfCbVN7w6XUhtldU/SfQnuxaBRVD9nL22heB2fjdxyyL3WqqQz/WTauPrINHV
   UHmImoqKwba9oUgYftzYgBoRGRjNYZmBVvbJ43bnxOQbX0P4PpT/djk9ntSZz0rd
   KOtfJqGVWEjVGv7XJz/9kNF2ht0csGBc8w2o7uCJob054ThO2m67Np375SFTWsPK
   6Wrxoj7bQ7gzyE84FJKZ9d3OVG3ZXQIUH0AzfAPilbLCIXVzUstG2MQ0HKKlS43N
   b3Y3LIU/Gs4m6Ri+kAewQ3+ViCCCcPDMyu/9KTVcH4k4Vfc3iosJocsL6TEa/y4Z
   XDlx4b6cpwoG1iZnt5LmTl/eeqxJzy6kdJKt2zyknIYf48FWGysj/4+16oh7cGvm
   oLr9Oj9FpsToFpFSi0HASIRLlk2rREDjjfAVKM7t8RhWByovEMQMCGQ8M4+uKIw8
   y4+ICw2/O/TOHnuO77Xry7fwdxPm5yg/rBKupS8ibEH5glwVZsxsDsrFhsP2JjMM
   B0ug0wcCampAMEhLNKhRILutG4UI4lkNbcoFUCvqShyepf2gpx8GdOfy1lKQ/a+F
   SCH5Vzu0nAPthkX0tGFuv2jiJmCG6sivqf6UHedjGzqGVnhO
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

{{< note >}}
This step is only necessary if you are onboarding a member as a notary. When onboarding a notary, you need to use the notary CPK to build a notary CPI.
{{< /note >}}

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
  "corda.session.key.id": "'$SESSION_KEY_ID'",
  "corda.session.key.signature.spec": "SHA256withECDSA",
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
  'corda.session.key.id' =  $SESSION_KEY_ID
  'corda.session.key.signature.spec' = "SHA256withECDSA"
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