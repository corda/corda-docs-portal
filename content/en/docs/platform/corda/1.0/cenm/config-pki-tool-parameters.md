---
aliases:
- /releases/release-1.0/config-pki-tool-parameters.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- config
- pki
- tool
- parameters
title: Public Key Infrastructure (PKI) Tool Configuration Parameters
---


# Public Key Infrastructure (PKI) Tool Configuration Parameters


* **defaultPassword**: 
This password is going to be used whenever a password is required unless it is specified on a more granular level.


* **keyStores**: 

Specification of the key stores used by the PKI Tool. It is a map between the key store aliases and their
actual configurations.



* **file**: 
Key store file location. If the file does not exist it will be created automatically.
If it does exist and consist the keys with the same aliases as those specified in the `key` section configuration,
the generation process will skip those and reuse existing ones for any signing process.


* **password**: 
Key store password. If not specified, the password specified under the `defaultPassword` will be used.


* **host**: 
Host name (or IP address) of the HSM device.


* **port**: 
Port number of the HSM service.


* **users**: 
List of user authentication configurations. See below section on User Authentication Configuration.




* **certificatesStore**: 
Certificates store specific configuration.


* **file**: 
Certificate store file location. If the file does not exist it will be created automatically.


* **password**: 
Certificate store password. If not specified, the `defaultPassword` attribute is going to be used.




* **defaultKeyStores**: 
List of key store aliases corresponding to the key stores that are to store the generated keys in case
of them not being explicitly specified in the generated key configuration. This can be a list of multiple
aliases only in case of the local key stores. In case of the HSM key stores this list can hold only
a single element corresponding to the HSM key store. This is due to the fact that in case of the HSM key
stores, there is no notion of a key duplication to another HSM key store as the keys are generated in the HSM.
That does not hold in case of local key stores, where the keys are generated in memory and can be stored
in an arbitrary number of file-based key stores.


* **defaultCertificatesStores**: 
List of certificates store aliases corresponding to the certificates stores that are to store
generated certificates in case of them not being explicitly specified in the certificate configurations.


* **certificates**: 
Map between certificate aliases and their configurations.
If not specified, the key of the map will be used as the generated key alias, and also as the alias for the certificate.




## Certificate Configuration

Allowed parameters are:


