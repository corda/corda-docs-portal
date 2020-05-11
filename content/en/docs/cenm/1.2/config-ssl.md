---
aliases:
- /releases/release-1.2/config-ssl.html
- /docs/cenm/head/config-ssl.html
- /docs/cenm/config-ssl.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- config
- ssl
title: SSL Settings
---


# SSL Settings

SSL Can be configured at both the client and listener ends of the CENM stack. The presence of the SSL
configuration entity will enable the use of SSL communication between the two parties


* **ssl**:
SSL settings


* **keyStore**:
The services keystore location.


* **location**:
Where the keystore (jks) is, must be a fully resolvable path.


* **password**:
Password for the keystore


* **keyPassword**:
*(Optional)* Password for the keypair, can be omitted if the same as the keystore.




* **trustStore**:
*(Optional)* If a unique trust root is being used, i.e. all SSL Keys are signed by a commonroot, then this keystore needs to contain the certificate representing the public key of
that root. The `keyStore` configured above will contain a keypair signed by the root.Can be omitted if a single certificate and keypair is being used or the trust root certificate
has been added to the `keyStore`
* **location**:
Where the keystore (jks) is, must be a fully resolvable path.


* **password**:
*(Optional)* Password for the truststore, will inherit the keyStore password if not set
