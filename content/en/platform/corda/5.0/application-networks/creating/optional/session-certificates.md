---
date: '2022-11-15'
version: 'Corda 5.0'
title: "Session Certificates"
menu:
  corda5:
    identifier: corda5-network-session-certificates
    parent: corda5-networks-optional
    weight: 2000
section_menu: corda5
---

# Session Certificates

You can configure a dynamic network to use session certificates when sending messages. This requires additional steps when onboarding an MGM or member into the dynamic network.

## Generate a Certificate Signing Request (CSR)

After creating the MGM or member session key pair, but before building the registration context, generate a CSR for the session certificate by running the following command, replacing `X500_NAME` with the X.500 name of the MGM or member:
```shell
curl --fail-with-body -s -S -k -u $REST_API_USER:$REST_API_PASSWORD  -X POST -H "Content-Type: application/json" -d '{"x500Name": "'$X500_NAME'"}' $REST_API_URL"/certificates/"$HOLDING_ID/$SESSION_KEY_ID > $WORK_DIR/request.csr
```
Similarly to the TLS certificate, the CSR can be processed to issue a certificate using a CA chosen by the MGM operator. The CA trustroot for session certificates should be configured during the MGM onboarding.

Once you have a certificate based on the CSR exported from Corda issued by the CA, you must upload the certificate chain to the Corda cluster. To upload the certificate chain, run:
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT  -F certificate=@/tmp/ca/request/certificate.pem -F alias=session-certificate $REST_API_URL/certificates/vnode/$HOLDING_ID/p2p-session
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
   curl --insecure -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/config/corda.p2p.linkManager
   ```
2. Save the displayed version number from the response as a variable:
   ```shell
   export CONFIG_VERSION=<configuration-version>
   ```
3. Send the following request to disable revocation checks for the specified gateway worker:
   ```
   curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"section":"corda.p2p.linkManager", "version":"'$CONFIG_VERSION'", "config": { "revocationCheck": { "mode": "OFF" } }, "schemaVersion": {"major": 1, "minor": 0}}' $REST_API_URL"/config"
   ```

## Build Registration Context for MGM Registration

If using session certificates, make the following changes to the [MGM registration context]({{< relref "../mgm/register.md#build-registration-context" >}}):

1. Add an extra JSON field `corda.group.truststore.session.0` with the truststore of the CA to the registration context (similar to `corda.group.truststore.tls.0`).
2. Set the JSON field `corda.group.pki.session` to `"Standard"` instead of `"NoPKI"`.

## Configure Virtual Node as Network Participant

If using session certificates, you must also add the `sessionCertificateChainAlias` and `useClusterLevelSessionCertificateAndKey` JSON fields to the network setup REST request. For example:
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeyId": "'$SESSION_KEY_ID'", "sessionCertificateChainAlias": "session-certificate", "useClusterLevelSessionCertificateAndKey": false}' $REST_API_URL/network/setup/$HOLDING_ID
```
