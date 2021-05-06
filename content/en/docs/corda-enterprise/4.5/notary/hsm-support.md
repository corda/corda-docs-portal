---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-notaries
tags:
- hsm
- support
title: HSM support for Notaries
weight: 3
---

# HSM support for notaries

## Overview

![hsm support](../resources/hsm-support.png "hsm support")
Two notary workers and their relevant cryptographic keys used for P2P messaging and transaction signing. The red rectangles represent the
Corda notary worker services. The distinct identity keys are represented by rectangles in green and yellow and the shared key of the
notary service identity is drawn in blue. Their cryptographic keys are held in a single HSM.



{{< warning >}}
As noted in the above diagram, if the workers are sharing a HSM then this should be setup in a highly available configuration. Using a
single non-HA HSM in a CFT notary cluster will introduce a single point of failure and is strongly discouraged. If a HA HSM configuration
is not possible then see the below section on [Using Multiple HSMs](#using-multiple-hsms) for how to setup one HSM per worker node.

{{< /warning >}}


Each Notary workers needs access to three private key entries, corresponding to following entities:



* The distributed Notary identity, responsible for notarising transactions.
* The node certificate authority, responsible for issuing the legal identity and TLS certificates.
* The node legal identity, which represents the unique identity of the notary worker.


See the *enterpriseConfiguration* section of the corda-configuration-file doc for more information on how to configure each alias.
When the private keys are stored in a HSM, only the certificates are stored in the keystore file.

The associated certificates for the distributed notary identity and node certificate authority are issued by the Identity Manager on the
network. See [https://docs.cenm.r3.com](https://docs.cenm.r3.com) for more information. The legal identity certificate is issued by the node certificate authority.

The worker specific legal identity key pair is used for P2P messaging, whereas the single distributed notary identity key pair is used by
all the notary workers of the CFT notary cluster to sign valid transactions. During operation, each notary worker will access the HSM and
use the distributed notary key when processing notarisation requests.

For information on which HSMs are supported by Corda Enterprise, see the [platform support matrix](../platform-support-matrix.md).
Please read the section below for setup instructions and [configuration details](../node/operating/cryptoservice-configuration.md/).


## Detailed instructions to deploy to Azure Key Vault

These instructions assume that a single Azure Key Vault is being used across all notary workers.

Add the following entries to your workers node.conf files, replacing the placeholders with the relevant/chosen values:

```sh
cryptoServiceName: "AZURE_KEY_VAULT"
cryptoServiceConf: "<path to the crypto service configuration file>"
cryptoServiceTimeout: "<the desired timeout, default: 1s>"
enterpriseConfiguration {
  identityKeyAlias: "<CUSTOM_WORKER_IDENTITY_KEY_ALIAS>"
  clientCaKeyAlias: "<CUSTOM_WORKER_CA_KEY_ALIAS>"
  distributedNotaryKeyAlias: "<CUSTOM_DISTRIBUTED_KEY_ALIAS>" # optional - can omit to use default
}
```

{{< note >}}
In order to use the same Keyvault across notary workers, distinct values for
the *identityKeyAlias* and *clientCaKeyAlias* settings must be used for each
worker. Otherwise the key aliases will clash in the Keyvault.

{{< /note >}}
Create a crypto service config file with the following content:

```sh
path: <path to saved pkcs12 file>
alias: "1"
password: "<password used in the key vault creation>"
keyVaultURL: "https://<key vault name>.vault.azure.net/"
clientId: "<app id from creation of the service principle>"
protection: "SOFTWARE" # HARDWARE can be specified if using a premium vault
```

When the configuration files are ready, register the notary service identity using the notary registration tool and any worker’s node.conf
file:

```sh
java -jar ha-utilities notary-registration \
     --config-file=node.conf \
     --network-root-truststore=<trust store> \
     --network-root-truststore-password=<password>
```

After successful registration, a keystore file is created by the tool in `certificates/nodekeystore.jks` this keystore contains the
service identity certificate that all notary workers of this notary cluster share. Copy the file before registering the individual identity
of the notary, to be able to distribute the file to all other notary workers.

```sh
cp certificates/nodekeystore.jks notary-service-keystore.jks
```

Register the individual identity of the notary using the Corda jar and the following command:

```sh
java -jar corda.jar initial-registration \
    --network-root-truststore-password=<password> \
    --network-root-truststore=<trust store>
```

To register a second notary worker, copy the `notary-service-keystore.jks` to the certificates directory of the next notary worker as
`certificates/nodekeystore.jks` and repeat the above command.


## Using Multiple HSMs

A highly-available HSM can be shared between notary workers in the current version of Corda, however each worker needs to be configured
to use a unique alias for the identity and client ca key. See the *enterpriseConfiguration* section of the corda-configuration-file
doc for more information on how to configure this.

If custom aliases have not been configured then, as each worker will attempt to create their identity and CA keys using the default alias,
separate HSMs must be used. Also, as noted above, if a HA HSM is not available then each worker should be setup with its own HSM.

When a “one HSM per worker” setup is being used, the distributed notary service signing key has to be copied between the HSMs to ensure
that each worker has access to it. As a consequence, your HSM of choice needs to provide a secure mechanism to copy keys between HSM instances.

{{< note >}}
A single Corda node (including notary workers) can not be configured to utilise more than one HSM in the current version.

{{< /note >}}
