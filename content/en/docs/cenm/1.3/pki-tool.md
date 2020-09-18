---
aliases:
- /pki-tool.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-pki-tool
    parent: cenm-1-3-tools-index
    weight: 1010
tags:
- pki
- tool
title: Public Key Infrastructure (PKI) Tool
---


# Public Key Infrastructure (PKI) Tool



## Overview

As described in the [Certificate Hierarchy Guide](pki-guide.md), a certificate hierarchy with certain properties is required to run a Corda
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

For more information about X.500 Name constraints, see the `Node naming` section in the [Corda documentation](../../corda-os/3.4/generating-a-node.md).

## Features


* Allows a user to define their desired certificate hierarchy via a configuration file.
* Ability to generate private and public key pairs along with accompanying X509 certificates for all entities.
* Supports local key and certificate generation as well as HSM integration for Utimaco, Gemalto, Securosys, Azure Key Vault and AWS CloudHSM.
* Supports ‘additive’ mode, allowing a user to use existing keys to generate key pairs and certificates for entities further down the chain.
* Certificate Revocation List (CRL) file generation.


## Running the PKI Tool

The tool is designed to be executed from the command-line, where the entire certificate hierarchy is specified in the
configuration file:

```bash
java -jar pkitool.jar --config-file <CONFIG_FILE>
```


### Generating Certificates for non-Production Deployments

By default, a check will be done on the proposed certificate hierarchy before any generation steps to ensure that CRL
information is present for all entities. If this is not required then this check can be disabled by passing the
`--ignore-missing-crl` or `-i` start-up flag:

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
The full list of the configuration parameters can be found in [Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md).

{{< /note >}}

#### Key Stores Configuration

This configuration block defines all key stores that should be used by the PKI Tool. Each key store can be either local
(backed by a Java key store file) or HSM (backed by a LAN HSM device). For HSM key stores, the available options and
authentication methods will depend on the HSM being used. See [Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md) for more details.

A mixture of key store types is allowed. That is, it is possible to generate some key pairs within a HSM device and
others locally. Note that mixing key store types is not supported for a given entity.


#### Certificates Stores Configuration

This configuration block defines all certificate stores that will contain generated certificates. All certificate stores
take the form of locally stored Java key store files, and contain no private keys.

{{< note >}}
A generated certificate will only be stored in a certificate store if explicitly specified via the `includeIn`
config parameter, or alternatively via the `defaultCertificatesStore` configuration parameter.

{{< /note >}}

#### Certificates Configurations

The certificates configuration block defines the actual entities that form the desired hierarchy, It is expressed as a
map from the user-defined alias to certificate configuration. The alias serves two purposes. Firstly, it can be used to
reference the given entity throughout the rest of the PKI Tool config. Secondly, it also defines the alias for the
generated (or existing) certificate entry in the corresponding certificate store. The certificate configuration defines
the entity specific properties of both the X509 certificate and associated key pair. See
[Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md) for more information.

If the desire is to use the resultant certificate hierarchy in a Corda network, this configuration block must define a
set of certificates that meet some basic requirements. In addition to the hierarchy having to be under a single trust
root (excluding SSL keys), it must include an entry for the Identity Manager CENM service, with the accompanying
certificate having the `DOORMAN_CA` role. It also must include an entry for the Network Map CENM service, with the
accompanying certificate having the `NETWORK_MAP` role. These certificate roles are validated by Corda nodes when they
receive a response from the CENM services, so failure to set the roles will result in a hierarchy incompatible with
Corda. CRL information is also needed if revocation is being used (see the [Certificate Revocation List Information](#certificate-revocation-list-information)
section below).


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

```docker
certificates = {
    "::CORDA_ROOT",
    "::CORDA_TLS_CRL_SIGNER",
    "::CORDA_SUBORDINATE",
    "::CORDA_IDENTITY_MANAGER",
    "::CORDA_NETWORK_MAP",
    "::CORDA_NETWORK_PARAMETERS"
}
```

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

```docker
certificates = {
    "::CORDA_TLS_CRL_SIGNER" {
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
        }
    },
    "customrootca::CORDA_ROOT" {
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "::CORDA_SUBORDINATE" {
        signedBy = "customrootca"
        subject = "CN=Custom Subordinate Certificate, O=Custom Company, L=New York, C=US"
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "::CORDA_IDENTITY_MANAGER",
    "::CORDA_NETWORK_MAP"
}
```

##### Free-form Certificates

As an alternative to using the templates, each key pair and certificate can defined using the standard configuration
options. See the [Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md) documentation for all possible parameters, and see below for examples
that use this approach. Note that the templates only support local key stores - using a HSM requires the certificate
hierarchy to be defined without templates.


##### Certificate Revocation List Information

Unless explicitly set, all configurations will be generated without CRL information. That is, unless the configuration
explicitly defines all necessary CRL file configurations or all CRL distribution URLs, all certificates will be
generated without the `Certificate Revocation List Distribution Point` extension and will therefore be incompatible
with any network using strict revocation checking.

As outlined in the [Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md) doc, this extension is defined using the following logic:


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
[Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md) for more information.

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
[Identity Manager Service](identity-manager.md) doc).


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

