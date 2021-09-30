---
aliases:
- /ejbca-plugin.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-ejbca-plugin
    parent: cenm-1-3-signing-plugin-samples
    weight: 340
tags:
- ejbca
- plugin
title: EJBCA Sample Plugin
---


# EJBCA Sample Plugin



## Overview

Signable Material Retriever servce (SMR) ships with default CA and Non CA plugin for the CENM provided Signing Service.
These plugins demonstrate the connectivity to the CENM Signing Service which doesn’t persist the signable materials
requests, and the data needs to be stored on the plugin’s side (SMR Service). To illustrate the reverse setup, where a
signing infrastructure (the replacement of CENM Signing Service) stores internally signable material requests, we
provide instruction how to setup EJBCA - the Open Source Certificate Authority, and sample plugin implementation.

{{< note >}}
The implementation shown below is meant for guiding the plugins development for own signing infrastructure.
The implementation should not be used in production deployment.

{{< /note >}}

## EJBCA Web Service Setup

Web service setup follows the same steps as [the official documentation](https://doc.primekey.com/ejbca6152/tutorials-and-guides/quick-start-guide).
We will setup a local environment as specified in Quick Start Guide. After this step you will be able to access EJBCA
Administration UI on specified address.

Next step is to import Corda’s CA. This is done by accessing *Certification Authorities* tab and using
*Import CA keystore…* option. The keystore you will need to import for successful CA material signing is
`corda-identity-manager-keys.jks` which is contained in Signing Service’s `certificates` directory. Keystore’s
password is `password` and *Alias of signature key* is `cordaidentitymanagerca`. Leave  *Alias of encryption key*
field empty.

{{< note >}}
Provided keystore must be in PKCS12 format.

{{< /note >}}
Corda’s certificates contain a custom extension named Certificate Role. We must enable its override during certificate
generation. This is done by accessing *System Configuration* tab followed by *Custom Certificate Extensions* tab. Here
we add new custom extension with following properties:

>
>
> * **OID** -> *1.3.6.1.4.1.50530.1.1*
> * **Label** -> *X509_EXTENSION_CORDA_ROLE*
> * **Critical** -> *No*
> * **Required** -> *Yes*
> * **Encoding** -> *DERINTEGER*
> * **Dynamic** -> *True*
> * **Value** -> *4*


Now we must set up new certificate profile in order to support Corda compatible certificate issuance. This is done by
accessing *Certificate Profiles* tab and adding new profile. After that edit profile to have following properties set up:

>
>
> * **Type** -> *Sub CA*
> * **Allow Extension Override** -> *True*
> * **Allow certificate serial number override** -> *True*
> * **Allow Key Usage Override** -> *True*
> * **Key Usage** -> *Use..*, *Critical*, *Digital Signature*, *Non-repudiation*, *Key encipherement*, *Key certificate sign*, *CRL sign*
> * **CRL Distribution Points** -> *Use..*
> * **Use CA defined CRL Distribution Point** -> *Use..*
> * **Used Custom Certificate Extensions** -> certificate role you’ve specified before
> * **Available CAs** -> Corda’s CA


At the end we must set up new end entity profile. This is done by accessing *End Entity Profiles* and adding new profile.
After that edit profile to have following properties set up:

>
>
> * **Subject DN Attributes** -> Add *OU*, *O*, *L*, *C*, *ST*, *DC*
> * **Default Certificate Profile** -> The one you’ve set up
> * **Available Certificate Profiles** -> The one you’ve set up
> * **Default CA** -> The one you’ve set up
> * **Available CAs** -> The one you’ve set up
> * **Custom certificate serial number** -> *Use*
> * **Custom certificate extension data** -> *Use*



## Implementation

EJBCA is oriented on CA related type of signable material. This is why the sample plugin implements `CASigningPlugin`
interface. It also implements `ENMLoggable` interface which is our internal logging interface. However this is optional
and it’s added for convenience.

The sample implementation follows the same steps as [the official documentation](https://doc.primekey.com/ejbca6152/ejbca-operations/ejbca-concept-guide/protocols/web-service-interface).
The suggested approach would be to follow the given link and this document at the same time to fill in the gaps.

`start()` method initialises communication with EJBCA Web Service set up prior and `EjbcaWS` typed member
`ejbcaraws` is used for client methods invocation. Keep in mind you have to export keystore for the user which has
permissions to invoke Web Service API methods. Creation of that user and the keystore export is done via EJBCA
administration UI.

`submitCSR()` method takes `CertificateSigningRequest` typed argument `csr` and based on its contents creates user
for which certificate will be created. Certificate request is done and after that we collect generated certifciate’s
chain since node will only accept chains which root certificate matches the one provided in network root truststore.

`submitCRL()` method takes current CRL in form of `crl` argument and a Certificate Revocation List to be updated. First of all, revocation of all new revocation requests is performed. After that CRL is updated and
fetched. At the end we form response as specified in interface.

```java
package com.r3.enm.smrplugins.ejbcaplugin;

import com.r3.enm.logging.ENMLoggable;
import com.r3.enm.logging.ILoggingContextWrapper;
import com.r3.enm.logging.LoggingContext;
import com.r3.enm.logging.LoggingContextWrapperFactory;
import com.r3.enm.model.CertificateRevocationRequest;
import com.r3.enm.model.CertificateSigningRequest;
import com.r3.enm.smrpluginapi.ca.CASigningPlugin;
import com.r3.enm.smrpluginapi.ca.CRLResponse;
import com.r3.enm.smrpluginapi.ca.CRLSigningData;
import com.r3.enm.smrpluginapi.ca.CSRResponse;
import com.r3.enm.smrpluginapi.ca.CSRSigningData;
import com.r3.enm.smrpluginapi.common.SMRPluginTerminalException;
import com.r3.enm.smrpluginapi.common.SigningStatus;
import org.cesecore.util.Base64;
import org.cesecore.util.CryptoProviderTools;
import org.ejbca.core.protocol.ws.client.gen.Certificate;
import org.ejbca.core.protocol.ws.client.gen.EjbcaWS;
import org.ejbca.core.protocol.ws.client.gen.EjbcaWSService;
import org.ejbca.core.protocol.ws.client.gen.UserDataVOWS;
import org.ejbca.core.protocol.ws.common.CertificateHelper;
import org.jetbrains.annotations.NotNull;
import net.corda.core.crypto.CryptoUtils;

import javax.annotation.Nullable;
import javax.xml.namespace.QName;
import java.io.ByteArrayInputStream;
import java.math.BigInteger;
import java.net.MalformedURLException;
import java.net.URL;
import java.security.cert.CRLException;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;
import java.security.cert.X509CRL;
import java.time.Instant;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class EJBCASigningPlugin implements CASigningPlugin, ENMLoggable {

    private static final String EJBCA_URL = "https://localhost:8443/ejbca/ejbcaws/ejbcaws?wsdl";

    // keystore from EJBCA user under role which has permissions to communicate with CA related web service APIs
    private static final String KEYSTORE_PATH = "p12/keystore.jks";
    private static final String KEYSTORE_PASSWORD = "password";

    private static final String CA_NAME = "CordaCA";
    private static final String END_ENTITY_PROFILE_NAME = "CENM";
    private static final String CERTIFICATE_PROFILE_NAME = "CENM";
    private static final String SIGNER_NAMES = "EJBCA";

    private static CertificateFactory certificateFactory;

    private EjbcaWS ejbcaraws;

    static {
        try {
            certificateFactory = CertificateFactory.getInstance("X509");
        } catch (CertificateException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void start() {
        CryptoProviderTools.installBCProvider();

        System.setProperty("javax.net.ssl.trustStore", KEYSTORE_PATH);
        System.setProperty("javax.net.ssl.trustStorePassword", KEYSTORE_PASSWORD);

        System.setProperty("javax.net.ssl.keyStore", KEYSTORE_PATH);
        System.setProperty("javax.net.ssl.keyStorePassword", KEYSTORE_PASSWORD);

        QName qname = new QName("http://ws.protocol.core.ejbca.org/", "EjbcaWSService");
        try {
            EjbcaWSService service = new EjbcaWSService(new URL(EJBCA_URL), qname);
            ejbcaraws = service.getEjbcaWSPort();
        } catch (MalformedURLException e) {
            getOpsLogger().error(() -> "Malformed URL provided, shutting down SMR");
            throw new SMRPluginTerminalException(e);
        } catch (Exception e) {
            throw new SMRPluginTerminalException(e);
        }

        getCtx().withLoggers(getConsoleLogger(), getOpsLogger()).forEach(logger -> logger.info(() -> "EJBCA plugin started"));
    }

    @Override
    public CSRResponse submitCSR(CertificateSigningRequest csr) {
        // fill user data
        final UserDataVOWS user = new UserDataVOWS();
        user.setUsername(csr.getLegalName().toString());
        user.setSubjectDN(csr.getLegalName().toString());
        user.setCaName(CA_NAME);
        user.setEndEntityProfileName(END_ENTITY_PROFILE_NAME);
        user.setCertificateProfileName(CERTIFICATE_PROFILE_NAME);
        user.setCertificateSerialNumber(BigInteger.valueOf(CryptoUtils.random63BitValue()));

        // submit certificate signing request
        try {
            ejbcaraws.certificateRequest(
                    user,
                    new String(Base64.encode(csr.getPkcS10CertificationRequest().getEncoded())),
                    CertificateHelper.CERT_REQ_TYPE_PKCS10,
                    null,
                    CertificateHelper.RESPONSETYPE_CERTIFICATE
            );
        } catch (Exception e) {
            getOpsLogger().error(() -> "Failed to create certificate for " + csr.getLegalName().toString());
            throw new RuntimeException(e);
        }
        getConsoleLogger().debug(() -> "Received certificate for " + csr.getLegalName().toString());
        getOpsLogger().info(() -> "Received certificate for " + csr.getLegalName().toString());

        // retrieve certificate chain for generated certificate
        List<Certificate> certChain;
        try {
            certChain = ejbcaraws.getLastCertChain(user.getUsername());
        } catch (Exception e) {
            getOpsLogger().error(() -> "Failed to retrieve certificate chain for certificate under name " +
                    csr.getLegalName().toString());
            throw new RuntimeException(e);
        }
        getConsoleLogger().debug(() -> "Received certificate chain for certificate under name " + csr.getLegalName().toString());
        getOpsLogger().info(() -> "Received certificate chain for certificate under name " + csr.getLegalName().toString());

        // form proper response to be passed to SMR
        try {
            return new CSRResponse(SigningStatus.COMPLETED, new CSRSigningData(
                    certificateFactory.generateCertPath(certChain.stream().map(cert -> {
                                try {
                                    return certificateFactory.generateCertificate(new ByteArrayInputStream(cert.getRawCertificateData()));
                                } catch (CertificateException e) {
                                    getOpsLogger().error(() -> "Failed to generate certificate from raw data");
                                    throw new RuntimeException(e);
                                }
                            }
                    ).collect(Collectors.toList())),
                    SIGNER_NAMES
            ));
        } catch (CertificateException e) {
            getOpsLogger().error(() -> "Failed to generate certificate path from raw data");
            throw new RuntimeException(e);
        }
    }

    @Override
    public CRLResponse submitCRL(@Nullable X509CRL crl, Set<CertificateRevocationRequest> newCRRs) {
        // revoke certificates
        Set<CertificateRevocationRequest> revokedRequests = new HashSet<>();
        newCRRs.forEach(crr -> {
            try {
                ejbcaraws.revokeCert(
                        crr.getCertificate().getIssuerDN().getName(),
                        crr.getCertificate().getSubjectDN().getName(),
                        crr.getReason().ordinal()
                );
                revokedRequests.add(crr);

                getOpsLogger().info(() -> "Revoked certificate under name " + crr.getCertificate().getSubjectDN().getName() +
                        " issued by " + crr.getCertificate().getIssuerDN().getName());
            } catch (Exception e) {
                getOpsLogger().info(() -> "Failed to revoke certificate under name " + crr.getCertificate().getSubjectDN().getName() +
                        " issued by " + crr.getCertificate().getIssuerDN().getName() + " due to " + e.getMessage());
            }
        });

        // create new certificate revocation list
        try {
            ejbcaraws.createCRL(CA_NAME);
        } catch (Exception e) {
            getOpsLogger().error(() -> "Failed to generate new CRL");
            throw new RuntimeException(e);
        }
        getConsoleLogger().debug(() -> "CRL generated");
        getOpsLogger().info(() -> "CRL generated");

        // retrieve created certificate revocation list
        byte[] newCrl;
        try {
            newCrl = ejbcaraws.getLatestCRL(CA_NAME, false);
        } catch (Exception e) {
            getOpsLogger().error(() -> "Failed to fetch CRL");
            throw new RuntimeException(e);
        }
        getConsoleLogger().debug(() -> "CRL fetched");
        getOpsLogger().info(() -> "CRL fetched");

        // form proper response to be passed to SMR
        try {
            return new CRLResponse(SigningStatus.COMPLETED, new CRLSigningData(
                    (X509CRL) certificateFactory.generateCRL(new ByteArrayInputStream(newCrl)),
                    SIGNER_NAMES,
                    Instant.now(),
                    revokedRequests
            ));
        } catch (CRLException e) {
            getOpsLogger().error(() -> "Failed to generate CRL from raw data");
            throw new RuntimeException(e);
        }
    }

    @NotNull
    @Override
    public LoggingContext getCtx() {
        return new LoggingContext("EJBCAPlugin", "", null, new LoggingContextWrapperFactory());
    }

    @NotNull
    @Override
    public ILoggingContextWrapper getOpsLogger() {
        return getCtx().getOps();
    }

    @NotNull
    @Override
    public ILoggingContextWrapper getAuditLogger() {
        return getCtx().getAudit();
    }

    @NotNull
    @Override
    public ILoggingContextWrapper getDevLogger() {
        return getCtx().getDev();
    }

    @NotNull
    @Override
    public ILoggingContextWrapper getConsoleLogger() {
        return getCtx().getConsole();
    }
}

```

## Running EJBCA plugin

To run the plugin you simply need to specify its `.jar` path for CSR and CRL material management tasks in SMR’s
configuration. The class name to configure is `com.r3.enm.smrplugins.ejbcaplugin.EJBCASigningPlugin`.

You run SMR as per usual with following command:

```bash
java -jar smr-<VERSION>.jar --config-file <CONFIG_FILE>
```

On success you should see a message similar to:

```kotlin
EJBCA plugin started
SMR Service started
```
