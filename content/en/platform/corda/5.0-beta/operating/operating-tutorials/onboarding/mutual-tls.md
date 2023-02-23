---
date: '2022-11-15'
title: "Configuring Mutual TLS"
menu:
  corda-5-beta:
    identifier: corda-5-beta-mgm-onboarding-tls
    parent: corda-5-beta-tutorials-deploy-dynamic
    weight: 4000
section_menu: corda-5-beta
---
As described in the [mutual TLS introduction](../../mutual-tls.md), you can configure the clusters in a dynamic network to connect using mutual TLS. This requires additional steps when onboarding an MGM or member into the dynamic network.

{{< note >}}
* Mutual TLS is set per cluster. It must apply to all groups that the cluster hosts and all clusters that host those groups. You can not onboard a member unless the TLS type of the MGM cluster is aligned with the TLS type of the member cluster.
* Changing the TLS type after a member or an MGM was onboarded, makes any TLS connection with that member unusable.
* A virtual node can only be configured with a single TLS certificate that will be used as both a client and a server certificate.
* A gateway accepts a TLS connection that uses a certificate associated with any member of any application network (partially) hosted in that cluster.
{{< /note >}}

## Modify the Cluster Configurations

To configure a cluster to use mutual TLS, you must set the `sslConfig.tlsType` flag in the `corda.p2p.gateway` configuration to `MUTUAL` for the following:
* The MGM cluster before registering the MGM
* All member clusters before uploading the CPI

### Enable Mutual TLS Using Bash

If using Bash, perform the following steps to enable mutual TLS by configuring the gateway SSL:

1. Retrieve the current gateway configuration version:

   ```shell
   curl --insecure -u admin:admin -X GET $API_URL/config/corda.p2p.gateway
   ```

2. Store the version number from the response:

   ```shell
   export CONFIG_VERSION=<configuration-version>
   ```

3. Using that version number, send the following request:

   ```shell
   curl -k -u admin:admin -X PUT -d '{"section":"corda.p2p.gateway", "version":"'$CONFIG_VERSION'", "config":"{ \"sslConfig\": { \"tlsType\": \"MUTUAL\"  }  }", "schemaVersion": {"major": 1, "minor": 0}}' $API_URL"/config"
   ```
   This command overwrites the revocation check setting. If you chose to disable revocation checks, use the following command instead:

   ```shell
   curl -k -u admin:admin -X PUT -d '{"section":"corda.p2p.gateway", "version":"'$CONFIG_VERSION'", "config":"{ \"sslConfig\": { \"tlsType\": \"MUTUAL\" , \"revocationCheck\": {\"mode\" : \"OFF\"} } }", "schemaVersion": {"major": 1, "minor": 0}}' $API_URL"/config"
   ```

### Enable Mutual TLS Using PowerShell

If using PowerShell, perform the following steps to enable mutual TLS by configuring the gateway SSL:

   ```shell
   $CONFIG_VERSION = (Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/config/corda.p2p.gateway").version
   Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
    section = "corda.p2p.gateway"
    version = $CONFIG_VERSION
    config = @{
        sslConfig = @{
            tlsType = "MUTUAL"
        }
    }
    schemaVersion = @{
        major = 1
        minor = 0
    }
  })

   ```

This command overwrites the revocation check setting. If you chose to disable revocation checks, use the following command instead:
```shell
$CONFIG_VERSION = (Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/config/corda.p2p.gateway").version
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Put -Uri "$API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
    section = "corda.p2p.gateway"
    version = $CONFIG_VERSION
    config = @{
        sslConfig = @{
            revocationCheck = @{
                mode = "OFF"
            }
            tlsType = "MUTUAL"
        }
    }
    schemaVersion = @{
        major = 1
        minor = 0
    }
})
```

## Set the TLS Type in the MGM Context

To register an MGM in a mutual TLS cluster, you must explicitly set the TLS type in the registration context. That is, the `corda.group.tls.type` field must be `Mutual`. If the field is not set, it defaults to one-way TLS. For example:
```shell
export REGISTRATION_CONTEXT='{
  "corda.session.key.id": "'$SESSION_KEY_ID'",
  "corda.ecdh.key.id": "'$ECDH_KEY_ID'",
  "corda.group.protocol.registration": "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
  "corda.group.protocol.synchronisation": "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
  "corda.group.protocol.p2p.mode": "Authenticated_Encryption",
  "corda.group.key.session.policy": "Combined",
  "corda.group.pki.session": "NoPKI",
  "corda.group.pki.tls": "Standard",
  "corda.group.tls.type": "Mutual",
  "corda.group.tls.version": "1.3",
  "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
  "corda.endpoints.0.protocolVersion": "1",
  "corda.group.truststore.tls.0" : "'$TLS_CA_CERT'"
}'
```

## Update the MGM Allowed Certificate Subject List

Before a member can register with a cluster that is configured with mutual TLS, you must add the certificate subject of that member to the allowed list of the MGM. Otherwise, the MGM gateway will reject the connection and the member will not be able to register. When the member is successfully onboarded, the MGM then distributes the certificate subject of the member to all other members in the group. The gateway in each member cluster uses this to accept TLS connections from any onboarded member.

To add a member TLS certificate subject to the MGM allowed list, run the following, where `CN=CordaOperator,C=GB,L=London,O=Org` is the subject of the TLS certificate created as part of [member onboarding](dynamic-onboarding.html#tls-key-pair-and-certificate):

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u admin:admin -X PUT  "$MGM_API_URL/mgm/$MGM_HOLDING_ID/mutual-tls/allowed-client-certificate-subjects/CN=CordaOperator,C=GB,L=London,O=Org"
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$MGM_API_URL/mgm/$MGM_HOLDING_ID/mutual-tls/allowed-client-certificate-subjects/CN=CordaOperator,C=GB,L=London,O=Org" -Method Put
```
{{% /tab %}}
{{< /tabs >}}

The `allowed-client-certificate-subjects` API also supports a `DELETE` and `GET` to manage the accepted list of certificates by the MGM. For example:
```shell
curl -k -u admin:admin -X DELETE  "$MGM_API_URL/mgm/$MGM_HOLDING_ID/mutual-tls/allowed-client-certificate-subjects/CN=CordaOperatorTwo,C=GB,L=London,O=Org"
curl -k -u admin:admin -X PUT  "$MGM_API_URL/mgm/$MGM_HOLDING_ID/mutual-tls/allowed-client-certificate-subjects/CN=CordaOperatorThree,C=GB,L=London,O=Org"
curl -k -u admin:admin "$MGM_API_URL/mgm/$MGM_HOLDING_ID/mutual-tls/allowed-client-certificate-subjects"
```