Some HSMs (e.g. Gemalto Luna, AWS CloudHSM) also require shared libraries to be provided. An example configuration block for this is:

```guess
hsmLibraries = [
    {
        type = GEMALTO_HSM
        jars = ["/path/to/LunaProvider.jar"]
        sharedLibDir = "/path/to/shared-libraries/dir/"
    }
]
```

See the example configurations below to see these configuration blocks being used in a complete file.


###### Azure Key Vault

To keep inline with the other HSMs, the Azure Key Vault client `.jar` needs to provided as above. Unlike the other HSMs,
there are many dependent libraries. The top-level dependencies are `azure-keyvault` and `adal4j`, however these both
have transitive dependencies that need to be included. That is, either all jars need to be provided separately (via a
comma-separated list) or an uber `.jar` needs to be provided.

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

This will create a `.jar` called `azure-keyvault-with-deps.jar` which can be referenced in the config.


##### Generating SSL Keys

As outlined in the [Configuring the CENM services to use SSL](enm-with-ssl.md) doc, all inter-service CENM communication can be configured to encrypt their
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
HSMs. Refer to the [Signing Services](signing-service.md) documentation for more information.

{{< /note >}}

#### Full Configuration (using Local key stores)

```docker
keyStores = {
    "identity-manager-key-store" = {
        type = LOCAL
        file = "./key-stores/identity-manager-key-store.jks"
        password = "key-password"
    }
    "network-map-key-store" = {
        type = LOCAL
        file = "./key-stores/network-map-key-store.jks"
        password = "key-password"
    }
    "network-parameters-key-store" = {
        type = LOCAL
        file = "./key-stores/network-parameters-key-store.jks"
        password = "key-password"
    }
    "subordinate-key-store" = {
        type = LOCAL
        file = "./key-stores/subordinate-key-store.jks"
        password = "key-password"
    }
    "root-key-store" = {
        type = LOCAL
        file = "./key-stores/root-key-store.jks"
        password = "key-password"
    }
    "tls-crl-signer-key-store" = {
        type = LOCAL
        file = "./key-stores/tls-crl-signer-key-store.jks"
        password = "key-password"
    }
    "corda-ssl-auth-keys" = {
         type = LOCAL
         file = "./key-stores/ssl-auth-key-store.jks"
         password = "password"
    }
    "corda-ssl-farm-keys" = {
         type = LOCAL
         file = "./key-stores/corda-ssl-farm-keys.jks"
         password = "key-password"
    }
    "corda-ssl-farm-private-keys" = {
         type = LOCAL
         file = "./key-stores/corda-ssl-farm-private-keys.jks"
         password = "key-password"
    }
    "corda-ssl-identity-manager-keys" = {
        type = LOCAL
        file = "./key-stores/ssl-identity-manager-key-store.jks"
        password = "key-password"
    }
    "corda-ssl-network-map-keys" = {
        type = LOCAL
        file = "./key-stores/ssl-network-map-key-store.jks"
        password = "key-password"
    }
    "corda-ssl-root-keys" = {
        type = LOCAL
        file = "./key-stores/ssl-root-key-store.jks"
        password = "key-password"
    }
    "corda-ssl-signer-keys" = {
        type = LOCAL
        file = "./key-stores/ssl-signer-key-store.jks"
        password = "key-password"
    }
    "corda-ssl-zone-keys" = {
        type = LOCAL
        file = "./key-stores/corda-ssl-zone-keys.jks"
        password = "key-password"
    }
}
certificatesStores = {
    "network-root-trust-store" = {
        file = "./trust-stores/network-root-truststore.jks"
        password = "trust-store-password"
    }
    "corda-ssl-trust-store" = {
        file = "./trust-stores/corda-ssl-trust-store.jks"
        password = "trust-store-password"
    }
}
certificates = {
    "cordatlscrlsigner" = {
        key = {
            type = LOCAL
            includeIn = ["tls-crl-signer-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = true
        keyUsages = [CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-root-trust-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            indirectIssuer = true
            issuer = "CN=Corda TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
            file = "./crl-files/tls.crl"
        }
    },
    "cordarootca" = {
        key = {
            type = LOCAL
            includeIn = ["root-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = true
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = true
        subject = "CN=Test Root CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-root-trust-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasslrootca" = {
        key = {
            type = LOCAL
            includeIn = ["corda-ssl-root-keys"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = true
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = true
        subject = "CN=Test SSL Root CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["corda-ssl-trust-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/sslroot"
            file = "./crl-files/sslroot.crl"
        }
    },
    "cordasubordinateca" = {
        key = {
            type = LOCAL
            includeIn = ["subordinate-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordarootca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = true
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        key = {
            type = LOCAL
            includeIn = ["identity-manager-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordasubordinateca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        role = DOORMAN_CA
        issuesCertificates = true
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
    },
    "cordanetworkmap" = {
        key = {
            type = LOCAL
            includeIn = ["network-map-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordasubordinateca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        role = NETWORK_MAP
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
    },
    "cordanetworkparameters" = {
        key = {
            type = LOCAL
            includeIn = ["network-parameters-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordasubordinateca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        role = NETWORK_MAP
        issuesCertificates = false
        subject = "CN=Test Network Parameters Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
    },
    "cordasslidentitymanager" = {
        key = {
            type = LOCAL
            includeIn = ["corda-ssl-identity-manager-keys"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordasslrootca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = false
        subject = "CN=Test Identity Manager SSL Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["corda-ssl-trust-store"]
    },
    "cordasslnetworkmap" = {
        key = {
            type = LOCAL
            includeIn = ["corda-ssl-network-map-keys"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "password"
        }
        isSelfSigned = false
        signedBy = "cordasslrootca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = false
        subject = "CN=Test Network Map SSL Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["corda-ssl-trust-store"]
    },
    "cordasslsigner" = {
        key = {
            type = LOCAL
            includeIn = ["corda-ssl-signer-keys"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordasslrootca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = false
        subject = "CN=Test Signer SSL Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["corda-ssl-trust-store"]
    },
    "cordasslauth" = {
        key = {
            type = LOCAL
            includeIn = ["corda-ssl-auth-keys"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordasslrootca"
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = false
        subject = "CN=Test Auth SSL Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["corda-ssl-trust-store"]
    },
    "cordasslfarm" = {
       key = {
            type = LOCAL
            includeIn = ["corda-ssl-farm-keys"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "key-password"
        }
        isSelfSigned = false
        signedBy = "cordasslrootca"
        keyUsages = [DIGITAL_SIGNATURE]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = false
        subject = "CN=Test Farm TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
        includeIn = ["corda-ssl-trust-store"]
    },
    "cordasslfarm-private" = {
        key = {
             type = LOCAL
             includeIn = ["corda-ssl-farm-private-keys"]
             algorithm = "ECDSA_SECP256R1_SHA256"
             password = "key-password"
         }
         isSelfSigned = false
         signedBy = "cordasslrootca"
         keyUsages = [DIGITAL_SIGNATURE]
         keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
         validDays = 7300
         issuesCertificates = false
         subject = "CN=Test Farm Private TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
         includeIn = ["corda-ssl-trust-store"]
     },
     "cordasslzone" = {
         key = {
             type = LOCAL
             includeIn = ["corda-ssl-zone-keys"]
             algorithm = "ECDSA_SECP256R1_SHA256"
             password = "key-password"
         }
         isSelfSigned = false
         signedBy = "cordasslrootca"
         keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
         keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
         validDays = 7300
         issuesCertificates = false
         subject = "CN=Test Zone SSL Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
         includeIn = ["corda-ssl-trust-store"]
     }
}
```

