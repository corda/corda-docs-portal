---
aliases:
- /releases/release-1.0/tool-certificates-validator.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-tool-certificates-validator
    parent: cenm-1-0-tools-index
    weight: 1020
tags:
- tool
- certificates
- validator
title: Certificates Validator
---


# Certificates Validator

The purpose of the Certificates Validator Tool is to provide means for the certificate hierarchy verification.
The verification is tailored towards Corda Platform and as such some proprietary checking is done in order to ensure correctness
for the Corda Network deployment.
The tool is intended to be executed automatically. Therefore no human interaction is required. All necessary data is fed
to the tool from the provided configuration file. See below for more details on how to configure the tool.

Performed validation:


* The network trust store consists of at least one certificate (i.e. the root certificate).
* There is certificate is stored under the “cordarootca” alias. Note: This is required for Corda releases: 3.2 OS and 3.3 ENT.
* The certificate under the “cordarootca” is self-signed.
* The are certificates with roles: DOORMAN_CA and NETWORK_MAP that share the same root certificate.


## Running the tool

```bash
java -jar utilities.jar certs-validator --config-file <CONFIG_FILE>
```


## Configuration Parameters

The configuration file consists the following attributes:


* **certificatesStore**: 
Certificates store specific configuration.


* **file**: 
Location of the certificates store file.


* **password**: 
Password to the certificates store file.




* **networkRootTrustStore**: 
Network trust store specific configuration.


* **file**: 
Location of the network trust store file.


* **password**: 
Password to the network trust store file.






## Example Configuration

```guess
certificatesStore {
    file = "./certificateStore.jks"
    password = "password"
}
networkRootTrustStore {
    file = "./network-root-truststore.jks"
    password = "trustpass"
}
```

