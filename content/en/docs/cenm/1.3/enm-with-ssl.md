---
aliases:
- /enm-with-ssl.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-enm-with-ssl
    parent: cenm-1-3-configuration
    weight: 250
tags:
- enm
- ssl
title: Configuring the CENM services to use SSL
---


# Configuring the CENM services to use SSL

The following components of the CENM suite can all be configured to encrypt their inter-process communication channels.


* Identity Manager (containing previously named Doorman and Revocation services)
* Network Map
* Signing Service

How to configure this is discussed in this section, whilst the flow of information between these various components
is shown in the following diagram

![enm with ssl](/en/images/enm-with-ssl.png "enm with ssl")

## Recommended Key and Cert hierarchy

For SSL to work some PKI infrastructure must be in place. We recommend generating a self signed root key that can
then be used to sign a key for each service. This way, all that needs distributing to the machines hosting the JVMs
running the CENM components is a keystore containing the trust root (the Certificate representing the root key) and a
keystore containing the keypair generated for that service.

The SSL handshake will, when one component talks to another, check that the exchanged keys have a certificate chain
that chains back to the common root.


{{< important >}}
For the avoidance of doubt, the trust root, certificates and keys used to secure communication between
CENM components are completely independent of those created/managed by this toolset for the management of
a Corda network.


{{< /important >}}

Thus the key signing hierarchy would be


* Root
* Identity Manager
* Network Map
* Revocation
* Signing Service (including CSRs, CRRs, CRLs, Network Parameters, and the Network Map)

{{< note >}}
A single self-signed key can be used. However, we consider this a less secure option that should not be used
outside of a testing environment.

{{< /note >}}

## Configuration

In general CENM components are configured with SSL via the inclusion of an `ssl` configuration block
#. The SSL settings themselves, locations of keystores and passwords
#. The enabling of individual communication channels to use SSL.


{{< warning >}}
If you enable SSL server side, for example on the Identity Manager, then any client that will talk to that
service must configure SSL for that communication stream.

{{< /warning >}}


SSL enablement *could* be mixed within a single CENM deployment, with only a select set of channels encrypted,
but it will almost certainly be easier to roll it out as a whole.

{{< note >}}
By client, we are referring to elements of the CENM suite talking to another that is listening for such
messaging. This does not refer to, and has no impact on, the interaction of the CENM tools and Corda nodes
acting as clients of the network.

{{< /note >}}

### SSL Certificate Configuring

All components should be configured to use SSL with the following configuration block. More details can be found in
[Identity Manager Configuration Parameters](config-identity-manager-parameters.md) and [Network Map Configuration Parameters](config-network-map-parameters.md)

```docker
ssl = {
    keyStore = {
        location = /path/to/keystore.jks
        password = <key store password>
        keyPassword = <key password>
    }
    trustStore = {
        location = /path/to/trustroot.jks
        password = <key store password>
    }
}
```

The `keyStore` contains the public and private keypair of the service signed by the root key


{{< important >}}
The root key should not be in this keystore, only the keypair and the associated certificate associated
with this CENM service.


{{< /important >}}

The `trustStore` contains the root key’s certificate. This is, in effect, common across the entire CENM deployment
as it is this that enables the various components to trust one another checking that the certificate presented
chains back to this root certificate.

However, if the key and keystore passwords are the same, then the `keyPassword` option can be omitted

```docker
ssl = {
    keyStore = {
        location = /path/to/keystore.jks
        password = <key store and key password>
    }
    trustStore = {
        location = /path/to/trustroot.jks
        password = <key store password>
    }
}
```

Finally, if the keystore contains the trustroot, then the trustStore can in turn be omitted.

```docker
ssl = {
    keyStore = {
        location = /path/to/keystore.jks
        password = <key store and key password>
    }
}
```


### Server Side Enablement

Those services that open ports for other CENM components to talk to can enable SSL by including the above settings within
their `enmListener` configuration block:

```docker
enmListener {
    port = 5050
    ssl = {
        <<< As configured above >>>
    }
}
```

This will include the `Network Map` as well as both the `Issuance` and `Revocation` workflows inside the Identity
Manager. Leaving these configuration blocks out of the respective configuration files will mean that each CENM listening server
will be created without SSL and default to the following ports:


* **Network Map** - 5050
* **Issuance (Identity Manager)** - 5051
* **Revocation (Identity Manager)** - 5052


### Client Side Enablement

Those CENM services which need to talk to other services as a client are configured similarly to the above, on a
per-service basis. For example, the Network Map is configured to talk to the Identity Manager Service:

```docker
networkMap = {
    ...
    identityManager = {
        host       = localhost
        port       = 5050
        ssl = {
            <<< As configured above >>>
        }
    }
    ...
}
```

When SSL is enabled on the Identity Manager it must be set here. This will cause any connections made to the Identity
Manager to use the SSL credentials configured. Without these credentials, the Network Map side will attempt to
initialise an unencrypted connection, whilst the Identity Manager will be expecting an initial SSL handshake to occur,
resulting in an unsuccessful connection.


