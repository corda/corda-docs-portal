---
aliases:
- /ejbca-plugin.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-ejbca-plugin
    parent: cenm-1-4-signing-plugin-samples
    weight: 340
tags:
- ejbca
- plugin
title: EJBCA Sample Plugin
---


# EJBCA Sample Plugin



## Overview

In CENM 1.4, the Signing Service ships with default CA and non-CA plug-ins.
These plug-ins demonstrate the connectivity to the CENM Signing Service which doesn’t persist the signable materials
requests, and the data needs to be stored on the plug-in’s side. To illustrate the reverse setup, where a
signing infrastructure (the replacement of the CENM Signing Service) stores internally signable material requests, we
provide instruction how to setup EJBCA - the Open Source Certificate Authority, and sample plugin implementation.

{{< note >}}
The implementation shown below is meant for guiding the plugins development for own signing infrastructure.
The implementation should not be used in production deployment.

{{< /note >}}

## EJBCA Web Service Setup

1. Follow [the official documentation](https://doc.primekey.com/ejbca6152/tutorials-and-guides/quick-start-guide) for the initial web service setup.
This section shows a setup of a local environment as specified in the Quick Start Guide. After this step you will be able to access EJBCA
Administration UI on the specified address.

2. Import Corda’s CA. To do so, access the *Certification Authorities* tab and use the
*Import CA keystore…* option. The keystore you will need to import for successful CA material signing is
`corda-identity-manager-keys.jks`, which is contained in the Signing Service’s `certificates` directory. The keystore’s
password is `password`, and the *Alias of signature key* is `cordaidentitymanagerca`. Leave the  *Alias of encryption key*
field empty.

{{< note >}}
Provided keystore must be in PKCS12 format.
{{< /note >}}

3. Corda’s certificates contain a custom extension named Certificate Role. You must enable override during certificate generation. This is done by accessing the *System Configuration* tab followed by *Custom Certificate Extensions* tab. Here
we add a new custom extension with following properties:

    >
    >
    > * **OID** -> *1.3.6.1.4.1.50530.1.1*
    > * **Label** -> *X509_EXTENSION_CORDA_ROLE*
    > * **Critical** -> *No*
    > * **Required** -> *Yes*
    > * **Encoding** -> *DERINTEGER*
    > * **Dynamic** -> *True*
    > * **Value** -> *4*

4. The EJBCA plugin contains certain hardcoded values. The configuration set up in the EJBCA web service should match those values, as listed below:

    >
    >
    > * `CA_NAME = "CordaCA";`
    > * `END_ENTITY_PROFILE_NAME = "CENM";`
    > * `CERTIFICATE_PROFILE_NAME = "CENM";`



5. Set up a new certificate profile in order to support a Corda-compatible certificate issuance. Access the *Certificate Profiles* tab and add a new profile.

6. Edit the profile to have the following properties set up:

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


7. Set up a new end entity profile. Access *End Entity Profiles* and add a new profile.

8. Edit the profile to have the following properties set up:

    >
    >
    > * **Subject DN Attributes** -> Add *OU*, *O*, *L*, *C*, *ST*, *DC*
    > * **Default Certificate Profile** -> The one you’ve set up
    > * **Available Certificate Profiles** -> The one you’ve set up
    > * **Default CA** -> The one you’ve set up
    > * **Available CAs** -> The one you’ve set up
    > * **Custom certificate serial number** -> *Use*
    > * **Custom certificate extension data** -> *Use*

9. You can also assign Administrator role permissions for the end entity created above. Access *Administrator Roles* -> *Super Administrator Role* -> *Members* and edit the following fields:

    >
    >
    > * **Match with** -> X509: CN, Common Name
    > * **CA** -> ManagementCA
    > * **Match Value** ->...

## EJBCA Client Setup

You will also need to generate certificates used for establishing a secure connection between the plug-in and the web service.

1. Access *Add End Identity* and edit the profile as shown below:

    >
    >
    > * **User** -> ...
    > * **Password** -> *password*
    > * **Common Name** ->...
    > * **End Entity Profile** -> *EMPTY*
    > * **Certificate Profile** -> *ENDUSER*
    > * **CA** -> *ManagementCA*
    > * **Token** -> *JKS file*

2. Validate the existence of the new identity by accessing *Search End Entities* and searching for entities with the status *ALL*.

3. Once confirmed, follow the same steps described above to assign Administrator role permissions to the new end entity.

4. Generate and download a JKS keystore for the end entity.

5. Access *Public Web* then *Create Keystore*. Enter the following information:

    >
    >
    > * **User** -> ...
    > * **Password** -> *password*
    > * **Common Name** ->...
    > * **Key specification** -> *RSA 2048 bits*
    > * **Certificate Profile** -> *ENDUSER*

6. Create a directory with the name *`p12`* in the Signing Service folder and add the downloaded keystore.

7. Rename the keystore to *`keystore.jks`*. The keystore's password is `password`.

{{< note >}}

The keystore path must be `p12/keystore.jks` to match the hardcoded file name and location.

{{< /note >}}


## Implementation

EJBCA is oriented on CA-related type of signable material. This is why the sample plug-in implements the `CASigningPlugin`
interface. It also implements the `ENMLoggable` interface, which is the CENM internal logging interface. However this is optional
and it is added for convenience only.

The sample implementation follows the same steps as [the official documentation](https://doc.primekey.com/ejbca6152/ejbca-operations/ejbca-concept-guide/protocols/web-service-interface).
The suggested approach would be to follow the given link and this document at the same time in order to fill in the gaps.

The `start()` method initialises the communication with the previously set up EJBCA Web Service, and the `EjbcaWS` typed member
`ejbcaraws` is used for client methods invocation. Please note that you have to export the keystore for the user that has
permissions to invoke Web Service API methods. Use the EJBCA administration UI to create that user and to export the keystore.

The `submitCSR()` method takes the `CertificateSigningRequest` typed argument `csr`, and based on its contents it creates a user
for which a certificate will be created. The certificate request is done and after that the generated certificate’s
chain is collected since the node will only accept chains whose root certificate matches the one provided in network root truststore.

The `submitCRL()` method takes the current CRL in the form of a `crl` argument, and a Certificate Revocation List to be updated. First of all, a revocation of all new revocation requests is performed. After that the CRL is updated and fetched. The last step is to form a response as specified in the interface.

```java
package com.r3.enm.smrplugins.ejbcaplugin;

import com.r3.enm.logging.ENMLoggable;
import com.r3.enm.logging.ILoggingContextWrapper;
import com.r3.enm.logging.LoggingContext;
import com.r3.enm.logging.LoggingContextWrapperFactory;
import com.r3.enm.model.CertificateRevocationRequest;
import com.r3.enm.model.CertificateSigningRequest;
import com.r3.enm.signingpluginapi.ca.CASigningPlugin;
import com.r3.enm.signingpluginapi.ca.CRLResponse;
import com.r3.enm.signingpluginapi.ca.CRLSigningData;
import com.r3.enm.signingpluginapi.ca.CSRResponse;
import com.r3.enm.signingpluginapi.ca.CSRSigningData;
import com.r3.enm.signingpluginapi.common.SigningServicePluginTerminalException;
import com.r3.enm.signingpluginapi.common.SigningStatus;
import org.cesecore.util.Base64;
import org.cesecore.util.CryptoProviderTools;
import org.ejbca.core.protocol.ws.client.gen.Certificate;
import org.ejbca.core.protocol.ws.client.gen.EjbcaWS;
import org.ejbca.core.protocol.ws.client.gen.EjbcaWSService;
import org.ejbca.core.protocol.ws.client.gen.UserDataVOWS;
import org.ejbca.core.protocol.ws.common.CertificateHelper;
import org.jetbrains.annotations.NotNull;
import net.corda.core.crypto.CryptoUtils;

import javax.annotation.Nonnull;
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
            getOpsLogger().error(() -> "Malformed URL provided, shutting down Signing Service");
            throw new SigningServicePluginTerminalException(e);
        } catch (Exception e) {
            throw new SigningServicePluginTerminalException(e);
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
            return new CSRResponse(SigningStatus.FAILED, null, null);
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
            return new CSRResponse(SigningStatus.FAILED, null, null);
        }
        getConsoleLogger().debug(() -> "Received certificate chain for certificate under name " + csr.getLegalName().toString());
        getOpsLogger().info(() -> "Received certificate chain for certificate under name " + csr.getLegalName().toString());

        // form a proper response to be passed to the Signing Service
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
        } catch (Exception e) {
            getOpsLogger().error(() -> "Failed to generate certificate path from raw data");
            return new CSRResponse(SigningStatus.FAILED, null, null);
        }
    }

    @Override
    public CRLResponse submitCRL(@Nullable X509CRL crl, @Nonnull Set<CertificateRevocationRequest> newCRRs) {
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
            return new CRLResponse(SigningStatus.FAILED, null, null);
        }
        getConsoleLogger().debug(() -> "CRL generated");
        getOpsLogger().info(() -> "CRL generated");

        // retrieve created certificate revocation list
        byte[] newCrl;
        try {
            newCrl = ejbcaraws.getLatestCRL(CA_NAME, false);
        } catch (Exception e) {
            getOpsLogger().error(() -> "Failed to fetch CRL");
            return new CRLResponse(SigningStatus.FAILED, null, null);
        }
        getConsoleLogger().debug(() -> "CRL fetched");
        getOpsLogger().info(() -> "CRL fetched");

        // form a proper response to be passed to the Signing Service
        try {
            return new CRLResponse(SigningStatus.COMPLETED, new CRLSigningData(
                    (X509CRL) certificateFactory.generateCRL(new ByteArrayInputStream(newCrl)),
                    SIGNER_NAMES,
                    Instant.now(),
                    revokedRequests
            ));
        } catch (CRLException e) {
            getOpsLogger().error(() -> "Failed to generate CRL from raw data");
            return new CRLResponse(SigningStatus.FAILED, null, null);
        }
    }

    @Override
    public CSRResponse checkCSRSubmissionStatus(@Nonnull String requestId) {
        return null;
    }

    @Override
    public CRLResponse checkCRLSubmissionStatus(@Nonnull String requestId) {
        return null;
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


## Running the EJBCA plug-in

From CENM 1.4, each signing task has a new property called `plugin`, which consists of `pluginJar` and `pluginClass`. If the `plugin` property is defined, it means that the plug-in will be used to sign data instead of the default signing mechanism used by the Signing Service.

To run the EJBCA plug-in, you need to:

1. Specify its `.jar` path for CSR and CRL signing tasks in the Signing Service configuration (see [Signing Service](signing-service.md) for details).
2. Run the Signing Service in the standard way:

```bash
java -jar signer-<VERSION>.jar --config-file <CONFIG_FILE>
```

On success you should see a message similar to:

```kotlin
EJBCA plugin started
Signing Service started
```