#### Local Configuration

```docker
defaultPassword = "password"
keyStores = {
    "identity-manager-key-store" = {
        type = LOCAL
        file = "./key-stores/identity-manager-key-store.jks"
    }
    "network-map-key-store" = {
        type = LOCAL
        file = "./key-stores/network-map-key-store.jks"
    }
    "subordinate-key-store" = {
        type = LOCAL
        file = "./key-stores/subordinate-key-store.jks"
    }
    "root-key-store" = {
        type = LOCAL
        file = "./key-stores/root-key-store.jks"
    }
    "tls-crl-signer-key-store" = {
        type = LOCAL
        file = "./key-stores/tls-crl-signer-key-store.jks"
    }
}
certificatesStores = {
    "truststore" = {
        file = "./trust-stores/network-root-truststore.jks"
    }
}
certificates = {
    "cordatlscrlsigner" = {
        key = {
            type = LOCAL
            includeIn = ["tls-crl-signer-key-store"]
        }
        isSelfSigned = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["truststore"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        }
    },
    "cordarootca" = {
        key = {
            type = LOCAL
            includeIn = ["root-key-store"]
        }
        isSelfSigned = true
        subject = "CN=Test Foundation Service Root Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["truststore"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasubordinateca" = {
        key = {
            type = LOCAL
            includeIn = ["subordinate-key-store"]
        }
        signedBy = "cordarootca"
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        key = {
            type = LOCAL
            includeIn = ["identity-manager-key-store"]
        }
        signedBy = "cordasubordinateca"
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        role = DOORMAN_CA
    },
    "cordanetworkmap" = {
        key = {
            type = LOCAL
            includeIn = ["network-map-key-store"]
        }
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        role = NETWORK_MAP
    }
}
```

