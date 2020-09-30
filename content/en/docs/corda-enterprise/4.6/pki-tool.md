---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-networks
tags:
- pki
- tool
title: Public Key Infrastructure (PKI) Tool
weight: 10
---


# Public Key Infrastructure (PKI) Tool



## Overview

A certificate hierarchy with certain properties is required to run a Corda
network. Specifically, the certificate hierarchy should include the two main CENM entities - the Identity Manager and
the Network Map - and ensure that all entities map back to one common root of trust. The key pairs and certificates for
these entities are used within the Signing Service to sign related network data such as approved CSRs, CRRs, Network Map
and Network Parameter changes.

This certificate hierarchy should be generated prior to setting up the network as it must be provided to the Signing
Service during setup of the CENM services. Generation of all key pairs and certificates in the hierarchy is left up to
the discretion of the network operator. That is, provided the resulting keys and certificates adhere to the requirements
set out in the linked guide above, an operator is free to use any generation process/method they wish.

The security requirements of the PKI will depend on the requirements of the underlying Corda network and the levels of
assumed trust throughout the system. The security around the PKI is ultimately up to the operator, however some general
recommendations are:


* Using locally generated Java key stores for anything other than a toy/test network is **strongly** discouraged.
* All keys should be generated and stay within the confines of a Hardware Security Module (HSM).
* Due to its importance, the root key should be protected by extra security measures. This could range from living in a
separate HSM to only existing as offline shards distributed across different geographical locations.

The PKI Tool is a CENM provided utility that can be used to generate a Corda compliant hierarchy.


## Features


* Allows a user to define their desired certificate hierarchy via a configuration file.
* Ability to generate private and public key pairs along with accompanying X509 certificates for all entities.
* Supports local key and certificate generation as well as HSM integration for Utimaco, Gemalto, Securosys and Azure Key Vault.
* Supports ‘additive’ mode, allowing a user to use existing keys to generate key pairs and certificates for entities further down the chain.
* Certificate Revocation List (CRL) file generation.


## Running the PKI Tool

The tool is designed to be executed from the command line, where the entire certificate hierarchy is specified in the
configuration file:

```bash
java -jar pkitool.jar --config-file <CONFIG_FILE>
```


### Generating Certificates for non-Production Deployments

By default, a check will be done on the proposed certificate hierarchy before any generation steps to ensure that CRL
information is present for all entities. If this is not required then this check can be disabled by passing the
`--ignore-missing-crl` or `-i` startup flag:

```bash
java -jar pkitool-<VERSION>.jar --ignore-missing-crl --config-file <CONFIG_FILE>
```

