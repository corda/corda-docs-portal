---
date: '2022-11-15'
title: "Configuring Optional Session Certificates"
menu:
  corda-5-beta:
    identifier: corda-5-beta-mgm-onboarding-session-certificates
    parent: corda-5-beta-tutorials-deploy-dynamic
    weight: 3000
section_menu: corda-5-beta
---
You can configure a dynamic network to use session certificates when sending messages using the P2P layer. This requires additional steps when onboarding an MGM or member into the dynamic network.

## Set Variables

Set the holding identity short hash of the virtual node of either the MGM or member as a variable for use in later commands:
```shell
export HOLDING_ID=<holding-id>
```

## Build Registration Context for MGM Registration

If using session certificates, make the following changes to the [MGM REGISTRATION_CONTEXT](mgm-onboarding.html#build-registration-context):

1. Add an extra JSON field `corda.group.truststore.session.0` with the truststore of the CA to the registration context (similar to `corda.group.truststore.tls.0`).
2. Set the JSON field `corda.group.pki.session` to `"Standard"` instead of `"NoPKI"`.

## Generate a Certificate Signing Request (CSR)

After creating the MGM or member session key pair, but before building the registration context, generate a CSR for the session certificate by running the following command, replacing `X500_NAME` with the X500Name of the MGM or member:
```shell
curl --fail-with-body -s -S -k -u admin:admin  -X POST -H "Content-Type: application/json" -d '{"x500Name": "'$X500_NAME'"}' $API_URL"/certificates/"$HOLDING_ID/$SESSION_KEY_ID > $WORK_DIR/request.csr
```
Similarly to the TLS certificate, the CSR can be processed to issue a certificate using a CA chosen by the MGM operator. The CA trustroot for session certificates should be configured during the MGM onboarding.

Once you have a certificate based on the CSR exported from Corda issued by the CA, you must upload the certificate chain to the Corda cluster. To upload the certificate chain, run:
```shell
curl -k -u admin:admin -X PUT  -F certificate=@/tmp/ca/request/certificate.pem -F alias=session-certificate $API_URL/certificates/vnode/$HOLDING_ID/p2p-session
```
You can optionally omit the root certificate.

{{< note >}}
If you upload a certificate chain consisting of more than one certificates, ensure that `-----END CERTIFICATE-----` and `-----BEGIN CERTIFICATE-----` from the next certificate are separated by a new line with no empty spaces in between.
{{< /note >}}

### Revocation Checks

If session certificates are used, revocation checks are performed by the P2P Gateway. As a result, the P2P Gateway's firewall zone must be configured to allow access to the certificate's online certificate status protocol (OSCP) and/or Certificate Revocation List (CRL) endpoint.

If the CA has not been configured with revocation, you can disable revocation checks. By default, revocation checks are enabled.
To disable revocation checks, do the following:
1. Retrieve the current link manager configuration version:
   ```shell
   curl --insecure -u admin:admin -X GET $API_URL/config/corda.p2p.linkManager
   ```
2. Save the displayed version number from the response as a variable:
   ```shell
   export CONFIG_VERSION=<configuration-version>
   ```
3. Send the following request to disable revocation checks for the specified gateway worker:
   ```
   curl -k -u admin:admin -X PUT -d '{"section":"corda.p2p.linkManager", "version":"'$CONFIG_VERSION'", "config": { "revocationCheck": { "mode": "OFF" } }, "schemaVersion": {"major": 1, "minor": 0}}' $API_URL"/config"
   ```
## Configure Virtual Node as Network Participant

If using session certificates, you must also add the `sessionCertificateChainAlias` and `useClusterLevelSessionCertificateAndKey` JSON fields to the network setup RPC request. For example:
```shell
curl -k -u admin:admin -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeyId": "'$SESSION_KEY_ID'", "sessionCertificateChainAlias": "session-certificate", "useClusterLevelSessionCertificateAndKey": false}' $API_URL/network/setup/$HOLDING_ID
```
