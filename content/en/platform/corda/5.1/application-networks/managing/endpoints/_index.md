---
date: '2023-09-21'
title: "Member Endpoints"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-networks-member-endpoints
    parent: corda51-networks-manage
    weight: 3000
section_menu: corda51
---
# Member Endpoints

If a member needs to make changes to their endpoint information (for example, changing the URL of the endpoint or adding a new endpoint), the member must re-register with the updated endpoint information. To minimize communication disruption, the member should also configure the P2P Gateway with both the old and new information, before re-registering, and then remove the old information, as follows:

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
3. Re-register with the updated registration context that contains the new endpoint URL. After successful re-registration, you should be able to see the member's new endpoint URL in their member-provided context. For example:
   ```shell
   REGISTRATION_CONTEXT='{
   "corda.session.keys.0.id": "'$SESSION_KEY_ID'",
   "corda.session.keys.0.signature.spec": "SHA256withECDSA",
   "corda.ledger.keys.0.id": "'$LEDGER_KEY_ID'",
   "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
   "corda.endpoints.0.connectionURL": "https://'$P2P_GATEWAY_HOST':8081",
   "corda.endpoints.0.protocolVersion": "1"
   }'
   ``` 
4. Remove the old endpoint from the cluster's P2P Gateway configuration to make it unavailable for Corda services. For example:
   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   export NEW_CONFIG='{
   "config": {
     "serversConfiguration":[{"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8081,"urlPath":"/"}]
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
         "serversConfiguration":[{"hostAddress":"'$P2P_GATEWAY_HOST'","hostPort":8081,"urlPath":"/"}]
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