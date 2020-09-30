---
aliases:
- /crl-endpoint-check-tool.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-crl-endpoint-check-tool
    parent: cenm-1-4-tools-index
    weight: 1060
tags:
- crl
- endpoint
- check
- tool
title: CRL Endpoint Check Tool
---


# CRL Endpoint Check Tool



## Overview

The CRL Endpoint Check Tool allows users to check health of CRL distribution endpoints in a given keystore. User
provides keystore file’s path and password. It iterates through all alias names in the keystore and their certificate
hierarchies. For each certificate it first checks whether it contains a CRL endpoint. If there is one, the tool
attempts to connect to it and retrieve the CRL. Upon receiving this information, a formatting check is performed and
the revocation list’s update time is logged to console. Detailed information on certificates and their CRLs is
available in the log files.


## Using the CRL Endpoint Check Tool

The CRL Endpoint Check tool resides in the `crlendpointchecktool.jar`. It is run by the following command:

```bash
java -jar crlendpointchecktool.jar --keystore=<keystore-file> --password<keystore-password>
```

On success you should see a console message similar to:

```bash
Listing certificates' CRLs under cordaclientca alias:
 O=PartyA, L=London, C=GB
    Contacting http://localhost:10000/certificate-revocation-list/doorman CRL endpoint...
    - Next update: Fri Jan 10 15:50:13 GMT 2020
    Please re-sign CRL, update deadline has passed
 C=US, L=New York, O=R3 HoldCo LLC, OU=Corda, CN=Test Identity Manager Service Certificate
    Contacting http://localhost:10000/certificate-revocation-list/subordinate CRL endpoint...
    - Next update: Sat Jan 05 10:47:37 GMT 2030
 C=US, L=New York, O=R3 HoldCo LLC, OU=Corda, CN=Test Subordinate CA Certificate
    Contacting http://localhost:10000/certificate-revocation-list/root CRL endpoint...
    - Next update: Sat Jan 05 10:47:37 GMT 2030
 C=US, L=New York, O=R3 HoldCo LLC, OU=Corda, CN=Test Root Certificate
    - No CRL endpoints provided for given certificate
 ------------------------
 Listing certificates' CRLs under identity-private-key alias:
 O=PartyA, L=London, C=GB
    - No CRL endpoints provided for given certificate
 O=PartyA, L=London, C=GB
    Contacting http://localhost:10000/certificate-revocation-list/doorman CRL endpoint...
    - Next update: Fri Jan 10 15:50:13 GMT 2020
    Please re-sign CRL, update deadline has passed
 C=US, L=New York, O=R3 HoldCo LLC, OU=Corda, CN=Test Identity Manager Service Certificate
    Contacting http://localhost:10000/certificate-revocation-list/subordinate CRL endpoint...
    - Next update: Sat Jan 05 10:47:37 GMT 2030
 C=US, L=New York, O=R3 HoldCo LLC, OU=Corda, CN=Test Subordinate CA Certificate
    Contacting http://localhost:10000/certificate-revocation-list/root CRL endpoint...
    - Next update: Sat Jan 05 10:47:37 GMT 2030
 C=US, L=New York, O=R3 HoldCo LLC, OU=Corda, CN=Test Root Certificate
    - No CRL endpoints provided for given certificate
 ------------------------
```
