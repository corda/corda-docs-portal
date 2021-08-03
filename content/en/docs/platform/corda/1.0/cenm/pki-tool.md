---
aliases:
- /releases/release-1.0/pki-tool.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-pki-tool
    parent: cenm-1-0-tools-index
    weight: 1010
tags:
- pki
- tool
title: Public Key Infrastructure (PKI) Tool
---


# Public Key Infrastructure (PKI) Tool

The purpose of the PKI Tool is to facilitate the certificate hierarchy generation process. Using the tool one is able to
set up key stores (both local and HSM) with customised certificates and generate accompanied certificate revocation lists.

## Running the PKI Tool

The tool is designed to be executed from the command line, where the entire certificate hierarchy is specified in the
configuration file.

Command line syntax:

```bash
java -jar pkitool-<VERSION>.jar --config-file <CONFIG_FILE>
```

## Generating Certificates for non-Production Deployments

If the generated certificate hierarchy is not intended for the production deployment and the CRL information
is not necessary to be present in the certificates, the configuration validation against the CRL config needs
to be disabled. To do so, the `--ignore-missing-crl` needs to be passed to the execution command.

```bash
java -jar pkitool-<VERSION>.jar --ignore-missing-crl --config-file <CONFIG_FILE>
```

{{< note >}}
See [Configuring Certificate Revocation List Data](#configuring-certificate-revocation-list-data) section below to learn about configuring the CRL information.

{{< /note >}}

## Default Configuration

The PKI tool comes with the default configuration. This configuration resembles the Corda Network certificate hierarchy.
In order to generate the certificate hierarchy using the default configuration, please omit the –config-file argument.

Command line syntax:

```bash
java -jar pkitool-<VERSION>.jar
```

Expected output:

The artifacts produced by this command are the key stores and the network trust store. Those can be found in the relevant
directories under the path, where the tool has been executed.

{{< note >}}
The generated hierarchy will not have any CRL-related extensions included.
Moreover, the default configuration assumes local key stores and as such it is not applicable for production deployments.

{{< /note >}}

## Configuration

The PKI Tool configuration is composed of three sections:

* Key stores configuration. This is a list of key stores that are used by the tool in order to either store the
generated keys and certificate chains or to be inspected for the signing key retrieval.
* Certificates stores configuration. This is a list of certificates stores that are used by the tool for storing generated
certificates.
* Certificate hierarchy configuration. It consists of certificates and keys specification.

{{< note >}}
The full list of the configuration parameters can be found in [Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md).

{{< /note >}}

## Key stores configuration

Key stores specification defines the key stores used by the PKI Tool.
The key stores can be either local (backed by a JKS file) or HSM (backed by a LAN HSM device). For the HSM devices, the
tool supports different kind of authentications. See [Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md) for more details.
The mixed list of the key store types is allowed by the tool.
This way the scenario where some keys are generated on an HSM device and some are stored locally is supported.

### Example of local key stores specification

```guess
keyStores = {
    "identity-manager-key-store" = {
        file = "./identity-manager-key-store.jks"
        password = "Password123"
    }
    "network-map-key-store" = {
        file = "./network-map-key-store.jks"
        password = "Password123"
    }
    "root-key-store" = {
        file = "./root-key-store.jks"
        password = "Password123"
    }
}
```

### Example of HSM key stores specification

```guess
keyStores = {
    "identity-manager-key-store" = {
        host = "192.0.0.1"
        port = "288"
        users = [{
            mode = "PASSWORD"
            password = "Password123"
            username = "USER"
        }]
    }
    "network-map-key-store" = {
        host = "192.0.0.1"
        port = "288"
        users = [{
            mode = "PASSWORD"
            password = "Password123"
            username = "USER"
        }]
    }
    "root-key-store" = {
        host = "192.0.0.1"
        port = "288"
        users = [{
            mode = "PASSWORD"
            password = "Password123"
            username = "USER"
        }]
    }
}
```

### Example of mixed key stores specification

```guess
keyStores = {
    "identity-manager-key-store" = {
        file = "./identity-manager-key-store.jks"
        password = "Password123"
    }
    "network-map-key-store" = {
        file = "./network-map-key-store.jks"
        password = "Password123"
    }
    "root-key-store" = {
        host = "192.0.0.1"
        port = "288"
        users = [{
            mode = "PASSWORD"
            password = "Password123"
            username = "USER"
        }]
    }
}
```

In case of the local key store specification, the password attribute can be omitted and in such a case the
value defined in *defaultPassword* will be used.

### Example of local key stores specification without password

```guess
defaultPassword = "Password123"
keyStores = {
    "identity-manager-key-store" = {
        file = "./identity-manager-key-store.jks"
    }
    "network-map-key-store" = {
        file = "./network-map-key-store.jks"
    }
    "root-key-store" = {
        file = "./root-key-store.jks"
    }
}
```

## Certificates stores configuration

The certificates stores configuration is a list the certificates stores that will hold the generated certificates.

### Example of the certificates stores specification

```guess
certificatesStores = {
    "network-root-trust-store" = {
        file = "./network-root-trust-store.jks"
        password = "Password123"
    }
   "all-certificates-store" = {
        file = "./all-certificates-store.jks"
        password = "Password123"
    }
}
```

Similarly, the password parameter can be omitted from the certificate store specification and the one defined under the
*defaultPassword* will be used instead.

### Example of certificates stores specification without password

```guess
defaultPassword = "Password123"
certificatesStores = {
    "network-root-trust-store" = {
        file = "./network-root-trust-store.jks"
    }
   "all-certificates-store" = {
        file = "./all-certificates-store.jks"
    }
}
```

## Certificate configuration

The certificate configuration consists of the actual certificate hierarchy definition. It is expressed as a map between
the aliases and certificate configuration objects. Most of the configuration parameters have default values, so if not
specified explicitly in the configuration file those will be used. See [Public Key Infrastructure (PKI) Tool Configuration Parameters](config-pki-tool-parameters.md) for more information.

Following is the example of the certificate hierarchy specification in the PKI Tool configuration file.

### Example of certificates configuration

```guess
keyStores = {
    "identity-manager-key-store" = {
        file = "./identity-manager-key-store.jks"
        password = "Password123"
    }
    "network-map-key-store" = {
        file = "./network-map-key-store.jks"
        password = "Password123"
    }
    "subordinate-key-store" = {
        file = "./root-key-store.jks"
        password = "Password123"
    }
    "root-key-store" = {
        file = "./root-key-store.jks"
        password = "Password123"
    }
}
certificatesStores = {
    "network-root-trust-store" = {
        file = "./network-root-trust-store.jks"
        password = "Password123"
    }
}
certificates = {
    "cordarootca" = {
        key = {
            alias = "cordarootca"
            includeIn = ["root-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "Password123"
        }
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = true
        isSelfSigned = true
        subject = "CN=Corda Foundation Service Root Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
        includeIn = ["network-root-trust-store"]
    },
    "cordasubordinateca" = {
        key = {
            alias = "cordasubordinateca"
            includeIn = ["subordinate-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "Password123"
        }
        isSelfSigned = false
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        issuesCertificates = true
        signedBy = "cordarootca"
        subject = "CN=Corda Subordinate CA Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
    },
    "cordaidentitymanagerca" = {
        key = {
            alias = "cordaidentitymanagerca"
            includeIn = ["identity-manager-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "Password123"
        }
        isSelfSigned = false
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        role = DOORMAN_CA
        issuesCertificates = true
        signedBy = "cordasubordinateca"
        subject = "CN=Corda Identity Manager Service Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
    }
    "cordanetworkmap" = {
        key = {
            alias = "cordanetworkmap"
            includeIn = ["network-map-key-store"]
            algorithm = "ECDSA_SECP256R1_SHA256"
            password = "Password123"
        }
        isSelfSigned = false
        keyUsages = [DIGITAL_SIGNATURE, KEY_CERT_SIGN, CRL_SIGN]
        keyPurposes = [SERVER_AUTH, CLIENT_AUTH]
        validDays = 7300
        role = NETWORK_MAP
        signedBy = "cordasubordinateca"
        issuesCertificates = false
        subject = "CN=Corda Network Map Service Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
    }
}
```

Assuming default values this could be reduced to the following:

### Example of certificates configuration (reduced)

```guess
defaultPassword = "Password123"
defaultKeyStores = ["key-store"]
keyStores = {
    "key-store" = {
        file = "./key-store.jks"
    }
}
defaultCertificatesStores = ["certificates-store"]
certificatesStores = {
   "certificates-store" = {
        file = "./certificates-store.jks"
    }
}
certificates = {
    "cordarootca" = {
        subject = "CN=Corda Foundation Service Root Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
    },
    "cordasubordinateca" = {
        signedBy = "cordarootca"
        subject = "CN=Corda Subordinate CA Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
    },
    "cordaidentitymanagerca" = {
        signedBy = "cordasubordinateca"
        role = DOORMAN_CA
        subject = "CN=Corda Identity Manager Service Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
    }
    "cordanetworkmap" = {
        signedBy = "cordasubordinateca"
        role = NETWORK_MAP
        subject = "CN=Corda Network Map Service Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
    }
}
```

## Corda Certificate Types

To simplify Corda compliant certificate hierarchy, the PKI Tool introduces Corda certificate types. Those can be seen,
as predefined certificate configurations that default even more values than those that can be seen above.
Each Corda certificate type has its subject, role and signer predefined as well. Therefore, in scenarios where slight adjustment
to the Corda hierarchy is required, this feature comes very handy and reduces the amount of configuration a user needs to provide.

Following are the Corda certificate types that can be used in the certificate hierarchy configuration:

### Corda Network Certificates

* `CORDA_TLS_CRL_SIGNER` - certificate for signing the CRL for the Corda Node’s TLS-level certificate.
* `CORDA_ROOT` - Corda Root certificate
* `CORDA_SUBORDINATE` - Corda Subordinate certificate
* `CORDA_IDENTITY_MANAGER` - Corda Identity Manager certificate
* `CORDA_NETWORK_MAP` - Corda Network Map certificate

### SSL Certificates for Corda Network Services

* `CORDA_SSL_ROOT` - Corda SSL Root certificate
* `CORDA_SSL_IDENTITY_MANAGER` - Corda SSL Identity Manager certificate
* `CORDA_SSL_NETWORK_MAP` - Corda SSL Network Map certificate
* `CORDA_SSL_SIGNER` - Corda SSL Signer certificate

### Corda Certificate Types usage

Corda certificate types can be used in the certificate hierarchy configuration in place of
the certificate aliases prepended with `::`.

### Example (Corda Network hierarchy with Corda Certificate Types)

```guess
certificates = {
    "::CORDA_ROOT",
    "::CORDA_TLS_CRL_SIGNER",
    "::CORDA_SUBORDINATE",
    "::CORDA_IDENTITY_MANAGER",
    "::CORDA_NETWORK_MAP"
}
```

{{< note >}}
Apart from the no-config-file execution of the PKI Tool, this is the minimal configuration required to recreate
the Corda Network certificate hierarchy. Important note is that this hierarchy will not have CRL data included,
therefore it will not work in environments where the certificate revocation functionality is required. In order,
to have the certificate revocation support, some customizations are necessary. See below for more details.

{{< /note >}}

### Example (Corda SSL Certificate Types)

```guess
certificates = {
    "::CORDA_SSL_ROOT",
    "::CORDA_SSL_IDENTITY_MANAGER",
    "::CORDA_SSL_NETWORK_MAP",
    "::CORDA_SSL_SIGNER"
}
```

Each certificate type has a default key store associated with it that is protected with the default password: “password”.
As such there is no need for the `keyStores` section specification.
Similar goes with the `certificatesStore`. By default the “network-root-truststore.jks” certificates store file
protected with the “trustpass” password is created and only two: “CORDA_ROOT” and “CORDA_TLS_CRL_SIGNER” certificates
are included in this store.

The above Corda certificate type configuration assumes also the default certificate/key aliases. Those are as following:

### Corda Certificate Types Aliases

* `CORDA_TLS_CRL_SIGNER` - “cordatlscrlsigner”
* `CORDA_ROOT` - “cordarootca”
* `CORDA_SUBORDINATE` - “cordasubordinateca”
* `CORDA_IDENTITY_MANAGER` - “cordaidentitymanagerca”
* `CORDA_NETWORK_MAP` - “cordanetworkmap”
* `CORDA_SSL_ROOT` - “cordasslrootca”
* `CORDA_SSL_IDENTITY_MANAGER` - “cordasslidentitymanager”
* `CORDA_SSL_NETWORK_MAP` - “cordasslnetworkmap”
* `CORDA_SSL_SIGNER` - “cordasslsigner”

In order to use your custom aliases for certificate/key referencing, one needs to prepend the Corda certificate types with
the chosen alias. Following is the usage example for custom aliases with Corda certificate types:

### Example (Corda Certificate Types with custom aliases)

```guess
certificates = {
    "customrootca::CORDA_ROOT",
    ...
}
```

The above configuration results in the Corda Network hierarchy generation, where each certificate/key is now aliased
(within the corresponding key store) with the `custom*` aliases.

Apart from the alias customization, the Corda certificate types can be customised further
by overriding the default properties of the certificate configuration.
Following is the example of the `subject` property customization in the CORDA_NETWORK_MAP certificate type.

### Example (Corda Certificate Types with custom properties)

```guess
certificates = {
    ...
    "networkmap::CORDA_NETWORK_MAP" = {
         subject = "CN=Custom Network Map Service Certificate, OU=Custom, O=Custom Company, L=New York, C=US"
    }
}
```

In the similar vein, other properties can be override.

{{< note >}}
It is important to remember of the signed-by relation. By default the Corda types have `signedBy` property
set to the alias of the signing certificate, which is assumed to be the default one. As such,
whenever the default alias of a certificate changes, all the certificates (configurations) being signed by
this certificate needs to be updated by overriding the `signedBy` property. Following is the example of that.

{{< /note >}}

### Example (Corda Certificate Types with custom aliases)

```guess
certificates = {
    "customrootca::CORDA_ROOT",
    "customtlscrlsigner::CORDA_TLS_CRL_SIGNER",
    "customsubordinateca::CORDA_SUBORDINATE" = {
         signedBy = "customrootca"
    },
    "customidentitymanagerca::CORDA_IDENTITY_MANAGER" = {
         signedBy = "customsubordinateca"
    },
    "customnetworkmap::CORDA_NETWORK_MAP" = {
         signedBy = "customsubordinateca"
    }
}
```

## Configuring Certificate Revocation List Data

By default all certificate configurations (including the Corda certificate types) come without the certificate revocation
information. As such, all the certificates will be generated without `Certificate Revocation List Distribution Point`
extension. In order to configure the Certificate Revocation Distribution Point extension and potentially generate a
CRL file signed by the CRL issuer, the issuing certificate configuration needs to be enriched by the CRL configuration block.

### Example (Corda Certificate Types with CRL configuration)

```guess
certificates = {
    "::CORDA_TLS_CRL_SIGNER" = {
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/tls"
            indirectIssuer = true
            issuer = "CN=Corda TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
            filePath = "./crl-files/tls.crl"
        }
    },
    "::CORDA_ROOT" = {
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/root"
            filePath = "./crl-files/root.crl"
        }
    }
    "::CORDA_SUBORDINATE" = {
        crl = {
            crlDistributionUrl = "http://127.0.0.1/certificate-revocation-list/subordinate"
            filePath = "./crl-files/subordinate.crl"
        }
    },
    "::CORDA_IDENTITY_MANAGER",
    "::CORDA_NETWORK_MAP"
}
```

{{< note >}}
It is important to note that the CRL configuration block applies to the certificates issued by the CA which certificate
configuration is extended with the CRL configuration block. In the above example, the CRL block is present in the
`::CORDA_SUBORDINATE` certificate, however both `::CORDA_IDENTITY_MANAGER` and `::CORDA_NETWORK_MAP` are the certificates
that will have the CRL Distribution Point extension pointing to the `http://127.0.0.1/certificate-revocation-list/subordinate`
serving the “subordinate.crl” file.

{{< /note >}}