#### Utimaco HSM Configuration

```docker
hsmLibraries = [{
    type = UTIMACO_HSM
    jars = ["/path/to/CryptoServerJCE.jar"]
}]

defaultPassword = "password"
defaultKeyStores = ["example-hsm-key-store"]

keyStores = {
    "example-hsm-key-store" = {
        type = UTIMACO_HSM
        host = "192.0.0.1"
        port = "288"
        users = [{
            mode = "PASSWORD"
            username = "example-user-1"
            password = "example-password-1"
        }]
    }
}
certificatesStores = {
    "network-truststore" = {
        file = "./trust-stores/network-trust-store.jks"
    },
    "certificate-store" = {
        file = "./trust-stores/certificate-store.jks"
    }
}
certificates = {
    "cordatlscrlsigner" = {
        isSelfSigned = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        }
    },
    "cordarootca" = {
        isSelfSigned = true
        subject = "CN=Test Foundation Service Root Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasubordinateca" = {
        signedBy = "cordarootca"
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        signedBy = "cordasubordinateca"
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = DOORMAN_CA
    },
    "cordanetworkmap" = {
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = NETWORK_MAP
    }
}
```

#### Gemalto HSM Configuration

```docker
hsmLibraries = [{
    type = GEMALTO_HSM
    jars = ["/path/to/primusX.jar"]
    sharedLibDir = "/path/to/shared/lib/dir/"
}]

defaultPassword = "password"
defaultKeyStores = ["example-hsm-key-store"]

keyStores = {
    "example-hsm-key-store" = {
        type = GEMALTO_HSM
        user = {
            keyStore = "tokenlabel:example-label"
            password = "example-password"
        }
    }
}
certificatesStores = {
    "network-truststore" = {
        file = "./trust-stores/network-trust-store.jks"
    },
    "certificate-store" = {
        file = "./trust-stores/certificate-store.jks"
    }
}
certificates = {
    "cordatlscrlsigner" = {
        isSelfSigned = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        }
    },
    "cordarootca" = {
        isSelfSigned = true
        subject = "CN=Test Foundation Service Root Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasubordinateca" = {
        signedBy = "cordarootca"
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        signedBy = "cordasubordinateca"
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = DOORMAN_CA
    }
    "cordanetworkmap" = {
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = NETWORK_MAP
    }
}
```

