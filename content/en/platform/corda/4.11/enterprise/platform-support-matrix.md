---
date: '2023-02-13'
menu:
  corda-enterprise-4-11:
    parent: about-corda-landing-4-11-enterprise
    name: Platform support
tags:
- platform
- support
- matrix
title: Corda Enterprise 4.11 platform support
weight: 250
---

# Platform support

This topic lists the JDKs, operating systems and database types that support Corda Enterprise Edition 4.11, both for production and for development. For the 'end of life schedule' for Corda versions and the associated documentation, refer to the [End of Life Schedule]({{< relref "../../eol-schedule.md" >}}).

## JDK support

Corda Enterprise Edition supports a subset of the platforms that are supported by [Java](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

### JDK support in production

Corda Enterprise Edition 4.11 has been tested and verified to work with **Oracle JDK 8 JVM 8u472** and **Azul Zulu Enterprise 8u471**, for Azure deployment downloadable from
[Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise Edition 4.11.

{{< warning >}}
In accordance with the [Oracle Java SE Support Roadmap](https://www.oracle.com/technetwork/java/java-se-support-roadmap.html),
which outlines the end of public updates of Java SE 8 for commercial use, please ensure you have the correct Java support contract in place
for your deployment needs.
{{< /warning >}}

### JDK support in development

The following JDKs support Corda for development purposes. Corda does not currently support Java 9 or higher.

{{< table >}}

| Supported JDKs                                                                   | Latest supported version |
|----------------------------------------------------------------------------------|--------------------------|
| [Oracle JDK](https://www.oracle.com/ie/java/technologies/downloads/)             | 8u472                    |
| [Amazon Corretto 8](https://aws.amazon.com/corretto/)                            | 8.252.09.1               |
| [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk/overview/)      | 8u322                    |
| [Zulu OpenJDK](https://www.azul.com/)                                            | 8u471                    |

{{< /table >}}

## Operating systems support

### Operating systems support in production

Production use of Corda Enterprise Edition 4.11 is only supported on Linux OS; see details below.

{{< table >}}

| Platform                      | CPU architecture | Versions             |
|-------------------------------|------------------|----------------------|
| Red Hat Enterprise Linux      | x86-64           | 8.x, 9.x, 10.x       |
| Suse Linux Enterprise Server  | x86-64           | 12.x, 11.x           |
| Ubuntu Linux                  | x86-64           | 20.04, 22.04, 24.04  |
| Oracle Linux                  | x86-64           | 7.x, 6.x             |

{{< /table >}}

### Operating systems support in development

The following operating systems can be used with Corda for development purposes.

{{< table >}}

| Platform                 | CPU architecture | Versions             |
|--------------------------|------------------|----------------------|
| Microsoft Windows        | x86-64           | 10, 8.x              |
| Microsoft Windows Server | x86-64           | 2016, 2012 R2, 2012  |
| Apple macOS              | x86-64           | 10.9 and above       |


{{< /table >}}

## Database support

The following database types are supported both in production and for development purposes.

### Node databases

{{< table >}}
| Vendor      | CPU architecture | Versions                                    | JDBC Driver                     |
|------------|-------------------|---------------------------------------------|---------------------------------|
| Microsoft  | x86-64            | Azure SQL, SQL Server 2022                  | Microsoft JDBC Driver 13.2.1    |
| Oracle     | x86-64            | 19c                                         | Oracle JDBC 6                   |
| Oracle     | x86-64            | 19c                                         | Oracle JDBC 8                   |
| Oracle     | x86-64            | 12cR2                                       | Oracle JDBC 8                   |
| Oracle     | x86-64            | 11gR2                                       | Oracle JDBC 6                   |
| Oracle     | x86-64            | 23ai (23.4)                                 | Oracle JDBC 8                   |
| PostgreSQL | x86-64            | 12.x, 13.x, 14.x, 15.x, 16.x, 17.x, 18.x ]  | PostgreSQL JDBC Driver 42.7.8   |


{{< /table >}}

### MySQL notary databases

{{< table >}}

| Vendor                                  | CPU Architecture | Versions | JDBC Driver              |
|-----------------------------------------|------------------|----------|--------------------------|
| Percona Server for MySQL *(deprecated)* | x86-64           | 5.7      | MySQL JDBC Driver 8.0.16 |


{{< /table >}}

### JPA notary databases

{{< table >}}

| Vendor      | CPU architecture | Versions        | JDBC Driver                  |
|-------------|------------------|-----------------|------------------------------|
| CockroachDB | x86-64           | 23.1.x, 24.1.x  | PostgreSQL JDBC Driver 42.5.0 |
| Oracle RAC  | x86-64           | 19c             | Oracle JDBC 8                |

{{< /table >}}

## Docker images

The Docker images used for the Kubernetes deployment are listed below for reference:

{{< table >}}
| Service           | Image name                                                  |
|-------------------|-------------------------------------------------------------|
| Identity Manager  | `corda/enterprise-identitymanager:1.6-zulu-openjdk8u392`  |
| Network Map       | `corda/enterprise-networkmap:1.6-zulu-openjdk8u392`       |
| Signing           | `corda/enterprise-signer:1.6-zulu-openjdk8u392`           |
| Zone              | `corda/enterprise-zone:1.6-zulu-openjdk8u392`             |
| Auth              | `corda/enterprise-auth:1.6-zulu-openjdk8u392`             |
| Gateway           | `corda/enterprise-gateway:1.6-zulu-openjdk8u392`          |
| PKI Tool          | `corda/enterprise-pkitool:1.6-zulu-openjdk8u392`          |
| Notary            | `corda/enterprise-notary:4.11.1-zulu-openjdk8u392`           |
{{< /table >}}


## Hardware Security Modules (HSM)

{{< table >}}

|Device                         | Legal identity and CA keys  | TLS keys                | Confidential identity keys | Notary service keys         |
|-------------------------------|--------------------------|--------------------------|----------------------------|-----------------------------|
| Utimaco SecurityServer Se Gen2| Firmware version 4.21.1  | Firmware version 4.21.1  | Firmware version 4.21.1    | Firmware version 4.21.1     |
|                               | Driver version 4.21.1    | Driver version 4.21.1    | Driver version 4.21.1      | Driver version 4.21.1       |
| Gemalto Luna (firmware)       | Firmware version 7.0.3   | Firmware version 7.0.3   | Firmware version 7.0.3     | Firmware version 7.0.3      |
| Gemalto Luna driver with Corda 4.9.6 and earlier, 4.10, 4.10.1, 4.10.2  | Driver version 7.3 | Driver version 7.3 | Driver version 7.3 | Driver version 7.3 |
| Gemalto Luna driver with Corda 4.9.7 and later versions of 4.9.*, 4.10.2 and later versions of 4.10.*, plus 4.11 | Driver version 10.4.0 | Driver version 10.4.0 | Driver version 10.4.0 | Driver version 10.4.0 |
| FutureX Vectera Plus          | Firmware version 6.1.5.8 | Firmware version 6.1.5.8 | Firmware version 6.1.5.8   | Firmware version 6.1.5.8    |
|                               | PKCS#11 version 3.1      | PKCS#11 version 3.1      | PKCS#11 version 3.1        | PKCS#11 version 3.1         |
|                               | FXJCA version 1.17       | FXJCA version 1.17       | FXJCA version 1.17         | FXJCA version 1.17          |
| Azure Key Vault               | Driver version           | Driver version           | Driver version (SOFTWARE mode only)| Driver version      |
|                               | azure-identity 1.2.0     | azure-identity 1.2.0     | azure-identity 1.2.0       | azure-identity 1.2.0        |
|                               | azure-security-keyvault-keys 4.2.3| azure-security-keyvault-keys 4.2.3| azure-security-keyvault-keys 4.2.3| azure-security-keyvault-keys 4.2.3|
| Securosys PrimusX             | Firmware version 2.7.4 or newer  | Firmware version 2.7.4 or newer | Firmware version 2.8.5 or newer   | Firmware version 2.7.4 or newer |
|                               | Driver version 1.8.2 or newer    | Driver version 1.8.2 or newer    | Driver version 2.3.4 or newer       | Driver version 1.8.2 or newer      |
| nCipher nShield Connect       | Firmware version 12.50.11| Firmware version 12.50.11| Firmware version 12.50.11  | Firmware version 12.50.11 |
|                               | Driver version 12.60.2   | Driver version 12.60.2   | Driver version 12.60.2     | Driver version 12.60.2    |
| AWS CloudHSM                  | Driver version 3.2.1     | Driver version 3.2.1     | Driver version 3.2.1       | Driver version 3.2.1      |

{{< /table >}}
