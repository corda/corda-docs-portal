---
aliases:
- /releases/release-1.0/signing-service.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-signing-service
    parent: cenm-1-0-operations
    weight: 150
tags:
- signing
- service
title: Signing Service
---


# Signing Service



## Purpose

The Signing Service is a service that forms part of the Corda Enterprise Network Manager, alongside the Identity
Operator and Network Map. It acts as a bridge between the main CENM services and the HSM infrastructure, enabling a
network operator to verify and sign incoming requests and changes to the network.

As mentioned in the CENM service documentation (doorman and [Network Map Service](network-map.md)), the main CENM services can be
configured with an integrated *local signer* that will automatically sign all unsigned data using a provided key.
While this is convenient, it is intended for use within for testing and toy environments, and should **not** be used in
production environments. Instead, large and important changes to the network should go through a series of checks before
being approved and signed, ideally with a network operator manually verifying and signing new CSRs, CRLs and Network
Parameter changes. The Signing Service provides this behaviour, with HSM integration enabling the signing of any
particular data to require authentication from multiple users.

The verification and signing of data is done via the set of user configured signing tasks within the service, with each
task being configured with:


* **Data type:** CSR, CRL, Network Map or Network Parameters
* **Data source:** the CENM service to retrieve unsigned data and persist signed data *(e.g. a network’s Identity Manager)*
* **Signing key:** the key that should be used to sign the data *(e.g. a particular key within a HSM using keycard authentication)*

Once the service has been configured with this set of signing tasks, an execution of a given signing task will:


* Retrieve unsigned data from the data source
* Signing it using the provided key, requesting manual authentication if required.
* Persist the signed data back to the data source.

Each signing task is configured independently from one another, meaning different keys can (and should) be used to sign
different data types or data from different sources. The independence of each signing task also means that the Signing
Service is not constrained to a given network. For a given signing task, as long as the Signing Service can reach the
configured data source and access the configured signing key (or HSM) then the task can be executed. Therefore one
Signing Service can be used to manage several networks/sub-zones.

Due to security concerns, the signing service should be hosted on private premises, **not** in a cloud environment. As
mentioned above, the only communication requirements are outgoing connections to the CENM services configured as data
sources, and outgoing connections to the HSMs for the configured signing keys. The overall flow of communication can be
seen in the below diagram:

![signing service communication](/en/images/signing-service-communication.png "signing service communication")
{{< note >}}
All inter-service communication can be configured with SSL support to ensure the connection is encrypted. See
[Configuring the ENM services to use SSL](enm-with-ssl.md)

{{< /note >}}
{{< note >}}
This document does not cover HSM setup, rather assumes that the HSM(s) have already been configured - the
users and certificates should have been previously setup on the box.

{{< /note >}}

## Running the Signing Service

Once the Signing Service has been configured, it can be run via the command:

```bash
java -jar signer-<VERSION>.jar --config-file <CONFIG_FILE>
```

On success you should see a message similar to:

```kotlin
2019-01-01T12:34:56,789 [main] INFO - Binding Shell SSHD server on port <SSH PORT>
```

The service can then be accessed via ssh, either locally on the machine or from another machine within the same secure,
closed network that the service is being run on.


### Executing A Signing Task

Once the configured service is up and running, a user can execute a signing task via the interactive shell via the `run
signer name: <SIGNING_TASK_ALIAS>` command. This will execute the task, prompting the user for signing key
authentication, if required, and verification of the changes.

{{< note >}}
Any configured task can be run through the shell, even automated scheduled tasks.

{{< /note >}}

### Viewing Available Signing Tasks

A user can see what signing tasks are available by executing the `view signers` command within the shell. This will
output all tasks that can be run along with their schedule, if applicable.


### Performing A Health Check

To verify that all configured CENM data sources are reachable by the Signing Service, a health check can be performed
by running the `run clientHealthCheck`. This will iteratively run through each service, sending a simple ping message
and verifying a successful response. Any unsuccessful connection attempts will be displayed to the console. This method
is especially useful after the initial setup to verify that the Signing and CENM services have been configured
correctly.


## Configuration

The configuration for the service consists of the following sections:


* The [global configuration options](#global-configuration-options) (interactive shell and optional default certificate store)
* The [signing keys](#signing-keys) that are used across all signing tasks
* The [data sources (CENM service locations)](#data-sources-cenm-service-locations) that are used across all signing tasks
* The [signing tasks](#signing-tasks) that can be run through the service


### Global Configuration Options


#### Shell Configuration

The Signing Service is interacted with via the shell, which is configured at the top level of the config file. This
shell is similar to the interactive shell available in other ENM services and is configured in a similar way. See
[Shell Configuration](shell.md#shell-config) for more information on how to configure the shell.


#### Global Certificate Store

Signing keys that use a HSM require a certificate store to be defined also, containing all certificates to build the
entire certificate chain from the signing key back to the root. If a global certificate store is used containing all
required certificates for different signing keys then repetition in the configuration can occur - hence a top level
global certificate store can be configured that will be used by any signing key that does not have its own certificate
store configured.

```guess
...
globalCertificateStore = {
    file = "path/to/certificate/store.jks"
    password = "example-password"
}
...
```


### Signing Keys

The signing keys that are used across all signing task need to be configured. As, potentially, one signing key could be
reused across several signing tasks these are configured in the form of a map of human-readable aliases (referenced by
the signing task configuration) to signing keys. A signing key can come from either a local key store or a HSM.

Each signing key can be optionally configured to include its authentication details. This allows a signing task to be
configured with this signing key such that it can be executed by any user with access to the shell, or alternatively
scheduled to run automatically (see below for more information). Due to the decreased security with this approach, it is
not recommended to include authentication credentials within a production environment configuration.


### Data Sources (CENM Service Locations)

For each signing task, the data source for getting the unsigned data and persisting the signed data needs to be defined.
Similarly to the signing keys above, one data source could potentially be used across multiple signing tasks, hence they
are configured as a map of human-readable aliases (referenced by the signing task configuration) to ENM service
locations.

{{< note >}}
Communication with the configured service locations can be configured to use SSL for a secure, encrypted
connection. This is strongly recommended for production deployments. See [Configuring the ENM services to use SSL](enm-with-ssl.md) for more
information.

{{< /note >}}

### Signing Tasks

This configuration section defines each signing task that can be run via the service. Each task is defined by adding an
entry to the `signers` configuration map, keyed by the human-readable alias for the task (used when interacting with
the service via shell). The value for the entry consists of the configuration options specific to that task such as the
signing key and data source that is uses (using the previously defined aliases in the `signingKeys` and
`serviceLocations` configuration parameters), data type specific options such as the CSR validity period as well as
schedule if applicable.

Each signing task maps to exactly one of four possibly data types:


* **CSR data** - signing approved but unsigned Certificate Signing Requests
* **CRL data** - building and signing new Certificate Revocation Lists using newly approved Certificate Revocation Requests
* **Network Map** - building and signing a new Network Map
* **Network Parameters** - signing new Network Parameters and Network Parameter Updates


#### Scheduling Signing Tasks

A signing task can be configured to automatically run on a set schedule, providing *no manual user input is required*.
That is, the signing key that is configured for the task requires no user input to authenticate (e.g. keyfile or
username/password provided in configuration file). This behaviour can be useful for testing and toy environments, as
well as automating the signing of lower risk changes such as Network Map changes.


{{< warning >}}
Automated, scheduled signing of important changes such as Network Parameter updates, CSRs and CRLs should
not be configured in production environments.

{{< /warning >}}


An appropriate signing task can be scheduled via the `schedule` config block within the signing task configuration:

```guess
...
"Example Signing Task" = {
    ...
    schedule {
        interval = 1hour
    }
}
...
```

The `interval` parameter can either take a number, interpreted as the number of milliseconds between each
execution, or a string consisting of a number followed by the units suffix as above. The possible unit suffixes are:


* ns, nano, nanos, nanosecond, nanoseconds
* us, micro, micros, microsecond, microseconds
* ms, milli, millis, millisecond, milliseconds
* s, second, seconds
* m, minute, minutes
* h, hour, hours
* d, day, days

{{< note >}}
Attempting to configure a non-schedulable signing task (e.g. signing via HSM requiring manual user
authentication) will result in an error upon service startup.

{{< /note >}}

### Detailed Example Signing Task Execution

Listed below are the steps involved in signing an example Network Parameter update. The steps involved in signing other
data types are very similar.


* A network operator issues a Network Parameter update via the appropriate Network Map service. At this point, as the
update is unsigned, it will not be broadcast to the network.

The parameter update is ready to be signed.


* A privileged user accesses the Signing Service via ssh and runs the pre-configured Network Parameter signing task for
the given Network Map service.
* A connection to the Network Map service is established and the unsigned Network Parameter update is fetched and
displayed to the user.
* The user confirms that the changes are correct and should be signed.
* A connection to the appropriate HSM is created, and the user is prompted for their authentication credentials. The
exact format of this authentication will depend on the configured signing key that the signing task uses.
* Once the user has been successfully authenticated and their privileges are strong enough, then the signing process
commences using the configured signing key. If their privileges are not sufficient then the signing task will prompt
for another user to be authenticated, repeating this process until the configured HSM authentication threshold has
been exceeded.
* The Network Parameter update is signed then persisted back to the appropriate Network Map service. When the Network
Map is next updated and signed, the newly signed parameter update will be included and therefore broadcast to the
network participants.

The steps involved in signing other data types are very similar to above, mainly differing in the unsigned information
that is retrieved from the corresponding CENM service:

**Network Map:**
The latest unsigned network map is fetched from the appropriate Network Map service. This will include all network
participants (new and current) that have a valid, non-revoked certificate signed by the network’s Identity Manager, as
well as the signed Network Parameters (active and pending update if applicable). If the Network Map has not changed
since it was last signed then the signing process will finish.

**Certificate Signing Request (CSR)**:
All approved but unsigned CSRs are fetched from the appropriate Identity Manager and displayed to the user. They can
then select all or a subset of these to sign.

**Certificate Revocation List (CRL)**:
All approved but unsigned Certificate Revocation Requests (CRRs) are fetched from the appropriate Identity Manager and
displayed to the user. They can then select all or a subset of these to sign, which are then included in the latest
signed CRL.

{{< note >}}
The signing of the Network Map is completely separate from the signing of the Network Parameters. A parameter
update will only be included in a network map if the update has been previously signed.

{{< /note >}}

## Configuration Parameters

The configuration file for the Signing Service should include the following parameters (optional arguments are marked as
such where appropriate):


* **shell**:
The configuration for the services integrated shell.


* **globalCertificateStore**:
*(Optional)* Certificate store that will be used for any signers that don’t have their own certificate store
defined. Should contain all certificates to build the entire certificate chain from the signing key back to the root.


* **file**:
Certificate store file location.


* **password**:
Certificate store password.




* **signingKeys**:
Map of human-readable aliases (string) to signing key configurations. Should contain all signing keys that
are used within the signing processes defined in the signers map. See the [signing key map entry example](#signing-key-map-entry-example)
below for the expected format.


* **serviceLocations**:
Map of human-readable aliases (string) to ENM service location configurations. Should contain all
services that are used within the signing processes defined in the signers map. See the
[service location map entry example](#service-location-map-entry-example) below for the expected format.


* **signers**:
Map of human-readable aliases (string) to signing task configuration. Defines the tasks that can be run by a
user via the interactive shell. Each signing task should refer to exactly one signing key and one service
location using the alias defined in the above maps. See the [signers map entry example](#signers-map-entry-example) below for the
expected format.




### Signing Key Map Entry Example

Each entry in the `signingKeys` map should be keyed on the user-defined, human-readable alias. This can be any string
and is used only within the config to map the signing keys to each signing task that use it.

A signing key can come from two sources - a local key store or a HSM.

**Local Signing Key Example:**


* **alias**:
Alias of the signing key within the key store


* **keyStore**:
File path of the local key store


* **password**:
Password to access the key store



If the signing key is within a HSM then the user authentication needs to be defined. This also determines whether a
signing task can be automatically scheduled.

**HSM Signing Key Example**:


* **alias**:
Alias of the signing key within the HSM


* **keyStore**:
Configuration of the HSM key store.


* **host**:
Host name (or IP address) of the HSM device.


* **port**:
Port number of the HSM device.


* **users**:
List of user authentication configurations. Each entry in the list should have the following format:


* **username**:
HSM username.


* **mode**:
One of the 3 possible authentication modes:
`PASSWORD` - User’s password as set-up in the HSM.
`CARD_READER` - Smart card reader authentication.
`KEY_FILE` - Key file based authentication.


* **password**:
Only relevant if mode is `PASSWORD` or `KEY_FILE`. Specifies either the password credential
for the associated user or the password to the key file, depending on the selected mode.


* **keyFilePath**:
Only relevant if mode is `KEY_FILE`. Key file path.


* **device**:
Only relevant if mode is `CARD_READER`. Specifies the connection string to the card reader device.
Default value: “:cs2:auto:USB0”.






* **group**:
Key group (string) of the signing key. This is the Utimaco HSM name spacing concept. See Utimaco docs for more
details.


* **specifier**:
Key specifier (string) of the signing key. This is the legacy Utimaco HSM name spacing concept. See Utimaco
docs for more details.


* **authThreshold**:
Authentication threshold required to access the signing key within the HSM. This value corresponds to
the summation of permission values of all logged-in users. Setting this provides a way to ensure use of
the signing key (and therefore execution of the signing task) can only be achieved once X out of Y
privileged HSM users authenticated. Defaults to 1.


* **certificateStore**:
*(Optional if using globalCertificateStore)* Certificate store containing all certificates required to build the
entire certificate chain from the signing key back to the root. This is required as the signing keys within the HSM
do not contain their full certificate chains.


* **file**:
Certificate store file location.


* **password**:
Certificate store password.






### Service Location Map Entry Example

Each entry in the `serviceLocations` map should be keyed on the user-defined, human-readable alias. This can be any
string and is used only within the config to map the service locations to each signing task that use it.


* **enmService**:
The connection details for the CENM service that acts as the data source


* **host**:
Host name (or IP address) that the CENM service is running on


* **port**:
Port that the CENM service is listening on (for inter-ENM communication)


* **verbose**:
Boolean representing whether debug information for the IPC between the Signer and the remote service
should be displayed.


* **ssl**:
*(Optional)* SSL Information for connection with the CENM service.


* **keyStore**:
Key store configuration for the Signing Service SSL key pair.


* **location**:
Location on the file system of the keystore containing the SSL public / private keypair
of the Signing Service.


* **password**:
password for the keyStore


* **keyPassword**:
*(Optional)* Password for the keypair, can be omitted if the same as the keystore.




* **trustStore**:
Trust store configuration for the SSL PKI root of trust.


* **location**:
Location on the file system of the keystore containing the SSL PKI root of trust.


* **password**:
password for the trust root keystore.










### Signers Map Entry Example

Each entry in the `signers` map should be keyed on the user-defined, human-readable alias. This can be any
string and is used by the user when viewing and invoking the signing task from within the interactive shell.

Each signing task should use exactly one signing key and service location, and be configured for exactly one data type.


* **type**:
The data type for the signing task. Should be one of `CSR`, `CRL`, `NETWORK_MAP` or `NETWORK_PARAMETERS`.


* **signingKeyAlias**:
The alias for the signing key used by the signing task. Should refer to one of the aliases in the
`signingKeys` map defined above.


* **serviceLocationAlias**:
The alias for the service location used by the signing task. Should refer to one of the aliases
in the `serviceLocations` map defined above.


* **crlDistributionPoint**:
Relevant only if type is `CRL` or `CSR` (optional for `CSR`). The endpoint that the CRL is
hosted on.


* **updatePeriod**:
Relevant only if type is `CRL`. The millisecond duration between CRL updates.


* **validDays**:
Relevant only if type is `CSR`. The number of days that a certificate is valid for, counted from the time
of signing.


* **schedule**:
*(Optional)* The scheduled for automated execution of the signing task. Note that this can only be set on tasks that
are linked to signing keys that require no manual user authentication. That is, either a local key store or HSM
signing key using `PASSWORD` or `KEY_FILE` authentication with the password preconfigured.


* **interval**:
The duration interval between signing executions. Either a number representing the millisecond duration
or a string duration with unit suffix. See above [scheduling signing tasks](#scheduling-signing-tasks) section on accepted format.






## Example Configuration

Below are two example configuration files, one using signing keys from local key stores and the other using signing keys
from a HSM. If desired, any combination of local/HSM signing keys can be included within the configuration file.


### Signing Keys From Local Key Store

```kotlin
shell = {
  sshdPort = 20003
  user = "testuser"
  password = "example-password"
}

#############################################
# All individual keys used in signing tasks #
#############################################
signingKeys = {
    "IdentityManagerLocal" = {
        alias = "example-key-alias-2"
        password = "example-key-password-2"
        keyStore {
            file = "exampleKeyStore.jks"
            password = "example-password"
        }
    },
    "NetworkMapLocal" = {
        alias = "example-key-alias"
        password = "example-key-password"
        keyStore {
            file = "exampleKeyStore.jks"
            password = "example-password"
        }
    }
}

##########################################################
# All ENM service endpoints for fetching/persisting data #
##########################################################
serviceLocations = {
    "identity-manager" = {
        host = localhost
        port = 5050
        verbose = true
    },
    "network-map" = {
        host = localhost
        port = 5053
        verbose = true
    },
    "revocation" = {
        host = localhost
        port = 5051
        verbose = true
    }
}

###################################################
# Signing tasks to be run (manually or scheduled) #
###################################################
signers = {
    "Example CSR Signer" = {
        type = CSR
        signingKeyAlias = "IdentityManagerLocal"
        serviceLocationAlias = "identity-manager"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        validDays = 365
        schedule {
            interval = 1minute
        }
    },
    "Example CRL Signer" = {
        type = CRL
        signingKeyAlias = "IdentityManagerLocal"
        serviceLocationAlias = "revocation"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        updatePeriod = 3600
        schedule {
            interval = 60minute
        }
    },
    "Example Network Map Signer" = {
        type = NETWORK_MAP
        signingKeyAlias = "NetworkMapLocal"
        serviceLocationAlias = "network-map"
        schedule {
            interval = 1minute
        }
    },
    "Example Network Parameters Signer" = {
        type = NETWORK_PARAMETERS
        signingKeyAlias = "NetworkMapLocal"
        serviceLocationAlias = "network-map"
        schedule {
            interval = 10minute
        }
    }
}

```

### Signing Keys From HSM

```kotlin
shell = {
  sshdPort = 20003
  user = "testuser"
  password = "example-password"
}

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
    "CSRHsmSigningKey" = {
        alias = "example-csr-key-alias"
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
    "CRLHsmSigningKey" = {
        alias = "example-crl-key-alias"
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
    "NetworkMapHsmSigningKey" = {
        alias = "example-map-key-alias"
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
    "NetworkParametersHsmSigningKey" = {
        alias = "example-parameter-key-alias"
        group = "example-hsm-group"
        specifier = 1
        keyStore {
            host = "192.168.0.1"
            port = "3001"
            users = [{
                mode = CARD_READER
            }]
        }
    }
}

##########################################################
# All ENM service endpoints for fetching/persisting data #
##########################################################
serviceLocations = {
    "identity-manager" = {
        host = localhost
        port = 5050
        verbose = true
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
    },
    "network-map" = {
        host = localhost
        port = 5053
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
    },
    "revocation" = {
        host = localhost
        port = 5051
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
}

###################################################
# Signing tasks to be run (manually or scheduled) #
###################################################
signers = {
    "Example CSR Signer" = {
        type = CSR
        signingKeyAlias = "CSRHsmSigningKey"
        serviceLocationAlias = "identity-manager"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        validDays = 1
    },
    "Example CRL Signer" = {
        type = CRL
        signingKeyAlias = "CRLHsmSigningKey"
        serviceLocationAlias = "revocation"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        updatePeriod = 1000
    },
    "Example Network Map Signer" = {
        type = NETWORK_MAP
        signingKeyAlias = "NetworkMapHsmSigningKey"
        serviceLocationAlias = "network-map"
        schedule {
            interval = 1minute
        }
    },
    "Example Network Parameter Signer" = {
        type = NETWORK_PARAMETERS
        signingKeyAlias = "NetworkParametersHsmSigningKey"
        serviceLocationAlias = "network-map"
    }
}

```