### Sharing SSL Settings

For some services, such as the Network Map, it is possible multiple SSL configuration blocks within the configuration
file. It is considered to be most secure if each of these connections use a unique set of SSL keys, however in some
situations it may be desirable to use the same SSL keys and certificates across multiple connections. To avoid
repetition within the configuration files and improve readability the SSL configuration block can be extracted out to a
separate file and then dynamically included within the configuration file. For example, the SSL settings below can be extracted
to the file `ssl-settings.conf`:

```docker
ssl = {
    keyStore = {
        location = /path/to/keystore.jks
        password = <key store and key password>
    }
    trustStore = {
        location = /path/to/trustroot.jks
        password = <key store password>
    }
}
```

and then included in the Network Map Service configuration file as below:

```docker
...
enmListener {
    port = 20001
    ssl = include "ssl-settings.conf"
}
...
identityManager = {
    host       = localhost
    port       = 5051
    ssl = include "ssl-settings.conf"
}
revocation = {
    host       = localhost
    port       = 5052
    ssl = include "ssl-settings.conf"
}
```


## An Example

The following configuration files configure a small test deployment of the CENM suite of tools on a single machine.
This is why all of the services are binding to localhost and can refer to a central location for the PKI and
SSL certificates as well as the `.jar` files.


### Identity Manager and Revocation Service

```docker
address = "localhost:10000"

database {
    driverClassName = org.h2.Driver
    url = "jdbc:h2:file:./identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "example-db-password"
}

workflows {
    "issuance" = {
        type = ISSUANCE
        updateInterval = 1000
        enmListener {
            port = 5051
            reconnect = true
            ssl {
                keyStore {
                    location = exampleSslKeyStore.jks
                    password = "password"
                }
                trustStore {
                    location = exampleSslTrustStore.jks
                    password = "trustpass"
                }
            }
        }
        plugin {
            pluginClass = "com.r3.enmplugins.jira.JiraCsrWorkflowPlugin"
            config {
                address = "https://doorman-jira-host.r3.com/"
                projectCode = "CSR"
                username = "example-jira-username"
                password = "example-jira-password"
            }
        }
    },
    "revocation" = {
        type = REVOCATION
        enmListener {
            port = 5052
            reconnect = true
            # note that this SSL configuration could use different keys to the above if desired
            ssl {
                keyStore {
                    location = exampleSslKeyStore.jks
                    password = "password"
                }
                trustStore {
                    location = exampleSslTrustStore.jks
                    password = "trustpass"
                }
            }
        }
        plugin {
            pluginClass = "com.r3.enmplugins.jira.JiraCrrWorkflowPlugin"
            config {
                address = "https://doorman-jira-host.r3.com/"
                projectCode = "CRR"
                username = "example-jira-username"
                password = "example-jira-password"
            }
        }
        crlCacheTimeout = 2000
        crlFiles = ["./crl/root.crl", "./crl/subordinate.crl", "./crl-files/tls.crl"]
    }
}

shell {
    sshdPort = 10002
    user = "testuser"
    password = "example-password"
}

```

### Network Map Service

```docker
address = "localhost:20000"

database {
    driverClassName = org.h2.Driver
    url = "jdbc:h2:file:./network-map-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "example-db-password"
}

pollingInterval = 60000

enmListener {
    port = 5050
    reconnect = true
    ssl {
        keyStore {
            location = exampleSslKeyStore.jks
            password = "password"
        }
        trustStore {
            location = exampleSslTrustStore.jks
            password = "trustpass"
        }
    }
}

identityManager {
    host = "example-identity-manager-host"
    port = 5051
    reconnect = true
    # note that this SSL configuration could use different keys to the above if desired
    ssl {
        keyStore {
            location = exampleSslKeyStore.jks
            password = "password"
        }
        trustStore {
            location = exampleSslTrustStore.jks
            password = "trustpass"
        }
    }
}

revocation {
    host = "example-identity-manager-host"
    port = 5052
    reconnect = true
    # example revocation communication configuration without SSL
}

checkRevocation = true

shell {
    sshdPort = 20002
    user = "testuser"
    password = "example-password"
}

```

### Signing Service

