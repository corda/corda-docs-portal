---
aliases:
- /releases/4.4/cenm/signing-service.html
date: '2020-01-08T09:59:25Z'
menu:
- corda-enterprise-4-4
tags:
- signing
- service
title: Signing Services
---


# Signing Services



## Purpose

The Signable Material Retriever (SMR) and Signing Service are services that form part of
Corda Enterprise Network Manager, alongside the Identity Operator and Network Map. They act as
a bridge between the main CENM services and PKI/HSM infrastructure, enabling a network operator
to verify and sign incoming requests and changes to the network.

As mentioned in the CENM service documentation ([Identity Manager Service](identity-manager.md) and [Network Map Service](network-map.md)), the main CENM services
can be configured with an integrated *local signer* that will automatically sign all unsigned data using a provided key.
While this is convenient, it is intended for use within for testing and experimental environments, and **should not** be used in
production environments. Instead, large and important changes to the network should go through a series of checks before
being approved and signed, ideally with a network operator manually verifying and signing new CSRs, CRLs and Network
Parameter changes. The Signing Service provides this behaviour, with HSM integration enabling the signing of any
particular data to require authentication from multiple users.


## Signable Material Retriever

The Signable Material Retriever service acts as a bridge between other CENM services and one or more
signing services. It delegates signing to a plugin, which routes work either to the CENM Signing Service,
or to a third party service. Third party integration plugins are not provided as part of CENM.


### Running the Signable Material Retriever Service

Once the Signable Material Retriever has been configured, it can be run via the command:

```bash
java -jar smr-<VERSION>.jar --config-file <CONFIG_FILE>
```

Optional parameter:

```bash
--working-directory=<DIR>
```

This will set the working directory to the specified folder. The service will look for files in that folder. This means
certificates, config files etc. should be under the working directory.
If not specified it will default to the current working directory (the directory from which the service has been started).

On success you should see a message similar to:

```kotlin
Plugin started
SMR Service started
```


### SMR Configuration

The configuration of the SMR service consists of the following two components:


* [CENM service locations](#cenm-service-locations) which determine SMR’s data sources
* [Material Management Tasks](#material-management-tasks) parameters modeling how each signable material is managed by SMR


#### CENM Service Locations

For each material management task, the data source for getting the unsigned data and persisting signed data must be
defined. One data source could be potentially used across multiple material management tasks, hence they are configured
as a map of human-readable aliases (referenced by the material management task configuration) to ENM service locations.

{{< note >}}
Communication with the configured SMR service location can be configured to use SSL for a secure, encrypted
connection. This is strongly recommended for production deployments. See [Configuring the ENM services to use SSL](enm-with-ssl.md) for more
information.

{{< /note >}}
Configuration parameters are same as in [Signable Material Retriever Location Example](#signable-material-retriever-location-example)


#### Material Management Tasks

Each material management task is configured as a map of human-readable aliases (exactly the same as in singing tasks
configuration of Signing Service) to Material Management Task configuration.

Here are configuration parameters:


* **type**: 
The data type for the signing task. Should be one of `CSR`, `CRL`, `NETWORK_MAP` or `NETWORK_PARAMETERS`.


* **location**: 
The alias for the service location used by the material management task. Should refer to one of the aliases
in the serviceLocations map defined above.


* **schedule**: 
The schedule for automated execution of the material management task.


* **interval**: 
The duration interval between signing executions. Either a number representing the millisecond
duration or a string duration with unit suffix. See below scheduling signing tasks section on
accepted format.




* **pluginJar**: 
The absolute path to signing plugin JAR file


* **pluginClass**: 
The class that will be loaded from plugin JAR file and will be its entry point from SMR




### Example SMR Configuration

Here is example of complete SMR configuration:


### Signing Plugin

As mentioned before, we enable possibility of writing custom plugin to support external Signing infrastructures. Each
plugin must implement following *SigningPlugin* interface which methods have predefined input and output parameters:


### Internal Signing Plugin

SMR ships with a plugin for the CENM provided Signing ServiceThe only requirement is to provide
the plugin’s JAR path. The plugin class name to configure is always *com.r3.enm.smrplugin.SMRSigningPlugin*.

This internal plugin also has its own simple configuration which defines the port the SMR will
bind to for the Signing Service to connect to. Here is example plugin configuration:

```docker
enmListener = {
    port = 5010
}
```

{{< note >}}
Plugin’s configuration file must be in same directory as plugin’s JAR file and must be named “plugin.conf”

{{< /note >}}

## Signing Service

CENM’s Signing Service supports the following HSMs (see [CENM support matrix](cenm-support-matrix.md) for more information):


* Utimaco
* Gemalto Luna
* Securosys PrimusX
* Azure Key Vault

The verification and signing of data is done via the set of user configured signing tasks within the service, with each
task being configured with:


* **Data type:** CSR, CRL, Network Map or Network Parameters
* **Data source:** the SMR service to retrieve unsigned data and persist signed data
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
mentioned above, the only communication requirements are outgoing connections to the SMR service configured as data
source which then connects to CENM services (Identity Manager and Network Maps), and outgoing connections to the HSMs
for the configured signing keys. The overall flow of communication can be seen in the below diagram:

![signing service communication](cenm/../resources/signing-service-communication.png "signing service communication")
{{< note >}}
All inter-service communication can be configured with SSL support to ensure the connection is encrypted. See
[Configuring the ENM services to use SSL](enm-with-ssl.md)

{{< /note >}}
{{< note >}}
This document does not cover HSM setup, rather assumes that the HSM(s) have already been configured - the
users and certificates should have been previously setup on the box.

{{< /note >}}

### Running the Signing Service

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

To verify that SMR data source is reachable by the Signing Service, a health check can be performed by running the
`run clientHealthCheck`. This will send a simple ping message and verify a successful response. Any unsuccessful
connection attempts will be displayed to the console. This method is especially useful after the initial setup to
verify that the Signing and SMR services have been configured correctly.


## Signing Service Configuration

The configuration for the Signing Service consists of the following sections:


* The [global configuration options](#global-configuration-options) (interactive shell and optional default certificate store)
* The [signing keys](#signing-keys) that are used across all signing tasks
* The [data source (SMR Service Location)](#data-source-smr-service-location) that is used across all signing tasks
* The [signing tasks](#signing-tasks) that can be run through the service


### Global Configuration Options


#### Shell Configuration

The Signing Service is interacted with via the shell, which is configured at the top level of the config file. This
shell is similar to the interactive shell available in other ENM services and is configured in a similar way. See
[Shell Configuration](../shell.md#shell-config) for more information on how to configure the shell.


#### HSM Libraries

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

See the 
{{< warning >}}`Example Configuration`_{{< /warning >}}

 section below for examples of these config blocks being used in a complete file.


##### Azure Key Vault

To keep inline with the other HSMs, the Azure Key Vault client jar needs to provided as above. Unlike the other HSMs,
there are many dependent libraries. The top-level dependencies are `azure-keyvault` and `adal4j`, however these both
have transitive dependencies that need to be included. That is, either all jars need to be provided separately (via a
comma-separated list) or an uber jar needs to be provided.

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

This will create a jar called `azure-keyvault-with-deps.jar` which can be referenced in the config.


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
{{< warning >}}`Configuration Parameters`_{{< /warning >}}

 section
below.


### Data Source (SMR Service Location)

For all signing tasks, global data source for getting the unsigned data and persisting the signed data needs to be
defined. This is ENM location of Signable Material Retriever Service.

{{< note >}}
Communication with the configured SMR service location can be configured to use SSL for a secure, encrypted
connection. This is strongly recommended for production deployments. See [Configuring the ENM services to use SSL](enm-with-ssl.md) for more
information.

{{< /note >}}

#### Signing Tasks

This configuration section defines each signing task that can be run via the service. Each task is defined by adding an
entry to the `signers` configuration map, keyed by the human-readable alias for the task (used when interacting with
the service via shell). The value for the entry consists of the configuration options specific to that task such as the
signing key and data source that is uses (using the previously defined alias in the `signingKeys` configuration
parameters), data type specific options such as the CSR validity period as well as schedule if applicable.

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
* A connection to the Signable Material Retriever service is established and the unsigned Network Parameter update is
fetched and displayed to the user.
* The user confirms that the changes are correct and should be signed.
* A connection to the appropriate HSM is created, and the user is prompted for their authentication credentials. The
exact format of this authentication will depend on the configured signing key that the signing task uses.
* Once the user has been successfully authenticated and their privileges are strong enough, then the signing process
commences using the configured signing key. If their privileges are not sufficient then the signing task will prompt
for another user to be authenticated, repeating this process until the configured HSM authentication threshold has
been exceeded.
* The Network Parameter update is signed then persisted back to the Signable Material Retriever service. When the Network
Map is next updated and signed, the newly signed parameter update will be included and therefore broadcast to the
network participants.

The steps involved in signing other data types are very similar to above, mainly differing in the unsigned information
that is retrieved from the corresponding CENM service:

**Network Map:**
The latest unsigned network map is fetched from the Signable Material Retriever service. This will include all network
participants (new and current) that have a valid, non-revoked certificate signed by the network’s Identity Manager, as
well as the signed Network Parameters (active and pending update if applicable). If the Network Map has not changed
since it was last signed then the signing process will finish.

**Certificate Signing Request (CSR)**:
All approved but unsigned CSRs are fetched from the Signable Material Retriever and displayed to the user. They can
then select all or a subset of these to sign.

**Certificate Revocation List (CRL)**:
All approved but unsigned Certificate Revocation Requests (CRRs) are fetched from the Signable Material Retriever and
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
The HSM type for the library (`UTIMACO_HSM`, `GEMALTO_HSM`, `SECUROSYS_HSM` or `AZURE_KEY_VAULT_HSM`).


* **jars**: 
List of paths for the HSM Jars.


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
below for the expected format.


* **smrLocation**: 
Signable Material Retriever ENM service location configuration.


* **signers**: 
Map of human-readable aliases (string) to signing task configuration. Defines the tasks that can be run by a
user via the interactive shell. Each signing task should refer to exactly one signing key and one service
location using the alias defined in the above maps. See the [signers map entry example](#signers-map-entry-example) below for the
expected format.




### Signing Key Map Entry Example

Each entry in the `signingKeys` map should be keyed on the user-defined, human-readable alias. This can be any string
and is used only within the config to map the signing keys to each signing task that use it.

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








### Signable Material Retriever Location Example


* **enmService**: 
The connection details for the SMR service that acts as the data source


* **host**: 
Host name (or IP address) that the SMR service is running on


* **port**: 
Port that the SMR service is listening on (for inter-ENM communication)


* **verbose**: 
Boolean representing whether debug information for the IPC between the Signer and the remote service
should be displayed.


* **ssl**: 
*(Optional)* SSL Information for connection with the SMR service.


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


* **crlDistributionPoint**: 
Relevant only if type is `CRL` or `CSR` (optional for `CSR`). The endpoint that the CRL is
hosted on.


* **updatePeriod**: 
Relevant only if type is `CRL`. This represents the millisecond duration between CRL updates and is baked into the
generated CRL via the `nextUpdate` X509 field. For users of this CRL, this defines two key pieces of information:

> 
> 
> * When the next CRL should be available, which is used by some libraries for cache invalidation.
> * When then current CRL should be considered expired and therefore obsolete.


To ensure that the transition from an old CRL to a new one, this value should always be set to a time period much
larger than the original planned update period. For example, if the `schedule` parameter below has been set to
generate a new CRL every 2 hours, then a `updatePeriod` value would be at least day or multiple days. If the CRL
signing task is being run manually then a sufficiently large enough value should be set here to allow for breakdowns
or delays in the process.


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
or a string duration with unit suffix. See above [scheduling signing tasks](#scheduling-signing-tasks) section on accepted format.






## Example Signing Service Configuration

Below are two example configuration files, one using signing keys from local key stores and the other using signing keys
from a HSM. If desired, any combination of local/HSM signing keys can be included within the configuration file.


### Signing Keys From Local Key Store


### Signing Keys From HSM

