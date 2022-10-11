---
title: "Setting up SSL encryption"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-operating
    identifier: corda-5-dev-preview-1-nodes-operating-ssl-encryption
    weight: 4200
section_menu: corda-5-dev-preview
description: >
  How to set up SSL encryption for HTTP-RPC.
---

Use this guide to set up SSL encryption for HTTP-RPC by:
1. [Obtaining an SSL certificate](#obtain-an-ssl-certificate).
2. <a href="#add-ssl-configuration-to-nodeconf">Adding SSL configuration to `node.conf`</a>.

Corda's HTTP-RPC API supports HTTP and HTTPS. Use HTTPS wherever possible as it's more secure—the connection between the
server and client is encrypted using Transport Layer Security (TLS). An exception to this may be in a dev environment where
you need to inspect the network traffic. However, tooling to do this for HTTPS is available.

{{< warning >}}

Never run a node that is exposed to the internet without configuring SSL encryption.

{{< /warning >}}

You should configure SSL encryption for your node to ensure secure communication between the server and client. If you don't, its RPC API is vulnerable to attacks inherent to the HTTP protocol,
even if [authentication](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/authentication/authentication.md) is properly configured. For example, motivated actors with access to
network traffic will be able to:
* Obtain legitimate users' credentials (when basic authentication is in place).
* Impersonate a legitimate user by stealing their authentication tokens (though their actual credentials are not exposed)(when Azure Active Directory is in place).

Even nodes used in a dev environment can potentially expose users' credentials. For example, if employees don't use a dedicated password for the API when accessing their node via the public internet.

Due to the security implications, Corda requires a valid SSL configuration when `devMode` is set to `false` in `node.conf`.

## Obtain an SSL certificate

There are several ways you can obtain an SSL certificate:
* From a public Certificate Authority (CA), such as [IdenTrust](https://www.identrust.com), [DigiCert](https://www.digicert.com), and [GoDaddy](https://www.godaddy.com).
* From your organization's internal CA.
* By [creating a self-signed certificate](#create-a-self-signed-certificate-for-development) (not for use in a production environment).

### Create a self-signed certificate for development

A self-signed certificate is signed with its own private key, rather than by another certificate
(usually held by a CA). Although this makes it easy to create, it lacks the security benefits of a CA-signed certificate.
For example, since there is no proof of origin provided by a separate signer, anyone with basic technical skills could
create their own 'fake', cryptographically correct certificate which makes the same claims as another. Therefore, a
connection to a server cannot be deemed secure based on a self-signed certificate as the certificate's proof of origin cannot
be verified.

{{< warning >}}

You should not use a self-signed certificate in a production environment.

{{< /warning >}}

There may, however, be scenarios where a self-signed certificate is useful:
* For testing configuration.
* During development. For example, using (unencrypted) network traffic between the server and client for troubleshooting.
* When operating in special circumstances. For example, a company intranet with no public network connection. However, the preference is to use a properly configured certificate hierarchy.

Consult your organization's security division for further guidance.

Assuming Java is installed on your machine (either JRE or JDK, runtime or developer kit), you can use <a href="https://docs.oracle.com/cd/E54932_01/doc.705/e54936/cssg_create_ssl_cert.htm#CSVSG178">`keytool`</a> to create a self-signed certificate. `keytool` will prompt you to provide information about the **subject** of the certificate (the node you are configuring). Make sure to enter the name of your node when prompted: `What is your first and last name?`.

In this example, a self-signed certification is created using `keytool`:

```console
farm@JUGGERNAUT:~/git/engineering-kb$ keytool -genkey -keyalg RSA -keysize 2048 -keystore keystore.jks -storepass ThisIsntSecure -validity 360
What is your first and last name?
  [Unknown]:  Sample Node
What is the name of your organizational unit?
  [Unknown]:  Production Operations
What is the name of your organization?
  [Unknown]:  Contoso LLC
What is the name of your City or Locality?
  [Unknown]:  Paris
What is the name of your State or Province?
  [Unknown]:
What is the two-letter country code for this unit?
  [Unknown]:  FR
Is CN=Sample Node, OU=Production Operations, O=Contoso LLC, L=Paris, ST=Unknown, C=FR correct?
  [no]:  y
```

To create your own self-signed certificate, you need to adapt these arguments in the command from the previous example:
* `keyalg` specifies which cryptographic algorithm to use. If you don't have a preference, `RSA` is a good option.
* `keysize` specifies the size of the cryptographic keys that will be generated. The recommended baseline option is `2048`.
* `keystore` specifies the path to the output file, including file name. You need to include this in `node.conf`.
* `storepass` specifies the password of the output file. You need to include this in `node.conf` as `keystore-password`.
* `validity` specifies the number of days from issuing the command to when the certificate expires.

## Add SSL configuration to `node.conf`

Once you have obtained a certificate, place it into a directory that the node can access. Then add this section to your node's `node.conf` file, under `httpRpcSettings`:

```
"ssl": {
  "keyStorePath": "/path/to/keystore/https.keystore",
  "keyStorePassword": "keystore-password"
}
```

For more information, read <a href="configure-nodeconf.md">how to configure `node.conf` for HTTP-RPC</a>.
