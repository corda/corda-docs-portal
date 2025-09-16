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

- This release introduces upgrades to the Java and Kotlin versions, along with associated upgrade support. In this release:
  - Java has been upgraded from Java 8 to **Java 17.0.16**
  - Kotlin has been upgraded from Kotlin 1.3.72 to **Kotlin 1.9.23**
- The PKI tool configuration file now has an optional `subjectAlternativeNames` field to add subject alternative names to certificates as a list. <!--ENT-13318 -->
- The PKI tool can now generate certificates and keys using all supported algorithms, including  RSA, ECDSA (secp256k1 and secp256r1) and EdDSA (Ed25519). <!--ENT-13741-->

### Fixed issues
 
- Fixed various issues related to CENM deployment using Docker, Kubernetes, and Helm charts. <!-- ENT-13988 and ENT-14010 -->
- Fixed an issue where an incorrect error message "No NETWORK_MAP type signing process set up" appeared when displaying unsigned network parameters data via the CENM tool. <!-- ENT-13920 -->
- The [shell Signing Service]({{< relref "shell.md#signing-service" >}}) `clientHealthCheck` health checks now work correctly across all service types. <!-- ENT-13897 -->
- Fixed an issue where setting `certificates.key.type` to `AZURE_MSAL_KEY_VAULT_HSM` in the PKI tool configuration file was generating an error. <!--ENT-13898 -->


### Upgraded dependencies

