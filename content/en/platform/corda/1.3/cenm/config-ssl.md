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

You can configure SSL at both the client and listener ends of the CENM stack. The presence of the SSL
configuration entity enables the SSL communication between the two parties.

{{< note >}}
When you enable SSL between two CENM components, the connection between them is mutually authenticated.
{{< /note >}}


* **ssl**:
SSL settings.


  * **keyStore**:
  The services `keyStore` location.


    * **location**:
    Path to the location of the `keyStore` `.jks` - must be a fully resolvable path.


    * **password**:
    Password for the `keyStore`.


    * **keyPassword**:
    *(Optional)* Password for the key pair - can be omitted if it is the same as the `keyStore` password.


  * **trustStore**:
  *(Optional)* If a unique trust root is used (where all SSL keys are signed by a common root), then this `keyStore` must contain the certificate representing the public key of
  that root. The `keyStore` configured above contains a key pair signed by the root. Can be omitted if a single certificate and key pair is being used or the trust root certificate
  has been added to the `keyStore`.

    * **location**:
    Path to the location of the `keyStore` `.jks` - must be a fully resolvable path.


    * **password**:
    *(Optional)* Password for the `trustStore`. If not set, inherits the `keyStore` password.