{{< note >}}
See [Certificate Revocation List Information](#certificate-revocation-list-information) section below to learn about configuring the CRL information.

{{< /note >}}

## Configuration


### Default Configuration

The PKI tool comes with the default configuration which can be used for testing. This configuration resembles a basic
version of the Corda Network certificate hierarchy, with the key omission of any CRL information. To generate the
certificate hierarchy using the default configuration, omit the `--config-file` argument:

```bash
java -jar pkitool.jar --ignore-missing-crl
```

The output of this command are a set of local key stores within the generated `key-stores/` directory along with the
network trust store within the generated `trust-stores/` directory. Note these directories are generated relative to
the working directory that the tool is run from.

{{< note >}}
The generated hierarchy will not have any CRL-related extensions included, hence the `--ignore-missing-crl` flag.

{{< /note >}}

### Custom Configuration

For anything other than a simple test, a custom configuration file can be created to define the hierarchy. Along with
other parameters, the configuration is composed of three main sections:


* [Key Stores Configuration](#key-stores-configuration): This is the list of key stores (local or HSM) that are used by the PKI tool. Each key
store is referenced by a certificate configuration and is used to either generate and store the key pair along with
the accompanying X509 certificate (if it does not currently exist). Alternatively, if the key pair and certificate
has been previously generated then the existing values will be used to generated the remaining entities in the
configured hierarchy.
* [Certificates Stores Configuration](#certificates-stores-configuration): This is a list of certificates stores (in the form of Java key stores) that
are used by the tool for storing generated certificates.
* [Certificates Configurations](#certificates-configurations): This is the list of configurations for the entities that form the desired certificate
hierarchy.

{{< note >}}
The full list of the configuration parameters can be found in config-pki-tool-parameters.

{{< /note >}}

#### Key Stores Configuration

This configuration block defines all key stores that should be used by the PKI Tool. Each key store can be either local
(backed by a Java key store file) or HSM (backed by a LAN HSM device). For HSM key stores, the available options and
authentication methods will depend on the HSM being used. See config-pki-tool-parameters for more details.

A mixture of key store types is allowed. That is, it is possible to generate some key pairs within a HSM device and
others locally. Note that mixing key store types is not supported for a given entity.


#### Certificates Stores Configuration

This configuration block defines all certificate stores that will contain generated certificates. All certificate stores
take the form of locally stored Java key store files, and contain no private keys.

{{< note >}}
A generated certificate will only be stored in a certificate store if explicitly specified via the `includeIn`
config parameter, or alternatively via the `defaultCertificatesStore` config parameter.

{{< /note >}}

#### Certificates Configurations

The certificates configuration block defines the actual entities that form the desired hierarchy, It is expressed as a
map from the user-defined alias to certificate configuration. The alias serves two purposes. Firstly, it can be used to
reference the given entity throughout the rest of the PKI Tool config. Secondly, it also defines the alias for the
generated (or existing) certificate entry in the corresponding certificate store. The certificate configuration defines
the entity specific properties of both the X509 certificate and associated key pair. See
config-pki-tool-parameters for more information.

If the desire is to use the resultant certificate hierarchy in a Corda network, this configuration block must define a
set of certificates that meet some basic requirements. In addition to the hierarchy having to be under a single trust
root (excluding SSL keys), it must include an entry for the Identity Manager CENM service, with the accompanying
certificate having the `DOORMAN_CA` role. It also must include an entry for the Network Map CENM service, with the
accompanying certificate having the `NETWORK_MAP` role. These certificate roles are validated by Corda nodes when they
receive a response from the CENM services, so failure to set the roles will result in a hierarchy incompatible with
Corda. CRL information is also needed if revocation is being used (see the [Certificate Revocation List Information](#certificate-revocation-list-information)
section below).

{{< note >}}
An additional `NETWORK_PARAMETERS` certificate role is available which can be used to create a different entity,
separate from the Network Map entity, that is responsible for signing Network Parameter changes. This can be useful
as a network operator will often want to have the Network Map signing task run automatically on a schedule. Having a
different PKI entity for each task allows the operator to keep the process of signing the high risk and infrequent
Network Parameter changes isolated from the low risk and frequent process of signing Network Map changes.

{{< /note >}}

{{< warning >}}
The additional `NETWORK_PARAMETERS` role is only supported in Corda nodes running platform version 4+. Therefore,
this should only ever be used in a network with `minimumPlatformVersion` >= 4.

{{< /warning >}}



##### Certificate Templates

Out of the box, the PKI Tool comes with some predefined certificate templates that can be used to generate a basic,
Corda compliant certificate hierarchy. Each template defines all necessary parameters, such as certificate subject, role
and signedBy attributes, and greatly reduces the size of the configuration file.

The following certificate templates are available:


{{< table >}}

|**Template Name**|**Description**|**Default Alias**|
|`CORDA_TLS_CRL_SIGNER`|Certificate for signing the CRL for the Corda Node’s TLS-level certificate|cordatlscrlsigner|
|`CORDA_ROOT`|Corda Root certificate|cordarootca|
|`CORDA_SUBORDINATE`|Corda Subordinate certificate|cordasubordinateca|
|`CORDA_IDENTITY_MANAGER`|Corda Identity Manager certificate|cordaidentitymanagerca|
|`CORDA_NETWORK_MAP`|Corda Network Map certificate|cordanetworkmap|
|`CORDA_SSL_ROOT`|Corda SSL Root certificate|cordasslrootca|
|`CORDA_SSL_IDENTITY_MANAGER`|Corda SSL Identity Manager certificate|cordasslidentitymanager|
|`CORDA_SSL_NETWORK_MAP`|Corda SSL Network Map certificate|cordasslnetworkmap|
|`CORDA_SSL_SIGNER`|Corda SSL Signer certificate|cordasslsigner|

{{< /table >}}

Each certificate type has a default key store associated with it that is protected with the default password “password”.
Similarly, the root and tls crl signer certificates are preconfigured to be stored in a default
“network-root-truststore” with the default password “trustpass”. As a result, there is no need to specify the
`keyStores` or `certificatesStore` configuration block.

A certificate template can be used in the `certificates` configuration block, in place of the certificate aliases,
by prepending the template name with `::`. A basic example of this is:

{{< note >}}
This is the same configuration that is used as the default when no configuration file is passed to the PKI Tool. It
represents the minimal configuration required to create a Corda network certificate hierarchy. It is mainly intended
to facilitate quick hierarchy creation for testing, and should not be used for generating production certificates.
One important omission from this template is CRL information, meaning that any network using the generated
certificates will not support revocation. See the section below on how the templates can be extended and customised.

{{< /note >}}

###### Customising The Templates

Customisation of the templates is supporting, allowing the default values within each template to be overridden. This
can be achieved by extending the template:

```guess
certificates = {
   ...
   "::CORDA_SUBORDINATE" {
     subject = "CN=Custom Subordinate Certificate, O=Custom Company, L=New York, C=US"
   },
   ...
}
```

In this scenario, the `CORDA_SUBORDINATE` certificate and key pair will be generated using the defaulted values from
the template for all parameters apart from the explicitly set subject.

The certificate alias can also be overridden by prepending the template notation with the chose custom alias. For
example, a custom alias for the root entity can be defined by:

```guess
certificates = {
    "customrootca::CORDA_ROOT",
    ...
}
```

{{< note >}}
It is important to remember of the signedBy relation. By default the Corda types have `signedBy` property set to
the alias of the signing certificate, which is assumed to be the default one. As such, whenever the default alias of
a certificate changes, all the certificates (configurations) being signed by this certificate needs to be updated by
overriding the `signedBy` property. Following is the example of that.

{{< /note >}}
An example configuration that uses templates and customisation is:


##### Free-form Certificates

As an alternative to using the templates, each key pair and certificate can defined using the standard configuration
options. See the config-pki-tool-parameters documentation for all possible parameters, and see below for examples
that use this approach. Note that the templates only support local key stores - using a HSM requires the certificate
hierarchy to be defined without templates.


##### Certificate Revocation List Information

Unless explicitly set, all configurations will be generated without CRL information. That is, unless the configuration
explicitly defines all necessary CRL file configurations or all CRL distribution URLs, all certificates will be
generated without the `Certificate Revocation List Distribution Point` extension and will therefore be incompatible
with any network using strict revocation checking.

As outlined in the config-pki-tool-parameters doc, this extension is defined using the following logic:


* If the certificate configuration has the `crlDistributionUrl` parameter set then use this.
* Otherwise take the `crlDistributionUrl` value from the parent entities CRL file configuration (if exists).

{{< note >}}
For a given certificate chain (e.g. a chain from the Node CA certificate back to the root), the revocation status of
each certificate in the chain will be resolved by downloading the Certificate Revocation List referenced in the
crlDistributionPoint extension and checking that the certificate is not present on this list. When strict revocation
checking is being used, any failures to resolve a certificate’s revocation status (e.g. if the endpoint is incorrect)
will be treated the same as a if the certificate was revoked. Therefore it is of the utmost importance that these CRL
endpoints are correct. Once a certificate has been generated, this crlDistributionPoint extension cannot be changed.

{{< /note >}}

###### CRL File Configuration

As referenced above, the PKI Tool can be configured to generate an accompanying CRL file for each CA entity via the
`crl` configuration block. This configuration determines the resulting CRL file for that entity as well as, by
association, the CRL endpoint configuration for any child entities in the hierarchy.

For example, a CRL file for the root can be defined:

```guess
certificates {
   ...
   "example-subordinate-alias" {
      ...
      crl = {
         crlDistributionUrl = "http://example-endpoint.com/certificate-revocation-list/subordinate"
         file = "./crl-files/subordinate.crl"
      }
   },
   "example-networkmap-alias" {
      ...
      issuesCertificates = false
      signedBy = "example-subordinate-alias"
   }
   ...
}
```

This will result in the encoded CRL file `crl-files/subordinate.crl` being created and will also result in any other
certificates that have been configured to be signed by “example-subordinate-alias” having the crlDistributionPoint
extension set to `http://example-endpoint.com/certificate-revocation-list/subordinate`. Note that this means that the
subordinate’s CRL file must be hosted, and available, on this endpoint.

{{< note >}}
Existing revocations can be added to the CRL file via the `crl.revocations` parameter. See
config-pki-tool-parameters for more information.

{{< /note >}}
For a given certificate, the exact crlDistributionPoint extension can be defined explicitly (rather than inheriting from
its parent) by using the top-level `crlDistributionUrl` parameter. This allows a certificate hierarchy to be defined
that can use previously or externally generated CRL files. The above configuration snippet can be defined without CRL
file configurations as follows:

```guess
certificates {
   ...
   "example-subordinate-alias" {
      ...
      crlDistributionUrl = "http://example-endpoint.com/certificate-revocation-list/root"
   },
   "example-networkmap-alias" {
      ...
      issuesCertificates = false
      signedBy = "example-subordinate-alias"
      crlDistributionUrl = "http://example-endpoint.com/certificate-revocation-list/subordinate"
   }
   ...
}
```

As previously mentioned, it is up to the network operator to ensure that any configured CRL endpoints are available.
The Identity Manager supports hosting of these CRL files (see the the “CRL Configuration” section of the
identity-manager doc).


##### HSM Libraries

If using the PKI Tool with a HSM then, due to the proprietary nature of the HSM libraries, the appropriate jars need to
be provided separately and referenced within the configuration file. The libraries that are required will depend on the
HSM that is being used.

An example configuration block for a PKI Tool integrating with a Utimaco HSM is:

```guess
hsmLibraries = [
    {
        type = UTIMACO_HSM
        jars = ["/path/to/CryptoServerJCE.jar"]
    }
]
```

Some HSMs (e.g. Gemalto Luna) also require shared libraries to be provided. An example configuration block for this is:

```guess
hsmLibraries = [
    {
        type = GEMALTO_HSM
        jars = ["/path/to/LunaProvider.jar"]
        sharedLibDir = "/path/to/shared-libraries/dir/"
    }
]
```

See the example configurations below to see these config blocks being used in a complete file.


###### Azure Key Vault

To keep inline with the other HSMs, the Azure Key Vault client jar needs to provided as above. Unlike the other HSMs,
there are many dependent libraries. The top-level dependencies are `azure-keyvault` and `adal4j`, however these both
have transitive dependencies that need to be included. That is, either all jars need to be provided separately (via a
comma-separated list) or an uber jar needs to be provided.

The gradle script below will build an uber jar. First copy the following text in to a new file called build.gradle
anywhere on your file system. Please do not change any of your existing build.gradle files.

```kotlin
plugins {
  id 'com.github.johnrengelman.shadow' version '4.0.4'
  id 'java'
}

repositories {
    jcenter()
}

dependencies {
    compile 'com.microsoft.azure:azure-keyvault:1.2.1'
    compile 'com.microsoft.azure:adal4j:1.6.4'
}

shadowJar {
    archiveName = 'azure-keyvault-with-deps.jar'
}
```

Then if gradle is on the path run the following command.

```kotlin
gradle shadowJar
```

or if gradle is not on the path but gradlew is in the current directory then run the following command.

```kotlin
./gradlew shadowJar
```

This will create a jar called `azure-keyvault-with-deps.jar` which can be referenced in the config.


##### Generating SSL Keys

As outlined in the enm-with-ssl doc, all inter-service CENM communication can be configured to encrypt their
messages via SSL. This feature requires the operator to provide a set of SSL key pairs and certificates to each service,
which can be generated using the PKI tool.

The template values described above can be used to generate these if required, or alternatively they be configured by
the operator. Note that these keys are only to establish trust between services and should be completely separate from
the main certificate hierarchy. Further more, in most cases, there should not be a need for CRL information - if they
key pairs need to be rotated for any reason then an operator can just regenerate a new set of trusted key pairs and
reconfigure the CENM services to use these.

A basic example configuration using the templates is:

```guess
certificates = {
   "::CORDA_SSL_ROOT"
   "::CORDA_SSL_IDENTITY_MANAGER"
   "::CORDA_SSL_NETWORK_MAP"
   "::CORDA_SSL_SIGNER"
}
```


### Configuration Examples

{{< note >}}
HSM keys used by the Signing Service require an accompanying certificate store that contains all certificates in
the chain, from the signing entity back to the root. This is because the full chains cannot be stored within the
HSMs. Refer to the signing-service documentation for more information.

{{< /note >}}

#### Full Configuration (using Local key stores)


#### Local Configuration


#### Utimaco HSM Configuration


#### Gemalto HSM Configuration


#### Securosys HSM Configuration


#### Azure Key Vault HSM Configuration

