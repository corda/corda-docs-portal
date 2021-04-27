---
date: '2020-12-16T01:00:00Z'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-operations-guide-deployment-hsm-integration
    parent: corda-enterprise-4-8-operations-guide-deployment-hsm
    name: "Integrating an HSM"
tags:
- operations
- deployment
- hsm
- integration
title: Integrating an HSM
weight: 60
---

# Integrating an HSM

While Corda Enterprise supports a variety of HSMs for storing legal identity and confidential identity keys, you can also integrate other HSMs with Corda Enterprise using Corda Enterprise APIs. Once HSM integration has been written, HSMs can be tested against Corda Enterprise using the HSM Technical Compatibility Kit (TCK), a test suite [available here](hsm-integration-tck.md/).

To help write integration for your HSM, there is an example HSM implementation available as part of the `com.r3.corda:corda-enterprise-utils:4.8` resources. We'll go over this example HSM here to explain what the components are, and how they work.

In the example HSM there are five key files:

  - A configuration file, called `AWSCloudConfiguration.java`.
  - A configuration parser, called `AWSCloudConfigurationParser.java`.
  - A factory class called `AWSCloudCryptoServiceProvider.java`.
  - A file specifying the java class that implements the `CryptoServiceProvider` interface, called `resources/META-INF/services/com.r3.corda.utils.CryptoServiceProvider`.
  - The HSM integration, called `AWSCloudCryptoService.java`.


We'll go through each of these files and use them as a basis for explaining how to integrate an HSM with Corda Enterprise.

## The HSM configuration file

In the example HSM implementation the HSM configuration file `AWSCloudConfiguration.java` contains the following code:

{{< codesample file="/content/en/docs/corda-enterprise/codesamples/AWSCloudConfiguration.java" >}}

The HSM configuration contains the basic configuration information required by the HSM, and implements `CryptoServiceCredentials`. When implementing `CryptoServiceCredentials` the only argument should be the configuration class itself.

Ensure that the configuration options required by the HSM correspond to the configuration options in this file.

The `samePartition` section is required by Corda Enterprise tools to manage multiple public keys being used to access shared HSMs.

## The configuration parser

The configuration parser file `AWSCloudConfigurationParser.java` implements the `ConfigParser` interface, and contains the following code:

{{< codesample file="/content/en/docs/corda-enterprise/codesamples/AWSCloudConfigurationParser.java" >}}

The configuration parser will be unique to the HSM implementation, and is used to deserialise HSM configuration to a Java class.

## The factory class

The factory class `AWSCloudCryptoServiceProvider` implements the `CryptoServiceProvider` interface, and contains the following code:

{{< codesample file="/content/en/docs/corda-enterprise/codesamples/AWSCloudCryptoServiceProvider.java" >}}

Corda Enterprise uses a service loader class to discover implementations of `CryptoServiceProvider`.

The class takes the configuration information and creates an instance of the `CryptoService` - in this case `AWSCloudCryptoService` - including an X500 identifier and the configuration information defined in `AWSCloudConfiguration.java`.

## Java class specification file

This file is required when integrating an HSM. It must have the following filepath: `src/main/resources/META-INF/services/com.r3.corda.utils.cryptoservice.CryptoServiceProvider`.

The file must contain the fully qualified name of the Java class that implements the `CryptoServiceProvider` interface. In this example implementation, the content of the file is:

{{< codesample file="/content/en/docs/corda-enterprise/codesamples/com.r3.corda.utils.CryptoServiceProvider" >}}

## The HSM integration

The HSM integration will differ depending on the mechanics of any given HSM, but in this example we've used a Java helper class `JCACryptoService` to reduce the complexity. This class was created to facilitate the integration of further HSM vendors that provide a JCA provider.

When writing HSM integration, there are two groups of keys to consider: "alias" keys used for Artemis, node legal identity, and TLS, and "non-alias" keys, used for confidential identities.

Alias keys are stored in the HSM, and are never removed. Each HSM implementation should only have a very small number of alias keys.

Non-alias keys are generated using the HSM and extracted from HSMs in a wrapped format. Depending on the implementation there may be many confidential identity keys. Confidential identity keys are not stored in the HSM. The key used to wrap confidential identity keys is stored in the HSM and is not extracted.

All asymmetric keypairs (TLS, Artemis, and node legal identity) should use elliptic-curve keys, and all wrapping keys should use at least AES 256-bit keys.

```java
public class AWSCloudCryptoService extends JCACryptoService implements CryptoServiceAdmin {
    public static String NAME = "AWS_CLOUD_SAMPLE";
    private static Logger logger = LoggerFactory.getLogger(AWSCloudCryptoService.class);
    private LoginManager loginManager = LoginManager.getInstance();
    private AWSCloudConfiguration config;

    AWSCloudCryptoService(KeyStore keyStore, Provider provider, X500Principal x500Principal, AWSCloudConfiguration config) {
        super(keyStore, provider, x500Principal);
        this.config = config;
    }
```

The above code block also includes the HSM configuration, and defines the HSM class, including `keyStore`, `Provider`, `X500Principal`, and `config` arguments. For full details, see the [JCACryptoService definition](../../../codesamples/JCACryptoService.kt).

The HSM integration must include code for authenticating with the HSM, creating keypairs, retrieving public keys, signing, creating wrapping keys, wrapping private keys, and error handling.

The full HSM integration example is as follows:

{{< codesample file="/content/en/docs/corda-enterprise/codesamples/AWSCloudCryptoService.java" >}}