* **key**: 
Configuration of the key that is going to be generated. This can be either Local of HSM configuration.
See corresponding configurations [Key Configuration (Local)](#key-configuration-local) and [Key Configuration (HSM)](#key-configuration-hsm)


* **signedBy**: 
Signing key alias. This is a shortcut parameter to reference the key that is already specified in the configuration.
Optional in case of self-signed certificates.


* **signingKey**: 
Full specification of the signing key. This is required when the signing key is not specified in the tool’s configuration.


* **alias**: 
Signing key alias.


* **password**: 
Signing key password. Applicable only if the signing key is in the local key store.


* **algorithm**: 
Signature algorithm for the certificate signing key. Default value: `SHA256withECDSA`.


* **group**: 
Key group under which the signing key is stored in the HSM. This is the Utimaco HSM name spacing concept.
See Utimaco docs for more details.


* **specifier**: 
Key specifier under which the signing key is stored in the HSM. This is the Utimaco HSM name spacing concept.
See Utimaco docs for more details. The default value is `1`.


* **keyStore**: 
Alias of the key store containing the signing key. This is used only in case of the HSM signing key specification.
In case of the local signing key, all the local key stores are queried for the key with the given alias.
If not specified, the *defaultKeyStores* will be used, with assumption that it consists the HSM key store alias.






* **isSelfSigned**: 
Flag denoting whether this certificate is self-signed. Default value depends on the `signer` field. If signer is defined then false, true otherwise.


* **includeIn**: 
List of aliases corresponding to the certificate stores in which the generated certificate should be stored.
If not specified the `defaultCertificatesStores` list will be used.


* **validDays**: 
How many days this certificate is valid. Default value: `7300`.


* **role**: 
Role of the certificate. Allowed value is either `DOORMAN_CA` or `NETWORK_MAP` or unspecified (default). Optional.


* **keyUsages**: 
Possible usages of the keys associated with the certificate (Optional). This is an array of values from the following set:



* `DIGITAL_SIGNATURE`,
* `NON_REPUDIATION`,
* `KEY_ENCIPHERMENT`,
* `DATA_ENCIPHERMENT`,
* `KEY_AGREEMENT`,
* `KEY_CERT_SIGN`,
* `CRL_SIGN`,
* `ENCIPHER_ONLY`,
* `DECIPHER_ONLY`


Default value: [`DIGITAL_SIGNATURE`, `KEY_CERT_SIGN`, `CRL_SIGN`].


* **keyPurposes**: 
Possible extended usages of the keys associated with the certificate (Optional).
This is an array of values from the following set:



* `ANY_EXTENDED_KEY_USAGE`,
* `SERVER_AUTH`,
* `CLIENT_AUTH`,
* `CODE_SIGNING`,
* `EMAIL_PROTECTION`,
* `IPSEC_END_SYSTEM`,
* `IPSEC_TUNNEL`,
* `IPSEC_USER`,
* `IPSEC_TIME_STAMPING`,
* `OCSP_SIGNING`,
* `DVCS`,
* `SBGP_CERT_A_A_SERVER_AUTH`,
* `SCVP_RESPONDER`,
* `EAP_OVER_PPP`,
* `EAP_OVER_LAN`,
* `SCVP_SERVER`,
* `SCVP_CLIENT`,
* `IPSEC_IKE`,
* `CAPWAP_AC`,
* `CAPWAP_WTP`


Default value: [`SERVER_AUTH`, `CLIENT_AUTH`].


* **issuesCertificates**: 
Boolean flag indicating whether the subject is a certificate authority. Default value: `true`.


* **cpsUrl**: 
Certificate policies URL (Optional).


* **authorityAccessInfo**: 
Configuration of the Authority Access Info extension (Optional).


* **ocspUrl**: 
On-line Certificate Status Protocol responder URL.


* **issuerCertUrl**: 
Issuer’s certificate URL (Optional).




* **subject**: 
X500 name of the authority owning the key.


* **crl**: 
Certificate revocation list specific configuration.


* **validDays**: 
Validity period of the certificate revocation list. Default value: `3650`.


* **crlDistributionUrl**: 
Certificate revocation list distribution URL.


* **indirectIssuer**: 
Flag denoting whether the certificate revocation list has been issued by the certificate issuer or not.
Default value: false (meaning that the certificate issuer is also the issuer of the certificate revocation list).


* **filePath**: 
Location of the file where the encoded bytes of the certificate revocation list are to be stored.


* **revocations**: 
List of revocation data (Optional).


* **certificateSerialNumber**: 
Serial number of the revoked certificate.


* **dateInMillis**: 
Certificate revocation time.


* **reason**: 
Reason for the certificate revocation. The allowed value is one of the following:


`KEY_COMPROMISE`,
`CA_COMPROMISE`,
`AFFILIATION_CHANGED`,
`SUPERSEDED`,
`CESSATION_OF_OPERATION`,
`PRIVILEGE_WITHDRAWN`







* **crlDistributionUrl**: 
Certificate revocation list distribution URL. This attribute overwrites the crlDistributionUl in the parent CRL configuration.
This is useful in case when the signer of the certificate is not specified in the tool’s configuration
file but still the CRL distribution needs to be configured.


* **crlIssuer**: 
Certificate revocation list issuer (given in the X500 name format). This attribute overwrites the issuer of the certificate.
This is useful in case when the signer of the certificate is not specified in the tool’s configuration
file but still the CRL distribution needs to be configured.




## Key Configuration (HSM)

Allowed parameters are:


* **key**: 
Configuration of the key that is going to be generated (HSM key). Optional.


* **group**: 
Key group under which the key is going to be generated. This is the Utimaco HSM name spacing concept.
See Utimaco docs for more details. Default value: `PKI.TOOL.DEFAULT.HSM.GROUP`.


* **specifier**: 
Key specifier under which the key is going to be generated. This is the legacy Utimaco HSM name spacing concept.
See Utimaco docs for more details. Default value: `1`.


* **alias**: 
Key alias under which the key is going to be stored. If not specified the key of the *certificates* map will be used. See above.


* **storeExternal**: 
A boolean value indicating whether the key should be stored externally.
This configuration option is required when connecting to the Utimaco HSM. Default value: `false`.


* **override**: 
An integer value indicating whether the key could be overridden in the future. `1` for allow and `0` for deny. Default value: `0`.


* **export**: 
An integer value indicating whether the key should be exportable from the HSM. `1` for allow and `0` for deny. Default value: `0`.


* **curve**: 
Key curve for the ECDSA key generation process (Utimaco specific notation). Default value: `NIST-P256`.


* **genMechanism**: 
An integer value defining the key generation mechanism.
This is the Utimaco specific configuration (see Utimaco docs for more details): `MECH_KEYGEN_UNCOMP` = `4` or `MECH_RND_REAL` = `0`.
Default value: 4.


* **includeIn**: 
List (either empty or containing a single item) of key store aliases corresponding to key stores in which this key is supposed to be generated.
In case of the HSM, the list is either empty or containing a single alias, as in case of the HSM keys there is no notion
of a key duplication across HSM key stores. If not specified the `defaultKeyStores` will be used.




## Key Configuration (Local)

Allowed parameters are:


* **alias**: 
Key alias under which the key is going to be stored. If not specified the key of the `certificates` map will be used. See above.


* **password**: 
Private key password. If not specified, the `defaultPassword` attribute is going to be used.
If the `defaultPassword` is not specified the `keyStore.password` will be used.


* **algorithm**: 
Corda signature scheme name. Default value: `ECDSA_SECP256R1_SHA256`. Allowed values are:


* `RSA_SHA256`
* `ECDSA_SECP256K1_SHA256`
* `ECDSA_SECP256R1_SHA256`
* `EDDSA_ED25519_SHA512`
* `SPHINCS-256_SHA512`


* **includeIn**: 
List of key store aliases corresponding to key stores in which the generated key needs to be stored.
If not specified the `defaultKeyStores` will be used.




## User Authentication Configuration

Allowed parameters are:


* **username**: 
HSM username. This user needs to be allowed to generate keys/certificates and store them in HSM.


* **mode**: 
One of the 3 possible authentication modes:



* `PASSWORD` - User’s password as set-up in the HSM.
* `CARD_READER` - Smart card reader authentication.
* `KEY_FILE` - Key file based authentication.



* **password**: 
Only relevant, if mode == `PASSWORD` or mode == `KEY_FILE`. It specifies either the password credential
for the associated user or the password to the key file, depending on the selected mode.
If not specified in the configuration file, it will be prompted on the command line.


* **keyFilePath**: 
Only relevant, if mode == `KEY_FILE`. It is the key file path.


* **device**: 
Only relevant, if mode == `CARD_READER`. It specifies the connection string to the card reader device.
Default value: `:cs2:auto:USB0`.