The following table lists the dependency version changes between CENM 1.6.3 and CENM 1.7:

  Dependency                                           | Name                              | CENM 1.6.3       | CENM 1.7
  -----------------------------------------------------|-----------------------------------|------------------|---------------
  com.azure:azure-identity                             | Azure Identity                    | 1.1.2            | 1.2.0
  com.azure:azure-security-keyvault-secrets            | Azure Key Vault Secrets           | 4.2.1            | 4.9.1
  com.bmuschko.docker-remote-api                       | Gradle Docker                     | 6.4.0            | 9.3.1
  com.fasterxml.jackson                                | Jackson Faster XML                | 2.17.2           | 2.18.3
  com.github.briandilley.jsonrpc4j                     | jsonrpc4j                         | 1.5.3            | 1.7
  com.github.dozermapper                               | Dozer Mapper                      | 6.5.0            | 7.0.0
  com.github.node-gradle.node                          | Gradle Node Plugin                | 1.3.1            | 2.2.4
  com.google.guava                                     | Guava                             | 32.1.1-jre       |  33.4.7-jre
  com.gradle.common-custom-user-data                   | Custom Gradle User Data           | 1.6.3            |  2.2.1
  com.gradle.enterprise                                | Gradle Enterprise Plugin          | 3.8.1            |  3.19.2
  com.h2database                                       | H2 Database                       | 2.2.224          |  2.3.232
  com.jcabi:jcabi-manifests                            | Jcabi Manifests                   | 1.1              |  2.1.0
  com.jcraft.jsch                                      | JSch                              | 0.1.55           |  0.2.25
  com.microsoft.azure.msal4j                           | MSAL4J                            | 1.7.1            |  1.20.1
  com.microsoft.sqlserver                              | SQL Server JDBC                   | 8.2.2.jre8       |  12.10.0.jre11
  com.nimbusds:nimbus-jose-jwt                         | Nimbus JOSE + JWT                 | 9.48             |  10.0.2
  com.postgresql                                       | PostgreSQL JDBC                   | 42.5.2           |  42.7.7
  com.squareup.okhttp3                                 | OkHttp                            | 4.8.0            |  4.12.0
  com.typesafe                                         | Typesafe Config                   | 1.4.0            |  1.4.3
  com.willowtreeapps.assertk                           | AssertK (JVM)                     | 0.21             |  0.28.1
  com.zaxxer.hikari                                    | HikariCP                          | 3.3.1            |  6.3.0
  commons-codec                                        | Apache Commons Codec              | 1.14             |  1.18.0
  info.picocli                                         | Picocli                           | 4.3.2            |  4.7.7
  io.gitlab.arturbosch.detekt                          | Detekt                            | 1.5.0            |  1.23.6
  io.netty                                             | Netty                             | 4.1.126.Final    |  4.1.127.Final
  io.netty:netty-tcnative                              | Netty TC Native                   | 2.0.48.Final     |  2.0.65.Final
  io.spring.dependency-management                      | Spring Dependency Management      | 1.0.10.RELEASE   |  1.1.0
  jakarta.el:jakarta.el-api                            | Jakarta EL API                    | 3.0.0            |  6.0.1
  net.bytebuddy                                        | Byte Buddy                        | 1.9.10           |  1.17.5
  org.apache.commons:commons-dbcp2                     | Apache Commons DBCP2              | 2.9.0            |  2.13.0
  org.apache.logging.log4j                             | Log4j                             | 2.17.1           |  2.25.1
  org.apache.sshd                                      | Apache SSHD Common                | 2.9.2            |  2.15.0
  org.apache.tomcat.ebmed                              | Apache Tomcat                     | 9.0.108          |  10.1.40
  org.assertj                                          | AssertJ                           | 3.12.2           |  3.27.3
  org.bouncycastle                                     | Bouncy Castle                     | 1.78.1           |  2.73.8
  org.eclipse.jetty                                    | Jetty                             | 9.4.58.v20250814 |  12.0.19
  org.glassfish:jakarta.el                             | Jakarta EL                        | 3.0.4            |  4.0.2
  org.glassfish.jersey                                 | Jersey                            | 2.25             |  3.1.10
  org.gradle.test-retry                                | Gradle Test Retry Plugin          | 1.4.0            |  1.6.2
  org.hibernate                                        | Hibernate ORM                     | 5.6.14.Final     |  6.0.2.Final
  org.hibernate.validator                              | Hibernate Validator               | 6.2.5.Final      |  8.0.2.Final
  org.jenkins-ci.plugins:artifactory                   | Artifactory Plugin                | 4.33.20          |  4.33.24
  org.jetbrains.dokka                                  | Dokka                             | 0.9.17           |  2.0.0
  org.jfrog.buildinfo:artifactory                      | Artifactory Plugin                | 4.33.20          |  4.33.24
  org.json                                             | JSON In Java                      | 20231013         |  20250107
  org.junit                                            | Junit                             | 5.6.2            |  5.11.4
  org.mockito                                          | Mockito                           | 3.1.0            |  5.17.0
  org.mockito.kotlin                                   | Mockito Kotlin                    | 2.2.0            |  5.4.0
  org.objenesis                                        | Objenesis                         | 2.6              |  3.4
  org.postgresql                                       | PostgreSQL JDBC                   | 42.5.2           |  42.7.3
  org.slf4j:slf4j-nop                                  | SLF4J NOP                         | 1.7.30           |  2.0.17
  org.springframework                                  | Spring Framework                  | 5.3.39.tuxcare.1 |  6.2.10
  org.springframework.boot                             | Spring Framework Boot             | 2.3.4.RELEASE    |  3.4.9
  org.springframework.cloud                            | Spring Framework Cloud Gateway    | 2.2.5.RELEASE    |  4.2.2
  org.springframework.security                         | Spring Framework Security         | 5.8.16.tuxcare   |  6.4.9
  org.springframework.security:spring-security-oauth2  | Spring Framework OAuth2 Security  | 2.5.2.RELEASE    |  6.4.3
  org.testcontainers                                   | Test Containers                   | 1.15.2           |  1.20.6
  org.yaml:snakeyaml                                   | Snake YAML                        | 2.3              |  2.4

* CENM now supports JDK Zulu 17.0.16 and Oracle 17.0.16.
* CENM now supports version 9.x of the Red Hat Enterprise Linux production operating system.
* CENM now supports Ubuntu Linux production operating system versions: 20.04, 22.04, 24.04.
* CENM now supports the following databases:
  * Microsoft version: SQL Server 2022
  * Oracle version: 23.4
  * PostgreSQL versions: 12.x, 13.x, 14.x, 15.x, 16.x
* CENM now supports the following node databases:
  * Microsoft version: SQL Server 2022
  * PostgreSQL versions: 12.x, 13.x, 14.x, 15.x, 16.x

For more information about CENM dependencies, see [CENM support matrix]({{< relref "cenm-support-matrix.md" >}}).