#### Securosys HSM Configuration

```docker
hsmLibraries = [{
    type = SECUROSYS_HSM
    jars = ["/path/to/primusX.jar"]
}]

defaultPassword = "password"
defaultKeyStores = ["example-hsm-key-store"]

keyStores = {
    "example-hsm-key-store" = {
        type = SECUROSYS_HSM
        host = "192.0.0.1"
        port = 288
        users = [{
            username = "example-user-1"
            password = "example-password-1"
        }]
    }
}
certificatesStores = {
    "network-truststore" = {
        file = "./trust-stores/network-trust-store.jks"
    },
    "certificate-store" = {
        file = "./trust-stores/certificate-store.jks"
    }
}
certificates = {
    "cordatlscrlsigner" = {
        isSelfSigned = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=U"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=U"
        }
    },
    "cordarootca" = {
        isSelfSigned = true
        subject = "CN=Test Foundation Service Root Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasubordinateca" = {
        signedBy = "cordarootca"
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        signedBy = "cordasubordinateca"
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = DOORMAN_CA
    },
    "cordanetworkmap" = {
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = NETWORK_MAP
    }
}
```

#### Azure Key Vault HSM Configuration

```docker
hsmLibraries = [{
    type = AZURE_KEY_VAULT_HSM
    jars = ["/path/to/akvLibraries.jar"]
}]

defaultPassword = "password"
defaultKeyStores = ["example-hsm-key-store"]

keyStores = {
    "example-hsm-key-store" = {
        type = AZURE_KEY_VAULT_HSM
        keyVaultUrl = "http://example.com"
        protection = "HARDWARE"
        credentials = {
            keyStorePath = "/path/to/keystore.pem"
            keyStorePassword = "example-password"
            keyStoreAlias = "example-alias"
            clientId = "01234567-89ab-cdef-0123-456789abcdef"
        }
    }
}

certificatesStores = {
    "network-truststore" = {
        file = "./trust-stores/network-trust-store.jks"
    },
    "certificate-store" = {
        file = "./trust-stores/certificate-store.jks"
    }
}

certificates = {
    "cordatlscrlsigner" = {
        isSelfSigned = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        }
    },
    "cordarootca" = {
        isSelfSigned = true
        subject = "CN=Test Foundation Service Root Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasubordinateca" = {
        signedBy = "cordarootca"
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        signedBy = "cordasubordinateca"
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = DOORMAN_CA
    },
    "cordanetworkmap" = {
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = NETWORK_MAP
    }
}
```

#### AWS CloudHSM Configuration

```docker
hsmLibraries = [{
    type = AMAZON_CLOUD_HSM
    jars = ["/opt/cloudhsm/java/cloudhsm-3.0.0.jar"]
    sharedLibDir = "/opt/cloudhsm/lib"
}]

defaultPassword = "password"
defaultKeyStores = ["example-hsm-key-store"]

keyStores = {
    "example-hsm-key-store" = {
        type = AMAZON_CLOUD_HSM
        credentialsAmazon = {
    		partition = "<partition>"
    		userName = "<user>"
    		password = "<password>"
    	}
    	localCertificateStore = {
    		file = "./new-certificate-store.jks"
    		password = "password"
    	}
    }
}

certificatesStores = {
    "network-truststore" = {
        file = "./trust-stores/network-trust-store.jks"
    },
    "certificate-store" = {
        file = "./trust-stores/certificate-store.jks"
    }
}

certificates = {
    "cordatlscrlsigner" = {
        isSelfSigned = true
        subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            file = "./crl-files/tls.crl"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        }
    },
    "cordarootca" = {
        isSelfSigned = true
        subject = "CN=Test Foundation Service Root Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["network-truststore", "certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    },
    "cordasubordinateca" = {
        signedBy = "cordarootca"
        subject = "CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "cordaidentitymanagerca" = {
        signedBy = "cordasubordinateca"
        subject = "CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = DOORMAN_CA
    },
    "cordanetworkmap" = {
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US"
        includeIn = ["certificate-store"]
        role = NETWORK_MAP
    }
}
```
