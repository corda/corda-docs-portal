---
aliases:
- /config-ssl.html
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
    Path to the location of the keystore `.jks` - must be a fully resolvable path.


    * **password**:
    Password for the keystore.


    * **keyPassword**:
    *(Optional)* Password for the key pair - can be omitted if it is the same as the keystore password.




  * **trustStore**:
  *(Optional)* If a unique trust root is used (where all SSL keys are signed by a common root), then this keystore must contain the certificate representing the public key of
  that root. The `keyStore` configured above will contain a key pair signed by the root. Can be omitted if a single certificate and key pair is being used or the trust root certificate
  has been added to the `keyStore`.
    * **location**:
    Path to the location of the key store `.jks` - must be a fully resolvable path.


    * **password**:
    *(Optional)* Password for the truststore, will inherit the keyStore password if not set.
