---
date: '2023-09-12'
menu:
  cenm-1-7:
    identifier: cenm-1-7-release-notes
    parent: cenm-1-7-cenm-releases
    weight: 80
tags:
- cenm
- release
- notes
title: Release notes
---

# Corda Enterprise Network Manager release notes

## Corda Enterprise Network Manager 1.7

### New features and enhancements

- The PKI tool configuration file now has an optional `subjectAlternativeNames` field to add subject alternative names to certificates as a list. <!--ENT-13318 -->
- The PKI tool can now generate certificates and keys using all supported algorithms, including  RSA, ECDSA (secp256k1 and secp256r1) and EdDSA (Ed25519). <!--ENT-13741-->

### Fixed issues
 
- Fixed various issues related to CENM deployment using Docker, Kubernetes, and Helm charts. <!-- ENT-13988 and ENT-14010 -->
- Fixed an issue where an incorrect error message "No NETWORK_MAP type signing process set up" appeared when displaying unsigned network parameters data via the CENM tool. <!-- ENT-13920 -->
- The [shell Signing Service]({{< relref "shell.md#signing-service" >}}) `clientHealthCheck` health checks now work correctly across all service types. <!-- ENT-13897 -->
- Fixed an issue where setting `certificates.key.type` to `AZURE_MSAL_KEY_VAULT_HSM` in the PKI tool configuration file was generating an error. <!--ENT-13898 -->


### Upgraded dependencies

The following table lists the dependency version changes between CENM 1.6.2 and CENM 1.7:

NEED TO UPDATE

| Dependency                                                | Name                       | CENM 1.6.3       | CENM 1.7    |
|-----------------------------------------------------------|----------------------------|----------------|---------------|
| org.bouncycastle                                          | Bouncy Castle              | 1.75           | 1.78.1        |
| org.springframework.security.oauth:spring-security-oauth2 | Spring Security            | 2.5.0.RELEASE  | 2.5.2.RELEASE |
| org.springframework:spring-*                              | Spring Framework           | 5.3.27         | 5.3.39        |
| org.springframework.security:*                            | Spring Framework Security  | 5.5.8          | 5.8.16        |
| com.nimbusds:nimbus-jose-jwt                              | Nimbus JOSE+JWT            | 8.19           | 9.48          |
| com.fasterxml.jackson.core:*                              | Jackson                    | 2.14.2         | 2.18.2        |
| io.projectreactor:reactor-core	                           | Project Reactor Core	      | 3.4.11	        | 3.4.41        |
| org.apache.tomcat.embed:tomcat-embed-*	                   | Apache Tomcat	             | 9.0.81	        | 9.0.98        |
| org.yaml:snakeyaml	                                       | Snake YAML	                | 1.33	          | 2.3           |
| commons-io:commons-io	                                    | Apache Commons IO	         | 2.11.0	        | 2.18.0        |
| info.picocli:picocli	                                     | PicoCLI	                   | 3.9.6	         | 4.1.4         |
| com.typesafe:config	                                      | Typesafe Config		          | 1.3.4	         | 1.4.0         |
| org.testcontainers:testcontainers	                        | TestContainers	            | 1.14.3	        | 1.15.2        |
| org.mockito.kotlin:mockito-kotlin		                       | Mockito Kotlin	            | 2.0.0-alpha01	 | 2.2.0         |
| org.junit.jupiter:junit-jupiter-api		                     | JUnit Jupiter API	         | 5.6.1	         | 5.6.2         |
| commons-codec:commons-codec		                             | Apache Commons Codec	      | 1.13           | 1.14          |

* CENM now supports JDK Azul 8u422 and Oracle JDK 8u421.
* CENM now supports version 9.x of the Red Hat Enterprise Linux production operating system.
* CENM now supports Ubuntu Linux production operating system versions 20.04, 22.04, 24.04.
* CENM now supports the following databases:
  * Microsoft version: SQL Server 2022.
  * Oracle version: 23.4.
  * PostgreSQL versions: 12.19, 13.3, 13.15, 14.12, 15.7, 16.3.
* CENM now supports the following node databases:
  * Microsoft version: SQL Server 2022.
  * PostgreSQL versions: 12.19, 13.3, 13.15, 14.12, 15.7, 16.3.

For more information about CENM dependencies, see [CENM support matrix]({{< relref "cenm-support-matrix.md" >}}).