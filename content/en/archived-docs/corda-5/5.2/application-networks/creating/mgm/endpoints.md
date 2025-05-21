---
description: "Learn how to make changes to an MGM's endpoint information by re-registering the member with the updated information."
date: '2024-01-11'
title: "Modify an MGM Endpoint"
menu:
  corda52:
    identifier: corda52-networks-mgm-endpoints
    parent: corda52-networks-mgm
    weight: 5500
---

# Modify an MGM Endpoint

If an MGM needs to make changes to their endpoint information (for example, changing the URL of the endpoint or adding a new endpoint), the MGM must [re-register]({{< relref "reregister.md" >}}) with the updated endpoint information.

To minimize communication disruption, the MGM should first configure the P2P Gateway with both the old and new information, before re-registering, and then remove the old information, as follows:

1. Ensure that the cluster can accept connections on the new endpoint.
   In a production environment that exposes the Corda P2P Gateway service via a load balancer, this may require updating the load balancer configuration with the new endpoint.
2. Add the new endpoint information to the cluster's [P2P Gateway configuration]({{< relref "../../../deploying-operating/config/fields/p2p-gateway.md">}}) so that it listens on both the old and new endpoints. For example, to configure two endpoints with different ports, using Bash with Curl or PowerShell:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export NEW_CONFIG='{
   "config": {
     "serversConfiguration":[{"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8080,"urlPath":"/"}, {"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8081,"urlPath":"/"}]
   },
   "schemaVersion": {
     "major": 1,
     "minor": 0
   },
   "section": "corda.p2p.gateway",
   "version": 1
   }'
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -d "$NEW_CONFIG" -X 'PUT' "$REST_API_URL/config"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f ${REST_API_USER}:${REST_API_PASSWORD})} -Method Put -Uri "$REST_API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
      "config": "{
         "serversConfiguration":[{"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8080,"urlPath":"/"}, {"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8081,"urlPath":"/"}]
      }",
      "schemaVersion": {
         "major": 1,
         "minor": 0
      },
      "section": "corda.p2p.gateway",
      "version": 1
    })
   ```
   {{% /tab %}}
   {{< /tabs >}}
3. Update the MGM's registration context with the new endpoint. For example, for an MGM that has previously registered successfully with the following registration context:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```bash
   export REGISTRATION_CONTEXT='{
     "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
     "corda.ecdh.key.id": "'$ECDH_KEY_ID'",
     "corda.group.protocol.registration": "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
     "corda.group.protocol.synchronisation": "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
     "corda.group.protocol.p2p.mode": "Authenticated_Encryption",
     "corda.group.key.session.policy": "Combined",
     "corda.group.pki.session": "NoPKI",
     "corda.group.pki.tls": "Standard",
     "corda.group.tls.type": "OneWay",
     "corda.group.tls.version": "1.3",
     "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':'$P2P_GATEWAY_PORT'",
     "corda.endpoints.0.protocolVersion": "1",
     "corda.group.trustroot.tls.0" : "'$TLS_CA_CERT'"
   }'
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $REGISTRATION_CONTEXT = @{
     'corda.session.keys.0.id': $SESSION_KEY_ID,
     'corda.ecdh.key.id': $ECDH_KEY_ID,
     'corda.group.protocol.registration': "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
     'corda.group.protocol.synchronisation': "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
     'corda.group.protocol.p2p.mode': "Authenticated_Encryption",
     'corda.group.key.session.policy': "Combined",
     'corda.group.pki.session': "NoPKI",
     'corda.group.pki.tls': "Standard",
     'corda.group.tls.type': "OneWay",
     'corda.group.tls.version': "1.3",
     'corda.endpoints.0.connectionURL': "https://$P2P_GATEWAY_HOST:$P2P_GATEWAY_PORT",
     'corda.endpoints.0.protocolVersion': "1",
     'corda.group.trustroot.tls.0' : $TLS_CA_CERT
   }
   ```
   {{% /tab %}}
   {{< /tabs >}}

   Modify the endpoint, as required. For example, change the port to `8082`:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```bash
   export REGISTRATION_CONTEXT='{
     "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
     "corda.ecdh.key.id": "'$ECDH_KEY_ID'",
     "corda.group.protocol.registration": "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
     "corda.group.protocol.synchronisation": "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
     "corda.group.protocol.p2p.mode": "Authenticated_Encryption",
     "corda.group.key.session.policy": "Combined",
     "corda.group.pki.session": "NoPKI",
     "corda.group.pki.tls": "Standard",
     "corda.group.tls.type": "OneWay",
     "corda.group.tls.version": "1.3",
     "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':8082",
     "corda.endpoints.0.protocolVersion": "1",
     "corda.group.trustroot.tls.0" : "'$TLS_CA_CERT'"
   }'
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $REGISTRATION_CONTEXT = @{
     'corda.session.keys.0.id': $SESSION_KEY_ID,
     'corda.ecdh.key.id': $ECDH_KEY_ID,
     'corda.group.protocol.registration': "net.corda.membership.impl.registration.dynamic.member.DynamicMemberRegistrationService",
     'corda.group.protocol.synchronisation': "net.corda.membership.impl.synchronisation.MemberSynchronisationServiceImpl",
     'corda.group.protocol.p2p.mode': "Authenticated_Encryption",
     'corda.group.key.session.policy': "Combined",
     'corda.group.pki.session': "NoPKI",
     'corda.group.pki.tls': "Standard",
     'corda.group.tls.type': "OneWay",
     'corda.group.tls.version': "1.3",
     'corda.endpoints.0.connectionURL': "https://$P2P_GATEWAY_HOST:8082",
     'corda.endpoints.0.protocolVersion': "1",
     'corda.group.trustroot.tls.0' : $TLS_CA_CERT
   }
   ```
   {{% /tab %}}
   {{< /tabs >}}
   {{< note >}}
   If the MGM is changing to a new hostname and the new hostname is not already included in the TLS certificate’s Subject Alternative Name (SAN), before proceeding with the re-registration you must configure a new certificate, as follows:
   1. [Generate a new key pair and request the issuance of a new certificate that contains the new hostname in it]({{< relref "./key-pairs.md#configure-the-cluster-tls-key-pair" >}}). Ensure that you specify a new alias for the uploaded certificate.
   2. [Configure communication properties using the alias of the new certificate]({{< relref "./config-node.md" >}}).
   To avoid any communication disruption with other members after the new certificate is configured and before the re-registration is complete, the new TLS certificate should contain both the old and the new hostname as SANs.
   {{< /note >}}
4. [Re-register]({{< relref "reregister.md" >}}) with the updated registration context that contains the new endpoint URL. After successful re-registration, you should be able to see the MGM's new endpoint URL in their member-provided context. For example:
   ```shell
   REGISTRATION_CONTEXT='{
   "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
   "corda.session.keys.0.signature.spec": "SHA256withECDSA",
   "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
   "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
   "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':8082",
   "corda.endpoints.0.protocolVersion": "1"
   }'
   ```
5. Remove the old endpoint from the cluster's P2P Gateway configuration to make it unavailable for Corda services. For example:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export NEW_CONFIG='{
   "config": {
     "serversConfiguration":[{"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8082,"urlPath":"/"}]
   },
   "schemaVersion": {
     "major": 1,
     "minor": 0
   },
   "section": "corda.p2p.gateway",
   "version": 1
   }'
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -d "$NEW_CONFIG" -X 'PUT' "$REST_API_URL/config"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f ${REST_API_USER}:${REST_API_PASSWORD})} -Method Put -Uri "$REST_API_URL/config" -Body (ConvertTo-Json -Depth 4 @{
      "config": "{
         "serversConfiguration":[{"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8082,"urlPath":"/"}]
      }",
      "schemaVersion": {
         "major": 1,
         "minor": 0
      },
      "section": "corda.p2p.gateway",
      "version": 1
   })
   ```
   {{% /tab %}}
   {{< /tabs >}}
