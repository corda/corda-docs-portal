---
menu:
  cenm-1-7:
    identifier: cenm-1-7-auth-service
    parent: cenm-1-7-operations
tags:
- authentication
- auth
weight: 150
aliases: "/docs/cenm/1.7/auth-service.html"
title: Auth Service
---

# Auth Service

The Auth Service is the user authentication and authorisation service for managing Corda nodes and networks (CENM). It stores and controls secure user access to network services, such as:

* Nodes
* Identity Manager
* Zone Service
* Signing Service
* Network Map (and associated network configurations and node info)

Whenever you use the [User Administration Tool]({{< relref "user-admin.md" >}}) to create new users, groups or roles, the Auth Service is updated to authenticate those users and their permissions. When using the remote management tools such as the [CENM Command Line Interface]({{< relref "cenm-cli-tool.md" >}}) or the web GUIs hosted on the Gateway Service, the Auth Service verifies your identity and security clearance as needed.

You do not need to interact directly with the Auth Service once it has been installed and configured. To protect the integrity of this secure service, there is no direct API contact with the Auth Service: all front-end communications go via the Gateway Service.

The Auth Service can also be configured to use {{< cordalatestrelref "enterprise/node/azure-ad-sso/_index.md" "[Azure AD SSO" >}}.

Config obfuscation tool

## Installing the Auth Service

You can install the Auth Service by either:

- [Installing using the Docker image](#install-using-the-docker-image)
- [Installing using the JAR file](#install-using-the-jar-file) `accounts-application.jar`

### Install using the Docker image

The Docker image contains the application jar itself setup to run with the `Initial user` commands.

To install from the Docker image, ensure that the config file and other required files are mounted as a shared volume when running the container.

{{< note >}}
The Docker image contains an empty plugins folder: `/opt/authsvc/plugins`. When creating a new image from this one, you only need to copy the application specific baseline into this folder, and it will be picked up automatically.
{{< /note >}}

Environment variables:

* **INITIAL_ADMIN_USERNAME:** 
  Initial user name, defaults to `admin`
* **INITIAL_ADMIN_PASSWORD:** 
  Initial user password, defaults to `password`
* **CONFIG_FILE_LOCATION:** 
  Location of the configuration file, defaults to `/usr/auth/auth.conf`. 
  To use the default setting, the config file should be mounted under `/usr/auth`
* **ADDITIONAL_ARGUMENTS:** 
  Additional command line args passed to the service; 
  defaults to "--verbose"


### Install using the JAR file

To install the Auth Service using the `accounts-application.jar` JAR file:

1. Add the file `accounts-application.jar` to your CENM working directory.
2. Configure the Auth Service using the command line.

## Preparing for configuration

Before you can configure the Auth Service, you need to prepare SSL certificates, create signing keys and add your baseline permissions JAR file so that new permissions can be added to the Auth Service:

1. Create a SSL certificate in a `.jks` file using the [CENM PKI tool]({{< relref "pki-tool.md" >}}).
2. Generate a JWT signing key (RSA keypair) in a `.jks` file with the following command-line command:
`keytool -genkeypair -alias mytest -keyalg RSA -keypass mypass -keystore mytest.jks -storepass mypass`.
3. Ensure you have the CENM baseline JAR file `accounts-baseline-cenm-<VERSION>.jar` that contains the set
of available permissions and predefined roles. 
4. Copy this file to a directory called `plugins`, located inside the working directory.

## Configuring the Auth Service

To deploy the Auth Service, you need to create a configuration file. When you create this configuration file, you must establish its connection to your [Gateway Service]({{< relref "gateway-service.md" >}}). Make sure you know:

* Your Gateway service ID
* Your Gateway service secret

In the sample below, you can see the initial configuration process:

1. [Database configuration]({{< relref "database-set-up.md" >}}). Add the name, address and login credentials for the SQL database that supports the Auth Service.
   {{<note>}}
   If multiple CENM instances are connected to the same database, setting `lockResolutionStrategy` to `SingleInstance` can cause startup problems and/or database corruption. For more information, see the [database configuration options]({{< relref "config-database.md" >}}).
   {{</note>}}
2. Configure the JSON Web Key: set the user name, password, and location of the RSA keypair store for signing. The location must be the absolute path.
3. Configure the connection to the Gateway service. Add the ID, secret, and scope of services that you use when setting up the Gateway service.
4. Configure the web server.
5. Set optional password policy settings.


```
# database configuration
database {
    driverClassName = "org.h2.Driver"
    url = "jdbc:h2:file:/usr/auth/auth-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "testuser"
    password = "password"
    runMigration = true
    lockResolutionStrategy = "SingleInstance"
}
# JSON Web Key configration for JWT signing
jwk {
    # Location of the RSA keypair store for singing (MUST BE absolute path)
    location = "/usr/auth/jwt-store.jks"
    # Password for the keystore
    password = "password"
    # Key alias for the RSA keypair, default value is 'cordaauthjwk'
    keyAlias = "oauth-test-jwt"
}
# Client configuration, this should contain credentials and config for Gateway service instances
clientConfig = {
    clients = [
        {
            # Client id, must be the same as configured for Gateway
            clientId = "gateway1"
            # Client secret, must be the same as configured for Gateway
            clientSecret = "secret1"
            # Available scopes for this Gateway service instance, can be any of the below:
            #  - accounts:admin
            #    - indicates access to user management from the Gateway service
            #  - accounts:user
            #    - indicates zone access from the Gateway service
            # default value is 'accounts:user'
            scopes = [
                "accounts:admin"
            ]
            # This is a list of services that will accept the token generated through
            # this Gateway instance, possible values (it is case sensitive):
            #  - zone (zone service)
            #  - identity-manager (doorman service)
            #  - signer (signer service)
            #  - network-map (network-map service)
            audience = [
                "zone"
            ]
            # access token validity
            # Should be short, default is 1 hour
            accessTokenValidity = 300
            # refresh token validity
            # should be in sync with company 'stay logged in' policy
            # default value is 7 days
            refreshTokenValidity = 6000
        }
    ],
    # Issuer value for the JWTs, must match with whatever is configured for CENM services
    # Default is 'accounts-service'
    issuer = "http://test"
}
# Configuration for the web server
server {
    # listening port
    port = 8081
    # SSL data
    ssl = {
        keyStore = {
            # MUST BE absolute path
            location = "/usr/auth/corda-ssl-network-map-keys.jks"
            password = "password"
            # Defaults to 'cordasslauthservice' if not set
            keyAlias = "cordasslnetworkmap"
        }
        trustStore = {
            # MUST BE absolute path
            location = "/usr/auth/corda-ssl-trust-store.jks"
            password = "trustpass"
        }
    }
}
# Optional password policy settings
passwordPolicy = {
    # Enables password expiration
    # Disabled by default
    expiration = {
        enabled = true
        passwordMaxAge = 1
    }
    # Enables automatic user lockout after a certain number of failed login attempts
    # Disabled by default
    lock = {
        enabled = true
        loginAttempts = 1
    }
    # Enabled by default
    mustMeetComplexityRequirements = false
}
```

### Managing your configuration

You can manage the Auth Service configuration by specifying the following command line options for `accounts-application.jar`:

- `[-f, --config-file]` Path of the service config file.
- `[-o, --obfuscated]` Indicates an obfuscated config.
- `[--seed]` Optional seed for config deobfuscation.
- `[-v, --verbose]` Redirect all log output to the console. Also sets logging level to INFO.
- `[--logging-level]` Sets logging level. Accepts Log4j Levels.
- `[--initial-user-provider]` Sets the authentication provider for the initial user. Valid values are ```internal``` or ```azuread```; the default is ```internal```.

The initial admin user of the Auth Service is *initializer*: The following command line options allow configuration of that initial admin user.

- `[--initial-user-name]` Sets the name of the user.
- `[--initial-user-password]` Sets the password of the user when provider is ```internal```.
- `[--initial-user-external-id]` External ID of the user when using a provider other than ```internal``` that requires it. In case of AzureAD this should be the ObjectID of the user whose user name is used in the ```--initial-user-name``` parameter.
- `[--restore-admin-capability]` (**initializer**) If all admin users are locked out, for example because of password policy, this option unlocks them.

The following command line options can be used to reset, re-enable, and unlock a user. You can also sets a user's password or force the user to become an administrator. Administrators can create and edit other users, but cannot access CENM services directly.

* `[--reset-user-username]` Username to be reset.
* `[--reset-user-password]` New password for the user being reset.
* `[--reset-user-admin]` Flag to enable forcing the user to be admin.
* `[--keep-running]` Enables the application to keep running after any of the **initializer** arguments have been supplied.

## Setting up applications

{{< note >}}
The Auth Service needs to be set up with baseline permission data for each application.
{{< /note >}}

* [CENM management console]({{< relref "cenm-console.md#installing-the-cenm-management-console" >}})
* [Node management console]({{< relref "management-console.md#installation" >}})
* [Flow management console]({{< relref "node-flow-management-console.md#installation" >}})
