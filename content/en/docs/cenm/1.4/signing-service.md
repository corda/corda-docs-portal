---
aliases:
- /signing-service.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-signing-service
    parent: cenm-1-4-operations
    weight: 150
tags:
- signing
- service
title: Signing Service
---

# Signing Service

## Purpose

The Signing Service acts as a bridge between the main CENM services and the PKI/HSM infrastructure, enabling a network operator to verify and sign incoming requests and changes to the network.

The Signing Service forms a part of the main Corda Enterprise Network Manager (CENM) services, alongside the [Identity Manager Service](identity-manager.md) and the [Network Map Service](network-map.md) (and complemented by the [Auth Service](auth-service), the [Zone Service](zone-service.md), the [Angel Service](angel-service.md), and the [Gateway Service](gateway-service.md)).

As mentioned in other CENM service documentation ([Identity Manager Service](identity-manager.md) and [Network Map Service](network-map.md)), the main CENM services
can be configured with an integrated *local signer* that will automatically sign all unsigned data using a provided key.
While this is convenient, it is intended for use for development and testing environments, and **should not** be used in
production environments. Instead, large and important changes to the network should go through a series of checks before
being approved and signed, ideally with a network operator manually verifying and signing new CSRs, CRLs, and Network
Parameter changes. The Signing Service provides this behaviour, with HSM integration enabling the signing of any
particular data to require authentication from multiple users.

## Signing Service overview

