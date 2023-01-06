---
aliases:
- /releases/4.2/running-a-notary-cluster/hsm-support.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-hsm-support
    parent: corda-enterprise-4-2-toctree
    weight: 1080
tags:
- hsm
- support
title: HSM Support
---


# HSM Support


## Overview


![hsm support](/en/hsm-support.png "hsm support")
Two notary workers and their relevant cryptographic keys used for P2P
messaging and transaction signing. The red rectangles represent the Corda
notary worker services. The distinct identity keys are represented by
rectangles in green and yellow and the shared key of the notary service
identity is drawn in blue. Their cryptographic keys are held in two HSMs.


Notary workers hold three private key entries in their keystore.



* *cordaclientca*, the node certificate authority, issuing the legal identity and TLS keys.
* *identity-private-key*, the legal identity used to sign transactions.
* *distributed-notary-private-key*, used to notarise transactions.


The *cordaclientca* and *distributed-notary-private-key* are issued by the
Identity Manager of the Enterprise Network Map, see [https://docs.corda.net](https://docs.corda.net).
The *cordaclientca* is issuing the *identity-private-key*.

The *identity-private-key* is used for P2P messaging, whereas a single
*distributed-notary-private-key* is used by all the notary workers of the CFT
notary cluster to sign valid transactions. The *distributed-notary-private-key*
can be copied to all notary workers, or a single highly available HSM can be
used to hold the key. This HSM is then accessed by all the notary workers for
transaction signing.

{{< note >}}
A highly-available HSM can not be shared between notary workers in the
current version of Corda, since the alias of the *identity-private-key* is
not configurable and all the worker nodes have distinct identity keys. During
setup, all the workers will attempt to create a key under this alias, leading
to an error. The Corda node can not be configured to utilise more than one
HSM in the current version.

{{< /note >}}
See the certificates-hierarchy design doc for more information on the key hierarchies used by Corda.

At present the notary workers have to utilise distinct HSMs, all of which
hold a copy of the key of the service identity. This requires a mechanism to copy the
key from one HSM instance to the next, a feature that several HSM vendors implement.

Currently Corda Enterprise only supports Azure Key Vault. Please read the
section below for setup instructions.


## Detailed instructions to deploy to Azure Key Vault

Obtain one Azure Key Vault per notary worker. Other HSM types are not supported
at the moment.  Create a service principal and extract the *appId* from the
response of the Azure client utility and backup the private key to authenticate
your requests to the HSM. Give your principal permissions to access your
keyvault.

Add the following entries to your node.conf file

```sh
"cryptoServiceName": "AZURE_KEY_VAULT"
"cryptoServiceConf": "<path to the crypto service configuration file>"
```

Create a crypto service config file with the following content.

```sh
path: <path to saved pkcs12 file>
alias: "1"
password: "<password used in the key vault creation>"
keyVaultURL: "https://<key vault name>.vault.azure.net/"
clientId: "<app id from creation of the service principle>"
protection: "SOFTWARE"
```

When the configuration files are ready, register the notary service identity using
the notary registration tool.

```sh
java -jar notary-registration.jar register \
     --config-file=node.conf \
     --network-root-truststore=<trust store> \
     --network-root-truststore-password=<password>
```

After successful registration, a keystore file is created by the tool in *certificates/nodekeystore.jks* this keystore contains the service identity
key that all notary workers of this notary cluster share. Copy the file before registering the individual identity of the notary, to be able to
distribute the file to all other notary workers.

```sh
cp certificates/nodekeystore.jks notary-service-keystore.jks
```

Register the individual identity of the notary using the corda jar and the following command.

```sh
java -jar corda.jar initial-registration \
    --network-root-truststore-password=<password> \
    --network-root-truststore=<trust store>
```

To register a second notary worker, copy the *notary-service-keystore.jks* to
the certificates directory of the next notary worker as
*certificates/nodekeystore.jks* and repeat the above command.


### Troubleshooting

In case the tool returns an error code, you can obtain more information by providing the following log4j config file and updating the command line as shown below.

```xml
<?xml version="1.0" encoding="UTF-8"?>
  <Configuration status="INFO">
      <Loggers>
          <Logger name="notary-registration" additivity="false" level="INFO">
          <AppenderRef ref="RollingFile-Appender"/>
          </Logger>
      </Loggers>
 </Configuration>
```

Assuming you have stored the above snippet in a file named *notary-tool-log4j.xml* specify this file as the log4j config file to see the exception in the console as
shown below.

```sh
java -Dlog4j.configurationFile=notary-tool-log4j.xml \
     -jar notary-registration.jar register \
     --config-file=node.conf \
     --network-root-truststore=<trust store> \
     --network-root-truststore-password=<password>
```
