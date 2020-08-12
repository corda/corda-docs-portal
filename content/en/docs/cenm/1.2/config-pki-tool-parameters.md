---
aliases:
- /releases/release-1.2/config-pki-tool-parameters.html
- /docs/cenm/head/config-pki-tool-parameters.html
- /docs/cenm/config-pki-tool-parameters.html
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
Specification of the key stores used by the PKI Tool. It is a map of user-defined key store alias (for referencing
throughout the rest of the config) to key store configuration. See the below section on [Key Store Configuration](#key-store-configuration)
for the possible formats of these configurations.


* **certificatesStores**:
Specification of the local certificate stores used by the PKI Tool. It is a map of user-defined certificate store
alias (for referencing throughout the rest of the config) to certificate store config. Each certificate store
config takes the following form:


* **file**:
Certificate store file location. If the file does not exist it will be created automatically.


* **password**:
Certificate store password. If not specified, the `defaultPassword` attribute is going to be used.




* **defaultKeyStores**:
List of key store aliases corresponding to the key stores that are to store the generated keys in case of them not
being explicitly specified in the generated key configuration. This can be a list of multiple aliases only in case
of the local key stores. In case of the HSM key stores this list can hold only a single element corresponding to the
HSM key store. This is due to the fact that in case of the HSM key stores, there is no notion of a key duplication
to another HSM key store as the keys are generated in the HSM. That does not hold in case of local key stores, where
the keys are generated in memory and can be stored in an arbitrary number of file-based key stores.


* **defaultCertificatesStores**:
List of certificates store aliases corresponding to the certificates stores that are to store generated certificates
in case of them not being explicitly specified in the certificate configurations.


* **certificates**:
Map of user-defined certificate aliases to certificate configuration. The certificate alias serves two purposes.
Firstly, it can be used to reference the given entity throughout the rest of the PKI Tool config, for example in
another certificate config’s `signedBy` parameter. Secondly, it also defines the alias for the generated (or
existing) certificate entry in the corresponding certificate store. See the below section on
[Certificate Configuration](#certificate-configuration) for the format of this configuration.




## Key Store Configuration

The key store configuration defines the type of the underlying key store along with any type specific information. The
possible key store types are currently the same set as the possible key types. That is, `LOCAL`, `UTIMACO_HSM`,
`GEMALTO_HSM`, `SECUROSYS_HSM`, `AZURE_KEY_VAULT_HSM` or `AMAZON_CLOUD_HSM`.


### Local Key Store Configuration


* **type**:
Key store type. `LOCAL` in this case.


* **file**:
Path for the Java key store file. If no file exists then one will be created.


* **password**:
Password for the key store.




### Utimaco HSM Key Store Configuration


* **type**:
Key store type. `UTIMACO_HSM` in this case.


* **host**:
Host name (or IP address) of the Utimaco HSM device.


* **port**:
Port number of the Utimaco HSM service.


* **group**:
Key group for Utimaco HSM. This is a Utimaco HSM name spacing concept (see Utimaco docs for more information). Has
default value `PKI.TOOL.DEFAULT.HSM.GROUP`.


* **specifier**:
Key specifier for Utimaco HSM. This is a legacy Utimaco HSM name spacing concept (see Utimaco docs for more
information). Has default value `1`.


* **authThreshold**:
Authentication threshold configured on the Utimaco HSM (see Utimaco docs for more information).


* **users**:
List of user authentication configurations. See below section on User Authentication Configuration.




#### User Authentication Configuration

Each individual user authentication configuration will depend on the type of authentication that is being used. The
allowed parameters are:


* **username**:
HSM username. This user needs the appropriate permissions for key generation and storing.


* **mode**:
Currently, 3 authentication modes are supported:



* `PASSWORD` - User’s password as set-up in the HSM.
* `CARD_READER` - Smart card reader authentication.
* `KEY_FILE` - Key file based authentication.



* **password**:
Only relevant if mode is `PASSWORD` or mode is `KEY_FILE`. It specifies either the password credential for the
associated user or the password to the key file, depending on the selected mode. If not specified in the
configuration file, it will be prompted on the command line.


* **keyFilePath**:
Only relevant, if mode is `KEY_FILE`. It is the key file path.


* **device**:
Only relevant, if mode is `CARD_READER`. It specifies the connection string to the card reader device. Default
value is `:cs2:auto:USB0`.




### Gemalto HSM Key Store Configuration


* **type**:
Key store type. `GEMALTO_HSM` in this case.


* **user**:
User authentication credentials for the Gemalto HSM (note: this is a single value, not a list like other key store
configurations)


* **keyStore**:
Slot or partition of the HSM. E.g. “tokenlabel:<EXAMPLE_PARTITION_NAME>”


* **password**:
Password for the keyStore. E.g. the corresponding crypto officer role’s password. This can be omitted from the
configuration and input at runtime.






### Securosys HSM Key Store Configuration


* **type**:
Key store type. `SECUROSYS_HSM` in this case.


* **port**:
Port number of the Securosys HSM service.


* **users**:
List of user authentication configurations, formed of configurations with the below information:


* **username**:
HSM username. This user needs the appropriate permissions for key generation and storing.


* **password**:
Password associated with the user for the HSM. This can be omitted from the configuration and input at runtime.






### Azure Key Vault HSM Key Store Configuration


* **type**:
Key store type. `AZURE_KEY_VAULT_HSM` in this case.


* **keyVaultUrl**:
URL of the Azure Key Vault resource.


* **protection**:
Type of key protection to be used. This depends on the setup of the Azure Key Vault resource and can either be
`SOFTWARE`, corresponding to software-backed keys, or `HARDWARE`, corresponding to hardware-backed keys (via a
physical HSM).


* **credentials**:
The authentication credentials for the key vault. Currently, the only supported authentication method is via a
Service Principal and corresponding authentication key store.


* **keyStorePath**:
Path of the key store that contains the certificate and key pair of the Service Principal used to authenticate
against the key vault. Note that this file should be PKCS12 standard. One way of achieving this is by using
openssl to convert the Service Principal .pem file:

`openssl pkcs12 -export -in path/to/serviceprincipal.pem -out keyvault_login.p12`


* **keyStorePassword**:
Password of the key store.


* **keyStoreAlias**:
Alias of the Service Principal key entry within the key store.


* **clientId**:
ID of the client used during initial authentication.








### AWS CloudHSM Key Store Configuration

First of all AWS CloudHSM requires a UNIX client running on the machine. It will use that to connect to the HSM.
For detailed documentation about setting up the client please visit Amazon’s
[Getting Started with AWS CloudHSM](https://docs.aws.amazon.com/cloudhsm/latest/userguide/getting-started.html).
After the client is installed the shared library should be under the folder `/opt/cloudhsm/lib` so this should be
used when configuring the `hsmLibraries` property in the config. The jar can be found under `/opt/cloudhsm/java/cloudhsm-<version>.jar`
by default.


* **type**:
Key store type. `AMAZON_CLOUD_HSM` in this case.


* **credentialsAmazon**:
The credentials for logging in to the HSM.


* **partition**:
Partition for the HSM. This can be found in the AWS console.


* **userName**:
An existing CU type user in the HSM.


* **password**:
Password for the given CU account.




* **localCertificateStore**:
must be used.
* **file**:
The location of the local certificate store. This will be created if it does not exist.


* **password**:
The password for the local certificate store






## Certificate Configuration

The certificate configuration is specific to a particular entity within the hierarchy and defines all properties and
extensions for its X509 certificate as well as its key pair.


* **key**:
Configuration of the key pair for the entity. Similarly to the key store configuration above, this can either be
local, or one of the supported HSMs. See below section of [Key Configuration](#key-configuration) for the possible formats of this
configuration.


* **signedBy**:
The alias of the parent entity that signs this certificate, which should correspond with a key in the top-level
`certificates` map. If the certificate is self-signed (indicated by `isSelfSigned=true`) then this is not
required.


* **isSelfSigned**:
Flag denoting whether this certificate is self-signed. Setting this to true allows the omission of the `signedBy`
parameter above. If the `signedBy` parameter is included then this should not be provided.


* **includeIn**:
List of certificate store aliases, representing where the generated certificate should be stored. If not specified
the `defaultCertificatesStores` list will be used.


* **validDays**:
The number of days until this certificate expires. Default value: `7300`.


* **subject**:
X500 name of the entity owning the key.


* **role**:
Role of the certificate, embedded into the generated X509 certificate via the Corda specific role extension. The
allowed values are `DOORMAN_CA`, `NETWORK_MAP` or `NETWORK_PARAMETERS`. This parameter is optional. Omitting
it will result in the certificate being generated without a role extension.


* **keyUsages**:
Possible usages of the keys associated with the certificate (Optional). This is an array of values from the
following set:



* `DIGITAL_SIGNATURE`
* `NON_REPUDIATION`
* `KEY_ENCIPHERMENT`
* `DATA_ENCIPHERMENT`
* `KEY_AGREEMENT`
* `KEY_CERT_SIGN`
* `CRL_SIGN`
* `ENCIPHER_ONLY`
* `DECIPHER_ONLY`


Default value: [`DIGITAL_SIGNATURE`, `KEY_CERT_SIGN`, `CRL_SIGN`].


* **keyPurposes**:
Possible extended usages of the keys associated with the certificate (Optional). This is an array of values from the
following set:



* `ANY_EXTENDED_KEY_USAGE`
* `SERVER_AUTH`
* `CLIENT_AUTH`
* `CODE_SIGNING`
* `EMAIL_PROTECTION`
* `IPSEC_END_SYSTEM`
* `IPSEC_TUNNEL`
* `IPSEC_USER`
* `IPSEC_TIME_STAMPING`
* `OCSP_SIGNING`
* `DVCS`
* `SBGP_CERT_A_A_SERVER_AUTH`
* `SCVP_RESPONDER`
* `EAP_OVER_PPP`
* `EAP_OVER_LAN`
* `SCVP_SERVER`
* `SCVP_CLIENT`
* `IPSEC_IKE`
* `CAPWAP_AC`
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




* **crl**:
Certificate revocation list specific configuration.


* **validDays**:
Validity period of the certificate revocation list. Default value: `3650`.


* **crlDistributionUrl**:
Certificate revocation list distribution URL.


* **indirectIssuer**:
Flag denoting whether the generated certificate revocation list is intended to be used as the CRL for another
CA. This information is baked into the CRL via the `indirectCRL` flag inside the
`Issuing Distribution Point` extension. Has a default value of `false`, meaning that the generated CRL is
intended to be used as the CRL for all certificates issued by the current entity.


* **issuer**:
The issuer (given in the X500 name format) that should be included in the `Issuing Distribution Point` CRL
extension. Only applicable if the `indirectIssuer` is set to true above, in which case this must be set to the
same value as the entity’s subject.


* **file**:
Location of the file where the encoded bytes of the certificate revocation list are to be stored.


* **revocations**:
List of revocation data (Optional). Each entry in the list should take the following format:


* **certificateSerialNumber**:
Serial number of the revoked certificate.


* **dateInMillis**:
Certificate revocation time.


* **reason**:
Reason for the certificate revocation. The allowed value is one of the following:



* `KEY_COMPROMISE`
* `CA_COMPROMISE`
* `AFFILIATION_CHANGED`
* `SUPERSEDED`
* `CESSATION_OF_OPERATION`
* `PRIVILEGE_WITHDRAWN`







* **crlDistributionUrl**:
Certificate revocation list distribution URL. This parameter is optional and takes precedence over the default
behaviour of taking the value from the parent entity’s CRL information. This parameter can be used to specify the
CRL endpoints without having to configure or generate a CRL file.


* **crlIssuer**:
Certificate revocation list issuer (given in the X500 name format). This parameter is optional and takes precedence
over the default behaviour of taking the value from the parent entity’s CRL information. This parameter can be used
to specify the CRL endpoints without having to configure or generate a CRL file.




### Key Configuration

The key configuration defines the properties of the key pair associated with the entity. This key pair can be generated
(or already exist) in either a local key store or a supported HSM. Similar to the key store configuration above, each
key configuration has an associated type, with possible values: `LOCAL`, `UTIMACO_HSM`, `GEMALTO_HSM`,
`SECUROSYS_HSM`, `AZURE_KEY_VAULT_HSM` or `AMAZON_CLOUD_HSM`.


#### Local Key Configuration


* **type**:
Key type. `LOCAL` in this case.


* **alias**:
Alias under which the key is going to be stored. If not specified the key of the `certificates` map will be used.


* **includeIn**:
List of key store aliases corresponding to key stores in which the generated key needs to be stored. If not
specified the `defaultKeyStores` will be used.


* **password**:
Password for the key entry within the defined key store. If not specified, the `defaultPassword` attribute will be
used.


* **algorithm**:
Corda signature scheme name. Default value: `ECDSA_SECP256R1_SHA256`. Allowed values are:



* `RSA_SHA256`
* `ECDSA_SECP256K1_SHA256`
* `ECDSA_SECP256R1_SHA256`
* `EDDSA_ED25519_SHA512`
* `SPHINCS-256_SHA512`





#### Utimaco HSM Key Configuration


* **type**:
Key type. `UTIMACO_HSM` in this case.


* **alias**:
Alias under which the key is going to be stored. If not specified the key of the *certificates* map will be used.


* **includeIn**:
List (either empty or containing a single item) of key store aliases corresponding to key stores in which this key
is should be generated (or already exist). In case of a HSM, the list is either empty or containing a single alias,
as in case of the HSM keys there is no notion of a key duplication across HSM key stores. If not specified the
`defaultKeyStores` will be used.


* **storeExternal**:
Boolean flag indicating whether the key should be stored externally. This configuration option is required when
connecting to the Utimaco HSM. Has default value `false`.


* **override**:
Boolean flag indicating whether the key could be overridden in the future. Has default value `false`.


* **export**:
Boolean flag indicating whether the key should be exportable from the HSM. Has default value `false`.


* **curve**:
Key curve for the ECDSA key generation process (Utimaco specific notation). Default value: `NIST-P256`.


* **genMechanism**:
An integer value defining the key generation mechanism. This is a Utimaco specific configuration option (see Utimaco
docs for more information). Suggest options are `MECH_KEYGEN_UNCOMP` = `4` or `MECH_RND_REAL` = `0`. Has
default value `4`.




#### Other HSM Key Configurations

The remaining HSM key configurations follow the similar format:


* **type**:
Key type. `GEMALTO_HSM`, `SECUROSYS_HSM`, `AZURE_KEY_VAULT_HSM` or `AMAZON_CLOUD_HSM` in this case.


* **alias**:
Alias under which the key is going to be stored. If not specified the key of the *certificates* map will be used.


* **includeIn**:
List (either empty or containing a single item) of key store aliases corresponding to key stores in which this key
is should be generated (or already exist). In case of a HSM, the list is either empty or containing a single alias,
as in case of the HSM keys there is no notion of a key duplication across HSM key stores. If not specified the
`defaultKeyStores` will be used.


* **curve**:
The standard name for the elliptic curve that should be used to generate the key pair. Has default value of
`secp256r1`. See documentation for `ECGenParameterSpec` Java class for more information.