The Signing Service supports the following HSMs (see [CENM support matrix](cenm-support-matrix.md#hardware-security-modules-hsms) for more information):

* Utimaco SecurityServer Se Gen2.
* Gemalto Luna.
* Securosys PrimusX.
* Azure Key Vault.
* AWS CloudHSM.

The verification and signing of data is done via the set of user configured signing tasks within the service, with each
task being configured with:

* **Data type:** CSR, CRL, Network Map, or Network Parameters.
* **Data source:** the CENM service to retrieve unsigned data and persist signed data - for example, a network’s Identity Manager Service.
* **Signing key:** the key that should be used to sign the data - for example, a particular key within a HSM using keycard authentication.

Once the service has been configured with this set of signing tasks, an execution of a given signing task will:

* Retrieve unsigned data from the data source.
* Sign it using the provided key, requesting manual authentication if required.
* Persist the signed data back to the data source.

Each signing task is configured independently from one another, meaning that different keys can (and should) be used to sign
different data types or data from different sources. The independence of each signing task also means that the Signing
Service is not constrained to a given network. For a given signing task, the task can be executed as long as the Signing Service can reach the
configured data source and access the configured signing key (or HSM). Therefore one Signing Service can be used to manage several networks/sub-zones.

Due to security concerns, the Signing Service should be hosted on private premises and **not** in a cloud environment.
As mentioned above, the only communication requirements are outgoing connections to the CENM services as data sources, and outgoing connections to the HSMs
for the configured signing keys. The overall flow of communication can be seen in the following diagram:

![signing service communication](/en/images/signing-service-communication.png "signing service communication")

{{< note >}}
All inter-service communication can be configured with SSL support to ensure the connection is encrypted. See
[Configuring the CENM services to use SSL](enm-with-ssl.md) for more information.
{{< /note >}}

{{< note >}}
This document does not cover HSM setup. It is based on the assumption that the HSM(s) have already been configured - the
users and certificates should have previously been set up on the box.
{{< /note >}}

### Running the Signing Service

Once the Signing Service has been configured, you can run it using the following command:

```bash
java -jar signer-<VERSION>.jar --config-file <CONFIG_FILE>
```

You can use the following optional parameter to specify the working directory:

```bash
--working-dir=<DIR>
```

If a specific working directory is set in this way, the Signing Service will look for files in that directory, meaning that all certificates and configuration files should be located in that directory.
If not specified, the Signing Service use the current working directory - this is the directory from which the service has been started.

On success you should see a message similar to:

```kotlin
2019-01-01T12:34:56,789 [main] INFO - Binding Shell SSHD server on port <SSH PORT>
```
The service can then be accessed via SSH, either locally on the machine or from another machine within the same secure,
closed network that the service is being run on.

### Executing a signing task

Once the configured service is up and running, a user can execute a signing task via the interactive shell via the `run
signer name: <SIGNING_TASK_ALIAS>` command. This will execute the task, prompting the user for signing key
authentication, if required, and verification of the changes.

{{< note >}}
Any configured task can be run through the shell, even automated scheduled tasks.

{{< /note >}}

### Viewing available signing tasks

A user can see what signing tasks are available by executing the `view signers` command within the shell. This will
output all tasks that can be run along with their schedule, if applicable.


### Performing a health check

To verify that all configured CENM data sources are reachable by the Signing Service, a health check can be performed
by running the `run clientHealthCheck`. This will iteratively run through each service, sending a simple ping message
and verifying a successful response. Any unsuccessful connection attempts will be displayed to the console. This method
is especially useful after the initial setup to verify that the Signing and CENM services have been configured
correctly.


## Signing Service configuration

The configuration for the Signing Service consists of the following sections:


* The [global configuration options](#global-configuration-options) (interactive shell and optional default certificate store)
* The [signing keys](#signing-keys) that are used across all signing tasks
* The [signing tasks](#signing-tasks) that can be run through the service


### Global configuration options


#### Shell configuration

The Signing Service is interacted with via the shell, which is configured at the top level of the configuration file. This
shell is similar to the interactive shell available in other CENM services and is configured in a similar way. See
[Shell Configuration](shell.md#shell-config) for more information on how to configure the shell.


#### HSM libraries

If using the Signing Service with a HSM then, due to the proprietary nature of the HSM libraries, the appropriate Jars
need to be provided separately and referenced within the configuration file. The libraries that are required will depend
on the HSM that is being used.

An example configuration block for a Signing Service integrating with a Utimaco HSM is:

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

See the [Example Signing Service Configuration](#example-signing-service-configuration) section below for examples of these configuration blocks being used in a complete file.


##### Azure Key Vault

To keep inline with the other HSMs, the Azure Key Vault client `.jar` needs to provided as above. Unlike the other HSMs,
there are many dependent libraries. The top-level dependencies are `azure-keyvault` and `adal4j`, however these both
have transitive dependencies that need to be included. That is, either all jars need to be provided separately (via a
comma-separated list) or an uber `.jar` needs to be provided.

The gradle script below will build an uber jar. First copy the following text in to a new file called build.gradle
anywhere on your file system. Please do not change any of your existing build.gradle files.

```docker
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

```bash
gradle shadowJar
```

or if gradle is not on the path but gradlew is in the current directory then run the following command.

```bash
./gradlew shadowJar
```

This will create a `.jar` called `azure-keyvault-with-deps.jar` which can be referenced in the configuration.


#### Global Certificate Store

Signing keys that use a HSM require a certificate store to be defined also, containing all certificates to build the
entire certificate chain from the signing key back to the root. If a global certificate store is used containing all
required certificates for different signing keys then repetition in the configuration can occur - hence a top level
global certificate store can be configured that will be used by any signing key that does not have its own certificate
store configured. Please note that the `globalCertificateStore` property will not be used in case of an AWS HSM.

```guess
...
globalCertificateStore = {
    file = "path/to/certificate/store.jks"
    password = "example-password"
}
...
```


### Signing keys

The signing keys that are used across all signing task need to be configured. As, potentially, one signing key could be
reused across several signing tasks these are configured in the form of a map of human-readable aliases (referenced by
the signing task configuration) to signing keys.

A signing key can reside in either a local java key store or a HSM. For HSM signing keys, authentication must be
performed against the HSM before the keys can be accessed. The credentials for this can optionally be included in the
configuration, allowing for any signing tasks using that key to be executed automatically on a schedule. Due to the
decreased security with this approach, it is not recommended to include all authentication credentials within a
production environment configuration.

{{< note >}}
Using a local java keystore in a production system is strongly discouraged.

{{< /note >}}
More detailed descriptions of how to configure a signing key can be found in the
`Configuration Parameters` section below.


### Data sources

You must configure a service location for each signing task. The tasks retrieve
unsigned material from these defined locations, and then push the signed material back to the
same location once signed.

Service locations directly connect to the service, which manages the material
(CSRs, Network Map).

#### Signing Tasks

This configuration section defines each signing task that can be run via the service. Each task is defined by adding an
entry to the `signers` configuration map, keyed by the human-readable alias for the task (used when interacting with
the service via shell). The value for the entry consists of the configuration options specific to that task such as the
signing key and data source that is uses (using the previously defined aliases in the `signingKeys` and
`serviceLocation` configuration parameters and an optional `plugin` parameter if the task requires a plug-in for signing),
data type specific options such as the CSR validity period as well as schedule if applicable.

Each signing task maps to exactly one of four possibly data types:


* **CSR data** - signing approved but unsigned Certificate Signing Requests.
* **CRL data** - building and signing new Certificate Revocation Lists using newly approved Certificate Revocation Requests.
* **Network Map** - building and signing a new Network Map.
* **Network Parameters** - signing new Network Parameters and Network Parameter Updates.

#### Using a Signing plugin

Each entry in the `signers` map can use a plug-in for signing. If the `plugin` configuration property is defined
the material will be retrieved from the matching service (Identity Manager or Network Map) and it will be sent
to the plug-in for signing.

The rest depends on the plug-in's architecture. The only contract between the Signing Service and its plug-ins
that the returned signing data must be a pre-defined type. For more information about these types, see the
[Developing Signing Plugins](#developing-signing-plugins) section.

#### Scheduling Signing tasks

A signing task can be configured to automatically run on a set schedule, providing *no manual user input is required*.
That is, the signing key that is configured for the task requires no user input to authenticate (e.g. keyfile or
username/password provided in configuration file). This behaviour can be useful for testing and toy environments, as
well as automating the signing of lower risk changes such as Network Map changes.


{{< warning >}}
Automated, scheduled signing of important changes such as Network Parameter updates, CSRs, and CRLs should
not be configured in production environments.

{{< /warning >}}


{{< note >}}
Even though scheduled signing of CRLs should not be configured in production environment, they should be signed
manually from time to time depending on its’ `nextUpdate` property. This is to ensure an up-to-date CRL is
distributed in the network before the previous one expires. Conventionally they have a lifecycle of 6 months
and are manually signed every 3 months. See [CRL Endpoint Check Tool](crl-endpoint-check-tool.md) for more information how to check
CRLs’ update deadlines.

{{< /note >}}
An appropriate signing task can be scheduled via the `schedule` configuration block within the signing task configuration:

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
authentication) will result in an error upon service start-up.

{{< /note >}}

### Detailed Example Signing Task Execution

Listed below are the steps involved in signing an example Network Parameter update. The steps involved in signing other
data types are very similar.


* A network operator issues a Network Parameter update via the appropriate Network Map Service. At this point, as the
update is unsigned, it will not be broadcast to the network.

The parameter update is ready to be signed.


* A privileged user accesses the Signing Service via ssh and runs the pre-configured Network Parameter signing task for
the given Network Map Service.
* A connection to the Network Map or Signable Material Retriever service is established and the unsigned Network Parameter update is
fetched and displayed to the user.
* The user confirms that the changes are correct and should be signed.
* A connection to the appropriate HSM is created, and the user is prompted for their authentication credentials. The
exact format of this authentication will depend on the configured signing key that the signing task uses.
* Once the user has been successfully authenticated and their privileges are strong enough, then the signing process
commences using the configured signing key. If their privileges are not sufficient then the signing task will prompt
for another user to be authenticated, repeating this process until the configured HSM authentication threshold has
been exceeded.
* The Network Parameter update is signed then persisted back to the appropriate Network Map Service or Signable Material Retriever service. When the Network
Map is next updated and signed, the newly signed parameter update will be included and therefore broadcast to the
network participants.

The steps involved in signing other data types are very similar to above, mainly differing in the unsigned information
that is retrieved from the corresponding CENM service:

**Network Map:**
The latest unsigned network map is fetched from the appropriate Network Map or Signable Material Retriever service. This will include all network
participants (new and current) that have a valid, non-revoked certificate signed by the network’s Identity Manager, as
well as the signed Network Parameters (active and pending update if applicable). If the Network Map has not changed
since it was last signed then the signing process will finish.

**Certificate Signing Request (CSR)**:
All approved but unsigned CSRs are fetched from the appropriate Identity Manager or Signable Material Retriever and displayed to the user. They can
then select all or a subset of these to sign.

**Certificate Revocation List (CRL)**:
All approved but unsigned Certificate Revocation Requests (CRRs) are fetched from the appropriate Identity Manager or Signable Material Retriever and
displayed to the user. They can then select all or a subset of these to sign, which are then included in the latest
signed CRL.

{{< note >}}
The signing of the Network Map is completely separate from the signing of the Network Parameters. A parameter
update will only be included in a network map if the update has been previously signed.

{{< /note >}}

## Signing Service Configuration Parameters

The configuration file for the Signing Service should include the following parameters (optional arguments are marked as
such where appropriate):


* **shell**:
The configuration for the services integrated shell.


* **hsmLibraries**:
List of configurations for any third party HSM libraries.


  * **type**:
  The HSM type for the library (`UTIMACO_HSM`, `GEMALTO_HSM`, `SECUROSYS_HSM`, `AZURE_KEY_VAULT_HSM` or `AMAZON_CLOUD_HSM`).


  * **jars**:
  List of paths for the HSM `.jar` files.


* **sharedLibDir**:
Optional path to the shared library directory.




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
below for the expected format. Please note that if a plugin is used for all the signing tasks in the config then this property must not be present since
it will not be used at all.



  * **timeout**
  An optional parameter that enables you to set a Signing Service timeout for communication to each of the services used within the signing processes defined in the signers map, in a way that allows high node count network maps to get signed and to operate at reliable performance levels.
  The `timeout` value is set in milliseconds and the default value is 10000 milliseconds.
  The example below shows a `serviceLocation` configuration block for the Network Map Service using the `timeout` parameter:

  ```yaml
  serviceLocation = [
      {
               host = http://example.com
               port = 10000
               ssl = {
                   keyStore = {
                       location = "./corda-ssl-signer-keys.jks"
                       password = password
                   }
                   trustStore = {
                       location = "./corda-ssl-trust-store.jks"
                       password = trust-store-password
                   }
                   validate = true
               }
               timeout = 10000
           }
  ]
  ```


* **signers**:
Map of human-readable aliases (string) to signing task configuration. Defines the tasks that can be run by a
user via the interactive shell. Each signing task should refer to exactly one signing key and one service
location using the alias defined in the above maps. See the [signers map entry example](#signers-map-entry-example) below for the
expected format.




### Signing Key Map Entry Example

Each entry in the `signingKeys` map should be keyed on the user-defined, human-readable alias. This can be any string
and is used only within the configuration to map the signing keys to each signing task that use it.

A signing key can come from two sources - a local Java key store or a HSM.


#### Local Signing Key Example


* **alias**:
Alias of the signing key within the key store


* **type**:
The signing key type - `LOCAL` in this case


* **keyStore**:
File path of the local key store


* **password**:
Password to access the key store




#### Utimaco HSM Signing Key Example

If the signing key is within a Utimaco HSM then the HSM connection details needs to be included in the configuration as
well as a list of authentication credentials. The setup of the HSM determines the authentication thresholds are required
to access the keys so this should be checked with the appropriate security engineer. Note that the credentials that can
be omitted from the configuration and input at runtime are given below.

{{< note >}}
A signing task can only be scheduled if its signing key requires no runtime user input for authentication.

{{< /note >}}

* **alias**:
Alias of the signing key within the HSM


* **type**:
The signing key type - `UTIMACO_HSM` in this case


* **keyStore**:
Configuration of the HSM key store.


* **host**:
Host name (or IP address) of the HSM device.


* **port**:
Port number of the HSM device.


* **users**:
List of user authentication configurations. Each entry in the list should have the following format:


* **username**:
HSM username. This can be omitted from the configuration and input at runtime.


* **mode**:
One of the 3 possible authentication modes:
`PASSWORD` - User’s password as set-up in the HSM.
`CARD_READER` - Smart card reader authentication.
`KEY_FILE` - Key file based authentication.


* **password**:
Only relevant if mode is `PASSWORD` or `KEY_FILE`. Specifies either the password credential
for the associated user or the password to the key file, depending on the selected mode. This can be
omitted from the configuration and input at runtime.


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






#### Gemalto Luna HSM Signing Key Example

If the signing key is within a Gemalto HSM then the configuration is simpler than the Utimaco example. This is due to
a lot of the connection logic being within the Java provider library which has to be installed and setup prior to
running the Signing Service (see Gemalto documentation for this). A partition should have been previously set up within
the HSM along with a crypto officer role.


* **alias**:
Alias of the signing key within the HSM


* **type**:
The signing key type - `GEMALTO_HSM` in this case


* **credentials**:
Connection credentials for the HSM.


* **keyStore**:
Slot or partition of the HSM. E.g. “tokenlabel:<EXAMPLE_PARTITION_NAME>”


* **password**:
Password for the keyStore. E.g. the corresponding crypto officer role’s password. This can be omitted
from the configuration and input at runtime.




* **certificateStore**:
*(Optional if using globalCertificateStore)* Certificate store containing all certificates required to build the
entire certificate chain from the signing key back to the root. This is required as the signing keys within the HSM
do not contain their full certificate chains.


  * **file**:
  Certificate store file location.


  * **password**:
  Certificate store password.








#### AWS CloudHSM Signing Key Example

First of all AWS CloudHSM requires a UNIX client running on the machine. It will use that to connect to the HSM.
For detailed documentation about setting up the client please visit Amazon’s
[Getting Started with AWS CloudHSM](https://docs.aws.amazon.com/cloudhsm/latest/userguide/getting-started.html).
After the client is installed the shared library should be under the folder `/opt/cloudhsm/lib` so this should be
used when configuring the `hsmLibraries` property in the configuration. The `.jar` can be found under `/opt/cloudhsm/java/cloudhsm-<version>.jar`
by default.


* **alias**:
Alias of the signing key within the HSM


* **type**:
The signing key type - `AMAZON_CLOUD_HSM` in this case


* **credentialsAmazon**:
The credentials for logging in to the HSM.


* **partition**:
Partition for the HSM. This can be found in the AWS console.


* **userName**:
An existing CU type user in the HSM.


* **password**:
Password for the given CU account.




* **localCertificateStore**:
must be used.
* **file**:
The location of the local certificate store. This will be created if it does not exist.
The local certificate store should contain the entire certificate chain from the signing key back to the root,
because currently `globalCertificateStore` property is not in effect for AWS HSM.


* **password**:
The password for the local certificate store






### Signers Map Entry Example

Each entry in the `signers` map should be keyed on the user-defined, human-readable alias. This can be any
string and is used by the user when viewing and invoking the signing task from within the interactive shell.

Each signing task should use exactly one signing key and service location, and be configured for exactly one data type.


* **type**:
The data type for the signing task. Should be one of `CSR`, `CRL`, `NETWORK_MAP` or `NETWORK_PARAMETERS`.


* **signingKeyAlias**:
The alias for the signing key used by the signing task. Should refer to one of the aliases in the
`signingKeys` map defined above. Please note that if a plugin is used this property must not be present since it is not going to be used.










* **serviceLocation**:
An array containing one or more service locations. For non-CA (Network Map) signing tasks this can be multiple (with subzones).
Expected format:
```docker
serviceLocation = [
    {
        host = localhost
        port = 5050
        verbose = true
        reconnect = true
        ssl = {
            keyStore = {
                location = "./corda-ssl-signer-keys.jks"
                password = password
            }
            trustStore = {
                location = "./corda-ssl-trust-store.jks"
                password = trust-store-password
            }
            validate = true
        }
        timeout = 10000
        subZoneId = 12
    }
]
```

Only the host and port are mandatory, the rest of the properties are optional.
When using a CSR or CRL task please make sure that no `subZoneId` is provided since that is only valid when using a Network Map.
{{< note >}}
Please note that this configuration might lead to duplication. For example, for Network Parameters
and Network Map signing tasks, the `serviceLocation` property will probably be the same.
{{< /note >}}

* **crlDistributionPoint**:
Relevant only if type is `CRL` or `CSR` (optional for `CSR`). The endpoint that the CRL is
hosted on.


* **updatePeriod**:
Relevant only if type is `CRL`. This represents the millisecond duration between CRL updates and is baked into the
generated CRL via the `nextUpdate` X509 field. For users of this CRL, this defines two key pieces of information:
  * Defines when the next CRL should be available - used by some libraries for cache invalidation.
  * Defines when the current CRL has expired and is therefore obsolete.


To ensure that the transition from an old CRL to a new one, this value should always be set to a time period much
larger than the original planned update period. For example, if the `schedule` parameter below has been set to
generate a new CRL every 2 hours, then a `updatePeriod` value would be at least day or multiple days.

If the CRL signing task is being run manually then a sufficiently large enough value should be set here to allow
for breakdowns or delays in the process. A value of 6 months (with signing being performed every 3 months) is
suggested for manual signing scenarios.


* **validDays**:
Relevant only if type is `CSR`. The number of days that a certificate is valid for, counted from the time of
signing. It is highly important that this is set to something sufficiently large enough (e.g 7300 which represents
20 years) as nodes with expired certificates will not be able to communicate across the network.


* **schedule**:
*(Optional)* The scheduled for automated execution of the signing task. Note that this can only be set on tasks that
are linked to signing keys that require no manual user authentication. That is, either a local key store or HSM
signing key using `PASSWORD` or `KEY_FILE` authentication with the password preconfigured.


  * **interval**:
  The duration interval between signing executions. Either a number representing the millisecond duration
  or a string duration with unit suffix. See the [scheduling signing tasks](#scheduling-signing-tasks) section above for information about the accepted format.

* **plugin**:
*(Optional)* Defines which plugin to use for the given signing task.
If this property is present both sub-properties must be present as well.
If a plugin is used the `signingKeyAlias` field must not be present.

  * **pluginJar**:
  A path where the plugin `.jar` file is located. It can be either absolute or relative.

  * **pluginClass**: A package path where the plugin class is located.
  The plugin class must implement either the `NonCASigningPlugin` or the `CASigningPlugin` interface.
  If it does not, an error will be thrown.


## Example Signing Service Configuration

Below are two example configuration files, one using signing keys from local key stores and the other using signing keys
from a HSM. If desired, any combination of local/HSM signing keys can be included within the configuration file.


### Signing Keys From Local Key Store

```docker
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
        type = LOCAL
        password = "example-key-password-2"
        keyStore {
            file = "exampleKeyStore.jks"
            password = "example-password"
        }
    },
    "NetworkMapLocal" = {
        alias = "example-key-alias"
        type = LOCAL
        password = "example-key-password"
        keyStore {
            file = "exampleKeyStore.jks"
            password = "example-password"
        }
    }
}

###################################################
# Signing tasks to be run (manually or scheduled) #
###################################################
signers = {
    "Example CSR Signer" = {
        type = CSR
        signingKeyAlias = "IdentityManagerLocal"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        validDays = 7300 # 20 year certificate expiry
        schedule {
            interval = 1minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5050
                verbose = true
            }
        ]
    },
    "Example CRL Signer" = {
        type = CRL
        signingKeyAlias = "IdentityManagerLocal"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        updatePeriod = 86400000 # 1 day CRL expiry
        schedule {
            interval = 60minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5051
                verbose = true
            }
        ]
    },
    "Example Network Map Signer" = {
        type = NETWORK_MAP
        signingKeyAlias = "NetworkMapLocal"
        schedule {
            interval = 1minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5051
                verbose = true
                subZoneId = 1
            }
        ]
    },
    "Example Network Parameters Signer" = {
        type = NETWORK_PARAMETERS
        signingKeyAlias = "NetworkMapLocal"
        schedule {
            interval = 10minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5051
                verbose = true
                subZoneId = 1
            }
        ]
    }
}

```

### Signing Keys From HSM (no plugin)

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

###################################################
# Signing tasks to be run (manually or scheduled) #
###################################################
signers = {
    "Example CSR Signer" = {
        type = CSR
        signingKeyAlias = "CSRUtimacoHsmSigningKey"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        validDays = 7300 # 20 year certificate expiry
        serviceLocation = [
            {
                host = localhost
                port = 5050
                verbose = true
            }
        ]
    },
    "Example CRL Signer" = {
        type = CRL
        signingKeyAlias = "CRLUtimacoHsmSigningKey"
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        updatePeriod = 5184000000 # 60 day CRL expiry
        serviceLocation = [
            {
                host = localhost
                port = 5051
                verbose = true
            }
        ]
    },
    "Example Network Map Signer" = {
        type = NETWORK_MAP
        signingKeyAlias = "NetworkMapUtimacoHsmSigningKey"
        schedule {
            interval = 1minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5052
                verbose = true
                subZoneId = 1
            }
        ]
    },
    "Example Network Parameter Signer" = {
        type = NETWORK_PARAMETERS
        signingKeyAlias = "NetworkParametersUtimacoHsmSigningKey"
        serviceLocation = [
            {
                host = localhost
                port = 5052
                verbose = true
                subZoneId = 1
            }
        ]
    }
}

```






### CA plugin and non-CA default mechanism

```docker
# In this config a plugin is handling the CA signing and the default CENM signing handles the non-CA signing

shell = {
  sshdPort = 20003
  user = "testuser"
  password = "example-password"
}

#############################################
# All individual keys used in signing tasks #
#############################################
signingKeys = {
    "NetworkMapLocal" = {
        alias = "example-key-alias"
        type = LOCAL
        password = "example-key-password"
        keyStore {
            file = "exampleKeyStore.jks"
            password = "example-password"
        }
    }
}

###################################################
# Signing tasks to be run (manually or scheduled) #
###################################################
signers = {
    "Example CSR Signer" = {
        type = CSR
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        validDays = 7300 # 20 year certificate expiry
        serviceLocation = [
            {
                host = localhost
                port = 5053
                verbose = true
            }
        ]
        schedule {
            interval = 1minute
        }
        plugin {
            pluginJar = "./MySigningPlugin.jar"
            pluginClass = "com.package.MySigningPlugin"
        }
    },
    "Example CRL Signer" = {
        type = CRL
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        updatePeriod = 86400000 # 1 day CRL expiry
        schedule {
            interval = 60minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5054
                verbose = true
            }
        ]
        plugin {
            pluginJar = "./MySigningPlugin.jar"
            pluginClass = "com.package.MySigningPlugin"
        }
    },
    "Example Network Map Signer" = {
        type = NETWORK_MAP
        signingKeyAlias = "NetworkMapLocal"
        schedule {
            interval = 1minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5050
                verbose = true
                subZoneId = 12
            }
        ]
    },
    "Example Network Parameters Signer" = {
        type = NETWORK_PARAMETERS
        signingKeyAlias = "NetworkMapLocal"
        schedule {
            interval = 10minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5050
                verbose = true
                subZoneId = 12
            }
        ]
    }
}

authServiceConfig = {
    disableAuthentication = true
}
```

### Plugin for CA and non-CA tasks

```docker
shell = {
  sshdPort = 20003
  user = "testuser"
  password = "example-password"
}

###################################################
# Signing tasks to be run (manually or scheduled) #
###################################################
signers = {
    "Example CSR Signer" = {
        type = CSR
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        validDays = 7300 # 20 year certificate expiry
        serviceLocation = [
            {
                host = localhost
                port = 5050
                verbose = true
            }
        ]
        plugin {
            pluginJar = "./MySigningPlugin.jar"
            pluginClass = "com.package.MySigningPlugin"
        }
    },
    "Example CRL Signer" = {
        type = CRL
        crlDistributionPoint = "http://localhost:10000/certificate-revocation-list/doorman"
        updatePeriod = 5184000000 # 60 day CRL expiry
        serviceLocation = [
            {
                host = localhost
                port = 5051
                verbose = true
            }
        ]
        plugin {
            pluginJar = "./MySigningPlugin.jar"
            pluginClass = "com.package.MySigningPlugin"
        }
    },
    "Example Network Map Signer" = {
        type = NETWORK_MAP
        schedule {
            interval = 1minute
        }
        serviceLocation = [
            {
                host = localhost
                port = 5052
                verbose = true
                subZoneId = 1
            }
        ]
        plugin {
            pluginJar = "./MySigningPlugin.jar"
            pluginClass = "com.package.MySigningPlugin"
        }
    },
    "Example Network Parameter Signer" = {
        type = NETWORK_PARAMETERS
        serviceLocation = [
            {
                host = localhost
                port = 5052
                verbose = true
                subZoneId = 1
            }
        ]
        plugin {
            pluginJar = "./MySigningPlugin.jar"
            pluginClass = "com.package.MySigningPlugin"
        }
    }
}

authServiceConfig = {
    disableAuthentication = true
}

```
## Developing Signing Plugins

As mentioned before, we enable possibility of writing custom plugin to support external Signing infrastructures. A plugin
class must implement `CASigningPlugin` or `NonCASigningPlugin` interface depending on type of signable material type
it will handle.

Both interfaces extend common `StartablePlugin` interface containing a single method `start()`. The method is run by
Signing Service upon the service start-up and it’s intended to contain plugin’s initialization code (e.g. a database
connection initialization).

```java
public interface StartablePlugin {
    /**
     * Starts the handles plugin's initialization.
     */
    void start();
}

```

Each signable material submission plugin method must return its’ status:

```java

/**
 * A plugin submission must return the signing status of signable material passed.
 * [SigningStatus.COMPLETED] means signing infrastructure has done the successful signing of the material
 * [SigningStatus.PENDING] means signing infrastructure hasn't done a signing of the material yet or it has failed doing so
 */
public enum SigningStatus {PENDING, COMPLETED}
```

### Asynchronous signing

In 1.4 a new asynchronous infrastructure has been added to the plugins.
If your plugin does not sign requests immediately, you can easily return a tracking id (`String` type) and the Signing Service will keep checking
whether the plugin has already signed that particular request.

That is why the plugin interfaces contain new methods called `check*SubmissionStatus()`.
If your plugin simply does not support asynchronous signing you can ignore these tracking functions and just return `null`.
This way the Signing Service will know that the plugin is not asynchronous and will not force tracking the request.

Please note that an optional `requestId` has been added to the plugin response objects (for example `CSRResponse`).
These values are also nullable so when your plugin assembles these please use `null` if your plugin is not asynchronous.

However if your plugin is asynchronous then the returned `SigningStatus` must be `PENDING` and the `requestId` must be present.
This is the only way the Signing Service will be able to track the request.

### CA Signing Plugin

This type of plugin handles Certificate Signing Requests (CSR) and Certificate Revocation List (CRL) signing. A plugin
class must implement following methods with predefined input and output parameters:

```java

/**
 * This is the interface which each CA Signing Service plugin must implement. This is basically the entry point of external Signing
 * Service communication. Each submission request method retrieves signable material and retrieves response containing
 * a signing status (PENDING, COMPLETED) and supporting data to be stored in CENM services.
 */
public interface CASigningPlugin extends StartablePlugin {

    /**
     * Handle retrieved Certificate Signing Requests (CSR) retrieved from Signing Service.
     *
     * @param csr the signing request to route.
     * @return a response describing the status of the request.
     * The response might return a pending status and a request
     * UUID that can be used to check the request status later.
     */
    CSRResponse submitCSR(CertificateSigningRequest csr);

    /**
     * Handle retrieved CRL and CRRs retrieved from Signing Service.
     *
     * @param crl     the signing request to route.
     * @param newCRRs the set of new revocation requests in this batch.
     * @return a response describing the status of the request.
     * The response might return a pending status and a request
     * UUID that can be used to check the request status later.
     */
    CRLResponse submitCRL(@Nullable X509CRL crl, @Nonnull Set<CertificateRevocationRequest> newCRRs);

    /**
     * Retrieves the status of an ongoing CSR signing request.
     *
     * @param requestId The ID of the request
     * @return a response describing the status of the request.
     * This function should only be called after the
     * {@link #submitCSR(CertificateSigningRequest)}
     * returned a {@link SigningStatus#PENDING} status and an ID.
     */
    @Nullable CSRResponse checkCSRSubmissionStatus(@Nonnull String requestId);

    /**
     * Retrieves the status of an ongoing CRL signing request.
     *
     * @param requestId The ID of the request
     * @return a response describing the status of the request.
     * This function should only be called after the {@link #submitCRL(X509CRL, Set)}
     * returned a {@link SigningStatus#PENDING} status and an ID.
     */
    @Nullable CRLResponse checkCRLSubmissionStatus(@Nonnull String requestId);
}

```

CSR submission method output:

```java
/**
 * Signing Service plugin response containing the status of a certificate signing requests (CSR).
 */
public final class CSRResponse {

    /**
     * Returns material's signing status.
     */
    @Nonnull
    public final SigningStatus getStatus();

    /**
     * Returns signed certificate signing request (CSR).
     */
    @Nullable
    public final CSRSigningData getCsrSigningData();

    /**
     * Returns the ID of the request. Might be null if the request is completed immediately and no ID is provided
     * for later use.
     */
    @Nullable
    public String getRequestId() {
        return requestId;
    }

    /**
     * Constructs a response with CRL request status. with the specified data.
     *
     * @param status         Signing status, should be non null otherwise a {@link IllegalArgumentException} is thrown.
     * @param csrSigningData Signed Certificate Request.
     * @param requestId The id of the request for tracking, if the request can be tracked
     */
    @ConstructorForDeserialization
    public CSRResponse(@Nonnull SigningStatus status, @Nullable CSRSigningData csrSigningData, @Nullable String requestId) {
        checkParameterIsNotNull(status, "status", "constructor");
        this.status = status;
        this.csrSigningData = csrSigningData;
        this.requestId = requestId;
    }
}

/**
 * Signed certificate signing request (CSR).
 */
public final class CSRSigningData {

    /**
     * Returns a certificate path generated for associated signed certificate.
     */
    @Nonnull
    public final CertPath getCertPath();

    /**
     * Returns signers' names of entities performing actual signing.
     */
    @Nonnull
    public final String getSigners();

    /**
     * Constructs a signed CSR with the specified data.
     * Both parameters should be not null otherwise {@link IllegalArgumentException} is thrown.
     *
     * @param certPath Certificate path generated for associated signed certificate
     * @param signers  Names of entities performing actual signing.
     */
    public CSRSigningData(@Nonnull CertPath certPath, @Nonnull String signers);
}
```

CRL submission method output:

```java
/**
 * Signing Service plugin response containing the status
 * of a certificate revocation list (CRL) request.
 */
public final class CRLResponse {

    /**
    * Returns material's signing status.
    */
    @Nonnull
    public final SigningStatus getStatus();

    /**
    * Returns signed certificate revocation list (CRL).
    */
    @Nullable
    public final CRLSigningData getCrlSigningData();

    /**
    * Returns the ID of the request. Might be null if the request is completed immediately and no ID is provided
    * for later use.
    */
    @Nullable
    public String getRequestId();

    /**
    * Constructs a response with the specified status and signed CRL.
    *
    * @param status         Signing status, should be non null otherwise a {@link IllegalArgumentException} is thrown.
    * @param crlSigningData Signed Certificate Revocation List (CRL).
    * @param requestId The id of the request for tracking, if the request can be tracked
    */
    @ConstructorForDeserialization
    public CRLResponse(@Nonnull SigningStatus status, @Nullable CRLSigningData crlSigningData, @Nullable String requestId);
}

/**
 * Signed certificate revocation list (CRL).
 */
public final class CRLSigningData {

    /**
     * Returns a newly created signed Certificate Revocation List (CRL).
     */
    @Nonnull
    public final X509CRL getCrl();

    /**
     * Returns names of entities performing actual signing.
     */
    @Nonnull
    public final String getSigners();

    /**
     * Returns a specific time at which signing was executed.
     */
    @Nonnull
    public final Instant getRevocationTime();

    /**
     * Return set of the revocation requests.
     */
    @Nonnull
    public final Set<CertificateRevocationRequest> getRevokedRequests()

    /**
     * Constructs a signed CRL with the specified data.
     * All parameters should be not null otherwise {@link IllegalArgumentException} is thrown.
     *
     * @param crl             Newly created signed Certificate Revocation List (CRL)
     * @param signers         Names of entities performing actual signing
     * @param revocationTime  Specific time at which signing was executed
     * @param revokedRequests Set of all the revocation requests inside the list
     */
    public CRLSigningData(
        @Nonnull X509CRL crl,
        @Nonnull String signers,
        @Nonnull Instant revocationTime,
        @Nonnull Set<CertificateRevocationRequest> revokedRequests
    );
}
```


### Non CA Signing Plugin

This type of plugin handles Network Map and Network Parameters signing. A plugin class must implement following methods
with predefined input and output parameters:

```java

/**
 * This is the interface which each non-CA Signing Service plugin must implement. This is basically the entry point of external Signing
 * Service communication. Each submission request method retrieves signable material and retrieves response containing a
 * singing status (PENDING, COMPLETED) and supporting data to be stored in CENM services.
 */
public interface NonCASigningPlugin extends StartablePlugin {

    /**
     * Handle routing network map to a signing backend.
     *
     * @param signerName name of the back-end signer to route this request to. Must be the signer for
     *                   the subzone the network map is associated with.
     * @return a response describing the status of the request.
     */
    NetworkMapResponse submitNetworkMap(@Nonnull NetworkMap networkMap,
                                        @Nonnull String signerName);

    /**
     * Handle routing network parameters to a signing backend.
     *
     * @param signerName name of the back-end signer to route this request to. Must be the signer for
     *                   the subzone the network parameters are associated with.
     * @return a response describing the status of the request.
     */
    NetworkParametersResponse submitNetworkParameters(@Nonnull UnsignedNetworkParametersData networkParametersData,
                                                      @Nonnull String signerName);

    /**
     * Retrieves the status of an ongoing Network Map signing request.
     *
     * @param requestId The ID of the request
     * @return a response describing the status of the request.
     * This function should only be called after the {@link #submitNetworkMap(NetworkMap, String)}
     * returned a {@link SigningStatus#PENDING} status and an ID.
     */
    @Nullable NetworkMapResponse checkNetworkMapSubmissionStatus(String requestId);

    /**
     * Retrieves the status of an ongoing Network Parameters signing request.
     *
     * @param requestId The ID of the request
     * @return a response describing the status of the request.
     * This function should only be called after the
     * {@link #submitNetworkParameters(UnsignedNetworkParametersData, String)}
     * returned a {@link SigningStatus#PENDING} status and an ID.
     */
    @Nullable NetworkParametersResponse checkNetworkParametersSubmissionStatus(String requestId);
}

```

Network Map submission method output:

```java
/**
 * Signing Service plugin response containing the status of a Network Map signing request.
 */
@CordaSerializable
public final class NetworkMapResponse {

    /**
     * Returns material's signing status.
     */
    @Nonnull
    public final SigningStatus getStatus();

    /**
     * Returns the ID of the request. Might be null if the request is completed immediately and no ID is provided
     * for later use.
     */
    @Nullable
    public String getRequestId();

    /**
     * Returns signed Network Map
     */
    @Nullable
    public final NMSigningData getNmSigningData();

    /**
     * Constructs a response object.
     *
     * @param status        Signing status, should be non null otherwise a {@link IllegalArgumentException} is thrown.
     * @param nmSigningData Signed Network Map data
     * @param requestId The id of the request for tracking, if the request can be tracked
     */
    @ConstructorForDeserialization
    public NetworkMapResponse(@Nonnull SigningStatus status, @Nullable NMSigningData nmSigningData, @Nullable String requestId);
}
```

Network Parameters submission method output:

```java
/**
 * Signing Service plugin response containing the status of a Network Parameters signing request.
 */
@CordaSerializable
public final class NetworkParametersResponse {

    /**
     * Returns material's signing status.
     */
    @Nonnull
    public final SigningStatus getStatus();

    /**
     * Returns the ID of the request. Might be null if the request is completed immediately and no ID is provided
     * for later use.
     */
    @Nullable
    public String getRequestId();

    /**
     * Returns signed Network Parameters
     */
    @Nullable
    public final NMSigningData getNmSigningData();

    /**
     * Constructs a response object.
     * All parameters should be not null otherwise {@link IllegalArgumentException} is thrown.
     *
     * @param status        Signing status, should be non null otherwise a {@link IllegalArgumentException} is thrown.
     * @param nmSigningData
     */
    public NetworkParametersResponse(@Nonnull SigningStatus status, @Nullable NMSigningData nmSigningData);
}
```

Both responses use same signature data:

```java
/**
 * Signed Network Map or Network Parameters
 */
public final class NMSigningData {

    /**
     * Returns signed material's certificate
     */
    @Nonnull
    public final X509Certificate getSignerCertificate();

    /**
     * Returns list of all the parent certificates of the material
     */
    @Nonnull
    public final List<X509Certificate> getParentCertsChain();

    /**
     * Returns raw signature
     */
    @Nonnull
    public final byte[] getSignature();

    /**
     * Constructs an object.
     * All parameters should be not null otherwise {@link IllegalArgumentException} is thrown.
     *
     * @param signerCertificate Signed material's certificate
     * @param parentCertsChain  List of all the parent certificates of the material
     * @param signature         Raw signature
     */
    public NMSigningData(
        @Nonnull X509Certificate signerCertificate,
        @Nonnull List<X509Certificate> parentCertsChain,
        @Nonnull byte[] signature
    );
}
```


### Example Signing Plugins

The Signing Service ships with example plug-ins.

{{< note >}}
Please note that these plug-ins should only be used as a base
when developing plug-ins and they should never be used in a production environment.
{{< /note >}}

Please refer to the `README` docs inside the source directories for each plug-in as they contain all the
necessary information about the architecture and usage of those plug-ins.

#### Example CA Signing Plugin

The CA plugin class name to configure is always `com.r3.enm.signingserviceplugins.exampleplugin.ca.ExampleCaSigningPlugin`.

The diagram below shows how the plug-in works on a high level.  
The plug-in acts as a bridge between the Signing Service and a possible third-party signer architecture.  
The plug-in will launch its own RPC server for the third party to connect to.
This RPC API involves fetching (getting the signable data) and submitting (pushing the signed data back).

The plug-in has an in-memory storage that acts as a database and stores two things:
1. The requests that are signed by the third party.
2. The requests that are ready to sign by the third party.

When the user submits a request for signing to the Signing Service, it sends the signable
data to the plug-in and returns a `PENDING` status immediately.
The signing request is NOT persisted to the CENM services at this stage (the request is not yet considered done).


The user is informed that the signing has not finished yet, and is sent an ID for tracking.
For a CSR request, this looks as follows:

```
The following requests didn't sign immediately, please follow up with the provided tracking it to check the request status:
 O=NodeA, L=London, C=GB - Tracking id: 00354917-5795-4969-96ee-ae2c4406fde3
```

In the background, the Signing Service periodically queries the plug-in to check whether the given request(s) has/have been completed.

If any of the pending requests has been signed by the plug-in (so a `COMPLETED` status is returned for it), the Signing Service
persists it to the CENM services, and the request is considered as done. As a result, in case of a CSR request for example,
the Corda node will join the network.

If any of the pending requests fails, it is not persisted and is removed from the pending requests.


{{< figure zoom="./resources/example-ca-plugin-diagram.png" width="800" title="Example CA plug-in diagram (click to zoom)" alt="Example CA plug-in diagram" >}}

An example third-party signer is also attached. It uses a Signing Service configuration to sign the
data stored inside the example CA plug-in.

{{< note >}}
CA Plugin’s configuration file must be in the same directory as the service’s `.jar` file and must be named
“ca-plugin.conf”

{{< /note >}}

There is an example configuration attached to the source for both the CA plug-in and the third-party Signer.

#### Non CA Example Signing Plugin

The non-CA plug-in's class name to configure is always `com.r3.enm.signingserviceplugins.example.nonca.ExampleNonCaSigningPlugin`.

The plug-in has an in-memory storage that contains two maps - one for the Network Parameters requests and another one
for the Network Map requests. In a real-world scenario, this would be a database where the status of
each submitted request could be stored.

The plug-in uses a dummy signing mechanism using the `NonCaLocalSigner` class.

{{< note >}}
Non CA Plugin’s configuration file must be in the same directory as the service’s `.jar` file and must be named
“non-ca-local-signer.conf”
{{< /note >}}

There is an example configuration in the `resources` directory.

This configuration contains the signing key that should be used for Network Map / Network Parameters signing. The configuration
is parsed as a Signing Service configuration for the sake of simplicity, so it contains some placeholder data.

The plug-in can use HSM signing too, not just local signing -
refer to the [Signing Service configuration](#signing-service-configuration) section for more information on how to do that
and create the configuration accordingly.

{{< note >}}
The Network Map signing key must be aliased as `NetworkMapLocal` in the configuration.
{{< /note >}}

Once the signing is done, the plug-in will return a `COMPLETED` status immediately.

This means that this example does not utilise the asynchronous signing completely - so, there will be no `PENDING` status.
However, the tracking ID will still be returned and the request can be tracked via the tracking functions.

### Other Sample Plugins

See [EJBCA Sample Plugin](ejbca-plugin.md) for sample open source CA implementation.

### Admin RPC Interface

To enable the CENM Command-Line Interface (CLI) tool to send commands to the Signing Service,
you must enable the RPC API by defining a configuration property called `adminListener`.

For example, add the following to the service configuration:

```guess
...
adminListener {
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
...
```

{{< note >}}
The `reconnect` parameter is optional - it will default to `reconnect = true` if not set.
{{< /note >}}

{{% important %}}
If the `adminListener` property is present in the configuration, this means that the service must only be used via Admin RPC. In this case, the `shell` configuration property will be disabled. The `shell` and `adminListener` properties cannot be used in the configuration at the same time.
{{% /important %}}

The admin RPC interface requires an Auth Service to verify
requests, which must be configured below in a `authServiceConfig` block. Typically
this is provided automatically by the Zone Service (via an Angel Service),
however an example is provided below for reference:

```guess
authServiceConfig {
    host = <auth service host>
    port = <auth service port>
    trustStore = {
        location = /path/to/trustroot.jks
        password = <key store password>
    }
    issuer = <issuer>
    leeway = <leeway duration>
}
```

## Obfuscated configuration files

To view the latest changes to the obfuscated configuration files, see [Obfuscation configuration file changes](obfuscated-config-file-changes.md).
