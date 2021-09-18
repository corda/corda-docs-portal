---
aliases:
- /releases/release-1.1/config-network-map-parameters.html
- /config-network-map-parameters.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-1:
    identifier: cenm-1-1-config-network-map-parameters
    parent: cenm-1-1-configuration
    weight: 230
tags:
- config
- network
- map
- parameters
title: Network Map Configuration Parameters
---


# Network Map Configuration Parameters

Configuration reference for the Network Map Service


* **address**:
The host and port on which the service runs


* **database**:
See [CENM Database Configuration](config-database.md)


* **shell**:
*(Optional)*  See [Shell Configuration Parameters](config-shell.md)


* **enmListener**:
Details on how the service will communicate with the rest of the ENM deployment.


* **port**:
Port that the service will bind to and other ENM components will connect to.


* **verbose**:
*(Optional)* Enables verbose logging for the socket layer


* **reconnect**:
Whether a client should be attempt to reconnect if the connection is dropped.


* **ssl**:
See [SSL Settings](config-ssl.md)




* **privateNetworkAutoEnrolment**:
To enable nodes to be automatically enrolled in a private network this must
be set to true. Setting it to false will result in all nodes being added
to the public zone and require manual movement into the private network
desired. Setting to true requires communication with the Identity Manager
to be in place to allow the Netowrk Map to interogate it as to which,
if any, private network a ndoe should be put in.


* **checkRevocation**:
If set to true then the Network Map will check with the Identity Manager’s revocation
service weather the registering node is revoked.


* **pollingInterval**:
How often nodes registering with the network map should check back for new entries.


* **identityManager**:
details where the issuance service is on the network


* **host**:
Which host  the Identity Manager is running on


* **port**:
To which port it’s enmListener is bound


* **ssl**:
See [SSL Settings](config-ssl.md)




* **revocation**:
details where the revocation service is on the network


* **host**:
Which host  the Identity Manager is running on


* **port**:
To which port it’s enmListener is bound


* **ssl**:
See [SSL Settings](config-ssl.md)




* **localSigner**:
*(Optional)* Configuration of the local signer for the Identity Manager service. Useful for debug, testing orwhen HSM support is not available.
* **keyStore**:
Configuration for key store containing the Identity Manager key pair.


* **file**:
Path to the key store file containing the signing keys for the Identity Manager service.


* **password**:
Key store password.




* **keyAlias**:
Key alias under which the key can be found in the key store.


* **keyPassword**:
Password for the ‘keyAlias’ key entry within the key store.


* **signInterval**:
How often the signing process should be triggered (in milliseconds).


* **timeout**:
*(Optional)* The maximum time allowed for execution of the signing process (in milliseconds). Defaults
to 30 seconds. If the timeout threshold is reached then the signing process will be aborted and wait
before retrying. The wait time after each failure is determined by an exponential backoff strategy.


* **crlDistributionUrl**:
*(Optional)* REST endpoint under which the certificate revocation list issued by Identity Manager can be obtained.
It is needed as this URL is encoded in certificates issued by Identity Manager.





