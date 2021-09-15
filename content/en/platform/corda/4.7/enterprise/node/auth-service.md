---
menu:
  corda-enterprise-4-7:
    parent: corda-enterprise-4-7-corda-nodes
tags:
- authentication
- auth
weight: 150
title: Auth service
---

# Auth Service

The Auth Service is the user authentication and authorisation service for managing Corda Nodes and networks (CENM). It stores and controls secure user-access to network services, such as:

* Nodes.
* Identity Manager
* Zone Service
* Signing Service
* Network Map (and associated network configurations and node info)

Whenever you use the [User Administration Tool](../../../cenm/1.5/user-admin) to create new users, groups or roles, the Auth Service is updated to authenticate those users and their permissions. When using the remote management tools such as the [CENM Command Line Interface](../../../cenm/1.5/cenm-cli-tool) or the web GUIs hosted on the Gateway Service, the Auth Service verifies your identity and security clearance as needed.

You do not need to interact directly with the Auth Service once it has been installed and configured. To protect the integrity of this secure service, there is no direct API contact with the Auth Service: all front-end communications go via the Gateway Service.

Auth Service can also be configured to use [Azure AD SSO](azure-ad-sso).

## Install the Auth service

You can install the Auth service by either:

* Installing the `accounts-application.jar`.
* Installing the Docker image.

### Install using the docker image

The docker image contains the application jar itself setup to run with the `Initial user` commands.

To install from the docker, ensure that the config file and other required files are mounted as a shared volume when running the container.

{{< note >}}
The docker image contains an empty plugins folder: `/opt/authsvc/plugins`. When creating a new image from this one, you only need to copy the application specific baseline into this folder, and it will be picked up automatically.
{{< /note >}}

Environment variables:

* INITIAL_ADMIN_USERNAME
  * Initial user name, defaults to `admin`
* INITIAL_ADMIN_PASSWORD
  * Initial user password, defaults to `password`
* CONFIG_FILE_LOCATION
  * Location of the configuration file, defaults to `/usr/auth/auth.conf`
  * To use the default setting the config file should be mounted under `/usr/auth`
* ADDITIONAL_ARGUMENTS
  * Additional command line args passed to the service
  * Defaults to "--verbose"


### Install using the .jar file

1. Add the file `accounts-application.jar` to your CENM working directory.
2. Configure the Auth service using the command line.

### Prepare for configuration

Before you can configure the Auth service, you need to prepare SSL certificates, create signing keys and add your baseline permissions `.jar` file so that new permissions can be added to the Auth service.

To do this:

1. Create a SSL certificate in a `.jks` file using the [CENM PKI tool](../../../cenm/1.5/PKI-tool).

2. Generate a JWT signing key (RSA keypair) in a `.jks` file with the following command-line command:
`keytool -genkeypair -alias mytest -keyalg RSA -keypass mypass -keystore mytest.jks -storepass mypass`.

3. Ensure you have the CENM baseline `.jar` file `accounts-baseline-cenm-<VERSION>.jar` that contains the set
of available permissions and predefined roles. Copy this file to a directory called `plugins`, located inside the working directory.

## Configure the auth service

To deploy the Auth service, you need to create a configuration file.

When you create your config file, you establish its connection to your [Gateway Service](gateway-service). Make sure you know:

* Your Gateway service ID.
* Your Gateway service secret.

In the sample below, you can see the initial configuration process:

1. [Database configuration](../../../cenm/1.5/database-set-up). Add the name, address and login credentials for the SQL database that supports the Auth Service.

{{<note>}}
If multiple CENM instances are connected to the same database, setting `lockResolutionStrategy` to `SingleInstance` can cause startup problems and/or database corruption. For more information, see the [database configuration options](../../../cenm/1.5/config-database.md).
{{</note>}}

2. JSON Web Key configuration. Set the user name, password, and location of the RSA keypair store for signing. The location must be the absolute path.

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

### Manage your configuration

You can manage the Auth Service configuration using the command line.

Command line arguments:

* `[-f, --config-file]` Path of the service config file.
* `[-o, --obfuscated]` Indicates an obfuscated config.
* `[--seed]` Optional seed for config deobfuscation.
* `[-v, --verbose]` Redirect all log output to the console. Also sets logging level to INFO.
* `[--logging-level]` Sets logging level. Accepts Log4j Levels.

Initial user **initializer**: This command group allows configuration of the initial admin user. Both options are required when any of them is in use.
* `[--initial-user-name]` Sets the name of the user.
* `[--initial-user-password]` Sets the password of the user.

* `[--restore-admin-capability]` ()**initializer**) If all admin users are locked out, for example because of password policy, this option unlocks them.

Reset user (**initializer**): Use this command group to reset, re-enable, and unlock a user. You can also sets a user's password or force the user to become an administrator. Administrators can create and edit other users, but cannot access CENM services directly.

* `[--reset-user-username]` Username to be reset.
* `[--reset-user-password]` New password for the user being reset.
* `[--reset-user-admin]` Flag to enable forcing the user to be admin.

* `[--keep-running]` Enables the application to keep running after any of the **initializer** arguments have been supplied.

## Setting up applications

{{< note >}}
Auth Service needs to be set up with baseline permission data for each application.
{{< /note >}}

* [CENM management console](../../../cenm/1.5/cenm-console#installation)
* [Node management console](management-console#installation)
* [Flow management console](node-flow-management-console#installation)