```docker
shell = {
  sshdPort = 20003
  user = "testuser"
  password = "example-password"
}

#############################
# Proprietary HSM libraries #
#############################
hsmLibraries = [
  {
    type = UTIMACO_HSM
    jars = ["/path/to/CryptoServerJCE.jar"]
  },
  {
    type = GEMALTO_HSM
    jars = ["/path/to/LunaProvider.jar"]
    sharedLibDir = "/path/to/shared-libraries/dir/"
  },
  {
    type = SECUROSYS_HSM
    jars = ["/path/to/primusX.jar"]
  },
  {
    type = AZURE_KEY_VAULT_HSM
    jars = ["/path/to/akvLibraries.jar"]
  },
  {
      type = AMAZON_CLOUD_HSM
      jars = ["/opt/cloudhsm/java/cloudhsm-3.0.0.jar"]
      sharedLibDir = "/opt/cloudhsm/lib"
  }
]

####################################################
# Optional default certificate store for any HSM   #
# signing keys without a certificate store defined #
####################################################
globalCertificateStore = {
  file = "exampleGlobalCertificateStore.jks"
  password = "example-password"
}

#############################################
# All individual keys used in signing tasks #
#############################################
signingKeys = {
    "CSRUtimacoHsmSigningKey" = {
        alias = "example-csr-key-alias"
        type = UTIMACO_HSM
        group = "example-hsm-group"
        specifier = 1
        keyStore {
            host = "192.168.0.1"
            port = "3001"
            users = [{
                mode = CARD_READER
            }]
        }
    },
    "CRLUtimacoHsmSigningKey" = {
        alias = "example-crl-key-alias"
        type = UTIMACO_HSM
        group = "example-hsm-group"
        specifier = 1
        keyStore {
            # Example using a different HSM to above key
            host = "192.168.0.2"
            port = "3002"
            # username and password omitted, user will be prompted during task execution
            users = [{
                mode = PASSWORD
            }]
        },
        # Using a unique, non-global certificateStore
        certificateStore = {
            file = "exampleCertificateStore.jks"
            password = "example-password"
        }
    },
    "NetworkMapUtimacoHsmSigningKey" = {
        alias = "example-map-key-alias"
        type = UTIMACO_HSM
        group = "example-hsm-group"
        specifier = 1
        keyStore {
            host = "192.168.0.1"
            port = "3001"
            users = [{
                mode = KEY_FILE
                keyFilePath = example-key-file
                password = "test-password"
            }]
        }
    },
    "NetworkParametersUtimacoHsmSigningKey" = {
        alias = "example-parameter-key-alias"
        type = UTIMACO_HSM
        group = "example-hsm-group"
        specifier = 1
        keyStore {
            host = "192.168.0.1"
            port = "3001"
            users = [{
                mode = CARD_READER
            }]
        }
    },
    "ExampleGemaltoHsmSigningKey" = {
        alias = "example-parameter-key-alias"
        type = GEMALTO_HSM
        credentials {
            keyStore = "tokenlabel:example-partition-name"
            password = "example-crypto-office-password" # this can be omitted and input at runtime
        }
    },
    "ExampleSecurosysHsmSigningKey" = {
        alias = "example-parameter-key-alias"
        type = SECUROSYS_HSM
        keyStore {
            host = "127.0.0.1"
            port = 1234
        }
        credentials = [{
            username = "example-username" # this can be omitted and input at runtime
            password = "example-password" # this can be omitted and input at runtime
        }]
    },
    "ExampleAzureKeyVaultHsmSigningKey" = {
        alias = "example-parameter-key-alias"
        type = AZURE_KEY_VAULT_HSM
        keyStore {
            keyVaultUrl = "http://example.com"
            protection = SOFTWARE
        }
        credentials {
            keyStorePath = "path/to/keystore"
            keyStorePassword = "example-password"
            keyStoreAlias = "example-alias"
            clientId = "12345-abcde-54321"
        }
    },
    "ExampleAwsCloudHsmSigningKey" = {
        alias = "example-parameter-key-alias"
        type = AMAZON_CLOUD_HSM
        credentialsAmazon {
            partition = "example-partition"
            userName = "example-user"
            password = "example-password"
        }
        localCertificateStore = {
            file = "exampleCertificateStore.jks"
            password = "password"
        }
    }
}

##########################################################
# All CENM service endpoints for fetching/persisting data #
##########################################################
caSmrLocation = {
    host = localhost
    port = 5010
    verbose = true
    # note that this SSL configuration could use different keys to the other locations if desired
    ssl {
        keyStore {
            location = exampleSslKeyStore.jks
            password = "password"
        }
        trustStore {
            location = exampleSslTrustStore.jks
            password = "trustpass"
        }
    }
}

nonCaSmrLocation = {
    host = localhost
    port = 5011
    verbose = true
    # note that this SSL configuration could use different keys to the other locations if desired
    ssl {
        keyStore {
            location = exampleSslKeyStore.jks
            password = "password"
        }
        trustStore {
            location = exampleSslTrustStore.jks
            password = "trustpass"
        }
    }
}

###################################################
# Signing tasks to be run (manually or scheduled) #
###################################################
signers = {
    "Example CSR Signer" = {
        type = CSR
        signingKeyAlias = "CSRUtimacoHsmSigningKey"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        validDays = 7300 # 20 year certificate expiry
    },
    "Example CRL Signer" = {
        type = CRL
        signingKeyAlias = "CRLUtimacoHsmSigningKey"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        updatePeriod = 5184000000 # 60 day CRL expiry
    },
    "Example Network Map Signer" = {
        type = NETWORK_MAP
        signingKeyAlias = "NetworkMapUtimacoHsmSigningKey"
        schedule {
            interval = 1minute
        }
    },
    "Example Network Parameter Signer" = {
        type = NETWORK_PARAMETERS
        signingKeyAlias = "NetworkParametersUtimacoHsmSigningKey"
    }
}

```
