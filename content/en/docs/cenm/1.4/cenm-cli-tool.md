---
aliases:
- /cenm-cli-tool.html
- /releases/release-1.4/cenm-cli-tool.html
date: '2020-05-28T17:40:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-cli-tool
    parent: cenm-1-4-tools-index
    weight: 1013
tags:
- CLI
- CENM command line interface
- CENM command-line interface
- shell
title: CENM Services Command-line Interface
---

# CENM Command-line Interface Tool

The CENM Command-line Interface (CLI) allows you to perform key CENM tasks remotely and securely.

Once you have the required permissions to access the CENM service you require, you can use the CLI to perform tasks with the following services:

* Identity Manager
* Zone Service
* Network Map
* Signing Service

## Install the CENM CLI Tool

The CLI Tool comes as a part of CENM 1.4 as a `.jar` file. If you cannot access the `.jar` file, you can install via Docker image.

To install using Docker:

1. Install Docker from the [Docker website](https://www.docker.com/get-started).

2. Use the command line to download the Docker image with CENM CLI:

     ```bash
     docker pull cenm-cli:1.4-zulu-openjdk8u242
     ```

You have installed the Docker image with CENM CLI tool.

To get the tool ready to use from within the Docker container, check the [Kubernetes deployment guide](deployment-kubernetes.md#network-operations).

## Set up the CENM CLI Tool

In order to use the CLI, you must have permission to access the CENM services you plan to use.

You should have an account that has been set up by a user administrator using the [User Admin application](user-admin.md/). This account gives you the credentials, roles, and permissions you need to access CENM services via the CLI.

For the below example, the credentials of a sample CENM user are shown:

Name: Alice Barthes
Username: alice.barthes
Password: w34rfrt45g4y65EERTR5


### Quickstart - outline of steps to set up a new network with the CLI

You must set up any new network in a specific order, as some services rely on information that must be in place before they can be created.
Most importantly, you must set the **Signing service** configuration last - this is because you need to have configuration details for all the other services before you can access their signing requests.

In the example below, you can see the steps to set up a new network with the CLI. When setting up your own network, you need to replace the sample parameters, usernames, passwords, service addresses and other information as applicable to your deployment.

To set up a new network with the CLI:

1. Login by setting the [context login address](#define-contexts-and-servers), your username, and password:

    `./cenm context login http://10.230.41.12 -u alice.barthes -p w34rfrt45g4y65EERTR5`

2. Set the Identity Manager's external admin address. This must be the address that the gateway Gateway service uses to communicate with the Identity Manager:

    `./cenm identity-manager config set-admin-address -a=identity-manager:5053`

3. Set the Identity Manager config. This command returns a **Zone token** which you should pass to your [Angel Service](angel-service):

    `./cenm identity-manager config set -f config/identitymanager.conf --zone-token`

4. Create a new subzone - including the admin address for Network Map. This must be the address that the gateway Gateway service uses to communicate with the Network Map:

    `./cenm zone create-subzone --config-file=config/networkmap.conf --label=Subzone --label-color="#000000" --network-map-address=networkmap:8080 --network-parameters=config/params.conf`

{{< note >}}
You can update the Network Map admin address using a command like this: `./cenm network-map config set-admin-address -a=networkmap:8081`. If you have multiple sub-zones, you need to specify which sub-zone you are updating in the command.
{{< /note >}}

5. Set the Network Map configuration for a subzone (the entry `1` below comes from the response to the create-subzone command):

    `./cenm netmap config set -s 1 -f config/networkmap.conf --zone-token`

6. Set the Signing Service's external admin address. This must be the address that the gateway Gateway service uses to communicate with the Identity Manager:

    `./cenm signer config set-admin-address -a=signer:9087`

7. Set the Signing Service configuration last, as it depends on the first two service's locations for it to be complete:

    `./cenm signer config set -f config/signer.conf --zone-token`

8. Set up any notaries required for your network, and update your network parameters. This process includes steps you would follow for any **Flag Day** network update:

    a. Fetch the node info file from the notary.

    b. Upload the node info file to the Network Map - command: `cenm netmap upload-node-info -f nodeInfo`.

    c. Edit the network parameters configuration to add the notary to the list, specifying the path to the node info file from step b, and to set an update deadline in the near future. For example, 5 minutes from now.

    d. Update network parameters in the Network Map to include the notary information - command: `cenm netmap netparams update submit -p config/parameters.conf`.

    e. Advertise the network parameter update to the network - command: `cenm netmap netparams update advertise`.

    f. Fetch the unsigned network parameters - command: `cenm signer netmap netparams unsigned`.

    g. Sign the updated network parameters - command: `cenm signer netmap netparams sign -h <hash>`.

    h. Accept the update from inside the notary.

    i. Execute the network parameter updates - command: `cenm netmap netparams update execute`.

    j. Fetch the unsigned Network Map - command: `cenm signer netmap unsigned`.

    k. Sign the Network Map - command: `cenm signer netmap sign -h <hash>`.


### Get Help in the CLI

To access help and get the version number, use the following command structure:

`cenm [-hV] [COMMAND]`

**Options**

`h,--help`
See a list of available commands and descriptions.

`v, --version`
See the current version of the CLI you are using.

### Overview of available commands

You can use the CLI to:

* Update the password you use to access CENM services.
* Set up and switch between contexts - allowing you to perform tasks across multiple servers with minimum effort to switch between them.
* Perform tasks in Identity Manager.
* Access the Network Map.
* Manage zones.
* Perform tasks in Signing Services.

The main commands are:

`change-password`
Change your CENM password.

`context`
Login and logout of CENM service management.

`zone`
Commands for zone-service management.

`signer`
Signing commands.

`identity-manager`
Identity-manager management features.

`netmap`
Network-map management features.


## Define contexts and servers

Your interaction with CENM services through the CLI is managed by the Front-end Application for Remote Management (Gateway) service. This service handles security checks and HTTP translation during your session, and acts as a gateway between the CLI and CENM.

When you log in to each session, you specify the full endpoint address of the Gateway service instance you are accessing, for example: `http://10.230.41.12`. You do this using the argument `<server>` in the command line. This endpoint forms the **context** for your session.

Setting a context means that your session can last for the full session duration set in your [Auth Service](auth-service) configuration, without being interrupted by any natural time-outs in your CENM service. It also means you can switch between servers, like staging and production servers, simply by switching from one context alias to another.

In most commands in the CLI, you can specify the context you want to use with the command option:

`-c, --use-context=<useContext>`


### Aliases for contexts

If you work on multiple services, or need to access the same service using multiple contexts, you can use the CLI to create **context aliases**. This means you can switch between sessions and back again by switching aliases.


## Change your password

This command allows you to change the password you use to access your CENM services.

{{< attention >}}

If you have been allocated a new password by an administrator using the [User admin tool](user-admin.md), you must change it to something only you know. You must do this before you continue to use CENM services.

{{< /attention >}}

**Sample command structure**

`cenm change-password -n[=<newPassword>] -p[=<password>] -u=<username> <server>`

**Options**

`-n, --new-password[=<newPassword>]`
New password. Leave `-n` without a value to enter your password on the next line. This prevents your password being visible in the command line history.

``-p, --password[=<password>]``
Current password. Leave `-p` without a value to enter your password on the next line. This prevents your password being visible in the command line history.

``-u, --username=<username>``
Username for password based authentication.

**Arguments**

``<server>``
URL for the targeted CENM API Gateway - the Gateway service.


## Log in to a CENM session

When you log in to a CENM session using the CLI, you do so by setting the required **Context** for your session. This ensures you are able to stay logged in to the correct server address for the duration of your work.

For example, once you have accessed the correct server for the **Signing service**, making this address the fixed context means that you no longer need to specify the server address for your subsequent commands.

#### Options

**-a, --alias=<alias>**
Optionally sets an alias for this session.

This can be used for setting the 'current context' and logging out later on.

**-p, --password[=<password>]**
Password for password based authentication. Leave `-p` without a value to enter your password on the next line. This prevents your password being visible in the command line history.

**-s, --set-active-context**
Sets the active context to the configured url.

**-u, --username=<username>**
Username for password based authentication.

#### Arguments
**<server>**
Url for the targeted CENM API Gateway (Gateway).

### Example

`./cenm.sh context login http://localhost:8081 -u jenny-editor -p password`

{{< note >}}
If you leave the -p value blank, the CLI will ask you for your password in the next response. You can use this method if you do not wish your password to appear on your command line history.
{{< /note >}}

## Identity Manager commands

You can perform the following tasks:

* Configure the Identity Manager service.
* Manage certificate signing requests.
* Display the certificate path for a legal name.
* Manage certificate revocation requests.
* Get certificate revocation list and related details.
* Check connectivity to the identity-manager service.
* Display configured approval plugins.


### Set external address and configure Identity Manager

You can use the CLI to configure the following elements of the Identity Manager service for the context you are working on:

* Update the Identity Manager's service address.
* Retrieve the Identity Manager configuration.
* Update the Identity Manager's configuration.


### Update the Identity Manager's service address.

To update the service address of the Identity Manager, use the `set-admin-address` command. Changing the address of the Identity Manager service also means you can update the Context of the current session to match the new address.

When entering the address, you must enter `<host>-<port>`. The `port` value must be the same as the value for `adminListener` in the services configuration file. **[PLEASE CHECK THIS]**

**Sample command structure**

`cenm identity-manager config set-admin-address -a=<address> [-c=<useContext>] [-o=<outputType>]`

**Options**

`-a, --address=<address>`
The new address of the service, in the format `<host>:<port>`. The value for `port` must match the value for `adminListener` in the service configuration file.

`-c, --use-context=<useContext>`
Sets the context of the command to override the current context you are using.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`

### Retrieve the current Identity Manager configuration

Use the command `get` to retrieve the current Identity Manager configuration. You can specify the output type, and request a Zone token in place of the config file if required.

**Sample command structure**

`cenm identity-manager config get [--zone-token] [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command that overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty

Default value is `pretty`

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the 'pretty' output type.


### Update the Identity Manager's configuration

To update the configuration of the Identity Manager, you need to include a config file with the new settings. Then use the `set` command to update the Identity Manager.

**Sample command structure**

`cenm identity-manager config set [--zone-token] [-c=<useContext>] -f=<configFile> [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command. This overrides the current context set.

`-f, --config-file=<configFile>`
Configuration file.

`-o, <outputType>``
Specifies output format. Valid values are: json, pretty. Default value is pretty

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the 'pretty' output type.


### Manage Identity Manager certificate signing requests

You can use the CLI to see the **approved** and **pending** certificate signing requests for the Identity Manager service.

To see the requests for a different context to the one you are on, you need to specify the context you require.

{{< note >}}

Requesting certificate signing requests on a different context may trigger a request for login details. Make sure you have authorisation to access this context before entering the command.

{{< /note >}}

### Get the approved certificate signing requests

**Sample command structure**

`cenm identity-manager csr approved [-c=<useContext>] [-o=<outputType>]`

**Options**

``-c, --use-context=<useContext>``
Sets the context of the command - overrides the current context set.

``-o, <outputType>``
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

 ### Get the pending certificate signing requests

 **Sample command structure**

 `cenm identity-manager csr pending [-c=<useContext>] [-o=<outputType>]`

 **Options**

 `-c, --use-context=<useContext>`
 Sets the context of the command - overrides the current context set.

 ``-o, <outputType>``
 Specifies output format. Valid values are: json, pretty. Default value is `pretty`.


 ### Manage the Identity Manager certificate revocation list

 Identity certificates allow parties to access the network managed by CENM. Using the CLI, you can:

 * Submit a certificate revocation request.
 * Get the list of **approved** certificate revocation requests.
 * Get the list of **pending** certificate revocation requests.

 You can use the CLI to see the **approved** and **pending** certificate revocation requests for the Identity Manager service.

 To see the requests for a different context to the one you are on, you need to specify the context you require.

 {{< note >}}

 Requesting certificate signing requests on a different context may trigger a request for login details. Make sure you have authorisation to access this context before entering the command.

 {{< /note >}}

When making a request to revoke a certificate, you must provide *only one* of the following certificate identifiers:

* Request ID of the certificate being revoked.
* Legal name of the party whose certificate is being revoked.
* The serial ID of the certificate being revoked.

### Request the revocation of a certificate

To request that a certificate is revoked, you must provide a reason for the revocation, and one form of certificate identifier.

**Sample command structure**

`cenm identity-manager crr submit (-n=<legalName> | -i=<requestId> | -s=<serial>) [-c=<useContext>] -e=<reporter> [-o=<outputType>] -r=<reason>`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command that overrides the current context set.

`-e, --reporter=<reporter>`
Specifies the reporter who requested the certificate revocation.

`-o, <outputType>``
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

``-r, --reason=<reason>``
Reason for the revocation. Possible values:
* `UNSPECIFIED`
* `KEY_COMPROMISE`
* `CA_COMPROMISE`
* `AFFILIATION_CHANGED`
* `SUPERSEDED`
* `CESSATION_OF_OPERATION`
* `CERTIFICATE_HOLD`
* `UNUSED`
* `REMOVE_FROM_CRL`
* `PRIVILEGE_WITHDRAWN`
* `AA_COMPROMISE`

**Certificate identifiers**

Only use one certificate identifier per request.

`-i, --request-id=<requestId>`
Submits a CRR using the request id. Can only be present if serial and legal name not set

`-n, --legal-name=<legalName>`
Submits a CRR using the legal name. Can only be present if request id and serial not set

`-s, --serial=<serial>`
Submits a CRR using the certificate serial.

Can only be present if request id and legal name not set

### See a list of approved certificate revocation requests

**Sample command structure**

cenm identity-manager crr approved [-c=<useContext>] [-o=<outputType>]

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### See a list of pending certificate revocation requests

**Sample command structure**

cenm identity-manager crr pending [-c=<useContext>] [-o=<outputType>]

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

``-o, <outputType>``
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### See the certificate path for a legal name

You can check the location path of an Identity Manager certificate attached to any legal name in the network.

**Sample command structure**

`cenm identity-manager cert-path [-c=<useContext>] -n=<legalEntityName> [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-n, --legal-entity-name=<legalEntityName>`
The legal entity name of the certificate.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Get the certificate revocation list

**Sample command structure**

`cenm identity-manager crl get [-c=<useContext>] [-i=<issuer>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context you have set.

`-i, --issuer=<issuer>`
Issuer of the CRL to display.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Get list of issuers of the certificate revocation list

**Sample command structure**

`cenm identity-manager crl issuers [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

``-o, <outputType>``
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### See Identity Manager service status and available plugins

You can use the CLI to check your connection to the Identity Manager service, and see available plugins to the service.

### Check Identity Manager service status

**Sample command structure**

`cenm identity-manager status [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

``-o, <outputType>``
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Check available plugins for the Identity Manager service

**Sample command structure**

`cenm identity-manager plugins [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

``-o, <outputType>``
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

## Zone Service commands

You can use the CLI to perform the following tasks related to zone management:

`status`
To check your connectivity to the Zone Service.

`create-subzone`
To create a subzone.

`get-subzones`
To list all subzones.

`addresses`
To list all service addresses.

### Check connectivity to the Zone Service

**Sample command structure**

`cenm zone status [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Create a subzone

To create a subzone using the CLI, you need to provide:

* A config file to configure the settings for the new subzone.
* The Network Map address for the new subzone.
* The parameters for the network.

**Sample command structure**

`cenm zone create-subzone [--zone-token] [-c=<useContext>] --config-file=<networkMapConfigFile> --label=<label> --label-color=<labelColor> --network-map-address=<networkMapAddress> --network-parameters=<networkParameters> [-o=<outputType>]`

**Options**

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the 'pretty' output type.

`--config-file=<networkMapConfigFile>`
Network Map configuration file.

``--label=<label>``
Friendly name of the subzone.

`--label-color=<labelColor>`
The label color for the subzone. Must be in hex format, like #FFFFFF.

`--network-map-address=<networkMapAddress>`
Sets the address of the Network Map service. Must be in a format of `<hostname>:<port>`
The port should be the same as the one set for the adminListener in the network-map config.

`--network-parameters=<networkParameters>`
Initial network parameters.

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Get a list of existing subzones

You can use the CLI to get a list of existing subzones and their basic details.

**Sample command structure**

`cenm zone get-subzones [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Get a list of all service addresses in a subzone

You can find the addresses of all the services on a specified subzone. If you only have access to one subzone, you do not need to specify the subzone option in your command.

**Sample command structure**

`cenm zone addresses [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.


## Signing Service commands

You can use the CLI to perform the following tasks in the Signing Service:

* See the list of pending certificate signing requests.
* Get a full list of unsigned certificate revocation requests.
* Sign Identity Manager certificates.
* See pending Identity Manager certificate revocation requests.
* Sign certificate revocation requests.
* Get a list of unsigned network parameters.
* Sign network parameters.
* Get subzone material detailing parameters of a network.
* See unsigned Network Map data.
* Sign Network Map.
* Set the Signing Service address.
* Get the Signing Service configuration details.
* Configure the Signing Service.
* Check your connectivity to the Signing Service.
* List all signers currently configured.
* Get zone material relating to the Signing Service.


### See a list of outstanding certificate signing requests

**Sample command structure**

`cenm signer csr list [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Sign an Identity Manager certificate

When you sign Identity Manager certificate requests using the CLI, you  need to include the ID of the request you are signing.

**Sample command structure**

`cenm signer csr sign [-c=<useContext>] [-o=<outputType>] REQUEST_ID`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

**Arguments**

`REQUEST_ID`
The ID of the request you wish to sign.

### Sign an Identity Manager certificate revocation request

When using the CLI to sign a certificate revocation request, you have the option to update the list of revoked certificates. If you keep a list, you should always use this option to ensure your list remains up to date.

**Sample command structure**

`cenm signer crl sign [-c=<useContext>] [-h=<crlHash>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-h, --crl-hash=<crlHash>`
Hash of the CRL to be appended or empty if non exists.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Get a list of certificate revocation requests

**Sample command structure**

`cenm signer crl get [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### See pending Identity Manager certificate revocation requests

**Sample command structure**

`cenm signer crl crrs [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Sign network parameters

**Sample command structure**

`cenm signer netmap netparams sign [-c=<useContext>] -h=<hash> [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-h, --crl-hash=<crlHash>`
Hash of the network parameters to be signed.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Get a list of unsigned network parameters

**Sample command structure**

`cenm signer netmap netparams unsigned [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Sign a Network Map

**Sample command structure**

`cenm signer netmap sign [-c=<useContext>] -h=<hash> [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-h, --crl-hash=<crlHash>`
Hash of the Network Map to be signed.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Get subzone material for a Network Map

**Sample command structure**

`cenm signer netmap material [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### See unsigned Network Map data

**Sample command structure**

`cenm signer netmap unsigned [--node-infos] [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`--node-infos`
Allows you to print a list of node info from the Network Map.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Configure the Signing Service

To configure the Signing Service, you must include a configuration file with the correct configuration data.

**Sample command structure**

`cenm signer config set [--zone-token] [-c=<useContext>] -f=<configFile> [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-f, --config-file=<configFile>`
Configuration file.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the `pretty` output type.

### Set the address of the Signing Service

**Sample command structure**

`cenm signer config set-admin-address -a=<address> [-c=<useContext>] [-o=<outputType>]`

**Options**

`-a, --address=<address>`
The new address of the service, in the format `<host>:<port>`. The value for `port` must match the value for `adminListener` in the service configuration file.

`-c, --use-context=<useContext>`
Sets the context of the command to override the current context you are using.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### See the Signing Service configuration

**Sample command structure**

`cenm signer config get [--zone-token] [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the `pretty` output type.

### Check the connection status of the Signing Service

**Sample command structure**

`cenm signer status [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### See a list of configured signers

**Sample command structure**

`cenm signer list [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### Get zone material for the signing service

**Sample command structure**

`cenm signer zone-material [-c=<useContext>] [-o=<outputType>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

## Network Map service commands

You can use the CLI to perform the following tasks on Network Map services:

* Get network parameters.
* Update network parameters.
* Get the current Network Map configuration.
* Get the label data for a subzone.
* Update the configuration of a Network Map.
* Set the address of a Network Map.
* Update the labels for a Network Map.
* Check the connection status of the Network Map service.
* Get the current Network Map data.
* See a list of available node information.
* Upload new node information to a Network Map.

### Get network parameters

**Sample command structure**

`cenm netmap netparams get [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Submit a new network parameters update

To create a new parameters update, you must submit it to the Zone Service database. It can then be **Advertised**, and then **Executed** when the changes are brought into effect.

When using this command, you must include the new parameters using the option described below.

**Sample command structure**

`cenm netmap netparams update submit [-c=<useContext>] [-o=<outputType>] -p=<networkParameters> [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-p, --network-parameters=<networkParameters>`
Updated network parameters.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Advertise pending network parameter changes

You can use the CLI to advertise upcoming changes to network parameters across the network.

**Sample command structure**

`cenm netmap netparams update advertise [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Cancel pending network parameter changes

Use this command to remove network parameter changes from the pending list. Canceled pending network parameter changes can no longer be executed and brought into effect.

**Sample command structure**

`cenm netmap netparams update cancel [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Execute network parameters update - triggering a **Flag day**.

When you execute pending changes to the network parameters, it triggers a **Flag day**. This causes all nodes in the network to shut down. On restart, they can accept the new network parameters and continue operating.

**Sample command structure**

`cenm netmap netparams update execute [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Get the status of a network parameters update

**Sample command structure**

`cenm netmap netparams update status [--accepted] [-c=<useContext>] -h=<parameterHash> [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`--accepted`
Add this option to see a list of nodes that accepted the change. To see a list of nodes that have not yet accepted, do not include this option.

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-h, --crl-hash=<crlHash>`
Hash of the network parameter.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

### See pending network parameter update

**Sample command structure**

`cenm netmap netparams update pending [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### See the latest update stored in the Zone Service

**Sample command structure**

`cenm netmap netparams update get [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Get the current Network Map configuration

**Sample command structure**

`cenm netmap config get [--zone-token] [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the `pretty` output type.

### See the current Network Map label data

Use this command to see the assigned label data used in the current Network Map configuration.

**Sample command structure**

`cenm netmap config get-label [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Update the Network Map configuration

To update the Network Map configuration with the CLI, you must include a new config file as one of the options in the command.

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-f, --config-file=<configFile>`
Configuration file.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the `pretty` output type.

### Update the address of the Network Map

**Sample command structure**

`cenm netmap config set-admin-address -a=<address> [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-a, --address=<address>`
The new address of the service, in the format `<host>:<port>`. The value for `port` must match the value for `adminListener` in the service configuration file.

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-f, --config-file=<configFile>`
Configuration file.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the `pretty` output type.

### Update the Network Map label data

**Sample command structure**

`cenm netmap config set-label [-c=<useContext>] --label=<label> --label-color=<labelColor> [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

``--label=<label>``
Friendly name of the subzone.

`--label-color=<labelColor>`
The label color for the subzone. Must be in hex format, like #FFFFFF.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

`--zone-token`
Indicates that the zone token should be printed instead of the config, when using the `pretty` output type.

### Check the connection status of the Network Map service

**Sample command structure**

`cenm netmap status [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### See the node info for the Network Map

**Sample command structure**

`cenm netmap node-infos [-c=<useContext>] [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.

### Add node information to the Network Map

To upload node info to the Network Map, you must include an updated **Node Info file**.

**Sample command structure**

`cenm netmap upload-node-info [-c=<useContext>] -f=<nodeInfoFile> [-o=<outputType>] [-s=<subzoneId>]`

**Options**

`-c, --use-context=<useContext>`
Sets the context of the command - overrides the current context set.

`-f, --node-info-file=<nodeInfoFile>`
A file containing the new node information.

`-o, <outputType>`
Specifies output format. Valid values are: json, pretty. Default value is `pretty`.

`-s, --subzone-id=<subzoneId>`
Sets which subzone to operate on. If you are operating on just one subzone you do not need to include this option.
